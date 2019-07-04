<?PHP
//////////////////////////////////////////////////////////////////////////////////////////
/////  My_Plan_Course.php
/////  學生「我的選課計畫」畫面
/////  選課系統抓取課程地圖系統的選課計畫資料，提醒學生當學期開設的計畫中課程，建議加選。
/////  Updates:
/////    2011/11/27 Created by Nidalap :D~

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
require_once $LIBRARY_PATH . "Grade.php";
require_once $LIBRARY_PATH . "Student_Course.php";
require_once $LIBRARY_PATH . "English.php";

session_start();
$smarty = init_smarty(3);
$DBH = PDO_connect();           ///  連到 academic_kiki 資料庫

$session_id     = quotes($_GET["session_id"]);
$session        = Read_Session($session_id);
Renew_Session($session_id);
$stu = Read_Student($session["id"]);
$dept = Read_Dept($stu["dept"]);
if( Check_SU_Password($session["password"], "", $stu["id"]) ) {
  $_SESSION["SUPERUSER"] = 1;           ///  檢查 SU password
}else{
  unset($_SESSION["SUPERUSER"]);
}
  if( $IS_ENGLISH ) {
    $HEAD_DATA = Form_Head_Data($stu["id"], $stu{"ename"}, $dept{"ename"}, $stu{"grade"}, $stu{"class_"});
  }else{
    $HEAD_DATA = Form_Head_Data($stu["id"], $stu{"name"}, $dept{"cname"}, $stu{"grade"}, $stu{"class_"});
  }
if( $stu["id"] == "999999999" ) {
  $my_plan_course = Get_My_Plan_Course("guest");
}else{
  $my_plan_course = Get_My_Plan_Course($stu["id"]);
}

$sel_status_code = array(
  0=>"",
  1=>"<IMG src='../../Graph/O.gif' width=16 height=16>",
  2=>"<IMG src='../../Graph/Checked_blue.gif' width=16 height=16>"
);

$txt = Init_Text_Values();

$smarty->assign("IS_ENGLISH", $IS_ENGLISH);
$smarty->assign("sel_status_code", $sel_status_code);
$smarty->assign("session_id", $session_id);
$smarty->assign("my_plan_course", $my_plan_course);
$smarty->assign("HEAD_DATA", $HEAD_DATA);
$smarty->assign("txt", $txt);
$smarty->display("class/My_Plan_Course.tpl");

//////////////////////////////////////////////////////////////////////////////////////////////
/////  因應英文版本，將所有要顯示的文字在此整理，依照 $IS_ENGLISH 自動判別  2013/08/08
function Init_Text_Values()
{
    global $IS_ENGLISH;
	
	$txtall = array(
	  'title'		=> array('c'=>'我的選課計畫', 'e'=>'My Course Plans'), 
	  'not_yet'		=> array('c'=>'我尚未建立選課計畫，來去 
								<A href="http://coursemap.ccu.edu.tw/" target="_NEW">課程地圖系統</A>建立！',
						     'e'=>'I have not yet established a course selection plan. Establish one in the 
							   <A href="http://coursemap.ccu.edu.tw/" target="_NEW">course map system</A>!'),
	  'note1'		=> array('c'=>'我在<A href="http://coursemap.ccu.edu.tw/" target="_NEW"
								課程地圖系統</A>中擬定的選課計畫，其中以下科目在本學期有開課（點選科目名稱以加選）：',
						     'e'=>'The following courses are in my course plans (from 
								<A href="http://coursemap.ccu.edu.tw/" target="_NEW">the Course Map System</A>) 
								and are available this semester. Click on the course title to add.'),
	  'status'		=> array('c'=>'加選狀態', 'e'=>'Status'),
	  'dept'		=> array('c'=>'開課系所', 'e'=>'Department'),
	  'grade'		=> array('c'=>'開課年級', 'e'=>'Year Standing'),
	  'cid'			=> array('c'=>'科目代碼', 'e'=>'Course ID'),
	  'cname'		=> array('c'=>'科目名稱', 'e'=>'Course Title'),
	  'note2'		=> array('c'=>'「加選狀態說明」：
								<IMG src="../../Graph/O.gif" width=16 height=16>：本學期已加選
								<IMG src="../../Graph/Checked_blue.gif" width=16 height=16>：過去已選修並通過',
						     'e'=>'Notes on status：
								<IMG src="../../Graph/O.gif" width=16 height=16>: Already added in this semester
								<IMG src="../../Graph/Checked_blue.gif" width=16 height=16>: Already added and passed before'),

	  'submit'		=> array('c'=>'確認更改', 
							 'e'=>'Change My Password')
 
	);

	foreach( $txtall as $k=>$v ) {
	  if( $IS_ENGLISH )	{
	    $txt[$k] = $v['e'];
		if( isset($v['url']) ) {
		  if( strstr($v['url'], "?") )
		    $txt[$k."_url"] = $v['url'] . "&e=1";
		  else
		    $txt[$k."_url"] = $v['url'] . "?e=1";
		}
	  }else{
	    $txt[$k] = $v['c'];
		if( isset($v['url']) )
		  $txt[$k."_url"] = $v['url'];
	  }
	}	
    return $txt;
}
?>

