<?PHP

//////////////////////////////////////////////////////////////////////////////////////////
/////  Withdrawal_Form_Apply1.php
/////  學生申請棄選單確認畫面
/////  列出即將申請棄選的科目資料
/////  Updates:
/////    2013/04/15 從 Concent_Form_Apply1.php 加簽申請單修改而來 by Nidalap :D~
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
require_once $LIBRARY_PATH . "English.php";

session_start();
$system_settings = Get_System_State();
if( $system_settings['redirect_to_query'] == 1 ) {			///  抓上學期開課選課資料
  list($year, $term) = Last_Semester(1);  
}else{														///  抓本學期開課選課資料
  $year = $YEAR;
  $term = $TERM;
}

//print_r($_GET);
$session_id	= quotes($_GET["session_id"]);
$dept		= quotes($_GET["dept"]);
$cid		= quotes($_GET["cid"]);
$grp		= quotes($_GET["grp"]);
$session	= Read_Session($session_id);
Renew_Session($session_id);

$DBH = PDO_connect($DATABASE_NAME);
$stu = Read_Student($session["id"]);
$dept_data = Read_Dept($stu["dept"]);

$course = Read_Course($dept, $cid, $grp, $year, $term);
$course_of_student = Course_of_Student($stu["id"], $year, $term);

//$student_in_course = Student_in_Course($cid, $grp);
$student_count = sizeof($student_in_course);

if( Check_SU_Password($session["password"], "", $stu["id"]) ) {
  $_SESSION["SUPERUSER"] = 1;           ///  檢查 SU password
}else{
  unset($_SESSION["SUPERUSER"]);
}

$HEAD_DATA = Form_Head_Data($stu["id"], $stu["name"], $dept_data["cname2"], $stu["grade"], $stu["class"]);
$HTML_BANNER = Print_HTML_Banner();


$_SESSION["session_id"]	= $session_id;
$_SESSION["dept"]	= $dept;
$_SESSION["cid"]	= $cid;
$_SESSION["grp"]	= $grp;

/////  判別學生是否可申請棄選
list($withdrawal_form_allowed, $wf_msg)	= Apply_Form_Allowed("withdrawal");		//  條件1：目前是否允許申請棄選
if( $withdrawal_form_allowed == 1 ) {
  $withdrawal_form_allowed = 0;
  foreach ( $course_of_student as $cou ) {										//  條件2：此科目為學生所選科目之一
//    echo "[$cid, $grp] <-> [" . $cou['id'] . $cou['group'] . "]<BR>\n";
    if( ($cou['id'] == $cid) and ($cou['group'] == $grp) )   $withdrawal_form_allowed = 1;
  }
}
if( $withdrawal_form_allowed == 1 ) {											//  條件3：「大學部」棄選「前」學分數不得少於9
  $MIN_CREDIT = 9;
  $total_credit = 0;
  foreach ($course_of_student as $cos) {
    $total_credit += $cos['credit'];
  }
  if( ($total_credit < $MIN_CREDIT) 
       and ( substr($session["id"],0,1)=='4' ) ) {
    $withdrawal_form_allowed = -1;
	echo substr($session["id"],0,1);
  }
}

if( $withdrawal_form_allowed == 0 ) {
  $message = "目前並非棄選時段，或您本學期沒有加選修過此課程，請勿申請棄選！";
  $back_text = "我要回上頁";
}else if($withdrawal_form_allowed == -1 ) {
  $message = "依規定當學期修習總學分數不得少於 $MIN_CREDIT 學分才能棄選，您無法申請棄選！";
  $back_text = "我要回上頁";
}else{
  $DBH = PDO_connect();								///  連到 academic_kiki 資料庫  
  
  /////  每學期只能棄選一門，所以先找出該生棄選資料，判斷是否為目前科目。
  $application = Withdrawal_Form_Apply_Status($stu["id"], "", $year, $term);
  
  //echo "application = ";
  //print_r($application);
  
  if( $application == -1 ) {			///  尚未棄選過此科目: 新增棄選資料
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
      $back_text = "否，我要回上頁";
  }else if( $application == -2 ) {		///  已經有核可了的棄選單，不可再申請！
      //$application = Withdrawal_Form_Apply_Status($stu["id"], "verified");
	  //echo "verified already!<BR>\n";
	  //print_r($application);
	  
	  $message = "
            您已有已經核可的加簽單，請勿再申請！
			詳見「<A href='My_Withdrawal_Form.php?session_id=$session_id'>我的棄選單</A>」功能。
      ";
      $withdrawal_form_allowed = 0;
      $back_text = "回上頁";
  
  }else if( ($course['id'] == $application['course_id']) and ($course['group'] == $application['grp']) ) {
	  /////  曾經棄選過此科目: 帶出舊資料
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
      $back_text = "否，我要回上頁";
  }else{			/////  棄選了別的科目！
    foreach ( $course_of_student as $cou ) {
      if( ($cou['id'] == $application['course_id']) and ($cou['group'] == $application['grp']) ) {
	    $application['dept'] = $cou['dept'];		///  因 Read_Course() 架構缺陷，需先找出原先已申請過的科目之開課系所
	  }
    }
	$original_course = Read_Course($application['dept'], $application['course_id'], $application['grp']);
    $message = "
            您已經在 " . $application["apply_time"] ." 申請棄選過此科目：
            <P>  
            <CENTER>  
              <B><U>" . $original_course["cname"] . "(代碼 " . $application['course_id'] . " 班別 " . $application['grp'] . " )</U></B>  
            </CENTER>  
            <P>  
            <FONT color=RED>
			  依規定，每學期限申請一門棄選科目，
			  確定要改棄選 " . $course["cname"] . "(代碼 $cid 班別 $grp ) 嗎？
			</FONT>
			
    ";
    $submit_text = "是，我要改棄選 " . $course["cname"];
    $back_text = "否，我要保留" . $original_course["cname"] ;
  }
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
";
if( $IS_ENGLISH ) {
  echo "  <INPUT type='hidden' name='e' value='1'>";
}
if( $withdrawal_form_allowed == 1 ) {
  echo "  <INPUT type=SUBMIT value='$submit_text'>";
}
echo "
    <INPUT type=BUTTON value='$back_text' onclick='javascript:history.back()'>
  </FORM>
";

//////////////////////////////////////////////////////////////////////////////////////
function Print_HTML_Banner()
{
  global $EXPIRE_META_TAG, $BG_PIC, $GRAPH_URL, $HEAD_DATA;

  print "
    <HTML>
    $EXPIRE_META_TAG
    <BODY background='$BG_PIC'>
      <CENTER>
        $HEAD_DATA
        <HR>
  ";
}

?>