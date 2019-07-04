1;
use Digest::MD5 qw(md5 md5_hex md5_base64);

#########################################################################
#####   Password.pm
#####   所有與密碼相關的函式
#####       Crypt()
#####       Check_Dept_Password()
#####       ......
#####   Coder: Nidalap
#####   Updates:
#####     1998/12/24  Created?
#####  	  2009/11/18  密碼改為 MD5 編碼，相關增修  Nidalap :D~
#########################################################################

#########################################################################
sub Create_Random_Password
{
  my(@char, $i, $char, $salt,  $password, $crypt_pass);
#  @char = ("a","b","c","d","e","f","g","h","i","j","k","m","n","p",
#           "q","r","s","t","u","v","w","x","y","z","A","B","C","D",
#           "E","F","G","H","J","K","L","M","N","P","Q","R","S","T",
#           "U","V","W","X","Y","Z","2","3","4","5","6","7","8","9");

  @char = ("a","b","c","d","e","f","g","h","i","j","k","m","n","p",
           "q","r","s","t","u","v","w","x","y","z");

  $salt = $char[int(rand(@char))];
  $salt .= $char[int(rand(@char))];
  for($i=0; $i<5; $i++) {
    $char = int( rand(@char) );
    $char = $char[$char];
    $password .= $char;
  }
  if( $USE_MD5_PASSWORD == 1 ) {
    $crypt_pass = md5_hex($password);
  }else{
    $crypt_pass = Crypt($password, $salt);
    $crypt_pass = $salt . $crypt_pass;
  }
  return($password, $crypt_pass);

}
#########################################################################
sub Change_Dept_Password
{
  my($password_file, $dept, $new_password, $md5_password);
  my($su_result, $crypt_salt);
  ($dept,$old_password, $new_password) = @_;

  ###  將密碼寫入 kiki 的 MD5 密碼檔
  if( $USE_MD5_PASSWORD == 1 ) {
    $password_file = $DEPT_PASSWORD_MD5_PATH . $dept . ".pwd";
    $md5_password = md5_hex($new_password);
    open(FILE, ">$password_file"); 
    print FILE $md5_password;
    close(FILE);
  }
  ###  然後將密碼寫入 kiki 舊的 DES 密碼檔
  $crypt_salt = "pa";
  $password_file = $DEPT_PASSWORD_PATH . $dept . ".pwd";
#  Check_Dept_Password($dept, $old_password);
#  print("new = $new_password, salt = $crypt_salt<br>\n");
  $new_password = Crypt($new_password, $crypt_salt);
  $new_password = $crypt_salt . $new_password;
  open(FILE, ">$password_file"); 
    print FILE $new_password;
  close(FILE);
  Dept_Log("PASSWD", $dept, "", "");

  if( $USE_MD5_PASSWORD == 1 ) {
    return($md5_password);		###  回傳編碼加密過後的密碼
  }else{
    return($new_password);
  }
}

#########################################################################
#sub Change_Student_Password
#{
#  my($password_file, $id, $old_password, $new_password, $salt);
#  ($id, $dept, $old_password, $new_password) = @_;
#  if( $USE_MD5_PASSWORD == 1 ) {
#    $password_file = $STUDENT_PASSWORD_MD5_PATH . $id . ".pwd";
#  }else{
#    $password_file = $STUDENT_PASSWORD_PATH . $id . ".pwd";
#  }
#  open(FILE, ">$password_file") or Fatal_Error("Cannot open file $password_file in Password::Change_Student_Password");
#  print FILE $new_password;
#  close FILE;
#  Student_Log("Passwd",$id);
#}
#
#
#########################################################################
#####   Read_Crypt_Salt()
#####   讀取密碼檔中 crypt 所用的 salt, 用以將使用者輸入明碼編碼
#########################################################################
sub Read_Crypt_Salt
{
  my($id, $type, $salt);
  my($password_file);
  ($id, $type) = @_;
  
  if     ($type eq "dept") {
    $password_file = $DEPT_PASSWORD_PATH . $id . ".pwd";
  }elsif ($type eq "teacher") {
    $password_file = $TEACHER_PASSWORD_PATH . $id . ".pwd";
  }elsif ($type eq "student") {
    $password_file = $STUDENT_PASSWORD_PATH . $id . ".pwd";
  }
  if( open(PASSWORD, $password_file) ) {
    $salt = <PASSWORD>;
    close(PASSWORD);
    $salt =~ /^(..)/;
    $salt = $1;
  }else{
    if( $type eq "dept" ) {
      print("密碼資料錯誤, 請洽電算中心!");
      exit(1);
    }else{
      print("學號輸入錯誤, 請重新輸入學號!");
    }
  }
  if($salt eq "")  { $salt = "aa" }
#    print("$id 's salt = $salt<br>\n");
  return $salt;
}

