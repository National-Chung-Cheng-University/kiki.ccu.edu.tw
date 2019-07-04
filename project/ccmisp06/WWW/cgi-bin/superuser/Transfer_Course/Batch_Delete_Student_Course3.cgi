#!/usr/local/bin/perl

###########################################################################
#####   Batch_Delete_Student_Course3.cgi
#####   批次退選
#####   產生網頁, 確認所有要退選的學生名單及科目
#####   Coder: Nidalap
#####   Date : Oct,18,1999
###########################################################################
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."System_Settings.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Course.pm";

print("Content-type:text/html\n\n");

%Input = User_Input();

($course_id, $course_group) = split(/_/, $Input{course_id});
%course = Read_Course($Input{course_dept}, $course_id, $course_group);

if( $Input{student_dept} eq "all" ) {
  $dept{cname} = "全部系所";
}else{
  %dept = Read_Dept($Input{student_dept});
}
if( $Input{grade} eq "all" ) {
  $grade_show = "全部年級";  
}else{  
  $grade_show = $Input{grade};
}
if( $Input{class} eq "all" ) {
  $class_show = "全部班級";  
}else{  
  $class_show = $Input{class};
}

@student = Student_in_Course($Input{student_dept}, $course_id, $course_group);
print qq(
  <HEAD>
    $EXPIRE_META_TAG
    <TITLE>批次退選</TITLE>
  </HEAD>  
  <BODY background="$GRAPH_URL./ccu-sbg.jpg">
    <CENTER>
      <H1>批次退選<hr></H1>
      要退選的科目: [$course_id _ $course_group]$course{cname}<br>
      要退選的學生系所: $dept{cname}<br>
      要退選的學生年級: $grade_show<br>
      要退選的學生班級: $class_show<br>
      符合此身份的學生名單:<br>
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
    if( ($student{grade} eq $Input{grade}) or ($Input{grade} eq "all") ) {
      if( ($student{class} eq $Input{class}) or ($Input{class} eq "all") )  {
        $student_count ++;
        print("<TD><font size=2 color=555555>$student{id}, $student{name}</font></TD>");
        if($student_string eq "") {
          $student_string = $student_string . $student{id};
        }else{
          $student_string = $student_string . "," . $student{id};
        }
      }
    }
  }
  $i++;  
  if($i==6) { $i=0; }
#  print("$student{id}, $student{name}<br>\n");
}
print("</TR></TABLE>");
print("共 $student_count 名學生<BR>\n");
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
    <INPUT type=submit value="確定退選">
  </FORM>
);


