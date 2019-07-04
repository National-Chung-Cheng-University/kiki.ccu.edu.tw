#!/usr/local/bin/perl
###########################################################################
#####   Transfer_Course3.cgi
#####   轉必修/必選課
#####   幫某系級班的學生全部選修某科目班別
#####   Coder: Nidalap
#####   Date : Jun,03,1999
###########################################################################
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Course.pm";
print("Content-type:text/html\n\n");

%Input = User_Input();
%dept = Read_Dept($Input{dept});
%stu_dept = Read_Dept($Input{stu_dept});
@property = ("", "必修", "選修", "通識");
($course_id, $course_group) = split(/_/, $Input{course});
%course = Read_Course($dept{id}, $course_id, $course_group, "");

print << "TABLE_1"
 <HEAD><TITLE>必修/必選課轉檔</TITLE></HEAD>
   <BODY background="$GRAPH_URL./ccu-sbg.jpg"><CENTER>
     <H1>必修/必選課轉檔<br>轉檔結果<hr></H1>
TABLE_1
;

@student = Find_All_Student_In_Dept($Input{stu_dept});
Check_For_Any_Time_Collision();
Print_Course_Table();
Print_Student_Table();
#############################################################################
sub Check_For_Any_Time_Collision()
{
  my(@course_of_student, %cos, $collision_flag, $stu_for_test);
  my $i = 10;

  foreach $student (@student) {
    %student = Read_Student($student);
    if(($student{grade} eq $Input{stu_grade})and($student{class} eq $Input{stu_class}) ) {
      $i--;
      if($i == 0) {    ## 略過前 $i 個(避開休學生影響判斷)
        $stu_for_test = $student;
        last;
      }
    }
  }
  @course_of_student = Course_of_Student($stu_for_test);
  
  foreach $cos (@course_of_student) {
    %cos = Read_Course($$cos{dept}, $$cos{id}, $$cos{group}, "", "");
#    print("cos[id, group] = [$cos{id}, $cos{group}<BR>\n");
    foreach $time (@{$cos{time}}) {
      foreach $time2 (@{$course{time}}) {
#        print("Checking collsion:
#           [$$time{week}, $$time{time}] <-> [$$time2{week}, $$time2{time}]<BR>\n");
        $collision_flag = is_Time_Collision($$time{week}, $$time{time}, 
                          $$time2{week}, $$time2{time});
        if($collision_flag != 0) {
          print("與科目 $cos{id}_$cos{group} 有衝堂情形! 轉檔中斷!!<BR>\n");
          print("student for test = $stu_for_test<BR>");
          exit();
        }
      }
    }
  }

  print("科目衝堂檢核無誤!<BR>");
}
#############################################################################
sub Print_Student_Table()
{
  print("<TABLE border=1>");  
  print("  <TR><TD>姓名</TD><TD>學號</TD><TD>姓名</TD><TD>學號</TD>\n");
  print("      <TD>姓名</TD><TD>學號</TD><TD>姓名</TD><TD>學號</TD>\n");
  print("      <TD>姓名</TD><TD>學號</TD></TR>\n");
  $lc = 0;
  foreach $student (@student) {
    %student = Read_Student($student);
    if(($student{grade} eq $Input{stu_grade})and($student{class} eq $Input{stu_class}) ) {
      Add_Student_Course($student , $Input{dept}, $course_id, $course_group, $Input{property});
#      print("$student , $Input{dept}, $course_id, $course_group, $Input{property}<br>");
      if($lc%5 == 0) {
        print qq(</tr><tr><td>$student{name}</td><td>$student{id}</td>\n);
      }elsif($lc%5 == 4) {
        print qq(<td>$student{name}</td><td>$student{id}</td></tr>\n);
      }else{
        print qq(<td>$student{name}</td><td>$student{id}</td>\n);
      }
      $lc++;
    }
  }
  print("</TABLE>");
}
#############################################################################
sub Print_Course_Table() 
{
  print qq(
    <TABLE border=0>
      <TR><TD valign=top>
        <TABLE border=1 valign=top>
          <TR><TD colspan=2 bgcolor=YELLOW aling=center>科目資料</TD></TR>
          <TR><TD>所屬系所</TD><TD>$dept{cname}</TD></TR>
          <TR><TD>科目代碼</TD><TD>$course{id}</TD></TR>
          <TR><TD>科目班別</TD><TD>$course{group}</TD></TR>
          <TR><TD>科目中文名稱</TD><TD>$course{cname}</TD></TR>
          <TR><TD>限修人數</TD><TD>$course{number_limit}</TD></TR>
          <TR><TD>開課屬性</TD><TD>$property[$course{property}]</TD></TR>
        </TABLE>
      </TD><TD valign=top>
        <TABLE border=1>
          <TR><TD colspan=2 bgcolor=YELLOW aling=center>學生資料</TD></TR>
          <TR><TD>所屬系所</TD><TD>$stu_dept{cname}</TD></TR>
          <TR><TD>年級</TD><TD>$Input{grade}</TD></TR>
          <TR><TD>班級</TD><TD>$Input{stu_class}</TD></TR>
          <TR><TD>選課屬性</TD><TD>$property[$Input{property}]</TD></TR>
        </TABLE>
      </TR>
    </TABLE>
  );
}
############################################################################
