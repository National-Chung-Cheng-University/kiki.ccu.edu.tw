1;
#use encoding 'big5', STDIN => 'big5', STDOUT => 'big5';

######################################################################################################
#####     Reference.pm
#####     存放所有系統相關環境變數.
#####     Coder: Nidalap
#####     Updates :
#####       1998/12/28 Created
#####       ????/??/?? ...
#####       2009/06/06 透過 Determine_Account_Name() 決定 $ACCOUNT_NAME。從此以後，
#####		       程式可直接從測試帳號更新到正式帳號，不需手動更改該變數。  <-- 暫停使用 Nidalap :D~
#####	    2009/10/09 新增 $MIN_PASSWORD_LENGTH, $MAX_PASSWORD_LENGTH 兩個變數  
#####	    2009/10/29 新增學生密碼改用 MD5 編碼相關參數
######################################################################################################

$YEAR			=	105;		###  學年度(限數字)
$TERM			=	2;			###  學期(用來判斷的)
############################################################################
#####  目錄及URL設定

$ACCOUNT_NAME		=	"ccmisp06";
$DATABASE_TYPE		=	"postgresql";
#$ACCOUNT_NAME		=	Determine_Account_Name();

$MAIN_ACCOUNT1		=	"ccmisp06";
$MAIN_ACCOUNT2		=	"ccmisp07";    
$TEST_ACCOUNT		=	"ccmisp12";
$IS_GRA				=   is_GRA();				### 是否專班的 ccmisp07, 04, 09
$IS_MAIN_SYSTEM		=	is_Main_System();		### 是否 ccmisp06 或 07(06/07:傳回1; 測試:傳回-1; 其他:傳回0)
$IS_SUMMER			=	is_Summer();			### 是否暑修(0,1)
$SUB_SYSTEM			=	Determine_Sub_System();	### 子系統別： 1=一般; 2=暑修; 3=專班; 4=專班暑修

#$IS_GRA = 1;
#$SUB_SYSTEM = 3;
#$IS_SUMMER = 1;

$HOME_PATH			=	"/NFS/project/" . $ACCOUNT_NAME . "/";
$MAIN_HOME_PATH1	=	"/NFS/project/" . $MAIN_ACCOUNT1 . "/";
$MAIN_HOME_PATH2	=	"/NFS/project/" . $MAIN_ACCOUNT2 . "/";
$BIN_PATH           =       $HOME_PATH . "BIN/";
#$TEMP_PATH			=	$HOME_PATH . "WWW/Temp/";
$LIBRARY_PATH       =       $HOME_PATH . "LIB/";
$DATA_PATH			=	$HOME_PATH . "DATA/";
$REFERENCE_PATH		=	$DATA_PATH . "Reference/";
$PASSWORD_PATH		=	$DATA_PATH . "Password/";
$SESSION_PATH		=	$DATA_PATH . "Session_data/";    ### 2005/02/17
$BAN_LIST_PATH		=	$DATA_PATH . "Ban_List/";	 ### 2005/04/29
$MESSAGE_PATH		=	$DATA_PATH . "Public_Message/";
$TEMP_PATH			=	$DATA_PATH . "Temp";		 ### 2010/03/26
$WWW_PATH			=	$HOME_PATH . "WWW/";
$CGI_PATH			=	$HOME_PATH . "WWW/cgi-bin/";
$PDF_TEMP_PATH		=	$HOME_PATH . "WWW/PDF_temp/";

$STUDENT_PASSWORD_PATH	=	$PASSWORD_PATH . "student/";
$STUDENT_PASSWORD_MD5_PATH =	$PASSWORD_PATH . "student_MD5/";
$DEPT_PASSWORD_PATH		=	$PASSWORD_PATH . "dept/";
$DEPT_PASSWORD_MD5_PATH	=	$PASSWORD_PATH . "dept_MD5/";
$TEACHER_PASSWORD_PATH	=	$PASSWORD_PATH . "teacher/";
$LOG_PATH				=	$DATA_PATH . "LOGS/";
$COURSE_PATH			=	$DATA_PATH . "Course/";
$STUDENT_PATH			=	$DATA_PATH . "Student/";
$STUDENTS_OF_COURSE_PATH=	$DATA_PATH . "Student_of_course/";
$STUDENT_OF_COURSE_PATH	=       $DATA_PATH . "Student_of_course/";
$HISTORY_PATH			=	$DATA_PATH . "History/";
$HISTORY_COURSE_PATH	=	$HISTORY_PATH . "Course/";
$HISTORY_SOC_PATH		=	$HISTORY_PATH . "Student_of_course/";
$CHANGE_COURSE_PATH		=	$DATA_PATH."Change_Course/";
	
