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

$SUB_SYSTEM_NAME[1] = "一般";

$course_count = Count_Open_Course();
$course_count_all = Count_Open_Course("history");
$system_state = Whats_Sys_State();
@SYSTEM_STATE = ("關閉", "開放查詢", "開放加退選");
print("Content-type:text/html\n\n");

print qq(
  <H1>開排選課系統狀態</H1>
  <HR>
  <CENTER>
  <TABLE border=1 width=75%>
    <TR>
      <TD rowspan=4 bgcolor=YELLOW>系統狀態</TD>
      <TD>學年</TD><TD>$YEAR</TD>
    </TR>
    <TR><TD>學期</TD><TD>$TERM</TD></TR>
    <TR><TD>子系統名稱</TD><TD>$SUB_SYSTEM($SUB_SYSTEM_NAME[$SUB_SYSTEM])</TD></TR>
    <TR><TD>系所數量</TD><TD>$dept_count</TD></TR>
    
    <TR>
      <TD rowspan=3 bgcolor=YELLOW>開課系統狀態</TD>
      <TD></TD><TD></TD>
    </TR>
    <TR><TD>當學期開課數目</TD><TD>$course_count</TD></TR>
    <TR><TD>歷年開課數目</TD><TD>$course_count_all</TD></TR>
        
          
    <TR>    
      <TD rowspan=2 bgcolor=YELLOW>選課系統狀態</TD>
      <TD>系統開關</TD><TD>$SYSTEM_STATE[$system_state]</TD>
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