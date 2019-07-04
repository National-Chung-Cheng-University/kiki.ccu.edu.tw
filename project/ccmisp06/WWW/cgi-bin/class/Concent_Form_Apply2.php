<?PHP
//////////////////////////////////////////////////////////////////////////////////////////
/////  Concent_Form_Apply2.php
/////  學生申請科目加簽
/////  動態產生 PDF 文件，供學生列印
/////  Updates:
/////   2010/08/02 Created by Nidalap :D~
/////   2012/02/15 加入學號 barcode，以方便管理者輸入資料。  Nidalap :D~
/////   2012/11/05 改採 PDO 連線資料庫 by Nidalap :D~
/////	2013/09/05 修正因 Sybase->PostgreSQL 而不能執行的部份，以及 PDF 排版跑掉微調 Nidalap :D~
/////   2016/09/09 因應通識中心政策改變，針對通識移除部分欄位，以及修改部分注意事項 Nidalap :D~
/////   2016/09/20 新增加簽原因：輔系、雙主修、客製化學程。 by Nidalap :D~

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
require_once $LIBRARY_PATH . "Grade.php";
define("FPDF_FONTPATH",$LIBRARY_PATH."fpdf17/font/");
require_once $LIBRARY_PATH . "fpdf17/chinese-unicode.php";
//require_once $LIBRARY_PATH . "fpdf17/fpdf.php";
//require_once $LIBRARY_PATH . "fpdf17/code39.php";
//require_once $LIBRARY_PATH . "fpdf17/chinese.php";

session_start();
$DBH = PDO_connect($DATABASE_NAME);

$session_id     = quotes($_SESSION["session_id"]);
$dept		= quotes($_SESSION["dept"]);	///  本科目開課系所, 非學生所屬系所
$cid            = quotes($_SESSION["cid"]);
$grp            = quotes($_SESSION["grp"]);

$system_settings = Get_System_State();
$course = Read_Course($dept, $cid, $grp, "", "");
$course_time_string = Format_Time_String($course{"time"});

$session = Read_Session($session_id);
Renew_Session($session_id);
$stu = Read_Student($session["id"]);
$dept_data = Read_Dept($stu["dept"]);
$all_teachers = Read_All_Teacher();  
$course_of_student = Course_of_Student($stu["id"], "", "");
$student_in_course = Student_in_Course($cid, $grp);
$student_count = sizeof($student_in_course);
//$stu_grade = Read_Grade_From_DB($stu["id"]);

if( array_key_exists("SUPERUSER", $_SESSION) and $_SESSION["SUPERUSER"] )  
        $SUPERUSER = $_SESSION["SUPERUSER"];

//foreach($grade as $g) {
//  print_r($g);
//}
$stu_grade = Read_Grade_From_DB($stu["id"]);    ///  抓學生的成績
list($double, $minor) = Read_Student_State_Files();
//print_r($stu_grade);

list($stu_can_apply,$ban_reasons) = Stu_Can_Apply_Concent_Form($stu, $course, $course_of_student, $student_count, $stu_grade);

if( $stu_can_apply ) {
  //  Check_Student_Apply_Status
  //  Find_Apply Reasons
  //db_connect(1,1);
  $DBH = PDO_connect();
  $apply_data = Concent_Form_Apply_Status($stu["id"], $cid, $grp, "", "");

  if( $apply_data == -1 ) {
    Concent_Form_Stu_Apply($stu["id"], $cid, $grp);		/// 新增此加簽資料 -> DB
    Student_Log("Apply_Concent", $stu["id"], $cid, $grp, "", "SELF");
  }else{
    Student_Log("View_Concent", $stu["id"], $cid, $grp, "", "SELF");
  }
  ob_clean();
  //db_connect(1,0);
  $DBH = PDO_connect($DATABASE_NAME);
  Create_PDF();
}else{
  Student_Log("Concent_No_Need", $stu["id"], $cid, $grp, "", "SELF");
  echo "您無需申請加簽!";
}