$KIKI_URL			=	"https://kiki.ccu.edu.tw/";
$HOME_URL			=	"https://kiki.ccu.edu.tw/~" . $ACCOUNT_NAME . "/";
$GRAPH_URL			=	$HOME_URL . "Graph/";
$CGI_URL			=	$HOME_URL . "cgi-bin/";
$PROJECT_URL		=	$CGI_URL . "project/";
$CLASS_URL			=	$CGI_URL . "class_new/";
$PDF_TEMP_URL		=	$HOME_URL . "PDF_temp/";
if( $IS_SUMMER ) {			###  2015/06/24 加入暑修判斷 by Nidalap :D~
  $ECOURSE_QUERY_COURSE_URL =	"http://ecourse2.ccu.edu.tw/php/Courses_Admin/guest3.php";
}else{
  $ECOURSE_QUERY_COURSE_URL =	"http://ecourse.ccu.edu.tw/php/Courses_Admin/guest3.php";
}
$ECOURSE_QUERY_COURSE_URL .=	"?PHPSESSID=0466f8e4b492c9294334e34ad49e1de8";
$TITLE_LINE		=	$GRAPH_URL . "line.gif";

###########  非一般系所或者較特殊的單位  ############################################
$DEPT_CGE		=	"I001";		### 通識中心
$DEPT_EDU		=	"7306";		### 師資培育中心
$DEPT_LAN		=	"Z121";		### 語言中心
$DEPT_MIL		=	"V000";		### 軍訓
$DEPT_PHY		=	"F000";		### 體育中心
$DEPT_PHYSICS	=	"2204";		### 物理系
$EARLY_WARNING_21_DEPT	=	$DEPT_PHYSICS;	### 21學生預警功能 - 目前只有物理系

###########################################################################
#####  $TERM學期可能的值分別為1, 2, 3(第1學期, 第2學期, 暑修)
#####  
@SUB_SYSTEM_NAME	=	("", "", "暑修", "專班", "專班暑修");
@TERM_NAME			=	("", "第1學期", "第2學期", "暑修");

$SUB_SYSTEM_NAME	=	$SUB_SYSTEM_NAME[$SUB_SYSTEM];
$YEAR_NAME			=	'九十';		###  學年度(中文)(尚未用到)
$TERM_NAME			=	$TERM_NAME[$TERM];
$USE_MD5_PASSWORD	=	0;		### 啟用MD5學生密碼，而非DES(added 20091029)
$TIME_OUT_SECONDS	=	1200;            ### xx 秒後 session time out(預設 600)
$SESSION_CLEAR_SECONDS	=	660;		### 清除超過 xx 秒的 session files(預設 660)
$ADD_COURSE_LIMIT	=	200;		### 一個 session 內最多加選次數(預設 200)
$BAN_DURATION		=	60*60*8;	### 因不當加選而停權的時間(秒數)(預設 60*60*8)
$BAN_COUNT_LIMIT	=	7;		### 超過此次數的異常加選, 才有可能被停權(需配合系統設定的黑名單開放與否)(預設30)
$BAN_COUNT_LIMIT2	=	5;		### 超過此次數的異常加選, 會看到警告訊息(需配合系統設定的黑名單開放與否)(預設10)

$SHOW_LAST_TOTAL	=	1;		### 加選時顯示上次篩選後名額
$ALLOW_PRE_ENTRANCE_STUDENT_TEMP	= 0;    ###  提早入學學生可以選課
                                                ###  (2003/02/14暫時做的違章建築)
$MIN_PASSWORD_LENGTH	=	6;		### 密碼最小長度
$MAX_PASSWORD_LENGTH	=	8;		### 密碼最大長度

$DEPT_SERV_CODE			=	"888";	### 系所服務學習課程流水號(ex:中文系 = 1104888)
    
#$TEMP_FLAG_20040225	=	0;		### 公告錯誤退選 flag
#$TEMP_FLAG_CHANGE_PASS	=	0;		### 將預設密碼改為生日
#$TEMP_REMEDY_20040224	=	0;		### 補救 20040224 事件
$TEMP_RESTRICT_DEPT     =	0;      ### 畢業資格審核表限中文/政治/資工系檢視
$TEMP_INFOTEST_MSG		=	0;		### 顯示資訊能力測驗的公告


##########################################################################

@AVAILABLE_CLASSES	=	('A','B');	### 所有可能的班級(學生班級，非開課班級)
@PROPERTY_TABLE		=	("", "必修", "選修", "通識");
@PROPERTY_TABLE_E	=	("", "Required", "Elective", "Gen Edu");
%PROPERTY_TABLE2    =   (
							"1" => "必修",         "2" => "選修",          "3" => "通識",
                            "4" => "輔系",         "5" => "雙主修",        "6" => "大學部課程",
                            "7" => "教育學程",     "8" => "不列入畢業學分",
                            "A" => "必修(抵免)",   "B" => "選修(抵免)",
                            "9" => "棄選"
                        );
