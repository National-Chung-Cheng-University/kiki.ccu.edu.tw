<meta http-equiv="Content-Type" content="text/html; charset=utf-8">

<?PHP

//////////////////////////////////////////////////////////////////////////////////////////
/////  SystemChoose_Analyze01.php
/////  系統（限修）篩選紀錄檔分析
/////  為瞭解各系課程需求人數，於每次限修人數篩選時，額外紀錄每一門課篩選前後的選修人數，並分析之。
/////  第二頁：抓取上一頁要分析的紀錄檔（可能多筆），執行分析。
/////  Updates:
/////    2016/03/01 Created by Nidalap :D~

require_once "../../library/Reference.php";
require_once $LIBRARY_PATH . "Error_Message.php";
require_once $LIBRARY_PATH . "Common_Utility.php";
require_once $LIBRARY_PATH . "System_Settings.php";
require_once $LIBRARY_PATH . "Dept.php";
require_once $LIBRARY_PATH . "Course.php";
require_once $LIBRARY_PATH . "Password.php";
require_once $LIBRARY_PATH . "Teacher.php";

$DEBUG = 0;
session_start();
if( array_key_exists("password", $_POST) )  $_SESSION["password"] = $_POST["password"];
if( ! Check_SU_Password($_SESSION["password"], "SystemChoose_Analyze", "") )
  die("Invalid password!");

$log_path = $DATA_PATH . "SystemChoose_Course_Req/";

if( array_key_exists("log_id", $_POST) )	$log_id = $_POST['log_id'];
else										$log_id = $_GET['log_id'];

//echo "log_id = $log_id<BR>\n";

$log["file"]	= Verify_Specific_Data($log_id, "int", 12, 0);
$log["year"]	= substr($log_id, 0, 4);
$log["month"]	= substr($log_id, 4, 2);
$log["day"]		= substr($log_id, 6, 2);
$log["hour"]	= substr($log_id, 8, 2);
$log["min"]		= substr($log_id, 10, 2);
$log["id"]		= $log_id;
$log["file"]	= $log_path . $log_id . ".log";

$all_teachers = Read_All_Teacher();
$result = Parse_Log_File($log);

if( !array_key_exists("sort", $_GET) )	$_GET['sort'] = 'cid';
if( array_key_exists('sort', $_GET) and ($_GET['sort'] == 'diff') )			usort($result, "Sort_By_Diff");
else if( array_key_exists('sort', $_GET) and ($_GET['sort'] == 'ratio') )	usort($result, "Sort_By_Ratio");

$sort_by_cid_html = "<A href='SystemChoose_Analyze02.php?log_id=$log_id&sort=cid'>"
    . "<IMG src='../../../Graph/icon-arrow-down-b-128.png' width=20 height=20></A>";
$sort_by_diff_html = "<A href='SystemChoose_Analyze02.php?log_id=$log_id&sort=diff'>"
    . "<IMG src='../../../Graph/icon-arrow-down-b-128.png' width=20 height=20></A>";
$sort_by_ratio_html = "<A href='SystemChoose_Analyze02.php?log_id=$log_id&sort=ratio'>"
    . "<IMG src='../../../Graph/icon-arrow-down-b-128.png' width=20 height=20></A>";

$sort_field_highlight[$_GET['sort']] = " bgcolor='YELLOW'";

$log_date_text = implode("/", array($log["year"], $log["month"], $log["day"]));
echo "
  <CENTER>
    <H1>
	  課程需求分析（根據 $log_date_text 的限修篩選記錄）
	</H1>
    <HR>
  <P>
  <TABLE border=1>
    <TR>
	  <TH>系所</TH>
	  <TH " . $sort_field_highlight['cid'] . ">科目代碼 $sort_by_cid_html</TH>
	  <TH>班別</TH>
	  <TH>科目名稱</TH>
	  <TH>學分數</TH>
	  <TH>限修人數</TH>
	  <TH>保留人數</TH>
	  <TH>篩選前</TH>
	  <TH>篩選後</TH>
	  <TH " . $sort_field_highlight['diff'] . ">落選人數 $sort_by_diff_html</TH>
	  <TH " . $sort_field_highlight['ratio'] . ">需求/供給比例 $sort_by_ratio_html</TH>
	</TR>
