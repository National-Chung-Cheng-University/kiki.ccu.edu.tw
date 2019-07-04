<?PHP
//////////////////////////////////////////////////////////////////////////////////////////
/////  Withdrawal_Form_Apply2.php
/////  學生申請科目棄選
/////  動態產生 PDF 文件，供學生列印
/////  Updates:
/////    2013/04/15 從 Concent_Form_Apply2.php 加簽申請功能改來。 Nidalap :D~
/////    2013/12/02 加入判斷系統設定的 redirect_to_query 設定，判別是否抓上學期課程資料。 by Nidalap :D~

include "../library/Reference.php";
include $LIBRARY_PATH . "Error_Message.php";
include $LIBRARY_PATH . "Common_Utility.php";
//include $LIBRARY_PATH . "System_Settings.php";
include $LIBRARY_PATH . "Session.php";
include $LIBRARY_PATH . "Student.php";
require_once $LIBRARY_PATH . "Dept.php";
require_once $LIBRARY_PATH . "Course.php";
require_once $LIBRARY_PATH . "Student_Course.php";
require_once $LIBRARY_PATH . "Teacher.php";
require_once $LIBRARY_PATH . "Database.php";
require_once $LIBRARY_PATH . "English.php";
//require_once $LIBRARY_PATH . "fpdf17/chinese.php";
define("FPDF_FONTPATH",$LIBRARY_PATH."fpdf17/font/");
require_once $LIBRARY_PATH . "fpdf17/chinese-unicode.php";

$system_settings = Get_System_State();
if( $system_settings['redirect_to_query'] == 1 ) {			///  抓上學期開課選課資料
  list($year, $term) = Last_Semester(1);  
}else{														///  抓本學期開課選課資料
  $year = $YEAR;
  $term = $TERM;
}

session_start();
$DBH = PDO_connect($DATABASE_NAME);

$session_id     = quotes($_SESSION["session_id"]);
$dept		= quotes($_SESSION["dept"]);	///  本科目開課系所, 非學生所屬系所
$cid            = quotes($_SESSION["cid"]);
$grp            = quotes($_SESSION["grp"]);

//if( $IS_ENGLISH ) die("english!");

$system_settings = Get_System_State();

//$course_time_string = Format_Time_String($course{"time"});

$session = Read_Session($session_id);
Renew_Session($session_id);
$stu = Read_Student($session["id"]);
$dept_data = Read_Dept($stu["dept"]);
$all_teachers = Read_All_Teacher();  
$course = Read_Course($dept, $cid, $grp, $year, $term);
$course_of_student = Course_of_Student($stu["id"], $year, $term);

//$student_in_course = Student_in_Course($cid, $grp);
//$student_count = sizeof($student_in_course);
//$stu_grade = Read_Grade_From_DB($stu["id"]);

if( array_key_exists("SUPERUSER", $_SESSION) and $_SESSION["SUPERUSER"] )  
        $SUPERUSER = $_SESSION["SUPERUSER"];

//foreach($grade as $g) {
//  print_r($g);
//}
//$stu_grade = Read_Grade_From_DB($stu["id"]);    ///  抓學生的成績
//print_r($stu_grade);

/////  判別學生是否可申請棄選此科目
list($withdrawal_form_allowed, $wf_msg)	= Apply_Form_Allowed("withdrawal");		//  條件1：目前是否允許申請棄選
if( $withdrawal_form_allowed == 1 ) {
  $withdrawal_form_allowed = 0;
  foreach ( $course_of_student as $cou ) {										//  條件2：此科目為學生所選科目之一
//    echo "[$cid, $grp] <-> [" . $cou['id'] . $cou['group'] . "]<BR>\n";
    if( ($cou['id'] == $cid) and ($cou['group'] == $grp) )   $withdrawal_form_allowed = 1;
  }
}

