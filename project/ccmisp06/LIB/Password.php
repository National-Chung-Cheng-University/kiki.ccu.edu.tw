<?PHP

//////////////////////////////////////////////////////////////////////////////////////////
/////  Password.php
/////  (幾乎所有)密碼相關的函式
/////  Updates:
/////    2009/10/29 因應學生密碼改為 MD5 編碼，做相關修改  Nidalap :D~
//////////////////////////////////////////////////////////////////////////////////////////
function Check_Password($id, $password, $return_type="", $password_original="")
{
  global $STUDENT_PASSWORD_PATH, $STUDENT_PASSWORD_MD5_PATH, $USE_MD5_PASSWORD;

  if( ($id == "") or ($password == "") ) {   ### 不允許空資料
    Show_Password_Error_Message();
  }
  global $SUPERUSER;
  $SUPERUSER = Check_SU_Password($password, "", $id);           ///  檢查 SU password

  if( $USE_MD5_PASSWORD == 1 ) {
    $password_file = $STUDENT_PASSWORD_MD5_PATH . $id . ".pwd";
    $file_handle = fopen($password_file, "r");
    list($real_pass) = fscanf($file_handle, "%s\n");
    fclose($file_handle);
  }else{
    $password_file = $STUDENT_PASSWORD_PATH . $id . ".pwd";
    $file_handle = fopen($password_file, "r");
    list($real_pass) = fscanf($file_handle, "%s\n");
    fclose($file_handle);
    $real_pass = substr($real_pass, 2, 24);
  }
          
//  echo $password_file;
//  echo("[$id, $password] : $password_file<BR>\n");

  if( ($SUPERUSER == 1) or ($password == $real_pass) ) {    	///  密碼正確或是管理者 -> return
    return(1);
  }else{							///  密碼錯誤且非管理者 -> 紀錄，顯示錯誤
//	echo "ccc";
//    Append_Login_Error_LOG($id, $password_original);
    Student_Log("LoginFail",$id,$password_original);
//    echo("<BR>$password <-> $real_pass<BR>");
    if( $return_type == "new" ) {
      Show_Password_Error_Message(1);
    }else{
      Show_Password_Error_Message();
    }

  }
}
/////////////////////////////////////////////////////////////////////////////////////////////
/////  紀錄「失敗」登入的 LOG 資料 -> Error.log
/////  改為透過 Student_Log() 紀錄到 Student.log  2009/10/23 Nidalap :D~
/*
function Append_Login_Error_LOG($id, $password_original)  
{
  global $LOG_PATH;

  $log_file = $LOG_PATH . "Error.log";
  if( ($file_handle = fopen($log_file, "a")) == 0 ) {
    echo("系統運作內部錯誤!<BR>");
    $error_code = "ERROR_WRITE_LOG_FOR_ERROR_LOGIN";
    Error_Please_Report($error_code);
  }
  list($timestring, $junk) = gettime("");
  $ip = getenv("HTTP_X_FORWARDED_FOR");
  if( $ip == "" ) { $ip = getenv("REMOTE_ADDR"); }

  $message = $timestring . " : " . $ip . " : " . $id . " login fail using password " . $password_original;
  global $SUPERUSER;
  if( $SUPERUSER == 1 ) {
    $message .= "SU";
  }
  $message .= "\n";
  fputs($file_handle, $message);
  fclose($file_handle);
}
*/

/////////////////////////////////////////////////////////////////////////////////////////////
function Check_Password_Database($id, $password, $real_pass)
{
//  if( ($id == "") or ($password == "") ) {   ### 不允許空資料
//  if( $id == "" ) {				### 不允許空資料, 但是為了新生, 密碼可允許空白
//    echo("null");

  //echo "$id, $password, $real_pass";
  if( $id == "" ) {
    Show_Password_Error_Message();
  }

  global $SUPERUSER;
  $SUPERUSER = Check_SU_Password($password, "", $id);

  if( ($SUPERUSER == 1) or ($password == $real_pass) ) {
    return;
  }else{
//    print "[$password<->$real_pass]<BR>\n";
    Show_Password_Error_Message();
  }
}

