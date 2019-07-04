#!/usr/local/bin/perl
########################################################################################
#####  Selected_View00.cgi
#####  檢視已選修科目
#####  Updates: 
#####    2002/05/07  加入 75/50 分鐘並行制, 修改功課表, code refinement
#####    2008/09/03  加入課程大綱連結
#####    2010/01/04  將 $yearterm 改為 $year, $term 以避免民國百年 bug  Nidalap :D~
#####    2010/08/10  全英語授課課程要顯示註解.  Nidalap :D~
#####    2012/02/29  教師查詢功能不受系統不允許查詢的限制  Nidalap :D~
#####    2012/04/25  依照 Student_warning/ 資料，顯示「篩選狀態」欄位  Nidalap :D~
#####    2012/12/19  新學期開課期間，教專系統查詢一律給予「上學期」資料 Nidalap :D~
#####    2013/04/15  加入「申請棄選」按鍵功能（只有在設定時間內出現）  Nidalap :D~
#####    2013/07/25  英文版相關增修：將顯示文字拉到 Init_Text_Values() 中設定。 Nidalap :D~
#####    2013/10/02  新增新版本驗證碼 key 以避免使用者隨便看任何學生的資料 Nidalap :D~
#####    2014/09/18  篩選狀態改由「上次」篩選後選課資料 Student_last/* 判斷，以避免誤判。  Nidalap :D~
#####    2015/12/31  抓取「上學期」開課資料的判斷，改為課程異動前一律抓取之。  Nidalap :D~
########################################################################################
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
require $LIBRARY_PATH."English.pm";

print("Content-type:text/html\n\n");
print $EXPIRE_META_TAG;

$online_help = Online_Help();
%system_settings = Read_System_Settings();

#foreach $k (keys %system_settings) {
#  print "$k : $system_settings{$k}<BR>\n";
#}

%Input = User_Input();

#Print_Hash(%Input);

if( $Input{session_id} eq "" ) {			###  如果是從別的系統連過來的
  $id = $Input{id};
  $teacher_login_flag = 1;
  $in_key			= $Input{key};
  $in_timestamp	= $Input{key1};
  
  $key = Generate_Key2($id, "bOsSlesSLESswORK", $in_timestamp);
  if( (Check_HTTP_REFERER() != 1) or ($key ne $in_key) ) {			###  檢查來源
    Show_Password_Error_Message();
  }
}else{							###  一般情況: 系統內部連結來的
  ($id, $Input{password}, $login_time, $ip) = Read_Session($Input{session_id}, "", 1);
  Check_Student_Password($id, $Input{password});
}

