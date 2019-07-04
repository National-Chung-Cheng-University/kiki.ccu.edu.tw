#!/usr/local/bin/perl
##########################################################################
#####   new_message02.cgi
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
if( $Input{sticky} eq "on" ) {
  $sticky = "�O";
}else{
  $Input{sticky} = "off";
  $sticky = "�_";
}

$message_file = $MESSAGE_PATH . $Input{message_id} . ".txt";

while( -e $message_file ) {
#  $message_file .= "a";
  preg_replace(".txt", "a.txt", $message_file);
  print("�ɮפw�g�s�b, ��W��  $message_file.<BR>");
}

open(FILE, ">$message_file");
print FILE ("$Input{title}\n");
print FILE ("$Input{sticky}\n");
print FILE $Input{text};
close(FILE);

$message_id = Generate_Message_ID();
$Input{text} =~ s/\n/<BR>/mg;

print << "END_OF_HTML"
  <HTML>
    <HEAD>
      <TITLE>�ק��Ҥ��i�D��</TITLE>
      <meta http-equiv="Content-Type" content="text/html; charset=big5">
    </HEAD> 
    <BODY background="$GRAPH_URL./manager.jpg">
      <Center><H1>��Ҩt�Τ��i<hr></h1>
        ���i�w�g�s�W����!<P>
        <TABLE border=0> 
          <TR>
            <TD bgcolor=YELLOW>�T��id:</TD>
            <TD>$Input{message_id}</TD>
          </TR>
          <TR>
            <TD bgcolor=YELLOW>���D:</TD>
            <TD>$Input{title}</TD>
          </TR>
          <TR>
            <TD bgcolor=YELLOW>�m��:</TD>
            <TD>$sticky</TD>
          </TR>
          <TR>
            <TD bgcolor=YELLOW>���e</TD>
            <TD>$Input{text}</TD>
          </TR>
        </TABLE>
        <br>
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