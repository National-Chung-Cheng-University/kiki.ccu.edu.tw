<meta http-equiv="Content-Type" content="text/html; charset=utf-8">

<?PHP

//////////////////////////////////////////////////////////////////////////////////////////
/////  Concent_Form_Approval.php
/////  加簽單審核介面
/////  列出(某學生)本學年學期所有加簽單及其審核、選課狀態，供管理者審核確認
/////  Updates:
/////    2010/08/16 Created by Nidalap :D~
/////    2012/11/01 改採 PDO 連線 by Nidalap :D~
/////    2013/09/09 修正因轉換資料庫導致不能執行的問題 Nidalap :D~
/////    2014/02/20 修正上學期因轉換資料庫改寫導致列表效能奇差的問題(原46sec改後0sec)  Nidalap :D~

require_once "../library/Reference.php";
require_once $LIBRARY_PATH . "Error_Message.php";
require_once $LIBRARY_PATH . "Common_Utility.php";
require_once $LIBRARY_PATH . "System_Settings.php";
require_once $LIBRARY_PATH . "Session.php";
require_once $LIBRARY_PATH . "Dept.php";
require_once $LIBRARY_PATH . "Course.php";
require_once $LIBRARY_PATH . "Student.php";
require_once $LIBRARY_PATH . "Database.php";
require_once $LIBRARY_PATH . "Password.php";
require_once $LIBRARY_PATH . "Student_Course.php";

$DEBUG = 0;
$time_start = time();

//db_connect(1,1);
$DBH = PDO_connect();
session_start();

if( array_key_exists("password", $_POST) )  $_SESSION["password"] = $_POST["password"];
if( array_key_exists("action", $_POST) )    $_SESSION["action"] = $_POST["action"];
if( array_key_exists("stu_id", $_POST) )    $_SESSION["stu_id"] = $_POST["stu_id"];
if( ! Check_SU_Password($_SESSION["password"], "Concent_Form_Approval", "") )
  die("Invalid password!");

//var_dump($_POST);
//echo "<HR>";
//var_dump($_SESSION);
//echo "<HR>";

if( To_Approve() ) {			///  如果要審核/取消任何加簽單
  Approve();				///   那就做吧！
//  echo "going to verify...<BR>";
}
Print_Banner_And_Input();

$exe_time = time() - $time_start;
if($DEBUG)  echo "Phase 1: 程式執行耗費 $exe_time 秒<BR>\n";

//print_r($_SESSION);
if( $_SESSION["action"] == "list_stu" ) {
  List_Records($_SESSION["stu_id"]);	///  列出單一學生所有加簽單
}else{
  List_Records("");			///  列出所有加簽單
}

echo "
  <FORM action='su.cgi' method=POST>
    <INPUT type=hidden name=password value='" . $_SESSION["password"] . "'>
    <INPUT type=hidden name=do_not_crypt value=1>
    <INPUT type=submit value='回管理主選單'>
  </FORM>
";

$exe_time = time() - $time_start;
echo "完成： 程式執行耗費 $exe_time 秒<BR>\n";

