<meta http-equiv="Content-Type" content="text/html; charset=utf-8">

<?PHP
////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////   Create_Password2.php
/////   批次產生新生密碼
/////   Updates:
/////     2001/08/09  perl cgi 版本完成修改，由原先的隨機密碼改為預設身份證號  Nidalap :D~
/////     2010/01/12  為避免重複的更改密碼函式，改寫 php 版本  Nidalap :D~
/////     2013/02/18  改採 PDO 連線資料庫  Nidalap :D~

include_once "../../library/Reference.php";
include_once $LIBRARY_PATH . "Common_Utility.php";
include_once $LIBRARY_PATH . "Error_Message.php";
include_once $LIBRARY_PATH . "Student.php";
include_once $LIBRARY_PATH . "Password.php";
include_once $LIBRARY_PATH . "Database.php";

////////////////////////  檢查密碼是否正確
/*
$result = Check_SU_Password($_POST["password"], "su", "su");
if( $result != "TRUE" ) {
  print("Password Check Error for $_POST[password]");
  exit(0);
}
*/
?>
  <HEAD><TITLE>產生新生密碼</TITLE></HEAD>
  <BODY background="<?PHP echo $GRAPH_URL; ?>/bk.jpg">
    <CENTER>
      <H1>產生新生密碼</H1>
      <HR>
      密碼產生中, 請稍後...<BR>
<?PHP  

  $DBH = PDO_connect($DATABASE_NAME);
  $student = Find_All_Student();
  $change_count = 0;
  $tital_count = 0;
  foreach ( $student as $stu ) {
    $password_file = $STUDENT_PASSWORD_PATH . $stu . ".pwd";
    $total_count++;
    if( !file_exists($password_file) ) {
//      print("checking $password_file...<BR>\n");
      $s = Read_Student($stu);
//      print_r($s);
//      print "change ". $stu. $s["personal_id"]. " <BR>\n";
      list($flag,$flag1,$flag2, $crypted_password) = Change_Password($stu, $s["personal_id"]);
      if( $flag == 0 ) {
        echo "錯誤：無法更改 $stu! [flag1, flag2] = [$flag1, $flag2]\n<BR>";
      }
      $change_count++;
    }
  }
  echo("完成！共檢查 $total_count 筆學生資料，並產生 $change_count 筆密碼資料.");





?>
