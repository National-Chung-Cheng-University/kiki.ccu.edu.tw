#!/usr/local/bin/perl
###########################################################################################
#####  Add_Course_01.cgi
#####  處理學生加選資料
#####  接收 Add_Course_00.cgi 傳來的資料, 判斷學生選課資料合法性
#####  (密碼, 擋修, 限修人數 etc), 決定是否加選及顯示開課資料網頁
#####  Coder   : Nidalap :D~
#####  Modified: Jan 10/2001
#####            2008/06/03  增加跨領域學程功能, 轉向到 Show_All_GRO.cgi	Nidalap :D~
#####		 2008/08/05  增加連結前往 Ecourse 課程大綱			Nidalap :D~
#####		 2008/09/01  體育課程相關增修, 詳見 CHECK_VALID_SELECT_COURSE() Nidalap :D~
###########################################################################################
print("Content-type: text/html\n\n");

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

my(%Student,%Dept);
%time = gettime();

###################    讀取使用者輸入資料    ######################
%system_flags = Read_System_Settings();
%Input=User_Input();
($Input{id}, $Input{password}, $login_time, $ip, $add_course_count) = Read_Session($Input{session_id}, 1);
#print("session_id, id, pass = $Input{session_id}, $Input{id}, $Input{password}<BR>"); 

#if( length($Input{dept}) == 2 ) {		###  跨領域學程
#  print qq (Location: Show_All_GRO.cgi?gro_id=$Input{dept} );  
#}else{
#  print("Content-type: text/html\n\n");
#}

%Student=Read_Student($Input{id});
%Dept=Read_Dept($Student{dept});
%SelectDept=Read_Dept($Input{dept});

Check_Student_Password($Input{id}, $Input{password});
my($HEAD_DATA)=Head_of_Individual($Student{name},$Student{id},$Dept{cname},$Student{grade},$Student{class});

if($add_course_count >= $ADD_COURSE_LIMIT) {
  Session_Add_Course_Limit($system_flags{black_list}, $time{time_string}, $Input{id}, $ip);
}
$add_course_count ++  if($Input{SelectTag} == 1);
Write_Session($Input{session_id}, $Input{id}, $Input{password}, $add_course_count);

###################    若非選課時間則顯示不可進入  ################
if($SUPERUSER != 1){     ## 非 superuser 的使用者
  if( (Whats_Sys_State()==0)or(Whats_Sys_State()==1)or(Check_Time_Map(%Student)!=1) ){
    Enter_Menu_Sys_State_Forbidden($HEAD_DATA);
  }
}
###################    限定不可使用GET, 一律用POST  ###################
#if( $ENV{REQUEST_METHOD} ne "POST" ) {
#  Enter_Menu_Sys_State_Forbidden($HEAD_DATA);
#}
#######################################################################
########    判斷使用者是否為研究所以上學生    ########
########    如果是，則年級一律為一年級        ########
########    應課務組需求將此條件限制去除      ########
#if($Input{dept}%10 > 4){
#    $Input{grade}=1;
#}
###########################################################################
####    宣告全域變數 (Golobal Variable)    ####
my($ERROR_DATA_1)="";                  ##紀錄衝堂檢查時發生衝堂的科目訊息

my($Current_Page)=$Input{page};
my($TotalPages)=0;
Read_Student_State_Files();            ### 讀取輔系雙主修名單->全域變數 %FU,%DOUBLE

if( ($Input{dept} eq "6104") or ($Input{dept} eq "6154") or
    ($Input{dept} eq "6204") ) {
                                                ### 如果開課系所是法律系任一組
  if( ($FU{$Student{id}} eq "6054") or ($FU{$Student{id}} eq "3254") ) {
                                                ### 且學生是法律系輔系生  
    $FU{$Student{id}} = $Input{dept};           ### 則視同是該組的輔系生
  }
}
if( $Input{dept} =~ /^5/ ) {          ###  如果開課系所是管院的     
  if( $FU{$Student{id}} =~ /^5/ ) {   ###  如果學生是管院任一系的輔系生
    $FU{$Student{id}} = $Input{dept}; ###  則視同是該組的輔系生(管院課程整合)
  }
  if( $DOUBLE{$Student{id}} =~ /^5/ ) {   ###  如果學生是管院任一系的雙主修生
    $DOUBLE{$Student{id}} = $Input{dept}; ###  則視同是該組的雙主修生(管院課程整合)
  }
}

############################################################################

####    學生年級是否需要自動升級之判斷    ####
####    使用時機：次一學年開始前使用      ####
if( is_Grade_Update() == 1){
  $Student{grade}++;
  $Student{grade}=4  if( $Student{grade} > 4 );  ### 2004/06/07發現BUG更新
}

####    建立 HTML 檔案的表頭部分    ####
####    包括使用者的身份資料等      ####

#############################################################################
####    本程式的核心請由此處著手往下看各個相關的函式                     ####
#############################################################################
########    判斷是否需要處理選課資料    ########