////////////////////////////////////////////////////////////////////////////////////////////////////
/////  檢查是否有要審核/取消審核任何加簽單
function To_Approve()
{
  foreach( $_REQUEST as $key=>$value) {
    if( preg_match("/^check_/", $key) ) 
      return 1;
  }
  return 0;
}
////////////////////////////////////////////////////////////////////////////////////////////////////
/////  執行審核/取消審核
function Approve()
{
  global $DBH;
  foreach( $_REQUEST as $key=>$value) {		///  先解析傳進來要核可/取消的加簽單資料
    if( preg_match("/^check_/", $key) ) {
      list($j, $stu_id, $course_id, $grp) = explode("_", $key);
      $verify = $value;
      break;
    }
  }
//  echo "[$stu_id, $course_id, $grp, $verify]<BR>";
  list($j, $time, $j) = gettime(""); 
  
  if( $verify == "on" )	{				///  要核可
    $verify_text = "1";
    $verify_text2 = "核可";
    $verify_text3 = ", verify_time ='$time'";
    Modify_Immune_Record("add", $course_id, $grp, $stu_id);
    SU_Log("add_concent", $stu_id);
  }else{						///  要取消
    $verify_text = "0";
    $verify_text2 = "取消";
    $verify_text3 = ", verify_time = NULL ";
    Modify_Immune_Record("del", $course_id, $grp, $stu_id);
    SU_Log("del_concent", $stu_id);
  }
  
  $sql = "UPDATE concent_form SET verified='$verify_text'" . $verify_text3 . 
          "WHERE stu_id='$stu_id' AND course_id='$course_id' AND grp='$grp'";
  echo "<FONT color=RED>";
  
  if( $DBH->query($sql) === FALSE ) {
    echo "更新失敗！哪裡有了問題！？！？勿關視窗快找萬惡的電算中心求救！！<BR>\n";
    echo "[$stu_id, $course_id, $grp, $verify]<BR>\n";
    echo $sql . "<BR>";
    echo $DBH->errorInfo();
    exit();
  }else{
    echo "成功 " . $verify_text2 . "此加簽單(學號 $stu_id, 科目 $course_id, 班別 $grp)";
  }
  echo "</FONT>";
}
////////////////////////////////////////////////////////////////////////////////////////////////////
/////  列出全部或特定學號的加簽單資料(HTML table)
function List_Records($stu_id)
{
  global $DATABASE_NAME, $GRAPH_URL, $YEAR, $TERM, $DBH;
  global $DEBUG, $exe_time, $time_start;
  $DBH_a = PDO_connect("academic");
    
  define("HIGHLIGHT1", 5);
  define("HIGHLIGHT2", 10);
//  $sql = "SELECT DISTINCT CF.*, AC.cname FROM concent_form AS CF, " . $DATABASE_NAME . 
//         "..a31tallcourse AS AC WHERE CF.course_id = AC.coursecd ";
  
  /////  先抓各科目核可人數
  $sql = "SELECT count(*) as verified_count, course_id, grp
            FROM concent_form
           WHERE verified = '1' AND year='$YEAR' AND term='$TERM'
           GROUP BY verified, course_id, grp";
  $STH = $DBH->query($sql);

  while( $temp = $STH->fetch(PDO::FETCH_ASSOC) )  {
    $id_grp = $temp["course_id"] . "_" . $temp["grp"];
    $verified_count[$id_grp] = $temp["verified_count"];
  }
  
  $exe_time = time() - $time_start;
  if($DEBUG) echo "Phase 2: 程式執行耗費 $exe_time 秒<BR>\n";
  
//  print_r($verified_count)  ;

  /////  再抓取列表資料
  /*$sql = "SELECT DISTINCT year, term, course_id, CF.grp, stu_id, serialno, verified, AC.cname,
                 CONVERT(char(11), apply_time, 111)+CONVERT(char(8), apply_time, 8) as apply_time,
                 CONVERT(char(11), verify_time, 111)+CONVERT(char(8), verify_time, 8) as verify_time,
                 CONVERT(char(11), add_time, 111)+CONVERT(char(8), add_time, 8) as add_time
            FROM concent_form AS CF, " . $DATABASE_NAME . 
         "..a31vallcourse AS AC WHERE CF.course_id = AC.coursecd ";
  */
//  $STH = $DBH->query($sql);
//  while( $temp = $STH->fetch(PDO::FETCH_ASSOC) )  $rows[] = $temp;
//  $row_count = count($rows);

  /////  先抓取 concent_form 內的資料
  $sql = "SELECT DISTINCT year, term, course_id, grp, stu_id, serialno, verified, 
				 apply_time, verify_time, add_time
            FROM concent_form
		   WHERE year='$YEAR' AND term='$TERM'";
  if( $stu_id ) {					///  如果要列出特定學生加簽單
    $sql .= " AND stu_id = '$stu_id'";
    $stu = Read_Student($stu_id);
  }
  $sql .= " ORDER BY stu_id, course_id, grp";
  $STH = $DBH->query($sql);
  $rows = $STH->fetchAll(PDO::FETCH_ASSOC);
  $row_count = count($rows);
  
  $exe_time = time() - $time_start;
  if($DEBUG)  echo "Phase 3: 程式執行耗費 $exe_time 秒<BR>\n";
  //print_r($rows);
  //echo "<HR>\n";
  
  /////  再抓取教務系統 a31vallcourse 的資料補齊
  $sql = "SELECT DISTINCT coursecd, cname FROM a31vallcourse";
  $STH = $DBH_a->query($sql);
  $temp_cname_all = $STH->fetchAll(PDO::FETCH_ASSOC);
  foreach($temp_cname_all as $temp) {
    $temp_cname[$temp['coursecd']] = $temp['cname'];
  }  
  $i=0;
  foreach( $rows as $row ) {
//    $sql = "SELECT DISTINCT cname FROM a31vallcourse WHERE coursecd = '" . $row['course_id'] . "'";
//	$STH = $DBH_a->query($sql);
//	$temp = $STH->fetch(PDO::FETCH_ASSOC);
//	$rows[$i]['cname'] = $temp['cname'];
    $rows[$i]['cname'] = $temp_cname[$row['course_id']];
	$i++;
  }
  
  $exe_time = time() - $time_start;
  if($DEBUG)  echo "Phase 4: 程式執行耗費 $exe_time 秒<BR>\n";
  //print_r($rows);
  //echo "<HR>\n";
  
/*
  $sql = "SELECT DISTINCT cname FROM a31vallcourse WHERE coursecd IN (";
  $i = 0;
  foreach( $rows as $row ) {
    if( $i != 0 )  $sql .= ", ";
    $sql .= "'" . $row['course_id'] . "'";
	$i++;
  }  
  $sql .= ") ORDER BY coursecd";
  
  $STH = $DBH_a->query($sql);
//  echo $sql . "<BR>\n";
//  print_r($DBH_a->errorInfo());
  
  $i = 0;
  while( $temp = $STH->fetch(PDO::FETCH_ASSOC) ) 
	$rows[$i++]['cname'] = $temp['cname'];
*/
  if( $stu_id ) {
    if( isset($stu) && ($stu["id"] != $stu_id) ) {
      $stu = Read_Student($stu_id);
    }
    $header_text = $stu["name"] . "($stu_id)目前共有 $row_count 筆加簽紀錄：";
  }else{
    $header_text = "目前全部共有$row_count 筆加簽紀錄：";
  }
  $exe_time = time() - $time_start;
  if($DEBUG)  echo "Phase 5: 程式執行耗費 $exe_time 秒<BR>\n";
  echo $header_text . "<BR>";
  echo "<FORM id=form2 action='Concent_Form_Approval.php' method=POST>";
  echo "<TABLE border=1 width=90%>";
  echo "  <TR>
            <TH>審核</TH>
            <TH>科目代碼</TH>
            <TH>班別</TH>
			<TH>科目名稱</TH>
			<TH>學號</TH>
            <TH>姓名</TH>
            <TH>序號</TH>
            <TH>核可人數</TH>
            <TH>申請時間</TH>
            <TH>審核時間</TH>
            <TH>加選與否</TH>
          </TR>";
	
  reset($rows);	
  foreach( $rows as $row ) {
    $stu = Read_Student($row["stu_id"], 1);
    $student_course = Course_of_Student($row["stu_id"]);

    //////  格式化「加選與否」
    $add_flag = "&nbsp;";
    if( $row["verified"] )  $add_flag = "<FONT color=RED>否</FONT>";
    if( $student_course ) {						///  從該學生已選修科目，判斷是否選過此科目
      foreach( $student_course as $stu_cou ) {
        if( ($stu_cou["id"] == $row["course_id"]) and ($stu_cou["group"] == $row["grp"]) ) {
          $add_flag = "是";
        }
      }
    }
    //////  審核 Checkbox 
    $checkbox_id = "check_" . $row["stu_id"] . "_" .  $row["course_id"] . "_" . $row["grp"];
    if( $row["verified"] ) {
      $checked_html = "<A href='Concent_Form_Approval.php?$checkbox_id=off'><IMG border=0 class=cancel src='" . $GRAPH_URL . "checked.jpg'></A>";
    }else{
      $checked_html = "<INPUT type=checkbox name=$checkbox_id>";
    }
    /////  格式化「序號」
    if( $row["serialno"] >= HIGHLIGHT1 )  {
      $highlight = "bgcolor=YELLOW";
      if( $row["serialno"] >= HIGHLIGHT2) {
        $highlight = "bgcolor=RED";
      }
    }else{
      $highlight = "";
    }
    /////  格式化「核可人數」
    $id_grp = $row["course_id"] . "_" . $row["grp"];    
    $verified_count[$id_grp] = array_key_exists($id_grp, $verified_count) ? $verified_count[$id_grp] : 0;
    if( $verified_count[$id_grp] >= HIGHLIGHT1 )  {
      $highlight2 = "bgcolor=YELLOW";
      if( $verified_count[$id_grp] >= HIGHLIGHT2) {
        $highlight2 = "bgcolor=RED";
      }
    }else{
      $highlight2 = "";
    }
    
    echo "<TR>
            <TD align=CENTER>$checked_html</TD>
            <TD>" . $row["course_id"] . "</TD>
            <TD>" . $row["grp"] . "</TD>
			<TD>" . $row["cname"] . "</TD>
			<TD>" . $row["stu_id"] . "</TD>
            <TD>" . $stu["name"] . "</TD>
            <TD align=CENTER $highlight>" . $row["serialno"] . "</TD>
            <TD align=CENTER $highlight2>" . $verified_count[$id_grp] . "</TD>
            <TD>" . $row["apply_time"] . "</TD>
            <TD>" . ($row["verify_time"] ? $row["verify_time"] : "&nbsp;") . "</TD>
            <TD>" . $add_flag . "</TD>
          </TR>
    ";
  }
  echo "</TABLE></FORM>";
  $exe_time = time() - $time_start;
  if($DEBUG)  echo "Phase 6: 程式執行耗費 $exe_time 秒<BR>\n";
}
///////////////////////////////////////////////////////////////////////////////////////////////////
/////  新增/刪除加簽紀錄 local files 版本，供 perl 程式讀取
/////  2011/08/17 從原有加簽程式移植修改 by Nidalap :D~
function Modify_Immune_Record($action, $c_id, $c_group, $stu_id)
{
//  my($c_id, $c_group, $stu_id) = @_;
  global $DATA_PATH, $YEAR, $TERM;

  $immune_file = $DATA_PATH . "Course_Upper_Limit_Immune/" . $YEAR . "_" . $TERM . "/";
  if( !is_dir($immune_file) ) {			///  若目錄尚未建立，建之。
    umask("0000");
    if( !mkdir($immune_file) )
      die("Failed to make dir $immune_file!<BR>\n");
  }  
  $immune_file .=  $c_id . "_" . $c_group;

  if( $IMMUNE = fopen($immune_file, "r") ) {
    while( $temp=fgets($IMMUNE) )  $lines[] = rtrim($temp);
    fclose($IMMUNE);
  }
  
  if( $action == "add" ) {			///  新增加簽紀錄
//    Student_Log("Add_Concent", $stu_id, $c_id, $c_group, "", "");
    if( $lines ) {
      foreach($lines as $line) {				///  如果早已有紀錄，不管了
        if($line == $stu_id)  return FALSE;
      }
    }

    if( $IMMUNE = fopen($immune_file, "a") ) {		///  將此筆學號寫入此科目的 immune file
      fputs($IMMUNE, "$stu_id\n");
      fclose($IMMUNE);
      return TRUE;
    }else{
      die("Failed to append file $immune_file!<BR>\n");
    }
  }else{					///  刪除加簽紀錄
//    Student_Log("Del_Concent", $stu_id, $c_id, $c_group, "", "");
    for($i=0; $i<count($lines); $i++) {			///  如果早已有紀錄，刪除之
      if($lines[$i] == $stu_id) unset($lines[$i]);
    }
    if( $IMMUNE = fopen($immune_file, "w") ) {          ///  將此筆學號寫入此科目的 immune file
      foreach( $lines as $line ) {
        fputs($IMMUNE, "$line\n");
      }
      fclose($IMMUNE);
      return TRUE;
    }else{
      die("Failed to write to file $immune_file!<BR>\n");            
    }    
  }
}

