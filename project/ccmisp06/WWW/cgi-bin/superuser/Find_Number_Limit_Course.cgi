#!/usr/local/bin/perl
#################################################################
#####  Find_All_Course.cgi
#####  查詢所有科目中文名稱
#####  因教學組列印用, 此程式產生虛擬txt檔可供word列印.
#####  Coder: Nidalap 
#####  Date : May 10,2000
#################################################################

require "../../../LIB/Reference.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Course.pm";
require $LIBRARY_PATH . "Classroom.pm";
require $LIBRARY_PATH . "Teacher.pm";

print("Content_type:text/plain\n\n");

Read_Teacher_File();

#foreach $t (keys %Teacher_Name) {
#  print("$t -> $Teacher_Name{$t}<br>\n");
#}
@dept = Find_All_Dept();
foreach $dept (@dept) {
  %dept = Read_Dept($dept);
  for($grade = 1 .. 4) {
    @course = Find_All_Course($dept, $grade);
    foreach $course (@course) {
      %course = Read_Course($dept, $$course{id}, $$course{group});
      if( $course{number_limit} != 0 ) {
        $course{note} =~ s/\n/ /g;
        $teacher_string = "";
        $i=0;
        while( $course{teacher}[$i] ne "" ) {
          $teacher_string = $teacher_string . $Teacher_Name{$course{teacher}[$i]} . " ";
          $i++;
        }
        %classroom = Read_Classroom($course{classroom});
        $time_string = Format_Time($course{time});

        printf("%-30s  %-8s  %-2s  %-60s  %-20s  %-10s  %-30s  %-20s  %-120s\n",
                $dept{cname}, $course{id}, $course{group}, $course{cname}, $time_string,
                $course{number_limit}, $teacher_string, $classroom{cname}, $course{note}
        );
#        print("$dept{cname}\t\t\t$course{id}\t\t\t$course{group}\t\t\t$course{cname}\t\t\t$course\n");
      }
    }
  }
}

#########################################################################
sub Format_Time()
{
  my($rtime) = @_;
  my $time_string = "";
  my $last_day = "";
  my @week = ("", "一", "二", "三", "四", "五", "六", "日");
  my @time = ("A","1","2","3","4","B","5","6","7","8","C","D","E");
  foreach $ele ( @{$rtime} ) {
    if( $$ele{week} ne $last_day ) {
       $time_string .= $week[$$ele{week}];
    }
    $time_string .= $time[$$ele{time}];
    $last_day = $$ele{week};
  }

  return($time_string);
}
############################################################################
