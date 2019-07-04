<?PHP

//////////////////////////////////////////////////////////////////////////////////
/////  Course_Data.php
/////  （由資工所 CCULife iOS 系統）傳入課程代碼、班別、學年、學期等資訊，
/////  回傳課程開課詳細資料。
/////  2016/08/26  Created by Nidalap :D~

require_once "../library/Reference.php";
require_once $LIBRARY_PATH . "Database.php";
require_once $LIBRARY_PATH . "Common_Utility.php";
require_once $LIBRARY_PATH . "Dept.php";
require_once $LIBRARY_PATH . "Course.php";
require_once $LIBRARY_PATH . "Password.php";
require_once $LIBRARY_PATH . "Teacher.php";
require_once $LIBRARY_PATH . "Student_Course.php";
require_once $LIBRARY_PATH . "Error_Message.php";


//echo "<meta http-equiv='content-type' content='text/html; charset=utf-8'/>";

$system_settings = Get_System_State();
$debug = 0;

$query		= Verify_Specific_Data($_REQUEST['query'], "text", 300);
$year		= $_REQUEST['year'] ? Verify_Specific_Data($_REQUEST['year'], "year") : $YEAR;
$term		= $_REQUEST['term'] ? Verify_Specific_Data($_REQUEST['term'], "term") : $TERM;

$courses = Process_Query_String($query);
if( $debug ) {
  echo "[year, term] = [$year, $term]<BR>\n";
  echo "query = ";  print_r($query);  echo "<BR>\n";
  echo "courses = ";  print_r($courses);  echo "<BR>\n";
}

$course_dept = Read_All_Course_Dept("history");
$all_teachers = Read_All_Teacher();

$json = "
  {
	'result': [
";

foreach( $courses as $cour ) {
  $cid = $cour['cid'];
  $grp = $cour['grp'];
  
//  echo $course_dept[$cid]['dept_id'] . ", $cid, $grp<BR>\n";
  $c = Read_Course($course_dept[$cid]['dept_id'], $cid, $grp, $year, $term);
  
  $teacher_string = Format_Teacher_String($c['teacher']);
  $time_string = Format_Time_String($c['time']);
  
  $json .= "
      {
		'grade'		: '" . $c['grade'] . "',
		'id'		: '" . $c['id'] . "',
		'chtTitle'	: '" . $c['cname'] . "',
		'engTitle'	: '" . $c['ename'] . "',
		'teacher'	: '$teacher_string',
		'credit'	: '" . $c['credit'] . "',
		'credit_attr':  '" . $c['property'] . "',
		'time'		: '$time_string',
		'classroom'	: '" . $c['classroom'] . "',
		'limit'		: '" . $c['number_limit'] . "'
	  }
  ";
  
}

$json .= "
    ]
  }
";

echo $json;

//////////////////////////////////////////////////////////////////////////////////////////////////////////
function Process_Query_String($query)
{
  $courses = array();
  $i = 0;
  foreach($query as $cid_grp) {
	if( $cid_grp == "" )  continue;
	list($cid, $grp) = explode("_", $cid_grp);
	
	Verify_Specific_Data($cid, "coursecd");
	Verify_Specific_Data($grp, "group");
	
	$courses[$i++] = array("cid" => $cid, "grp" => $grp);
  }
  return $courses;
}

?>