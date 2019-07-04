#!/usr/local/bin/perl
###########################################################################
#####   Multi_Transfer_Course3.cgi
#####   �h��h�ॲ��/�����
#####   ���Y�t�ůZ���ǥͥ�����׬Y��دZ�O
#####   Coder: Nidalap
#####   Date : 09/05/2001
#####   Update: ����Ǹ��_���ƥ\��added on 2005/01/13 :D~
###########################################################################
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Course.pm";
print("Content-type:text/html\n\n");

%Input = User_Input();
%dept = Read_Dept($Input{dept});
%stu_dept = Read_Dept($Input{stu_dept});
@property = ("", "����", "���", "�q��");
@temp = split(/\*:::\*/,$Input{course});
$i = 0;
foreach $temp (@temp) {
  (${$course[$i]}{id}, ${$course[$i]}{group}) = split(/_/, $temp);
  $i++;
}
@stu_dept = split(/\*:::\*/,$Input{stu_dept});
@stu_grade = split(/\*:::\*/,$Input{stu_grade});
@stu_class = split(/\*:::\*/,$Input{stu_class});

print << "TABLE_1"
 <HEAD><TITLE>����/���������</TITLE></HEAD>
   <BODY background="$GRAPH_URL./ccu-sbg.jpg"><CENTER>
     <H1>����/���������<br>���ɽT�{<hr></H1>
TABLE_1
;

#foreach $course (@course) {
#  print("$$course{id}, $$course{group}<BR>\n");
#}
#print("@stu_dept<BR>\n");
#print("@stu_grade<BR>\n");
#print("@stu_class<BR>\n");
#print("$Input{property}<BR>\n");

#@student = Find_All_Student_In_Dept($Input{stu_dept});
@all_student = Find_All_Student();
Read_All_Student_Data();          ## ����global var %S
Print_Course_Table();             ## �L�X�W�ӿ��ǤU�Ӫ����
@student = Find_Student_List();   ## ��X�Ҧ����v�T�ǥͪ����list(hash�L)
$student_number = @student;
@quota = Assign_Quota($student_number, $total_available_number,
                      @available_number);
@student_in_each_course = Dispatch();
Print_Quota_Table();
Print_Student_Table();
#Print_Test_Table();
Print_Form_Data();
#############################################################################
sub Print_Test_Table()
{
  my(%dispatch);
  my(@color) = ("990000", "009900", "000099", "999900", "009999");
  my $fs = "<FONT size=1>";
  print("<TABLE border=1>");
  $i=0;
  foreach $dispatch (@student_in_each_course) {
    foreach $student (@{$dispatch}) {
      $dispatch{$student} = $i;
    }
    $i++;
  }
                            
  foreach $student (@unscrambled_student) {
    print qq(
      <TR>
        <TD>$fs$student</TD>
        <TD>$fs<FONT color=$color[$dispatch{$student}]>��</FONT></TD>
      </TR>
    );
  }
  print("</TABLE>");
}
#############################################################################
sub Print_Form_Data()
{
  print qq(
    <FORM action=Multi_Transfer_Course4.cgi method=POST>
      <INPUT type="hidden" name="dept" value=$Input{dept}>
      <INPUT type="hidden" name="grade" value=$Input{grade}>
      <INPUT type="hidden" name="property" value=$Input{property}>
  );

  for($i=0; exists(${$course[$i]}{id}); $i++ ) {
    $course_ = ${$course[$i]}{id} . "_" . ${$course[$i]}{group};
    $stu_string = join("_", @{$student_in_each_course[$i]});
    print("<INPUT type=hidden name=\"$course_\" value=\"$stu_string\">\n")
  }

  print qq(
    <INPUT type=submit value="�T�{����">
  );
}
#############################################################################
sub Print_Quota_Table()
{
  print qq(
    <TABLE border=1>
      <TR>
        <TD bgcolor=YELLOW>�ǥͤH��</TD>
        <TD bgcolor=YELLOW>��ؾl�B�H��</TD>
        <TD bgcolor=YELLOW>�C�Z���t�H��</TD>
      </TR>
      <TR>
        <TD>$student_number</TD>
        <TD>$total_available_number</TD>
        <TD>@quota</TD>
      </TR>
    </TABLE>  
  );
}
#############################################################################
sub Dispatch()
{
  my($i, $j, $k, $rest, $quota_used, @dispatch);
  
  $quota_used = Sum(@quota);
  $rest = $student_number - $quota_used;
  $quota[0] += $rest;

  $k=0;
  for($i=0; exists(${$course[$i]}{id}); $i++) {
    for($j=0; $j<$quota[$i]; $j++) {
      push( @{$dispatch[$i]}, $student[$k] );
      $k++;
    }
  }
  return(@dispatch);
}
#############################################################################
sub Sum()
{
  my($sum);
  my(@list) = @_;
  foreach $mem (@list) {
    $sum += $mem;
  }
  return($sum);
}
#############################################################################
sub Assign_Quota()
{
  my($student_number, $total, @available) = @_;
  my(@quota);
#  print("$student_number, $total_available_number, @available_number<BR>");
  foreach $available (@available) {
    $quota = int($student_number * $available / $total);
    push(@quota, $quota);
  }
  return(@quota);
}
#############################################################################
sub Find_Student_List()
{
  $filter = $Input{stu_id_filter};
  
  foreach $stu (@all_student) {
    foreach $stu_dept (@stu_dept) {
      foreach $stu_grade (@stu_grade) {
        foreach $stu_class (@stu_class) {
          if(  ($$S{$stu}{dept} eq $stu_dept) 
               and($$S{$stu}{grade} eq $stu_grade)
               and($$S{$stu}{class} eq $stu_class) ) {
            if(   ($filter == "1")                         ##  �O�_����Ǹ��_����
                or( ($filter == "2") and ( ($stu%2) == 1 ) )
                or( ($filter == "3") and ( ($stu%2) == 0 ) ) )  {
              push(@student, $stu);
            }
          }
        }
      }
    }
  }
  @unscrambled_student = @student;           ### ���ե�
  @student = Scramble(@student);
  return(@student);
}
#############################################################################
sub Print_Student_Table()
{
  print qq(
    <TABLE border=1 width=85%>
      <TR><TH bgcolor=YELLOW>���</TH><TH bgcolor=YELLOW>�ǥ�</TH></TR>
  );
  for($i=0; exists(${$course[$i]}{id}); $i++ ) {
    print qq(
        <TR>
          <TD>${$course[$i]}{id}<BR>${$course[$i]}{group}</TD>
          <TD><FONT size=2>@{$student_in_each_course[$i]}</TD>
        </TR>
    );
  }
  print("</TABLE>");
}
#############################################################################
sub Scramble()
{
  my(@list) = @_;
#  my($id, $size, %list, @return_list, $i, $j, $victim);
  my($iteration, $i, $j, $tmp, @return_list);

  srand();
  $size = @list;
  for($iteration=0; $iteration<$size; $iteration++ ) {
    $i = int(rand($size));
    $j = int(rand($size));
    $tmp = $list[$i];
    $list[$i] = $list[$j];
    $list[$j] = $tmp;
  }
  @return_list = @list; 
#  foreach $element (@list) {
#    $list{$element} = 1;
#  }
#  foreach $element (keys %list) {
#    push(@return_list, $element);
#  } 
  return(@return_list);
}
#############################################################################
sub Print_Course_Table() 
{
  print qq(
    <TABLE border=1 width=85%>
      <TR><TD valign=TOP align=CENTER>
        <TABLE border=0 width=95%>
          <TR bgcolor=YELLOW>
            <TH colspan=5>��ظ��</TH>
          </TR><TR>
            <TD>��إN�X</TD>
            <TD>��دZ�O</TD>
            <TD>��ؤ���W��</TD>
            <TD>���פH��</TD>
            <TD>�l�B</TD>
          </TR>
  );
  foreach $course (@course) {
    %course = Read_Course($Input{dept}, $$course{id}, $$course{group}, "" );
    $num = Student_in_Course($Input{dept}, $$course{id}, $$course{group});
    $course{number_limit}=1000  if($course{number_limit} == 0);
    $num = $course{number_limit} - $num;
    push(@available_number, $num);
    $total_available_number += $num;
    print qq(
      <TR>
        <TD>$$course{id}</TD>
        <TD>$$course{group}</TD>
        <TD>$course{cname}</TD>
        <TD>$course{number_limit}</TD>
        <TD>$num</TD>
      </TR>
    );
  }
  $stu_dept = join(", ", @stu_dept);
  $stu_grade = join(", ", @stu_grade);
  $stu_class = join(", ", @stu_class);
  print qq(
        </TABLE>
     </TD>
     <TD valign=TOP align=CENTER>
        <TABLE border=0 width=95%>
          <TR>
            <TH colspan=4 bgcolor=YELLOW>�ǥ͸��</TH>
          </TR>
          <TR><TD>
            ���ݨt�� :$stu_dept<BR>
            �~�� : $stu_grade<BR>
            �Z�� : $stu_class<BR>
          </TD></TR>
        </TABLE>
       </TD>
      </TR>
     </TABLE>
  );
}
############################################################################
