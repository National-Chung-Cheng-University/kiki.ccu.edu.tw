#!/usr/local/bin/perl
##########################################################################
#####   delete_message01.cgi
#####   �R��login Message���G��
#####   Coder: Nidalap :D~
#####   Date : 20080520
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

$message_file = $MESSAGE_PATH . $Input{message_id} . ".txt";

if( unlink($message_file) ) {
  print("���i�w�R��<BR>\n");
}else{
  print("�R�����~!<BR>\n");
}