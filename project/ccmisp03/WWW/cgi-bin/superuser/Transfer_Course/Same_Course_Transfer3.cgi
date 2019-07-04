#!/usr/local/bin/perl

###########################################################################
#####   Same_Course_Transfer3.cgi
#####   �W�U�Ǵ���Z�妸�[��
#####   ���ͺ���, �T�{�Ҧ��n�[�諸�ǥͦW��ά��
#####   Coder: Nidalap :D~
#####   Date : 2004/12/22
#####   ��ӵo�{���\�ভ�b Batch_Add_Student_Course ���F XD~
###########################################################################
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Course.pm";

print("Content-type:text/html\n\n");

%Input = User_Input();

($course_id_this, $course_group_this) = split(/_/, $Input{course_id_this});
($course_id_last, $course_group_last) = split(/_/, $Input{course_id_last});

%course_this = Read_Course($Input{dept}, $course_id_this, $course_group_this);
%course_this = Read_Course($Input{dept}, $course_id_last, $course_group_last, "HISTORY");  

@student = Student_in_Course($Input{student_dept}, $course_id, $course_group);
print qq(
  <HEAD><TITLE>�妸�h��</TITLE></HEAD>
  <BODY background="$GRAPH_URL./ccu-sbg.jpg">
    <CENTER>
      <H1>�妸�h��<hr></H1>
      �n�h�諸���: [$course_id _ $course_group]$course{cname}<br>
      �n�h�諸�ǥͨt��: $dept{cname}<br>
      �n�h�諸�ǥͦ~��: $Input{grade}<br>
      �n�h�諸�ǥͯZ��: $Input{class}<br>
      �ŦX���������ǥͦW��:<br>
      <TABLE border=1><TR>
);
$i = 0;
$student_string = "";
$student_count = 0;
foreach $student (@student) {
  %student = Read_Student($student);
  print("</TR>") if($i == 6);
  print("<tr>")  if($i == 0);
  if( ($student{dept} eq $Input{student_dept}) or ($Input{student_dept} eq "all") ) {
    if( ($student{grade} eq $Input{grade}) and
        ($student{class} eq $Input{class})     ) {
      $student_count ++;
      print("<TD><font size=2 color=555555>$student{id}, $student{name}</font></TD>");
      if($student_string eq "") {
        $student_string = $student_string . $student{id};
      }else{
        $student_string = $student_string . "," . $student{id};
      }
    }
  }
  $i++;  
  if($i==6) { $i=0; }
#  print("$student{id}, $student{name}<br>\n");
}
print("</TR></TABLE>");
print("�@ $student_count �W�ǥ�<BR>\n");
#print("string = $student_string<br>\n");
print qq(
  <FORM action=Batch_Delete_Student_Course4.cgi method=POST>
    <INPUT type=hidden name=student value=$student_string>
    <INPUT type=hidden name=student_dept value=$Input{student_dept}>
    <INPUT type=hidden name=grade value=$Input{grade}>
    <INPUT type=hidden name=class value=$Input{class}>
    <INPUT type=hidden name=course_id value=$course_id>
    <INPUT type=hidden name=course_dept value=$Input{course_dept}>
    <INPUT type=hidden name=course_group value=$course_group>
    <INPUT type=submit value="�T�w�h��">
  </FORM>
);


