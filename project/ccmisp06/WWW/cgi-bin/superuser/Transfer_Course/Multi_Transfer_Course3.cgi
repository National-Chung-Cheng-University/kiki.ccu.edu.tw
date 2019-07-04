#!/usr/local/bin/perl
###########################################################################
#####   Multi_Transfer_Course3.cgi
#####   多對多轉必修/必選課
#####   幫某系級班的學生全部選修某科目班別
#####   Coder: Nidalap
#####   Date : 09/05/2001
#####   Update: 限制學號奇偶數功能added on 2005/01/13 :D~
###########################################################################
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."System_Settings.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Course.pm";
print("Content-type:text/html\n\n");

%Input = User_Input();
%dept = Read_Dept($Input{dept});
%stu_dept = Read_Dept($Input{stu_dept});
@property = ("", "必修", "選修", "通識");
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
  <HEAD>
    $EXPIRE_META_TAG
    <TITLE>多對多必修/必選課轉檔</TITLE>
  </HEAD>
   <BODY background="$GRAPH_URL./ccu-sbg.jpg"><CENTER>
     <H1>必修/必選課轉檔<br>轉檔確認<hr></H1>
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
Read_All_Student_Data();          ## 產生global var %S
Print_Course_Table();             ## 印出上個選單傳下來的資料
@student = Find_Student_List();   ## 找出所有受影響學生的資料list(hash過)
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
        <TD>$fs<FONT color=$color[$dispatch{$student}]>◎</FONT></TD>
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

#  foreach $k (keys %S) {
#    print("$k : $S{name}<BR>\n");
#  }

  for($i=0; exists(${$course[$i]}{id}); $i++ ) {
    $course_ = ${$course[$i]}{id} . "_" . ${$course[$i]}{group};
    $stu_string = join("_", @{$student_in_each_course[$i]});
    print("<INPUT type=hidden name=\"$course_\" value=\"$stu_string\">\n")
  }

  print qq(
    <INPUT type=submit value="確認轉檔">
  );
}
#############################################################################
sub Print_Quota_Table()
{
  print qq(
    <TABLE border=1>
      <TR>
        <TD bgcolor=YELLOW>學生人數</TD>
        <TD bgcolor=YELLOW>科目餘額人數</TD>
        <TD bgcolor=YELLOW>每班分配人數</TD>
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
            if(   ($filter == "1")                         ##  是否限制學號奇偶數
                or( ($filter == "2") and ( ($stu%2) == 1 ) )
                or( ($filter == "3") and ( ($stu%2) == 0 ) ) )  {
              push(@student, $stu);
            }
          }
        }
      }
    }
  }
  @unscrambled_student = @student;           ### 測試用
  @student = Scramble(@student);
  return(@student);
}
#############################################################################
sub Print_Student_Table()
{
  print qq(
    <TABLE border=1 width=85%>
      <TR><TH bgcolor=YELLOW>科目</TH><TH bgcolor=YELLOW>學生</TH></TR>
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
            <TH colspan=5>科目資料</TH>
          </TR><TR>
            <TD>科目代碼</TD>
            <TD>科目班別</TD>
            <TD>科目中文名稱</TD>
            <TD>限修人數</TD>
            <TD>餘額</TD>
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
            <TH colspan=4 bgcolor=YELLOW>學生資料</TH>
          </TR>
          <TR><TD>
            所屬系所 :$stu_dept<BR>
            年級 : $stu_grade<BR>
            班級 : $stu_class<BR>
          </TD></TR>
        </TABLE>
       </TD>
      </TR>
     </TABLE>
  );
}
############################################################################
