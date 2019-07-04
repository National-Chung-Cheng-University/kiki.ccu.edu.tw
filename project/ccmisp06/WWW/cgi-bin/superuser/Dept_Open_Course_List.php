<meta http-equiv="Content-Type" content="text/html; charset=utf-8">

<?PHP

//////////////////////////////////////////////////////////////////////////////////////////
/////  Dept_Open_Course_List.php
/////  系所開課狀態列表
/////  列出各系最近開課時間，用以判斷各系開課/異動與否
/////  Updates:
/////    2015/02/04 Created by Nidalap :D~

require_once "../library/Reference.php";
require_once $LIBRARY_PATH . "Error_Message.php";
require_once $LIBRARY_PATH . "Common_Utility.php";
require_once $LIBRARY_PATH . "System_Settings.php";
require_once $LIBRARY_PATH . "Session.php";
require_once $LIBRARY_PATH . "Dept.php";

$DEBUG = 0;
$threshold = 60*60*24*7*2;		///  最後一次更新開課資料的日期，若超過此時間則顯示為紅字。預設為兩週

session_start();

$now = time();

echo "
  <CENTER>
    <H1>各系開課狀態一覽表</H1>
    <TABLE border=1>
";
$depts = Find_All_Dept();
foreach ($depts as $dept_id) {
  $dept = Read_Dept($dept_id);
  
  $classindex_file = $DATA_PATH . "Course/" . $dept_id . "/classindex";
  $stat = stat($classindex_file);
  
  $diff = $now - $stat["mtime"];		///  classindex 檔案有多久沒更改了
  $date = date("Y/m/d", $stat["mtime"]);
  if( $diff > $threshold ) {
	if( $stat["mtime"] == 0 ) {
	  $date = "<FONT color='RED'>尚未開課</FONT>";
	}
	$date = "<FONT color='RED'>" . $date . "</FONT>";
  }
  
  echo "<TR><TD>" . $dept["cname"] . "</TD><TD>$date</TD></TR>";
  //echo $dept{"cname"} . "<BR>\n";
}



?>
