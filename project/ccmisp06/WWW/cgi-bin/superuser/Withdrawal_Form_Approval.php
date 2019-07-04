<meta http-equiv="Content-Type" content="text/html; charset=utf-8">

<?PHP

//////////////////////////////////////////////////////////////////////////////////////////
/////  Withdrawal_Form_Approval.php
/////  棄選單審核介面
/////  列出(某學生)本學年學期所有棄選單及其審核狀態，供管理者審核確認
/////  Updates:
/////    2013/11/15 從 Concent_Form_Approval.php 改來 by Nidalap :D~

require_once "../library/Reference.php";
require_once $LIBRARY_PATH . "Error_Message.php";
require_once $LIBRARY_PATH . "Common_Utility.php";
require_once $LIBRARY_PATH . "System_Settings.php";
require_once $LIBRARY_PATH . "Session.php";
require_once $LIBRARY_PATH . "Dept.php";
require_once $LIBRARY_PATH . "Course.php";
require_once $LIBRARY_PATH . "Student.php";
require_once $LIBRARY_PATH . "Database.php";
require_once $LIBRARY_PATH . "Password.php";
require_once $LIBRARY_PATH . "Student_Course.php";

$DBH = PDO_connect();
session_start();

$system_settings = Get_System_State();
if( $system_settings['redirect_to_query'] == 1 ) {			///  抓上學期開課選課資料
  list($year, $term) = Last_Semester(1);  
}else{														///  抓本學期開課選課資料
  $year = $YEAR;
  $term = $TERM;
}

if( array_key_exists("password", $_POST) )  $_SESSION["password"] = $_POST["password"];
if( array_key_exists("action", $_POST) )    $_SESSION["action"] = $_POST["action"];
if( array_key_exists("stu_id", $_POST) )    $_SESSION["stu_id"] = $_POST["stu_id"];
if( ! Check_SU_Password($_SESSION["password"], "Withdrawal_Form_Approval", "") )
  die("Invalid password!");

//var_dump($_POST);
//echo "<HR>";
//var_dump($_SESSION);
//echo "<HR>";

if( To_Approve() ) {			///  如果要審核/取消任何棄選單
  Approve();				///   那就做吧！
//  echo "going to verify...<BR>";
}
Print_Banner_And_Input();
//print_r($_SESSION);
if( $_SESSION["action"] == "list_stu" ) {
  List_Records($_SESSION["stu_id"]);	///  列出單一學生所有棄選單(有效的應該只有一個)
}else{
  List_Records("");			///  列出所有棄選單
}

echo "
  <FORM action='su.cgi' method=POST>
    <INPUT type=hidden name=password value='" . $_SESSION["password"] . "'>
    <INPUT type=hidden name=do_not_crypt value=1>
    <INPUT type=submit value='回管理主選單'>
  </FORM>
";