%PROPERTY_TABLE2_E  =   (
							"1" => "Required",      "2" => "Elective",       "3" => "Gen Edu",
                            "4" => "Minor",         "5" => "Double Major",   "6" => "Undergraduate",
                            "7" => "Education",     "8" => "不列入畢業學分",
                            "A" => "Required(deduct)", "B" => "Elective(deduct)",
                            "9" => "Withdrawal"
                        );

if( $IS_GRA )		{ $PROPERTY_TABLE2{4} = "基礎課程"; }

@WEEKDAY		=	("", "一","二","三","四","五","六","日");
@WEEKDAY_E		=	("", "Mon.","Tue.","Wed.","Thur.","Fri.","Sat.","Sun.");
@GRADE			=	("", "一年級", "二年級", "三年級", "四年級");
@GRADE_E		=  ("", "freshman", "sophomore", "junior", "senior");
%WEEKDAY_REGION		=	("1"  =>  "1", "3"  =>  "1", "5"  =>  "1",
                                 "2"  =>  "2", "4"  =>  "2");
@REGION			=	("I","II","III","IV","V");
@TIMEMAP50		=	(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15);
@TIMEMAP75		=	(A,B,C,D,E,F,G,H,I,J);
@REGION			=	("I", "II", "III", "IV", "V");
@REGION_TIME		=	("07:10~10:00", "10:10~13:00", 
                                 "13:10~16:00", "16:10~19:00", "19:10~22:00");
###  各個截次的時間(給人參考用, 不做衝堂判斷)
%TIME_TIME		=	(
                                 "1" => "07:10~08:00", "2" => "08:10~09:00", "3" => "09:10~10:00",
                                 "4" => "10:10~11:00", "5" => "11:10~12:00", "6" => "12:10~13:00",
                                 "7" => "13:10~14:00", "8" => "14:10~15:00", "9" => "15:10~16:00",
                                 "10" => "16:10~17:00", "11" => "17:10~18:00", "12" => "18:10~19:00",
                                 "13" => "19:10~20:00", "14" => "20:10~21:00", "15" => "21:10~22:00",
                                 "A" => "07:15~08:30", "B" => "08:45~10:00",
                                 "C" => "10:15~11:30", "D" => "11:45~13:00", 
                                 "E" => "13:15~14:30", "F" => "14:45~16:00",
                                 "G" => "16:15~17:30", "H" => "17:45~19:00", 
                                 "I" => "19:15~20:30", "J" => "20:45~22:00"
                                );
###  各個截次(time)所屬的區段(region)
%REGION_TIME_TABLE	=	("1"  =>  "0",  "2" =>  "0",  "3" =>  "0",
                                 "4"  =>  "1",  "5" =>  "1",  "6" =>  "1",
                                 "7"  =>  "2",  "8" =>  "2",  "9" =>  "2",
                                 "10" =>  "3", "11" =>  "3", "12" =>  "3",
                                 "13" =>  "4", "14" =>  "4", "15" =>  "4",
                                 "A"  =>  "0",  "B" =>  "0",
                                 "C"  =>  "1",  "D" =>  "1",
                                 "E"  =>  "2",  "F" =>  "2",
                                 "G"  =>  "3",  "H" =>  "3",
                                 "I"  =>  "4",  "J" =>  "4"
                                );
###  各個區段內的截次. [...] 之內的順序, 相鄰者必衝堂, 用作衝堂判斷.
@TIME_REGION_TABLE	=	(
				  ["1", "A", "2", "B", "3"],
				  ["4", "C", "5", "D", "6"],
				  ["7", "E", "8", "F", "9"],
				  ["10", "G", "11", "H", "12"],
				  ["13", "I", "14", "J", "15"]
				);

@PRINCIPLE		=	("不需篩選", "一次篩選", "二次篩選");
%PREREQUISITE_LOGIC		=	("AND" => "所有先修條件都必須符合",  "OR"  => "只要符合任一先修條件");
%PREREQUISITE_LOGIC_E	=	("AND" => "All must be satisfied",  "OR"  => "One of which satisfied");
%GRADE			=	( "40" => "40分以上", 
                                  "50" => "50分以上",
                                  "60" => "60分以上",
                                  "70" => "70分以上", 
                                  "80" => "80分以上",
                                  "pass" => "及格", 
                                  "0" => "曾經修習");
