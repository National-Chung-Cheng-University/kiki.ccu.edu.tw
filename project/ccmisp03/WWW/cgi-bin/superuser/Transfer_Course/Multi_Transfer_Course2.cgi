#!/usr/local/bin/perl

###########################################################################
#####   Transfer_Course2.cgi
#####   �h��h�ॲ��/�����
#####   �C�X���Өt�ůZ�����, �̷Ӷü���J���ӯZ�O.
#####   Coder: Nidalap
#####   Date : 09/04/2001
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
 <HEAD><TITLE>�h��h����/���������</TITLE></HEAD>
   <BODY background="$GRAPH_URL./ccu-sbg.jpg"><CENTER>
     <H1>�h��h����/���������<br>�п�����ɬ�ؤξǥͨt��,�~�ŤίZ�O<hr></H1>
     <FORM action="Multi_Transfer_Course3.cgi" method="POST">
       <INPUT type="hidden" name="dept" value=$Input{dept}>
       <INPUT type="hidden" name="grade" value=$Input{grade}>
       <TABLE border=1>
         <TR><TD align=center bgcolor=yellow>�п�����ɬ��(�ƿ�)</TD>
         <TD bgcolor=yellow>�п�����ɾǥͨt�ůZ(�ƿ�)</TD></TR>
         <TR><TD>
           ��إN�X�Z�O:<BR>
           <SELECT name="course" size=6 multiple>
               
TABLE_1
;
foreach $course (@course) {
  %course = Read_Course($Input{dept}, $$course{id}, $$course{group}, "");
  print qq(<OPTION value="$$course{id}_$$course{group}">$course{id}_$course{group} $course{cname});
}
print qq(
    </SELECT>
  </TD>
  <TD valign=top>
    <TABLE border=0>
      <TR>
        <TD><SELECT name="stu_dept" size=4 multiple>
);
foreach $dept (@dept) {
  %dept = Read_Dept($dept);
  print qq(<OPTION value="$dept">$dept{cname2});
}
print qq(
    </SELECT>
  </TD>
  <TD>
    <SELECT name="stu_grade" size=4 multiple>
      <OPTION value="1">�@�~�� <OPTION value="2">�G�~��
      <OPTION value="3">�T�~�� <OPTION value="4">�|�~��
    </SELECT>
  </TD>
  <TD>
    <SELECT name="stu_class" size=4 multiple>
);
@temp = (A..E);
foreach $i (@temp) {
  print qq(<OPTION value="$i">$i);
}
print qq(
        </SELECT>
      </TD>
    </TR>
  </TABLE>
);
print qq(
  �׽��ݩ�: <SELECT name="property">
    <OPTION value="1" selected>����
    <OPTION value="2">���
    <OPTION value="3">�q��
  </SELECT>
  <BR>
  �O�_����Ǹ�: <SELECT name="stu_id_filter">
    <OPTION value="1" selected>���]��
    <OPTION value="2">�u���_��
    <OPTION value="3">�u������
  </SELECT>
);
print("</TABLE>");

print << "END_OF_HTML"
    <INPUT type=submit value="�i�J�T�{���">
  </FORM>
  ���{�����ˬd���ƿ��, �Y�w�g���ɹL��, �n�ק��ݩ�, �Х�����妸�h��A����<br>
END_OF_HTML

