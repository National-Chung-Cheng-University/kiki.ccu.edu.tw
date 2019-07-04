#!/usr/local/bin/perl
##########################################################################
#####   Create_Password1.cgi
#####   批次產生新生密碼
#####   Coder: Nidalap
#####   Date : 2001/08/09
#####   Note : 原政策是產生隨機密碼, 今年改為預設為身份證號
#####          系統讀取由學籍資料轉來的 student.txt,
#####          為沒密碼的學生產生密碼檔.
##########################################################################
print("Content-type:text/html\n\n");
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Password.pm";
require $LIBRARY_PATH . "Error_Message.pm";
$fs = "<FONT size=2>";

%Input = User_Input();

$result = Check_SU_Password($Input{password}, "su", "su");
if( $result ne "TRUE" ) {
  print("Password Check Error!!");
  exit(0);
}
$student_txt = $REFERENCE_PATH . "student.txt";

($j,$j,$j,$j,$j,$j,$j,$j,$j,$mtime,@j) = stat($student_txt);
($j,$min,$hour,$mday,$mon,$year,@j) = localtime($mtime);
$year += 1900;

print qq (
  <HEAD><TITLE>產生新生密碼</TITLE></HEAD>
  <BODY background=$GRAPH_URL/bk.jpg>
    <CENTER>
      <H1>產生新生密碼</H1>
      <HR>
      <FORM action="Create_Password2.cgi" method=POST>
      
      產生密碼前請先確認學籍資料已更新, 包含新生資料.<BR>
      (上次更新時間: <FONT color=RED>$year年$mon月$mday日, $hour:$min</FONT>)<P>

      <INPUT type=hidden name=password value="$Input{password}">
      <INPUT type=SUBMIT value="產生所有無密碼學生的密碼資料">
);
