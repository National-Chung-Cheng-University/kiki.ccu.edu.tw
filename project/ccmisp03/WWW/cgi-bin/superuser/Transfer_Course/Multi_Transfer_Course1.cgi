#!/usr/local/bin/perl

###########################################################################
#####   Multi_Transfer_Course1.cgi
#####   多對多轉必修/必選課
#####   產生網頁, 選擇系所及年級
#####   Coder: Nidalap
#####   Date : 09/04/2001
###########################################################################
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student.pm";

print("Content-type:text/html\n\n");

@dept = Find_All_Dept();
print << "TABLE_1"
  <HEAD><TITLE>多對多必修/必選課轉檔</TITLE></HEAD>
  <BODY background="$GRAPH_URL./ccu-sbg.jpg">
    <CENTER>
      <H1>多對多必修/必選課轉檔<br>
      請選擇轉檔科目所在系所及年級<hr></H1>
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
        <OPTION value="1">一年級
        <OPTION value="2">二年級
        <OPTION value="3">三年級
        <OPTION value="4">四年級
      </SELECT>
  </td></tr>
GRADE_SELECT
;
print << "END_OF_HTML"
        </TABLE>
      <INPUT type=submit value="對此系級科目轉檔">
    </FORM>
   </CENTER>
 </BODY>
END_OF_HTML

