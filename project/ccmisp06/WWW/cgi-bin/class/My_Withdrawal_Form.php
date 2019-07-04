<?PHP

//////////////////////////////////////////////////////////////////////////////////////////
/////  My_Withdrawal_Form.php
/////  學生「我的棄選單」畫面
/////  列出該學生所有棄選單申請狀態一覽表
/////  Updates:
/////    2013/11/15 從 My_Concent_Forms.php 改來 by Nidalap :D~
/////    2013/12/02 加入判斷系統設定的 redirect_to_query 設定，判別是否抓上學期課程資料。 by Nidalap :D~

require_once "../library/Reference.php";
require_once $LIBRARY_PATH . "Error_Message.php";
require_once $LIBRARY_PATH . "Common_Utility.php";
require_once $LIBRARY_PATH . "System_Settings.php";
require_once $LIBRARY_PATH . "Session.php";
require_once $LIBRARY_PATH . "Password.php";
require_once $LIBRARY_PATH . "Dept.php";
require_once $LIBRARY_PATH . "Course.php";
require_once $LIBRARY_PATH . "Student.php";
require_once $LIBRARY_PATH . "Database.php";
require_once $LIBRARY_PATH . "Student_Course.php";

session_start();

//print_r($_GET);
$session_id	= quotes($_GET["session_id"]);
$session	= Read_Session($session_id);
Renew_Session($session_id);

$system_settings = Get_System_State();
if( $system_settings['redirect_to_query'] == 1 ) {			///  抓上學期開課選課資料
  list($year, $term) = Last_Semester(1);  
}else{														///  抓本學期開課選課資料
  $year = $YEAR;
  $term = $TERM;
}

$stu = Read_Student($session["id"]);
$dept_data = Read_Dept($stu["dept"]);
if( Check_SU_Password($session["password"], "", $stu["id"]) ) {
  $_SESSION["SUPERUSER"] = 1;           ///  檢查 SU password
}else{
  unset($_SESSION["SUPERUSER"]);
}
//print_r($session);

$HEAD_DATA = Form_Head_Data($stu["id"], $stu["name"], $dept_data["cname2"], $stu["grade"], $stu["class"]);
$HTML_BANNER = Print_HTML_Banner();

//db_connect(1,1);			///  連到 academic_kiki 資料庫  
$DBH = PDO_connect();		///  連到 academic_kiki 資料庫
$apply_data = Withdrawal_Form_Apply_Status($stu["id"], "", $year, $term);

Print_My_Withdrawal_Form($apply_data);

//////////////////////////////////////////////////////////////////////////////////////////////////
function Print_My_Withdrawal_Form($apply_data)
{
  global $GRAPH_URL, $stu, $session_id, $year, $term;
  $system_settings = Get_System_State();
  list($year, $term) = Last_Semester(1);  
  
  if( $apply_data == -1 ) {						///  尚未申請棄選
	echo "您尚未申請棄選！<P>\n";
	die();
  }
  
  if( $apply_data == -2 ) {						///  已有已核可的棄選單
    $apply_data = Withdrawal_Form_Apply_Status($stu["id"], "verified", $year, $term);
	echo "恭喜！您申請的棄選單<FONT color=RED>已經核可</FONT>。<P>\n";
  }else{										///  尚未核可
    echo "您申請的棄選單<FONT color=RED>正在審核中</FONT>......<P>\n";
  }
  
  ///  這一段是為了彌補 Read_Course() 需要系所代碼的缺陷，用來找出該參數用
  if( $system_settings['redirect_to_query'] == 1 ) {			///  抓上學期選課資料
    $stu_cour = Course_of_Student($stu['id'], $year, $term);
  }else{														///  抓本學期選課資料
    $stu_cour = Course_of_Student($stu['id']);
  }
  //$stu_cour = Course_of_Student($stu['id']);
  foreach( $stu_cour as $cour ) {
    if( $cour['id'] == $apply_data['course_id'] ) 
	  $apply_data['dept'] = $cour['dept'];
  }
  if( $system_settings['redirect_to_query'] == 1 ) {			///  抓上學期開課資料
    $course = Read_Course($apply_data['dept'], $apply_data['course_id'], $apply_data['grp'], $year, $term);
  }else{														///  抓本學期開課資料
    $course = Read_Course($apply_data['dept'], $apply_data['course_id'], $apply_data['grp']);
  }
  //$course = Read_Course($apply_data['dept'], $apply_data['course_id'], $apply_data['grp']);

  echo "<TABLE border=1 width=95%>";
  echo "<TR bgcolor=YELLOW>
          <TH>申請時間</TH>
          <TH>科目代碼</TH>
          <TH>班別</TH>
          <TH>科目名稱</TH>
        </TR>";

  $apply_data["apply_time"] = preg_replace("/ ..:..:..$/", "", $apply_data["apply_time"]);
    
  echo "
    <TR>
      <TD align=CENTER>" . $apply_data["apply_time"] . "</TD>
      <TD align=CENTER>" . $apply_data["course_id"] . "</TD>
      <TD align=CENTER>" . $apply_data["grp"] . "</TD>
      <TD>" . $course["cname"] . "</TD>
    </TR>
  ";

  echo "</TABLE>";


  //list($withdrawal_form_allowed, $cf_msg) = Apply_Form_Allowed("withdrawal");          /// 目前是否允許申請棄選 
  //if( $withdrawal_form_allowed == 1 ) {
  //  echo "<P>【<A href='Selected_View00.cgi?session_id=$session_id'>申請棄選課程</A>】";
  //}
  //echo "
  //  </CENTER><HR><P>
  //";
}


//print_r($apply_data);

/*
if( $application == -1 ) {		///  尚未棄選過此科目: 新增棄選資料
  $message = "
        您正要申請棄選此科目：  
        <P>  
        <CENTER>  
          <B><U>" . $course["cname"] . "(代碼 $cid 班別 $grp)</U></B>  
        </CENTER>  
        <P>  
        是否正確？  
        若是請點選「是，我要申請」，並列印下頁棄選單。  
  ";
  $submit_text = "是，我要申請";
}else{					///  曾經棄選過此科目: 帶出舊資料
  $message = "
        您已經在 " . $application["apply_time"] ." 申請棄選過此科目：
        <P>  
        <CENTER>  
          <B><U>" . $course["cname"] . "(代碼 $cid 班別 $grp)</U></B>  
        </CENTER>  
        <P>  
        若要重新列印請點選「是，我要重新列印」，並列印下頁棄選單。
  ";
  $submit_text = "是，我要重新列印";
}

//print_r($application);

echo "
  <P>
  <TABLE border=1 width=50%>
    <TR>
      <TD bgcolor=LIGHTYELLOW>$message</TD>
    </TR>
  </TABLE>
 
  <FORM action='Withdrawal_Form_Apply2.php' method='POST'>
    <INPUT type=SUBMIT value='$submit_text'>
    <INPUT type=BUTTON value='否，我要回上頁' onclick='javascript:history.back()'>
  </FORM>
";
*/
//////////////////////////////////////////////////////////////////////////////////////
function Print_HTML_Banner()
{
  global $EXPIRE_META_TAG, $BG_PIC, $GRAPH_URL, $HEAD_DATA;

  print "
    <HTML>
      <HEAD>
        <TITLE>我的棄選單</TITLE>
        $EXPIRE_META_TAG
      </HEAD>
    <BODY background='$BG_PIC'>
      <CENTER>
        $HEAD_DATA
        <HR>
  ";
}

?>