////////////////////////////////////////////////////////////////////////////////////////////////////
/////  檢查是否有要審核/取消審核任何棄選單
function To_Approve()
{
  foreach( $_REQUEST as $key=>$value) {
    if( preg_match("/^check_/", $key) ) 
      return 1;
  }
  return 0;
}
////////////////////////////////////////////////////////////////////////////////////////////////////
/////  執行審核/取消審核
function Approve()
{
  global $DBH, $year, $term;
  foreach( $_REQUEST as $key=>$value) {		///  先解析傳進來要核可/取消的棄選單資料
    if( preg_match("/^check_/", $key) ) {
      list($j, $stu_id, $course_id, $grp) = explode("_", $key);
      $verify = $value;
      break;
    }
  }
//  echo "[$stu_id, $course_id, $grp, $verify]<BR>";
  list($j, $time, $j) = gettime(""); 
  
  if( $verify == "on" )	{					///  要核可
    $verify_text = "1";
    $verify_text2 = "核可";
    $verify_text3 = ", verify_time ='$time'";
    SU_Log("add_withdrawal", $stu_id);
  }else{									///  要取消
    $verify_text = "";
    $verify_text2 = "取消";
    $verify_text3 = ", verify_time = NULL ";
    SU_Log("del_withdrawal", $stu_id);
  }
  
  $sql = "UPDATE withdrawal_form SET verified='$verify_text'" . $verify_text3 . 
          "WHERE stu_id='$stu_id' 
		     AND course_id='$course_id' 
			 AND grp='$grp'
			 AND year='$year'
			 AND term='$term'
		     AND verified != 'a'";
  echo "<FONT color=RED>";
  
  if( $DBH->query($sql) === FALSE ) {
    echo "更新失敗！哪裡有了問題！？！？勿關視窗快找萬惡的電算中心求救！！<BR>\n";
    echo "[$stu_id, $course_id, $grp, $verify]<BR>\n";
    echo $sql . "<BR>";
    echo $DBH->errorInfo();
    exit();
  }else{
    echo "成功 " . $verify_text2 . "此棄選單(學號 $stu_id, 科目 $course_id, 班別 $grp)";
  }
  echo "</FONT>";
}
////////////////////////////////////////////////////////////////////////////////////////////////////
/////  列出全部或特定學號的棄選單資料(HTML table)
function List_Records($stu_id)
{
  global $DATABASE_NAME, $GRAPH_URL, $year, $term, $DBH;
  $DBH_a = PDO_connect("academic");
  
  
  define("HIGHLIGHT1", 5);
  define("HIGHLIGHT2", 10);
  
  /////  先抓取 withdrawal_form 內的資料
  $sql = "SELECT DISTINCT year, term, course_id, grp, stu_id, verified, 
				 apply_time, verify_time
            FROM withdrawal_form
		   WHERE year='$year' AND term='$term'";
  if( $_REQUEST['include_abandoned'] != 'on' ) {
    $sql .= " AND verified != 'a' ";
  }else{
    //$sql .= " AND (verified='' or verified='1')";
  }
  
  if( $stu_id ) {					///  如果要列出特定學生棄選單
    $sql .= " AND stu_id = '$stu_id'";
    $stu = Read_Student($stu_id);
  }
  $sql .= " ORDER BY stu_id, course_id, grp";
  
  //echo $sql;
  $STH = $DBH->query($sql);
  $rows = $STH->fetchAll(PDO::FETCH_ASSOC);
  $row_count = count($rows);
  
  //print_r($rows);
  //echo "<HR>\n";
  
  /////  再抓取教務系統 a31vallcourse 的資料補齊
  $i=0;
  foreach( $rows as $row ) {
    $sql = "SELECT DISTINCT cname FROM a31vallcourse WHERE coursecd = '" . $row['course_id'] . "'";
	$STH = $DBH_a->query($sql);
	$temp = $STH->fetch(PDO::FETCH_ASSOC);
	$rows[$i]['cname'] = $temp['cname'];
	$i++;
  }
  
  //print_r($rows);
  //echo "<HR>\n";
  
/*
  $sql = "SELECT DISTINCT cname FROM a31vallcourse WHERE coursecd IN (";
  $i = 0;
  foreach( $rows as $row ) {
    if( $i != 0 )  $sql .= ", ";
    $sql .= "'" . $row['course_id'] . "'";
	$i++;
  }  
  $sql .= ") ORDER BY coursecd";
  
  $STH = $DBH_a->query($sql);
//  echo $sql . "<BR>\n";
//  print_r($DBH_a->errorInfo());
  
  $i = 0;
  while( $temp = $STH->fetch(PDO::FETCH_ASSOC) ) 
	$rows[$i++]['cname'] = $temp['cname'];
*/
  if( $stu_id ) {
    if( isset($stu) && ($stu["id"] != $stu_id) ) {
      $stu = Read_Student($stu_id);
    }
    $header_text = $stu["name"] . "($stu_id)目前共有 $row_count 筆棄選紀錄：";
  }else{
    $header_text = "目前全部共有$row_count 筆棄選紀錄：";
  }
  echo $header_text . "<BR>";
  echo "<FORM id=form2 action='Withdrawal_Form_Approval.php' method=POST>";
  echo "<TABLE border=1 width=90%>";
  echo "  <TR>
            <TH>審核</TH>
            <TH>學號</TH>
            <TH>姓名</TH>
            <TH>科目代碼</TH>
            <TH>班別</TH>
            <TH>科目名稱</TH>
            <TH>申請時間</TH>
            <TH>審核時間</TH>
			<TH>備註</TH>
          </TR>";
	
  reset($rows);	
  foreach( $rows as $row ) {
    $stu = Read_Student($row["stu_id"], 1);
    $student_course = Course_of_Student($row["stu_id"], $year, $term);

    //////  審核 Checkbox 
    $checkbox_id = "check_" . $row["stu_id"] . "_" .  $row["course_id"] . "_" . $row["grp"];
    if( $row["verified"] == '1') {
      $checked_html = "<A href='Withdrawal_Form_Approval.php?$checkbox_id=off'><IMG border=0 class=cancel src='" . $GRAPH_URL . "checked.jpg'></A>";
    }else{
      $checked_html = "<INPUT type=checkbox class='toggle_verify' name=$checkbox_id>";
    }
	//////  備註
	if( $row["verified"] == 'a') {
	  $style = 'bgcolor="GRAY"';
	  $note = '已取消';
	}else{
	  $style = '';
	  $note = '';
	}
 
    echo "<TR $style>
            <TD align=CENTER >$checked_html</TD>
            <TD>" . $row["stu_id"] . "</TD>
            <TD>" . $stu["name"] . "</TD>
            <TD>" . $row["course_id"] . "</TD>
            <TD>" . $row["grp"] . "</TD>
            <TD>" . $row["cname"] . "</TD>
            <TD>" . $row["apply_time"] . "</TD>
            <TD>" . ($row["verify_time"] ? $row["verify_time"] : "&nbsp;") . "</TD>
			<TD>" . $note . "</TD>
          </TR>
    ";
  }
  echo "</TABLE></FORM>";
}
////////////////////////////////////////////////////////////////////////////////////////////////////
function Print_Banner_And_Input() {
  global $EXPIRE_META_TAG, $GRAPH_URL;
  echo "<HTML>
    <HEAD>
      <TITLE>棄選單申請確認</TITLE>
      $EXPIRE_META_TAG
    </HEAD>";
  Print_Javascript();
  
  $inc_aba = 'checked';
  if( array_key_exists("include_abandoned", $_REQUEST) and ($_REQUEST['include_abandoned'] != 'on') )
    $inc_aba = ' ';
	
  echo "
  <BODY background='" . $GRAPH_URL . "manager.jpg'>
  <CENTER><H1>棄選單申請確認</H1><HR size=2 width=50%>
  <TABLE border=0 bgcolor=YELLOW>
    <TR>
      <TD>
      <FORM action='Withdrawal_Form_Approval.php' method='POST'>
	    <INPUT type=checkbox name='include_abandoned' $inc_aba>顯示已取消之棄選單
		<BR>
        <INPUT maxsize=9 name=stu_id id = stu_id>
        <INPUT type=hidden name=action value='list_stu'>
        <INPUT type='SUBMIT' value='列出此學生棄選單(學號)'>
      </FORM>
      </TD><TD width=150></TD><TD>
      <FORM action='Withdrawal_Form_Approval.php' method='POST'>
	    <INPUT type=checkbox name='include_abandoned' $inc_aba>顯示已取消之棄選單
		<BR>
        <INPUT type=hidden name=action value='list_all'>
        <INPUT type='SUBMIT' value='列出所有棄選單'>
      </FORM>
    </TR>
  </TABLE>
  ";
}
////////////////////////////////////////////////////////////////////////////////////////////////////
function Print_Javascript()
{
  echo "
    <SCRIPT type='text/javascript' src='https://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js'></script>
    <SCRIPT language='javascript'>
      \$(document).ready(function(){
        \$('#stu_id').focus();
        \$('input:checkbox.toggle_verify').click(function() {
          \$('#form2').submit();
        })
        \$('.cancel').click(function() {
          if( confirm('您確定要取消此棄選單?') ) {
            ///
          }else{
            return false;
          }
        })
      })
    </SCRIPT>
  ";
  echo "
    <STYLE>
	  .abandoned { color:GRAY; background-color:GRAY; }
	</STYLE>
  ";
  


}


/*
$session_id	= quotes($_GET["session_id"]);
$dept		= quotes($_GET["dept"]);
$cid		= quotes($_GET["cid"]);
$grp		= quotes($_GET["grp"]);
$session	= Read_Session($session_id);
Renew_Session($session_id);

$stu = Read_Student($session["id"]);
$dept_data = Read_Dept($dept);
$course = Read_Course($dept, $cid, $grp, "", "");
$HEAD_DATA = Form_Head_Data($stu["id"], $stu["name"], $dept_data["cname2"], $stu["grade"], $stu["class"]);
$HTML_BANNER = Print_HTML_Banner();

$_SESSION["session_id"]	= $session_id;
$_SESSION["dept"]	= $dept;
$_SESSION["cid"]	= $cid;
$_SESSION["grp"]	= $grp;

//print_r($_SESSION);
db_connect(1,1);			///  連到 academic_kiki 資料庫  
$application = Withdrawal_Form_Apply_Status($stu["id"], $cid, $grp, "", "");
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
 
  <FORM action='My_Withdrawal_Form2.php' method='POST'>
    <INPUT type=SUBMIT value='$submit_text'>
    <INPUT type=BUTTON value='否，我要回上頁' onclick='javascript:history.back()'>
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
*/

?>