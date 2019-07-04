#!/usr/local/bin/perl

###########################################################################
#####   Batch_Delete_Student_Course1.cgi
#####   批次退選
#####   產生網頁, 選擇科目系所及年級
#####   Coder: Nidalap
#####   Date : Jun,02,1999
###########################################################################
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student.pm";
@grade = (1,2,3,4);

print("Content-type:text/html\n\n");

@dept = Find_All_Dept();
print << "TABLE_1"
  <HEAD>
    $EXPIRE_META_TAG
    <TITLE>批次退選</TITLE>
  </HEAD>
  <BODY background="$GRAPH_URL./ccu-sbg.jpg">
    <CENTER>
      <H1>批次退選<br>請選擇科目所屬系所<hr></H1>
      <FORM action="Batch_Delete_Student_Course2.cgi" method="POST">
      <TABLE border=0>
        <TR>
          <TD>
            系所別:<SELECT name="course_dept">
TABLE_1
;

foreach $dept (@dept) {
  %dept = Read_Dept($dept);
  print qq(<OPTION value=$dept>$dept{cname});
}
print << "TABLE_2"
            
            </SELECT>
          </TD>
        </TR>
      </TABLE>
TABLE_2
;
print qq(<INPUT type="submit" value="挑選班級"></FORM>);