#########################################################################
#####   Crypt()
#####   若輸入有兩個值, 則以後者為salt對前者crypt編碼, 
#####   若無則隨機找出crypt salt, 以crypt()將明碼的密碼編碼
#########################################################################
sub Crypt
{
  my($inpassword, @char, $num1, $num2, $crypt_salt, $password);
  ($inpassword, $crypt_salt) = @_;

  if($crypt_salt eq "") {
     @char = ("a","b","c","d","e","f","g","h","i","j","k","m","n","p",
              "q","r","s","t","u","v","w","x","y","z","A","B","C","D",
              "E","F","G","H","J","K","L","M","N","P","Q","R","S","T",
              "U","V","W","X","Y","Z","2","3","4","5","6","7","8","9");
     srand(time ^ $$);
     $num1 = int( rand(@char) );
     $num2 = int( rand(@char) );
     $crypt_salt = $char[$num1] . $char[$num2];
  }
  
#  print("salt = $crypt_salt<br>");
   
  $password = crypt($inpassword,$crypt_salt);

#  print("(before, salt, after) = ($inpassword, $crypt_salt, $password)<br>\n");
  $password =~ s/^..//;
  return($password);
#  return($password, $crypt_salt);     ##  後面一個變數在Nov01,1999加入
				      ##  by Nidalap
}

