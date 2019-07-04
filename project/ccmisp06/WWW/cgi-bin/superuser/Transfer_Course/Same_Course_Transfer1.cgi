#!/usr/local/bin/perl

###########################################################################
#####   Same_Course_Transfer1.cgi
#####   上下學期原班批次加選
#####   產生網頁, 選擇系所及年級
#####   Coder: Nidalap
#####   Date : 2004/12/22
#####   後來發現本功能早在 Batch_Add_Student_Course 做了 XD~
###########################################################################
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student.pm";

print("Content-type:text/html\n\n");

@dept = Find_All_Dept();
print << "TABLE_1"
  <HEAD>
    $EXPIRE_META_TAG
    <TITLE>上下學期原班批次加選</TITLE>
  </HEAD>
  <BODY background="$GRAPH_URL./ccu-sbg.jpg">
    <CENTER>
      <H1>上下學期原班批次加選<br>
      請選擇原班科目所在系所及年級<hr></H1>
      <FORM action="Same_Course_Transfer2.cgi" method="POST">
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