////////////////////////////////////////////////////////////////////////////////////////////////////
function Print_Banner_And_Input() {
  global $EXPIRE_META_TAG, $GRAPH_URL;
  echo "<HTML>
    <HEAD>
      <TITLE>加簽單申請確認</TITLE>
      $EXPIRE_META_TAG
    </HEAD>";
  Print_Javascript();
  echo "
  <BODY background='" . $GRAPH_URL . "manager.jpg'>
  <CENTER><H1>加簽單申請確認</H1><HR size=2 width=50%>
  <TABLE border=0 bgcolor=YELLOW>
    <TR>
      <TD>
      <FORM action='Concent_Form_Approval.php' method='POST'>
        <INPUT maxsize=9 name=stu_id id = stu_id>
        <INPUT type=hidden name=action value='list_stu'>
        <INPUT type='SUBMIT' value='列出此學生加簽單(學號)'>
      </FORM>
      </TD><TD width=150></TD><TD>
      <FORM action='Concent_Form_Approval.php' method='POST'>
        <INPUT type=hidden name=action value='list_all'>
        <INPUT type='SUBMIT' value='列出所有加簽單'>
      </FORM>
    </TR>
  </TABLE>
  ";
}
////////////////////////////////////////////////////////////////////////////////////////////////////
function Print_Javascript()
{
  echo "
    <SCRIPT type='text/javascript' src='https://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js'></script>
    <SCRIPT language='javascript'>
      \$(document).ready(function(){
        \$('#stu_id').focus();
        \$('input:checkbox').click(function() {
          \$('#form2').submit();
        })
        \$('.cancel').click(function() {
          if( confirm('您確定要取消此加簽單?') ) {
            ///
          }else{
            return false;
          }
        })
      })
    </SCRIPT>
  ";


}


