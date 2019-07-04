#!/usr/local/bin/perl
#######################################################################################
#####  Student_Course_list.cgi
#####  �ǥͩҦ���Ҹ�ƦC��
#####  �i�Φb���׬d�֦W���
#####  2003/06/25
#####  Nidalap :D~
#######################################################################################
print "Content-type: text/html","\n\n";

require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Dept.pm";

@student = Find_All_Student();
Read_All_Student_Data();

$stu_count = $count = 0;
print("<H1>$YEAR�Ǧ~�ײ�$TERM�Ǵ�$SUB_SYSTEM_NAME��Ҩt�ΩҦ��׽Ҹ�ƦC��:</H1><HR>\n");
foreach $student (sort @student) {
  @course = Course_of_Student($student);
  $course_count_temp = @course;
  $stu_count++  if( $course_count_temp > 0 );
  foreach $course (@course) {
    %dept = Read_Dept($$S{$student}{dept});
    %course = Read_Course($$course{dept}, $$course{id}, $$course{group}, "", "");
    print("$student\t$$S{$student}{dept}\t$dept{cname2}\t$$S{$student}{grade}\t$$S{$student}{name}\t$course{id}\t$course{group}\t$course{cname}<BR>");
    $count++;
  }
}
print("(�@ $stu_count �Ӿǥ�, $count ����Ҹ��)");
