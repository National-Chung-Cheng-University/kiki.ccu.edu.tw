#!/usr/local/bin/perl

print("Content-type:text/html\n\n");
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Student.pm";

print $EXPIRE_META_TAG;
%Input = User_Input();

%action_map = (
  "Add"=>"加選", "Delete"=>"退選", "Print"=>"列印選課單", "View"=>"檢視已選修科目",
  "DelWait"=>"學生點選(延遲)退選",
  "Passwd"=>"更改密碼", "PasswdFail"=>"更改密碼失敗(資料庫", 
  "PasswdRevert"=>"密碼還原(更改ldap密碼失敗)",
  "Login"=>"成功\登入", "LoginFail"=>"不成功\登入", "Logout"=>"使用者登出",
  "Login_SSO"=>"SSO登入",
  "LoginM"=>"行動版登入",
  "LoginE"=>"英文版登入",
  "Online"=>"仍在線上", "TimeOut"=>"過時自動登出",
  "Apply_Concent"=>"申請加簽單", "View_Concent"=>"檢視加簽單"
);
%by_whom_map = (
  "SELF"=>"自行操作","SYSTEM_CHOOSE"=>"系統(限修)篩選","PRE_CHOOSE"=>"先修篩選",
  "DUP_CHOOSE"=>"重複修習篩選","UNDETERMINED"=>"未知", "CHECK_COURSE3"=>"檢查科目異常處理",
  "DELAYED_DEL"=>"延遲退選實際執行"
);

#%student = Read_Student($Input{id});
print qq(
  <HEAD><TITLE>學生加退選log記錄資料</TITLE></HEAD>
  <BODY background="$GRAPH_URL//ccu-bg.jpg">
    <CENTER>
      <H1>學生加退選log記錄資料</H1><HR>
      查詢條件: $Input{value}<BR>\n
);

if( $Input{LOGFILE} eq "previous" ) {
  $log_file = $DATA_PATH . "Student.old.log";
}else{
  $log_file = $DATA_PATH . "Student.log";
}

my $tmpfile = "/tmp/Student.log.grep";
system("grep $Input{value} $log_file > $tmpfile");

open(TMP, $tmpfile);
@line = <TMP>;
close(TMP);
unlink $tmpfile;
print("<TABLE border=1>");
print("<TR><TD>學號</TD><TD>動作</TD><TD>日期</TD><TD>來源</TD><TD>科目代碼</TD><TD>班別</TD><TD>屬性</TD><TD>(退選)原因</TD><TD>管理者</TD>\n");
foreach $line (@line) {
  $tr_bg = "";
  $su = "";
  $hit = 0;
  if($line =~ /SU/) {
    $su = "是";
    $line =~ s/SU//;
  }
  ($action,$day,$ip,$id,$course,$group,$property, $by_whom, $su, $mobile) = split(/\s:\s/,$line);
  $ip =~ s/\s//;
  $action =~ s/\s//g;
  $action_display = $action_map{$action};				###  「動作」顯示資訊
  $action_display = $action   if( $action_display eq "" );
#  $by_whom =~ s/\s//g;
  $by_whom_display = $by_whom_map{$by_whom};				###  「退選原因」顯示資訊
  $by_whom_display = $by_whom  if( $by_whom_display eq "");
  
#  $action="加選"       if($action =~ /Add/);
#  $action="退選"       if($action eq "Delete");
#  $action="列印選課單" if($action =~ /Print/);

  #####  設定 row bgcolor
  if( $Input{HIGHLIGHT} eq "on" ) {
    $tr_bg="BGCOLOR=#FF99FF"  if( $action eq "LoginFail" );
    $tr_bg="BGCOLOR=#99FF99"  if( $action eq "Add" );
    $tr_bg="BGCOLOR=#FFFF99"  if( $action eq "Delete" );
	$tr_bg="BGCOLOR=#EEEE99"  if( $action eq "DelWait" );
    $tr_bg="BGCOLOR=#99FFFF"  if( $action eq "Apply_Concent" );
    $tr_bg="BGCOLOR=#FF0000"  if( $action eq "PasswdFail" );
    $tr_bg="BGCOLOR=#FF0000"  if( $action eq "PasswdRevert" );
  }
  #####  過濾條件  
  next if( ($action =~ /Login/) and ($Input{NO_LOGIN} eq "on") );
  next if( ($actioLn eq "Online") and ($Input{NO_ONLINE} eq "on") ); 
    
  print("<TR $tr_bg><TD>$id</TD><TD>$action_display</TD><TD>$day</TD><TD>$ip</TD><TD>$course</TD>");
  print("<TD>$group</TD><TD>$property</TD><TD>$by_whom_display</TD><TD>$su</TD></TR>");
}
print("</TABLE>");
