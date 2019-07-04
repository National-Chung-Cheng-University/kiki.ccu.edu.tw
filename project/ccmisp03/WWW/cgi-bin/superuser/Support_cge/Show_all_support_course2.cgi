#!/usr/local/bin/perl

#################################################################
#####  Show_all_support_course2.cgi
#####  �䴩�q�Ѭ�ؤ@���� -- ��X�Ҧ����䴩�q�Ѫ����
#####  Coder: Nidalap
#####  Date : Nov17, 2000
#################################################################
print("Content-type: text/html\n\n");
require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Error_Message.pm";

my(%Input,%Student,%Dept);
@dept = Find_All_Dept();
%Input=User_Input();
%cge = Read_Cge();

print qq(
  <HTML>
    <HEAD><TITLE>�䴩�q�Ѭ�ؤ@����</TITLE></HEAD>
      <BODY background="$GRAPH_URL/bk.jpg">
        <CENTER>
        <H1>�䴩�q�Ѭ�ؤ@����</H1><HR>
        <TABLE border=1>
          <TR bgcolor=YELLOW><TH>�}�Ҩt��</TH><TH>��إN�X</TH><TH>�Z�O</TH><TH>��ئW��</TH><TH>�䴩���O</TH><TH>�䴩�H��</TH></TR>
);
foreach $dept (sort @dept) {
  @course = Find_All_Course($dept);
  foreach $course (@course) {
    %course = Read_Course($dept, $$course{id}, $$course{group}, "", "");
    %dept = Read_Dept($dept);
    if( ($course{support_cge_type} ne "0")or($dept eq "7006") ) {
      if($course{dept} eq "7006") {
        $course{id} =~ /^(....)/;
        $course{support_cge_type} = $1;
      }
                   
      print qq(
        <TR>
          <TD>$dept{cname2}</TD>
          <TD>$$course{id}</TD>
          <TD>$$course{group}</TD>
          <TD>$course{cname}</TD>
          <TD>$course{support_cge_type}</TD>
          <TD>$course{support_cge_number}</TD>\n
        </TR>
      );
    }
  }
}
print("</TABLE>");
 