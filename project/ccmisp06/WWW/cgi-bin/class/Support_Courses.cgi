#!/usr/local/bin/perl
###############################################################################################
#####  Support_Courses.cgi
#####  顯示支援本班課程
#####  Updates: 
#####    2008/04/29 從 Selected_View00.cgi 修改而來
#####	 2009/06/04  為 Find_All_Dept 加上 "NO_COM_DEPT" 參數，只讀取可以開課的系所 Nidalap :D~
#####    2010/01/04  將 $yearterm 改為 $year, $term 以避免民國百年 bug  Nidalap :D~
################################################################################################
#print("Content-type:text/html\n\n");

require "../library/Reference.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."System_Settings.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Password.pm";
#require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Select_Course.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Teacher.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Session.pm";

###########################################################################

print("Content-type:text/html\n\n");
%Input = User_Input();

($id, $Input{password}, $login_time, $ip) = Read_Session($Input{session_id}, "", 1);
Check_Student_Password($id, $Input{password});

############################################################################
###  由輸入的 year, term 判斷是否要讀取本學期資料, 或是以前的資料
if( $Input{year} != "" ) {
  $year = $Input{year};
}else{
  $year = $YEAR;
}

if( $Input{term} != "" ) {
  $term = $Input{term};
}else{
  $term = $TERM;
}

#if( ($year==$YEAR) and ($term==$TERM) ) {
#  $yearterm = "";
#}else{
#  $yearterm = $year . $term;
#}
#print("session_id, id, pass = $Input{session_id}, $id, $Input{password}<BR>"); 

############################################################################

my(%Student,%Dept);

#print("[year, term] = [$year, $term]<BR>\n");
#%Input=User_Input();

%Student=Read_Student($id);
if( $Student{name} eq "" ) {
  print("<CENTER><H1>查無此學生資料!<BR>");
  exit();
}

####    2009/06/05  改由在讀取學生學籍資料時，就依照註冊次數與升級與否設定判斷年級  Nidalap :D~
#if( is_Grade_Update() == 1){
#  $Student{grade}++;
#  $Student{grade}=4  if( $Student{grade} > 4 );  ### 2004/06/07發現BUG更新
#}

%Dept=Read_Dept($Student{dept});
@MyCourse=Course_of_Student($Student{id}, $year, $term);
my($HEAD_DATA)=Head_of_Individual($Student{name},$Student{id},$Dept{cname},$Student{grade},$Student{class});

###################    若非選課時間則顯示不可進入  ################
if($SUPERUSER != 1){     ## 非 superuser 的使用者
#  if( (Whats_Sys_State()==0)or(Check_Time_Map(%Student)!=1) ){
  if( Whats_Sys_State()==0 ) {
    Enter_Menu_Sys_State_Forbidden($HEAD_DATA);
  }
}
###################################################################
my($Table_Data)=Create_Support_Course_Table();
#my($COURSE_TIME_TABLE) = Create_Course_Time_Table();
#my($BOARD_TEXT) = Read_Board();

#Student_Log("View  ", $id, "", "", "");

MAIN_VIEW_HTML($HEAD_DATA,$Table_Data);

