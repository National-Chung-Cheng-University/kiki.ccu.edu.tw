1;

$PATH="/ultra2/project/ccmisp01/WWW";
$LIB="/ultra2/project/ccmisp01/WWW/cgi-bin/library";
$CGI="http://kiki.ccu.edu.tw/~ccmisp01/cgi-bin/Query";
$PASS="/ultra2/project/ccmisp01/password";
$HTTP="http://kiki.ccu.edu.tw/~ccmisp01";

## Begin of sub Print_Html_Header ##

sub Print_Html_Header
{
 my($Title,$BG);

 ($Title,$BG)=@_;
 print "<Html>\n";
 print "<Head><Title>$Title</Title></Head>\n";
 print "<Body Background=\"$BG\">\n";
 print "<center>\n";
}

sub Print_Html_Tail
{
 print "</center>\n";
 print "</Body>\n";
 print "</Html>\n";
}

sub CheckPasswd()
{
 my(@Pass,$P_Line,$PassWd,$SysAdmPass,$crypt_salt);
 
 $crypt_salt="tw";

 ## 讀取系統管理者 password ##

 if( -e "$PASS/SysAdm.pwd")
 {
 open(FILE,"<$PASS/SysAdm.pwd");
  $SysAdmPass=<FILE>; chop($SysAdmPass); 
 close(FILE);
 }
 else { Error("無法讀取系統管理者密碼檔...請與系統管理者聯絡"); }

 $PassWd= crypt( $Input{'passwd'},$crypt_salt );

 if( crypt( $Input{'passwd'} ,"pa" ) eq $SysAdmPass ) 
 { return; }
 
 if( -e "$PASS/Password_Of_Teachers" )
 {
 open(FILE,"<$PASS/Password_Of_Teachers");
  @Pass=<FILE>; chop(@Pass);
 close(FILE);
 }
 else { Error("讀不到密碼檔..請聯絡系統管理者"); }
 foreach $P_Line(@Pass)
 {
  ($useless,$StaffCd,$StaffPw)=split(/\s+/,$P_Line);
  if( $StaffCd eq $Input{'name'} )
  {
   if( $StaffPw eq $PassWd ) { return; }
   else { Error("密碼錯誤"); }
  }
 } 
 Error("查無此使用者 $Input{'name'}");  
}

sub Error
{
 my($E_Msg);
 ($E_Msg)=@_;
 
 print "<p><p><p><hr>";
 print "<font size=5 color=brown>系統發現錯誤:</font>";
 print "<font size=4 color=red> $E_Msg </font><hr>";
 print "<br> 請查明錯誤原因後重新輸入 <br><p>";
 print "<a href=\"$HTTP/Teacher_Query.html\">";
 print "請按此重新登入</a>";
 Print_Html_Tail();
 exit(0);
}