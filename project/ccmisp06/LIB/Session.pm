1;

###########################################################################
#####  Session.pm
#####  處理 server-side session 的資料
#####  Nidalap :D~
#####  Created on 2005/02/17
###########################################################################

sub Create_Session_ID
{
  my($session_id);
  my $salt = "pa";
  my($id, $password) = @_;
  
  $session_id = crypt($time{hour}.$time{min}, $salt) 
                . crypt($id, $salt)
                . crypt($password, $salt); 
  $session_id =~ tr/\.\\\//A/;   ### 轉換為一個合法的 unix 檔名
  $session_id =~ s/pa//;
#  Clear_Session();               ### 清除過時的(其他人的) session files
  return($session_id);
}
###########################################################################
#####  此版本部份流程與 php 版本不同，請注意
sub Read_Session
{
  my($session_id, $new_flag, $renew_sess) = @_;
  my($id, $password, $login_time, $ip);
  my($j, $mtime, $diff_time);

  my $session_file = $SESSION_PATH . $session_id;

  my $now = time;  
#  print("utime $now, $now, $session_file<BR>\n");
  if( ($session_id =~ /\./) or ($session_id =~ /\//) or ($session_id =~ /\\/) 
       or ($session_id =~ /;/) or ($session_id =~ /\`/) or ($session_id =~ /~/) ) {
    Session_Illegal();			       ### 有問題的 session_id(可能是入侵者)
  }
#  print "opening sess file $session_file...<BR>\n";
  
  open(SESSION_FILE, "$session_file") or Session_Not_Found($new_flag);
  ($j,$j,$j,$j,$j,$j,$j,$j,$j,$mtime,$j,$j,$j,) = stat(SESSION_FILE);
  $diff_time = $now - $mtime;

#  print("mtime, now, diff = [ $mtime, $now, $diff_time ]<BR>\n");

  $id		= <SESSION_FILE>;
  chop($id);
  $password	= <SESSION_FILE>;
  chop($password);
  $login_time	= <SESSION_FILE>;
  chop($login_time);
  $ip		= <SESSION_FILE>;
  chop($ip);
  $add_course_count = <SESSION_FILE>;
  chop($add_course_count);
    
#    if( $ip ne $ENV{HTTP_X_FORWARDED_FOR} ) {     ### 避免有人從不同 IP 偷用 session_id
#      if( ($ip !~ $ENV{HTTP_X_FORWARDED_FOR}) and ($ENV{HTTP_X_FORWARDED_FOR} !~ $ip) ) {
#        Session_Wrong_IP();
#      }
#    }
  
  close(SESSION_FILE);
#    my $t_flag = utime($now, $now, $session_file);        ###  renew 這個 session 時間
  if( $diff_time > $TIME_OUT_SECONDS ) {       ### Timeout 自動登出
    close(SESSION_FILE);
    Destroy_Session($session_id, $id);
    Session_Time_Out();
  }else{                                       ### 沒有 timeout, 繼續
    if( $renew_sess == 1 ) {			###  更新 session 時間
      Write_Session($session_id, $id, $password, $add_course_count);
    }						###  或是放著等過期
#    print("renew($t_flag): $now, $now, $session_file<BR>\n");   
    return($id, $password, $login_time, $ip, $add_course_count);  
  }
}
###########################################################################
sub Write_Session
{
  my($session_id, $id, $password, $add_course_count) = @_;
  if( ($session_id =~ /\./) or ($session_id =~ /\//) or ($session_id =~ /\\/)
       or ($session_id =~ /;/) or ($session_id =~ /\`/) or ($session_id =~ /~/) ) {
    Session_Illegal();                         ### 有問題的 session_id(可能是入侵者)
  }
  
  my $ip = $ENV{HTTP_X_FORWARDED_FOR};
  my $login_time = time;
  my $session_file = $SESSION_PATH . $session_id;

  umask(000);
  open(SESSION_FILE, ">$session_file");
  print SESSION_FILE ("$id\n");
  print SESSION_FILE ("$password\n");
  print SESSION_FILE ("$login_time\n");
  print SESSION_FILE ("$ip\n");
  print SESSION_FILE ("$add_course_count\n");
  
  close(SESSION_FILE);
}
###########################################################################
sub Renew_Session
{
  my($session_id) = @_;
  my $session_file = $SESSION_PATH . $session_id;

  my $now = time;
  utime($now, $now, $session_file);

}
###########################################################################
#####  刪除 session 資料(登出)
#####  Updates:
#####    2009/10/26 改寫自 php 版本  Nidalap :D~
sub Destroy_Session
{
  my ($session_id, $student_id) = @_;
  my $session_file = $SESSION_PATH . $session_id;
#  print("Attemp to destroy session $session_file<BR>\n");

  if( -e $session_file )  {
    Student_Log("TimeOut", $student_id, "");
    if( unlink($session_file) ) {
      return(1);
    }else{
      return(0);
    }
  }else{
    return(-1);
  }
}

###########################################################################
#####  Clear_Session()
#####  清除過期 session files
#####  因為影響線上效率, 這個功能移到 crontab 執行.
#####  詳見 ~/BIN/Cron_jobs/
#####  Updated: 2005/02/24  Nidalap :D~
#sub Clear_Session
#{
#  my(@session_files, $session_file);
#  my($j, $mtime, $now, $diff_time);
#  
#  $now = time;
#  opendir(SESSIONDIR, $SESSION_PATH);
#  @session_files = readdir(SESSIONDIR);
#  close(SESSIONDIR);
#  foreach $file (@session_files) {
#    next if( $file eq "." );
#    next if( $file eq ".." );
#    $session_file = $SESSION_PATH . $file;
#    ($j,$j,$j,$j,$j,$j,$j,$j,$j,$mtime,$j,$j,$j,) = stat($session_file);
#    $diff_time = $now - $mtime;
#    if($diff_time >= $SESSION_CLEAR_SECONDS) {
#      unlink($session_file);
#    }
##    print("$session_file -> $diff_time<BR>\n");
#  }
#}
###########################################################################
#####  Session_Not_Cound()
#####  找不到 session file, 顯示此 session 是無效的錯誤訊息.
#####  因為會有 crontab 定期清除, 這是使用者最容易見到的 time out message
#####  Updated: 2005/02/24 Nidalap :D~
sub Session_Not_Found
{
  my($new_flag) = @_;
  my $link, @txt;
  
  if( $IS_ENGLISH ) {
    @txt = ("Re-login", "CCU Course Selection System", "CCU Course Selection System",
			   "Session timeout", "You have been logged out!");
  }else{
    @txt = ("我要重新登入", "國立中正大學選課系統", 
	           "中正大學<FONT color=RED></FONT>" . $SUB_SYSTEM_NAME . "選課系統", 
			   "您本次的登入已經無效!", "可能是因為太久沒有動作, 系統已經幫您登出!");
  }

  
#  if( $new_flag ) {
    $link = "<A href=\"index.html\" target=_top>" . $txt[0] . "</A>";
#  }else{
#    $link = "<A href=\"Login.cgi\">我要重新登入</A>";
#  }
  print '
    <html>
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>' . $txt[1] . '</title>
      </head>
      <body background="$GRAPH_URL/ccu-sbg.jpg">
        <center>
        <H1><FONT face="標楷體">' . $txt[2] . '
        <IMG src="$GRAPH_URL/mouse.gif">
        <BR><HR></H1>
           <font size=3 face="標楷體">
            ' . $txt[3] . '<BR>
            ' . $txt[4] . '<P>
            ' . $link . '
      </BODY>
    </HTML>
  ';
  exit();
}

###########################################################################
#####  Session_Time_Out()
#####  顯示該 session_id 是已經過期的.
#####  雖然有 crontab 清除過期的 session file, 但是因為 crontab 執行不很頻繁,
#####  仍有可能性過期的 session file 仍暫時存在.
#####  Updated: 2005/02/24 Nidalap :D~
sub Session_Time_Out
{
  my @txt;
  if( $IS_ENGLISH ) {
    @txt = ("Re-login", "CCU Course Selection System", "CCU Course Selection System",
			   "Your session has timed out!", "");
  }else{
    @txt = ("我要重新登入", "國立中正大學選課系統", 
	           "中正大學<FONT color=RED></FONT>" . $SUB_SYSTEM_NAME . "選課系統", 
			   "您本次的登入已經無效!", "可能是因為太久沒有動作, 系統已經幫您登出!");
  }

  print '
    <html>
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>' . $txt[1] . '</title>
      </head>
      <body background="$GRAPH_URL/ccu-sbg.jpg">
        <center>
        <H1><FONT face="標楷體">' . $txt[2] . '
        <IMG src="$GRAPH_URL/mouse.gif">
        <BR><HR></H1>
           <font size=3 face="標楷體">
            ' . $txt[3] . '<P>
            <A href="' . $CLASS_URL . '" target=_TOP>' . $txt[0] . '</A>
      </BODY>
    </HTML>
  ';
  exit();
}
##########################################################################
sub Session_Wrong_IP
{
  my @txt;
  if( $IS_ENGLISH ) {
    @txt = ("CCU Course Selection System", 
			   "CCU Course Selection System",
			   "Your IP address has changed! In order to protect your account,",
			   "please re-login.");
  }else{
    @txt = ("國立中正大學選課系統", 
	           "中正大學<FONT color=RED></FONT>" . $SUB_SYSTEM_NAME . "選課系統", 
			   "系統察覺到您的 IP 已經有改變, 為了保護您的選課資料", 
			   "請重新登入.");
  }

  print '
    <html>
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>' . $txt[0] . '</title>
      </head>
      <body background="$GRAPH_URL/ccu-sbg.jpg">
        <center>
        <H1><FONT face="標楷體">' . $txt[1] . '</FONT>
        <IMG src="$GRAPH_URL/mouse.gif">
        <BR><HR></H1>
           <font size=3 face="標楷體">
            ' . $txt[2] . '<P>
            <A href="Login.cgi">' . $txt[3] . '</A>
      </BODY>
    </HTML>
  ';
  exit();
}

##########################################################################
sub Session_Illegal
{
  my @txt;
  if( $IS_ENGLISH ) {
    @txt = ("CCU Course Selection System", 
			   "CCU Course Selection System",
			   "We have detected an unusual error in your data, ",
			   "please contact system administrator ext:14203");
  }else{
    @txt = ("國立中正大學選課系統", 
	           "中正大學<FONT color=RED></FONT>" . $SUB_SYSTEM_NAME . "選課系統", 
			   "您輸入的資料有嚴重錯誤(一般情況下, 應該不會出現),", 
			   "請洽程式設計者 校內分機 14203 李永祥");
  }

  print '
    <html>
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>' . $txt[0] . '</title>
      </head>
      <body background="$GRAPH_URL/ccu-sbg.jpg">
        <center>
        <H1><FONT face="標楷體">' . $txt[1] . '</FONT>
        <IMG src="$GRAPH_URL/mouse.gif">
        <BR><HR></H1>
           <font size=3 face="標楷體">
            ' . $txt[2] . '<P>
            <A href="mailto:nidalap@ccu.edu.tw">' . $txt[3] . '</A>
      </BODY>
    </HTML>
  ';
  exit();
}
##########################################################################
#####  Session_Add_Course_Limit()
#####  此 session 已經到達加選次數上限, 強迫離開!
#####  很可能是 robot, 所以還要 log 使用者資料, 供參考用
sub Session_Add_Course_Limit
{
  my($black_list_flag, $time, $id, $ip) = @_;

  Add_Ban_Record($time, $id, $ip);

  my $message;
  if( $black_list_flag == 1 )  {  
    $message = "系統偵測到您異常連續多次加選, 嚴重影響系統效能與其他同學權益.<BR>";
    $message .= "<FONT color=RED>依據第81次教務會議決議, 停權八小時</FONT>.<BR>";
    $message .= "我們已經開始嚴密監控您的選課行為, 請自重!<P>";
    $message .= "若系統誤判, 同學可在上班時間電洽教務處教學組, 或在任何時候 email: nidalap\@ccu.edu.tw";
  }else{
    $message = "請重新登入!";
  }
          
  print qq(
      <html>
        <head>
          <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
          <title>國立中正大學選課系統</title>
        </head>
        <body background="$GRAPH_URL/ccu-sbg.jpg">
          <center>
          <H1><FONT face="標楷體">中正大學<FONT color=RED></FONT>$SUB_SYSTEM_NAME選課系統</FONT>
          <IMG src="$GRAPH_URL/mouse.gif">
          <BR><HR></H1>
             <font size=3 face="標楷體">
             $message
        </BODY>
      </HTML>
  );
  exit();
}
##########################################################################
#####  Add_Ban_Record()
#####  將已經到達加選上限的學生加入 log 中, 以及加入停權名單中
#####  Date: 2005/04/29
sub Add_Ban_Record
{
  my($time, $id, $ip) = @_;
  my($j, $mtime, $now, $diff_time);
  $now = time;

  #####  加入到 log 中(另外靠程式分析此 log)
  my $limit_log = $LOG_PATH . "Add_Course_Limit.log";
  open(LIMIT_LOG, ">>$limit_log");
  print LIMIT_LOG ("$time, $id, $ip\n");
  close(LIMIT_LOG);

  ##### 加入停權名單中
  my $ban_file = $BAN_LIST_PATH . $id . ".ban";
  if( -e $ban_file ) {
    ($j,$j,$j,$j,$j,$j,$j,$j,$j,$mtime,$j,$j,$j,) = stat($ban_file);
    $diff_time = $now - $mtime;
    return if( $diff_time < 300 );   ### 如果是十分鐘內停的, 不重複寫入資料
  }
  open(BAN_FILE, ">>$ban_file");
  print BAN_FILE ("$now, $time, $id, $ip\n");
  close(BAN_FILE);
}
##########################################################################
#####  Read_Ban_Record()
#####  讀取停權名單, 看某學生是否在停權名單中
#####  傳回值若大於 0 則是停權中.
#####  Date: 2005/04/29
sub Read_Ban_Record
{
  my($now, $j, $mtime, $diff_time, $res_time, $ban_count);
  my(@lines, $ban_file, $bantime1, $bantime, $id, $ip);
  my($id, $ban_count_limit) = @_;
  $res_time = 0;

  my $ban_file = $BAN_LIST_PATH . $id . ".ban";
  if( -e $ban_file ) {
    $now = time;
    open(BANFILE, $ban_file);
    @lines = <BANFILE>;
    $ban_count = @lines;
    foreach $line (@lines) {
      ($bantime1, $bantime, $id, $ip) = split(/, /, $line);
    }
    $diff_time = $now - $bantime1;
#    print("$now - $bantime1 = $diff_time<BR>\n");
    $res_time = $BAN_DURATION - $diff_time;
  }
#  print("[count, limit] = [$ban_count, $ban_count_limit]<BR>\n");
#  print("[res_time, BAN_DURATION, diff_time] = [$res_time, $BAN_DURATION, $diff_time]<BR>\n");
  if( $ban_count >= $ban_count_limit ) {   ###  若異常加選超過 $ban_count_limit 次
    return($res_time);
  }else{                                   ###  沒超過的話, 繼續觀察不停權
    return(0);
  }
}
##########################################################################
#####  Show_Ban_Message()
#####  顯示停權訊息給學生看
#####  輸入值: [停權恢復尚需秒數, 是否離開程式flag]
#####  Date: 2005/04/29
sub Show_Ban_Message
{
  my($res_time, $quit_flag) = @_;
  
  $res_time = int($res_time / 60);

  my $message = "系統偵測到您異常連續多次加選, 嚴重影響系統效能與其他同學權益, ";
  $message .= "<FONT color=RED>依據第81次教務會議決議, 停權八小時</FONT>.";
  $message .= "我們已經開始嚴密監控您的選課行為, 請自重!<P>";
  $message .= "<CENTER>您大約在 ";
  $message .= $res_time;
  $message .= " 分鐘後才可以加退選.</CENTER><P>";
  $message .= "若系統誤判, 同學可在上班時間電洽教務處教學組, 或在任何時候 email: nidalap@ccu.edu.tw";

  print qq(
    <TABLE border=1 width=50%>
      <TR><TD bgcolor=YELLOW>
        $message
      </TD></TR>
    </TABLE>  
  );
  if( $quit_flag == 1 ) {
    exit();
  }
}

