<?PHP 

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////  查詢修課學生名單
/////  判斷 Query_2.cgi 傳來的教師人事代碼以及科目代碼，列印該科目上課記事簿。
/////  Updates:
/////   2009/12/23 Created by Nidalap :D~
/////   2010/01/04 將原先讀取舊學期資料所傳入的 $yearterm 改為 $year 和 $term, 以避免民國百年 bug.  Nidalap
/////	2010/09/17 將教師人事代碼轉換為大寫  Nidalap :D~
/////   2010/09/23 改為：若是系所登入則檢查系所密碼，若是尚未登入則檢查上一頁傳來的教師身份證號  Nidalap :D~
/////	2016/07/15 從 perl 改寫 php 版本，並加入校際選課系統中選修的學生名單  Nidalap :D~
/////   2016/09/23 修正從上一頁一定要帶 teacher_id 的 BUG，以及修正修課人數忘了加上校際生的錯誤  Nidalap :D~
/////   2016/10/13 Read_Student() 呼叫時帶入 dont_die_flag=1，避免名單讀到一半就死掉了。  Nidalap :D~

//echo $EXPIRE_META_TAG;

require_once "../library/Reference.php";
require_once $LIBRARY_PATH."System_Settings.php";
require_once $LIBRARY_PATH."Database.php";
require_once $LIBRARY_PATH."Dept.php";
require_once $LIBRARY_PATH."Password.php";
require_once $LIBRARY_PATH."Student_Course.php";
require_once $LIBRARY_PATH."Course.php";
require_once $LIBRARY_PATH."Teacher.php";
require_once $LIBRARY_PATH."Classroom.php";
require_once $LIBRARY_PATH."Student.php";
require_once $LIBRARY_PATH."Common_Utility.php";
require_once $LIBRARY_PATH."Select_Course.php";
require_once $LIBRARY_PATH."Error_Message.php";

//$sys_state = Whats_Sys_State();

//////////  處理使用者輸入的資料

//print_r($_POST);

$dept_cd		= Verify_Specific_Data($_POST["dept_cd"], "deptcd", "學系代碼");
$last_semester	= Verify_Specific_Data($_POST["last_semester"], "int", "學年學期", 1);
$cid_grp		= Verify_Specific_Data($_POST["course_cd"], "cid_grp", "科目代碼班別");
$teacher_id		= array_key_exists("teacher_id", $_POST) ? Verify_Specific_Data($_POST["teacher_id"], "person_id", "教師代碼") : "";
$login_dept_id	= array_key_exists("login_dept_id", $_POST) ? Verify_Specific_Data($_POST["login_dept_id"], "deptcd", "學系代碼2") : "";
$open_dept		= array_key_exists("open_dept", $_POST) ? Verify_Specific_Data($_POST["open_dept"], "deptcd", "學系代碼3") : "";
$password		= array_key_exists("password", $_POST) ? Verify_Specific_Data($_POST["password"], "password", "密碼") : "";
$last_select	= array_key_exists("last_select", $_POST) ? Verify_Specific_Data($_POST["last_select"], "text", "上次篩選後名單", "1") : "";

list($cid, $grp) = preg_split("/_/", $cid_grp);
list($year, $term) = Last_Semester($last_semester);
$Course = Read_Course($dept_cd, $cid, $grp, $year, $term);
list($t, $t, $now) = gettime();
$system_settings = Get_System_State();

$title = "國立中正大學 " . $SYS['SUB_SYSTEM_NAME'] . " <U>$year</U> 學年度";
$title .= "第 <U>$term</U> 學期  教師上課記事簿";
$title_header = "國立中正大學 " . $SYS['SUB_SYSTEM_NAME'] . " $year 學年度";
$title_header .= "第 $term 學期  教師上課記事簿";
Print_Html_Header($title_header,"$GRAPH_URL/ccu-sbg.jpg");

//echo "cid grp dept_cd last_semester, y, t= $cid $grp $dept_cd, $last_semester, $year, $term<P>\n";
//echo "login_dept_id, open_dept, password = $login_dept_id, $open_dept, $password<P>\n";

if( $system_settings['sysstate'] == 0 ) {
  echo "
        <center>
         <img src=$GRAPH_URL/open.jpg><P>
         <h4>查詢修課學生名單功\能</h4><HR>
         目前系統暫不開放查詢!
  ";
  Print_Html_Tail();
  die();
}

//////////  判別輸入的教師人事代碼，是否是此科目的開課教師之一
$valid_teacher = 0;

if( $login_dept_id and $password ) {						//////  如果是系所登入
  //echo ".";
  $password_pass = Check_Dept_Password($open_dept, $password);  
  
}else{
  foreach ($Course["teacher"] as $teacher) {
    if( $teacher_id == $teacher )  $valid_teacher = 1;
//    print("teacher = $teacher<BR>\n");
  }
  if( $valid_teacher == 0 ) {
    echo ("<H1>錯誤：您並非本科目授課教師！</H1>"); 
    Print_Html_Tail();
    die();
  }
}

$notebook = Format_Notebook();

