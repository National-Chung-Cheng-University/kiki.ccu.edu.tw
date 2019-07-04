<meta http-equiv="Content-Type" content="text/html; charset=utf-8">

<?PHP

//////////////////////////////////////////////////////////////////////////////////////////
/////  My_Program_Approval.php
/////  客製化學程審核介面
/////  顯示某學生的客製化學程申請資料，供管理者審核確認
/////  Updates:
/////    2010/08/16 從 Concent_Form_Approval.php 複製改來 by Nidalap :D~

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

$DEBUG = 0;
$time_start = time();

$DBH_cm = PDO_connect("coursemap");
session_start();
$smarty = init_smarty(3);

$stu_id = $approve = NULL;
$STATUS = array("0"=>"尚未審核", "1" => "已核可", "2" => "不可");

if( array_key_exists("action", $_POST) )    $action = $_POST["action"];
if( array_key_exists("approve", $_POST) )  $approve = $_POST["approve"];
if( array_key_exists("stu_id", $_POST) )		$stu_id = $_POST["stu_id"];
if( array_key_exists("password", $_POST) )  $_SESSION["password"] = $_POST["password"];
if( ! Check_SU_Password($_SESSION["password"], "My_Program_Approval", "") )
    die("Invalid password!");

//print_r($_POST);
//echo "<HR>";
//print_r($_SESSION);

if( To_Approve() ) {			///  如果要審核/取消
  Approve();				///   那就做吧！
}
//Print_Banner_And_Input();

if( $action == "show_details" ) {
  Show_Details($stu_id);	///  列出單一學生所有加簽單
}else{
  List_Records();				///  列出所有加簽單
}

echo "
  <FORM action='su.cgi' method=POST>
    <INPUT type=hidden name=password value='" . $_SESSION["password"] . "'>
    <INPUT type=hidden name=do_not_crypt value=1>
    <INPUT type=submit value='回管理主選單'>
  </FORM>
";

$exe_time = time() - $time_start;
echo "完成： 程式執行耗費 $exe_time 秒<BR>\n";

////////////////////////////////////////////////////////////////////////////////////////////////////
/////  檢查是否有要審核/取消審核任何加簽單
function To_Approve()
{
	if( array_key_exists("approve", $_POST)  ) {
		return 1;
	}
	return 0;
}
////////////////////////////////////////////////////////////////////////////////////////////////////
/////  執行審核/取消審核
function Approve()
{
  global $DBH_cm, $STATUS, $smarty;
  
  list($j, $time, $j) = gettime(""); 
  $ip	=	getIP();
  
  $status = $_POST['approve'];
  if( ($status <=0) or ($status>3) )		$status = 0;			///  如果審核結果有異常，則設定為未審核。[0,1,2] = [尚未審核, 已核可, 不可]
  $stu_id = quotes($_POST['stu_id']);
  
  $sql = "
	UPDATE a36tmy_program 
		   SET status = '$status', verify_time = '$time', verify_ip = '$ip'
	 WHERE std_no = '$stu_id'		   
  ";
  
  //echo "sql = $sql<BR>";
  
  if( $DBH_cm->query($sql) === FALSE ) {
    echo "更新失敗！哪裡有了問題！？！？勿關視窗快找萬惡的電算中心求救！！分機 14203 李永祥！<BR>\n";
    echo $sql . "<BR>";
    echo $DBH_cm->errorInfo();
    exit();
  }else{
    $msg = "<FONT color=RED>成功將 $stu_id 的客製化學程申請狀態設定為" . $STATUS[$status] . "。<P>";
	$smarty->assign("msg", $msg);
  }
  echo "</FONT>";

}
////////////////////////////////////////////////////////////////////////////////////////////////////
/////  顯示特定學號的申請資料(HTML table)
function List_Records()
{
	global $DBH_cm, $smarty, $YEAR, $TERM, $STATUS;	
	
	$sql = "
		SELECT DISTINCT MP.std_no, create_time, update_time, cname, ename, status, verify_time, count(*) AS course_count
		   FROM a36tmy_program MP, a36tmy_program_course MPC
		 WHERE MP.std_no = MPC.std_no
		 GROUP BY MP.std_no
		 ORDER BY MP.status DESC, MP.std_no ASC
	";
	$MPs = array();
	
	$STH = $DBH_cm->query($sql);
	while( $MP = $STH->fetch(PDO::FETCH_ASSOC) ) {
		$student = Read_Student($MP["std_no"], $dont_die=1);
		$dept	= Read_Dept($student["dept"]);
		
		$MP["stu_cname"]		= $student["name"];
		$MP["grade"]			= $student["grade"];
		$MP["dept_cname"]	= $dept["cname"];
		
		array_push($MPs, $MP);
	}
	
	$smarty->assign("YEAR", $YEAR);
	$smarty->assign("TERM", $TERM);
	$smarty->assign("MPs", $MPs);
	$smarty->assign("STATUS", $STATUS);
	$smarty->display("superuser/My_Program_Approval_List.tpl");
}

