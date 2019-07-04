#!/usr/local/bin/perl
###########################################################################################
#####  Add_Course01.cgi
#####  處理學生加選資料
#####  接收 Add_Course_00.cgi 傳來的資料, 判斷學生選課資料合法性
#####  (密碼, 擋修, 限修人數 etc), 決定是否加選及顯示開課資料網頁
#####  Coder   : Nidalap :D~
#####  Updates :
#####	Jan 10/2001 Created
#####	2008/06/03 增加跨領域學程功能, 轉向到 Show_All_GRO.cgi	Nidalap :D~
#####	2008/08/05 增加連結前往 Ecourse 課程大綱			Nidalap :D~
##### 	2008/09/01 體育課程相關增修, 詳見 CHECK_VALID_SELECT_COURSE() Nidalap :D~
#####	2010/01/07 軍訓課程相關增修，同上  Nidalap :D~
#####	2010/08/10 全英語授課課程顯示註解要加上英文  Nidalap :D~
#####	2010/12/08 將「每學期限修一門」功能獨立出來，包括原有的軍訓、通識外語，和新增的中國語文知識與應用 Nidalap :D~
#####	2010/12/29 語言中心「應用英外語課程」相關增修，特定名單內才可選課 Nidalap :D~
#####	2011/02/10 新增物理系「二一邊緣學生輔導」機制. Nidalap :D~
#####	2011/03/10 選擇通識時，會顯示「第 X 領域」而非「第 X 年級」  Nidalap :D~
#####   2011/04/26 系所服務學習課程只允許加簽加選  Nidalap :D~
#####   2011/07/29 系統「只允許查詢」時也可看此網頁，但是無加選 checkbox 和加選執行按鈕。  Nidalap :D~
#####   2011/07/29 加入「加簽」選項，連結至線上加簽網頁  Nidalap :D~
#####   2012/02/15 系統「不開放查詢」時也可看此網頁，但是無加選 checkbox 和加選執行按鈕。
#####              另，此期間不出現已選上科目的小紅旗子  Nidalap :D~
#####   2012/02/15 軍訓限修一門課程的限制，可透過加簽迴避之。  Nidalap :D~
#####   2012/04/17 語言中心課程限修一門增修 & 開課學制(碩/博)欄位  Nidalap :D~
#####   2012/12/12 若加選課程不支援學生所屬系所，則顯示警訊  Nidalap :D~
#####   2013/08/07 英文版相關增修：將顯示文字拉到 Init_Text_Values() 中設定。 Nidalap :D~
#####   2013/12/12 因應通識改制，判斷學生身份，決定是否透過上一頁傳來的通識「向度」選項抓取科目清單。  Nidalap :D~
#####   2014/09/04 因應選課改制，先搶先贏期間退選餘額延後釋出，新增加選前該科目是否在等待退選狀態中檢查。  Nidalap :D~
#####   2014/09/14 新增「擋修與否」底色醒目提示。  Nidalap :D~
#####   2014/09/17 研究生學分上限預設為 20。  Nidalap :D~
#####   2014/11/06 新增行動化相關功能 by Nidalap :D~
#####   2014/12/30 行動化相關功能補強：點選科目後展開科目詳細資料  by Nidalap :D~
#####   2016/09/12 修正陳年老 BUG：依年級設定可否選課的功能沒有作用在加選上（設定某年級不可加選仍可加選！） by Nidalap :D~
#####   2016/09/21 因為行動版網頁無法從上頁帶入通識向度資料，此處特別從年級做判別。 by Nidalap :D~
################################################################################################
print("Content-type: text/html\n\n");

$DEBUG = 0;

require "../library/Reference.pm";
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
require $LIBRARY_PATH."Session.pm";
require $LIBRARY_PATH."English.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Teacher.pm";

#my(%Student,%Dept);
%time = gettime();

###################    讀取使用者輸入資料    ######################
%system_flags = Read_System_Settings();
#%Input=User_Input();
$Input[grade] = $Input[grade2]  if( $Input[dept] eq $DEPT_CGE );
%txt = Init_Text_Values();

#print "input = ";
#Print_Hash(%Input);

#print "[dept, grade] = [" . $Input{dept} . ", " . $Input{grade} . "]<BR>\n";

($Input{id}, $Input{password}, $login_time, $ip, $add_course_count) = Read_Session($Input{session_id}, 1, 1);
#print("session_id, id, pass = $Input{session_id}, $Input{id}, $Input{password}<BR>"); 

#if( length($Input{dept}) == 2 ) {		###  跨領域學程
#  print qq (Location: Show_All_GRO.cgi?gro_id=$Input{dept} );  
#}else{
#  print("Content-type: text/html\n\n");
#}

%Student=Read_Student($Input{id});
%Dept=Read_Dept($Student{dept});
%SelectDept=Read_Dept($Input{dept});

($cate_ref, $subcate_ref) = Get_CGE_Categories();
%category = %{$cate_ref};
%subcategory = %{$subcate_ref};
$use_cge_new_cate = Student_Suit_CGE_New_Category($Student{'id'});		###  判別學生是否適用 103 學年度後的通識「向度」
%txt = Init_Text_Values();

Check_Student_Password($Input{id}, $Input{password});
#my($HEAD_DATA)=Head_of_Individual($Student{name},$Student{id},$Dept{cname},$Student{grade},$Student{class});
if( $IS_ENGLISH ) {
  $HEAD_DATA = Head_of_Individual($Student{ename},$Student{id},$Dept{ename},$Student{grade},$Student{class});
}elsif( $IS_MOBILE ) {
  $HEAD_DATA = "";															###  行動版不顯示過長的學生個人資料欄
}else{
  $HEAD_DATA = Head_of_Individual($Student{name},$Student{id},$Dept{cname},$Student{grade},$Student{class});
}

($concent_form_allowed, $cf_msg) = Apply_Form_Allowed("concent");          ###  目前是否允許申請加簽

if($add_course_count >= $ADD_COURSE_LIMIT) {
  Session_Add_Course_Limit($system_flags{black_list}, $time{time_string}, $Input{id}, $ip);
}
$add_course_count ++  if($Input{SelectTag} == 1);
Write_Session($Input{session_id}, $Input{id}, $Input{password}, $add_course_count);

###################    若非選課時間則顯示不可進入  ################
#if($SUPERUSER != 1){     ## 非 superuser 的使用者
#  if( (Whats_Sys_State()==0)or(Whats_Sys_State()==1)or(Check_Time_Map(%Student)!=1) ){
#    Enter_Menu_Sys_State_Forbidden($HEAD_DATA);
#  }
#}

