#!/usr/local/bin/perl
##########################################################################
#####   Course_Upper_Limit_Immune02.cgi
#####   �B���[ñ page #2
#####   ���\�ǥͥ[���@���, �����Ӭ�ح����B���H�ƭ���(���ݨ���L����)
#####   Coder: Nidalap
#####   Date : 09/13/2001
##########################################################################
print("Content-type:text/html\n\n");
require "../../library/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
#require $LIBRARY_PATH . "Student.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Course.pm";
require $LIBRARY_PATH . "Password.pm";
require "./Course_Upper_Limit_Immune.pm";
require $LIBRARY_PATH . "Student.pm";
require $LIBRARY_PATH."Error_Message.pm";


%Input   = User_Input();
%student = Read_Student($Input{stu_id});

$pass_result = Check_SU_Password($Input{password}, "su", "su");
if($pass_result ne "TRUE") {
  print("�K�X���~!");
  exit(1);
}

print qq(
  <HTML>
    <HEAD><TITLE>�B���[ñ�W��</TITLE></HEAD>
    <BODY background="$GRAPH_URL./manager.jpg">
      <Center><H1>�B���[ñ�W��<hr></h1>
);

if( $Input{action} eq "add" ) {
  if( ($Input{stu_id} eq "") or ($Input{course_id} eq "") or ($Input{course_group} eq "")) {
    print("��J��Ƥ�����!!<BR>\n");
    exit(1);
  }
  if( length($Input{stu_id}) != 9 ) {
    print("���~: �ǥ;Ǹ������� 9 �X!<BR>\n");
    exit(1);
  }
  if( length($Input{course_id}) != 7 ) {
    print("���~: ��إN���ݬ� 7 �X!<BR>\n");
    exit(1);
  }
  print("�ǥ� $Input{stu_id}($student{name}) �[ñ��� $Input{course_id}, �Z�O $Input{course_group}<BR>\n");
  if($student{name} eq "") {
    print("<FONT color=RED>ĵ�i</FONT>! �䤣��ǥͪ����y���!!<BR>\n");
  }
  $result = Add_Immune_Record($Input{course_id},
                              $Input{course_group}, $Input{stu_id});
  if($result eq "TRUE") {
    print("��Ƥw�s�J.<BR>\n");
  }elsif($result eq "FALSE") {
    print("�ӥ͸�Ʀ��w�s�b, ��ƥ��s�J!<BR>\n");
  }else{
    print("�������~, �Ь��t�ε{���޲z��!!\n");
    exit(0);
  }
}elsif( $Input{action} eq "delete" ) {
  ($course_id, $course_group, $stu_id) = split(/_/, $Input{del_param});
  Delete_Immune_Record($course_id, $course_group, $stu_id);
}


