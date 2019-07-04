#!/usr/local/bin/perl
#################################################################
#####  Find_All_Course.cgi
#####  查詢所有科目中文名稱
#####  因教學組列印用, 此程式產生虛擬txt檔可供word列印.
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

