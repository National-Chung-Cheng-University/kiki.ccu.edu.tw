#!/usr/local/bin/perl

###########################################################################
#####   Batch_Delete_Student_Course4.cgi
#####   批次退選--確實對資料做動作
#####   Coder: Nidalap
#####   Date : Oct,19,1999
###########################################################################
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Course.pm";

print("Content-type:text/html\n\n");

%Input = User_Input();
%course = Read_Course($Input{course_dept}, $Input{course_id}, $Input{course_group});
%dept = Read_Dept($Input{student_dept});
@student = split(/,/,$Input{student});
print qq(
  <HEAD><TITLE>批次退選</TITLE></HEAD>
  <BODY background="$GRAPH_URL./ccu-sbg.jpg">
    <CENTER>
      <H1>批次退選<hr></H1>
      要退選的科目: [$Input{course_id} _ $Input{course_group}]$course{cname}<br>
      要退選的學生系所: $dept{cname}<br>
      要退選的學生年級: $Input{grade}<br>
      要退選的學生班級: $Input{class}<br>
      符合此身份的學生名單:<br>
      <TABLE border=1><TR>
);
$i=0;
foreach $student (@student) {
  Delete_Student_Course($student,$Input{course_dept},$Input{course_id},$Input{course_group});
  %student = Read_Student($student);
  print("</TR>") if($i == 6);
  print("<TR>")  if($i == 0);
  print("<TD><font color=555555 size=2>$student,$student{name}</font></TD>");
  $i++;
  $i=0  if($i==6);
}
print("</TR></TABLE>");

print("<Font color=RED size=4>退選完成!</FONT>");
