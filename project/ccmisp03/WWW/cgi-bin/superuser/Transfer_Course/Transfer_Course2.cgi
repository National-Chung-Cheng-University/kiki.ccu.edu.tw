#!/usr/local/bin/perl

###########################################################################
#####   Transfer_Course2.cgi
#####   �ॲ��/�����
#####   ��ܬY�t�Ŷ}����, ���ϥΪ̿������@���Ҩ���@�t�ůZ���ǥ�
#####   Coder: Nidalap
#####   Date : Jun,03,1999
###########################################################################
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Course.pm";
print("Content-type:text/html\n\n");

%Input = User_Input();
@dept = Find_All_Dept();
@course = Find_All_Course($Input{dept}, $Input{grade}, "");
print << "TABLE_1"
 <HEAD><TITLE>����/���������</TITLE></HEAD>
   <BODY background="$GRAPH_URL./ccu-sbg.jpg"><CENTER>
     <H1>����/���������<br>�п�����ɬ�ؤξǥͨt��,�~�ŤίZ�O<hr></H1>
     <FORM action="Transfer_Course3.cgi" method="POST">
       <INPUT type="hidden" name="dept" value=$Input{dept}>
       <INPUT type="hidden" name="grade" value=$Input{grade}>
       <TABLE border=1>
         <TR><TD align=center bgcolor=yellow>�п�����ɬ��</TD>
         <TD bgcolor=yellow>�п�����ɾǥͨt�ůZ</TD></TR>
         <TR><TD><SELECT name="course" size=15>
TABLE_1
;
foreach $course (@course) {
  %course = Read_Course($Input{dept}, $$course{id}, $$course{group}, "");
  print qq(<OPTION value="$$course{id}_$$course{group}">$course{id}_$course{group} $course{cname});
}
print qq(</SELECT></TD><TD valign=top><SELECT name="stu_dept" size=10>);
foreach $dept (@dept) {
  %dept = Read_Dept($dept);
  print qq(<OPTION value="$dept">$dept{cname});
}
print qq(</SELECT><br>
  �~��: <SELECT name="stu_grade">
    <OPTION value="1">�@�~�� <OPTION value="2">�G�~��
    <OPTION value="3">�T�~�� <OPTION value="4">�|�~��
  </SELECT><br>
  �Z��: <SELECT name="stu_class">
);
@temp = (A..E);
foreach $i (@temp) {
  print qq(<OPTION value="$i">$i);
}
print("</SELECT><br>");
print qq(
  �׽��ݩ�: <SELECT name="property">
    <OPTION value="1" selected>����
    <OPTION value="2">���
    <OPTION value="3">�q��
  </SELECT>
);
print("</TABLE>");

print << "END_OF_HTML"
    <INPUT type=submit value="�T�w����">
  </FORM>
  ���{�����ˬd���ƿ��, �Y�w�g���ɹL��, �n�ק��ݩ�, �Х�����妸�h��A����<br>
END_OF_HTML

