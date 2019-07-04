<?PHP
/////  Teacher_Course02.cgi
/////  教師查詢當學期一般生與碩士在職專班授課明細
/////  此功能不從教師專業系統連結過來，因為該系統不給兼任教師使用。
/////  Updates: 
/////	2016/01/12 Created by Nidalap :D~
///////////////////////////////////////////////////////////////////////////
//print("Content-type:text/html\n\n");

require_once "../library/Reference.php";
require_once $LIBRARY_PATH."Database.php";
require_once $LIBRARY_PATH."Common_Utility.php";
require_once $LIBRARY_PATH."Dept.php";
require_once $LIBRARY_PATH."Course.php";
require_once $LIBRARY_PATH."Password.php";
require_once $LIBRARY_PATH."Error_Message.php"; 
require_once $LIBRARY_PATH."Teacher.php";
require_once $LIBRARY_PATH."Classroom.php";
require_once $LIBRARY_PATH."System_Settings.php";

///////////////////////////////////////////////////////////////////////////

echo $EXPIRE_META_TAG;

//foreach($_POST as $k => $v) {
//  echo "$k -> $v <BR>\n";
//}

$teacher_id	= Verify_Specific_Data($_POST['teacher_id'], "person_id", "身份證號");
$password	= Verify_Specific_Data($_POST['password'], "person_password", "密碼");
$last_semester = Verify_Specific_Data($_POST['last_semester'], "int", "學年學期", 1);

//$teacher_id = 'R122389443';  $password	= "truck";
//$teacher_id = 'F203572458';  $password	= "syuxxzt";

list($year, $term) = Last_Semester($last_semester);

//echo "last, year, term = $last_semester, $year, $term<BR>\n";

//if ( !Check_Teacher_Password($teacher_id, $password) )  
//	Error_Msg("帳號或密碼輸入錯誤！請輸入您的行政自動化帳號與密碼。");
//echo  "id = $teacher_id<BR>\n";

$classroom = Read_Classroom();

Switch_To_GRA(0);
$teacher_course_temp1 = Get_Teacher_Courses($teacher_id, $year, $term);
Switch_To_GRA(1);
//echo ("reference path = $REFERENCE_PATH<BR>\n");  echo ("course path = $COURSE_PATH<BR>\n");
//$teacher_course = array_merge($teacher_course, Get_Teacher_Courses($teacher_id));
$teacher_course_temp2 = Get_Teacher_Courses($teacher_id, $year, $term);

//$teacher_course = array_merge($teacher_course_temp1, $teacher_course_temp2);
$teacher_course = $teacher_course_temp1;
foreach ($teacher_course_temp2 as $temp) {		///  不知為何 array_merge 沒作用，所以這樣結合一般和專班課程
  $teacher_course[] = $temp;
}

//echo "<HR>\n"; print_r($teacher_course_temp1);
//echo "<HR>\n"; print_r($teacher_course_temp2);

$course_HTML = Create_Course_HTML($teacher_course);

echo "
    <html>
      <head>
        $EXPIRE_META_TAG
        <title>教師查詢當學期授課明細</title> 
      </head>
      <body background=$GRAPH_URL/ccu-sbg.jpg>
        <center>
         <img src=$GRAPH_URL/open.jpg><P>
		 <H1>教師查詢當學期授課明細</H1>
		 <HR>
		 教授您好，以下是您在 $year 學年度第 $term 學期所開設之課程：<P>
		 $course_HTML
		 <P>
		 <A href='http://kiki.ccu.edu.tw/ccu_timetable.doc' target='NEW'>上課時間表</A>
		 <P>
		 <button onclick='javascript:history.back()'>回上頁</button>
	  </BODY>
	</HTML>
";

//print_r($teacher_course);
 
//Switch_To_GRA(0);
//echo ("reference path = $REFERENCE_PATH<BR>\n");
//echo ("course path = $COURSE_PATH<BR>\n");


/*

/////////////////////////////////////////////////////////////////////////////
//////  由輸入的 year, term 判斷是否要讀取本學期資料, 或是以前的資料
if( $Input{year} != "" ) {
  $year = $Input{year};
}else{
  $year = $YEAR;
}

if( $Input{term} != "" ) {
  $term = $Input{term};
}else{
  $term = $TERM;
}

//if( ($year==$YEAR) and ($term==$TERM) ) {
//  $yearterm = "";
//}else{
//  $yearterm = $year . $term;
//}
//print("session_id, id, pass = $Input{session_id}, $id, $Input{password}<BR>"); 

/////////////////////////////////////////////////////////////////////////////

*/


