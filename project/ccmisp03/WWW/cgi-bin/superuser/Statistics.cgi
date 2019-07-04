#!/usr/local/bin/perl

######### require .pm files #########
require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Select_Course.pm";
require $LIBRARY_PATH."Error_Message.pm";

######### Main Program Here #########
my(%Input);
%Input=User_Input();
@dept = Find_All_Dept();
$dept_count = @dept;

$SUB_SYSTEM_NAME[1] = "�@��";

$course_count = Count_Open_Course();
$course_count_all = Count_Open_Course("history");
$system_state = Whats_Sys_State();
@SYSTEM_STATE = ("����", "�}��d��", "�}��[�h��");
print("Content-type:text/html\n\n");

print qq(
  <H1>�}�ƿ�Ҩt�Ϊ��A</H1>
  <HR>
  <CENTER>
  <TABLE border=1 width=75%>
    <TR>
      <TD rowspan=4 bgcolor=YELLOW>�t�Ϊ��A</TD>
      <TD>�Ǧ~</TD><TD>$YEAR</TD>
    </TR>
    <TR><TD>�Ǵ�</TD><TD>$TERM</TD></TR>
    <TR><TD>�l�t�ΦW��</TD><TD>$SUB_SYSTEM($SUB_SYSTEM_NAME[$SUB_SYSTEM])</TD></TR>
    <TR><TD>�t�Ҽƶq</TD><TD>$dept_count</TD></TR>
    
    <TR>
      <TD rowspan=3 bgcolor=YELLOW>�}�Ҩt�Ϊ��A</TD>
      <TD></TD><TD></TD>
    </TR>
    <TR><TD>���Ǵ��}�Ҽƥ�</TD><TD>$course_count</TD></TR>
    <TR><TD>���~�}�Ҽƥ�</TD><TD>$course_count_all</TD></TR>
        
          
    <TR>    
      <TD rowspan=2 bgcolor=YELLOW>��Ҩt�Ϊ��A</TD>
      <TD>�t�ζ}��</TD><TD>$SYSTEM_STATE[$system_state]</TD>
    </TR>
    <TR><TD></TD><TD></TD></TR>         
    

                        
  </TABLE>

);
#########################################################################################
sub Count_Open_Course()
{
  my($history_flag) = @_;
  my(@course, $course_count);
  foreach $dept (@dept) {
    if($history_flag eq "history") {
      @course = Find_All_Course($dept, "", "history");
    }else{
      @course = Find_All_Course($dept, "", "");
    }
    $course_count += @course;
  }
  return($course_count);
}