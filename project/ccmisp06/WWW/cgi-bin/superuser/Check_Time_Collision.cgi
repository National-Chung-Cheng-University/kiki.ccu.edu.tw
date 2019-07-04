#!/usr/local/bin/perl
##########################################################################
#####     Check_Time_Collision.cgi
#####     找出所有學生選課衝堂的名單
#####     Coder: Nidalap
#####     Date: 2011/09/07
##########################################################################        
require "../../../LIB/Reference.pm";
require $LIBRARY_PATH . "Student_Course.pm";
require $LIBRARY_PATH . "Student.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Course.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "System_Settings.pm";
require $LIBRARY_PATH . "Common_Utility.pm";

$| = 1;

%Input = User_Input();
#$exceed_file = $TEMP_PATH . "exceed.txt";
#$exceed_URL = $HOME_URL . "Temp/exceed.txt";
open(EXCEED, ">$exceed_file");

print("Content-type:text/html\n\n");
print qq(
  $EXPIRE_META_TAG
  <BODY background="$GRAPH_URL/manager.jpg">
    <CENTER><H1>所有選課衝堂的學生
    <hr></H1>
    <TABLE border=1>
);

@dept = Find_All_Dept();
@stu = Find_All_Student();
local(@time_map);            ###  用做檢查衝堂的陣列, Check_Course_Conflict()會更動之

#%S = Read_All_Student_Data();  #  產生 %S



ID: foreach $id (@stu) {
  next if($id !~ /^400/ );
  
  @time_map = "";
  ####################  檢查學生早已修習的課, 建立@time_map及記算學分  ####################
  @Course_of_Student = Course_of_Student($id);
  foreach $stu_course (@Course_of_Student) {
    %The_Course = Read_Course($$stu_course{dept}, $$stu_course{id}, $$stu_course{group}, "", "", $id);
    my $course_identifier = join("_", $$stu_course{dept}, $$stu_course{id}, $$stu_course{group});
    ($conflict_flag, $conflict_string) = Check_Course_Conflict(%The_Course);
    if( $conflict_flag == 1 ) {
      push @conflict, $id;
      next ID;
#      return("0", $conflict_string); 
    };
  }
}

$count = @conflict;
print("共 $count 名新生有衝堂問題！<BR>\n");
foreach $id (@conflict) { 
  print "$id <BR>\n";
}

############################################################################################
#####  Check_Course_Conflict
#####  檢查科目衝堂
#####  檢查每個科目的時段, 將時段加入@time_map陣列, 如果陣列中已有值則判斷衝堂.
#####  先檢查已修習的科目, 是否已經有衝堂情形(可能因為科目異動),
#####  再檢查學生所選的科目.
#####  輸入         : %The_Course
#####  輸出         : ($conflict_flag, $conflict_string)   $conflict_flag:(0,1)=(不衝, 衝堂)
#####  使用local變數: @time_map, @Student_Course
############################################################################################
sub Check_Course_Conflict
{
  my(%The_Course) = @_;
  my($conflict_flag, $conflict_string);
#  print("Checking $The_Course{id} _ $The_Course{group}<br>\n");

  my $course_identifier = join("_", $The_Course{dept}, $The_Course{id}, $The_Course{group});
  foreach $course_time (@{$The_Course{time}}) {
#    print("Checking time [$$course_time{week}][$$course_time{time}]<br>\n");
    ($conflict_flag, $conflict_string) =
         Check_and_Modify_Time_Map($$course_time{week}, $$course_time{time}, $course_identifier);
    if($conflict_flag == 1) {
      return(1, $conflict_string);
    }
  }
}
############################################################################################
#####  Check_and_Modify_Time_Map
#####  檢查時間衝突
#####  由傳入的星期幾第幾堂時間, 比對每一筆@time_map中的資料, 並傳回是否衝堂的訊息
#####  輸入         : ($week, $time, $course_identifier)
#####  輸出         : ($conflict_flag, $conflict_string)          $flag:(0,1) = (不衝, 衝堂)
#####  用到local變數: @time_map
############################################################################################
sub Check_and_Modify_Time_Map
{
  my($week, $time, $course_identifier) = @_;
  my($conflict_string, $flag, $size);

  foreach $ut (@time_map) {           ### 檢查每一個已經用掉的時間, $ut = used_time
    $flag = is_Time_Collision($$ut{week}, $$ut{time}, $week, $time);
    if( $flag != 0 ) {                ###   若有衝堂情形...
      $conflict_string = "您所選的科目(或原先已選科目)有衝堂情形:<BR>";
      $conflict_string .="<FONT color=RED>(星期$WEEKDAY[$$ut{week}]的第 $$ut{time} 堂)";
      $conflict_string .=" 與 (星期$WEEKDAY[$week]的第 $time 堂)";
      last;
    }
  }
  if( $flag == 0 ) {                  ###  若檢查無誤, 將此時段標為已用
    $size = @time_map;
    $time_map[$size]{week} = $week;
    $time_map[$size]{time} = $time;
    return(0, "");
  }else{                              ###  若檢查有誤, 回覆錯誤訊息
    return(1, $conflict_string);
  }
}