#!/usr/local/bin/perl

###########################################################################
#####   Batch_Delete_Student_Course2.cgi
#####   �妸�h��
#####   ���ͺ���, ��ܭn�h�諸���
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
  <HEAD><TITLE>�妸�h��</TITLE></HEAD>
   <BODY background="$GRAPH_URL./ccu-sbg.jpg">
   <CENTER><H1>�妸�h��<br>�п�ܬ��<hr></H1>
    <FORM action="Batch_Delete_Student_Course3.cgi" method=POST>
      <TABLE border=0>
        <TR><TD>
);
print qq(<INPUT type="hidden" name=course_dept value="$Input{course_dept}">);
print qq(�п�ܭn�h�諸���:<SELECT name="course_id">);
foreach $course (@Course) {
  %course = Read_Course($Input{course_dept},$$course{id},$$course{group});
  print qq(<OPTION value="$$course{id}_$$course{group}">[$$course{id}_$$course{group}]$course{cname});
}
print ("</SELECT></TD></TR>");
print qq(
  <TR><TD>�п�ܾǥͨt�ҧO:<SELECT name="student_dept">
      <OPTION value=all> -- �����t�� --
);
foreach $dept (@dept) {
  %dept = Read_Dept($dept);
  print qq(<OPTION value=$dept>$dept{cname});
}
print ("</SELECT></TD></TR>");
print qq (<TR><TD>�п�ܾǥͦ~�ŧO:<SELECT name="grade">);
foreach $grade (@grade) {
  print qq(<OPTION value=$grade>$grade);
}
print ("</SELECT></TD></TR>");
print qq (<TR><TD>�п�ܾǥͯZ�O:<SELECT name="class">);
foreach $class (@class) {
  print qq(<OPTION value=$class>$class);
}
print ("</SELECT></TD></TR>");    

print qq(
  </TABLE>
  <INPUT type="submit" value="�i�J�T�{�e��">
  </FORM>
);