/*
Switch_To_GRA(1);
print("reference path = $REFERENCE_PATH<BR>\n");
print("course path = $COURSE_PATH<BR>\n");

Get_Teacher_Courses();
 
Switch_To_GRA(0);
print("reference path = $REFERENCE_PATH<BR>\n");
print("course path = $COURSE_PATH<BR>\n");

foreach $cou (@teacher_course) {
  print "$$cou{'id'} - $$cou{'group'}<BR>\n";
}

/////////////////////////////////////////////////////////////////////////////////
sub Print_BAN()
{
  my($msg) = @_;
  if( $msg eq "key_error" ) {
    $msg_show = "驗證碼錯誤，<FONT color=RED>請回上一頁重新讀取</FONT>，以更新驗證碼！";
  }else{
    $msg_show = "";
  }
  
  print qq(
    <html>
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <TITLE>國立中正大學$SUB_SYSTEM_NAME選課系統--檢視目前已選修科目</TITLE>
    </head>
    <body background="$GRAPH_URL./ccu-sbg.jpg">
    <center>
      <FONT face="標楷體">
        <H1>國立中正大學$SUB_SYSTEM_NAME選課系統--檢視目前已選修科目</H1>
      </FONT>
    <HR>
    $msg_show<BR>
  );
  die();
}
*/
////////////////////////////////////////////////////////////////////////////////////////////////
function Get_Teacher_Courses($in_teacher_id, $year, $term)
{
  global $REFERENCE_PATH, $classroom;
  
  if( preg_match("/06/", $REFERENCE_PATH) )	$is_GRA = "一般";
  else										$is_GRA = "專班";
  
  $i = 0;
  $all_dept = Find_All_Dept();
  foreach($all_dept as $dept_id) {
   //echo "dept = $dept_id<BR>\n";
   $dept = Read_Dept($dept_id);
   $courses = Find_All_Course($dept_id, "", $year, $term);
   foreach( $courses as $course ) {
     $cour = Read_Course($dept_id, $course['id'], $course['grp'], $year, $term);
	 //print_r($cour['teacher']);
	 $time_string = Format_Time_String($cour['time']);
	 
	 foreach ($cour['teacher'] as $teacher) {
	   //echo "$teacher<BR>\n";
	   //echo "$teacher found in $dept_id - " . $course['id'] . " - " . $course['grp'] . '<BR>\n';
	   //print_r($classroom[$cour['classroom']]);
	   
	   if( $teacher == $in_teacher_id) {
	      $teacher_course[$i++] = array(
			'id'			=> $cour['id'], 
			'group'			=> $cour['group'], 
			'credit'		=> $cour['credit'], 
			'cname'			=> $cour['cname'], 
			'time'			=> $cour['time'], 

			'dept_cname'	=> $dept['cname'],
			'time_string'	=> $time_string,
			'is_GRA'		=> $is_GRA,
			'classroom'		=> $classroom[$cour['classroom']]['cname']
		  );
	   }
	 }
	 //print_r($cour);
   }
 }
// print_r($teacher_course);
 return $teacher_course;
}

////////////////////////////////////////////////////////////////////////////////////////////////

function Switch_To_GRA($switch)
{
  global $REFERENCE_PATH, $COURSE_PATH;
  
  $debug = 0;
  if($debug) echo "<HR>\n";
  if($debug) echo "COU PATH now $COURSE_PATH<BR>\n";
  
  if( $switch == 1 ) {
	$REFERENCE_PATH = preg_replace("/ccmisp../", "ccmisp07", $REFERENCE_PATH);
	$COURSE_PATH	= preg_replace("/ccmisp../", "ccmisp07", $COURSE_PATH);
	if($debug) echo "switch = 1<BR>\n";
  }else{
	$REFERENCE_PATH = preg_replace("/ccmisp../", "ccmisp06", $REFERENCE_PATH);
	$COURSE_PATH	= preg_replace("/ccmisp../", "ccmisp06", $COURSE_PATH);
	if($debug) echo "switch = 0<BR>\n";
  }
  if($debug) echo "COU PATH now $COURSE_PATH<BR>\n";
  if($debug) echo "<HR>\n";
}
//////////////////////////////////////////////////////////////////////////////////////////////////
function Create_Course_HTML($teacher_course)
{
  if( count($teacher_course) == 0 ) {
	$html = "<H1>查無您在本學期的開課資料！</H1><BR>\n";
	return $html;
  }

  $html = "
    <TABLE border=1 width='75%'>
	  <TR>
	    <TH>一般/專班</TH>
	    <TH>開課系所</TH>
	    <TH>科目代碼</TH>
		<TH>班別</TH>
		<TH>科目名稱</TH>
		<TH>學分數</TH>
		<TH>上課時間</TH>
		<TH>上課教室</TH>
	  </TR>
  ";
  
  foreach( $teacher_course as $cour ) {
	$html .= "<TR>";
	$html .= "<TH>" . $cour['is_GRA'] ."</TH>";
	$html .= "<TH>" . $cour['dept_cname'] ."</TH>";
	$html .= "<TH>" . $cour['id'] . "</TH>";
	$html .= "<TH>" . $cour['group'] ."</TH>";
	$html .= "<TH>" . $cour['cname'] ."</TH>";
	$html .= "<TH>" . $cour['credit'] ."</TH>";
	$html .= "<TH>" . $cour['time_string'] ."</TH>";
	$html .= "<TH>" . $cour['classroom'] ."</TH>";
	$html .= "</TR>";
  }
  $html .= "</TABLE>";
  return $html;
}


?>