////////////////////////////////////////////////////////////////////
/////  處理授課教師顯示字串
function Format_Notebook()
{
  global $Course, $cid, $grp, $now, $last_select, $dept_cd, $year, $term;
  $teacher_string = "";
  $Teachers=Read_All_Teacher();

  $T = count($Course["teacher"]);
  foreach($Course["teacher"] as $teacher)  {
    $teacher_string .= $Teachers[$teacher]["name"];
    
    if($teacher != $T-1){
      $teacher_string .= ", ";
    }
  }
  
//  echo "teacher_string = $teacher_string<BR>\n";
  
  //////  處理上課時間顯示字串
  $time_string = Format_Time_String($Course["time"]);

  ////// 讀取教室資料
//  %Room=Read_Classroom($Course{classroom});
  ////// 讀入學生名單 //////

  if( $last_select == 1 ) {
    $list_title = "上次篩選後名單";
    $Students = Student_in_Course($Course["id"],$Course["group"], "last");  
  }else{
    $list_title = "目前選課名單";
    $Students = Student_in_Course($Course["id"],$Course["group"], $year, $term);
//  print("$Input{dept_cd},$Course{id},$Course{group}, $year, $term<BR>\n");
  }
//  echo "$dept_cd," . $Course["id"] . "," . $Course["group"] . ", $year, $term";
  $total = count($Students);
  sort($Students);
  
  //////////////  抓取校際選課生資料
  
  $DBH_a = PDO_connect("academic");
  $sql = "
    SELECT * FROM a32t_other_sel_class 
     WHERE year = '$year'  AND term = '$term' 
	   AND cour_id = '" . $Course['id'] . "' AND grp = '" . $Course['group'] . "'
  ";
  
  $sql = "
	SELECT OSC.*, SCH.sch_name, SOR.name 
	  FROM a32t_other_sel_class AS OSC, a32tstd_other_rec AS SOR, a30tcourse_school AS SCH
	 WHERE OSC.sch = SOR.sch_no AND OSC.std_no = SOR.std_no AND SCH.sch_no = SOR.sch_no
	   AND OSC.year='$year' AND OSC.term='$term'
	   AND OSC.cour_cd = '$cid' AND OSC.grp = '$grp'
       AND status != '0'
	   
	 UNION
	
	SELECT OSC.*, SCH.sch_name, SOR.name 
	  FROM a32t_other_sel_class AS OSC, a32tstd_other_web_rec AS SOR, a30tcourse_school AS SCH
	 WHERE OSC.sch = SOR.sch_no AND OSC.std_no = SOR.std_no AND SCH.sch_no = SOR.sch_no
	   AND OSC.year='$year' AND OSC.term='$term'
	   AND OSC.cour_cd = '$cid' AND OSC.grp = '$grp'  
       AND status != '0'
  ";
  
  $STH = $DBH_a->query($sql);
  $Students_other = $STH->fetchAll(PDO::FETCH_ASSOC);
  
  $total += count($Students_other);
  
  //////////////  顯示科目基本資料
  $th  = "科目編號: " . $Course['id'] . " &nbsp;&nbsp; 科目班別: " . $Course['group'] . " &nbsp;&nbsp; ";
  $th .= "學分數: " . $Course['credit'] . " &nbsp;&nbsp; 修課人數: $total &nbsp;&nbsp; ";
  $th .= "授課教師: $teacher_string<BR>";
  $th .= "科目名稱: " . $Course['cname'] . "<BR>";
  
  echo "
    <P ALIGN=RIGHT>
      (本表供教師平時記事考核用)  &nbsp;&nbsp;&nbsp;&nbsp;  列印日期: $now
    </P>
    <TABLE border=1 width=100%>
      <TR align=JUSTIFY>
        <TH colspan=8>$th</TH>
      </TR>
      <TR>
        <TH width=10%>系所別</TH><TH width=10%>學號</TH><TH width=10%>姓名</TH>
        <TH>備註</TH><TH colspan=4>重要記事</TH>
      </TR>
  ";
  
  foreach( $Students as $student ) {
//	echo "[student = $student]<BR>\n";
    
    //echo ".";
    $stu	= Read_Student($student, 1);
    $dept	= Read_Dept($stu['dept']);
    echo "
      <TR>
        <TD>" . $dept['cname2'] . "</TD><TD>" . $stu['id'] . "</TD><TD>" . $stu['name'] ."</TD>
        <TD>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</TD>
        <TD width=7%>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</TD>
        <TD width=7%>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</TD>
        <TD width=7%>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</TD>
        <TD width=7%>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</TD>
	  </TR>
    ";
  }
  foreach( $Students_other as $stu ) {
	echo "
	  <TR bgcolor='LIGHTYELLOW'>
	    <TD>" . $stu['sch_name'] . "</TD><TD>" . $stu['std_no'] . "(校際)</TD><TD>" . $stu['name'] ."</TD>
		<TD>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</TD>
        <TD width=7%>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</TD>
        <TD width=7%>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</TD>
        <TD width=7%>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</TD>
        <TD width=7%>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</TD>
	  </TR>
	";
  }
  echo "</tr></table>\n";
  echo "<p><a href=\"Login.cgi\">回到查詢修課學生主選單</a><br>\n";
}


Print_Html_Tail();
////////////////////////////////////////////////////////////////////////////////////////////////////////////
function Print_Html_Header($title, $BG)
{
  global $GRAPH_URL, $EXPIRE_META_TAG;
  
  if($BG == "")  $BG = $GRAPH_URL . "/ccu-sbg.jpg";
  echo "
   <HTML>
     <HEAD>
       $EXPIRE_META_TAG
       <TITLE>$title</TITLE>
     </HEAD>
     <BODY background='$BG'>
       <CENTER>
         <H2>
           $title
         </H2>
       </CENTER>
       <HR>
  ";
}
/////////////////////////////////////////////////////////////////////////////////////////////////////////////
function Print_Html_Tail()
{
  echo "
        </center>
      </Body>
    </Html>
  ";
}

?>