if($system_flags{black_list} == 1) {
  $ban_time = Read_Ban_Record($Student{id}, $BAN_COUNT_LIMIT);	### 停權尚須多久恢復(大於0就是停權中)
  if( $ban_time > 0 ) {
    Show_Ban_Message($ban_time, 1);
  }
}
if($Input{SelectTag} == 0 or not defined $Input{SelectTag}){
    $Current_Page++;      ####    讀取下一頁    ####
    VIEW_COURSE();
}else{                    ####    先處理選課程序，再讀取選課後資料    ####
    SELECT_COURSE($HEAD_DATA,$Input{dept},$Input{course});
    VIEW_COURSE();
}
#############################################################################
#############################################################################
#####  SELECT_COURSE()
#####  若學生有選課(Input{SelectTag}有設定), 先處理選課資料
#####  先判斷選課資料的合法性, 再進行選課或回報錯誤訊息.
#####  更新: 將判斷合法性的程式放在同一迴圈內, 以減少多次呼叫Read_Course()
#####        造成的多餘IO減慢速度 (Nidalap, Jan10/2001)
#############################################################################
sub SELECT_COURSE
{
  my($HEAD_DATA, $course_stream);
  ($HEAD_DATA,$course_dept,$course_stream)=@_;
  @Courses=split(/\*:::\*/,$course_stream);
  my(@Courses_Data, $valid_flag, $valid_string);
  my($count)=0;

  ($valid_flag, $valid_string) = CHECK_VALID_SELECT_COURSE(@Courses);
  if($valid_flag == 0) {                                        ### 若選課資料不合法
    REPORT_ERROR($valid_string);
  }else{                        		                ### 若選課資料合法                                
    foreach $course(@Courses){
      my($id,$group)=split(/_/,$course);
      %the_Course=Read_Course($course_dept,$id,$group,"",$Input{id});
                                          ## 學生選的課有某一門有先修條件, 將於網頁上顯示警訊
      if( $pre_course_count == 0 ) {
         $pre_course_count = @{$the_Course{prerequisite_course}};
         if($the_Course{prerequisite_course}[0]{dept} eq "99999") {
           $pre_course_count = 0;
         }
      }
      Add_Student_Course($Input{id},$course_dept,$id,$group,$Input{$course});
#      $add_course_count ++;
#      Write_Session($Input{session_id}, $Input{id}, $Input{password}, $add_course_count);
    }
  }
}
###########################################################################################
#####  CHECK_VALID_SELECT_COURSE
#####  判斷選課資料合法性
#####  原先有數個檢查函式, 但每個都會再讀數次Read_Course()造成程式慢, 
#####  所以將數個檢查改做在一起, 減少IO增進速度效能
#####  檢查的項目有:
#####     a. 科目衝堂	: 不可選
#####     b. 屬性有誤	: 不可選
#####     c. 擋修	: 除管理者外不可選
#####     d. 超過25學分	: 除管理者外不可選
#####     e. 限修人數	: 視系統限修條件(管理者不在此限)
#####     f. 專班不得選外所 : 包括專班及專班暑修(管理者不在此限)
#####     g. 通識中心不開放大四(視管理選單設定而定)
#####     h. 依照管理者設定開放或不開放數學系的課和非數學系的課
#####     i. 每學期僅限修一門必修體育(2008/09/01)
#####     j. 體育課可下修不可上修(跨年級)
#####  輸入: (@Courses)                     ## 學生點選要修的科目
#####  輸出: ($valid_flag, $valid_string)   ## $valid_flag:(0,1) = (不合法, 合法)
#####  Jan10/2001改寫(Nidalap:D~)
###########################################################################################
sub CHECK_VALID_SELECT_COURSE
{
  my($id, $group, %The_Course);
  my($conflict_flag, $property_flag, $ban_flag, $credit_25_limit_flag, $number_limit_flag);
  local($conflict_string, $valid_string);
  local $total_credit = 0;
  local $valid_flag = 1;                                               ###  預設選課資料為合法
  local(@time_map);            ###  用做檢查衝堂的陣列, Check_Course_Conflict()會更動之
  local(@Course_of_Student);   ###  用做檢查衝堂及25學分上限, 學生早已選修的科目
  my(@Courses) = @_;
  
  ####################  檢查學生早已修習的課, 建立@time_map及記算學分  ####################
  @Course_of_Student = Course_of_Student($Student{id});
  foreach $stu_course (@Course_of_Student) {
    %The_Course = Read_Course($$stu_course{dept}, $$stu_course{id}, $$stu_course{group}, "", $Student{id});
    $total_credit += $The_Course{credit};
    my $course_identifier = join("_", $$stu_course{dept}, $$stu_course{id}, $$stu_course{group});
    ($conflict_flag, $conflict_string) = Check_Course_Conflict(%The_Course);
    if( $conflict_flag == 1 ) {
      return("0", $conflict_string);
    };
  }
  #######################  處理學生目前所選的課, 檢查合法性  #######################
  foreach $course (@Courses) {
    ($id, $group) = split(/_/, $course);
    %The_Course = Read_Course($course_dept, $id, $group, "", $Student{id});
    ################  檢查學生目前所選的課, 建立@time_map及記算學分 ################
    ($conflict_flag, $conflict_string) = Check_Course_Conflict(%The_Course);
    if( $conflict_flag == 1 ) {
      return("0", $conflict_string);
    };
    ################  檢查學分歸屬是否有選  ################################################
    ################  ps. 可選的欄位在Show_Property_Select已設好了, 在此應不會有選錯情形  ############
    $property_flag = Check_Property($The_Course{property}, $Input{$course});
    if($property_flag != 99) {
      return("0", "您選的科目未正確選取學分歸屬");
    }
    ####################################################################################
    $ban_flag = Check_Ban_Limit(%The_Course);
    if( $ban_flag == 1 ) {
      return("0", "您所選的科目<FONT color=RED>有擋修</FONT>, 以致於您無法加選");
    }
    ####################################################################################
    $credit_25_limit_flag = Check_Credit_Upper_Limit($Student{id}, $total_credit, $The_Course{credit});
    if( $credit_25_limit_flag == 0 ) {
      return("0", "您所選的科目<FONT color=RED>學分數已經過多</FONT>");
    }else{
      if( ($total_credit + $The_Course{credit} > 25) and ($SUPERUSER == 1) ) {
        print("<FONT color=RED>NOTE: 您選的學分數已經超過25學分!</FONT><BR>");
      }
      $total_credit += $The_Course{credit};     ####  若學生一次選多門課學分要重複累加
    }
    ####################################################################################
    $number_limit_flag = Check_Number_Limit($Student{id}, %The_Course);
    if( $number_limit_flag == 0 ) {
      return("0", "您選的科目<FONT color=RED>目前選課人數已滿,</FONT>");
    }
    ####################################################################################
    ####  2003/09/09 暫時修改!
#    if( ($The_Course{id} eq "7102001") and ($The_Course{group} eq "02") ) {
#      return("0", "本科目即將取消, 請勿選修本科目");
#    }
    
  }
  #################################################################################
  if( $SUPERUSER != 1 ) {
    if( ($SUB_SYSTEM==3) or ($SUB_SYSTEM==4) ) {      ### 專班及專班暑修, 不得選外所
      if($Student{dept} ne $Input{dept}) {
        return("0", "專班同學請勿修習外所課程!");
      }
    }
  }
  ######################################################################################
  if( $SUPERUSER != 1 ) {
    if( $Input{dept} eq "7006" ) {
      if( $system_flags{cge_ban_grade} == 1 ) {
        if( $Student{grade} == 4 ) {
          return("0", "第一階段通識課程不開放大四生修習!");
        }
      }elsif( $system_flags{cge_ban_grade} == 2 ) {
        if( ($Student{grade} == 3) or ($Student{grade} == 4) ) {
          return("0", "第一階段通識課程不開放大四生修習!");
        }
      }
    }
  }
  ######################################################################################
  if( $SUPERUSER != 1 ) {
    if( ($system_flags{allow_select_math} == 1) and (is_Math_Dept($Input{dept})) ) {
      return("0", "目前系統不開放選修數學系所開設之科目, 請於開放期間選課!");
    }elsif( ($system_flags{allow_select_math} == 2) and (not is_Math_Dept($Input{dept})) ) {
      return("0", "目前系統不開放選修非數學系所開設之科目, 請於開放期間選課!");
    }
  }
  ######################################################################################
  ###  教育學程開設科目, 只有擁有教育學程資格者可以修習(Added 2003/09/09, Nidalap :D~)
  if($SUPERUSER != 1) {
    if( ($Input{dept} eq "7306") or ($Input{dept} eq "3546") ) {
      my($is_teacher_edu);
      $is_teacher_edu = is_Teacher_Edu($Student{id});
      ###  為配合舊規定, 教育系所高年級以上的也可修教育學程所開設課程
      ###  2004/06 取消此規定, 僅教育學程學生可選修之 :D~
#      if( $Student{dept} =~ /^7/ )  {
#        if( ($YEAR - $Student{grade}) <= 90 )  {    ###  92_1 時, 二年級以上的教育學院學生
#          $is_teacher_edu = 1;
#        }
#      }
      
      if($is_teacher_edu != 1) {
        return("0", "教育學程開設科目, 限擁有教育學程資格者修習!");
      }
    }
  }
  ######################################################################################
  ###  體育課相關限制  (Added 2008/09/01, Nidalap :D~)
  ###  1. 每學期僅限修一門必修體育
  if($SUPERUSER != 1) {
    if( $The_Course{id} =~ /^902(1|2)/ ) {		### 9021, 9022 分別是給一年級, 二年級的
      foreach $stu_course (@Course_of_Student) {
        if( $$stu_course{id} =~ /^902(1|2)/ ) { 
          return("0", "每一學期僅限修一門必修體育課程!");
        }
      }
    }
    ###  2. 體育課可下修不可上修(跨年級) 
    if( $The_Course{id} =~ /^902(.)/ ) {		### 科目代碼第四碼, 拿來與年級相比較
      if( ($Student{grade} < $1) and ($Student{id} =~ /^4/) ) {
        return("0", "體育課程可下修, 但不可上修!");
      }
    }
    
  }    

  ######################################################################################
  ### 開給大一的軍訓課不准研究生選限制(Added 2004/06/07, Nidalap :D~)
  ### 本規定已取消(2006/04/18, Nidalap :D~)
  #if( $id =~ /^9031/ ) {
  #  if( $Student{id} !~ /^4/ ) {
  #    return("0", "研究所同學請勿選修開設給大一的軍訓課程!");
  #  }
  #  elsif( $Student{grade} == 2 ) {    
  #    return("0", "大二同學請勿選修開設給大一的軍訓課程");        
  #  }   
  #}
  #if( $id =~ /^9032/ ) {
  #  if( ($Student{id} =~ /^4/) and ($Student{grade} == 1) ) {
  #    return("0", "大一同學請勿選修開設給大二的軍訓課程");
  #  }
  #}
  
  return($valid_flag, $valid_string);      ###  檢查合法傳回值
}

