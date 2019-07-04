#!/usr/local/bin/perl
#################################################################
#####  Find_All_Course.cgi
#####  �d�ߩҦ���ؤ���W��
#####  �]�оǲզC�L��, ���{�����͵���txt�ɥi��word�C�L.
#####  Coder: Nidalap 
#####  Date : Aug 05, 1999
#################################################################

require "../../../LIB/Reference.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Course.pm";

print("Content_type:text/plain\n\n");

@dept = Find_All_Dept();
foreach $dept (@dept) {
  %dept = Read_Dept($dept);
  for($grade = 1 .. 4) {
    @course = Find_All_Course($dept, $grade);
    foreach $course (@course) {
      %course = Read_Course($dept, $$course{id}, $$course{group});
      print("$dept{cname}\t\t\t$course{cname}\n");
    }
  }
}

