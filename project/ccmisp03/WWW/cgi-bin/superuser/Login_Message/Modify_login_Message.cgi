#!/usr/local/bin/perl
##########################################################################
#####   Modify_lgoin_Message.cgi
#####   �ק�login Message���G��
#####   Coder: victora
#####   Date : 6/9,1999
#####   Modified: 
#####		2008/06/04 �אּ���C���e�{, ��o���إ��D  Nidalap :D~
##########################################################################
print("Content-type:text/html\n\n");
require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH . "Error_Message.pm";

%Input = User_Input();

$pass_result = Check_SU_Password($Input{password}, "su", "su");
if($pass_result ne "TRUE") {
  print("�K�X���~!");
  exit(1);
}
    
opendir(MSGDIR, $MESSAGE_PATH) or mkdir($MESSAGE_PATH);
@files = readdir(MSGDIR);

print qq(
  <HTML>
    <HEAD>
      <TITLE>�ק��Ҥ��i�D��</TITLE>
      <meta http-equiv="Content-Type" content="text/html; charset=big5">
    </HEAD>
    <BODY background="$GRAPH_URL./manager.jpg">
      <Center><H1>��Ҩt�Τ��i<hr></h1>
      <FORM action="new_message01.cgi" method=POST>
        <INPUT type=hidden name=password value=$Input{password}>
        <INPUT type=submit value="�s�W��Ҥ��i">
      </FORM>
      <TABLE border=0 width=75%>
        <TR bgcolor=YELLOW>
          <TH bgcolor=YELLOW>�ק�</TH><TH bgcolor=YELLOW>�R��</TH>
          <TH bgcolor=YELLOW>���iID</TH><TH>�m��</TH><TH bgcolor=YELLOW width=60%>���D</TH>
        </TR>
);

foreach $file (@files) {
  next if( ($file eq ".") or ($file eq "..") );
  $file_open = $MESSAGE_PATH . $file;
  $message_id = $file;
  $message_id =~ s/.txt//; 
  open(FILE, $file_open);
  $title = <FILE>;
  $sticky = <FILE>;
  $sticky =~ s/\n//;
  if( $sticky eq "on" ) {
    $sticky = "<FONT color=RED>�O</FONT>";
  }else{
    $sticky = "&nbsp";
  }
  print qq(
    <TR>
      <TD><A href="modify_message01.cgi?message_id=$message_id&password=$Input{password}">�ק�</A></TD>
      <TD><A href="delete_message01.cgi?message_id=$message_id&password=$Input{password}">�R��</A></TD>
      <TD>$message_id</TD><TD>$sticky</TD><TD>$title</TD>
    </TR>\n
  );
}


print << "END_OF_HTML"
      </TABLE>
    </BODY>
  </HTML>
END_OF_HTML

