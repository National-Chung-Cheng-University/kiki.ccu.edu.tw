#!/usr/local/bin/perl
#################################################################
#####  Find_All_Course2.cgi
#####  查詢所有科目中文名稱
#####  從 Find_All_Course.cgi 修改而來
#####  產生開課明細資料, 供學期末成績核對用(?)
#####  Coder: Nidalap 
#####  Date :2005/02/18
#################################################################

require "../../../LIB/Reference.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Student_Course.pm";
require $LIBRARY_PATH . "Course.pm";
require $LIBRARY_PATH . "Teacher.pm";

print("Content_type:text/plain\n\n");
Read_Teacher_File();

print("當學期開課明細表: $YEAR 學年度第 $TERM 學期\n");
print("-------------------------------------------\n");
print("開課系所\t開課編碼\t班別\t科目名稱\t修課人數\t任課教師\n");
@dept = Find_All_Dept();
foreach $dept (@dept) {
  %dept = Read_Dept($dept);
#  next if( $dept ne "1104");
  for($grade = 1 .. 4) {
    @course = Find_All_Course($dept, $grade);
    foreach $course (@course) {
      %course = Read_Course($dept, $$course{id}, $$course{group});
      $count = Student_in_Course($dept, $course{id}, $course{group});
      $teacher_string = Format_Teacher_String(@{$course{teacher}});
      print("$dept{cname}\t$course{id}\t$course{group}\t$course{cname}\t$count\t$teacher_string\n");
    }
  }
}

