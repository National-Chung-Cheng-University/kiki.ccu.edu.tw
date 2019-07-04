<?PHP

//////////////////////////////////////////////////////////////////////////////////////////
/////  Concent_Form_Apply1.php
/////  學生申請加簽單確認畫面
/////  列出即將申請加簽的科目資料
/////  Updates:
/////    2010/07/30 Created by Nidalap :D~
/////    2012/11/05 改採 PDO 連線資料庫 by Nidalap :D~

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
require_once $LIBRARY_PATH . "Grade.php";

session_start();
  
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
$course = Read_Course($dept, $cid, $grp, "", "");
$course_of_student = Course_of_Student($stu["id"]);
$student_in_course = Student_in_Course($cid, $grp);
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

//print_r($_SESSION);
//db_connect("","");
$stu_grade = Read_Grade_From_DB($stu["id"]);	///  抓學生的成績
if( $stu_grade ) {
  foreach( $stu_grade as $grade ) {
    if( $grade["cour_cd"] == $cid ) {
      if( Grade_Pass($stu["id"], $grade["trmgrd"]) )  $already_pass = 1;
    }
  }
}

//print_r($stu_grade);

if( isset($already_pass) ) {			///  重複修習！
  $message = "您早已修過此課程，請勿加選或加簽！";
  $back_text = "我要回上頁";
}else{

//  print_r($course);
  list($stu_can_apply,$ban_reasons) = Stu_Can_Apply_Concent_Form($stu, $course, $course_of_student, $student_count, $stu_grade);
  if( !$stu_can_apply ) {			///  系統判斷無須加簽
    $message = "您無須申請加簽！";
    $back_text = "我要回上頁";
  }else{
    //db_connect(1,1);                                ///  連到 academic_kiki 資料庫  
	$DBH = PDO_connect();								///  連到 academic_kiki 資料庫  
    $application = Concent_Form_Apply_Status($stu["id"], $cid, $grp, "", "");
	
    if( $application == -1 ) {			///  尚未加簽過此科目: 新增加簽資料
      $message = "
            您正要申請加簽此科目：  
            <P>  
            <CENTER>  
              <B><U>" . $course["cname"] . "(代碼 $cid 班別 $grp)</U></B>  
            </CENTER>  
            <P>  
            是否正確？  
            若是請點選「是，我要申請」，並列印下頁加簽單。
      ";
      if( $dept == $DEPT_PHY )
        $message .= "<P><FONT color=RED>欲申請加簽體育課程，請先洽體育中心！</FONT>";
        
      $submit_text = "是，我要申請";
      $back_text = "否，我要回上頁";
    }else{					///  曾經加簽過此科目: 帶出舊資料
      $message = "
            您已經在 " . $application["apply_time"] ." 申請加簽過此科目：
            <P>  
            <CENTER>  
              <B><U>" . $course["cname"] . "(代碼 $cid 班別 $grp)</U></B>  
            </CENTER>  
            <P>  
            若要重新列印請點選「是，我要重新列印」，並列印下頁加簽單。
      ";
      $submit_text = "是，我要重新列印";
      $back_text = "否，我要回上頁";
    }
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
 
  <FORM action='Concent_Form_Apply2.php' method='POST'>
";
if( !isset($already_pass) and $stu_can_apply ) {
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