%GRADE_E		=	( "40" => "above 40", 
                                  "50" => "above 50",
                                  "60" => "above 60",
                                  "70" => "above 70", 
                                  "80" => "above 80",
                                  "pass" => "passed", 
                                  "0" => "taken");
%S_MATCH		=	( "0" => "--請選擇符合程度--",
                                  "1" => "100%符合",
                                  "2" => "90%符合",
                                  "3" => "80%符合",
                                  "4" => "70%符合",
                                  "5" => "60%符合",
                                  "6" => "60%以下符合",
                                  "7" => "教師待聘" );
%ATTR			=	( "0" => "--請選擇開課學制--",
                                  "1" => "碩士班課程",
                                  "2" => "博士班課程",
                                  "3" => "碩博合開" );
%ATTR_E			=	( "0" => "--請選擇開課學制--",
                                  "1" => "Open for Graduate students",
                                  "2" => "Open for Ph.D students",
                                  "3" => "Open for both Graduate and Ph.D students" );

if( $DATABASE_TYPE eq "postgresql" ) {
  $charset = "utf-8";
}else{
  $charset = "big5";
}
$EXPIRE_META_TAG	= "
      <meta http-equiv=\"Content-Type\" content=\"text/html; charset=" . $charset  . "\">
      <META HTTP-EQUIV=\"Pragma\" CONTENT=\"NO-CACHE\">
      <META HTTP-EQUIV=\"expires\" CONTENT=\"-1\">
      ";
$EXPIRE_META_TAG2	= "
      <HEAD>
        <META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">
        <META HTTP-EQUIV=\"Expires\" CONTENT=\"-1\">
      </HEAD>
      ";
$LOG_IGNORE_IP = "140.123.26.154";	###  LOG 中將此 IP 相關資訊過濾掉不紀錄
      
#######################################################################################################
#####  Determine_Account_Name()
#####  依照環境變數的 SCRIPT_FILENAME，判別此系統的所屬帳號
sub Determine_Account_Name
{
  my($account_name, $base_account_name, @dir);
  
  $base_account_name = "ccmisp";
#  print("filename = $ENV{'SCRIPT_FILENAME'}<BR>\n");
  
  @dir = split(/\//, $ENV{'SCRIPT_FILENAME'});
  foreach $dir (@dir) {
#    print("checking $dir...<BR>\n");
    if( $dir =~ /$base_account_name/ ) {
      $account_name = $dir;
      return($account_name);
    }
  }
  die("CRITICAL INTERNAL ERROR! CANNOT DETERMINE ACCOUNT NAME!")  
}
#######################################################################################################
#####  is_GRA()
#####  檢查本子系統是否專班學生使用
sub is_GRA
{
  my $is_gra;

  if( ($ACCOUNT_NAME eq $MAIN_ACCOUNT2) or ($ACCOUNT_NAME eq "ccmisp04") or ($ACCOUNT_NAME eq "ccmisp09") ) {
    $is_gra = 1;
  }else{
    $is_gra = 0;
  }
  return($is_gra);
}
########################################################################################################
#####  is_Summer()
#####  檢查本子系統是否暑修使用
sub is_Summer
{
  my $is_summer;

#  if( (($SUB_SYSTEM==2) or ($SUB_SYSTEM==4)) or ($TERM==3) ) {
  if( $TERM==3 ) {
    $is_summer = 1;
  }else{
    $is_summer = 0;
  }
  return($is_summer);
}
#########################################################################################################
#####  is_Main_System()
#####  檢查本子系統是否為正式上下學期使用(ccmisp06的一般生 和 07的專班生, 上下學期使用)
sub is_Main_System
{
  my $is_main_system;
  if( ($ACCOUNT_NAME eq $MAIN_ACCOUNT1) or ($ACCOUNT_NAME eq $MAIN_ACCOUNT2) ) {
    $is_main_system = 1;
  }elsif( $ACCOUNT_NAME eq $TEST_ACCOUNT ) {
    $is_main_system = -1;
  }else{
    $is_main_system = 0;
  }
  return($is_main_system);
}
#########################################################################################################
#####  Determine_Sub_System()
#####  檢查本子系統是那個子系統
#####  [1,2,3,4] = [一般生, 一般生暑修, 專班, 專班暑修]
sub Determine_Sub_System
{
  my $sub_system;
  
  if( $IS_GRA ) {
    if( $IS_SUMMER ) {
	  $sub_system = 4;		###  專班暑修
	}else{
	  $sub_system = 3;		###  專班上下學期
	}
  }else{
    if( $IS_SUMMER ) {
	  $sub_system = 2;		###  一般生暑修
	}else{
	  $sub_system = 1;		###  一般生上下學期
	}
  }
  return $sub_system;
}