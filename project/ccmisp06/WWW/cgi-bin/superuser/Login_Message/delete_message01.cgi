#!/usr/local/bin/perl
##########################################################################
#####   delete_message01.cgi
#####   刪除login Message公佈欄
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
  print("密碼錯誤!");
  exit(1);
}

$message_file = $MESSAGE_PATH . $Input{message_id} . ".txt";

if( unlink($message_file) ) {
  print("公告已刪除<BR>\n");
}else{
  print("刪除錯誤!<BR>\n");
}