if($SUPERUSER != 1){     ## 非 superuser 的使用者
#  if( (Whats_Sys_State()==0)or(Check_Time_Map(%Student)!=1) ){
#    Enter_Menu_Sys_State_Forbidden($HEAD_DATA);
#  }elsif(Whats_Sys_State()==1) {
#  if( Whats_Sys_State()<=1 ) {
if( (Whats_Sys_State()==0)or(Whats_Sys_State()==1)or(Check_Time_Map(%Student)!=1) ){
    $disabled_html = " DISABLED='DISABLED' ";		###  僅供查詢 or 不開放查詢: 不可點選 checkbox
    if( Whats_Sys_State() == 0 ) {
      $view_only_flag = 2;				###  不開放查詢！！
    }else{
      $view_only_flag = 1; 				###  僅供查詢！
    }
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

$Current_Page = $Input{page};
$Current_Page = 1  if( $Current_Page == "" );
$TotalPages = 0;
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
####    2009/06/05  改由在讀取學生學籍資料時，就依照註冊次數與升級與否設定判斷年級  Nidalap :D~
#if( is_Grade_Update() == 1){
#  $Student{grade}++;
#  $Student{grade}=4  if( $Student{grade} > 4 );  ### 2004/06/07發現BUG更新
#}

####    建立 HTML 檔案的表頭部分    ####
####    包括使用者的身份資料等      ####

#############################################################################
####    本程式的核心請由此處著手往下看各個相關的函式                     ####
#############################################################################
########    判斷是否需要處理選課資料    ########

if($system_flags{black_list} == 1) {
  $ban_time = Read_Ban_Record($Student{id}, $BAN_COUNT_LIMIT);	### 停權尚須多久恢復(大於0就是停權中)
#  print "ban_time = $ban_time";
  if( $ban_time > 0 ) {
    Show_Ban_Message($ban_time, 1);
  }
}
if($Input{SelectTag} == 0 or not defined $Input{SelectTag}){
    #$Current_Page++;      ####    讀取下一頁    ####
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
  
  ###################    若非選課時間則顯示不可進入  ################
  if($SUPERUSER != 1){     ## 非 superuser 的使用者
    if( (Whats_Sys_State()==0)or(Whats_Sys_State()==1)or(Check_Time_Map(%Student)!=1) ){
      Enter_Menu_Sys_State_Forbidden($HEAD_DATA);
    }
  }
  
  ($valid_flag, $valid_string) = CHECK_VALID_SELECT_COURSE(@Courses);
  if($valid_flag == 0) {                                        ### 若選課資料不合法
    REPORT_ERROR($valid_string);
  }elsif($view_only_flag == 1) {				### 若目前系統為「僅供查詢」
    REPORT_ERROR($txt{'nosel'});
  }elsif($view_only_flag >= 1) {				### 若目前系統為「不開放查詢」
    REPORT_ERROR($txt{'nosel'});
  }else{                        		                ### 若選課資料合法                                
    $supported = 1;
	
    foreach $course(@Courses){
      my($id,$group)=split(/_/,$course);
      %the_Course=Read_Course($course_dept,$id,$group,"","",$Input{id});
      ### 學生選的課有某一門有先修條件, 將於網頁上顯示警訊
      if( $pre_course_count == 0 ) {
         $pre_course_count = @{$the_Course{prerequisite_course}};
         if($the_Course{prerequisite_course}[0]{dept} eq "99999") {
           $pre_course_count = 0;
         }
      }
	  ### 學生選的課有某一門有支援條件(且並非學生所屬學系), 將於網頁上顯示警訊
	  
	  #Print_Hash(%system_flags);
	  	  
	  $supported_temp = 0;
      if( $$the_Course{support_dept}[0] )  {
	    foreach $sup_dept (@{$the_Course{support_dept}}) {
	      if( ($sup_dept eq $Student{dept}) or ($sup_dept eq $FU{$Student{id}}) or ($sup_dept eq $DOUBLE{$Student{id}}) )  {
	        $supported_temp++;
	      }
	    }
		$supported *= $supported_temp;
	  }else{
	    if( ($sup_dept eq $Student{dept}) or ($sup_dept eq $FU{$Student{id}}) or ($sup_dept eq $DOUBLE{$Student{id}}) ) {
		  $supported = 1;
		}else{
		  $supported = 0;
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
#####     c. 擋修	: 除管理者、加簽核可外不可選
#####     d. 超過25學分	: 除管理者外不可選
#####     e. 限修人數	: 視系統限修條件(管理者不在此限)
#####     f. 專班不得選外所 : 包括專班及專班暑修(管理者不在此限)
#####     g. 通識中心不開放大四(視管理選單設定而定)
#####     h. 依照管理者設定開放或不開放數學系的課和非數學系的課
#####     i. 每學期僅限修一門必修體育(2008/09/01)
#####     j. 體育課可下修不可上修(跨年級)
#####     k. 每學期限選一門課程：軍訓、通識外語、中國語文及應用(since 2010/01/06)
#####     l. 專班不得選外所 -> 師培中心所開課程除外(2010/02/22)
#####	  m. 通識外語選課限制: 檢查新生分級名單，以及同一學期不可選兩門通識外語課 2010/09/02
#####	  n. 通識外語選課限制：依照預先匯入的新生分級名單，只有名單內的學生可選課 2010/09/04
#####     o. 物理系「二一邊緣學生輔導」機制 2011/02/10
#####     p. 不可直接加選「系所服務課程」(管理者不在此限) 2011/04/26
#####     q. 語言中心課程，針對「修課抵畢業門檻」名單，限制每人只能選一門課程  2012/04/17
#####     r. 因應選課改制，先搶先贏期間退選餘額延後釋出，新增加選前該科目是否在等待退選狀態中檢查  2014/09/04
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
  local(@Course_of_Student, @Course_of_Student2);   ###  前者用做檢查衝堂及25學分上限, 學生早已選修的科目。後者延遲退選檢查用
  my(@Courses) = @_;
  my @Courses_ = @Courses;      ###  用作在 foreach (@Courses) 內仍要檢查該生本次選擇的所有科目用
  
  ####################  檢查學生早已修習的課, 建立@time_map及記算學分  ####################
  @Course_of_Student  = Course_of_Student($Student{id});
  #####   這個版本包含尚在等待延遲退選的科目
  @Course_of_Student2 = Course_of_Student($Student{id}, "", "", 1);
  foreach $stu_course (@Course_of_Student) {
    %The_Course = Read_Course($$stu_course{dept}, $$stu_course{id}, $$stu_course{group}, "", "", $Student{id});
    $total_credit += $The_Course{credit};
    my $course_identifier = join("_", $$stu_course{dept}, $$stu_course{id}, $$stu_course{group});
    ($conflict_flag, $conflict_string) = Check_Course_Conflict(%The_Course);
    if( $conflict_flag == 1 ) {
      return("0", $conflict_string);
    };
  }
  
  %The_Course = "";  ###  清除此變數，以免影響以下判斷
  
  #######################  處理學生目前所選的課, 檢查合法性  #######################
  foreach $course (@Courses) {
    ($id, $group) = split(/_/, $course);
    %The_Course = Read_Course($course_dept, $id, $group, "", "", $Student{id});
    $upper_limit_immune_flag = Check_Course_Upper_Limit_Immune( $The_Course{id}, $The_Course{group}, $stu_id);
    ################  檢查學生目前所選的課, 建立@time_map及記算學分 ################
    ($conflict_flag, $conflict_string) = Check_Course_Conflict(%The_Course);
    if( $conflict_flag == 1 ) {
      return("0", $conflict_string);
    };
    ################  檢查學分歸屬是否有選  ################################################
    ################  ps. 可選的欄位在Show_Property_Select已設好了, 在此應不會有選錯情形  ############
    $property_flag = Check_Property($The_Course{property}, $Input{$course});
    if($property_flag != 99) {
      return("0", $txt{'no_property'});
    }
    ####################################################################################
    #####  2011/08/23 擋修系所年級班級，加上加簽檢查(若加簽已通過則 bypass
    $ban_flag = Check_Ban_Limit(%The_Course);
    if( $ban_flag == 1 ) {
#      $upper_limit_immune_flag = Check_Course_Upper_Limit_Immune( $The_Course{id}, $The_Course{group}, $stu_id);
      if( !$upper_limit_immune_flag ) {
        return("0", $txt{'ban_dept'});
      }
    }
    ####################################################################################
    $credit_25_limit_flag = Check_Credit_Upper_Limit($Student{id}, $total_credit, $The_Course{credit});
    if( $credit_25_limit_flag == 0 ) {
      return("0", $txt{'over_credit'});
    }else{
      if( ($total_credit + $The_Course{credit} > 25) and ($SUPERUSER == 1) ) {
        print($txt{'over_credit2'} ."<BR>");
      }
      $total_credit += $The_Course{credit};     ####  若學生一次選多門課學分要重複累加
    }
    ####################################################################################
    $number_limit_flag = Check_Number_Limit($Student{id}, %The_Course);
    if( $number_limit_flag == 0 ) {
      return("0", $txt{'no_avail'});
    }
    ######################################################################################
    ### 不可直接加選「系所服務課程」(管理者不在此限) 2011/04/26
    if($SUPERUSER != 1) {
      my $is_dept_serv = 0;
      $is_dept_serv = 1  if( $The_Course{id} eq Get_Dept_Serv_Course_ID($Input{dept}) );
      if( $is_dept_serv and !$upper_limit_immune_flag ) {
        return("0", $txt{'dept_serv_sel'});
      }
    }
  }
  #################################################################################
  if( $SUPERUSER != 1 ) {
    if( ($SUB_SYSTEM==3) or ($SUB_SYSTEM==4) ) {      ### 專班及專班暑修, 不得選外所
      if($Student{dept} ne $Input{dept}) {
        ###  2009/06/09 違章建築, 除外台文，勞工，經濟的課  <- 2010/06/23 拆除！ Nidalap :D~ 
        ###  2010/02/22 師培中心(7306)不在此限  Nidalap :D~
#        if( ($Input{dept}!="7306") and 
#            ($Input{dept}!="1516") and ($Input{dept}!="3206") and ($Input{dept}!="5106") ) {
        if( $Input{dept} != $DEPT_EDU ) {
          return("0", "專班同學請勿修習外所課程!");		### 此警訊不需英文版
        }
      }
    }
  }
  ######################################################################################
  if( $SUPERUSER != 1 ) {
    if( $Input{dept} eq $DEPT_CGE ) {
      if( $system_flags{cge_ban_grade} == 1 ) {
        if( $Student{grade} == 4 ) {
          return("0", $txt{'cge_no_4'});
        }
      }elsif( $system_flags{cge_ban_grade} == 2 ) {
        if( ($Student{grade} == 3) or ($Student{grade} == 4) ) {
          return("0", $txt{'cge_no_4'});
        }
      }
    }
  }
  ######################################################################################
#  if( $SUPERUSER != 1 ) {
#    if( ($system_flags{allow_select_math} == 1) and (is_Math_Dept($Input{dept})) ) {
#      return("0", "目前系統不開放選修數學系所開設之科目, 請於開放期間選課!");
#    }elsif( ($system_flags{allow_select_math} == 2) and (not is_Math_Dept($Input{dept})) ) {
#      return("0", "目前系統不開放選修非數學系所開設之科目, 請於開放期間選課!");
#    }
#  }
  ######################################################################################
  ###  教育學程開設科目, 只有擁有教育學程資格者可以修習(Added 2003/09/09, Nidalap :D~)
  if($SUPERUSER != 1) {
    if( $Input{dept} eq $DEPT_EDU ) {
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
        return("0", $txt{'no_edu'});
      }
    }
  }
  ######################################################################################
  ###  體育課相關限制  (Added 2008/09/01, Nidalap :D~)
  ###  1. 每學期僅限修一門必修體育
  if($SUPERUSER != 1) {
    if( $The_Course{id} =~ /^902(1|2)/ ) {		### 9021, 9022 分別是給一年級, 二年級的
      foreach $stu_course (@Course_of_Student) {	###   檢查學生已經選上了的課
        if( $$stu_course{id} =~ /^902(1|2)/ ) { 
          return("0", $txt{'one_phy'});
        }
      }
      foreach $stu_course (@Courses_) {                 ###   檢查學生本次所選的其他課
        my($temp_id,$temp_group) = split(/_/, $stu_course);
        next  if( ($temp_id eq $The_Course{id}) and ($temp_group eq $The_Course{group}) );
        if( $temp_id =~ /^902(1|2)/ ) {
          return("0", $txt{'one_phy'});
        }
      }
    }
    ###  2. 體育課可下修不可上修(跨年級) 
    if( $The_Course{id} =~ /^902(.)/ ) {		### 科目代碼第四碼, 拿來與年級相比較
      if( ($Student{grade} < $1) and ($Student{id} =~ /^4/) ) {
        return("0", $txt{'no_phy_up'});
      }
    }
    
  }    

#  print("正在檢查 $The_Course{id} <BR>\n");
  
  ######################################################################################
  ###  每學期限修一門課限制  2010/12/08  Nidalap :D~
  ($tmp_flag, $tmp_reply) = Check_One_Course_Only(\%The_Course, \@Course_of_Student, \@Courses_);
  return($tmp_flag, $tmp_reply)   if( $tmp_flag == 0 );
  
  

  #######################################################################################
  ### 通識外語選課限制：依照預先匯入的新生分級名單，只有名單內的學生可選課  2010/09/04  Nidalap :D~
  ### Update: 2011/12/27  新增 [5,6] = [抵免一科(基礎), 抵免一科(強化)]
  $upper_limit_immune_flag = Check_Course_Upper_Limit_Immune( $The_Course{id}, $The_Course{group}, $stu_id);
      
  if($SUPERUSER != 1) {
    if( $The_Course{id} =~ /^7102[12]/) {               ### 通識外語課
      if( $Student{grade} == 1 ) {						###  只對大一作用 ( 以後可能要拆除此限制 20100903 )
#        print("檢查通識外語...<BR>\n");
        $genedu_foreign_lang_file = $DATA_PATH . "Grade/genedu_foreign_lang/" . $Student{id};
        if( not -e $genedu_foreign_lang_file ) {				###  若無此學生英檢資料
          return("0", $txt{'eng_1'});
        }else{									###  檢查新生英檢成績檔
          open(GENEDU_FOREIGN_LAN, $genedu_foreign_lang_file);
          $line = <GENEDU_FOREIGN_LAN>;
          close(GENEDU_FOREIGN_LAN);
          ($f_id, $f_grade) = split(/\s+/, $line);				###  讀取新生英檢成績檔
#          print("[$f_id, $f_cname, $f_grade ]<BR>\n");
          if( $f_grade == 4 ) {
            return("0", $txt{'eng_2'});
          }elsif( $f_grade == 3 )  {
            return("0", $txt{'eng_3'});
          }elsif( (($f_grade == 2)or($f_grade == 6)) and ($The_Course{id} !~ /^7102.2.$/) )  {
            return("0", $txt{'eng_4'});
          }elsif( (($f_grade == 1)or($f_grade == 5)) and ($The_Course{id} !~ /^7102.1.$/) )  {
            return("0", $txt{'eng_5'}); 
          }else{
            ###  通過此檢查
          }
        }
      }
    }
  }

  #######################################################################################
  ### 語言中心應用英外語課程選課限制：依照預先匯入的分級名單，只有名單內的學生可選課  2010/12/29  Nidalap :D~
  if($SUPERUSER != 1) {
    if( $The_Course{id} =~ /^190(.)/) {               ### 應用英外語課程
      $apply_eng_level = $1;							###  此課程的等級( [基礎,中階,進階,高級] = [1,2,3,4] )
	  my @APPLY_ENG_LEVEL;
      if( $IS_ENGLISH ) {
	    @APPLY_ENG_LEVEL = ("", "Basic", "Intermediate", "Advanced", "Advanced");
	  }else{
	    @APPLY_ENG_LEVEL = ("", "基礎", "中階", "進階", "高級");
	  }
      
#       print("應用英外語課程...<BR>\n");
      Read_Apply_Eng_List(\%apply_eng_class, \%apply_eng_deduct);	###  讀取兩個名單

#	  Print_Hash(%apply_eng_class);
#	  print("<HR>");
#	  Print_Hash(%apply_eng_deduct);
#	  print("<HR>");
      $upper_limit_immune_flag = Check_Course_Upper_Limit_Immune( $The_Course{id}, $The_Course{group}, $stu_id);
#      print "limit immune = $upper_limit_immune_flag . <BR>";
	  
      if( $system_flags{current_system_timeline} >= 4 ) {
        if( $upper_limit_immune_flag != 1 ) {
          return("0", $txt{'eng_6'});
        }
      }else{
#        print "$apply_eng_class{$Student{id}} , $apply_eng_deduct{$Student{id}} <-- $apply_eng_level <BR>";
        if( !exists($apply_eng_class{$Student{id}}) and
            !exists($apply_eng_deduct{$Student{id}}) ) {			###  不是學程生，也不是修課抵畢業門檻名單
          return("0", $txt{'eng_7'});
        }else{														###  檢查英檢等級
#          print "checking $apply_eng_class{$Student{id}} , $apply_eng_deduct{$Student{id}} <-- $apply_eng_level <BR>";
          if( exists($apply_eng_class{$Student{id}}) ) {							###    學程生，檢查等級
            if( $apply_eng_level < $apply_eng_class{$Student{id}} ) {
              my $error_text = $txt{'eng_8'} . $APPLY_ENG_LEVEL[$apply_eng_class{$Student{id}}] 
       	                         . $txt{'eng_9'} . $APPLY_ENG_LEVEL[$apply_eng_level] . $txt{'eng_10'};
              return("0", $error_text);
            }
          }else{												###    抵免生，檢查等級
            if( ($apply_eng_level < $apply_eng_deduct{$Student{id}}) or ($apply_eng_level >=3 ) ) {
              my $error_text = $txt{'eng_8'} . $APPLY_ENG_LEVEL[$apply_eng_deduct{$Student{id}}] 
	                         . $txt{'eng_9'} . $APPLY_ENG_LEVEL[$apply_eng_level] . $txt{'eng_10'};
	      return("0", $error_text);
	    }
          }
        }
      }
      ###  語言中心課程，針對「修課抵畢業門檻」名單，限制每人只能選一門課程  2012/04/16 Nidalap :D~
      if( exists($apply_eng_deduct{$Student{id}}) ) {
        foreach $cos (@Course_of_Student) {		###  檢查學生已經選了的課
          if( $$cos{id} =~ /^190/ ) {
            return("0",  $txt{'eng_11'});
          }
        }
        foreach $cou (@Courses_) {			###  檢查學生本次所選的其他課
          if( $cou =~ /^190/ ) {
            my($temp_id,$temp_group) = split(/_/, $cou);
            next  if( ($temp_id eq $The_Course{id}) and ($temp_group eq $The_Course{group}) );
            return("0",  $txt{'eng_11'});
          }
        }
      }
    }
  }
  ######################################################################################
  ### 新增物理系「二一邊緣學生輔導」機制  Added 2011/02/10  Nidalap :D~
  if($SUPERUSER != 1) {
    #if( $Student{dept} eq $EARLY_WARNING_21_DEPT ) {		### 特定系所(目前只有物理系)
    if( is_Same_Dept($Student{dept}, $EARLY_WARNING_21_DEPT) ) {     ### 2016/12/20 改為透過 is_Same_Dept() 判斷相同系所
      my $error_text;
      $status = Early_Warning_21_Status($Student{id});
#      print(" status = $status<BR>\n");
      if( $status == 0 ) {
        $error_text = "
          您暫時無法選課，詳情如下：<BR>
          <TABLE border=1 width=75% bgcolor=LIGHTYELLOW>
            <TR><TD>
              親愛的同學:
              <P>
              本學期本系針對上學期二分之一不及格之同學開始實施選課輔導機制，
              請同學至系辦領取選課輔導審核表，
              經導師輔導及簽名後送回系辦，才能上網進行選課作業。
              <P>
              物理系關心你
            </TD></TR>
          </TABLE>
        ";
        return("0", $error_text);
      }
    }
  }
  ######################################################################################
  ###  因應選課改制，先搶先贏期間退選餘額延後釋出，新增加選前該科目是否在等待退選狀態中檢查。  Nidalap :D~
  foreach $cos ( @Course_of_Student2 ) {
    if( ($$cos{id} eq $The_Course{id}) and ($$cos{group} eq $The_Course{group}) ) {
	  $error_text = "您剛退選此課，系統尚在處理中，請稍後再行加選。";
	  return("0", $error_text);
	}
  }
  
  
  ######################################################################################
  ### 開給大一的軍訓課不准研究生選限制(Added 2004/06/07, Nidalap :D~)  <---  本規定已取消(2006/04/18, Nidalap :D~)
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
#####  Check_One_Course_Only
#####  檢查科目每學期限修一門的科目
#####  2012/02/15 增加 allow_concent，若為 1，可允許加簽開放。  Nidalap :D~
#####  2013/06/21 管理者外，暑修也不需檢查。 Nidalap :D~
sub Check_One_Course_Only
{
  my %The_Course = %{$_[0]};
  my @Course_of_Student = @{$_[1]};
  my @Courses_ = @{$_[2]};
  
  my @checks = (
    {"pat"=>"^903", "cou"=>"軍訓", "allow_concent"=>1},			###  軍訓課(Added 2010/01/06 Nidalap :D~)
    {"pat"=>"^7102[12]", "cou"=>"通識外語", "allow_concent"=>0},	###  通識外語課(Added 2010/09/02 Nidalap :D~)
    {"pat"=>"^7101", "cou"=>"中國語文知識與應用", "allow_concent"=>0}	###  Added 2010/12/08 Nidalap :D~
  );
  
#  print("正在檢查 $The_Course{id} <BR>\n");
  foreach $check (@checks)  {
    if( ($SUPERUSER != 1) and (!is_Summer()) ) {				###  管理者或暑修不需檢查 20130621加入暑修 Nidalap :D~
#	  print("正在檢查 $check : $$check{pat} _ $$check{cou}<BR>\n");
      $immune_flag = Check_Course_Upper_Limit_Immune($The_Course{id}, $The_Course{group}, $Student{id});
#      print "immune_flag = $immune_flag<BR>\n" . $The_Course{id} . $The_Course{group} . $Student{id};
      if( ($$check{"allow_concent"}==1) and $immune_flag ) {
        next;
      }else{
        if( ($The_Course{id} =~ /$$check{pat}/) ) {
          foreach $stu_course (@Course_of_Student) {	###   檢查學生已經選上了的課
#  		  print("正在檢查 $stu_course...<BR>");
            if( $$stu_course{id} =~ /$$check{pat}/ ) {
              return("0", "每一學期僅限修一門$$check{cou}課程!");
            }
          }
          foreach $stu_course (@Courses_) {			###   檢查學生本次所選的其他課
            my($temp_id,$temp_group) = split(/_/, $stu_course);
#            print("Checking ($temp_id eq $The_Course{id}) and ($temp_group eq $The_Course{group})<BR>\n");
            next  if( ($temp_id eq $The_Course{id}) and ($temp_group eq $The_Course{group}) );
            if( $temp_id =~ /$$check{pat}/ ) {
              return("0", "每一學期僅限修一門$$check{cou}課程!!");
            }
          }
        }
      }
    } 
  }
  return(1, "");
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
#####  Check_Credit_Upper_Limit()
#####  檢查學分上限(現在規定是25學分)
#####  除管理者外不得選修超過學分上限
#####  更新: 
#####    2001/09/04 考慮個別學生學分上限限制(在管理選單中設定) Nidalap
#####    2014/09/17 研究生學分上限預設為 20 by Nidalap :D~
#####  輸入: ($total_credit, $The_Course{credit})
#####  輸出: $limit_flag                   $limit_flag:(0,1) = (超過, 不超過)
############################################################################################
sub Check_Credit_Upper_Limit()
{
  my($upper_limit_file) = $REFERENCE_PATH . "credit_upper_limit.txt";
  my($temp_id, $temp_limit, $upper_limit);
  my( $student_id, $total_credit, $credit ) = @_;
  $upper_limit = 25;
  if( $student_id =~ /^[689]/ ) {		###  碩博士生預設為 20 學分
    $upper_limit = 20;
  }
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
  
  print qq[
    <html>
      <head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head>
      <body background="$GRAPH_URL./ccu-sbg.jpg">
        <center>
        $HEAD_DATA
        <hr><br>
        <font size=5>錯誤: $error_string</FONT><BR>
        <font size=5>請<a href="javascript:history.back()">重新選取</a></font>
        </center>
      </body>
    </html>
  ];
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
#  print("Check_Property ($Property,$MyProperty ) <BR>\n");
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
my(@TimeMap)=("A","1","2","3","4","B","5","6","7","8","C","D","E");
$use_cge_new_cate = Student_Suit_CGE_New_Category($Student{'id'});		###  判別學生是否適用 103 學年度後的通識「向度」

if($Input{dept} eq "" or $Input{grade} eq ""){   ####  並未選取系所年級  ####
    RESELECT($HEAD_DATA);                        ####  請重新選取        ####
}else{
    if( ($Input{dept} eq $DEPT_CGE) and ($use_cge_new_cate == 1) ) {
      if( $IS_MOBILE ) {                         ####  針對行動版網頁傳來的「年級」轉換向度
        if( $Input{'grade'} <=3 ) {              ####    基礎通識
          $Input{'cge_cate'} = 1;
          $Input{'cge_subcate'} = $Input{'grade'};
        }else{                                   ####    博雅通識
          $Input{'cge_cate'} = 2;
          $Input{'cge_subcate'} = $Input{'grade'} - 5;
        }
      }
	  my $cate = quotes($Input{'cge_cate'});
	  my $subcate = quotes($Input{'cge_subcate'});
       
	  print("cate, sub = [$cate, $subcate]<BR>\n") if $DEBUG;
	  #die("ccc") if( ($cate eq "") or ($subcate eq "") );
	  @Course=Find_All_Course_by_CGE_Category($cate, $subcate);
    }else{
	  @Course=Find_All_Course($Input{dept},$Input{grade},"");
	}
    $Count=@Course;
	
    if(($Count % 10) == 0 && ($Count != 0)){
      $TotalPages=int($Count/10);
    }else{
      $TotalPages=int($Count/10)+1;
    }

  if( $DEBUG ) {
    print("Count = $Count<BR>\n");
    print("Current_Page = $Current_Page<BR>\n");
  }
  
  if($Count != 0){                               ####  正常情況          ####
    ####  避免頁數超過  ####                     ####  可正常選課        ####
    while($Current_Page*10 >= $Count+10){
        $Current_Page--;
    }
  

  
  #####  是否顯示「開課學制」欄位(非專班的研究所)  2012/04/17  Nidalap :D~
  if( !$IS_GRA and !is_Undergraduate_Dept($Input{dept}) and !is_Exceptional_Dept($Input{dept}) ) {      
    $show_attr = 1;
  }else{ 
    $show_attr = 0;
  }

  if( $IS_MOBILE ) {			###  顯示行動化介面
    $mobile_temp = Create_jQuery_Mobile_Script(0);
    print qq(
      <html>
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	    $mobile_temp
        <TITLE>加選 - 選擇系所年級($Student{name})</TITLE>
      </head>
    );
    print Show_M_Javascript();
    print Create_jQuery_Mobile_Title_Tag();
    print Show_M_Form_Start();
  }
  
  #####  接下來處理顯示課表的 TABLE 的 HTML

    my $DATA   = "<TABLE width=100% border=1>\n";			###  要用來顯示的課程列表資料
	my $DATA_M = "<div data-role='collapsible-set' data-mini='true'  data-iconpos='none'>\n";
	
    $DATA = $DATA."<tr>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>" . $txt{"mark"} . "</font></th>";
    if( $concent_form_allowed == 1 ) {
      $DATA = $DATA."<th bgcolor=yellow><font size=2>" . $txt{"add_permission"} . "</font></th>";
    } 
    $DATA = $DATA."<th bgcolor=yellow><font size=2>" . $txt{"number_stu"} . "</font></th>";
    my $limit_state = Limit_State();				###  只有在先搶先贏階段要顯示
    if( ($system_flags{show_immune_count} == 1) and ($limit_state == 2) ) {
      $DATA = $DATA."<TH bgcolor=YELLOW><FONT size=2>" . $txt{"number_avail"} . "</FONT></TH>";
    } 
    if( $system_flags{show_last_total} == 1 ) {
      $DATA = $DATA."<th bgcolor=yellow><font size=2>" . $txt{"left_before"} . "</font></th>";
    }
    $DATA = $DATA."<th bgcolor=yellow><font size=2>" . $txt{"cname"} . "</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>" . $txt{"teacher"} . "</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>" . $txt{"class"} . "</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>" . $txt{"credit"} . "</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>" . $txt{"property"} . "</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>" . $txt{"weekday"} . "</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>" . $txt{"classroom"} . "</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>" . $txt{"property2"} . "</font></th>";
    if( $show_attr ) {
      $DATA = $DATA . "<th bgcolor=yellow><font size=2>" . $txt{"attr"} . "</font></th>";
    }
    $DATA = $DATA."<th bgcolor=yellow><font size=2>" . $txt{"syllabus"} . "</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>" . $txt{"note"} . "</font></th>";
    $DATA = $DATA."</tr>";

    @Course_of_Student = Course_of_Student($Student{id});  

    ####  限制相關頁數的科目  ####
    for($i=($Current_Page-1)*10; $i < $Count and $i < $Current_Page*10; $i++){
	   
	  #print "[i, Count, Current_Page] = [$i, $Count, $Current_Page]<BR>\n";
	  #print "i < Count = " . ($i<$Count) . "<BR>\n";
	  #print "i < Current_Page*10 = " . ($i<$Current_Page*10) . "<BR>\n";
	
	  %the_Course=Read_Course($Input{dept},$Course[$i]{id},$Course[$i]{group});
	  
	  my $DATA_ME = "<P>\n<TABLE width=100% border=1><TR>\n";	
	  #my $DATA_ME = "<DIV class='course_extra' id='course_extra_" . $the_Course{id}  . "_" . $the_Course{group} . "'>" .
	  #              "<TABLE width=100% border=1>\n";			###  要用來顯示的課程列表資料（行動版，點選科目後跳出來的額外資訊欄位）
      ####  開始讀取相關科目的相關資料，減少搜尋範圍，節省時間  ####
      
	  if( $i%2 == 1 ) {
	    $table_tr_bgcolor = "#F3D484";
	  }else{
	    $table_tr_bgcolor = "#EBF5FF";
	  }
      $ban_limit = Check_Ban_Limit(%the_Course);	###  若該科目擋修此學生，設定底色為灰色  added 2014/09/16 Nidalap :D~
	  if( $ban_limit == 1) {
	    $table_tr_bgcolor = "GRAY";
		$ban_cour_count++;
	  }

      $DATA   .= "<tr bgcolor=$table_tr_bgcolor>";                        ##  標記
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

      $DATA   .= "<th>";
	  $DATA_M .= "<div data-role='collapsible' data-collapsed='true'>\n";
	  $DATA_M .= "<H3><TABLE border=0 width='100%'>\n<TR><TD width=50>";
	  
#	  $temp_M .= "<div data-role='collapsible'>\n<H3>\n";
	  #$DATA_M .= "<TD><TABLE border=1 width='100%'><TR><TD width=20>";			###  為了顯示點選科目後顯示出來的 DIV，行動版的資料多深一層 TABLE
      if( ($view_only_flag<=1) and ($Flag == 1) ){		###  該門課已經選過了(只有在系統可查詢期間顯示)
          $DATA=$DATA."<img src=\"".$GRAPH_URL."flag.gif\">\n";		###  標示已選上的小紅旗子
		  $DATA_M .= "<img src=\"".$GRAPH_URL."flag.gif\">\n";
      }else{							###  該門課尚未選過
	    $DATA .= "<input type=checkbox name='course'
				         value='" . $the_Course{id}."_".$the_Course{group} .  "'" . $disabled_html . ">"; 	 ###  加選的核取方塊
		$DATA_M .= "<input type=checkbox name='course' class='course_checkbox' " .
		           "value='" . $the_Course{id}."_".$the_Course{group} .  "'" . $disabled_html . ">"; 	 ###  加選的核取方塊
      }
      $DATA   .= "</th>\n";
	  $DATA_M .= "</TD>\n";
      #################################################################################
      #####  加簽選項 Added 2011/07/29  Nidalap :D~
      my $concent_add_html = "<A href='Concent_Form_Apply1.php?session_id=" 
                       . $Input{session_id} . "&dept=" . $the_Course{dept} 
                       . "&cid=" . $the_Course{id} . "&grp=" . $the_Course{group} . "'>$txt{'add_permission'}</A>";

      $student_count = Student_in_Course($Input{dept}, $Course[$i]{id}, $Course[$i]{group});  
#      @Course_of_Student = Course_of_Student($Student{id});
      if( $concent_form_allowed == 1 ) { 	###  系統設定可加簽
        $apply_concent_flag = Stu_Can_Apply_Concent_Form(
                                     \%Student, \%the_Course, \@Course_of_Student, $student_count);
        if( $apply_concent_flag == 1 ) {
          $DATA   .= "<TD>$concent_add_html</TD>";
		  #$DATA_M .= "<TD>$concent_add_html</TD>";
        }else{
          $DATA   .=" <TD></TD>";
		  #$DATA_M .=" <TD></TD>";
        }
      }

      ###########  是否額滿註記 Added Feb 21,2000 Nidalap
#      $course_full_flag = Student_of_Course_Number($Input{dept}, $Course[$i]{id}, $Course[$i]{group});
#      $student_count = Student_in_Course($Input{dept}, $Course[$i]{id}, $Course[$i]{group});
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
      $DATA    .= "<TH>" . $student_count_show . "</TH>";
	  $DATA_ME .= "<TD><FONT size=2>目前人數：" . $student_count_show . "</FONT></TD>";
      
      #####################################################################   
      ### 要顯示可加選名額, 強制只有在先選先贏時才顯示
      if( ($system_flags{show_immune_count} == 1) and ($limit_state == 2) ) {
          my($immune_count, $available_count);
          $DATA    .= "<TH>";
		  $DATA_ME .= "<TD><FONT size=2>可加選名額：";
          $immune_count = Check_Course_Upper_Limit_Immune_Count($Course[$i]{id}, $Course[$i]{group}, "add");
          if( ($the_Course{number_limit} == 0) or ($the_Course{number_limit} == 999) ) {
            $DATA    .= "<FONT size=2>" . $txt{'unlimited'} . "</FONT>";
			$DATA_ME .= $txt{'unlimited'};
          }else{
            $immune_count = 0  if($immune_count <= 0);
            $available_count = $the_Course{number_limit} + $immune_count - $student_count;
            $available_count = 0  if( $available_count <= 0 );    ###  應該不會發生 :P
            if( $available_count == 0) {
              $available_count_show = "<FONT color=RED size=2>" . $available_count . "</FONT>";
            }else{
              $available_count_show = $available_count;
            }
            $DATA    .= $available_count_show;
			$DATA_ME .= $available_count_show;
          }
          $DATA    .= "</TH>";
		  $DATA_ME .= "</TD>";
      }
      #####################################################################
      if( ($system_flags{show_last_total} == 1) ) {  ### 要顯示上次篩選後餘額    
        $rest_count = Student_in_Course($Input{dept}, $Course[$i]{id}, $Course[$i]{group}, "last");
        $rest_count = $the_Course{number_limit} - $rest_count;
        $rest_count = 0  if($rest_count < 0);
        if( $rest_count == 0 ) {
          $DATA    .= "<FONT color=RED>";
		  $DATA_ME .= "<FONT color=RED>";
        }
        $rest_count = "<FONT size=2 color=BLACK>".$txt{'unlimited'}   if( $the_Course{number_limit} == 0 );
        $DATA    .= "<TH>" . $rest_count . "</TH>";
		$DATA_ME .= "<TD>上次篩選餘額: " . $rest_count . "</TH>";
      }
	  $DATA_ME .= "</TR><TR>\n";
      #####################################################################
      $DATA   .= "<th><font size=2>";
      $DATA   .= $the_Course{id};               ##  科目代碼
      #$DATA_M .= "<TD>(" . $the_Course{id} . "_" . $the_Course{group} . ")" . $the_Course{cname} . "</TD>";     ##  行動版科目代碼班別名稱
	  
	  #$DATA_M .= "<TD><FONT size=2><SPAN class='course_list' id='course_list_" . $the_Course{id}."_".$the_Course{group} . "'>";
	  #$DATA_M .= "(" . $the_Course{id} . "_" . $the_Course{group} . ")" . $the_Course{cname} . "</SPAN></FONT></TD>";     ##  行動版科目代碼班別名稱
	  $DATA_M .= "<TD><FONT size=2>(" . $the_Course{id} . "_" . $the_Course{group} . ")" . $the_Course{cname} . "</FONT></TD>";     ##  行動版科目代碼班別名稱
	  
	  if( $IS_ENGLISH ) { 
	    $DATA=$DATA."<br>".$the_Course{ename};     ##  科目名稱
	  }else{
	    $DATA=$DATA."<br>".$the_Course{cname};     ##  科目名稱
	  }
	  
      if( $the_Course{distant_learning} == 1 ) {        ##  如果是遠距教學or全英語授課, 註記之. 20090320
        $DATA .= "<BR><FONT color=RED>(遠距教學課程)";
      }
      if( $the_Course{english_teaching} == 1 ) {
        $DATA .= "<BR><FONT color=RED>(全英語授課/English-Taught Course)";
      } 
      $DATA=$DATA."</font></th>\n";

      $DATA    .= "<th><font size=2>";           ##  授課教師
	  $DATA_ME .= "<TR><TD><font size=2>教師：";
      $T=@{$the_Course{teacher}};

      for($teacher=0; $teacher < $T; $teacher++){
        $DATA=$DATA.$Teacher_Name{$the_Course{teacher}[$teacher]};
		if( $teacher == 0 )  { 
		  $DATA_ME .= $Teacher_Name{$the_Course{teacher}[$teacher]};
		  if( $teacher ==1 ) {
		    $DATA_ME .= "等";
		  }
		}
        if($teacher != $T-1){
          $DATA=$DATA.", ";
        }
      }
      $DATA    .= "</font></th>\n";
	  $DATA_ME .= "</font></TD>";
	  
	  $DATA   .= "<th><font size=2>" . $the_Course{"group"} . "</font></th>\n";		##  班別
	  
#      $DATA=$DATA."<th><font size=2>";
#      $DATA=$DATA.$the_Course{group};            ##  班別
#      $DATA=$DATA."</font></th>\n";
	  
	  
      $DATA=$DATA."<th><font size=2>";
      $DATA=$DATA.$the_Course{credit};           ##  學分數
      $DATA=$DATA."</font></th>\n";
	  
      $DATA_ME .= "<TD><font size=2>學分：" . $the_Course{credit} . "</font></TD>\n";
	  
      $DATA=$DATA."<th><font size=2>";
	  if( $IS_ENGLISH ) {						##  科目屬性
	    $DATA    .= $PROPERTY_TABLE_E[$the_Course{property}];
	  }else{
	    $DATA    .= $PROPERTY_TABLE[$the_Course{property}];
		$DATA_ME .= "<TD><font size=2>" . $PROPERTY_TABLE[$the_Course{property}] . "</FONT></TD>\n";
	  }

      $DATA=$DATA."</font></th>\n";

	  $time_string = Format_Time_String($the_Course{time});
      $DATA   .= "<th><font size=2>$time_string</font></th>\n";           ## 星期節次
	  $DATA_M .= "<TD width=60><font size=2>$time_string</font></TD>\n";           ## 行動版星期節次
      
      #$DATA .= $time_string;
      #$DATA   .= "</font></th>\n";

      
      %Room=Read_Classroom($the_Course{classroom});						##  教室
      $DATA    .= "<th><font size=2>" . $Room{name} . "</font></th>\n";
	  
	  $DATA_ME .= "</TR><TR><TD>教室：<font size=2>" . $Room{cname} . "</font></TD>";

      $DATA  =  $DATA."<th><font size=2>";##  學分歸屬
	  $DATA_M .= "<TD width=60>";
      if($Flag == 0){
        $DATA   .= Show_Property_Select();
		$DATA_M .= Show_Property_Select();
      }else{
	    if( $IS_ENGLISH ) {
		  $DATA   .= $PROPERTY_TABLE2_E{$Property};
		}else{
		  $DATA   .= $PROPERTY_TABLE2{$Property};
		  $DATA_M .= $PROPERTY_TABLE2{$Property};
		}
      }

      $DATA=$DATA."</font></th>\n";
	  $DATA_M .= "</TD>";
      ###  開課學制 2012/04/17 Nidalap :D~
      if( $show_attr ) {
        $DATA = $DATA . "<th><font size=2>" . 
				  ( $IS_ENGLISH ? $ATTR_E{$the_Course{attr}} : $ATTR{$the_Course{attr}} ). 
				"</font></th>\n";
      }      
      ###  課程大綱 Added 20080805 Nidalap :D~
      $DATA    .= "<th><font size=2>";
      $DATA    .= "<A href=\"".$ECOURSE_QUERY_COURSE_URL."&courseno=".$the_Course{id} . "_" . $the_Course{group} .
	              "&year=".$YEAR."&term=".$TERM."\" target=NEW>" . $txt{"syllabus"} . "</A>";
      $DATA    .= "</font></th>\n";
	  
	  $DATA_ME .= "<TD><A href=\"".$ECOURSE_QUERY_COURSE_URL."&courseno=".$the_Course{id} . "_" . $the_Course{group} .
	              "&year=".$YEAR."&term=".$TERM."\" target=NEW>" . $txt{"syllabus"} . "</A></TD>\n";

#      my($FILENAME)=$CLASS_URL."ShowNote.cgi";
      my($FILENAME)="ShowNote.cgi";
	  
	  $DATA    .= "<th><font size=2><a href='" . $FILENAME . "?user=" . $Input{id} . "&dept=" . $Input{dept} . 
                   "&course=" . $the_Course{id} . "&group=" . $the_Course{group} . "'>" . $txt{"note"} . "</a></font></th>\n";
      $DATA_ME .= "<TD><font size=2><a href='" . $FILENAME . "?user=" . $Input{id} . "&dept=" . $Input{dept} . 
                   "&course=" . $the_Course{id} . "&group=" . $the_Course{group} . "'>" . $txt{"note"} . "</a></font></TD></TR>\n";
	  
#      $DATA=$DATA."<th><font size=2>";
#      $DATA=$DATA."<a href=\"".$FILENAME."?";
#      $DATA=$DATA."user=";
#      $DATA=$DATA.$Input{id};
#      $DATA=$DATA."&dept=";
#      $DATA=$DATA.$Input{dept};
#      $DATA=$DATA."&course=";
#      $DATA=$DATA.$the_Course{id};
#      $DATA=$DATA."&group=";
#      $DATA=$DATA.$the_Course{group};
#      $DATA=$DATA."\">" . $txt{"note"} . "</a>";
#      $DATA=$DATA."</font></th>\n";

      $DATA    .= "</tr>";
	  #$DATA_ME .= "</TR></TABLE></DIV>";
	  $DATA_ME  .= "</TR></TABLE>\n</P>";
	  $temp_ME  .= "\n</P>\n";
	  
	  $DATA_M  .= "</TR></TABLE>\n</H3>\n\n" . $DATA_ME . "\n</DIV>\n\n";
	  $temp_M  .= "\n</H3>\n\n" . $temp_ME . "\n</DIV>\n\n";
	  
	}  ###  結束每一門課程的 for 迴圈

    $DATA   .= "</table>\n";
	#$DATA_M .= "</table>\n";
	$DATA_M .= "</DIV>\n";
	$temp_M .= "</DIV>\n";

	$temp = '
	<div data-role="collapsible-set">

	<div data-role="collapsible" data-collapsed="false">
	<h3>Section 1</h3>
	<p>I am the collapsible set content for section 1.</p>
	</div>
	
	<div data-role="collapsible">
	<h3>Section 2</h3>
	<p>I am the collapsible set content for section 2.</p>
	</div>
	</div>
	';
	
	
	if( $IS_MOBILE ) {
	  $DATA = $DATA_M;
	  #$DATA = $temp_M;
	  #$DATA = $temp; 
	}
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
  my($property_select, $graduate_select_under, $support_dept);
  my($fu_support, $double_support);				###  支援系所的輔系/雙主修
  $graduate_select_under = 0;

  if( ($Student{dept} =~ /6$/) and
      ( ($the_Course{dept} =~ /4$/)or($the_Course{dept} eq "7006")
        or($the_Course{dept} eq "I000")or($the_Course{dept} eq "V000")
        or($the_Course{dept} eq "Z121")or($the_Course{dept} eq "F000")  ) ) {
     $graduate_select_under = 1;                               ###  研究生修大學部課程
  }

  $property_select .= "<select name=\"$the_Course{id}_$the_Course{group}\" class='property_select'>\n";
#  $property_select .= "<option value=0>學分歸屬\n";
  
  %prop = $IS_ENGLISH ? %PROPERTY_TABLE2_E : %PROPERTY_TABLE2;
  
  if( (($the_Course{property} == 1) or ($SUPERUSER == 1)) and ($the_Course{dept} ne "7306") ) {
    if( $graduate_select_under != 1 ) {
      $property_select .= "<option value=1>" . $prop{1} . "\n";             ###  開為必修, 且不是學程的課
    }
  }
  if( (($the_Course{property} == 2) or ($SUPERUSER == 1)) and ($the_Course{dept} ne "7306") ) {
    if( $graduate_select_under != 1 ) {
      $property_select .= "<option value=2>" . $prop{2} . "\n";             ###  開為選修, 且不是學程的課
    }
  }
  if( ($the_Course{property} == 3) or ($SUPERUSER == 1) or ($the_Course{support_cge_type} ne "0") ) {
    if( $graduate_select_under != 1 ) {
      $property_select .= "<option value=3>" . $prop{3} . "\n";              ### 如果該科開為通識或支援通識
    }
  }
  if( ($the_Course{dept} ne "7306") and ($the_Course{dept} ne "I000") and ($the_Course{dept} ne "7006") ) {
                                                                ### 學程中心, 共同科, 通識中心開的課不得選為輔系
                                ###  讓支援系所的輔系/雙主修學生也能選擇輔系/雙主修 added 2009/02/23 Nidalap :D~
    foreach $support_dept (@{$the_Course{support_dept}}) {	  
      $fu_support=1      if($FU{$Student{id}}     eq $support_dept);
      $double_support=1  if($DOUBLE{$Student{id}} eq $support_dept);
    }
    if( ($FU{$Student{id}} eq $the_Course{dept}) or ($fu_support==1) or ($SUPERUSER == 1) ) {
      $property_select .= "<option value=4>" . $prop{4} . "\n";
    }
    if( ($DOUBLE{$Student{id}} eq $the_Course{dept}) or ($double_support==1) or ($SUPERUSER == 1) ) {
      $property_select .= "<option value=5>" . $prop{5} . "\n";
    }
  }
  if( $graduate_select_under == 1 ) {
    $property_select .= "<option value=6>" . $prop{6} . "\n";
  }

  if( $the_Course{dept} eq "7306" ) {                                ### 學程中心開的課才能選為學程
    $property_select .= "<option value=7>" . $prop{7} . "\n";
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

##### 已經搬到 System_Settings.pm   2009/06/04 Nidalap :D~
#sub is_Grade_Update()
#{
#  my($FileName)=$REFERENCE_PATH."Basic/GradeState";
#  open(FILE,"<$FileName")
#                   or die("Cannot open file $FileName!\n");
#  $State=<FILE>;
#  close(FILE);
#
#  return($State);
#}

########################################################################
####    產生該選擇的相關係所開課資料的 HTML 檔案                    ####
####    產生 table 的函式在上面                                     ####
########################################################################
sub DEPTS_COURSE
{
my($HEAD_DATA,$id,$password,$DATA)=@_;
my($NEXT_URL)="Add_Course01.cgi";
my($LINK)=Select_Course_Link($Input{id},$Input{password});
my($PRE_COURSE_WARNING, $SUP_COURSE_WARNING, $EDU_COURSE_WARNING, $MIL_COURSE_WARNING);

if($pre_course_count > 0) {        ###### 有先修科目的話, 顯示警訊html檔
  $PRE_COURSE_WARNING = qq(
    <SCRIPT language="javascript">
      messageWindow = open('Show_Special_Announce.php?type=prerequisite_msg', 'messageWindow', 'resizable=yes, width=250, height=250');
    </SCRIPT>
  );
}

if(defined($supported) and ($supported == 0)) {		##### 不支援本系的話, 顯示警訊html檔
  if( $system_flags{limit_number_state} == 0)  {	##### 前提二：目前系統採篩選制  
    if( is_Undergraduate_Dept($Input{dept})==1 ) {	##### 前提三：一般系所
      my($announce_title, $announce_content) =  Read_Special_Announce("not_supported");
      $SUP_COURSE_WARNING = Special_Announce_Table($announce_title, $announce_content);
	}
  }
}

if( $Input{dept} eq "7306" ) {     ######  修教育學程的課, 必須是教育學程的學生html warning
  my($announce_title, $announce_content) =  Read_Special_Announce("edu_msg");
  $COURSE_WARNING2 = Special_Announce_Table($announce_title, $announce_content);    
}

if( $Input{dept} eq "V000" ) {     ######  軍訓課程說明 (added 2006/11/14)
  my($announce_title, $announce_content) =  Read_Special_Announce("military_msg");
  $COURSE_WARNING2 = Special_Announce_Table($announce_title, $announce_content);
}

if( $Input{dept} eq "F000" ) {     ######  體育課程說明 (added 2006/11/24)  
  my($announce_title, $announce_content) =  Read_Special_Announce("physical_msg");
  $COURSE_WARNING2 = Special_Announce_Table($announce_title, $announce_content);
}

#####  2011/01/05 應惠如要求暫時移除  Nidalap :D~
#if( $Input{dept} eq "I001" ) {     ######  通識課程說明 (added 2009/12/29)  
#  my($announce_title, $announce_content) =  Read_Special_Announce("cge_msg");
#  $COURSE_WARNING2 = Special_Announce_Table($announce_title, $announce_content);
#}

if( $Input{dept} eq "Z121" ) {     ######  語言中心課程說明 (added 2006/12/26)
  $MIL_COURSE_WARNING = qq(
    <SCRIPT language="javascript">
      messageWindow = open('Show_Special_Announce.php?type=lang_msg','messageWindow', 'resizable=yes, width=800, height=600');
    </SCRIPT>
  );
  
  my($announce_title, $announce_content) =  Read_Special_Announce("lang_msg");
  $COURSE_WARNING2 = Special_Announce_Table($announce_title, $announce_content);
}

  ###############  依通識與否判別該顯示「第 X 年級」還是「第 X 領域」  20110310 Nidalap :D~
  if( $Input{dept} eq $DEPT_CGE ) {
    if( $use_cge_new_cate == 1 ) {					###  通識新制：顯示 XX 向度
	  $grade_show = " - " . $txt{'cge_subcate' . quotes($Input{'cge_cate'}) . '_' . quotes($Input{'cge_subcate'}) };
	}else{											###  通識舊制：顯示 XX 領域
      if( $Input{grade} == 2 ) {
	    #$grade_show = "第 2、5 領域";
	    $grade_show = $txt{'cge2'};
	  }else{
	    #$grade_show = "第" . $Input{grade} . "領域";
	    $grade_show = $txt{'cge'.$Input{'grade'}};
	  }
	}
  }else{											###  一般系所：顯示 XX 年級
    #$grade_show = $Input{grade} . "年級";
	#print "is under = " . is_Undergraduate_Dept($Input{dept});
    if( is_Undergraduate_Dept($Input{dept}) != 0 ) {
      $grade_show = $txt{'grade'.$Input{'grade'}};
    }else{
      $grade_show = $txt{'grade0'};;				###  研究所不顯示「年級」
    }
	#$grade_show = $txt{'grade'.$Input{'grade'}};
  }
  ##################################  顯示科目列表  ####################################
  if( $ban_cour_count >= 1 ) {
    $ban_cour_reminder = "<TR><TD>(以上灰色底色之課程為擋修科目，若需加選請於加簽開放時間申請加簽。)</TD></TR>";
  }else{
    $ban_cour_reminder = "";
  }
  if( $view_only_flag >= 1 ) {
    @warning_msg = ("非加退選期間", "目前不可加選，請於加退選期間加選課程。");
    if( $view_only_flag ==2 ) {
      $warning_msg[1] .= "<BR>因目前系統不開放查詢，科目列表中一律不顯示標示已選上的小紅旗。";
    }
    $VIEW_ONLY_WARNING = Special_Announce_Table(@warning_msg);
    $submit_html = "
              <tr>
              <th colspan=2>
                 <input type=submit value='目前不可加選' DISABLED>
              </th>
              </tr>";
  }else{
    $submit_html = "
              <tr> 
              <th colspan=2>
                 <input type=submit value='" . $txt{'submit_add'} . "'>
              </th>
              </tr>";
  }
  
  if( $IS_ENGLISH ) {
    $course_list_show = $grade_show . " of " . $SelectDept{'ename'};
	$input_hidden_e = "<INPUT TYPE='hidden' name='e' value='1'>";
  }else{
    $course_list_show = $SelectDept{'cname'} . $grade_show;
	$input_hidden_e = "<INPUT TYPE='hidden' name='e' value='0'>";
  }
  if( $IS_MOBILE ) {
    $input_hidden_m = "<INPUT TYPE='hidden' name='m' value='1'>";
  }else{
    $input_hidden_m = "<INPUT TYPE='hidden' name='m' value='0'>";
  }
  
  

  $switch_page = Create_Switch_Page_HTML();
  print "
    <html>
      <head>
        <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
        <Title>$course_list_show</Title>
      </head>
      <script language='javascript'>
        function FreeSelect(OBJ)
        {
            OBJ.page.value=3;
            OBJ.submit();
        }
      </script>
      $PRE_COURSE_WARNING	  
      $EDU_COURSE_WARNING
      $MIL_COURSE_WARNING
      
      <body background='$GRAPH_URL/ccu-sbg.jpg'>
        <center>
            $HEAD_DATA
        <hr>
        <br>
        <b>
        $COURSE_WARNING2
		$SUP_COURSE_WARNING
        $VIEW_ONLY_WARNING
        <font size=5>$course_list_show</font>
        </b>
        <br>
        <form action='$NEXT_URL' method='post' name='SelectForm'>
          <input type=hidden name='session_id' value='$Input{session_id}'>
          <input type='hidden' name='dept' value='$Input{dept}'>
          <input type='hidden' name='grade' value='$Input{grade}'>
		  <INPUT type='hidden' name='cge_cate' value='" . quotes($Input{'cge_cate'}) . "'>
		  <INPUT type='hidden' name='cge_subcate' value='" . quotes($Input{'cge_subcate'}) . "'>
          <input type='hidden' name='page' value='$Current_Page'>
		  $input_hidden_e
		  $input_hidden_m
          <input type='hidden' name='SelectTag' value=1>
          <table border=0 width=100%>
            <tr>
              <th colspan=2>
                $DATA
              </th>
            </tr>
			$ban_cour_reminder
            $submit_html
          </form>
              <tr>
                <th align=CENTER>
                  <form action='$NEXT_URL' method='post' name='NextForm'>
                    <input type=hidden name='session_id' value='$Input{session_id}'>
                    <input type='hidden' name='dept' value='$Input{dept}'>
                    <input type='hidden' name='grade' value='$Input{grade}'>
					<INPUT type='hidden' name='cge_cate' value='" . quotes($Input{'cge_cate'}) . "'>
					<INPUT type='hidden' name='cge_subcate' value='" . quotes($Input{'cge_subcate'}) . "'>
                    <input type='hidden' name='SelectTag' value=0>
                    <input type='hidden' name='page' value='$Current_Page'>
					$input_hidden_e
					$input_hidden_m
                    $switch_page
                </th>	
                  </form>
                <th align=right>
                  " . $txt{'page_number1'} . $Current_Page . "/" . $TotalPages . $txt{'page_number2'} . "
                </th>
              </tr>
        </table>
      </center>
      </body>
    </html>
  ";

}
#################################################################################
sub Create_Switch_Page_HTML
{
  my $html = "[";
  my $i, $i_max;

  
  my $target = "<A href='$NEXT_URL?session_id=" . $Input{session_id} . 
	           "&use_cge_new_cate=$use_cge_new_cate&m=$IS_MOBILE&dept=" . $Input{dept};
  #####  建立切換年級的選項 added 2015/01/14 Nidalap :D~
  if( is_Undergraduate_Dept($Input{dept}) ) {
    $i_max = 4;
  }else{
    $i_max = 2;
  }

  if( $Input{dept} ne $DEPT_CGE) {		###  為避免難以判斷的麻煩，通識課程不提供切換年級功能
    for($i=1; $i<=$i_max; $i++) {    
	  if( $IS_ENGLISH ) {   $html .= $target . "&grade=$i&e=1'>" . "year $i" . "</A>\n";  }
	  else				{   $html .= $target . "&grade=$i'>" . $GRADE[$i] . "</A>\n";  }
	  $html .= " | "  if( $i != $i_max );
    }
    $html .= "]<BR>\n[";
  }
  
  print("TotalPages = $TotalPages") if $DEBUG;
  #####  建立換頁的選項，修改於 2015/01/15 Nidalap :D~
  for( $p=1; $p<=$TotalPages; $p++ ) {
	#$TotalPages
    #$Current_Page
	if( $p == $Current_Page ) {
	  if( $IS_ENGLISH ) { $html .= "page $p\n"; }
	  else				{ $html .= "第 $p 頁\n"; }
	}else{ 
      $html .= $target . "&grade=" . $Input{grade} . "&page=" . $p;
	  if( ($Input{dept} eq $DEPT_CGE) and ($use_cge_new_cate == 1) ) {
		$html .= "&cge_cate=" . quotes($Input{'cge_cate'}) . "&cge_subcate=" . quotes($Input{'cge_subcate'});
	  }
	  if( $IS_ENGLISH ) { $html .= "&e=1'>page $p" . "</A>\n"; }
	  else				{ $html .= "'>第 $p 頁" . "</A>\n"; }
	  
	}
	$html .= " | "  if( $p != $TotalPages );
  }
  $html .= "]<BR>\n";
  
#  $html .=  "
#    <input type=button value='" . $txt{'last_page'} . "' onClick='javascript:history.back()'>
#    <input type=submit value='" . $txt{'next_page'} . "'>
#  ";
  return $html;


}
#################################################################################
sub RESELECT
{
my($HEAD_DATA)=@_;
print << "End_of_HTML"
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
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
  my $dept_grade_show;

  #print "is under = " . is_Undergraduate_Dept($Input{dept});
  if( is_Undergraduate_Dept($Input{dept}) != 0 ) {
    $dept_grade_show = $SelectDept{cname} . $Input{grade} . "年級";
  }else{
    $dept_grade_show = $SelectDept{cname};
  }

  if( length($Input{dept}) == 2 ) {               ###  跨領域學程
    $gro_url = "Show_All_GRO.cgi?session_id=$Input{session_id}&gro_no=$Input{dept}";
	$gro_url .= "&e=1"		if( $IS_ENGLISH );
    print "
      <html>                                   
        <head>
          <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
          <meta http-equiv='refresh' content='1; URL=$gro_url'>
          <Title>dept_grade_show 科目列表</Title>  
        </head>  
        <BODY background='$GRAPH_URL./ccu-sbg.jpg'>
          <CENTER>
		  " . $txt{'redirect2'} . "
		  <A href='Show_All_GRO.cgi?session_id=$Input{session_id}&gro_no=$Input{dept}'>" .  $txt{'redirect3'} . "</A>.
        </BODY>
      </HTML>
    ";
  }else{
    if( ($use_cge_new_cate == 1) and ($Input{dept} eq $DEPT_CGE) ) {
      $grade_show = $txt{"cge_subcate" . $Input{cge_cate} . "_" . $Input{cge_subcate}};
    }else{
      $grade_show = $Input{grade} . " 年級";
    }

    print "
      <html>
	  <head>
	    <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
	  </head>
	  <body background='$GRAPH_URL./ccu-sbg.jpg'>
	  <center>
	    $HEAD_DATA
	    <hr><br><br>
	    <font size=5>
		  " . $txt{'reselect'} . "
		</font>
	  </center>
	  </body>
      </html>
    ";
  }
}
######################################################################################
sub Special_Announce_Table()
{
  my ($announce_title, $announce_content) = @_;
  my $COURSE_WARNING2 = qq(
    <TABLE border=1 width=70% cellspacing=0>
      <TR><TH bgcolor=RED>$announce_title</TH></TR>
      <TR><TD bgcolor=LIGHTYELLOW>
    )
    . $announce_content
    . qq(        
      </TD></TR>
    </TABLE>
    <P>
  );
  return($COURSE_WARNING2);
}
##################################################################################

####################################################################################################
sub Show_M_Form_Start
{
#  my $html = qq|
#    <form action="Add_Course01.cgi" method="post" id=form1 data-ajax="false">
#    <input type=hidden name="session_id" value="$Input{session_id}">
#	<input type=hidden name="use_cge_new_cate" id="use_cge_new_cate" value="$use_cge_new_cate">
#    <input type=hidden name="m" value=1>
#    <input type='hidden' name='dept' value='$Input{dept}'>
#    <input type='hidden' name='grade' value='$Input{grade}'>
#	<INPUT type='hidden' name='cge_cate' value='" . quotes($Input{'cge_cate'}) . "'>
#	<INPUT type='hidden' name='cge_subcate' value='" . quotes($Input{'cge_subcate'}) . "'>
#    <input type='hidden' name='SelectTag' value=0>
#    <input type='hidden' name='page' value='$Current_Page'>
#	$input_hidden_e
#  |;
  
  my $html = qq|
    <form action="Add_Course01.cgi" method="post" id=form1 data-ajax="false">
    <input type=hidden name="m" value=1>
	    
    <input type='hidden' name='page' value='$Current_Page'>
	$input_hidden_e
  |;
  return $html;
}
####################################################################################################
sub Show_M_Form_End
{
  my $html = qq|
    <INPUT type='submit' value="檢視科目列表">
    </FORM>
  |;
  return $html;
}
####################################################################################################
sub Show_M_Grade_Sel
{
  my $html;
  
  my @grade = (1..4);
  
  $html = "<SPAN id='m_grade_caption'>年級</SPAN>：<SELECT data-role=select name='grade' id='m_grade_sel'>";
  foreach $grade (sort @grade) {
    $html .= "<OPTION value='$grade'>$grade	\n";
  }
  $html .= "</SELECT><P>\n";
  return $html;

}
####################################################################################################
#####  行動化介面的 Javascript
sub Show_M_Javascript
{
  my $html = "";
  #$html = qq|<SCRIPT type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js"></script>|;
  $html .= qq|
    <SCRIPT language="javascript">
	  \$(document).ready(function(){
		/////  以下是行動化專屬的 script
	    \$(".course_extra").hide();
		\$(".course_list").click(function(){
		  var element_id = \$(this).attr('id');
		  var cid   = element_id.substr(12,7);
		  var group = element_id.substr(20,2);
		  //alert(cid + "-" + group);
		  element_id = "course_extra_" + cid + "_" + group;
		  //alert(element_id);
		  var hidden = \$("#" + element_id).is(':hidden');
		  \$(".course_extra").hide();
		  if( hidden )  \$("#" + element_id).show();
		  else			\$("#" + element_id).hide();
		})
		/////  點選科目前的 checkbox，或者後面的學分歸屬 select 時，不要觸發 accordion 的展開事件
		\$('.course_checkbox').click(function(event){
		  event.stopPropagation();
        });
		\$('.property_select').click(function(event){
		  event.stopPropagation();
        });
		
	  });
	</SCRIPT>
	
	<STYLE type="text/css"> 
	  table { 
        border: 0; 
        font-family: arial; 
        font-size:14px; 
      } 
	</STYLE>
  |;
  return $html;
}

############################################################################################
#####  因應英文版本，將所有要顯示的文字在此整理，依照 $IS_ENGLISH 自動判別  2013/07/24
sub Init_Text_Values
{
  my %txtall;
  
  %txtall = (
	'class'		=> {'c'=>'班別', 'e'=>'Class'},
	'dept'		=> {'c'=>'系所', 'e'=>'Department'},
	'grade0'	=> {'c'=>'科目列表', 'e'=>'Course List'},
	'grade1'	=> {'c'=>'一年級科目列表', 'e'=>'Course List of 1st Year Standing'},
	'grade2'	=> {'c'=>'二年級科目列表', 'e'=>'Course List of 2nd Year Standing'},
	'grade3'	=> {'c'=>'三年級科目列表', 'e'=>'Course List of 3rd Year Standing'},
	'grade4'	=> {'c'=>'四年級科目列表', 'e'=>'Course List of 4th Year Standing'},
	'cge1'		=> {'c'=>'第一領域科目列表', 'e'=>'Course List of First General Education Course Module'},
	'cge2'		=> {'c'=>'第二、五領域科目列表', 'e'=>'Course List of Second and Fifth General Education Course Module'},
	'cge3'		=> {'c'=>'第三領域科目列表', 'e'=>'Course List of Third General Education Course Module'},
	'cge4'		=> {'c'=>'第四領域科目列表', 'e'=>'Course List of Fourth General Education Course Module'},

	'mark'		=> {'c'=>'標記', 'e'=>'Mark'},
	'add_permission'=> {'c'=>'加簽', 'e'=>'Add Permission'},
	'number_stu'=> {'c'=>'目前選修人數', 'e'=>'Number of Students Enrolled'},
	'number_avail'=> {'c'=>'可加選名額', 'e'=>'Vacancy Available'},
	'cname'		=> {'c'=>'科目名稱與代碼', 'e'=>'Course Title & ID'},
	'teacher'	=> {'c'=>'授課教師', 'e'=>'Instructor'},
	'class'		=> {'c'=>'班別', 'e'=>'Class'},
	'credit'	=> {'c'=>'學分', 'e'=>'Credit'},
    'property2'	=> {'c'=>'科目屬性', 'e'=>'Credit Type'},
	'property'	=> {'c'=>'學分歸屬', 'e'=>'Credit Type'},
    'weekday'	=> {'c'=>'星期節次', 'e'=>'Day/Period'},
    'classroom'	=> {'c'=>'教室', 'e'=>'Class Location'},
	'syllabus'	=> {'c'=>'課程大綱', 'e'=>'Syllabus'},
	'note'		=> {'c'=>'其他', 'e'=>'Remarks'},
	'submit_add'=> {'c'=>'加選以上標記科目', 'e'=>'Add all courses above with selection marks'},
	'last_page'	=> {'c'=>'上一頁', 'e'=>'Last Page'},
	'next_page'	=> {'c'=>'下一頁', 'e'=>'Next Page'},
	'page_number1'	=> {'c'=>'第', 'e'=>'Page'},
	'page_number2'	=> {'c'=>'頁', 'e'=>''},
	
	
	'nosel'		=> {'c'=>'目前非加退選時間，請勿加選！', 
	                'e'=>'System NOT available for course selection!'},
	
	'no_property' => {'c'=>'您選的科目未正確選取學分歸屬', 'e'=>'Please select credit type!'},
	'ban_dept' 	=> {'c'=>'您所選的科目<FONT color=RED>有擋修</FONT>, 以致於您無法加選', 
					'e'=>'Unable to add course due to forbidden department restrictions.'},
	'over_credit' => {'c'=>'您所選的科目<FONT color=RED>學分數已經過多</FONT>', 
					'e'=>'You have selected too many courses, '},
	'over_credit2'=> {'c'=>'<FONT color=RED>NOTE: 您選的學分數已經超過25學分!</FONT>', 
					'e'=>'You have selected too many courses(more than 25 credits), '},
	'no_avail'	=> {'c'=>'您選的科目<FONT color=RED>目前選課人數已滿,</FONT>',
					'e'=>'There is no vacancy available for this course, '},
	'no_course'	=> {'c'=>'您所選的系所年級無開課資料，請<A href="javascript:history.back()">重新選取</A>。',
					'e'=>'No course available, please <A href="javascript:history.back()">reselect</A>。'},
	'dept_serv_sel'	=> {'c'=>'您無法直接加選「系所服務學習課程」，請透過加簽處理！', 
					'e'=>'The course "Service Learning: Campus Service" cannot be selected at this time. 
						Please go through the additional signing process!'},
	'cge_no_4'	=> {'c'=>'第一階段通識課程不開放大四生修習!', 
					'e'=>'Senior Students are ineligible to choose G.E. courses during the first course selection period.'},
	'no_edu'	=> {'c'=>'教育學程開設科目, 限擁有教育學程資格者修習!', 
					'e'=>'Courses offered by the Educational Program for Teachers are only for students taking the program.'},
	'one_phy'	=> {'c'=>'每一學期僅限修一門必修體育課程!', 
					'e'=>'You can select only one required P.E course per semester!'},
	'no_phy_up'	=> {'c'=>'體育課程可下修, 但不可上修!', 
					'e'=>'P.E. courses can only be selected by students in the required year of study or above.'},
	'unlimited'	=> {'c'=>'無限制', 'e'=>'unlimited'},
	'left_before'=> {'c'=>'上次篩選後餘額', 'e'=>'Courses remaining after the previous screening process'},
	'attr'	=> {'c'=>'開課學制', 'e'=>'Course Regulations'},
	'redirect2'	=> {'c'=>'本頁將轉向所有跨領域學程網頁, 請稍後.<BR>如果網頁沒有轉向, 請', 
						'e'=>'This page will redirect to the course list of your selection. If redirection fails, please click '},
	'redirect3'	=> {'c'=>'這裡', 'e'=>'here'},
	'reselect'	=> {'c'=>'您所選的系所年級<br>本學期並未開課</font><br>請<a href="javascript:history.back()">重新選取</a>', 
						'e'=>'No course available for the department/year standing you selected.</font><br>
								Please <a href="javascript:history.back()">Re-select</a>'},
		
	'eng_1'		=> {'c'=>'您尚未參加新生英檢，無法加選此課程!', 
					'e'=>'You have not yet joined the English placement test for new students, ineligible to choose this course!'},
	'eng_2'		=> {'c'=>'您尚未通過新生英檢，無法加選此課程!', 
					'e'=>'You have not yet passed the English placement test for new students, ineligible to choose this course!'},
	'eng_3'		=> {'c'=>'您已經免修通識外語課，無法加選此課程!', 
					'e'=>'You have already succesfully waived the required G.E. foreign language courses, 
						ineligible to choose this course!'},
	'eng_4'		=> {'c'=>'您只能選修「強化」課程，無法加選此課程!', 
					'e'=>'You are only eligible to choose the "Intermediate" course, ineligible to choose this course!'},
	'eng_5'		=> {'c'=>'您只能選修「基礎」課程，無法加選此課程!', 
					'e'=>'You are only eligible to choose the "Pre-intermediate" course, ineligible to choose this course!'},
	
	'eng_6'		=> {'c'=>'第二階段選課不開放加選應用英外語課程，請辦理加簽，核可後方可選課!', 
					'e'=>'"Applied English" courses are not open for selection during the second course selection period. 
						Please go through the additional signing process.'},
	'eng_7'		=> {'c'=>'您並非應用英外語學程生，亦未申請修課抵畢業門檻，無法選修此課程!', 
					'e'=>'You are not a student of the English Deparment and have not applied the additional permission 
						for taking courses to fulfuill graduation requirements, ineligible to choose this course!'},
	'eng_8'		=> {'c'=>'您的英檢程度為', 'e'=>'Your English placement test result is '},
	'eng_9'		=> {'c'=>'不能選擇', 'e'=>' ineligible to choose a/an '},
	'eng_10'	=> {'c'=>'課程!', 'e'=>' course!'},
	'eng_11'	=> {'c'=>'每學期請勿選修超過一門語言中心課程！', 'e'=>'Language Center courses are limited to one per semester!'},
  );

  #####  處理通識向度的中英文資料
  foreach $cate (keys %category) {
    #print ("$cate : " . $category{$cate}{'cname'} . "<BR>\n");
	$txtall{'cge_new'.$cate} = {'c'=>$category{$cate}{'cname'}, 'e'=>$category{$cate}{'ename'}};
  }
  foreach $cate (keys %subcategory) {
    foreach $subcate (keys %{$subcategory{$cate}} ) {
	  #print ("$cate : $subcate : " . $subcategory{$cate}{$subcate}{'cname'} . "<BR>\n");
	  $txtall{'cge_subcate'.$cate.'_'.$subcate} = {'c'=>$subcategory{$cate}{$subcate}{'cname'}, 
												   'e'=>$subcategory{$cate}{$subcate}{'ename'}};
	}
  }
  
  foreach $k (keys %txtall) {
	if( $IS_ENGLISH ) {
	  $txt{$k} = $txtall{$k}{'e'};
	}else{
	  $txt{$k} = $txtall{$k}{'c'};
	}
  }

  #print "<meta http-equiv='Content-Type' content='text/html; charset=utf-8'>";
  #use Data::Dumper;
  #print Dumper(%txt);
  
  return %txt;  
}

