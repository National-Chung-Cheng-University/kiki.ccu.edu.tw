#!/usr/local/bin/perl
##########################################################################
#####     Find_Exceed.cgi
#####     ��X�Ҧ���פH�ƶW�L (��ح��פH�� - �O�d�H��) ���W��
#####     ���{�����Ϥ��{��, �]�������p�@�뤣�|�o��!
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
    <CENTER><H1>�Ҧ��W�׬��
    <hr></H1>
    <TABLE border=1>
    <TR bgcolor=YELLOW><TD>�t�O</TD><TD>��إN�X</TD><TD>��دZ�O</TD><TD>���פH��</TD><TD>�O�d�H��</TD><TD>��פH��</TD><TD>�ݰh��H��</TD><TD>�ݰh��H��(���Ҽ{�O�d)</TD></TR>
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
#        print ("$dept{cname2}  $course{id}  $course{group} ���� $course{number_limit} �H, �O�d $course{reserved_number} �H, �׽� $no_of_student �H.\n<br>");
        print ("<TR bgcolor=#dddddd><TD>$dept{cname2}</TD><TD>$course{id}</TD><TD>$course{group}</TD><TD>��$course{number_limit}�H</TD><TD>�O�d$course{reserved_number}�H</TD><TD>$no_of_student�H</TD><TD><font color=red>$no_of_exceed�H</font></TD><TD><font color=red>$no_of_exceed2�H</font></TD></TR>\n");
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
  <font color=red>�@ $no_of_course ����ضW��, $total_of_exceed �W�ǥͻݳQ�h��!, $total_of_exceed2 �W�ǥͻݳQ�h��(���Ҽ{�O�d)!\n</font><br>
  <FORM action="Find_Exceed.cgi" method=POST>
       <INPUT type="hidden" name="see_student" value="1">
       <INPUT type="submit" value="�˵��ǥͦW��">
  </FORM>
);

if( $Input{see_student} == 1 ) {
 print qq (
   <A href="$exceed_URL">�M��C�L�W��</A>
   (�n�ݳ̷s��<font color=RED>�аȥ�Reload!</FONT>)<br>
   <FORM action="Find_Exceed.cgi" method="POST">
     <INPUT type="hidden" name="delete_course" value="1">
     <INPUT type="hidden" name="see_student" value="1">
     <INPUT type="submit" value="�N�W�׾ǥͰh��">(�Фp�ߨϥ�!)
   </FORM>

 );
}
