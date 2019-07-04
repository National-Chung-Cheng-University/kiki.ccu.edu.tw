#!/usr/local/bin/perl
##########################################################################
#####   new_message01.cgi
#####   �ק�login Message���G��
#####   Coder: Nidalap :D~
#####   Date : 20080514
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
    
$message_id = Generate_Message_ID();

print << "END_OF_HTML"
  <HTML>
    <HEAD>
      <TITLE>�ק��Ҥ��i�D��</TITLE>
      <meta http-equiv="Content-Type" content="text/html; charset=big5">
    </HEAD> 
    <BODY background="$GRAPH_URL./manager.jpg">
      <Center><H1>��Ҩt�Τ��i<hr></h1>
      <FORM action="new_message02.cgi" method=POST>
        <INPUT type=hidden name=password value=$Input{password}>
        <TABLE border=0> 
          <TR>
            <TD bgcolor=YELLOW>�T��id:</TD>
            <TD><INPUT name=message_id value=$message_id></TD>
          </TR>
          <TR>
            <TD bgcolor=YELLOW>���D:</TD>
            <TD><INPUT name=title></TD>
          </TR>
          <TR>
            <TD bgcolor=YELLOW>�m��:</TD>
            <TD><INPUT type=checkbox name=sticky></TD>
          </TR>
          <TR>
            <TD bgcolor=YELLOW>���e</TD>
            <TD><TEXTAREA cols=50 rows=10 name=text></TEXTAREA></TD>
          </TR>
        </TABLE>
        <br>
        <INPUT type=submit value="�T�w�ק�">
      </FORM>
    </BODY>
  </HTML>
END_OF_HTML
;

###########################################################################
sub Generate_Message_ID()
{
  my(%time, $message_file_test);
  
#  opendir(MSG, $MESSAGE_PATH) or mkdir($MESSAGE_PATH);
#  @files = readdir(MSG);
  %time = gettime();
  $time{month} = "0".$time{month}	if( $time{month} < 10);
  $time{day} = "0".$time{day}		if( $time{day} < 10);  
  $message_id = $time{year} . $time{month} . $time{day};

  return($message_id);  
}