//////////////////////////////////////////////////////////////////////////////////////////
function Check_SU_Password($password, $reason, $id)
{
  // 檢查 password
  global $STUDENT_PASSWORD_PATH, $STUDENT_PASSWORD_MD5_PATH, $USE_MD5_PASSWORD, $DATA_PATH;
  global $SUPERUSER;
  $result = 0;

  if( $USE_MD5_PASSWORD == 1 ) {
    $su_file = $DATA_PATH . "Password/SysAdm_MD5.pwd";
    $file_handle = fopen($su_file, "r");
    list ($pass) = fscanf($file_handle, "%s\n");
//      echo("$password <-> $pass<BR>\n");
    if( $password == $pass ) {
      $result = 1;
    }
  }else{
    $su_file = $DATA_PATH . "Password/SysAdm.pwd";
    $file_handle = fopen($su_file, "r");
    while( list ($pass) = fscanf($file_handle, "%s\n") ) {
//      echo("$password <-> $pass<BR>\n");
      $pass = substr($pass, 2, 20);
      if( $password == $pass ) {
        $result = 1;
        $SUPERUSER = 1;
//        echo("Match! $pass<BR>\n");
      }
    }
  }

  // 寫入 SU log

  return($result);
}

//////////////////////////////////////////////////////////////////////////////////////////
function Read_Crypt_Salt($id)
{
  global $STUDENT_PASSWORD_PATH;
  $password_file = $STUDENT_PASSWORD_PATH . $id . ".pwd";

//  echo $password_file;
  $file_handle = fopen($password_file, "r");
  list($real_pass) = fscanf($file_handle, "%s\n");
  fclose($file_handle);
  $salt = substr($real_pass, 0, 2);
  return($salt);
}