#####  新學期開課期間，教專/SSO 系統查詢一律給予「上學期」資料  2012/12/19 Nidalap :D~
#####  2015/12/31 改為異動前一律給「上學期」資料  Nidalap :D~
if( ($system_settings{"current_system_timeline"} <= 2) and ($teacher_login_flag==1) ) {
  ($year, $term) = Last_Semester(1);
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

%txt = Init_Text_Values();

#print("session_id, id, pass = $Input{session_id}, $id, $Input{password}<BR>"); 

############################################################################

my(%Student,%Dept);

%Student=Read_Student($id);
if( $Student{name} eq "" ) {
  print "<CENTER><H1>" . $txt{'no_stu_rec'} . "<BR>";
  exit();
}

%Dept=Read_Dept($Student{dept});
@MyCourse=Course_of_Student($Student{id}, $year, $term);

if( $IS_ENGLISH ) {
  $HEAD_DATA = Head_of_Individual($Student{ename},$Student{id},$Dept{ename},$Student{grade},$Student{class});
}else{
  $HEAD_DATA = Head_of_Individual($Student{name},$Student{id},$Dept{cname},$Student{grade},$Student{class});
}

###################    若非選課時間則顯示不可進入  ################
if($SUPERUSER != 1){			### 非 superuser 的使用者
#  if( (Whats_Sys_State()==0)or(Check_Time_Map(%Student)!=1) ){
  if( $teacher_login_flag != 1 ) {		### 非教專系統登入
    if( Whats_Sys_State()==0 ) {
      Enter_Menu_Sys_State_Forbidden($HEAD_DATA);
    }
  }
}
###################################################################
my($Table_Data)=CREAT_COURSE_TABLE();
#my($COURSE_TIME_TABLE) = Create_Course_Time_Table();
#my($BOARD_TEXT) = Read_Board();

Student_Log("View  ", $id, "", "", "");

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
  my $show_help = Show_Online_Help('SELECTED_VIEW');

  print 
    $online_help .
    '<head>
      ' . $EXPIRE_META_TAG . '
      <TITLE>' . $txt{'sys_title'} . '</TITLE>
    </head>
    <body background="' . $GRAPH_URL . '/ccu-sbg.jpg" ' . $reload_tag . '> 
    <center>
      ' . $HEAD_DATA . '
      <hr>
      <br>
  ';
  
  #print "<B><FONT color=RED>第一階段選課篩選為限修人數篩選，先修篩選及重複修習篩選將於本學期成績到齊後執行。</FONT></B><P>";

  Warn_of_Course_Conflict();

#  print("enrollnum = " . $Student{'enrollnum'} . "<BR>\n");
#  print("grade = " . $Student{'grade'} . "<BR>\n");
  
  #####  判斷是否低於學分下限, 顯示短修警訊 (2008/11/14 Nidalap :D~)
  $lower_credit_limit = Lower_Credit_Limit(%Student);
  if( $CreditSum < $lower_credit_limit ) {
    print '<FONT color=RED><B>' . $txt{'limit1'} . $CreditSum . $txt{'limit2'} . $lower_credit_limit . $txt{'limit3'} . '</B></FONT>';
    $temp_help = Show_Online_Help("LOWER_CREDIT_LIMIT");
    print("$temp_help</B></FONT><P>\n");
  }

#  print qq(
#    <BUTTON onClick="window.location.reload()">REFRESH</BUTTON>
#  );
  
  if( $system_settings{'limit_number_state'} == 0 ) {
    $course_status_ps = '
      <TD align=left><FONT size=-1>
        ' . $txt{'choose1'} . '
          <IMG src="../../Graph/O.gif" width=16>:' . $txt{'choose2'} . '&nbsp;&nbsp;&nbsp;&nbsp;
          <IMG src="../../Graph/Q.gif" width=16>:' . $txt{'choose3'} . '&nbsp;&nbsp;&nbsp;&nbsp;
          <B>免</B>： ' . $txt{'choose4'} . '
      </TD>
    ';
  }    
  
  print '
      <font size=4><b>' . $txt{'title'} . '</b></font>' .
      $show_help .
      $DATA .
      '<table border=0 width=90%>
      <tr>'
        . $course_status_ps . 
        '<th align=right><font size=2>' . $txt{'total1'} . '<u> <SPAN id="total_course">' . $MyCount . '</SPAN> </u>' . $txt{'total2'} . '
		                             <u> <SPAN id="total_credit">' . $CreditSum . '</SPAN> </u>' . $txt{'total3'} . '</font></th>
      </tr>
      </table>
      <P>
  ';
  Create_Course_Time_Table();
#  Warn_of_Course_Conflict();
  print "
    </center>
        $BOARD_TEXT
    <FONT color=RED>
      " . $txt{'note'} . "
    </FONT>

    </body>
    $EXPIRE_META_TAG2
    </html>
  ";
}
######################################################################
sub CREAT_COURSE_TABLE
{
my($DATA)="";
my(@Teachers)=Read_Teacher_File();
my @WeekDay;
if( $IS_ENGLISH ) {
  @WeekDay = @WEEKDAY_E;
}else{
  @WeekDay = @WEEKDAY;
}
my @TimeMap = @TIMEMAP;
%system_flags = Read_System_Settings();
%course_status = Find_Course_Last_Choose_Status($id);	###  科目「上次」限修篩選成功與否

my($withdrawal_form_allowed, $wf_msg)	= Apply_Form_Allowed("withdrawal");		### 目前是否允許申請棄選

#print "withdrawal form allowed = $withdrawal_form_allowed, $wf_msg<BR>\n";

$CreditSum=0;
$MyCount=@MyCourse;
@Credit=CREDIT_TABLE();

  $DATA = $DATA."<table width=90% border=1 cellspacing=0 cellpadding=3>\n";
  $DATA = $DATA."<tr>\n";
  
  if( ($withdrawal_form_allowed == 1) and !$IS_MOBILE ) {			###  目前可加簽且非行動版，才顯示申請加簽選項
    $DATA = $DATA."  <th bgcolor=yellow><font size=2>" . $txt{'withdrawal'} . "</font></th>\n";
  }
  if( $system_settings{'limit_number_state'} == 0 ) {
    $DATA = $DATA."  <th bgcolor=yellow><font size=2>" . $txt{'choosestatus'} . "</font></th>\n";
  }
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>" . $txt{'cid'} . "</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>" . $txt{'group'} . "</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>" . $txt{'cname'} . "</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>" . $txt{'teacher'} . "</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>" . $txt{'credit'} . "</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>" . $txt{'property'} . "</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>" . $txt{'weekday'} . "</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>" . $txt{'classroom'} . "</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>" . $txt{'syllabus'} . "</font></th>\n";  
  $DATA = $DATA."</tr>\n";

  ####  列印相關課程資料  ####
  
  #print "MyCount = $MyCount<BR>\n";
  
  for($i=0; $i < $MyCount; $i++){
  
      my(%theCourse)=Read_Course($MyCourse[$i]{dept},$MyCourse[$i]{id},$MyCourse[$i]{group},$year, $term);
      $CreditSum += $theCourse{credit};
      $DATA = $DATA."<tr>\n";
	  
	  #print "[i, MyCount] = [$i, $MyCount]<BR>\n";
	  
	  #print "theCourse :<BR>\n";
	  #Print_Hash(%theCourse);
	  #print "cccccccccccccccccc<HR>\n";

	  if( ($withdrawal_form_allowed == 1) and !$IS_MOBILE ) {			###  目前可加簽且非行動版，才顯示申請加簽選項
	    $DATA = $DATA."<th><font size=2>";
        $DATA = $DATA."<A href='Withdrawal_Form_Apply1.php?session_id=" 
                    . $Input{session_id} . "&dept=" . $theCourse{dept} 
					. "&cid=" . $theCourse{id} . "&grp=" . $theCourse{group}
					. "&e=" . $IS_ENGLISH
					. "'>" . $txt{'withdrawal'} . "</A>";			## 科目篩選狀態
        $DATA = $DATA."</font></th>\n";
	  }
      if( $system_settings{'limit_number_state'} == 0 ) {	## 只有在系統還要篩選時，才顯示篩選狀態
        if( $theCourse{number_limit} > 0 ) {
          $status = $course_status{$theCourse{id}}{$theCourse{group}};
          if( ($status ne "0") and ($status ne "") ) {		## [0, ""] = [上次沒過, 不曾選過]
            $course_status_text = "<IMG src='../../Graph/O.gif' width=16 title='已於 " . $status . "通過'>";
          }else{
            $course_status_text = "<IMG src='../../Graph/Q.gif' width=16 title='尚未通過'>";
          }
        }else{
          $course_status_text = "免";
        }
        $DATA = $DATA."<th><font size=2>";
        $DATA = $DATA.$course_status_text;			## 科目篩選狀態
        $DATA = $DATA."</font></th>\n";
      } 
      $DATA = $DATA."<th><font size=2>";
      $DATA = $DATA.$theCourse{id};				##  科目代碼
      $DATA = $DATA."</font></th>\n";
      $DATA = $DATA."<th><font size=2>";
      $DATA = $DATA.$theCourse{group}."</font></th>\n";		##  班別

      $DATA = $DATA."<th><font size=2>";
      
	  if( $IS_ENGLISH ) {
	    $DATA = $DATA.$theCourse{ename};			    ##  科目名稱(英文)
	  }else{
	    $DATA = $DATA.$theCourse{cname};			    ##  科目名稱
	  }
      if( $theCourse{english_teaching} ) {
        $DATA .= "<BR><FONT color=RED>(全英語授課/English-Taught Course)";
      }
      $DATA = $DATA."</font></th>\n";

	  #print "[b: i, MyCount] = [$i, $MyCount]<BR>\n";

      $DATA=$DATA."<th><font size=2>";           ##  授課教師
      $T=@{$theCourse{teacher}};
      for($teacher=0; $teacher < $T; $teacher++){
        if($theCourse{teacher}[$teacher] != 99999){
          $DATA=$DATA.$Teacher_Name{$theCourse{teacher}[$teacher]};
        }else{
          $DATA=$DATA . $txt{'no_teacher'};
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

	  #print "[c: i, MyCount] = [$i, $MyCount]<BR>\n";
	  
      $DATA=$DATA."<th><font size=2>";           ## 星期節次
      $time_string = Format_Time_String($theCourse{time});
      $DATA .= $time_string;
      $DATA=$DATA."</font></th>\n";

	  #print "[e: i, MyCount] = [$i, $MyCount]<BR>\n";
	  
      $DATA=$DATA."<th><font size=2>";           ##  教室
      %Room=Read_Classroom($theCourse{classroom});
	  
	  #print "[f: i, MyCount] = [$i, $MyCount]<BR>\n";
	  
      $DATA=$DATA.$Room{name};
      $DATA=$DATA."</font></th>\n";

	  #print "[d: i, MyCount] = [$i, $MyCount]<BR>\n";
	  
	  ###  課程大綱 Added 20080805 Nidalap :D~
	  if( $system_flags{"redirect_to_query"} == 1 ) {		###  如果目前系統正在開下學期的課，連至「上學期」的大綱 20150515
	    ($y,$t) = Last_Semester(1);
	  }else{
	    $y = $YEAR; $t = $TERM;
	  }
     
      $DATA=$DATA."<th><font size=2>";
      $DATA=$DATA."<A href=\"".$ECOURSE_QUERY_COURSE_URL."&courseno=".$theCourse{id}
        ."_".$theCourse{group}."&year=".$y."&term=".$t."\" target=NEW>"
        . $txt{'link'} . "</A>";
      $DATA=$DATA."</font></th>\n";

      $DATA = $DATA."</tr>\n";
	  
	  #print "[i, MyCount] = [$i, $MyCount]<BR>\n";
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
      if( $IS_ENGLISH ) {
	    $selected_time[$i]{course} = $the_Course{ename};
	  }else{
	    $selected_time[$i]{course} = $the_Course{cname};
	  }
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
      $conflict_string .=" 與 (星期$WEEKDAY[$week]的第 $time 堂).<BR>";
      $conflict_string .="請優先排除衝堂，再行加退選！</B></U></FONT>";
      $conflict_string .= Show_Online_Help("COURSE_CONFLICT");
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
#############################################################################################
#####  讀取學生上次篩選後的選課紀錄檔
#####  傳回值：%course_status = 該生各科目篩選成功與否 [否，是] = [0,1]
#####  原本抓取 Student_warning/ 篩選紀錄檔判斷，但若學生曾自行退選後來又再加回來，
#####  此處會誤判以為已經通過篩選(實際上已經放棄優先權)。故修正改抓 Student_last/   2014/09/18 Nidalap :D~

sub Find_Course_Last_Choose_Status
{
  my ($id) = @_;
  my $update_time, $j, @j, $cid, $group, $status;
  my $dev,$ino,$mode,$nlink,$uid,$gid,$rdev,$size,$atime,$mtime,$ctime,$blksize,$blocks;
  my $mday_tmp,$month_tmp,$year_tmp;
  
  my @cour_last = Course_of_Student($id, "last");
  foreach $cour (@cour_last) {
    $course_status{$$cour{id}}{$$cour{group}} = 1;
  }
  
  return %course_status;
}
##################################################################################
#####  因應英文版本，將所有要顯示的文字在此整理，依照 $IS_ENGLISH 自動判別  2013/07/25
sub Init_Text_Values
{
  my %txtall;
  
  %txtall = (
    'no_stu_rec'=> {'c'=>'查無此學生資料!', 'e'=>'Cannot find your record!'},
	'view'		=> {'c'=>'檢視已選修科目', 'e'=>'Preview Courses Selected'},
	'sys_title'	=> {'c'=>'國立中正大學' . $SUB_SYSTEM_NAME . '選課系統', 'e'=>'CCU Course Selection System'},

	'limit1'	=> {'c'=>'您目前共選修 ', 'e'=>'You have chosen '},
	'limit2'	=> {'c'=>' 學分，尚未達本學期的學分下限', 
					'e'=>' credits, which is still less than the lower limit.'},
	'limit3'	=> {'c'=>' 學分。已送短修請單之同學，注意系統所選學分數≧申請後之修課下限，系統上之短修顯示可略過。', 
					'e'=>' credits.'},
	
	'title'		=> {'c'=>$year . '學年度第' . $TERM_NAME[$term] . '學期選修科目', 
					'e'=>'Course Selection List of ' . Year_Term_English()},

	'withdrawal'=> {'c'=>'申請棄選', 'e'=>'Apply for withdrawal'},
	'choosestatus' => {'c'=>'篩選狀態', 'e'=>'Screening Status:'},
	'cid'		=> {'c'=>'科目代碼', 'e'=>'Course ID'},
	'group'		=> {'c'=>'班別', 'e'=>'Class'},
	'cname'		=> {'c'=>'科目名稱', 'e'=>'Course Title'},
	'teacher'	=> {'c'=>'授課教師', 'e'=>'Instructor'},
	'no_teacher'=> {'c'=>'教師未定', 'e'=>'Undetermined'},
	'credit'	=> {'c'=>'學分', 'e'=>'Credit'},
    'property'	=> {'c'=>'學分歸屬', 'e'=>'Credit Type'},
    'weekday'	=> {'c'=>'星期節次', 'e'=>'Day/Period'},
    'classroom'	=> {'c'=>'教室', 'e'=>'Class Location'},
	'syllabus'	=> {'c'=>'大綱', 'e'=>'Syllabus'},
	'total1'	=> {'c'=>'共修習', 'e'=>'You have selected'},
	'total2'	=> {'c'=>'科', 'e'=>'courses and'},
	'total3'	=> {'c'=>'學分', 'e'=>'credits in total.'},
	'link'		=> {'c'=>'連結', 'e'=>'link'},
	
	'choose1'	=> {'c'=>'篩選狀態說明', 'e'=>'Notes about Screening Status:'},
	'choose2'	=> {'c'=>'已通過限修人數篩選', 'e'=>'Courses Already Passing Screening'},
	'choose3'	=> {'c'=>'尚未經過限修人數篩選', 'e'=>'Courses Subject to Further Screening'},
	'choose4'	=> {'c'=>'此科目不必篩選', 'e'=>'Courses not subject to Screening'},
	'note'		=> {'c'=>'本單僅供同學自行參考, 非正式選課單. 欲列印選課單請到主選單選擇"列印選課單"選項. 謝謝!', 
	                'e'=>'This page is for reference only. For a formal course selection list, ' 
					   . 'please go to the main menu and click "Print Courses Selected".'},
	
	'a'		=> {'c'=>'a', 'e'=>'a'}
  );

  foreach $k (keys %txtall) {
	if( $IS_ENGLISH ) {
	  $txt{$k} = $txtall{$k}{'e'};
	}else{
	  $txt{$k} = $txtall{$k}{'c'};
	}
  }
 
  return %txt;  
}