///////////////////////////////////////////////////////////////////////////////////////////
/////  透過 fpdf 函式庫動態產生加簽單 PDF 檔案供列印
function Create_PDF()
{
  global $LIBRARY_PATH;
  global $YEAR,$TERM,$GRAPH_URL, $DEPT_CGE;
  global $system_settings, $course, $course_time_string, $dept, $cid, $dept_data, $stu;
  global $form_create_time, $ban_reasons, $apply_data;
  global $double, $minor;
  
  list($now1, $now2, $now3) = gettime("");
//  $now2 = preg_replace("/:\d*$/", "", $now2);

  if( $apply_data == -1 ) {			///  新申請
    $form_sn = Get_Concent_Form_Max_Serialno($course["id"], $course["group"]) + 1;
    $form_create_time = $now2;
  }else{					///  抓取舊資料
    $form_sn		= $apply_data["serialno"];
    $form_create_time	= $apply_data["apply_time"];    
  }
//  if( $form_sn == NULL )		$form_sn = 1;
//  if( $form_create_time == NULL )	$form_create_time = $now2;
  $form_create_time_display = preg_replace("/:/", ": ", $form_create_time);

  $font_title	= 20;
  $font_big	= 16;
  $font_small	= 12;

  $height		= 6;
  $width["indent"]	= 10;
  $width["cid"]		= 27;
  $width["group"]	= 10;
  $width["time"]	= 30;
  $width["cname"]	= 110;

//  $cou["id"]	= $_SESSION["cid"];
//  $cou["group"]	= $_SESSION["grp"];
//  $cou["cname"]	= "超級電子學三";
  $stu_grade = Read_Grade_From_DB($stu["id"]);

//  $pdf=new PDF_Chinese();
  $pdf=new PDF_Unicode();
  //$pdf=new PDF_Code39();
  
  $pdf->FPDF ('P', 'mm', 'A4');  //P 直式，L 橫式
  $pdf->SetAuthor("National Chung Cheng University");
  $pdf->SetSubject("Course Registration Consent Form");
  $pdf->SetTitle("Course Registration Consent Form");
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
  $y_emblem = 10;
  $pdf->SetX($x_emblem);
  $pdf->SetY($y_emblem);
  //$emblem = $GRAPH_URL . "emblem.jpg";
  $emblem = "http://140.123.30.101/~ccmisp06/Graph/emblem.jpg";   		///  校徽圖片
  $pdf->Image($emblem,$x_emblem,$y_emblem,15,15,"JPEG");
          
  $pdf->SetFont("font1","B",$font_title);
  $title = "國立中正大學 " . $YEAR . " 學年度第 " . $TERM . " 學期加簽/擋修申請單";
  $pdf->Cell($x_emblem,3, "");
  $pdf->Cell(0,$height*3,$title,0,1,"C"); 

  /////  學生個人資料 & 表單序號、申請時間
  $pdf->SetFont("font1","",$font_small);
  $stu_info[2]	= "系所：" . $dept_data["cname2"];
  $stu_info[3]	= "年級：" . $stu["grade"];
  $stu_info[4]	= "班級：" . $stu["class"];
  $stu_info[0]	= "學號：" . $stu["id"];
  $stu_info[1]	= "姓名：" . $stu["name"];
  $stu_info_w   = array(37,37,37,25,25);

  for( $i=0; $i<sizeof($stu_info); $i++ ) {
    if( $i < sizeof($stu_info)-1 )  
      $pdf->Cell($stu_info_w[$i],$height,$stu_info[$i],0,0,"L");
    else
      $pdf->Cell($stu_info_w[$i],$height,$stu_info[$i],0,1,"L");
  }

  $pdf->SetFont("font1","",$font_small);  
  $sn_and_print_time = "加簽單序號：$form_sn   申請時間：" . $form_create_time_display;
  $pdf->Cell(0,$height,$sn_and_print_time,"", "", "L");

  /////  加入3of9 barcode(學號)
  //$pdf->AddFont("barcode", "","3of9.php");  
  //$pdf->SetFont("barcode", "", 25);  
  //$pdf->Cell(37,$height,"*".$stu["id"]."*",0,0,"L");
  //$pdf->Code39(37,$height,"*".$stu["id"]."*");
  $pdf->Code39(157,35,$stu["id"], 0.7,7);			/// 第4~5個參數設定 barcode 大小  
  
  /////  加簽科目資料
  $pdf->Ln($height+4);
  $pdf->SetFont("font1","B",$font_small);
  $pdf->SetFillColor(200);
  $pdf->Cell($width["indent"],$height,"");
  $pdf->Cell($width["cid"],$height,"科目編號",1,0,"C",1);
  $pdf->Cell($width["group"],$height,"班別",1,0,"C",1);  
  $pdf->Cell($width["time"],$height,"上課時間",1,0,"C",1);
  $pdf->Cell($width["cname"],$height,"科目名稱",1,1,"C",1);
  $pdf->SetFont("font1","",$font_small);
  $pdf->Cell($width["indent"],$height,"");
  $pdf->Cell($width["cid"],$height,$course["id"],1,0,"C");
  $pdf->Cell($width["group"],$height,$course["group"],1,0,"C");
  $pdf->Cell($width["time"],$height,$course_time_string,1,0,"C");
  $pdf->Cell($width["cname"],$height,$course["cname"],1,1,"C");

  /////  、系統擋修原因、加簽原因等(主要 table)
//  $ban_reason = "1. 太笨太笨太笨太笨太笨太笨太笨太笨!!! 還是太笨！！\n";
//  $ban_reason .= "2. 俺不想這個學生選！ 凸-_-\n";
//  $ban_reason .= "3. 此科目限修 60 人，限修人數尚未額滿。\n";
//  $ban_reason .= "4. 因為我家隔壁的母貓生了一窩小貓。";
  $ban_reason_line_count  = 5;			///  系統擋修原因可以放的行數
  $ban_line_reduct = 0;			///  因擋修原因超過一行，必須減少「系統擋修原因」Cell 的高度
  $line_break = 72;				///  一行內若有這麼多個字元則會折行

  $ban_reason = "";
  $ban_reasons_count = count($ban_reasons);
  
  for( $i=0; $i<$ban_reason_line_count; $i++ ) {
    if( $i <= $ban_reasons_count-1 ) {
      $ban_reason .= $i+1 . ". " . $ban_reasons[$i];
      $ban_line_reduct += floor( strlen($ban_reasons[$i]) / $line_break );
    }
//      if( strlen($ban_reason) >= $line_break ) $ban_reason_line_count2--;
    if( $i < $ban_reason_line_count - $ban_line_reduct )	///  剩餘擋修理由填空行
      $ban_reason .= "　\n";
  }


  $pdf->Cell($width["indent"],$height*$ban_reason_line_count,"");
//  $x=$pdf->GetX() + 50;
//  $y=$pdf->GetY() + $ban_reason_line_count * $height;
  $pdf->Cell($width["cid"],$ban_reason_line_count * $height,"系統擋修原因\n\n\n",1,0,"C");
//  $pdf->SetX($x);
//  $pdf->SetY($y);
//  $ban_reason .= "\n[x,y] = [" . $x . "," . $y . "]";
  $pdf->MultiCell($width["group"]+$width["time"]+$width["cname"],$height,$ban_reason,1,"L");

  //////////  已於 2016/09/09 依通識中心要求，移除此欄位。 by Nidalap :D~
/*  /////  學生選課學分
  if( $dept == $DEPT_CGE ) {
//    $add_reason = "老師我想要選課～老師我想要選課～老師我想要選課～老師我想要選課～老師我想要選課～";
    $total_credit = $cge_credit = $field_credit = 0;
    $cour_field = substr($cid, 1, 1);
    if( $stu_grade ) {
      foreach( $stu_grade as $g ) {
        if( Grade_Pass($stu["id"], $g["trmgrd"]) ) {		///  成績通過才算數
          $total_credit += $g["credit"];			///    計算總學分數
          if( preg_match("/^7[12345]0....$/", $g["cour_cd"]) ) 
            $cge_credit += $g["credit"];			///    計算通識總學分數
          $this_cour_field = substr($g["cour_cd"], 1, 1);
          if( $this_cour_field == $cour_field )
            $field_credit += $g["credit"];			///    計算通識此領域總學分數
        }
      }
    }
//    $add_reason = "學生目前已選修共 $total_credit 學分，其中包含通識 $cge_credit 學分，此科目所屬領域 $field_credit 學分。";
    $add_reason = "請檢附畢業資格審查表";
    $add_line_count =  ceil(strlen($add_reason)/$line_break);
    $pdf->Cell($width["indent"],$height*$add_line_count,"");
    $pdf->Cell($width["cid"],$height*$add_line_count,"學生選課學分",1,0,"C");
    $pdf->MultiCell($width["group"]+$width["time"]+$width["cname"],$height,$add_reason,1,"L");
  }
*/  
  /////  學生加簽原因（若無特殊原因，則留空白讓學生自己手寫）
  $apply_reason = "";
  if( array_key_exists($stu["id"], $double) and ($double[$stu["id"]] == $dept ) )
    $apply_reason = "學生修讀雙主修。\n";
  if( array_key_exists($stu["id"], $minor) and ($minor[$stu["id"]] == $dept ) )
    $apply_reason = "學生修讀輔系。\n";
  $my_program_courses = Get_My_Program_Course($stu["id"]);
  if( in_array($cid, $my_program_courses) ) {
    $apply_reason = "此科目為學生客製化學程中課程。";
  }
  
//  $pdf->Cell($width["indent"],$height,"");
//  $pdf->Cell($width["cid"],$height*4,"學生加簽原因",1,0,"C");
//  $pdf->Cell($width["group"]+$width["time"]+$width["cname"],$height*4,$reason,1,1,"C");

  $pdf->Cell($width["indent"],$height*4,"");
  $pdf->Cell($width["cid"], $height*4,"學生加簽原因\n\n\n",1,0,"C");
  $pdf->MultiCell($width["group"]+$width["time"]+$width["cname"],$height*4,$apply_reason,1,"L");


  /////  學生聯絡電話
  $pdf->Cell($width["indent"],$height*2,"");
  $pdf->Cell($width["cid"],$height*2,"學生聯絡電話",1,0,"C");
  $pdf->MultiCell($width["group"]+$width["time"]+$width["cname"],$height*2,"",1,"L");  

  ///// 任課教師填寫
  $concent_no_text = "加簽順序：第___名";
  //if( $dept == $DEPT_CGE )  $concent_no_text .= "( 通識課程限加簽三人，無順序者無效)";
  $teacher_str = Format_Teacher_String($course["teacher"]);
//  $teacher_str = implode("、", $teacher[$course["teacher"]]["name"]);
  $teacher_fill =  "　　簽核：_________________(" . $teacher_str . ")";
  
  $pdf->SetFont("font1","",$font_big);
  $pdf->Cell($width["indent"],$height+5,"");
  $pdf->Cell($width["cid"],$height+5,"任課教師填寫",0,1,"L");
  
  //$dept = "1154";
  
  if( $dept != $DEPT_CGE ) {
    $pdf->Cell($width["indent"]+$width["cid"]-10,$height,"");
    $pdf->Cell($width["group"]+$width["cname"]+30,$height+10,$teacher_fill, "LTR", 1);
    $pdf->Cell($width["indent"]+$width["cid"]-10,$height,"");  
    $pdf->Cell($width["group"]+$width["cname"]+30,$height-2,$concent_no_text, "LR", 1);
    $pdf->Cell($width["indent"]+$width["cid"]-10,$height,"");
    $pdf->Cell($width["group"]+$width["cname"]+30,$height+2,"加簽時間：___月___日___時___分", "LRB", 1);
  }else{
    $teacher_fill =  "簽核(" . $teacher_str . ")：";
    $pdf->Cell($width["indent"]+$width["cid"]-10,$height,"");
    $pdf->MultiCell($width["group"]+$width["cname"]+30,$height*2+4,$teacher_fill,1,"L");
  }
//  $pdf->MultiCell($width["group"]+$width["cname"],$height+6,$teacher_fill,1,"L");

  /////  開課系所主管 / 通識中心主任
  $chief_txt = "開課系所主管";
  if( $dept == $DEPT_CGE )  $chief_txt = "通識中心主任";
  $pdf->Cell($width["indent"],$height+5,"");
  $pdf->Cell($width["cid"],$height+5,$chief_txt,0,1,"L");
  $pdf->Cell($width["indent"]+$width["cid"]-10,$height,"");
  $pdf->MultiCell($width["group"]+$width["cname"]+30,$height*2+4,"簽核：",1,"L");
  
  /////  回執聯切割線
  $x_scissor = 10;
  $y_scissor = 195;
  $pdf->SetX($x_scissor);
  $pdf->SetY($y_scissor);
  $scissor = $GRAPH_URL . "scissor.jpg";
//  $pdf->Cell(1,1,$scissor,0,1);
  $pdf->Image($scissor,$x_scissor,$y_scissor,"","","JPEG");
  $pdf->SetFontSize(6);
  $dash = "       ";
  for ($j=0;$j<85;$j++)  $dash .= ". ";
  $pdf->Cell(1,1,$dash,0,1);

  /////  學生存根聯
  $cou_info[0] = "科目編號：" . $course["id"];
  $cou_info[1] = "班別：" . $course["group"];
  $cou_info[2] = "時間：" . $course_time_string;
  $cou_info[3] = "名稱：" . $course["cname"];

  $form_info[0] = "加簽單序號：" . $form_sn;
  $form_info[1] = "申請時間：" . $form_create_time_display;

  $width["stu"] = 40;
  $pdf->SetFont("font1","U",$font_small);
  $pdf->Cell(37,$height+5,"學生存根聯",0,1);
  /////  加入3of9 barcode(學號)
  //$pdf->AddFont("barcode", "","3of9.php");
  //$pdf->SetFont("barcode", "", 25);
  //$pdf->Cell(37,$height+5,"*".$stu["id"]."*",0,1,"L");
  $pdf->Code39(40,199,$stu["id"], 0.7,7);			/// 第4~5個參數設定 barcode 大小
  
  $pdf->SetFont("font1","",$font_small);
  $pdf->Cell($width["indent"],$height,"");
  $pdf->Cell($width["stu"],$height,$stu_info[0],0);	///  學生相關資料
  $pdf->Cell($width["stu"],$height,$stu_info[1],0);
  $pdf->Cell($width["stu"],$height,$stu_info[3],0);
  $pdf->Cell($width["stu"],$height,$stu_info[4],0,1);
  $pdf->Cell($width["indent"],$height,"");  
  $pdf->Cell($width["stu"],$height,$cou_info[0],0);	///  科目相關資料
  $pdf->Cell($width["stu"]-20,$height,$cou_info[1],0);
  $pdf->Cell($width["stu"]-10,$height,$cou_info[2],0);
  $pdf->Cell($width["stu"],$height,$cou_info[3],0,1);
  $pdf->Cell($width["indent"],$height,"");
  $pdf->Cell($width["stu"],$height,$form_info[0],0);        ///  加簽單相關資料
  $pdf->Cell($width["stu"],$height,$form_info[1],0,1);

  /////  注意事項
  /////  2016/09/09 以下通識特別的判斷，依通識中心要求暫時更改  Nidalap :D~
  if( $dept == $DEPT_CGE ) {
    $note[] = "通識中心加簽單收件時間：09/19(一)AM8：30至09/23(五)PM5：30(上班時間)。";
    $note[] = "各班加簽人數上限公告於通識中心網頁公告，9/23(五)收件截止後，通識中心將統一以電腦亂數篩選，並於09/24(六)中午12:00將篩選結果公告於通識中心網頁。";
    $note[] = "確定篩選上的同學，於9/26(一)上班時間內至通識中心辦公室領取加簽單，並至教學組辦理， 於加退選截止日(2016/09/26)晚間10時前儘速自行上系統選課。未上網選課者，加簽無效。";
  }else{
    $note[] = "申請核准後，請於 " .
             preg_replace("/^...../", "", $system_settings["concent_form_accept"]) . " AM8: 00 ~ " .
             preg_replace("/^...../", "", $system_settings["concent_form_end"]) .
             " PM5: 00(上班時間)，持本單至教學組辦理；\n" .
             "    並於加退選截止日 ( " .
             $system_settings["concent_form_end"] .
             " ) 晚間十點前儘速自行上系統選課。未上網選課者加簽無效。";
  }
  $note[] = "如有衝堂或超修，所申請之加簽無效。若有超修需求請另外申請超修。";
  $note[] = "本單需學生本人攜學生證親自辦理，教學組核章後存根由學生留存；" . 
           "嗣後如有疑義以本單為憑。";
  $note[] = "未經任課教師簽章而自行偽造者，將移送獎懲委員會論處。";
  if( $dept == $DEPT_CGE ) {
    if( preg_match("/^710/", $course["id"]) )  
      $note[] = "加簽第一領域英語課程者請至語言中心辦理。";
    /////  2016/09/09 經通識中心要求取消以下備註 by Nidalap :D~
    /*if( $stu["grade"] == 3 ) 
      $note[] = "大三申請通識加簽請提出成績證明。";
      $note[] = "提出申請者應為應屆畢業生且欠缺通識學分者。";
    */
  }

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
  $x = 0; //10.5;
  $y = $y_scissor + 46; //241;
  
  /////  2016/09/09 以下通識特別的判斷，依通識中心要求暫時更改  Nidalap :D~
  if( $dept != $DEPT_CGE ) {
    $pdf->Line($x+53,$y,$x+136,$y);			/// 注意事項底線
    $pdf->Line($x+28,$y+$height,$x+107,$y+$height);
    $pdf->Line($x+151,$y+$height,$x+193.5,$y+$height);
  }

  $pdf->SetTextColor(255,0,0);   			/// 注意事項一的粗體字
  $note0 = "";
  for( $i=0; $i<=125; $i++ ) $note0 .= " ";
  $note0 .= "未上網選課者加簽無效";
  $pdf->SetX($x_note0);
  $pdf->SetY($y_note0 - $height + 0.1);
  $pdf->Cell(0, $height,$note0, 0,1);

  /////  嘗試更改輸出檔名但失敗了！  2016/09/14 Nidalap XD~
  //$filename = "/tmp/" . implode("_", array($stu["id"], $cid, $course["group"])) . ".pdf";
  //$pdf->Cell(0, $height,$filename, 0,1);
  //$pdf->Output("F", $filename,1);
  $pdf->Output();
}

?>