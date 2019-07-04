#!/usr/local/bin/perl

###########################################################################
#####   Batch_Delete_Student_Course2.cgi
#####   批次退選
#####   產生網頁, 選擇要退選的科目
#####   Coder: Nidalap
#####   Date : Oct,18,1999
###########################################################################
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Course.pm";
@grade = (1,2,3,4);
@class = (A,B,C,D,E,F,G,H);

print("Content-type:text/html\n\n");

%Input = User_Input();
@dept = Find_All_Dept();
@Course = Find_All_Course($Input{course_dept});

print qq(
  <HEAD>
    $EXPIRE_META_TAG
    <TITLE>批次退選</TITLE>
  </HEAD>  
   <BODY background="$GRAPH_URL./ccu-sbg.jpg">
   <CENTER><H1>批次退選<br>請選擇科目<hr></H1>
    <FORM action="Batch_Delete_Student_Course3.cgi" method=POST>
      <TABLE border=0>
        <TR><TD>
);
print qq(<INPUT type="hidden" name=course_dept value="$Input{course_dept}">);
print qq(請選擇要退選的科目:<SELECT name="course_id">);
foreach $course (@Course) {
  %course = Read_Course($Input{course_dept},$$course{id},$$course{group});
  print qq(<OPTION value="$$course{id}_$$course{group}">[$$course{id}_$$course{group}]$course{cname});
}
print ("</SELECT></TD></TR>");
print qq(
  <TR><TD>請選擇學生系所別:<SELECT name="student_dept">
      <OPTION value=all> -- 全部系所 --
);
foreach $dept (@dept) {
  %dept = Read_Dept($dept);
  print qq(<OPTION value=$dept>$dept{cname});
}
print ("</SELECT></TD></TR>");
print qq (
  <TR><TD>請選擇學生年級別:<SELECT name="grade">
      <OPTION value=all> -- 全部年級 --
);

foreach $grade (@grade) {
  print qq(<OPTION value=$grade>$grade);
}
print ("</SELECT></TD></TR>");
print qq (
  <TR><TD>請選擇學生班別:<SELECT name="class">
      < <OPTION value=all> -- 全部班級 --
);
foreach $class (@class) {
  print qq(<OPTION value=$class>$class);
}
print ("</SELECT></TD></TR>");    

print qq(
  </TABLE>
  <INPUT type="submit" value="進入確認畫面">
  </FORM>
);