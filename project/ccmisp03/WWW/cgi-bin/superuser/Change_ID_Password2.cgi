#!/usr/local/bin/perl

require "../../../LIB/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";

%Input = User_Input();

print("Content-type:text/html\n\n");
print("<CENTER><H1>�ǥͪ����iŪ, �N�±K�X�ର�s�Ǹ��K�X</H1></CENTER>");

$old_file = $STUDENT_PASSWORD_PATH . $Input{old_id} . ".pwd";
$new_file = $STUDENT_PASSWORD_PATH . $Input{new_id} . ".pwd";
#print("$old_file<br>$new_file");

if( -e $old_file ) {
  system("mv $old_file $new_file");
  print("���ɧ���!!!");
}else{
  print("�䤣���¾Ǹ�!!!");
}
