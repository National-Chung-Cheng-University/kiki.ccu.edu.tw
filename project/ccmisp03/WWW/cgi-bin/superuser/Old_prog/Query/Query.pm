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

 ## Ū���t�κ޲z�� password ##

 if( -e "$PASS/SysAdm.pwd")
 {
 open(FILE,"<$PASS/SysAdm.pwd");
  $SysAdmPass=<FILE>; chop($SysAdmPass); 
 close(FILE);
 }
 else { Error("�L�kŪ���t�κ޲z�̱K�X��...�лP�t�κ޲z���p��"); }

 $PassWd= crypt( $Input{'passwd'},$crypt_salt );

 if( crypt( $Input{'passwd'} ,"pa" ) eq $SysAdmPass ) 
 { return; }
 
 if( -e "$PASS/Password_Of_Teachers" )
 {
 open(FILE,"<$PASS/Password_Of_Teachers");
  @Pass=<FILE>; chop(@Pass);
 close(FILE);
 }
 else { Error("Ū����K�X��..���p���t�κ޲z��"); }
 foreach $P_Line(@Pass)
 {
  ($useless,$StaffCd,$StaffPw)=split(/\s+/,$P_Line);
  if( $StaffCd eq $Input{'name'} )
  {
   if( $StaffPw eq $PassWd ) { return; }
   else { Error("�K�X���~"); }
  }
 } 
 Error("�d�L���ϥΪ� $Input{'name'}");  
}

sub Error
{
 my($E_Msg);
 ($E_Msg)=@_;
 
 print "<p><p><p><hr>";
 print "<font size=5 color=brown>�t�εo�{���~:</font>";
 print "<font size=4 color=red> $E_Msg </font><hr>";
 print "<br> �Ьd�����~��]�᭫�s��J <br><p>";
 print "<a href=\"$HTTP/Teacher_Query.html\">";
 print "�Ы������s�n�J</a>";
 Print_Html_Tail();
 exit(0);
}