if( $withdrawal_form_allowed == 0 ) {
  $message = "目前並非棄選時段，或您本學期沒有加選修過此課程，請勿申請棄選！";
  $back_text = "我要回上頁";
  Student_Log("Withdrawal_No_Need", $stu["id"], $cid, $grp, "", "SELF");
  echo "您無需申請棄選!";
}else{
  $DBH = PDO_connect();
  $apply_data = Withdrawal_Form_Apply_Status($stu["id"], "", $year, $term);
 
  if( $apply_data == -1 ) {														/// 若尚未申請過：新增此棄選資料
    Withdrawal_Form_Stu_Apply($stu["id"], $cid, $grp);
    Student_Log("Apply_Withdrawal", $stu["id"], $cid, $grp, "", "SELF");
  }else if( ($course['id'] == $apply_data['course_id']) and ($course['group'] == $apply_data['grp']) ) {
																				/// 若早已申請過：重新列印
    Student_Log("View_Withdrawal", $stu["id"], $cid, $grp, "", "SELF");  
  }else{																		/// 若早已申請過其他科目
    //$old_apply_data = Withdrawal_Form_Apply_Status($stu["id"], );
	if( $apply_data['verified'] == 'v' ) {										///   若舊申請的早已核可：拒絕棄選！
	  echo "您的另一張棄選單(科目代碼" . $apply_data['cid'] 
	       . ", 班別 " . $apply_data['grp'] . ")已通過，請勿再申請新的棄選單！";
	  exit();
	}else{																		///   若舊申請的尚未核可：刪除舊資料並新增此棄選資料
	  Withdrawal_Form_Stu_Abandon($stu["id"], $apply_data["course_id"], $apply_data["grp"]);
	  Withdrawal_Form_Stu_Apply($stu["id"], $cid, $grp);
	  Student_Log("Abandon_Withdrawal", $stu["id"], $apply_data["course_id"], $apply_data["grp"], "", "SELF");
	  Student_Log("Apply_Withdrawal", $stu["id"], $cid, $grp, "", "SELF");
	}
  }
  ob_clean();
  $DBH = PDO_connect($DATABASE_NAME);
  Create_PDF();
}


///////////////////////////////////////////////////////////////////////////////////////////
/////  透過 fpdf 函式庫動態產生棄選單 PDF 檔案供列印

