#!/usr/local/bin/perl
#################################################################
#####  List_Course2.cgi
#####  �d�ߩҦ���ظ��
#####  �]�оǲզC�L��, ���{�����͵���txt�ɥi��word�C�L.
#####  Coder: Nidalap 
#####  Date : May 16,2000
#################################################################

require "../../library/Reference.pm";
require $LIBRARY_PATH . "Common_Utility.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Course.pm";
require $LIBRARY_PATH . "Classroom.pm";
require $LIBRARY_PATH . "Teacher.pm";

print("Content_type:text/plain\n\n");

%Input = User_Input();
$number_limit_flag=1  if($Input{number_limit} eq "on");

Read_Teacher_File();

#foreach $t (keys %Teacher_Name) {
#  print("$t -> $Teacher_Name{$t}<br>\n");
#}
@dept = Find_All_Dept();
@pro = ("", "����", "���", "�q��");

printf ("%-30s %-8s  %-4s  %-60s  %-60s  %-4s  %-4s  %-20s  %-4s  %-10s  %-30s  %-20s  %-120s\n",
         "�t��", "��إN�X", "�Z�O", "����W��", "�^��W��", "�Ǥ�", "�ݩ�",  "�ɶ�", "�ɼ�", "����",
         "�Юv", "�Ы�" );
foreach $dept (@dept) {
  %dept = Read_Dept($dept);
  for($grade = 1 .. 4) {
    @course = Find_All_Course($dept, $grade);
    foreach $course (@course) {
      %course = Read_Course($dept, $$course{id}, $$course{group});
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
      printf("%-30s  %-8s  %-4s  %-60s  %-60s  %-4s  %-4s  %-20s  %-4s  %-10s  %-30s  %-20s  %-120s\n",
              $dept{cname},  $course{id}, $course{group}, $course{cname},
              $course{ename}, $course{credit}, $pro[$course{property}], $time_string, $course{total_time},
              $course{number_limit}, $teacher_string, $classroom{cname}, 
              $course{note}
      );
#      print("$dept{cname}\t\t\t$course{id}\t\t\t$course{group}\t\t\t$course{cname}\t\t\t$course\n");
    }
  }
}

#########################################################################
