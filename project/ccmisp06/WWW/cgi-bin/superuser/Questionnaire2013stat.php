<?PHP
  ///////////////////////////////////////////////////////////////////////////////////////////
  /////  Questionnaire2013stat.php
  /////  2013選課改制意見調查統計(中正大學選課系統暨通識篩選原則意見調查統計表)
  /////  2013/09 為調查同學對於因通識課程而起的選課制度改革意見，提供問卷的統計。
  /////  Updates:
  /////    2013/09/02 Created by Nidalap :D~
  
  require_once "../php_lib/Reference.php";
  require_once $LIBRARY_PATH . "Common_Utility.php";
  require_once $LIBRARY_PATH . "Session.php";
  require_once $LIBRARY_PATH . "Password.php";
  require_once $LIBRARY_PATH . "Database.php";
  require_once $LIBRARY_PATH . "Student.php";
  require_once $LIBRARY_PATH . "Dept.php";
  
  global $BG_PIC;
  
  if( ! Check_SU_Password($_POST["password"], "Questionnaire2013stat", "") )
    die("Invalid password!");
  
  $DBH = PDO_connect($KIKI_DB_NAME);
  //$DBH_a = PDO_connect($DATABASE_NAME);
  $sql = "SELECT * FROM questionnaire2013";
  $STH = $DBH->query($sql);
  $quesAll = $STH->fetchAll(PDO::FETCH_ASSOC);
  //$allstu = Find_All_Student();
  $ques = array();
  
  foreach( $quesAll as $quesTemp ) {
	$stu_grade = Find_Grade($quesTemp['stu_id']);
	
//	if( $stu_grade == 0 ) {
//	  die($quesTemp['stu_id']);
//	}
	
	if( $quesTemp['q1'] == ' ' )  $quesTemp['q1'] = 0;
	if( $quesTemp['q2'] == ' ' )  $quesTemp['q2'] = 0;
	if( $quesTemp['q3'] == ' ' )  $quesTemp['q3'] = 0;
	
    $ques['q1'][$stu_grade][$quesTemp['q1']] ++;			///  第一題此年級填答此選項人數++
	$ques['q2'][$stu_grade][$quesTemp['q2']] ++;
	$ques['q3'][$stu_grade][$quesTemp['q3']] ++;
	
	$ques['q1']['all_grade'][$quesTemp['q1']] ++;			///  第一題所有年級填答此選項人數++
	$ques['q2']['all_grade'][$quesTemp['q2']] ++;			///  第一題所有年級填答此選項人數++
	$ques['q3']['all_grade'][$quesTemp['q3']] ++;			///  第一題所有年級填答此選項人數++
	
	$ques['grade_sum'][$stu_grade]++;						///  此年級人數++
	
	//$ques['q3'][$stu_grade]['subtotal']++;
	
	if( $quesTemp['q1_note'] )  $ques['q1']['note'][] = $quesTemp['q1_note'];		///  紀錄文字意見
	if( $quesTemp['q2_note'] )  $ques['q2']['note'][] = $quesTemp['q2_note'];
	if( $quesTemp['q3_note'] )  $ques['q3']['note'][] = $quesTemp['q3_note'];
	
  }
  
  usort($ques['q1']['note'], "Sort_By_Wcount");				///  文字意見由長到短排序
  usort($ques['q2']['note'], "Sort_By_Wcount");
  usort($ques['q3']['note'], "Sort_By_Wcount");
  //sort($ques['q1']['note']);
  
  //print_r($ques);
	
  //Sort_Ques();
  

  
?>

<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <TITLE>2013選課改制意見調查統計</TITLE>
</head>
<body background=<?PHP echo $BG_PIC; ?>>
<center>
  <H2>2013選課改制意見調查統計</H2>
  <HR>

<?PHP  
  //echo "ques = ";  print_r($ques);
  $ques['q1']['q'] = "一、第一階段改三次篩選。";
  $ques['q2']['q'] = "二、第二階段選課擬由第一週篩選及第二週先選先贏，改為每日三段式選課。";
  $ques['q3']['q'] = "三、通識二至五領域篩選原則，擬由隨機亂數篩選修改為權重篩選。";
  
  print "
    <TABLE BORDER=1>
	  <TR><TH rowspan=2>題目</TH><TH rowspan=2>選項</TH><TH colspan=6>統計</TH></TR>
	  <TR><TH>大二</TH><TH>大三</TH><TH>大四</TH><TH>總和</TH><TH>%</TH></TR>
  ";
  