/*
$session_id	= quotes($_GET["session_id"]);
$dept		= quotes($_GET["dept"]);
$cid		= quotes($_GET["cid"]);
$grp		= quotes($_GET["grp"]);
$session	= Read_Session($session_id);
Renew_Session($session_id);

$stu = Read_Student($session["id"]);
$dept_data = Read_Dept($dept);
$course = Read_Course($dept, $cid, $grp, "", "");
$HEAD_DATA = Form_Head_Data($stu["id"], $stu["name"], $dept_data["cname2"], $stu["grade"], $stu["class"]);
$HTML_BANNER = Print_HTML_Banner();

$_SESSION["session_id"]	= $session_id;
$_SESSION["dept"]	= $dept;
$_SESSION["cid"]	= $cid;
$_SESSION["grp"]	= $grp;

//print_r($_SESSION);
db_connect(1,1);			///  連到 academic_kiki 資料庫  
$application = Concent_Form_Apply_Status($stu["id"], $cid, $grp, "", "");
if( $application == -1 ) {		///  尚未加簽過此科目: 新增加簽資料
  $message = "
        您正要申請加簽此科目：  
        <P>  
        <CENTER>  
          <B><U>" . $course["cname"] . "(代碼 $cid 班別 $grp)</U></B>  
        </CENTER>  
        <P>  
        是否正確？  
        若是請點選「是，我要申請」，並列印下頁加簽單。  
  ";
  $submit_text = "是，我要申請";
}else{					///  曾經加簽過此科目: 帶出舊資料
  $message = "
        您已經在 " . $application["apply_time"] ." 申請加簽過此科目：
        <P>  
        <CENTER>  
          <B><U>" . $course["cname"] . "(代碼 $cid 班別 $grp)</U></B>  
        </CENTER>  
        <P>  
        若要重新列印請點選「是，我要重新列印」，並列印下頁加簽單。
  ";
  $submit_text = "是，我要重新列印";
}

//print_r($application);

echo "
  <P>
  <TABLE border=1 width=50%>
    <TR>
      <TD bgcolor=LIGHTYELLOW>$message</TD>
    </TR>
  </TABLE>
 
  <FORM action='My_Concent_Form2.php' method='POST'>
    <INPUT type=SUBMIT value='$submit_text'>
    <INPUT type=BUTTON value='否，我要回上頁' onclick='javascript:history.back()'>
  </FORM>
";

//////////////////////////////////////////////////////////////////////////////////////
function Print_HTML_Banner()
{
  global $EXPIRE_META_TAG, $BG_PIC, $GRAPH_URL, $HEAD_DATA;

  print "
    <HTML>
    $EXPIRE_META_TAG
    <BODY background='$BG_PIC'>
      <CENTER>
        $HEAD_DATA
        <HR>
  ";
}
*/

?>