###################################################################################
sub MAIN_VIEW_HTML
{
  my($HEAD_DATA,$DATA)=@_;
  if(Whats_Sys_State() == 1){
    $LINK=Select_Course_Link_2_Safe($Input{session_id});
  }elsif(Whats_Sys_State() == 2){
    if(Check_Time_Map($id)==1){
      $LINK=Select_Course_Link($id,$Input{password});
    }else{
      $LINK=Select_Course_Link_2_Safe($Input{session_id});
    }
#   $LINK=Select_Course_Link($id,$Input{password});
  }

  if( $Input{reload} == 1 ) {
    $reload_tag = "onLoad=\"window.location.reload()\"";
  }

  print qq(
    <html>
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      $EXPIRE_META_TAG            
      <TITLE>國立中正大學$SUB_SYSTEM_NAME選課系統--支援本班課程</TITLE>
    </head>
    <body background="$GRAPH_URL./ccu-sbg.jpg" $reload_tag> 
    <center>
      $HEAD_DATA 
      <hr>
      <br>
  );
#  Warn_of_Course_Conflict();
#  print qq(
#    <BUTTON onClick="window.location.reload()">REFRESH</BUTTON>
#  );
  
  print qq(
      <font size=4><b>以下為支援 $Dept{cname} $Student{grade} 年級 $Student{class} 班的課程:<B></FONT><P>
      $DATA
      <P>
  );
#  Create_Course_Time_Table();
#  Warn_of_Course_Conflict();
  print qq(
    </center>
    </body>
    $EXPIRE_META_TAG2
    </html>
  );
}
######################################################################
sub Create_Support_Course_Table
{
  my($DATA)="";
  my(@Teachers)=Read_Teacher_File();
  my @WeekDay = @WEEKDAY;
  my @TimeMap = @TIMEMAP;
  my($supp_file) = $DATA_PATH . "Course_supported/" . $Student{dept} . "_" . $Student{grade} . $Student{class};
  my(@temp, $supp_dept, $supp_cid, $supp_group);
  
#  print("supp_file = $supp_file\n");
  open(SUPP_FILE, $supp_file);
  @temp = <SUPP_FILE>;
  close(SUPP_FILE);  
  
  $DATA = $DATA."<table width=90% border=1 cellspacing=0 cellpadding=3>\n";
  $DATA = $DATA."<tr>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>加選</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>開課系所</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>科目代碼</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>班別</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>科目名稱</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>授課教師</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>學分</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>星期節次</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>教室</font></th>\n";
  $DATA = $DATA."</tr>\n";

  ####  列印相關課程資料  ####
  foreach $temp (@temp) {
    ($supp_dept, $supp_cid, $supp_group) = split(/\s+/, $temp);
    my %supp_dept = Read_Dept($supp_dept);
    my(%theCourse)=Read_Course($supp_dept,$supp_cid,$supp_group);
      $CreditSum += $theCourse{credit};
      $DATA = $DATA."<tr>\n";
      $DATA = $DATA."<th><font size=2>";
      $DATA = $DATA."<A href=\"Add_Course01.cgi?session_id=$Input{session_id}&dept=$supp_dept&grade=$theCourse{grade}&page=0\">加選</A>";
      $DATA = $DATA."</font></th>\n";
      $DATA = $DATA."<th><font size=2>";
      $DATA = $DATA.$supp_dept{cname};                         ##  開課系所
      $DATA = $DATA."</font></th>\n";
      $DATA = $DATA."<th><font size=2>";
      $DATA = $DATA.$theCourse{id};                         ##  科目代碼
      $DATA = $DATA."</font></th>\n";
      $DATA = $DATA."<th><font size=2>";
      $DATA = $DATA.$theCourse{group}."</font></th>\n";     ##  班別

      $DATA = $DATA."<th><font size=2>";
      $DATA = $DATA.$theCourse{cname}."</font></th>\n";     ##  科目名稱

      $DATA=$DATA."<th><font size=2>";           ##  授課教師
      $T=@{$theCourse{teacher}};
      for($teacher=0; $teacher < $T; $teacher++){
        if($theCourse{teacher}[$teacher] != 99999){
          $DATA=$DATA.$Teacher_Name{$theCourse{teacher}[$teacher]};
        }else{
          $DATA=$DATA."教師未定";
        }
        if($teacher != $T-1){
          $DATA=$DATA.", ";
        }
      }
      $DATA=$DATA."</font></th>\n";


      $DATA = $DATA."<th><font size=2>";
      $DATA = $DATA.$theCourse{credit}."</font></th>\n";    ##  學分

      $DATA=$DATA."<th><font size=2>";           ## 星期節次
      $time_string = Format_Time_String($theCourse{time});
      $DATA .= $time_string;
      $DATA=$DATA."</font></th>\n";

      $DATA=$DATA."<th><font size=2>";           ##  教室
      %Room=Read_Classroom($theCourse{classroom});
      $DATA=$DATA.$Room{cname};
      $DATA=$DATA."</font></th>\n";

      $DATA = $DATA."</tr>\n";
  }

  $DATA = $DATA."</table>\n";

return($DATA);
}
#-----------------------------------------------------------------------
sub Check_Time_Map
{
  ###################################################
  ##  Step 1: 取得學生的年級##
  ##  Step 2: 讀取相關的時間設定檔##
  ###################################################
  my($user)=@_;
  my($MapClass)=Check_Map_Class($user);
  my($FileName)=$REFERENCE_PATH."SelectTimeMap/".$MapClass.".map";

  %User=Read_Student($user);
  open(FILE,"<$FileName");
      @Orignal=<FILE>;
      foreach $item(@Orignal){
        my($dept, $state)=split(/\s+/,$item);
        $My_Time{$dept}=$state;
      }
  $FileName=$REFERENCE_PATH."TimeMap/T".$My_Time{$User{dept}}.".map";
  open(FILE,"<$FileName");
  my($count)=0;
  @Duration=<FILE>;
  foreach $item(@Duration){
    $item=~s/\n//;
    ($TD[$count]{S},$TD[$count]{E})=split(/\s+/,$item);
    $count++;
  }

  my($sec,$min,$hour,$day,$nmonth,$year,$wday,$yday,$isdst) = localtime(time);

  $Value=$min+$hour*100;

  for($i=0; $i < $count; $i++){
    if( ($Value > int($TD[$i]{S})) && ($Value < int($TD[$i]{E})) ){
      $Flag = 1;
    }
  }

  return($Flag);
}
#-----------------------------------------------------------------------
sub Check_Map_Class
{
  my($user)=@_;
  %User=Read_Student($user);

  if($User{dept}%10 <= 4){    ##  大一至大四
    return($User{grade});
  }else{
    if($User{grade} == 1){    ##  研一或博一
      return(5);
    }else{                    ##  研二以上含博士班學生
      return(6);
    }
  }
}