function Create_PDF()
{
  global $LIBRARY_PATH;
  global $YEAR,$TERM,$GRAPH_URL, $DEPT_CGE, $PROPERTY_TABLE;
  global $system_settings, $course, $course_time_string, $dept, $cid, $dept_data, $stu, $course_of_student;
  global $form_create_time, $ban_reasons, $apply_data, $year, $term;
  
  list($now1, $now2, $now3) = gettime("");
//  $now2 = preg_replace("/:\d*$/", "", $now2);

  if( $apply_data == -1 ) {			///  新申請
    //$form_sn = Get_Form_Max_Serialno($course["id"], $course["group"], "withdrawal") + 1;
    $form_create_time = $now2;
  }else{					///  抓取舊資料
    //$form_sn		= $apply_data["serialno"];
    $form_create_time	= $apply_data["apply_time"];    
  }
//  if( $form_sn == NULL )		$form_sn = 1;
//  if( $form_create_time == NULL )	$form_create_time = $now2;
  $form_create_time_display = preg_replace("/:/", ": ", $form_create_time);

  $font_title	= 20;
  $font_big		= 16;
  $font_medium	= 14;
  $font_small	= 12;
  //$font_small	= $font_medium;

  $height		= 6;
  $width["indent"]	= 10;
  $width["cid"]		= 27;
  $width["group"]	= 10;
  $width["time"]	= 35;
  $width["cname"]	= 105;
  $width["credit"]	= 15;
  $width["property"]= 20;

//  $cou["id"]	= $_SESSION["cid"];
//  $cou["group"]	= $_SESSION["grp"];
//  $cou["cname"]	= "超級電子學三";
  //$stu_grade = Read_Grade_From_DB($stu["id"]);
/*
  $pdf=new PDF_Chinese();

  $pdf->SetAuthor("National Chung Cheng University");
  $pdf->SetSubject("Course Registration Consent Form");
  $pdf->SetTitle("Course Registration Consent Form");

  $pdf->AddBig5Font("font1","標楷體");
  $pdf->Open();
  $pdf->AddPage();
  $pdf->SetAutoPageBreak(0);
*/
  $pdf=new PDF_Unicode();
  //$pdf=new PDF_Code39();
  
  $pdf->FPDF ('P', 'mm', 'A4');  //P 直式，L 橫式
  $pdf->SetAuthor("National Chung Cheng University");
  $pdf->SetSubject("Course Registration Withdrawal Form");
  $pdf->SetTitle("Course Registration Withdrawal Form");
//  $pdf->AddUniCNShwFont("uni");
  $pdf->AddUniCNShwFont('font1','DFKaiShu-SB-Estd-BF'); 

  //$pdf->AddBig5Font("font1","標楷體");
//  $pdf->AddBig5Font("font1","uniKai");
  $pdf->Open();
  $pdf->AddPage();
  $pdf->SetAutoPageBreak(0);
//  SetCreator

  /////  標題 HEADER
  $x_emblem = 15;
  $y_emblem = 5;
  $pdf->SetX($x_emblem);
  $pdf->SetY($y_emblem);
  $emblem = $GRAPH_URL . "emblem.jpg";   
  $pdf->Image($emblem,$x_emblem,$y_emblem,"","","JPEG");
          
  $pdf->SetFont("font1","B",$font_title);
  $title = "國立中正大學 " . $year . " 學年度第 " . $term . " 學期  棄選申請單";
  $pdf->Cell($x_emblem,3, "");
  $pdf->Cell(0,$height*3,$title,0,1,"C"); 

  /////  加入3of9 barcode(學號)
  //$pdf->AddFont("barcode", "","3of9.php");  
  //$pdf->SetFont("barcode", "", 25);  
  //$pdf->Cell(37,$height,"*".$stu["id"]."*",0,1,"L");
  $pdf->Code39(162,28,$stu["id"], 0.7,7);			/// 第4~5個參數設定 barcode 大小  

  /////  學生個人資料 & 表單序號、申請時間
  $pdf->SetFont("font1","",$font_medium);
  $stu_info[0]	= "系所：" . $dept_data["cname2"];
  $stu_info[1]	= "年級/班別：" . $stu["grade"] . $stu["class"];
  //$stu_info[4]	= "班級：" . $stu["class"];
  $stu_info[3]	= "學號：" . $stu["id"];
  $stu_info[2]	= "姓名：" . $stu["name"];
  //$stu_info_w   = array(37,37,37,25,25);
  $stu_info_w   = array(100,100,100,100);
  
  for( $i=0; $i<sizeof($stu_info); $i++ ) {
    if( ($i==sizeof($stu_info)/2-1) or ($i==sizeof($stu_info)-1) )  {
      $pdf->Cell($stu_info_w[$i],$height,$stu_info[$i],0,1,"L");
    }else{
	  $pdf->Cell($width["indent"],$height,"");
      $pdf->Cell($stu_info_w[$i],$height,$stu_info[$i],0,0,"L");
	}
  }

  $pdf->SetFont("font1","",$font_small);  
  //$sn_and_print_time = "棄選單序號：$form_sn   申請時間：" . $form_create_time_display;
  //$pdf->Cell(0,$height,$sn_and_print_time,"", "", "R");

  /////  棄選科目資料
  $pdf->Ln($height+2);
  $pdf->SetFont("font1","B",$font_small);
  $pdf->SetFillColor(200);
  $pdf->Cell($width["indent"],$height,"");
  $pdf->Cell($width["cid"],$height,"科目編號",1,0,"C",1);
  $pdf->Cell($width["group"],$height,"班別",1,0,"C",1);  
  $pdf->Cell($width["cname"],$height,"科目名稱",1,0,"C",1);
  $pdf->Cell($width["credit"],$height,"學分",1,0,"C",1);
  $pdf->Cell($width["property"],$height,"學分歸屬",1,1,"C",1);
  
  $pdf->SetFont("font1","",$font_small);
  $pdf->Cell($width["indent"],$height,"");
  $pdf->Cell($width["cid"],$height,$course["id"],1,0,"C");
  $pdf->Cell($width["group"],$height,$course["group"],1,0,"C");
  $pdf->Cell($width["cname"],$height,$course["cname"],1,0,"C");
  $pdf->Cell($width["credit"],$height,$course["credit"],1,0,"C");
  $pdf->Cell($width["property"],$height,$PROPERTY_TABLE[$course["property"]],1,1,"C");

  /////  、系統擋修原因、棄選原因等(主要 table)
//  $ban_reason = "1. 太笨太笨太笨太笨太笨太笨太笨太笨!!! 還是太笨！！\n";
//  $ban_reason .= "2. 俺不想這個學生選！ 凸-_-\n";
//  $ban_reason .= "3. 此科目限修 60 人，限修人數尚未額滿。\n";
//  $ban_reason .= "4. 因為我家隔壁的母貓生了一窩小貓。";
  //$ban_reason_line_count  = 5;			///  系統擋修原因可以放的行數
  //$ban_line_reduct = 0;			///  因擋修原因超過一行，必須減少「系統擋修原因」Cell 的高度
  $line_break = 72;				///  一行內若有這麼多個字元則會折行

  /////  棄選理由(學生填寫)
  $pdf->Cell($width["indent"],$height,"");
  $pdf->Cell($width["cid"],$height*4,"棄選理由",1,0,"C");
  $pdf->Cell($width["group"]+$width["time"]+$width["cname"],$height*4,"",1,1,"C");

  /////  任課教師簽名
  $teacher_str = Format_Teacher_String($course["teacher"]);
  $teacher_fill =  "(" . $teacher_str . ")";
  $pdf->Cell($width["indent"],$height*2,"");
  $pdf->Cell($width["cid"],$height*4,"任課教師簽名",1,0,"C");
  $pdf->MultiCell($width["group"]+$width["time"]+$width["cname"],$height*4,$teacher_fill,1,"L");

  /////  學生聯絡電話
  $pdf->Cell($width["indent"],$height*2,"");
  $pdf->Cell($width["cid"],$height*2,"學生聯絡電話",1,0,"C");
  $pdf->MultiCell($width["group"]+$width["time"]+$width["cname"],$height*2,"",1,"L");  

  /////  (本學期)總學分數
  $total_credit = 0;
  foreach ($course_of_student as $cos) {
    $total_credit += $cos['credit'];
  }
  
  $pdf->SetFont("font1","",$font_medium);
  $pdf->Cell($width["indent"],$height+3,"", 0,1,"L");	///  表格下要有 $height+3 空白
  $pdf->Cell($width["indent"],$height+5);
  $pdf->Cell($width["cid"],$height+5,"本學期原修習總學分數： " . $total_credit,0,1,"L");
  $pdf->Cell($width["indent"],$height+5,"");
  $pdf->Cell($width["cid"],$height+5,"            棄選後總學分數： " . ($total_credit - $course['credit']),0,1,"L");
  $pdf->Cell($width["indent"]+$width["cid"]-10,$height,"");
  
  /////  回執聯切割線
  $x_scissor = 10;
  $y_scissor = 180;
  $pdf->SetX($x_scissor);
  $pdf->SetY($y_scissor);
  $scissor = $GRAPH_URL . "scissor.jpg";
//  $pdf->Cell(1,1,$scissor,0,1);
  $pdf->Image($scissor,$x_scissor,$y_scissor,"","","JPEG");
  $pdf->SetFontSize(6);
  $dash = "       ";
  for ($j=0;$j<175;$j++)  $dash .= ". ";
  $pdf->Cell(1,1,$dash,0,1);

  /////  學生存根聯
  $cou_info[0] = "科目編號：" . $course["id"];
  $cou_info[1] = "班別：" . $course["group"];
  $cou_info[2] = "時間：" . $course_time_string;
  $cou_info[3] = "科目名稱：" . $course["cname"];

  $form_info[0] = "棄選單序號：" . $form_sn;
  $form_info[1] = "申請時間：" . $form_create_time_display;

  $width["stu"] = 40;
  $pdf->SetFont("font1","U",$font_big);
  
  $pdf->Cell($width["indent"],$height,"",0,1);
  $pdf->Cell(37,$height+2,"學生存根聯",0,1);
  /////  加入3of9 barcode(學號)
  //$pdf->AddFont("barcode", "","3of9.php");
  //$pdf->SetFont("barcode", "", 25);
  //$pdf->Cell(37,$height+5,"*".$stu["id"]."*",0,1,"L");
  $pdf->Code39(40,186,$stu["id"], 0.7,7);			/// 第4~5個參數設定 barcode 大小  

  $pdf->SetFont("font1","",$font_small);
  $pdf->Cell($width["indent"],$height,"");
  $pdf->Cell($width["stu"],$height,$stu_info[0],0);	///  學生相關資料
  $pdf->Cell($width["stu"],$height,$stu_info[1],0);
  $pdf->Cell($width["stu"],$height,$stu_info[2],0);
  $pdf->Cell($width["stu"],$height,$stu_info[3],0,1);
  
  $pdf->Cell($width["indent"],$height,"");  
  $pdf->Cell($width["stu"],$height,$cou_info[0],0);	///  科目相關資料
  $pdf->Cell($width["stu"]-10,$height,$cou_info[1],0,1);
  //$pdf->Cell($width["stu"]-10,$height,$cou_info[2],0);
  $pdf->Cell($width["indent"],$height,"");  
  $pdf->Cell($width["stu"],$height,$cou_info[3],0,1);
//  $pdf->Cell($width["indent"],$height,"");
//  $pdf->Cell($width["stu"],$height,$form_info[0],0);        ///  棄選單相關資料
//  $pdf->Cell($width["stu"],$height,$form_info[1],0,1);

  /////  注意事項
  $note[] = "本申請表需由學生本人攜帶有照片之身份證件親自辦理，學生申請"
			. "棄選應於期中考後，最遲依行事曆所訂日期前送交教學組（本學期"
			. "棄選截止日是 "
			//. preg_replace("/^...../", "", $system_settings["withdrawal_form_end"]) 
			. $system_settings["withdrawal_form_end"]
            . "），始完成申請之手續。\n";
  $note[] = "棄選科目每學期以一科為限。";
  $note[] = "學士班當學期修習學分數低於八學分（含）者，不得辦理棄選，碩博士同學不在此限。";
  //$note[] = "請檢附當學期選課結果單。";
  $note[] = "請於棄選截止日後上教務系統->資料查詢->成績資料查詢，查詢課程是否註記棄選。";

  $pdf->SetFont("font1","U",$font_big);
  $pdf->Cell(0,$height+5,"注意事項",0,1);
  $pdf->SetFont("font1","",$font_small);
  $i=0;
  foreach( $note as $n ) { 
    $n = 1+$i . ". " . $n;
    $pdf->MultiCell(0,$height,$n,0);
    if( $i == 0 ) {
      $x_note0 = $pdf->GetX();
      $y_note0 = $pdf->GetY();
    }
    $i++;
  }
/*
  $x = 0; //10.5;
  $y = $y_scissor + 46; //241;
  $pdf->Line($x+49,$y,$x+128,$y);			/// 注意事項底線
  $pdf->Line($x+23.5,$y+$height,$x+94,$y+$height);
  $pdf->Line($x+145,$y+$height,$x+187.5,$y+$height);


  $pdf->SetTextColor(255,0,0);   			/// 注意事項一的粗體字
  $note0 = "";
  for( $i=0; $i<=125; $i++ ) $note0 .= " ";
  $note0 .= "未上網選課者加簽無效";
  $pdf->SetX($x_note0);
  $pdf->SetY($y_note0 - $height + 0.1);
  $pdf->Cell(0, $height,$note0, 0,1);
*/


  $pdf->Output();
}

?>