//  foreach( $ques as $id => $q ) {
  foreach( array('q1', 'q2', 'q3') as $id ) {
    $q = $ques[$id];
	//print_r($q);
	//echo "<HR>\n";	
	echo 
	  "<TR>
	    <TD rowspan=5>" . $q['q'] . "</TD>
	    <TD>贊成</TD>
		<TD>" . $q[2][1] . "</TD>
		<TD>" . $q[3][1] . "</TD>
		<TD>" . $q[4][1] . "</TD>
		<TD>" . $q['all_grade'][1] . "</TD>
		<TD>" . 100*round($q['all_grade'][1]/array_sum($ques['grade_sum']),3) . "%</TD>
	   </TR>
	   	<TD>不贊成</TD>
		<TD>" . $q[2][2] . "</TD>
		<TD>" . $q[3][2] . "</TD>
		<TD>" . $q[4][2] . "</TD>
		<TD>" . $q['all_grade'][2] . "</TD>
		<TD>" . 100*round($q['all_grade'][2]/array_sum($ques['grade_sum']),3) . "%</TD>
	   </TR>
	   	<TD>其他</TD>
		<TD>" . $q[2][3] . "</TD>
		<TD>" . $q[3][3] . "</TD>
		<TD>" . $q[4][3] . "</TD>
		<TD>" . $q['all_grade'][3] . "</TD>
		<TD>" . 100*round($q['all_grade'][3]/array_sum($ques['grade_sum']),3) . "%</TD>
	   </TR>
	   	<TD>未填寫</TD>
		<TD>" . $q[2][0] . "</TD>
		<TD>" . $q[3][0] . "</TD>
		<TD>" . $q[4][0] . "</TD>
		<TD>" . $q['all_grade'][0] . "</TD>
		<TD>" . 100*round($q['all_grade'][0]/array_sum($ques['grade_sum']),3) . "%</TD>
	   </TR>
	   </TR>
	   	<TD>總和</TD>
		<TD>" . $ques['grade_sum'][2] . "</TD>
		<TD>" . $ques['grade_sum'][3] . "</TD>
		<TD>" . $ques['grade_sum'][4] . "</TD>
		<TD>" . array_sum($ques['grade_sum']) . "</TD>
		<TD>100%</TD>
	   </TR>
	  ";
  }
  
  print "
    </TR>
	<TR>
	  <TH colspan=7>各題意見：
	    <A href='#q1'>第一題</A>
		<A href='#q2'>第二題</A>
		<A href='#q3'>第三題</A>
	  </TH>
	</TR>
  ";
  
  
  foreach ( $ques as $qid=>$q ) {
    echo "<TR><TH colspan=7 style='background-color:yellow;'><A id='$qid'>意見（" . $ques[$qid]['q'] . "）</A></TH></TR>";
	foreach ($q['note'] as $note ) {
	  echo "<TR><TD colspan=7>" . $note . "</TD></TR>";
	}
  }
  echo "	  
	</TABLE>    
  ";
  
///////////////////////////////////////////////////////////////////////////////

function Sort_Ques()
{
  global $ques;
  sort($ques['q1']);
    sort($ques['q1'][0]);
	sort($ques['q1'][1]);
	sort($ques['q1'][2]);
	sort($ques['q1'][3]);
  sort($ques['q2']);
    sort($ques['q2'][0]);
	sort($ques['q2'][1]);
	sort($ques['q2'][2]);
	sort($ques['q2'][3]);
  sort($ques['q3']);
    sort($ques['q3'][0]);
	sort($ques['q3'][1]);
	sort($ques['q3'][2]);
	sort($ques['q3'][3]);
}  
///////////////////////////////////////////////////////////////////////////////
function Find_Grade($stu_id) 
{
  $stu_year = substr($stu_id, 1, 2);
  switch ($stu_year)
  {
    case '01':
	  $grade = '2';
	  break;
    case '00':
	  $grade = '3';
	  break;
	default:
	  $grade = '4';
  }
  return $grade;
}
///////////////////////////////////////////////////////////////////////////////
function Sort_By_Wcount($a, $b)
{
  if( $a == $b )
    return 0;
  else
    return (strlen($a) > strlen($b)) ? -1 : 1;
}

?>
  
  

