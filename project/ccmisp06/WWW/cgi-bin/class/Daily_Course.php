<?PHP
///////////////////////////////////////////////////////////////////////////////////
/////  Daily_Course.php
/////  今日課表
/////  顯示今天或者一週內特定日的課表，用於內嵌於學生入口網站
/////  Updates:
/////    2012/01/16 Created by Nidalap :D~
/////    2012/06/28 透過 $encoding 判斷輸出 BIG5 或 utf-8(Smarty樣板有兩個)  
/////               從 SSO 確實抓取 id 和 encoding 資料，
/////               以及選擇星期時不透過 GET 重抓，改採 javascript/css 呈現  Nidalap :D~
/////	 2012/07/26 修正課程沒有照時間排序的 BUG。   Nidalap :D~
/////    2012/09/20 加入判斷系統目前不允許查詢功能。若不允許查詢，則顯示錯誤訊息。 Nidalap :D~
/////    2012/10/16 若是 guest 帳號登入，則隨機顯示一名學生選課資料。  Nidalap :D~
/////    2012/12/06 若是開課期間，抓取「上學期」選課與開課資料。   Nidalap :D~
/////    2014/02/10 加入行動版相關判斷與畫面最佳化 by Nidalap :D~
/////    2015/11/10 為統計分析理由，呼叫了 Student_Log() 留下紀錄。  by Nidalap :D~
/////    2015/12/31 抓取「上學期」開課資料的判斷，改為課程異動前一律抓取之。  Nidalap :D~
/////    2015/12/31 新增資工系學生 APP 程式（黃仁紘的學生）server IP 進允入清單  Nidalap :D~

require_once "../library/Reference.php";
require_once $LIBRARY_PATH . "Database.php";
require_once $LIBRARY_PATH . "Common_Utility.php";
require_once $LIBRARY_PATH . "Course.php";
require_once $LIBRARY_PATH . "Classroom.php";
require_once $LIBRARY_PATH . "Dept.php";
require_once $LIBRARY_PATH . "Student.php";
require_once $LIBRARY_PATH . "Student_Course.php";
require_once $LIBRARY_PATH . "Session.php";

$system_settings = Get_System_State();
$smarty = init_smarty(3);

if( $system_settings{'sysstate'} == 0 ) {
  $allow_query = 0;					///  系統設定不允許查詢
}else{
  $allow_query = 1;
}

$session_id	= quotes($_GET["session_id"]);
if( $session_id ) {												/////  如果是從選課系統內部連過來
  $encoding = 'utf-8';
  $session = Read_Session($session_id);
  Renew_Session($session_id);
  $id = $session['id'];
  list($time_string, $time_string2) = gettime($session_data{'login_time'});	
  $student = Read_Student($id);
  $welcome_msg  =  $student['name'] . "同學，歡迎！<BR>\n";
  $welcome_msg .= "您本次的登入時間是:[$time_string2]";

  $smarty->assign("session_id", $session_id);
  $smarty->assign("welcome_msg", $welcome_msg);
}else{															/////  抓取 SSO 傳過來的變數
  $encoding = ($_GET["encoding"]=="utf8") ? "utf-8" : "BIG5";		///  判斷輸出字元集
  $id = $_GET["acc"];
  $source_ip = getIP();  
  /////  驗證 SSO 來源 IP
  if( ($source_ip != $IP_SSO_FORMAL) and ($source_ip != $IP_SSO_TEST) 
	 and ($source_ip != "140.123.105.125")
     and !preg_match("/^140.123.19.115/", $source_ip) ) {                  /// 我測試的後門！
    $msg = "請求資料來源有誤: $source_ip";
    die($msg);
  }
  ///  檢查 id 是否為學號
  if( $id == "guest" ) {					///  若是訪客登入，隨機抓一個學生課表
    $all_stu = Find_All_Student();
    $stu_count = count($all_stu);
    $id = $all_stu[rand(0, $stu_count)];
  }else{
    Validate_Input($id, "id");
  }
}

if( $allow_query == 0 ) {				///  將來要改為「僅查詢上次篩選後課表」 20120920
//  echo iconv("big5", "utf-8", "選課系統篩選中，暫時無法查詢。");
  echo "選課系統篩選中，暫時無法查詢。";
  die();
}

//echo "current_system_timeline = " . $system_settings["current_system_timeline"];

if( $system_settings["current_system_timeline"] <= 2 ) {		///  課程異動前，抓取「上學期」選課資料
  list($year, $term) = Last_Semester(1);
  $courses = Course_of_Student($id, $year, $term);
}else{ 															///  一般期間，抓取本學期選課資料
  $courses = Course_of_Student($id);
}

$days = array("", "一", "二", "三", "四", "五", "六", "日");
/*if( $encoding == "utf-8" ) {
  foreach( $days as $i=>$d ) {			///  將 days 轉換為 utf-8
    $days[$i] = iconv("big5", "utf-8", $d);
  }
}
*/

for( $i=1; $i<=7; $i++ ) {
  $schedule[$i] = "";
}

foreach($courses as $cour) {			///  讀取學生所有課程，建立每日課表資料
  if( $system_settings["current_system_timeline"] == 0 ) {		///  開課期間，抓取「上學期」開課資料
    $course = Read_Course($cour["dept"], $cour["id"], $cour["group"], $year, $term);
  }else{														///  一般期間，抓取本學期開課資料
    $course = Read_Course($cour["dept"], $cour["id"], $cour["group"]);
  }
  $classroom = Read_Classroom($course["classroom"]);
  if( $encoding == "utf-8" ) {			///  將課程、教室名稱轉換為 utf-8
    //$course["cname"]	= iconv("big5", "utf-8", $course["cname"]);
    //$classroom["cname"]	= iconv("big5", "utf-8", $classroom["cname"]);
  }
  foreach( $course["time"] as $time) {
    $schedule[$time["week"]][] =  array("time"		=> $TIME_TIME[$time["time"]], 
                                        "course"	=> $course["cname"],
                                        "classroom"	=> $classroom["cname"]);
  }
}
foreach( $schedule as $day=>$day_schedule ) {
  usort($day_schedule, "sort_day_schedule");
  $schedule[$day] = $day_schedule;
}

Student_Log("DailyCourse", $id, NULL, NULL, NULL, NULL);

$smarty->assign("days", $days);
$smarty->assign("schedule", $schedule);
if( $encoding == "utf-8" ) {			///  判斷該使用 BIG5 或是 utf-8 的 smarty 樣板
  $smarty->display("class/Daily_Course_utf8.tpl");
}else{
  $smarty->display("class/Daily_Course.tpl");
}
/////////////////////////////////////////////////////////////////////////////
/////  對某日的課表，依照上課時間排序
function sort_day_schedule($a, $b)
{
  return ( $a["time"] < $b["time"] ) ? -1 : 1;
}


?>