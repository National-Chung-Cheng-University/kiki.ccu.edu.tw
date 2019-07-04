#!/usr/local/bin/perl
print "Content-type: text/plain","\n\n";

require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Dept.pm";

Read_All_Student_Data();

@dept = Find_All_Dept();

printf("%10s  %10s  %10s %2d\n", "學號", "姓名", "系所", "學分");
foreach $dept (@dept) {
  %dept = Read_Dept($dept);
  @student = Find_All_Student_In_Dept($dept);
  foreach $student (@student) {
    @course = Course_of_Student($student);
    $credit = 0;
    foreach $course (@course) {
      $credit += $$course{credit};
    }
    if($student ne "") {
      printf("%10s  %10s  %10s %2d\n", $student, $$S{$student}{name},
            $dept{cname2},$credit);
    }
  }
  
}