############################################################################################
#####  Check_Course_Conflict
#####  檢查科目衝堂
#####  檢查每個科目的時段, 將時段加入@time_map陣列, 如果陣列中已有值則判斷衝堂.
#####  先檢查已修習的科目, 是否已經有衝堂情形(可能因為科目異動),
#####  再檢查學生所選的科目.
#####  輸入	    : %The_Course
#####  輸出	    : ($conflict_flag, $conflict_string)   $conflict_flag:(0,1)=(不衝, 衝堂)
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
#####  輸出	    : ($conflict_flag, $conflict_string)          $flag:(0,1) = (不衝, 衝堂)
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

#  if( $time_map{$week}{$time} eq "" ) {                              ### 如果該時段是空的
#    $time_map{$week}{$time} = $course_identifier;
#    return(0, "");
#  }else{                                                             ### 如果該時段已被用
#    $conflict_string = "您所選的科目或原先已選科目在<BR><FONT color=RED>星期 $week 的第 $TIMEMAP[$time] 堂</FONT>有衝堂情形.";
#    return(1, $conflict_string);
#  }
}
############################################################################################
#####  Check_Ban_Limit
#####  檢查擋修系所年級班別
#####  檢查學生選修的科目, 是否有限定擋修系所年級班別. 如果有, 判斷該生身份,
#####  判斷是否可選修. (管理者不在此限)
#####  只要系所年級班別任一項有擋, 其他沒選的視同全部選. 三者以AND連結
#####  輸入	 : %The_Course
#####  輸出	 : $ban_flag                       $ban_flag:(0,1) = (不擋, 擋修)
#####  用到global: %Student
############################################################################################
sub Check_Ban_Limit()
{
  my($Ban_Dept_Num, $Ban_Grade_Num, $Ban_Class_Num);
  my($L1, $L2, $L3);
  my(%The_Course) = @_;
  
  $Ban_Dept_Num = @{$The_Course{ban_dept}};
  $Ban_Grade_Num = @{$The_Course{ban_grade}};
  $Ban_Class_Num = @{$The_Course{ban_class}};
  
  if( ($Ban_Dept_Num==0) and ($Ban_Grade_Num==0) and ($Ban_Class_Num==0) ) {
    return(0);                       ##  不擋修, return
  }else{                             ##  擋修, 繼續檢查
    if($Ban_Dept_Num == 0){             ##  如果沒有檔系所，則預設為所有系所
      @Ban_Dept=Find_All_Dept();
    }else{
      @Ban_Dept=@{$The_Course{ban_dept}};
    }

    if($Ban_Grade_Num == 0){            ##  如果沒有擋年級，則預設為所有年級
      @Ban_Grade=(1,2,3,4,5,6,7,8,9,10);
    }else{
      @Ban_Grade=@{$The_Course{ban_grade}};
    }

    if($Ban_Class_Num == 0){            ##  如果沒有擋班級，則預設為所有班級
      @Ban_Class=(A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z);
    }else{
      @Ban_Class=@{$The_Course{ban_class}};
    }
    $L1=$L2=$L3=0;

    foreach $item (@Ban_Dept){
      if($item eq $Student{dept}){
        $L1 = 1;
      }
    }

#    print("fu : $FU{$Student{id}}<BR>");
#    print("double : $DOUBLE{$Student{id}}<BR>");
#    print("this : $The_Course{dept}<BR>");
    if( ($The_Course{dept} eq "6104") or ($The_Course{dept} eq "6154") or
        ($The_Course{dept} eq "6204") ) {       ### 如果開課系所是法律系任一組
       if( $FU{$Student{id}} eq "6054" ) {      ### 且學生是法律系輔系生  
         $FU{$Student{id}} = $The_Course{dept}; ### 則視同是該組的輔系生
       }   
    }  
    if( $FU{$Student{id}} eq $The_Course{dept}) {
      $L1 = 0;                            ##  輔系不受擋修系所限制2002/02/26
    }
    if( $DOUBLE{$Student{id}} eq $The_Course{dept}) {
      $L1 = 0;                            ##  雙主修不受擋修系所限制2002/02/26
    }

    foreach $item(@Ban_Grade){            ##  要在意，升級後與升級前不同...
      if($item eq $Student{grade} ){      ##  小心，不在意會發生重大危機...
        $L2 = 1;
      }
    }
    foreach $item(@Ban_Class){
      if($item eq $Student{class}){
        $L3 = 1;
      }
    }

    if(($L1 == 1) && ($L2 == 1) && ($L3 == 1)){   ###  學生符合擋修系所年級班級
      if( $SUPERUSER == 1 ) {                ##  管理者不擋修
        return(0);
      }elsif($system_flags{no_ban} == 1) {   ##  若設定第二階段設定擋修無效:
        if( $Ban_Dept_Num < 10 ) {           ##    -> 擋修系所少於 10 個(視同於限本系), 要檔修
          return(1);
        }elsif( ($The_Course{dept} eq "V000") or ($The_Course{dept} eq "7006") ) {
          return(1);                         ##    -> 軍訓與通識仍要擋修
        }else{
          return(0);                         ##    -> 其他課程依設定不擋修
        }
      }else{
        if( $TEMP_REMEDY_20040224 == 1 ) {      ### 補救 20040224 事件
          ### 檢查該同學是否在補救名單內, 允許不受擋修限制(added 2004/06/08)
          my($temp_file, @temp_lines, $j, $temp_cid);
          $temp_file = $DATA_PATH . "20040224/" . $Student{id};
          if( -e $temp_file ) {
            open(TEMP_FILE, $temp_file);
            @temp_lines = <TEMP_FILE>;
            close(TEMP_FILE);
            foreach $temp_line (@temp_lines) {
              ($j, $temp_cid) = split(/\[/, $temp_line);
              ($temp_cid, $j) = split(/ /, $temp_cid);
#              print("allowed no-ban: $temp_cid <-> $The_Course{id}<BR>\n");
              if( $The_Course{id} eq $temp_cid ) {
                return(0);			## 在補救名單內, 不擋修
              }
            }
          }
        }
        return(1);                           ##  符合限制, 要擋修
      }
    }
  }
}
############################################################################################
#####  Check_Credit_Upper_Limit()
#####  檢查學分上限(現在規定是25學分)
#####  除管理者外不得選修超過學分上限
#####  更新: 考慮個別學生學分上限限制(在管理選單中設定) 2001/09/04 Nidalap
#####  輸入: ($total_credit, $The_Course{credit})
#####  輸出: $limit_flag                   $limit_flag:(0,1) = (超過, 不超過)
############################################################################################
sub Check_Credit_Upper_Limit()
{
  my($upper_limit_file) = $REFERENCE_PATH . "credit_upper_limit.txt";
  my($temp_id, $temp_limit, $upper_limit);
  my( $student_id, $total_credit, $credit ) = @_;
  $upper_limit = 25;
  $total_credit += $credit;

  open(LIMIT, $upper_limit_file);      ###  檢查個別學生學分上限檔
  @line = <LIMIT>;
  close(LIMIT);
  foreach $line (@line) {
    $line =~ s/\n//;
    ($temp_id, $temp_limit) = split(/\s+/, $line);
    if($temp_id eq $student_id) {
      $upper_limit = $temp_limit;
    }
  }

  if( $total_credit > $upper_limit ) {  
    if( $SUPERUSER == 1 ) {
      return(1);
    }else{
      return(0);
    }
  }else{
    return(1);
  }
}
############################################################################################
#####  Check_Number_Limit()
#####  檢查修課人數限制
#####  判斷該科目的修課人數, 限修條件, 以及目前系統的限修條件, 決定該學生是否可選修
#####  
#####  輸入: ($student_id, %The_Course)
#####  輸出: $number_limit_flag         (0,1) = (已滿, 未滿)
############################################################################################
sub Check_Number_Limit()
{
  my ($stu_id, %The_Course) = @_;
  my($number, $limit_state, $flag, $upper_limit_immune_flag);
  $number = Student_in_Course($The_Course{dept}, $The_Course{id}, $The_Course{group}, "");
  $limit_state = Limit_State();
  
  $The_Course{number_limit} = 0		if( $The_Course{number_limit} eq "" );
  $The_Course{reserved_number} = 0	if( $The_Course{reserved_number} eq "" );

  $flag = 0;				####  預設已滿不能選
    
  if( $SUPERUSER == 1 ) {
    $flag = 1;
  }elsif( $The_Course{number_limit} == 0 ) {      ###  限修 0 人視為不限修
    $flag = 1;
  }else{
    if( $limit_state == 0 ) {                     ###  系統設定不限修
      $flag = 1;      
    }elsif( $limit_state == 1 ) {                 ###  系統設定考慮保留人數
      $upper_limit_immune_flag = Check_Course_Upper_Limit_Immune( $The_Course{id},
                                     $The_Course{group}, $stu_id);
      if( $upper_limit_immune_flag == 1 ) {
        $flag = 1;
      }
      if( $number < $The_Course{number_limit} - $The_Course{reserved_number} ) {
        $flag = 1;
      }
    }elsif( $limit_state == 2 ) {                 ### 系統設定僅考慮限修人數
      my($immune_count);                          ### 額滿加簽不能算在選課人數內
      $immune_count = Check_Course_Upper_Limit_Immune_Count($The_Course{id}, $The_Course{group}, "add");
      $immune_count=0  if($immune_count < 0);
      if( $number < ($The_Course{number_limit} + $immune_count) ) {
        $flag = 1;
      }
      $upper_limit_immune_flag = Check_Course_Upper_Limit_Immune( $The_Course{id},
                                     $The_Course{group}, $stu_id);  
      if( $upper_limit_immune_flag == 1 ) {
        Upper_Limit_Immune_Add($The_Course{id}, $The_Course{group}, $stu_id);
                                                  ###  有加簽的加選, 要另外紀錄
        $flag = 1;
      }
    }
  }
#  print("upper_limit_immune_flag = $upper_limit_immune_flag<BR>\n");
  return($flag);
}
############################################################################################
#####  REPORT_ERROR()
#####  回報錯誤訊息
#####  輸出錯誤訊息HTML給學生, 告知為何選課無法接受.
#####  輸入: $error_string
#####  輸出: (none)
############################################################################################
sub REPORT_ERROR()
{
  my($error_string) = @_;
  
  print qq(
    <html>
      <head><meta http-equiv="Content-Type" content="text/html; charset=big5"></head>
      <body background="$GRAPH_URL./ccu-sbg.jpg">
        <center>
        $HEAD_DATA
        <hr><br>
        <font size=5>錯誤: $error_string</FONT><BR>
        <font size=5>請<a href="javascript:history.back()">重新選取</a></font>
        </center>
      </body>
    </html>
  );
  exit();
}
############################################################################
############################################################################
#####   檢查科目屬性及學分歸屬                                      
#####   比對科目的開課屬性, 及學生所選的學分歸屬, 並傳回比對結果
#####   輸入: ($Property, $MyProperty)
#####   輸出: $result: (正確的話傳回99)
############################################################################
sub Check_Property
{
  my($Property,$MyProperty)=@_;
  if($MyProperty == 0){                        ###  未選取學分歸屬
    return 0;
  }
  if($MyProperty == 1 and $Property != 1){     ###  必修
    return 1;
  }
#  if( $MyProperty != 3 and $Property == 3){    ###  通識科目
#    return 2;
#  }
  return 99;
}
#############################################################################
#############################################################################
sub VIEW_COURSE
{
@MyCourse=Course_of_Student($Student{id});
$MyCount=@MyCourse;
@Teachers=Read_Teacher_File();
my(@WeekDay)=("一","二","三","四","五","六","日");
my(@TimeMap)=(A,1,2,3,4,B,5,6,7,8,C,D,E);

if($Input{dept} eq "" or $Input{grade} eq ""){   ####  並未選取系所年級  ####
    RESELECT($HEAD_DATA);                        ####  請重新選取        ####
}else{
    @Course=Find_All_Course($Input{dept},$Input{grade},"");
    $Count=@Course;
    if(($Count % 10) == 0 && ($Count != 0)){
      $TotalPages=int($Count/10);
    }else{
      $TotalPages=int($Count/10)+1;
    }
  if($Count != 0){                               ####  正常情況          ####
    ####  避免頁數超過  ####                     ####  可正常選課        ####
    while($Current_Page*10 >= $Count+10){
        $Current_Page--;
    }

    my($DATA)="";

    $DATA = $DATA."<table width=800 border=1>\n";
    $DATA = $DATA."<tr>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>標記</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>目前選修人數</font></th>";
    if( $system_flags{show_immune_count} == 1 ) {
      $DATA = $DATA."<TH bgcolor=YELLOW><FONT size=2>可加選名額</FONT></TH>";
    } 
    if( $system_flags{show_last_total} == 1 ) {
      $DATA = $DATA."<th bgcolor=yellow><font size=2>上次篩選後餘額</font></th>";
    }
    $DATA = $DATA."<th bgcolor=yellow><font size=2>科目名稱</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>授課教師</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>班別</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>學分</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>科目屬性</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>星期節次</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>教室</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>學分歸屬</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>課程大綱</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>其他</font></th>";
    $DATA = $DATA."</tr>";

    ####  限制相關頁數的科目  ####
    for($i=($Current_Page-1)*10; $i < $Count and $i < $Current_Page*10; $i++){
      ####  開始讀取相關科目的相關資料，減少搜尋範圍，節省時間  ####
      %the_Course=Read_Course($Input{dept},$Course[$i]{id},$Course[$i]{group});
      $DATA=$DATA."<tr>";                        ##  標記
      $DATA=$DATA."<th>";
      my($Flag)=0;
      my($Property)="";
      for($j=0; $j < $MyCount; $j++){
          if( ($the_Course{id} eq $MyCourse[$j]{id})){
              if( ($the_Course{group} eq $MyCourse[$j]{group}) ){
                  $Flag=1;
                  $Property=$MyCourse[$j]{property};
                  break;
              }
          }
      }
                     
      if($Flag == 1){   ###  該門課已經選過了  ###
          $DATA=$DATA."<img src=\"".$GRAPH_URL."flag.gif\">\n";
      }else{            ###  該門課尚未選過    ###
          $DATA=$DATA."<input type=checkbox name=";
          $DATA=$DATA."\"course\" value=\"";
          $DATA=$DATA.$the_Course{id}."_".$the_Course{group}."\">";
      }
      $DATA=$DATA."</th>\n";

      ###########  是否額滿註記 Added Feb 21,2000 Nidalap
#      $course_full_flag = Student_of_Course_Number($Input{dept}, $Course[$i]{id}, $Course[$i]{group});
      $student_count = Student_in_Course($Input{dept}, $Course[$i]{id}, $Course[$i]{group});
      $student_count_show = $student_count;
      
#      $course_full_flag = "否";
#      print("$course_full_flag $the_Course{number_limit} $the_Course{reserved_number}");

      $limit_state = Limit_State();
      if( $limit_state == 1 ) {                                 ###  考慮保留人數
        if( ($student_count >= $the_Course{number_limit} - $the_Course{reserved_number}) and ($the_Course{number_limit} != 0)) {
          $student_count_show = "<font color=RED>" . $student_count . "</font>";
        }
      }elsif( $limit_state == 2 ) {                             ###  只考慮限修人數
        if( ($student_count >= $the_Course{number_limit}) and ($the_Course{number_limit} != 0)) {
          $student_count_show = "<font color=RED>" . $student_count . "</font>";
        }
      }            
      $DATA = $DATA . "<TH>";
      $DATA = $DATA . $student_count_show . "</TH>";
      
      #####################################################################   
      if( $system_flags{show_immune_count} == 1 ) {  ### 要顯示可加選名額
        my($limit_state);
        $limit_state = Limit_State();
        if( $limit_state == 2 ) {                    ### 強制只有在先選先贏時才顯示
          my($immune_count, $available_count);
          $DATA = $DATA . "<TH>";
          $immune_count = Check_Course_Upper_Limit_Immune_Count($Course[$i]{id}, $Course[$i]{group}, "add");
          if( ($the_Course{number_limit} == 0) or ($the_Course{number_limit} == 999) ) {
            $DATA .= "<FONT size=2>無限制</FONT>";
          }else{
            $immune_count = 0  if($immune_count <= 0);
            $available_count = $the_Course{number_limit} + $immune_count - $student_count;
            $available_count = 0  if( $available_count <= 0 );    ###  應該不會發生 :P
            if( $available_count == 0) {
              $available_count_show = "<FONT color=RED size=2>" . $available_count . "</FONT>";
            }else{
              $available_count_show = $available_count;
            }
            $DATA .= $available_count_show;
          }
          $DATA .= "</TH>";
        }
      }
      #####################################################################
      if( ($system_flags{show_last_total} == 1) ) {  ### 要顯示上次篩選後餘額    
        $DATA = $DATA . "<TH>";
        $rest_count = Student_in_Course($Input{dept}, $Course[$i]{id}, $Course[$i]{group}, "last");
        $rest_count = $the_Course{number_limit} - $rest_count;
        $rest_count = 0  if($rest_count < 0);
        if( $rest_count == 0 ) {
          $DATA = $DATA . "<FONT color=RED>";
        }
        $rest_count = "<FONT size=2 color=BLACK>無限制" if( $the_Course{number_limit} == 0 );
        $DATA = $DATA . $rest_count . "</TH>";
      }
      #####################################################################
      $DATA=$DATA."<th><font size=2>";
      $DATA=$DATA.$the_Course{id};               ##  科目代碼
      $DATA=$DATA."<br>".$the_Course{cname};     ##  科目名稱
      $DATA=$DATA."</font></th>\n";

      $DATA=$DATA."<th><font size=2>";           ##  授課教師
      $T=@{$the_Course{teacher}};

      for($teacher=0; $teacher < $T; $teacher++){
        if($the_Course{teacher}[$teacher] != 99999){
          $DATA=$DATA.$Teacher_Name{$the_Course{teacher}[$teacher]};
        }else{
          $DATA=$DATA."教師未定";
        }
        if($teacher != $T-1){
          $DATA=$DATA.", ";
        }
      }
      $DATA=$DATA."</font></th>\n";

      $DATA=$DATA."<th><font size=2>";
      $DATA=$DATA.$the_Course{group};            ##  班別
      $DATA=$DATA."</font></th>\n";
      $DATA=$DATA."<th><font size=2>";
      $DATA=$DATA.$the_Course{credit};           ##  學分數
      $DATA=$DATA."</font></th>\n";
      $DATA=$DATA."<th><font size=2>";

      if($the_Course{property} == 1){            ##  科目屬性
          $DATA=$DATA."必修";
      }elsif($the_Course{property} ==2){
          $DATA=$DATA."選修";
      }else{
          $DATA=$DATA."通識";
      }

      $DATA=$DATA."</font></th>\n";

      $DATA=$DATA."<th><font size=2>";           ## 星期節次
      $time_string = Format_Time_String($the_Course{time});
      $DATA .= $time_string;
      $DATA=$DATA."</font></th>\n";

      $DATA=$DATA."<th><font size=2>";           ##  教室
      %Room=Read_Classroom($the_Course{classroom});
      $DATA=$DATA.$Room{cname};
      $DATA=$DATA."</font></th>\n";

      $DATA=$DATA."<th><font size=2>";##  學分歸屬
      if($Flag == 0){
        $DATA .= Show_Property_Select();
      }else{
          if($Property == 1){$DATA=$DATA."必修";}
          if($Property == 2){$DATA=$DATA."選修";}
          if($Property == 3){$DATA=$DATA."通識";}
          if($Property == 4){$DATA=$DATA."輔系";}
          if($Property == 5){$DATA=$DATA."雙主修";}
          if($Property == 6){$DATA=$DATA."大學部課程";}
          if($Property == 7){$DATA=$DATA."教育學程";}
#          if($Property == 8){$DATA=$DATA."不列入畢業總學分";}
      }

      $DATA=$DATA."</font></th>\n";
      ###  課程大綱 Added 20080805 Nidalap :D~
      $DATA=$DATA."<th><font size=2>";
      $DATA=$DATA."<A href=\"".$ECOURSE_QUERY_COURSE_URL."&courseno=".$the_Course{id}
        ."_".$the_Course{group}."&year=".$YEAR."&term=".$TERM."\" target=NEW>"
        ."連結</A>";
      $DATA=$DATA."</font></th>\n";

#      my($FILENAME)=$CLASS_URL."ShowNote.cgi";
      my($FILENAME)="ShowNote.cgi";
      $DATA=$DATA."<th><font size=2>";
      $DATA=$DATA."<a href=\"".$FILENAME."?";
      $DATA=$DATA."user=";
      $DATA=$DATA.$Input{id};
      $DATA=$DATA."&dept=";
      $DATA=$DATA.$Input{dept};
      $DATA=$DATA."&course=";
      $DATA=$DATA.$the_Course{id};
      $DATA=$DATA."&group=";
      $DATA=$DATA.$the_Course{group};
      $DATA=$DATA."\">備註</a>";
      $DATA=$DATA."</font></th>\n";

      $DATA=$DATA."</tr>";
    }

    $DATA = $DATA."</table>\n";

    DEPTS_COURSE($HEAD_DATA,$Student{id},$Student{password},$DATA);
  }else{
      RESELECT2($HEAD_DATA);                     ##  無選課資料 重新選取  ##
  }
}
}
########################################################################
#####  Show_Property_Select()
#####  產生科目屬性選項供學生選擇
#####  依據開課屬性, 支援通識, 學生身份等而產生不同選項
#####  Update: Nov30,2000 Nidalap
########################################################################
sub Show_Property_Select()
{
  my($property_select, $graduate_select_under);
  $graduate_select_under = 0;

  if( ($Student{dept} =~ /6$/) and
      ( ($the_Course{dept} =~ /4$/)or($the_Course{dept} eq "7006")
        or($the_Course{dept} eq "I000")or($the_Course{dept} eq "V000")
        or($the_Course{dept} eq "Z121")or($the_Course{dept} eq "F000")  ) ) {
     $graduate_select_under = 1;                               ###  研究生修大學部課程
  }

  $property_select .= "<select name=\"$the_Course{id}_$the_Course{group}\">\n";
#  $property_select .= "<option value=0>學分歸屬\n";
  
  if( (($the_Course{property} == 1) or ($SUPERUSER == 1)) and ($the_Course{dept} ne "7306") ) {
    if( $graduate_select_under != 1 ) {
      $property_select .= "<option value=1>必修\n";             ###  開為必修, 且不是學程的課
    }
  }
  if( (($the_Course{property} == 2) or ($SUPERUSER == 1)) and ($the_Course{dept} ne "7306") ) {
    if( $graduate_select_under != 1 ) {
      $property_select .= "<option value=2>選修\n";             ###  開為選修, 且不是學程的課
    }
  }
  if( ($the_Course{property} == 3) or ($SUPERUSER == 1) or ($the_Course{support_cge_type} ne "0") ) {
    if( $graduate_select_under != 1 ) {
      $property_select .= "<option value=3>通識\n";              ### 如果該科開為通識或支援通識
    }
  }
  if( ($the_Course{dept} ne "7306") and ($the_Course{dept} ne "I000") and ($the_Course{dept} ne "7006") ) {
                                                                ### 學程中心, 共同科, 通識中心開的課不得選為輔系
    if( ($FU{$Student{id}} eq $the_Course{dept}) or ($SUPERUSER == 1) ) {
      $property_select .= "<option value=4>輔系\n";
    }
    if( ($DOUBLE{$Student{id}} eq $the_Course{dept}) or ($SUPERUSER == 1) ) {
      $property_select .= "<option value=5>雙主修\n";
    }
  }
  if( $graduate_select_under == 1 ) {
    $property_select .= "<option value=6>大學部課程\n";
  }

  if( $the_Course{dept} eq "7306" ) {                                ### 學程中心開的課才能選為學程
    $property_select .= "<option value=7>教育學程\n";
  }
###  "不列入畢業學分" 選項已經不復存在 (2003/01/06 Nidalap :D~)
#  if( (($Student{dept} =~ /4$/) and ($the_Course{dept} =~ /6$/)) and ($the_Course{dept} ne "7006") ) {
#                                                                     ### 如果是大學生修研究所課程, 或該科目是通識所開
#    $property_select .= "<option value=8>不列入畢業學分";
#  }
  $property_select .= "</select>\n";
}
################################################################################
########################################################################
####  加選系統控制單元子程式                                        ####
####    Limit_State() : 輸出目前選課人數限制的狀態 (0/1/2)          ####
####    is_Grade_Update() : 因應學生資料檔更新速度較慢的問題，於次  ####
####                    一學年開始前暫時將各年級學生年級自動加 1。  ####
########################################################################
sub Limit_State()
{
  my($FileName)=$REFERENCE_PATH."Basic/LimitNumberState";
  open(FILE,"<$FileName")
                   or die("Cannot open file $FileName!\n");
  $State=<FILE>;
  close(FILE);

  return($State);
}

sub is_Grade_Update()
{
  my($FileName)=$REFERENCE_PATH."Basic/GradeState";
  open(FILE,"<$FileName")
                   or die("Cannot open file $FileName!\n");
  $State=<FILE>;
  close(FILE);

  return($State);
}

########################################################################
####    產生該選擇的相關系所開課資料的 HTML 檔案                    ####
####    產生 table 的函式在上面                                     ####
########################################################################
sub DEPTS_COURSE
{
my($HEAD_DATA,$id,$password,$DATA)=@_;
my($NEXT_URL)="Add_Course01.cgi";
my($LINK)=Select_Course_Link($Input{id},$Input{password});
my($PRE_COURSE_WARNING, $EDU_COURSE_WARNING, $MIL_COURSE_WARNING);

if($pre_course_count > 0) {        ###### 有先修科目的話, 顯示警訊html檔
  $PRE_COURSE_WARNING = qq(
    <SCRIPT language="javascript">
      messageWindow = open('Show_Special_Announce.php?type=prerequisite_msg', 'messageWindow', 'resizable=yes, width=250, height=250');
    </SCRIPT>
  );
}
if( $Input{dept} eq "7306" ) {     ######  修教育學程的課, 必須是教育學程的學生html warning
  my($announce_title, $announce_content) =  Read_Special_Announce("edu_msg");
  $COURSE_WARNING2 = Special_Announce_Table($announce_title, $announce_content);    
#  $EDU_COURSE_WARNING = qq(
#    <SCRIPT language="javascript">
#      messageWindow = open('Show_Special_Announce.php?type=edu_msg','messageWindow', 'resizable=yes, width=250, height=250');
#    </SCRIPT>
#  );
}

if( $Input{dept} eq "V000" ) {     ######  軍訓課程說明 (added 2006/11/14)
  my($announce_title, $announce_content) =  Read_Special_Announce("military_msg");
  $COURSE_WARNING2 = Special_Announce_Table($announce_title, $announce_content);
      
#  $MIL_COURSE_WARNING = qq(
#    <SCRIPT language="javascript">
#      messageWindow = open('Show_Special_Announce.php?type=military_msg','messageWindow', 'resizable=yes, width=350, height=350');
#    </SCRIPT>
#  );
}

if( $Input{dept} eq "F000" ) {     ######  體育課程說明 (added 2006/11/24)  
  my($announce_title, $announce_content) =  Read_Special_Announce("physical_msg");
  $COURSE_WARNING2 = Special_Announce_Table($announce_title, $announce_content);
    
#  $MIL_COURSE_WARNING = qq(
#    <SCRIPT language="javascript">
#      messageWindow = open('Show_Special_Announce.php?type=physical_msg','messageWindow', 'resizable=yes, width=450, height=450');
#    </SCRIPT>
#  );
}

if( $Input{dept} eq "Z121" ) {     ######  語言中心課程說明 (added 2006/12/26)
  $MIL_COURSE_WARNING = qq(
    <SCRIPT language="javascript">
      messageWindow = open('Show_Special_Announce.php?type=lang_msg','messageWindow', 'resizable=yes, width=800, height=600');
    </SCRIPT>
  );
  
  my($announce_title, $announce_content) =  Read_Special_Announce("lang_msg");
  $COURSE_WARNING2 = Special_Announce_Table($announce_title, $announce_content);
#  $COURSE_WARNING2 = qq(
#    <TABLE border=0 width=70%>
#      <TR><TH bgcolor=YELLOW>$announce_title</TH></TR>
#      <TR><TD bgcolor=YELLOW>
#    )
#    . $announce_content
#    . qq(        
#      </TD></TR>
#    </TABLE>
#    <P>
#  );
}


#print("dept = $Input{dept}<BR>\n");

#if( length($Input{dept}) == 2 ) {               ###  跨領域學程
#  print qq(
#    <html>                                   
#      <head>
#        <meta http-equiv="Content-Type" content="text/html; charset=big5">
#        <meta http-equiv="refresh" content="1; URL=Show_All_GRO.cgi">
#        <Title>$SelectDept{cname}$Input{grade}年級科目列表</Title>  
#      </head>  
#  );
#
#}else{
  print << "End_of_HTML"
    <html>
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=big5">
        <Title>$SelectDept{cname}$Input{grade}年級科目列表</Title>
      </head>
      <script language="javascript">
        function FreeSelect(OBJ)
        {
            OBJ.page.value=3;
            OBJ.submit();
        }
      </script>
      $PRE_COURSE_WARNING
      $EDU_COURSE_WARNING
      $MIL_COURSE_WARNING
      
      <body background="$GRAPH_URL/ccu-sbg.jpg">
        <center>
            $HEAD_DATA
        <hr>
        <br>
        <b>
        $COURSE_WARNING2
        <font size=5>$SelectDept{cname}$Input{grade}年級科目列表</font>
        </b>
        <br>
        <form action="$NEXT_URL" method="post" name="SelectForm">
          <input type=hidden name="session_id" value="$Input{session_id}">
          <input type="hidden" name="dept" value="$Input{dept}">
          <input type="hidden" name="grade" value="$Input{grade}">
          <input type="hidden" name="page" value="$Current_Page">
          <input type="hidden" name="SelectTag" value=1>
          <table border=0 width=90%>
            <tr>
              <th colspan=2>
                $DATA
              </th>
            </tr>
            <tr>
              <th colspan=2> 
                 <input type=submit value="加選以上標記科目">
              </th>
              </tr>
          </form>
              <tr>
                <th align=left>
                  <form action="$NEXT_URL" method="post" name="NextForm">
                    <input type=hidden name="session_id" value="$Input{session_id}">
                    <input type="hidden" name="dept" value="$Input{dept}">
                    <input type="hidden" name="grade" value="$Input{grade}">
                    <input type="hidden" name="SelectTag" value=0>
                    <input type="hidden" name="page" value="$Current_Page">
                    <input type=button value="上一頁" onClick="javascript:history.back()">
                    <input type=submit value="下一頁">
                </th>	
                  </form>
                <th align=right>
                  第$Current_Page/$TotalPages頁
                </th>
              </tr>
        </table>
      </center>
      </body>
    </html>
End_of_HTML
#}

}
#################################################################################
sub RESELECT
{
my($HEAD_DATA)=@_;
print << "End_of_HTML"
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
</head>
<body background="$GRAPH_URL./ccu-sbg.jpg">
<center>
    $HEAD_DATA
    <hr><br>
    <br>
    <br>
    <font size=5>您尚未正確選取系所或年級</font><br>
    <font size=5>請<a href="javascript:history.back()">重新選取</a></font>
</center>
</body>
</html>
End_of_HTML
}

#####################################################################################
sub RESELECT2()
{
my($HEAD_DATA)=@_;

if( length($Input{dept}) == 2 ) {               ###  跨領域學程
  print qq(
    <html>                                   
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=big5">
        <meta http-equiv="refresh" content="1; URL=Show_All_GRO.cgi?session_id=$Input{session_id}&gro_no=$Input{dept}">
        <Title>$SelectDept{cname}$Input{grade}年級科目列表</Title>  
      </head>  
      <BODY background="$GRAPH_URL./ccu-sbg.jpg">
        <CENTER>
        本頁將轉向所有跨領域學程網頁, 請稍後.<BR>
        如果網頁沒有轉向, 
        請<A href="Show_All_GRO.cgi?session_id=$Input{session_id}&gro_no=$Input{dept}"">點選此處</A>.
      </BODY>
    </HTML>
  );
}else{
  print << "End_of_HTML"
    <html>
	<head>
	    <meta http-equiv="Content-Type" content="text/html; charset=big5">
	</head>
	<body background="$GRAPH_URL./ccu-sbg.jpg">
	<center>
	    $HEAD_DATA
	    <hr><br><br>
	    <font size=5>$SelectDept{cname}$Input{grade}年級截至目前為止</font><br>
	    <font size=5>並無任何開課資料可茲讀取</font><br>
	    <font size=5>請<a href="javascript:history.back()">重新選取</a></font>
	</center>
	</body>
    </html>
End_of_HTML
}
}
######################################################################################
sub Special_Announce_Table()
{
  my ($announce_title, $announce_content) = @_;
  my $COURSE_WARNING2 = qq(
    <TABLE border=0 width=70% cellspacing=0>
      <TR><TH bgcolor=YELLOW>$announce_title</TH></TR>
      <TR><TD bgcolor=YELLOW>
    )
    . $announce_content
    . qq(        
      </TD></TR>
    </TABLE>
    <P>
  );
  return($COURSE_WARNING2);
}
