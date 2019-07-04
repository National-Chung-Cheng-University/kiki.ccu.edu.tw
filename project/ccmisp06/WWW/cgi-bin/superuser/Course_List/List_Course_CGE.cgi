#!/usr/local/bin/perl
#################################################################
#####  List_Course_CGE.cgi
#####  查詢所有通識科目資料
#####  因韋岷的期末問卷系統列印用, 此程式列出所有通識課程的以下欄位：
#####    [代碼、班別、名稱、系所、教師姓名、學分、修課人數]
#####  Coder: Nidalap  :D~
#####  Date : 2015/12/16
#################################################################

require "../../library/Reference.pm";
require $LIBRARY_PATH . "Common_Utility.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Course.pm";
require $LIBRARY_PATH . "Classroom.pm";
require $LIBRARY_PATH . "Teacher.pm";
require $LIBRARY_PATH . "Student_Course.pm";

print("Content-type:text/html\n\n");
print("<HTML><HEAD>$EXPIRE_META_TAG</HEAD>");

%Input = User_Input();
if($Input{last_semester} eq "1") {
  ($year, $term) = Last_Semester(1);
}else{
  ($year, $term) = ($YEAR, $TERM);
}

Read_Teacher_File();

#foreach $t (keys %Teacher_Name) {
#  print("$t -> $Teacher_Name{$t}<br>\n");
#}
#@dept = Find_All_Dept();
@dept = ("I001");
#@pro = ("", "必修", "選修", "通識");
@pro = @PROPERTY_TABLE;
 
print ("以下是 $year 學年度第 $term 學期的通識課程清單:<P>\n");
printf ("%-8s  %-4s  %-60s  %-30s  %-20s  %-4s  %-3s<BR>\n",
         "代碼", "班別", "名稱", "系所", "教師姓名", "學分", "修課人數");
foreach $dept (@dept) {
  %dept = Read_Dept($dept);
  for($grade = 1 .. 4) {
    @course = Find_All_Course($dept, $grade, $year, $term);
    foreach $course (@course) {
      %course = Read_Course($dept, $$course{id}, $$course{group}, $year, $term);
      next if( ($course{number_limit}==0) and ($number_limit_flag==1) );
      $course{note} =~ s/\n/ /g;
      $teacher_string = "";
      $i=0;
      while( $course{teacher}[$i] ne "" ) {
        $teacher_string = $teacher_string . $Teacher_Name{$course{teacher}[$i]} . " ";
        $i++;
      }
      %classroom = Read_Classroom($course{classroom});
      $time_string = Format_Time_String($course{time});
	  
	  @stu_in_course = Student_in_Course($dept, $course{id}, $course{group}, $year, $term);
	  $stu_count = @stu_in_course;
	  
	  printf ("%-8s  %-4s  %-60s  %-30s  %-20s  %-4s  %-3s<BR>\n",
         $course{id}, $course{group}, $course{cname}, $dept{cname},  $teacher_string, $course{credit}, $stu_count);
	   
#      print("$dept{cname}\t\t\t$course{id}\t\t\t$course{group}\t\t\t$course{cname}\t\t\t$course\n");
    }
  }
}

#########################################################################
