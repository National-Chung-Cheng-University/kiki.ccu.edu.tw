#!/usr/local/bin/perl
############################################################################
#####  Selected_View_Multiple.cgi
#####  檢視已選修科目: 一次列印多個學生選課單, 方便導師一次檢視
#####  此功能是從教師專業系統連結過來(淑娟負責).
#####  Updates: 
#####    2008/06/06 從 Selected_View00.cgi 修改而來.
#####    2010/01/04 將 $yearterm 改為 $year, $term 以避免民國百年 bug  Nidalap :D~
#####		    不過此程式似乎沒有在使用了?
#####    2012/02/29  教師查詢功能不受系統不允許查詢的限制  Nidalap :D~
#####    2013/08/28  教師查詢功能帶入 stu_type 參數，用以顯示標題「全部」、「大學部」、「碩士」、「博士」 Nidalap :D~
#####    2013/10/02  新增新版本驗證碼 key 以避免使用者隨便看任何學生的資料 Nidalap :D~
############################################################################
#print("Content-type:text/html\n\n");

require "../library/Reference.pm";
require $LIBRARY_PATH."Common_Utility.pm";
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
require $LIBRARY_PATH."System_Settings.pm";

###########################################################################

$online_help = Online_Help();

print("Content-type:text/html\n\n");
%Input			= User_Input();
$in_key			= $Input{key};
$in_timestamp	= $Input{key1};
@id				= split(/\*:::\*/, $Input{id});

$id_sum = 0;
foreach my $id (@id) {
  $id_sum += $id;
}

$key = Generate_Key2($id_sum, "bOsSlesSLESswORK", $in_timestamp);		### 基本安全檢查
if( $key ne $in_key ) {
  Print_BAN("key_error");
}


print $EXPIRE_META_TAG;
#foreach $key (keys %Input) {
#  print("$key -> $Input{$key}<BR>\n");
#}




if( Check_HTTP_REFERER() != 1 ) {			###  檢查來源
#  print("error!!!");
  Show_Password_Error_Message();
}

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

%stu_type_show = (''=>'所有','4'=>'大學部', '6'=>'碩士', '8'=>'博士');

print "<CENTER><H1>查詢" . $stu_type_show{$Input{'stu_type'}} . "導生選課單</H1></CENTER>";

foreach $id (@id) {
#  print("processing $id...<BR>\n");
  %Student=Read_Student($id);
  if( $Student{name} eq "" ) {
    print("$id: 無此學生資料!<BR>\n");
    next;
  }
  %Dept=Read_Dept($Student{dept});
  @MyCourse=Course_of_Student($Student{id}, $year, $term);
  my($HEAD_DATA)=Head_of_Individual($Student{name},$Student{id},$Dept{cname},$Student{grade},$Student{class});

###################    若非選課時間則顯示不可進入  #################
#  if($SUPERUSER != 1){     ## 非 superuser 的使用者
#    if( Whats_Sys_State()==0 ) {
#      Enter_Menu_Sys_State_Forbidden($HEAD_DATA);
#    }
#  }
###################################################################
  my($Table_Data)=CREAT_COURSE_TABLE();

#Student_Log("View  ", $id, "", "", "");

  MAIN_VIEW_HTML($HEAD_DATA,$Table_Data);
  print("&nbsp<BR>&nbsp<BR>&nbsp<P>");
  
}
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
  my $show_help = Show_Online_Help('SELECTED_VIEW');

  print qq(
    <html>
    $online_help
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      $EXPIRE_META_TAG            
      <TITLE>國立中正大學$SUB_SYSTEM_NAME選課系統--檢視目前已選修科目</TITLE>
    </head>
    <body background="$GRAPH_URL./ccu-sbg.jpg" $reload_tag> 
    <center>
      $HEAD_DATA 
      <hr>
      <br>
  );
  Warn_of_Course_Conflict();
#  print qq(
#    <BUTTON onClick="window.location.reload()">REFRESH</BUTTON>
#  );
  
  print qq(
      <font size=4><b>$year學年度$TERM_NAME[$term]選修科目</b></font>
      $show_help
      $DATA
      <table border=0 width=640>
      <tr>
      <th align=right><font size=2>共修習<u> $MyCount </u>科<u> $CreditSum </u>學分</font></th>
      </tr>
      </table>
      <P>
  );
#  Create_Course_Time_Table();
#  print qq(
#    </center>
#        $BOARD_TEXT
#    <FONT color=RED>
#      本單僅供同學自行參考, 非正式選課單.
#      欲列印選課單請到主選單選擇"列印選課單"選項. 謝謝!
#    </FONT>
#
#    </body>
#    $EXPIRE_META_TAG2
#    </html>
#  );
}
######################################################################
sub CREAT_COURSE_TABLE
{
my($DATA)="";
my(@Teachers)=Read_Teacher_File();
my @WeekDay = @WEEKDAY;
my @TimeMap = @TIMEMAP;
$CreditSum=0;
$MyCount=@MyCourse;
@Credit=CREDIT_TABLE();

  $DATA = $DATA."<table width=90% border=1 cellspacing=0 cellpadding=3>\n";
  $DATA = $DATA."<tr>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>科目代碼</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>班別</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>科目名稱</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>授課教師</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>學分</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>學分歸屬</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>星期節次</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>教室</font></th>\n";
  $DATA = $DATA."</tr>\n";

  ####  列印相關課程資料  ####
  for($i=0; $i < $MyCount; $i++){
      my(%theCourse)=Read_Course($MyCourse[$i]{dept},$MyCourse[$i]{id},$MyCourse[$i]{group},$year, $term);
      $CreditSum += $theCourse{credit};
      $DATA = $DATA."<tr>\n";
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
      $DATA = $DATA."<th><font size=2>";
      $DATA = $DATA.$Credit[$MyCourse[$i]{property}];       ##  學分歸屬
      $DATA = $DATA."</font></th>\n";

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
##############################################################################
sub Print_BAN()
{
  my($msg) = @_;
  if( $msg eq "key_error" ) {
    $msg_show = "驗證碼錯誤，<FONT color=RED>請回上一頁重新讀取</FONT>，以更新驗證碼！";
  }else{
    $msg_show = "";
  }
  
  print qq(
    <html>
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <TITLE>國立中正大學$SUB_SYSTEM_NAME選課系統--檢視目前已選修科目</TITLE>
    </head>
    <body background="$GRAPH_URL./ccu-sbg.jpg">
    <center>
      <FONT face="標楷體">
        <H1>國立中正大學$SUB_SYSTEM_NAME選課系統--檢視目前已選修科目</H1>
      </FONT>
    <HR>
    $msg_show<BR>
  );
  die();
}
