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
require $LIBRARY_PATH . "Student.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Password.pm";
require $LIBRARY_PATH . "Error_Message.pm";
$fs = "<FONT size=2>";

%Input = User_Input();

##########################  �ˬdSU�K�X�O�_���T ###################
$result = Check_SU_Password($Input{password}, "su", "su");
if( $result ne "TRUE" ) {
  print("Password Check Error!!");
  exit(0);
}

##########################  ���ͽеy�᪺HTML #####################
print qq (
  <HEAD><TITLE>���ͷs�ͱK�X</TITLE></HEAD>
  <BODY background=$GRAPH_URL/bk.jpg>
    <CENTER>
      <H1>���ͷs�ͱK�X</H1>
      <HR>
      �K�X���ͤ�, �еy��...
);
$| = 1;
print "";
###########################
%S = Read_All_Student_Data();
@student = Find_All_Student();

$junk = "";
$count = 0;
foreach $student (@student) {
  $password_file = $STUDENT_PASSWORD_PATH . $student . ".pwd";
  if( not (-e $password_file) ) {
#    print("$student -> $$S{$student}{name} $$S{$student}{personal_id}<BR>\n");
    ($junk, $crypt_salt) = Create_Random_Password();
    $crypt_salt =~ /^(..)/;
    $crypt_salt = $1;       ### ���oRandom Crypt salt

    $password = Crypt($$S{$student}{personal_id}, $crypt_salt);
    $password = $crypt_salt . $password;

#    print("($$S{$student}{personal_id}, $crypt_salt) -> $password<BR>\n");
    Change_Student_Password($student, $junk, $junk, $password);
    $count++;
  }
}

############################ JOB FINISHED ########################
print qq(
  �@���� $count ���s�ͱK�X���.
);
