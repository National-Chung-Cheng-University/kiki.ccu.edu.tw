1;
############################################################################
sub Head_of_Individual
{

my($P_name,$P_id,$P_dept,$P_grade,$P_class)=@_;
my($HEAD_DATA)="";

if( $IS_ENGLISH ) {
  @cols = ("Name", "Student ID", "Department", "Year Standing", "Class");
}else{
  @cols = ("姓名", "學號", "系所", "年級", "班別");
}

$HEAD_DATA=$HEAD_DATA."  <table width=800 border=0>\n";
$HEAD_DATA=$HEAD_DATA."  <tr>\n";
$HEAD_DATA=$HEAD_DATA."    <th>" . $cols[0] . ": $P_name</th>\n";
$HEAD_DATA=$HEAD_DATA."    <th>" . $cols[1] . ": $P_id</th>\n";
$HEAD_DATA=$HEAD_DATA."    <th>" . $cols[2] . ": $P_dept</th>\n";
$HEAD_DATA=$HEAD_DATA."    <th>" . $cols[3] . ": $P_grade</th>\n";
$HEAD_DATA=$HEAD_DATA."    <th>" . $cols[4] . ": $P_class</th>\n";
$HEAD_DATA=$HEAD_DATA."    <th><FONT color=RED>*</TH>\n"  if( $SUPERUSER == 1 );
$HEAD_DATA=$HEAD_DATA."  </tr>\n";
$HEAD_DATA=$HEAD_DATA."  </table>\n";

return($HEAD_DATA);
}
##############################################################################
#####  設定學分代碼與名稱的陣列，目前已知 Add_Course01.cgi 和 Selected_View00.cgi 使用。
#####  Updates:
#####    2016/09/23 改為透過 %PROPERTY_TABLE2 重整，不在此函式內部 key。 Nidalap :D~
#####    2016/09/23 還是有問題！緊急回復為舊方法，待後續 DEBUG  Nidalap :D~
sub CREDIT_TABLE
{
  my %table;
  $i=0;
  
  if( $IS_ENGLISH ) {
    foreach $property (sort keys %PROPERTY_TABLE2_E) {
      $Credit[$i++] = $PROPERTY_TABLE2_E{$property};
    }
  }else{
    foreach $property (sort keys %PROPERTY_TABLE2) {
      $Credit[$i++] = $PROPERTY_TABLE2{$property};
    }
  }
  
  my(@Credit);

  if( $IS_ENGLISH ) {
    @Credit = ("Credit Type", "Required", "Elective", "CGE", "Minor", "Double Major", "Undergraduate", "教育學程", "不列入畢業總學分");
  }else{
    @Credit = ("學分歸屬", "必修", "選修", "通識", "輔系", "雙主修", "大學部課程", "教育學程", "不列入畢業總學分");
  }

#  foreach $cre (@Credit) {
#    print "$cre <BR>\n";
#  }
  
  return(@Credit);
}
############################################################################
sub Whats_Sys_State
{
  my($BasicData) = $REFERENCE_PATH."Basic/";
  my($FileName) = $BasicData."SysState";

  my($SysStatus);
  open(STATE,$FileName) or die("Cannot open file $FileName!\n");
  $SysStatus=<STATE>;
  close(STATE);

  return($SysStatus);
}
################################################################################################
#####  Check_Map_Class()
#####  由Check_Time_Map()呼叫, 傳回某個學生的年級
#####  從 class/Main.cgi 移到此, 供加退選程式使用
#####  Updates:
#####     Nov 28,2000 (Nidalap :D~)
#####     2010/09/08  移除 $limit_id 限制，因為現在所有轉學生資料均為當學年轉進來的  Nidalap :D~
################################################################################################
sub Check_Student_Grade
{
  my(%User) = @_;
  my(%change_school_student);
  
#  my $limit_id = $YEAR - 1;
#  $limit_id = "4" . $limit_id;      ###  限制轉學生學號前三碼為 4 . "YEAR-1"
                                    ###  以避免老轉學生, 也被視同新生允許選課. (2006/09/06)
  %change_school_student = Find_Change_School_Student($limit_id);
#  print("limit_id = $limit_id<br>\n");
#  print(" change_school flag = $change_school_student{$User{id}}<BR>\n");
  if( ($change_school_student{$User{id}} == 1) and ($TERM == 1) ) {
    return(1);		      ##  第一學期轉學生視同新生(2001/08/28)
  }
  
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
############################################################################
#####  Read_Time_Map()
#####  讀取所有年級系所可否選課的設定資料
#####  Updates:
#####    2009/09/08 Created  Nidalap :D~
sub Read_Time_Map
{
  my @grades = (1,2,3,4,5,6);
  my $filename, @lines, %time_map, $dept, $time;
  
  foreach $grade (@grades) {
    $filename = $REFERENCE_PATH . "SelectTimeMap/" . $grade . ".map";
    open(TIMEMAP, $filename);
    @lines = <TIMEMAP>;
    close(TIMEMAP);
    foreach $line (@lines) {
      ($dept, $time) = split(/\s+/, $line);
      $time_map{$grade}{$dept} = $time;
    }
  } 
  return(%time_map);
}

############################################################################
#####  Check_Time_Map()
#####  檢查各年級各系所學生是否可以選課
#####  從 class/Main.cgi 移到此, 供加退選程式使用
#####     Step 1: 取得學生的年級
#####     Step 2: 讀取相關的時間設定檔
#####  Update: Nov 29,2000 (Nidalap :D~)
############################################################################
sub Check_Time_Map
{
  my(%user)=@_;
  my($MapClass)=Check_Student_Grade(%user);           ### 取得學生的年級
  my($FileName)=$REFERENCE_PATH."SelectTimeMap/".$MapClass.".map";
  my $Flag = 0;
  my(@Original, %User, $dept, $state, @duration);
  my($time_permission, %TD);

  open(FILE,"<$FileName");
  @Orignal=<FILE>;
  foreach $item(@Orignal){
    ($dept, $state)=split(/\s+/,$item);
    if($dept eq $user{dept}) {
      $time_permission=$state;
    }
  }

  if( $time_permission == 0 ) {      ###    0: 該系所學生不允許選課
                                     ###  暫時加入提早入學生 692...... 的判斷,
                                     ###  本次選課(912)後必須修改此部分 code
                                     ###  2003/02/14 Nidalap :D~
                                     ###  2004/02/13 再度使用 ^^|||
    if($ALLOW_PRE_ENTRANCE_STUDENT_TEMP == 1) {
      if( $user{id} =~ /^693/  ) { 
        ($sec,$min,$hour,$day,$nmonth,$year,$wday,$yday,$isdst) = localtime(time);
        $Value=$min+$hour*100;
        if( ($Value >= 800) and ($Value < 2200) ) {
          return 1;
        }else{
          return 0;
        }
      }else{
        return 0;
      }
    }else{
      return 0;
    }
  }else{                             ###  123: 檢查可選課時段
    $FileName=$REFERENCE_PATH."TimeMap/T".$time_permission.".map";
    open(FILE,"<$FileName");
    my($count)=0;
    @duration=<FILE>;
    close(FILE);
    foreach $item(@duration){
      ($TD[$count]{S},$TD[$count]{E})=split(/\s+/,$item);
      $count++;
    }

    ($sec,$min,$hour,$day,$nmonth,$year,$wday,$yday,$isdst) = localtime(time);
    $Value=$min+$hour*100;           ### T?.map中存放時間的格式為 0800, 1200等
    for($i=0; $i < $count; $i++){
      if( ($Value > int($TD[$i]{S})) && ($Value < int($TD[$i]{E})) ){
          $Flag = 1;
      }
    }
    return($Flag);
  }
}
############################################################################
#####  Check_Course_Upper_Limit_Immune()
#####  檢查該學生是否在該科目的額滿加簽名單內
#####  若是, 則該生不受該科目額滿不得選修的限制
#####  傳回值: (0, 1) = (不在list, 在list)
#####  Date : 2001/09/14
#####  Coder: Nidalap XD~
############################################################################
sub Check_Course_Upper_Limit_Immune
{
  my($course_id, $course_group, $stu_id) = @_;
  my($immune_file, @line);

  $immune_file = $DATA_PATH . "Course_Upper_Limit_Immune/" . $YEAR . "_" . $TERM . "/" .
                 $course_id . "_" . $course_group;
#  print $immune_file;
  if( -e $immune_file ) {
    open(IMMUNE, $immune_file);
    @line = <IMMUNE>;
    close(IMMUNE);
    foreach $line (@line) {
      $line =~ s/\n//;
      return(1)  if( $line eq $stu_id );
    }
  }else{
    return(0);
  }
  return(0);
}
############################################################################
#####  Upper_Limit_Immune_Add() 
#####  有額滿權限的學生加選
#####  若是學生有額滿加簽權限, 他加選時要特別紀錄,
#####  作為其他學生選課時的人數計算參考(限修人數 + 此名單人數)
#####  傳回值: (null)
#####  Date : 2002/09/23
#####  Coder: Nidalap XD~
############################################################################
sub Upper_Limit_Immune_Add
{
  my($course_id, $course_group, $stu_id) = @_;
  my($immune_file, @line);

#  $immune_file = $DATA_PATH . "Course_Upper_Limit_Immune/" . $course_id . "_" .  $course_group . "_add";
  $immune_file = $DATA_PATH . "Course_Upper_Limit_Immune/" . $YEAR . "_" . $TERM . "/" .
                $course_id . "_" . $course_group . "_add";
  if( -e $immune_file ) {
    open(IMMUNE, $immune_file);
    @line = <IMMUNE>;
    close(IMMUNE);
    foreach $line (@line) {
      $line =~ s/\n//;
      return()  if($stu_id eq $line);
    }
  }
  push(@line, $stu_id);
  open(IMMUNE, ">$immune_file");
  foreach $line (@line) {
    print IMMUNE ("$line\n");
  }
  close(IMMUNE);
}
############################################################################
#####  Upper_Limit_Immune_Delete()
#####  有額滿權限的學生退選
#####  若是學生有額滿加簽權限, 他退選時也要取消特別紀錄,
#####  作為其他學生選課時的人數計算參考(限修人數 + 此名單人數)
#####  若退選學生不做這個動作, 有可能造成可加選名額計算錯誤.
#####  傳回值: (null)
#####  Date : 2007/03/08
#####  Coder: Nidalap :D~
############################################################################
#sub Upper_Limit_Immune_Delete()  <--- 移至 Student_Course.pm

############################################################################
#####  Check_Course_Upper_Limit_Immune_Count()
#####  檢查科目的額滿加簽名單(如果有), 傳回加簽人數或已加選的加簽人數
#####  在第二階段選課時, 額外加簽的人數不應佔了名額而影響其他學生的選課權利.
#####  傳回值: $count
#####  Date : 2002/09/23
#####  Coder: Nidalap XD~
############################################################################
sub Check_Course_Upper_Limit_Immune_Count
{
  my($course_id, $course_group, $selected_flag) = @_;
  my($immune_file, @line, $count);

  if( $selected_flag eq "add" ) {       ###  傳回加簽中 "已加選的人數"
#    $immune_file = $DATA_PATH . "Course_Upper_Limit_Immune/" . $course_id . "_" . $course_group . "_add";
    $immune_file = $DATA_PATH . "Course_Upper_Limit_Immune/" . $YEAR . "_" . $TERM . "/" .
                   $course_id . "_" . $course_group . "_add";
  }else{                                ###  傳回加簽人數
#    $immune_file = $DATA_PATH . "Course_Upper_Limit_Immune/" . $course_id . "_" . $course_group;
    $immune_file = $DATA_PATH . "Course_Upper_Limit_Immune/" . $YEAR . "_" . $TERM . "/" .
                   $course_id . "_" . $course_group;
  }
  if( -e $immune_file ) {
    open(IMMUNE, $immune_file);
    @line = <IMMUNE>;
    close(IMMUNE);
    $count = @line;
  }else{
    return(-1);
  }
  return($count);
}

############################################################################
#####   非選課時段顯示的選課畫面
#####   從Main.cgi移到此(Nidalap, Jan13,1999)
############################################################################
sub Enter_Menu_Sys_State_Forbidden
{
  my($HEAD_DATA)=@_;
  my @txt;
  if( $IS_ENGLISH ) {
    @txt = ("CCU Course Selection System", "System Not Available for Course Selection.
	         For more information, please refer to system announcement.");
  }else{
    @txt = ("國立中正大學選課系統", "系統暫時關閉，系統開放及關閉時間請參閱選課系統公告");
  }
  print '
    <html>
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <title>' . $txt[0] . '</title>
    </head>
    <body background="$GRAPH_URL./ccu-sbg.jpg">
    <center>
      ' . $HEAD_DATA . '
      <HR>
      <font size=3>' . $txt[1] . '</font>
    </center>
    </body>
    </html>
  ';
  exit(1);
}

