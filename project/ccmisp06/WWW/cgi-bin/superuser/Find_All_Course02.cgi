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
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Student_Course.pm";
require $LIBRARY_PATH . "Course.pm";
require $LIBRARY_PATH . "Teacher.pm";
require $LIBRARY_PATH . "Common_Utility.pm";
require $LIBRARY_PATH . "System_Settings.pm";

%Input=User_Input();

print("Content-type:text/html\n\n");
print("<HTML><meta http-equiv='Content-Type' content='text/html; charset=utf-8'>");
print("<PRE>");
Read_Teacher_File();
($year, $term) = Last_Semester($Input{last_semester});

print("當學期開課明細表: $year 學年度第 $term 學期\n");
print("-------------------------------------------\n");
print("開課系所\t開課編碼\t班別\t科目名稱\t學分數\t修課人數\t任課教師\n");
@dept = Find_All_Dept();
foreach $dept (@dept) {
  %dept = Read_Dept($dept);
#  next if( $dept ne "1104");
  for($grade = 1 .. 4) {
    @course = Find_All_Course($dept, $grade, $year, $term);
    foreach $course (@course) {
      %course = Read_Course($dept, $$course{id}, $$course{group}, $year, $term);

      $teacher_missing_count=0;
      if( $Input{"teacher_missing"} ) {
        foreach $teacher (@{$course{teacher}}) {
          $teacher_missing_count++  if($Teacher_Name{$teacher} eq "");
        }
      }
      
      $count = Student_in_Course($dept, $course{id}, $course{group}, $year, $term);
      $teacher_string = Format_Teacher_String(@{$course{teacher}});
      
#      print("$course{id}: $teacher_missing_count\n");
      if( $Input{"teacher_missing"} and ($teacher_missing_count == 0) ) {
        next;
      }
      print("$dept{cname}\t$course{id}\t$course{group}\t$course{cname}\t$course{credit}\t$count\t$teacher_string\n");
    }
  }
}

