<?PHP

//////////////////////////////////////////////////////////////////////////////////
/////  Course_Vacancy.php
/////  （由校際選課系統）傳入課程代碼、班別、開課系所，及其他安全檢查資訊，
/////  回傳此課程目前尚可選修人數等資訊，供判斷校際生選課是否需加簽。
/////  回傳資料：
/////    若有開課資料: (開課限修人數 - 目前選課人數), 開課限修人數, 目前選課人數
/////    若無開課資料: -1
/////  2016/04/18 Created by Nidalap :D~
/////  2016/05/18 若找不到開課資料，則回傳 -1。  by Nidalap :D~
/////  2016/08/31 不只回傳可加選人數，改為回傳可加選人數、限修人數、目前選課人數。 by Nidalap :D~

require_once "../library/Reference.php";
require_once $LIBRARY_PATH . "Database.php";
require_once $LIBRARY_PATH . "Common_Utility.php";
require_once $LIBRARY_PATH . "Dept.php";
require_once $LIBRARY_PATH . "Course.php";
require_once $LIBRARY_PATH . "Password.php";
require_once $LIBRARY_PATH . "Student_Course.php";
require_once $LIBRARY_PATH . "Error_Message.php";

$system_settings = Get_System_State();

$cour_id	= Verify_Specific_Data($_REQUEST['cour_id'], "course_id");
$grp		= Verify_Specific_Data($_REQUEST['grp'], "grp");
$password	= Verify_Specific_Data($_REQUEST['password'], "text", 20);
$key		= Verify_Specific_Data($_REQUEST['key'], "text", 20);

//die("2,60,58");


if( array_key_exists("dept_id", $_REQUEST) ) {			///  如果傳入了系所代碼，使用此資料
  $dept_id	= Verify_Specific_Data($_REQUEST['dept_id'], "dept_id");
}else{													///  如果沒有傳入開課系所代碼，這裡幫忙找出來（比較慢）
  $all_course_dept = Read_All_Course_Dept();
  $dept_id = $all_course_dept[$cour_id]["dept_id"];
  
  //print_r($all_course_dept);
  
  if( !array_key_exists($cour_id, $all_course_dept) ) {	///  如果找不到系所（開課資料不存在），回傳 -1
	echo "-1";
	die();
  }
}

//Check_Key($key, $cour_id.$grp, $password);			///  安全檢查: 檢查 $key 是否正確
//Check_Source_URL();									///  安全檢查: 檢查來源頁面 URL

//echo "$id, $password<br>\n";
//echo '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">';

//echo "[$dept_id, $cour_id, $grp]<BR>\n";

$course = Read_Course($dept_id, $cour_id, $grp);		///  抓取開課資料

if( preg_match("/FONT color/", $course['cname']) ) {	///  如果找不到系所（開課資料不存在），回傳 -1
  echo "-1";
  die();
}
//print_r($course);

$stu_in_cour = Student_in_Course($cour_id, $grp);		///  抓取目前選課名單
$stu_in_cour = count($stu_in_cour);						///  目前選課人數

$vacancy = $course["number_limit"] - $stu_in_cour;

if( $vacancy < 0 )  $vacancy = 0;

$vacancy_str = implode(",", array($vacancy, $course["number_limit"], $stu_in_cour));
echo $vacancy_str;
  
?>