//////////////////////////////////////////////////////////////////////////////////////////
function my_Crypt($password, $crypt_salt)
{
  $password = crypt($password, $crypt_salt);
  //$password = substr($password, 2, 20);
  $password = substr($password, 2, 24);
  return($password);
}
//////////////////////////////////////////////////////////////////////////////////////////
/////  2012/09/12 加入 $revert 參數，用以將密碼還原(其實就是呼叫者傳入更改不成功的舊密碼  by Nidalap :D~
function Change_Password($id, $password, $revert=NULL)
{
  global $STUDENT_PASSWORD_PATH, $STUDENT_PASSWORD_MD5_PATH, $USE_MD5_PASSWORD, $LOG_PATH1;  

  ///// 將新密碼寫入學籍資料庫的 table (包含 NETLOG)
  $flag1 = Update_Password($id, $password);  
  //$flag1 = 1;
//  $flag1 = NULL;
//  echo "flag1 = $flag1";

  if( isset($flag1) ) { 
//    echo "database updated, now trying to update file...";
    if( $USE_MD5_PASSWORD == 1 ) {	/// 將密碼寫入 kiki 的 MD5 密碼檔
      $password_file = $STUDENT_PASSWORD_MD5_PATH . $id . ".pwd";
      $password_md5 = MD5($password);
      $file_handle = fopen($password_file, 'w');
      $flag2 = fputs($file_handle, $password_md5);
      fclose($file_handle);
    }
    $password_file = $STUDENT_PASSWORD_PATH . $id . ".pwd";
    ///// 將新密碼寫入 kiki 選課主機的密碼檔(crypted)，現在寫入傳統 DES 的版本
    if( $file_handle = fopen($password_file, "r") ) {		//  若密碼檔早已存在, 讀取 salt
      list($real_pass) = fscanf($file_handle, "%s\n");
      fclose($file_handle);
      $salt = substr($real_pass, 0, 2);
    }else{							//  若否, 預設 salt
      $salt = "nu";
    }
    $password = crypt($password, $salt);
    $file_handle = fopen($password_file, 'w');
    $flag2 = fputs($file_handle, $password);
    fclose($file_handle);
    /////  要寫資料進去 LOG(kiki 端的文字檔)
    $log_file = $LOG_PATH1 . "Student.log";
    
    if( ($file_handle = fopen($log_file, "a")) == 0 ) {
      echo("系統運作內部錯誤!<BR>");
      // echo("$log_file<BR>\n");
      $error_code = "ERROR_WRITE_LOG_FOR_PASS";
      Error_Please_Report($error_code);
    }
  }
  /////  將更改成功/失敗/密碼還原等資訊紀錄 LOG
  list($timestring, $junk) = gettime("");
  $ip = getenv("HTTP_X_FORWARDED_FOR");
  if( $ip == "" ) { $ip = getenv("REMOTE_ADDR"); }

  if( isset($flag1) and isset($flag2) ) {		///  更新成功
    $message = "Passwd : " . $timestring . " : " . $ip . " : " . $id . " :  :  : ";
    global $SUPERUSER;
    if( $SUPERUSER == 1 ) {
      $message .= "SU";
    }
    $message .= "\n";
  }else{						///  更新失敗
    $message = "PasswdFail : " . $timestring . " : " . $ip . " : " . $id . " :  :  : Database\n";
  }
  fputs($file_handle, $message);

  if( isset($revert) ) {				//  因為 ldap 更改出問題而還原
    $message = "PasswdRevert : " . $timestring . " : " . $ip . " : " . $id . " :  :  :\n";
    fputs($file_handle, $message);  
  }
  fclose($file_handle);

  $flag = $flag1 * $flag2;             // 兩者都必須非零
  ///  回傳的 $password 已經是經過 crypt/MD5 編碼
  //echo "[flag, flag1, flag2] = [$flag, $flag1, $flag2]<BR>\n";
  
  return array ($flag, $flag1, $flag2, $password);
  
}
//////////////////////////////////////////////////////////////////////////////////////////
/////  檢查學生密碼是否過期了 (期限透過 $PASSWORD_MAX_CHANGE_TIME 定義 )
/////  若是，傳回過期天數; 若否，傳回 0 
function Password_Too_Old($id) 
{
  global $STUDENT_PASSWORD_MD5_PATH, $STUDENT_PASSWORD_PATH, $PASSWORD_MAX_CHANGE_TIME;
  global $USE_MD5_PASSWORD;
  $old_flag = 0;

  if( $USE_MD5_PASSWORD == 1 ) {  
    $pass_file = $STUDENT_PASSWORD_MD5_PATH . $id . ".pwd";
  }else{
    $pass_file = $STUDENT_PASSWORD_PATH . $id . ".pwd";
  }
  $file_change_time = time() - filemtime($pass_file);
 
  //echo "change time = $file_change_time <-> $PASSWORD_MAX_CHANGE_TIME <BR>\n";
  //die();
 
  if( $file_change_time > $PASSWORD_MAX_CHANGE_TIME ) {
    $old_flag = 1;
    $file_change_time = round( $file_change_time / (60*60*24));
//    echo("$file_change_time > $PASSWORD_MAX_CHANGE_TIME ");
  }
  if( $old_flag == 1 )  {
    return($file_change_time);
  }else{
    return($old_flag);
  }
}
//////////////////////////////////////////////////////////////////////////////////////////
function Show_Password_Error_Message($type)
{
  
  global $BG_PIC, $EXPIRE_META_TAG;
    
  if( $type = 1 ) {					###  在右側視窗顯示
    echo "<HTML><HEAD>" . $EXPIRE_META_TAG . "<TITLE>密碼有誤</TITLE></HEAD>";
    echo("<BODY background=$BG_PIC>");
    echo("<Center><FONT color=RED>密碼確認結果</FONT><hr>");
    echo("<FONT size=-1>您輸入的密碼有誤,<BR>請重新輸入!<p>");
    echo("<A href=\"login.php\">重新登入</A>");
    exit(2);
  }else{
    echo "<HTML><HEAD>" . $EXPIRE_META_TAG . "<TITLE>密碼有誤</TITLE></HEAD>";
    echo("<BODY background=$BG_PIC>");
    echo("<Center><H1>密碼確認結果<hr></H1>");
    echo("您輸入的密碼有誤, 請重新輸入!<p>");
    echo("<FONT color=RED>請區分英文字母大小寫(新生密碼身份證號一律為大寫)</FONT><P>");
    exit(2);
  }
}
//////////////////////////////////////////////////////////////////////////////////////////
/////  Check_Dept_Password()
/////  檢查系所輸入密碼, 是否為正確密碼或管理者密碼
//////////////////////////////////////////////////////////////////////////////////////////
function Check_Dept_Password($dept, $inpassword)
{
//  my($password_file, $dept, $inpassword, $real_password);
//  my $su_result;
  global $USE_MD5_PASSWORD, $DEPT_PASSWORD_PATH, $DEPT_PASSWORD_MD5_PATH;
  $md5_password_found = -1;                  ### [-1,0,1] = [不需要,找不到,找到了]
//  ($dept,$inpassword) = @_;

//  echo "check password: $dept, $inpassword ... <BR>\n";
  if( $USE_MD5_PASSWORD == 1 ) {                #####  檢查 MD5 版本的密碼
    $password_file = $DEPT_PASSWORD_MD5_PATH . $dept . ".pwd";
    if( $fp = fopen("$password_file", "r") ) {       ###    MD5 版本的密碼存在
      $md5_password_found = 1;
      $real_password = fgets($fp, 1024);
      fclose($fp);
      $real_password = rtrim($real_password);
    }else{                                        ###    MD5 版本的密碼不存在
      $md5_password_found = 0;
    }
  }
                                                #####  如果設定不用 MD5, 或是找不到 MD5 版本密碼
  if( ($USE_MD5_PASSWORD!=1) or ($md5_password_found!=1) ) {  #####  就使用 DES 密碼認證
//    print("dept = $dept; inpassword = $inpassword<br>");
    $password_file = $DEPT_PASSWORD_PATH . $dept . ".pwd";
    if( !($fp = fopen($password_file, "r")) )
      Show_Password_Error_Message("dept");
//      return("ERROR: Cannot open file $password_file in module Password.pm\n");
    $real_password = fgets($fp, 1024);
    fclose($fp);
    $real_password = rtrim($real_password);
    $real_password = preg_replace("/^../", "", $real_password);
  }

//  print("Checking su"); 
  $su_result = Check_SU_Password($inpassword,"dept", $dept);
//  $su_result = Check_SU_Password($inpassword,"系所$dept輸入密碼");

//  print("$inpassword (in) <---> (real) $real_password<br>\n");
//  if( $md5_password_found==0 ) $DEPT_NEED_TO_CHANGE_PASSWORD = 1;		### Global var  
  if( $su_result == 1 )						return(1);
  if( ($inpassword == $real_password) and ($inpassword != ""))	return(1);

  Show_Password_Error_Message("dept");
}
/////////////////////////////////////////////////////////////////////////////////////////////////
/////  Check_Teacher_Password
/////  從行政自動化資料庫中抓取，檢查教師帳密是否符合
/////  Updates: 
/////    2016/01/12 Created by Nidalap :D~
/////////////////////////////////////////////////////////////////////////////////////////////////
function Check_Teacher_Password($teacher_id, $in_password)
{
  $sql = "
    select staff_cd , convert_from( decrypt ( decode( password, 'hex'), 'bsofafrfktr', 'aes'), 'utf-8') AS password
    from x00tpseudo_uid_ where staff_cd = '$teacher_id'";
  $DBH = PDO_connect("ccucore");
  $STH = $DBH->query($sql);
  $row = $STH->fetch(PDO::FETCH_ASSOC);
  if( $in_password == $row['password']) {
    return 1;
  }else{
	return 0;
  }  
}
/////
function SU_Log($reason, $id)
{
  global $LOG_PATH, $SUPERUSER;
  $log_file = $LOG_PATH . "SysAdm.log";
  $ip = getenv("HTTP_X_FORWARDED_FOR");
  if( $ip == "" ) { $ip = getenv("REMOTE_ADDR"); }
  if( !($SU_LOG = fopen($log_file, "a")))   die("Fatal: Cannot append su_log!");

  list($t, $time, $t2) = gettime("");
  fputs($SU_LOG, "$time at $ip : $reason $id\t\t" . getenv("SCRIPT_NAME") . "\n");
  fclose($SU_LOG);
  $SUPERUSER = 1;                     ### 全域變數，某些程式會用到
}

?>