////////////////////////////////////////////////////////////////////////////////////////////////////
/////  顯示特定學號的申請資料(HTML table)
function Show_Details($stu_id)
{
	global $DATABASE_NAME, $GRAPH_URL, $YEAR, $TERM, $DBH_cm, $STATUS, $PROPERTY_TABLE;
	global $DEBUG, $exe_time, $time_start, $smarty;

	$stu_id = $_POST["stu_id"];
	
	/////  如果沒有輸入學號：改為顯示所有申請資料列表
	if( $stu_id == "" )	{
		List_Records();
		die();
	}
	
	$sql = "SELECT * FROM a36tmy_program WHERE std_no = '$stu_id'";
//	echo $sql; 
	$STH = $DBH_cm->query($sql);
	$MP = $STH->fetch(PDO::FETCH_ASSOC);
	
	if( $MP['std_no'] == NULL ) {
		echo "<FONT color='RED' size=4>查無 $stu_id 之申請資料！<P></FONT>";
		List_Records();
		die();
	}
	
	//$sql = "SELECT * FROM a36tmy_program_course WHERE std_no = '$stu_id'";
	$sql = "
	    SELECT DISTINCT MPC.course_id, COU.cname, COU.curpoint as credit, COU.deptcd, DEPT.abbrev AS dept_cname, MPC.attr,
		             CASE deptcd WHEN '$deptcd' THEN '1' ELSE '0' END AS is_my_dept,
					 CASE substring(deptcd from 4 for 4) WHEN '6' THEN '0' ELSE '1' END AS is_under
	      FROM a36tmy_program_course MPC, a31vallcourse COU, a36vdept DEPT
		 WHERE std_no = '$stu_id'
		      AND MPC.course_id = COU.coursecd
			  AND COU.deptcd = DEPT.cd
		  ORDER BY MPC.course_id
	  ";
//	echo $sql; 
	$STH = $DBH_cm->query($sql);
	$MPC = $STH->fetchAll(PDO::FETCH_ASSOC);
	
	$credits['total_max']  = 0;
	foreach( $MPC as $course ) {
		$credits['total_max'] += $course['credit'];
	}
	//print_r($MP);

	if( $_POST["stu_id"] == 'guest' )		$stu_id = '999999999';
	$student = Read_Student($stu_id, $dont_die=1);
	$dept	= Read_Dept($student["dept"]);
	if( substr($stu_id, 0, 1) == '4' )	$student['is_under'] = 1;
	else											$student['is_under'] = 0;
	
	//echo "substr = " . substr($stu_id, 0, 1);
	
	$smarty->assign("YEAR", $YEAR);
	$smarty->assign("TERM", $TERM);
	$smarty->assign("error_msg", $error_msg);
	$smarty->assign("student", $student);
	$smarty->assign("dept", $dept);
	$smarty->assign("MP", $MP);
	$smarty->assign("MPC", $MPC);
	$smarty->assign("credits", $credits);
	$smarty->assign("PROPERTY_TABLE", $PROPERTY_TABLE);
	$smarty->assign("STATUS", $STATUS);
	$smarty->display("superuser/My_Program_Approval.tpl");

}

////////////////////////////////////////////////////////////////////////////////////////////////////
/*function Print_Banner_And_Input() {
  global $EXPIRE_META_TAG, $GRAPH_URL;
  echo "<HTML>
    <HEAD>
      <TITLE>客製化學程審核</TITLE>
      $EXPIRE_META_TAG
    </HEAD>";
  Print_Javascript();
  echo "
  <BODY background='" . $GRAPH_URL . "manager.jpg'>
  <CENTER><H1>客製化學程審核</H1><HR size=2 width=50%>
  <TABLE border=0 bgcolor=YELLOW>
    <TR>
      <TD>
      <FORM action='My_Program_Approval.php' method='POST'>
        <INPUT maxsize=9 name=stu_id id = stu_id>
        <INPUT type=hidden name=action value='show_details'>
        <INPUT type='SUBMIT' value='列出此學生申請資料(學號)'>
      </FORM>
	  </TD>
    </TR>
  </TABLE>
  ";
}
*/
////////////////////////////////////////////////////////////////////////////////////////////////////
function Print_Javascript()
{
  echo "
    <SCRIPT type='text/javascript' src='https://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js'></script>
    <SCRIPT language='javascript'>
      \$(document).ready(function(){
        \$('#stu_id').focus();
        \$('input:checkbox').click(function() {
          \$('#form2').submit();
        })
        \$('.cancel').click(function() {
          if( confirm('您確定要取消此加簽單?') ) {
            ///
          }else{
            return false;
          }
        })
      })
    </SCRIPT>
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
$application = Concent_Form_Apply_Status($stu["id"], $cid, $grp, "", "");
if( $application == -1 ) {		///  尚未加簽過此科目: 新增加簽資料
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
  $submit_text = "是，我要申請";
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
}

//print_r($application);

echo "
  <P>
  <TABLE border=1 width=50%>
    <TR>
      <TD bgcolor=LIGHTYELLOW>$message</TD>
    </TR>
  </TABLE>
 
  <FORM action='My_Concent_Form2.php' method='POST'>
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