###########################################################################
###  讀取選課單公佈欄
sub Read_Board()
{
  my($text, $board_file, @temp);
  $board_file = $REFERENCE_PATH."select_course_board.txt";
  open(BOARD, $board_file) or 
      Fatal_Error("Cannot read file $board_file in Selected_View00.cgi!");
  @temp = <BOARD>;
  close(BOARD);
  $text = join("", @temp);
  $text =~ s/\n/<br>\n/g;
  return $text;
}
###########################################################################
#####  Create_Course_Time_Table()
#####  產生功課表HTML Table
###########################################################################
sub Create_Course_Time_Table()
{
  my($day, $time, $table_data, %time_map);
  my($i, @selected_time, %the_Course, %cell);

  foreach $course (@MyCourse) {
    %the_Course = Read_Course($$course{dept}, $$course{id}, $$course{group}, $year, $term);
#    print("$the_Course{id} $the_Course{cname}<br>\n");
    foreach $time (@{$the_Course{time}}) {
#      print("$time -> $$time{week} $$time{time}<BR>\n");
      $selected_time[$i]{week} = $$time{week};
      $selected_time[$i]{time} = $$time{time};
      $selected_time[$i]{course} = $the_Course{cname};
      $i++;
    }
  }
#  Check_Multiple_Course_Collisions(@selected_time);
  %cell = Format_Time(@selected_time);
  $time_table = Print_Timetable(%cell);
  print $time_table;
}
#############################################################################
#####  Warn_of_Course_Conflict()
#####  檢查並警告課程自相衝堂的問題(程式碼從 Add_Course01.cgi 抄來)
#####  Added: 2005/04/13, Nidalap :D~
#############################################################################
sub Warn_of_Course_Conflict()
{
  local @time_map;
  my %The_Course, $total_credit, $conflict_flag, $conflict_string;
  ####################  檢查學生早已修習的課, 建立@time_map及記算學分
  @Course_of_Student = Course_of_Student($Student{id}, $year, $term);
  foreach $stu_course (@Course_of_Student) {
    %The_Course = Read_Course($$stu_course{dept}, $$stu_course{id}, $$stu_course{group}, $year, $term, $Student{id});
    $total_credit += $The_Course{credit};
    my $course_identifier = join("_", $$stu_course{dept}, $$stu_course{id}, $$stu_course{group});
    ($conflict_flag, $conflict_string) = Check_Course_Conflict(%The_Course);
    if( $conflict_flag == 1 ) {
      print("<P>$conflict_string<P>");
#      return("0", $conflict_string);
    };
  }

}
############################################################################################
#####  Check_Course_Conflict
#####  檢查科目衝堂
#####  檢查每個科目的時段, 將時段加入@time_map陣列, 如果陣列中已有值則判斷衝堂.
#####  先檢查已修習的科目, 是否已經有衝堂情形(可能因為科目異動),
#####  再檢查學生所選的科目.
#####  輸入         : %The_Course
#####  輸出         : ($conflict_flag, $conflict_string) $conflict_flag:(0,1)=(不衝, 衝堂)
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
#####  輸出         : ($conflict_flag, $conflict_string) $flag:(0,1) = (不衝, 衝堂)
#####  用到local變數: @time_map
############################################################################################
sub Check_and_Modify_Time_Map
{
  my($week, $time, $course_identifier) = @_;
  my($conflict_string, $flag, $size);

  foreach $ut (@time_map) {           ### 檢查每一個已經用掉的時間, $ut = used_time
    $flag = is_Time_Collision($$ut{week}, $$ut{time}, $week, $time);
    if( $flag != 0 ) {                ###   若有衝堂情形...
      $conflict_string = "您所選的科目有衝堂情形:";
      $conflict_string .="<FONT color=RED><U><B>(星期$WEEKDAY[$$ut{week}]的第 $$ut{time} 堂)";
      $conflict_string .=" 與 (星期$WEEKDAY[$week]的第 $time 堂)</B></U></FONT>";
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
