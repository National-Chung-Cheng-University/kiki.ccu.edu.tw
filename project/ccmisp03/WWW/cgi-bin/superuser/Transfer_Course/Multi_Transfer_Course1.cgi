#!/usr/local/bin/perl

###########################################################################
#####   Multi_Transfer_Course1.cgi
#####   �h��h�ॲ��/�����
#####   ���ͺ���, ��ܨt�ҤΦ~��
#####   Coder: Nidalap
#####   Date : 09/04/2001
###########################################################################
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student.pm";

print("Content-type:text/html\n\n");

@dept = Find_All_Dept();
print << "TABLE_1"
  <HEAD><TITLE>�h��h����/���������</TITLE></HEAD>
  <BODY background="$GRAPH_URL./ccu-sbg.jpg">
    <CENTER>
      <H1>�h��h����/���������<br>
      �п�����ɬ�ةҦb�t�ҤΦ~��<hr></H1>
      <FORM action="Multi_Transfer_Course2.cgi" method="POST">
        <TABLE border=0>
          <TR>
            <TD><SELECT name="dept">
TABLE_1
;
foreach $dept (@dept) {
  %dept = Read_Dept($dept);
  print("<OPTION value=$dept>$dept{cname}\n");
}
print("</SELECT></td>");
print << "GRADE_SELECT"
  <td><SELECT name="grade">
        <OPTION value="1">�@�~��
        <OPTION value="2">�G�~��
        <OPTION value="3">�T�~��
        <OPTION value="4">�|�~��
      </SELECT>
  </td></tr>
GRADE_SELECT
;
print << "END_OF_HTML"
        </TABLE>
      <INPUT type=submit value="�惡�t�Ŭ������">
    </FORM>
   </CENTER>
 </BODY>
END_OF_HTML
