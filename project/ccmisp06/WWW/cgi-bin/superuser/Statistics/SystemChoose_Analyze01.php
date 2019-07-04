<meta http-equiv="Content-Type" content="text/html; charset=utf-8">

<?PHP

//////////////////////////////////////////////////////////////////////////////////////////
/////  SystemChoose_Analyze01.php
/////  系統（限修）篩選紀錄檔分析
/////  為瞭解各系課程需求人數，於每次限修人數篩選時，額外紀錄每一門課篩選前後的選修人數，並分析之。
/////  第一頁：選擇要分析哪一次的篩選記錄
/////  Updates:
/////    2016/03/01 Created by Nidalap :D~

require_once "../../library/Reference.php";
require_once $LIBRARY_PATH . "Error_Message.php";
require_once $LIBRARY_PATH . "Common_Utility.php";
require_once $LIBRARY_PATH . "System_Settings.php";
require_once $LIBRARY_PATH . "Dept.php";
require_once $LIBRARY_PATH . "Password.php";

//echo Include_jQuery(1);
$DEBUG = 0;

session_start();
if( array_key_exists("password", $_POST) )  $_SESSION["password"] = $_POST["password"];
if( ! Check_SU_Password($_SESSION["password"], "SystemChoose_Analyze", "") )
  die("Invalid password!");

$log_path = $DATA_PATH . "SystemChoose_Course_Req/";
$dh = opendir($log_path);

$i = 0;
while( $file = readdir($dh) ) {
  //echo $file . "<BR>\n";
  if( !preg_match("/^\d{12}\.log$/", $file) )	continue;
  
  $logs[$i]["year"]		= substr($file, 0, 4);
  $logs[$i]["month"]	= substr($file, 4, 2);
  $logs[$i]["day"]		= substr($file, 6, 2);
  $logs[$i]["hour"]		= substr($file, 8, 2);
  $logs[$i]["min"]		= substr($file, 10, 2);
  $logs[$i]["id"]		= substr($file, 0, 12);

  $i++;
}
sort($logs);

echo "
  <CENTER>
    <H1>課程需求分析（依限修篩選紀錄）</H1>
    <HR>
  <P>
  <FORM action='SystemChoose_Analyze02.php' method='POST'>
    <DIV align='LEFT' style='width:300px'>
    請選擇要分析的篩選紀錄檔：
    <P>
";

foreach( $logs as $log ) {
  echo "<INPUT type='radio' name='log_id' value='" . $log['id'] . "'>";
  echo $log['year'] . "/" . $log['month'] . "/" . $log['day'] . " " . $log['hour'] . ":" . $log['min'] . "<BR>\n";
}
echo "
      </DIV>	  
	  <INPUT type='SUBMIT' value='開始分析'>
    </FORM>	
";

?>