#########################################################################
#####  Check_Dept_Password()
#####  檢查系所輸入密碼, 是否為正確密碼或管理者密碼
#########################################################################
sub Check_Dept_Password
{
  my($password_file, $dept, $inpassword, $real_password);
  my $su_result;
  my $md5_password_found = -1;			### [-1,0,1] = [不需要,找不到,找到了]
  ($dept,$inpassword) = @_;

#  Error("[$dept,$inpassword]<BR>");
  if( ($dept eq "") or ($inpassword eq "") ) {
    Error("帳號密碼錯誤！");
#    print("Error!");
#    exit;
  }

  if( $USE_MD5_PASSWORD == 1 ) {		#####  檢查 MD5 版本的密碼
    $password_file = $DEPT_PASSWORD_MD5_PATH . $dept . ".pwd";
    if( open(PASSWORD,"$password_file") ) {	  ###    MD5 版本的密碼存在
      $md5_password_found = 1; 
      $real_password = <PASSWORD>;
      close(PASSWORD);
      $real_password =~ s/\n//;
    }else{					  ###    MD5 版本的密碼不存在
      $md5_password_found = 0;
    }
  }
                                                #####  如果設定不用 MD5, 或是找不到 MD5 版本密碼
  if( ($USE_MD5_PASSWORD!=1) or ($md5_password_found!=1) ) {  #####  就使用 DES 密碼認證
#    print("dept = $dept; inpassword = $inpassword<br>");
    $password_file = $DEPT_PASSWORD_PATH . $dept . ".pwd";
#    print("file = $password_file<BR>");
    open(PASSWORD,"$password_file") or
      Error("密碼錯誤！\n");
    $real_password = <PASSWORD>;
    close(PASSWORD);
    $real_password =~ s/\n//;
    $real_password =~ s/^..//;
  }
 
#  print("Checking su: $inpassword, $dept"); 
  $su_result = Check_SU_Password($inpassword,"dept", $dept);
#  $su_result = Check_SU_Password($inpassword,"系所$dept輸入密碼");

#  print("$inpassword (in) <---> (real) $real_password<br>\n");
  $DEPT_NEED_TO_CHANGE_PASSWORD = 1   if( $md5_password_found==0 );   ### Global var  
  return("TRUE")  if( $su_result eq "TRUE" );
  return("TRUE")  if( ($inpassword eq $real_password) and ($inpassword ne ""));

  Show_Password_Error_Message("dept");
  
}
#########################################################################
#####   Check_Teacher_Password()
#####   檢查教師輸入密碼 
#########################################################################
sub Check_Teacher_Password
{
  my($password_file,$teacher_id, $inpassword, $real_password);
  my($su_result);
  
  ($teacher_id, $inpassword) = @_;
  $password_file = $TEACHER_PASSWORD_PATH . $teacher_id . ".pwd";
  open(TEACHER, $password_file) or return("ERROR:Cannot open file $teacher_file");
  $real_password = <TEACHER>;
  close(TEACHER);
  $real_password =~ s/\n//;
  $real_password =~ s/^..//;
  $su_result = Check_SU_Password($inpassword, "teacher", $teacher_id);
#  $su_result = Check_SU_Password($inpassword, "教師輸入密碼");
 
#  print("$inpassword (in) <---> (real) $real_password<br>\n");
  return("TRUE")   if( $su_result eq "TRUE" );
  return("TRUE")   if( ($inpassword eq $real_password) and ($inpassword ne "") );
  Show_Password_Error_Message("teacher");
}
#########################################################################
sub Check_Student_Password
{
  my($id, $inpassword, $real_password, $password_file);
  ($id, $inpassword, $personal_id) = @_;
  
#  print "Checking $id, $inpassword, $personal_id";
  
  if( $USE_MD5_PASSWORD == 1 ) {			###  判斷要讀取哪個版本的密碼
    $password_file = $STUDENT_PASSWORD_MD5_PATH . $id . ".pwd";
  }else{
    $password_file = $STUDENT_PASSWORD_PATH . $id . ".pwd";
  }
  if( open(PASSWORD, $password_file) ) {
    $real_password = <PASSWORD>;
    close(PASSWORD);
    $real_password =~ s/\n//;
    if( $USE_MD5_PASSWORD == 1 ) {			###  如果是 MD5, 不需切掉 salt
      # (do nothing)
    }else{
      $real_password =~ s/^..//;
    }
    $su_result = Check_SU_Password($inpassword, "student", $id);
#    $su_result = Check_SU_Password($inpassword, "學生輸入密碼");
  }else{
    Fatal_Error("Canot open file $password_file in module Password.pm!");
  }
#  print("[id,in,real,personid] = [$id, $inpassword, $real_password, $personal_id]<BR>\n"); 
  return("TRUE")   if( $su_result eq "TRUE" );
  
  if( ($inpassword eq $real_password) and ($inpassword ne "" ) ) {  ##  密碼正確
#    if( $TEMP_FLAG_CHANGE_PASS == 1 ) {                             ##  TEMP! 2004/02/27
#      $student_changed_temp_file = $PASSWORD_PATH . "student_changed_temp/" . $id . ".pwd";
#      if( -e($student_changed_temp_file) ) {
#        open(TEMP_PASS, "$student_changed_temp_file");
#        $temp_pass = <TEMP_PASS>;
#        close(TEMP_PASS);
#        $temp_pass =~ s/\n//;
#        $temp_pass =~ s/^..//;
##        print("$inpassword <-> $temp_pass<BR>\n");
##        print("$personal_id <-> $inpassword<BR>\n");
#        if( $inpassword eq $temp_pass ) {
#          return("DEFAULT_PASSWORD2");
#        }
#      }
#    }
    if( ($personal_id ne "") and ($personal_id eq $inpassword) ) {  ##  若使用預設密碼
      return("DEFAULT_PASSWORD") if( $personal_id eq $inpassword );
    }else{ 
      return("TRUE");
    }
  }
#  if( ($personal_id ne "") and ($personal_id eq $inpassword) ) {  ## 若使用預設密碼
#    Show_Password_Error_Message2();
#  }
  Show_Password_Error_Message("student");
}
#########################################################################
################################################################################
#####  Check_Cashier_Password()
#####  檢查出納組使用功能的帳號密碼
#####  由於新增出納組查詢學生選課單, 而新增的功能. (2009/01)
#####  Coder: Nidalap :D~, 2009/01/19
sub Check_Cashier_Password
{
  my($id, $password) = @_;

  %white_list = ( "cashier" => "cash123" );

#  Check_SU_Password($password, "cashier_login", "cashier");

#  print("[$id, $password]<BR>");
  if( ($white_list{$id} eq $password) and ($id ne "") ) {
    return 1;
  }else{
    print("密碼錯誤!<P>\n");
    die();
  }
}
##################################################################################
sub Check_SU_Password
{
  my($su_file, $inpass, $reason, $id, @su_password, $password_file, $su_pass);
  my($crypt_salt);
  my($log_file, %time);
  $su_pass = 0;
  ($inpass, $reason, $id) = @_;
#  ($inpass, $reason) = @_;
  
  if( $USE_MD5_PASSWORD == 1 ) {                        ###  MD5 版本的密碼
    $su_file = $PASSWORD_PATH . "SysAdm_MD5.pwd";
    open(SU, "$su_file") or
      return("ERROR:Cannot open file $su_file in module Password.pm\n");
    $su_password = <SU>;
    $su_password =~ s/\n//;
    close(SU);
    if( $su_password eq $inpass ) {
      $su_pass = 1;
    }
  }else{						###  DES 版本的密碼：要先讀取 salt
    $su_file = $PASSWORD_PATH . "SysAdm.pwd";   
    $password_file = $DEPT_PASSWORD_PATH . $id . ".pwd" 
        if( $reason eq "dept" );
    $password_file = $STUDENT_PASSWORD_PATH . $id . ".pwd" 
        if( $reason eq "student");
    $password_file = $TEACHER_PASSWORD_PATH . $id . ".pwd"
        if( $reason eq "teacher");
    $password_file = $su_file
        if( $reason eq "su" );

#    print("reading file: $password_file<br>\n");
    open(PASS, $password_file) 
#        or return("FALSE");     ###  modified by Nidalap, Aug12,1999
        or Fatal_Error("Cannot open file $password_file at Password::Check_SU_Password(), arg=($inpass, $reason, $id)\n");
    $crypt_salt = <PASS>;
    close(PASS);
    $crypt_salt =~ /^(..)/;
    $crypt_salt = $1;
#    $crypt_salt = "aa" if ($crypt_salt eq "");
#    print("crypt_salt = $crypt_salt!!<br>");
    open(SU, "$su_file") or
      return("ERROR:Cannot open file $su_file in module Password.pm\n");
    @su_password = <SU>;
    close(SU);

    foreach $su_password (@su_password) {		###  DES 版本需要逐一判別不同 salt 版本的密碼
      $su_password =~ s/\n//;
      $su_password =~ /(^..)/;
      $su_salt = $1;
      $su_password =~ s/^..//;
      $crypt_salt = $su_salt  if($crypt_salt eq "");  ## 若學生選課檔不存在
      if( $su_salt eq $crypt_salt ) {
#        print("su_salt = $crypt_salt; su_pass = $su_password(inpass = $inpass)<br>");
        if( $su_password eq $inpass ) {
          $su_pass = 1;
          last;
        }
      }
    }
  }
  ###  到此為止，以 $su_pass 的值代表管理者密碼驗證是否成功
  if( $su_pass == 1 ) {
    $log_file = $LOG_PATH . "SysAdm.log";
    my($ip);
    if($ENV{HTTP_X_FORWARDED_FOR} eq "")  { $ip = $ENV{REMOTE_ADDR}; }
    else                                  { $ip = $ENV{HTTP_X_FORWARDED_FOR}; }
    umask(000);
    open(LOG,">>$log_file") or 
      Fatal_Error("ERROR:Cannot append $log_file in Password::Check_SU_Password()!");
    %time = gettime();
    print LOG ("$time{time_string} at $ip : $reason $id\t\t$ENV{'SCRIPT_NAME'}\n");
    close(LOG);
    $SUPERUSER = 1;			### 全域變數，某些程式會用到
#    print("SU check okay\n");
    return("TRUE");
  }else{
#    print("su check fail: [inpass, su_pass] = [$inpass, $su_password]\n");
    return("FALSE");
  }
}
############################################################################
sub Show_Password_Error_Message
{
  ($action) = @_;
  print("<HEAD>$EXPIRE_META_TAG</HEAD>\n");
  print("<BODY background=$GRAPH_URL/ccu-sbg.jpg>");

  print("<Center><H1>密碼確認結果<hr></H1>");
  print("您輸入的密碼有誤, 請重新輸入!<p>");
  print("<FONT color=RED>請區分英文字母大小寫(新生密碼身份證號一律為大寫)</FONT><P>");

  if( $action eq "dept" ) {
     $url = $PROJECT_URL . "Login.cgi";
     print("<A href=$url>回開排課系統首頁</A>");
  }
  if( $action eq "student" ) {
     $url = $CLASS_URL . "Login.cgi";
     print("<A href=$url>回選課系統首頁</A>");
  }
  exit(2);
}
############################################################################
sub Show_Password_Error_Message2
{
  print("<BODY background=$GRAPH_URL/ccu-sbg.jpg>");
  print qq(
    <CENTER>
    <TABLE border=0 width=60%>
      <TR><TD bgcolor=LIGHTYELLOW>
        <FONT color=RED>您使用身份證號做為密碼,
        為確保您選課帳號的安全, 系統已暫時將您的密碼改為生日,
        請改以生日做為密碼登入, 並立即更改密碼!</FONT>
        <P>
        生日格式: <FONT color=RED>YYMMDD</FONT><BR>
        生日使用中華民國年, 西元年請減1911.<BR>
        例:西元1975年(民國64年)3月6日生請填 640306
      </TD></TR>
    </TABLE>
       
  ); 
     $url = $CLASS_URL . "Login.cgi";
     print("<A href=$url>回選課系統首頁</A>");

  exit(2);
}
#################################################################################
#####  Need_To_Change_Password
#####  判斷是否需要改密碼
#####  94 學年度第 1 學期開始, 將一般生的密碼與學籍整合, 並強制學生必須更改密碼與 email
#####  2005/08/29 Nidalap :D~
sub Need_To_Change_Password
{
  my ($id, $password) = @_;
  my($j, $mtime);
  
  if( $USE_MD5_PASSWORD == 1 ) {
    $password_file = $STUDENT_PASSWORD_MD5_PATH . $id . ".pwd";
  }else{
    $password_file = $STUDENT_PASSWORD_PATH . $id . ".pwd";
  }
  ($j,$j,$j,$j,$j,$j,$j,$j,$j,$mtime,$j,$j,$j,) = stat($password_file);
#  print("mtime = $mtime<BR>\n");
  if( $mtime < 1125831944 ) {              ###  大約是 2005/09/04
    return(1);
  }else{ 
    return(0);
  }
}
##############################################################################
#####  Generate_Key()
#####  由學號, 密碼, 與大略的時間產生一個 md5 過的 key, 作為基本的安全保護,
#####  避免有心者直接連結改密碼網頁, 看到學生的部份個人資訊.
#####  Updates:
#####    2006/06/01 Created by Nidalap :D~
#####    2010/11/04 加入教專系統及其特殊判斷  Nidalap :D~
sub Generate_Key
{
  my($id, $password) = @_;
  $debug_flag = 0;
  $time = time();

  if( $password eq "" ) {           ##  如果沒有傳入 password, 使用預設密碼 
    $password = "ThiS_is_pAsswOrd_for_InfOtEst";
  }
  if( $password eq "bOsSlesSLESswORK" ) {	## 如果是教專系統進來
    $time = substr($time, 0, 6);		##   只取 timestamp 前六碼  
  }else{
    $time = substr($time, 0, 7);		## 其他人取前七碼
  }
  $key = $id . $time . $password;
  $key = md5_hex($key);

  if( $debug_flag == 1 ) {
    print("[ id,time,password,key ] = [ $id,$time,$password,$key ]<BR>\n");
  }

  return $key;
}
################################################################################
##############################################################################
#####  Generate_Key2()
#####  由學號, 密碼, 與傳入的時間timestamp產生一個 md5 過的 key, 作為基本的安全保護,
#####  避免有心者直接連結改密碼網頁, 看到學生的部份個人資訊.
#####  Updates:
#####    2013/10/02 與淑娟討論而得，由教專系統率先改用此方法（從Generate_Key改來）。
sub Generate_Key2
{
  my($id, $password, $in_timestamp) = @_;
  $debug_flag = 0;

  if( $password eq "" ) {           ##  如果沒有傳入 password, 使用預設密碼 
    $password = "ThiS_is_pAsswOrd_for_InfOtEst";
  }

  $key = $id . $in_timestamp . $password; 
  $key = md5_hex($key);

  if( $debug_flag == 1 ) {
    print("[ id,in_timestamp,password,key ] = [ $id,$in_timestamp,$password,$key ]<BR>\n");
  }

  return $key;
}
