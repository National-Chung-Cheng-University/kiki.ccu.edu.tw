#!/usr/local/bin/perl

require "../../../LIB/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";

%Input = User_Input();

print("Content-type:text/html\n\n");
print("<CENTER><H1>學生直接進讀, 將舊密碼轉為新學號密碼</H1></CENTER>");

$old_file = $STUDENT_PASSWORD_PATH . $Input{old_id} . ".pwd";
$new_file = $STUDENT_PASSWORD_PATH . $Input{new_id} . ".pwd";
#print("$old_file<br>$new_file");

if( -e $old_file ) {
  system("mv $old_file $new_file");
  print("轉檔完成!!!");
}else{
  print("找不到舊學號!!!");
}
