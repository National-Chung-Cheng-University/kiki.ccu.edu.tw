#!/usr/local/bin/perl
##########################################################################
#####   Create_Password1.cgi
#####   �妸���ͷs�ͱK�X
#####   Coder: Nidalap
#####   Date : 2001/08/09
#####   Note : ��F���O�����H���K�X, ���~�אּ�w�]�������Ҹ�
#####          �t��Ū���Ѿ��y�����Ӫ� student.txt,
#####          ���S�K�X���ǥͲ��ͱK�X��.
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
  <HEAD><TITLE>���ͷs�ͱK�X</TITLE></HEAD>
  <BODY background=$GRAPH_URL/bk.jpg>
    <CENTER>
      <H1>���ͷs�ͱK�X</H1>
      <HR>
      <FORM action="Create_Password2.cgi" method=POST>
      
      ���ͱK�X�e�Х��T�{���y��Ƥw��s, �]�t�s�͸��.<BR>
      (�W����s�ɶ�: <FONT color=RED>$year�~$mon��$mday��, $hour:$min</FONT>)<P>

      <INPUT type=hidden name=password value="$Input{password}">
      <INPUT type=SUBMIT value="���ͩҦ��L�K�X�ǥͪ��K�X���">
);
