#!/usr/local/bin/perl

#################################################################
#####  Show_all_support_course2.cgi
#####  �����t��ؤ@���� -- ��X�Ҧ��������t�ײߪ����
#####  Coder: Nidalap
#####  Date : Nov22, 2000
#################################################################
print("Content-type: text/html\n\n");
require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Error_Message.pm";

my(%Input,%Student,%Dept);
@dept = Find_All_Dept();
%Input=User_Input();

print qq(
  <HTML>
    <HEAD><TITLE>�����t��ؤ@����</TITLE></HEAD>
      <BODY background = $GRAPH_URL/bk.jpg>
        <CENTER>
        <H1>�����t��ؤ@����</H1><HR>
        �C�X�Ҧ��׭רt��6�ӥH�W�����
        <TABLE border=1>
          <TR bgcolor=YELLOW><TH>�}�Ҩt��</TH><TH>��إN�X</TH><TH>�Z�O</TH><TH>��ئW��</TH><TH>���פH��</TH><TH>�׭רt��</TH></TR>
);
$dept_count = @dept;
foreach $dept (sort @dept) {
  @course = Find_All_Course($dept);
  %dept = Read_Dept($dept);
  foreach $course (@course) {
    %course = Read_Course($dept, $$course{id}, $$course{group}, "", "");
    $Ban_dept_count = @{$course{ban_dept}};
    if($Ban_dept_count > 6) {
      print qq(
        <TR>
          <TD>$dept{cname2}</TD>
          <TD>$$course{id}</TD>
          <TD>$$course{group}</TD>
          <TD>$course{cname}</TD>
          <TD>$course{number_limit}</TD>
          <TD>
      );
      if($Ban_dept_count > 10) {
        print("$Ban_dept_count��");
      }else{
        foreach $ban_dept (@{$course{ban_dept}}) {
          print("$ban_dept ");
        }
      }
      print("</TD></TR>");

    }
  }
}
print("</TABLE>");

 