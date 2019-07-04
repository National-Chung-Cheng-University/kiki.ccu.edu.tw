#!/usr/local/bin/perl
##########################################################################
#####   Open_Course_Restriction_Immune02.cgi
#####   �}���ˮְj�ץ[ñ page #2
#####   
#####   Coder: Nidalap
#####   Date : 04/16/2002
##########################################################################
print("Content-type:text/html\n\n");
require "../../library/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Open_Course.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Course.pm";
require $LIBRARY_PATH . "Password.pm";
require $LIBRARY_PATH . "Error_Message.pm";
#require "./Open_Course_Restriction_Immune.pm";

%Input   = User_Input();

$pass_result = Check_SU_Password($Input{password}, "su", "su");
if($pass_result ne "TRUE") {
  print("�K�X���~!");
  exit(1);
}

print qq(
  <HTML>
    <HEAD><TITLE>�}���ˮְj�ץ[ñ</TITLE></HEAD>
    <BODY background="$GRAPH_URL./manager.jpg">
      <Center><H1>�}���ˮְj�ץ[ñ<hr></h1>
);

if( $Input{action} eq "add" ) {
  if( ($Input{course_id} eq "") or ($Input{course_group} eq "")) {
    print("��J��Ƥ�����!!<BR>\n");
    exit(1);
  }
  if( length($Input{course_id}) != 7 ) {
    print("���~: ��إN���ݬ� 7 �X!<BR>\n");
    exit(1);
  }
  if( ($Input{r1} != "1") and ($Input{r2} != "1") and
      ($Input{r3} != "1") and ($Input{r4} != "1") )   {
    print("�S���Ŀ����j�׳W�h, �Ц^�W���T�{!<BR>\n");
    exit(1);
  }

  $result = Add_Immune_Record($Input{course_id}, $Input{course_group},
            $Input{r1}, $Input{r2}, $Input{r3}, $Input{r4});
  if($result eq "TRUE") {
    print qq(
      <TABLE border=1>
        <TR>
          <TD>��إN�X</TD>
          <TD>�Z�O</TD>
          <TD>�s��T�p��</TD>
          <TD>��Ϭq</TD>
          <TD>�@�T��/�G�|</TD>
          <TD>��ѫh�P�I��</TD>
        </TR>
        <TR>
          <TD>$Input{course_id}</TD>
          <TD>$Input{course_group}</TD>
          <TD>$Input{r1}</TD>
          <TD>$Input{r2}</TD>
          <TD>$Input{r3}</TD>
          <TD>$Input{r4}</TD>
        </TR>
      </TABLE>
    );
    print("��Ƥw�s�J.<BR>\n");
  }elsif($result eq "FALSE") {
    print("�Ӹ�Ʀ��w�s�b, ��ƥ��s�J!<BR>\n");
  }else{
    print("�������~, �Ь��t�ε{���޲z��!!\n");
    exit(0);
  }
}elsif( $Input{action} eq "delete" ) {
  ($course_id, $course_group) = split(/_/, $Input{del_param});
  Delete_Immune_Record($course_id, $course_group);
}