";
//print_r($result);
$bgcolors_tr = array("#FFFFFF", "#EEEEEE");
$dept_last = ""; $i=0;

foreach( $result as $res ) {
  if( $dept_last != $res['dept_id'] )  {
	$dept_last = $res['dept_id'];
	$i++;
  }
 
  $bgcolor_tr = $bgcolors_tr[$i%2];
  //if( $res['diff'] > 0 )	$bgcolor_td = "bgcolor='YELLOW'";
  //else						$bgcolor_td = "";
  
  echo "
    <TR bgcolor='$bgcolor_tr'>
	  <TD>" . $res['dname']. "</TD>
	  <TD>" . $res['cid']. "</TD>
	  <TD>" . $res['grp']. "</TD>
	  <TD>" . $res['cname']. "</TD>
	  <TD>" . $res['credit']. "</TD>
	  <TD>" . $res['limit']. "</TD>
	  <TD>" . $res['reserved']. "</TD>
	  <TD>" . $res['before']. "</TD>
	  <TD>" . $res['after']. "</TD>
	  <TD $bgcolor_td>" . $res['diff']. "</TD>
	  <TD>" . $res['ratio']. "%</TD>
	</TR>
  ";
}

///////////////////////////////////////////////////////////////////////////////////////////////////
/////  讀取某個時間點的篩選記錄檔，抓取每一門科目的相關資料
function Parse_Log_File($log)
{
  //global $result;
  $FP = fopen($log["file"], "r");
  
  $param_line = fgets($FP, 1024);		///  第一行是篩選參數
  $i=0;
  while( $row = fgets($FP, 1024) ) {
	$row = rtrim($row);
	list($dept_id,$cid,$grp,$limit,$reserved,$before,$after) = explode("\t", $row);
	
	$result[$i]["cid"]		= $cid;
	$result[$i]["grp"]		= $grp;
	$result[$i]["dept_id"]	= $dept_id;
	$result[$i]["limit"]	= $limit;
	$result[$i]["reserved"]	= $reserved;
	$result[$i]["before"]	= $before;
	$result[$i]["after"]	= $after;
	$result[$i]["diff"]		= $before - $after;
	$result[$i]["ratio"]	= round(100*$before/$limit, 1);
	
	// if( $cid == "7301036" ) {
		// echo "[dept_id, cid, grp] = [$dept_id, $cid, $grp]<BR>\n";
	// }
	
	//$course = Read_Course($dept_id, $cid, $grp, "history");
	$course = Read_Course($dept_id, $cid, "01", "history");			///  因為篩選記錄不見得是本學期，在此抓取歷年資料，且 $grp='01'
	
	$result[$i]["cname"]			= $course['cname'];
	$dept = Read_Dept($dept_id);
	$result[$i]["dname"]			= $dept['cname2'];
	$result[$i]["credit"]			= $course['credit'];
		
	//$result[$i]["teacher_string"]	= Format_Teacher_String($course["teacher"]);		///  因為 course 抓的是歷年開課資料，此處不便抓教師
	
	$i++;
  }
  return $result;
}
///////////////////////////////////////////////////////////////////////////////////////////////////
/////  以「落選人數」排序（大到小）
/////  若落選人數相同，則以 (篩選後人數/限修人數) 排序（大到小）
function Sort_By_Diff($a, $b)
{
  if( $a['diff'] > $b['diff'] )		return -1;
  else if( $a['diff'] < $b['diff'])	return 1;
  else 
	return ($a['after']/$a['limit'] > $b['after']/$b['limit']) ? -1 : 1;  
}
///////////////////////////////////////////////////////////////////////////////////////////////////
/////  以「需求/供給比例」排序（大到小）
/////  若比例相同，則以落選人數排序（大到小）
function Sort_By_Ratio($a, $b)
{
  if( $a['ratio'] > $b['ratio'] )		return -1;
  else if( $a['ratio'] < $b['ratio'])	return 1;
  else 
	return ($a['diff'] > $b['diff']) ? -1 : 1;  
}

?>