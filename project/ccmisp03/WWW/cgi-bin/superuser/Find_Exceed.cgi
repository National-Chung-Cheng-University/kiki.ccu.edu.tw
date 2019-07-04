#!/usr/local/bin/perl
##########################################################################
#####     Find_Exceed.cgi
#####     找出所有選修人數超過 (科目限修人數 - 保留人數) 的名單
#####     本程式為救火程式, 因為此情況一般不會發生!
#####     Coder: Nidalap
#####     Date : Jul 01,1999
##########################################################################        
require "../../../LIB/Reference.pm";
require $LIBRARY_PATH . "Student_Course.pm";
require $LIBRARY_PATH . "Student.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Course.pm";
require $LIBRARY_PATH . "GetInput.pm";

%Input = User_Input();
$exceed_file = $TEMP_PATH . "exceed.txt";
$exceed_URL = $HOME_URL . "Temp/exceed.txt";
open(EXCEED, ">$exceed_file");

print("Content-type:text/html\n\n");
print qq(
  <BODY background="$GRAPH_URL/manager.jpg">
    <CENTER><H1>所有超修科目
    <hr></H1>
    <TABLE border=1>
    <TR bgcolor=YELLOW><TD>系別</TD><TD>科目代碼</TD><TD>科目班別</TD><TD>限修人數</TD><TD>保留人數</TD><TD>選修人數</TD><TD>需退選人數</TD><TD>需退選人數(不考慮保留)</TD></TR>
);

@dept = Find_All_Dept();
$all_student = Read_All_Student_Data();

foreach $dept (@dept) {
  @course = Find_All_Course($dept);
  %dept = Read_Dept($dept);
  foreach $course (@course) {
    %course = Read_Course($dept, $$course{id}, $$course{group});
    if( $course{number_limit} > 0 ) {
      @students = Student_in_Course($dept, $$course{id}, $$course{group});
      $no_of_student = @students;
      if( $no_of_student > $course{number_limit} - $course{reserved_number} ) {
        $no_of_course ++;
        $no_of_exceed = ($no_of_student - $course{number_limit} + $course{reserved_number});
        $total_of_exceed += $no_of_exceed;
	$no_of_exceed2 = $no_of_student - $course{number_limit};
	$no_of_exceed2 = 0  if($no_of_exceed2<0);
	$total_of_exceed2 += $no_of_exceed2;
#        print ("$dept{cname2}  $course{id}  $course{group} 限修 $course{number_limit} 人, 保留 $course{reserved_number} 人, 修課 $no_of_student 人.\n<br>");
        print ("<TR bgcolor=#dddddd><TD>$dept{cname2}</TD><TD>$course{id}</TD><TD>$course{group}</TD><TD>限$course{number_limit}人</TD><TD>保留$course{reserved_number}人</TD><TD>$no_of_student人</TD><TD><font color=red>$no_of_exceed人</font></TD><TD><font color=red>$no_of_exceed2人</font></TD></TR>\n");
        if($Input{see_student} == 1) {
          print("<TR>&nbsp<TD></TD><TD colspan=6>");
          $course_student_count = 0;
          foreach $student (@students) {
#            %student = Read_Student($student);
            if($course_student_count >= $course{number_limit} - $course{reserved_number} ) {
              print("$student $$S{$student}{name}, ");
              %s_dept = Read_Dept($$S{$student}{dept});
              print EXCEED ("$$S{$student}{dept}\t$s_dept{cname2}\t$student\t$$S{$student}{name}\t$course{id}\t$course{group}\t$course{cname}\n");
              if($Input{delete_course} == 1) {
                print("TEST: $student, $dept, $$course{id}, $$course{group}<br>");
#                Delete_Student_Course($student, $dept, $$course{id}, $$course{group});
              }
            }
            $course_student_count++;
          }
          print("</TD></TR>");
        }
      }
    }
  }
}
print ("</table>");
print qq (
  <font color=red>共 $no_of_course 門科目超修, $total_of_exceed 名學生需被退選!, $total_of_exceed2 名學生需被退選(不考慮保留)!\n</font><br>
  <FORM action="Find_Exceed.cgi" method=POST>
       <INPUT type="hidden" name="see_student" value="1">
       <INPUT type="submit" value="檢視學生名單">
  </FORM>
);

if( $Input{see_student} == 1 ) {
 print qq (
   <A href="$exceed_URL">套表列印名單</A>
   (要看最新版<font color=RED>請務必Reload!</FONT>)<br>
   <FORM action="Find_Exceed.cgi" method="POST">
     <INPUT type="hidden" name="delete_course" value="1">
     <INPUT type="hidden" name="see_student" value="1">
     <INPUT type="submit" value="將超修學生退掉">(請小心使用!)
   </FORM>

 );
}
