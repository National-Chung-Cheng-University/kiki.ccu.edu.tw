<?PHP

///////////////////////////////////////////////////////////////////////////////////////////////////////
/////     Reference.php
/////     存放所有系統相關環境變數.
/////     Coder: Nidalap
/////     Updates :
/////       20??/??/?? Created
/////       ????/??/?? ...
/////       2009/06/06 透過 Determine_Account_Name() 決定 $ACCOUNT_NAME。從此以後，
/////                  程式可直接從測試帳號更新到正式帳號，不需手動更改該變數。  Nidalap :D~
/////       2009/10/29 新增學生密碼改用 MD5 編碼相關參數
///////////////////////////////////////////////////////////////////////////////////////////////////////
  
  $ACCOUNT_NAME			=	"ccmisp06";
//  $ACCOUNT_NAME			=	Determine_Account_Name();

  $YEAR				=	105;				///  學年度(限數字)
  $TERM				=	2;					///  學期(用來判斷的)

  $MAIN_ACCOUNT1		=	"ccmisp06";		///  一般生主要帳號(上下學期)
  $MAIN_ACCOUNT2		=	"ccmisp07";		///  專班主要帳號(上下學期)
  $SUMMER_ACCOUNT		=	"ccmisp05";		///  一般生暑修帳號
  $SUMMER_ACCOUNT_GRA	=	"ccmisp09";		///  專班暑修帳號
  $ACCOUNTS				=	array($MAIN_ACCOUNT1, $MAIN_ACCOUNT2, $SUMMER_ACCOUNT, $SUMMER_ACCOUNT_GRA);
  $TEST_ACCOUNT			=	"ccmisp12";
  $IS_MAIN_SYSTEM		=	is_Main_System();		/// 是否 ccmisp06 或 07(06/07:傳回1; 測試:傳回-1; 其他:傳回0)

  $HOME_PATH			=	"/NFS/project/" . $ACCOUNT_NAME . "/";
  $MAIN_HOME_PATH1		=	"/NFS/project/" . $MAIN_ACCOUNT1 . "/";
  $MAIN_HOME_PATH2		=	"/NFS/project/" . $MAIN_ACCOUNT2 . "/";
  $LIBRARY_PATH			=	$HOME_PATH . "LIB/";
  $DATA_PATH			=	$HOME_PATH . "DATA/";
  $SESSION_PATH			=	$DATA_PATH . "Session_data/";
  $REFERENCE_PATH		=	$DATA_PATH . "Reference/";
  $BAN_LIST_PATH		=	$DATA_PATH . "Ban_List/";
  $MESSAGE_PATH			=	$DATA_PATH . "Public_Message/";
  $WWW_PATH			=	$HOME_PATH . "WWW/";
  $COURSE_PATH			=       $DATA_PATH . "Course/";
  $STUDENT_PATH			=	$DATA_PATH . "Student/";
  $HISTORY_PATH			=       $DATA_PATH . "History/";
  
  $KIKI_URL			=	"https://kiki.ccu.edu.tw/";
  $HOME_URL			=	"https://kiki.ccu.edu.tw/~" . $ACCOUNT_NAME . "/";
  $CLASS_URL			=	$HOME_URL . "cgi-bin/class_new/";
  $QUERY_URL			=	$HOME_URL . "cgi-bin/Query/";
  $GRAPH_URL			=	$HOME_URL . "Graph/";
//  $TEMP_20070904_FLAG		=       1;              // 20070904 在新生選課時舊生誤入而被回復的警訊. 顯示於 announce.php

  /////  非一般系所的單位
  $DEPT_CGE               =       "I001";         /// 通識中心
  $DEPT_EDU               =       "7306";         /// 師資培育中心
  $DEPT_LAN               =       "Z121";         /// 語言中心
  $DEPT_MIL               =       "V000";         /// 軍訓
  $DEPT_PHY               =       "F000";         /// 體育中心
  $DEPT_PHYSICS           =       "2204";         /// 物理系

  $TEST_STU_ID		  =	  "999999999"; 	  /// 測試學生帳號
  $DEPT_SERV_CODE	  =	  "888";	  /// 系所服務學習課程流水號(ex:中文系 = 1104888)
  ///  設定 PHP session save path 到 NFS，以避免不同主機上 session 資料不同步的問題
  session_save_path("/NFS/session"); 

  date_default_timezone_set("Asia/Taipei");
  //  將 "上學期查詢系統" 與 "暑修系統" 密碼資料導到正式系統上.

  $IS_GRA			=	is_GRA();
  $IS_SUMMER			=	is_Summer();

  if( ($ACCOUNT_NAME == "ccmisp03") or ($ACCOUNT_NAME == "ccmisp05")  ) {
    $STUDENT_PASSWORD_PATH	=	"/ultra2/project/" . $MAIN_ACCOUNT1 . "/DATA/Password/student/";
    $STUDENT_PASSWORD_MD5_PATH	=	"/ultra2/project/" . $MAIN_ACCOUNT1 . "/DATA/Password/student_MD5/";
    $DEPT_PASSWORD_PATH		=	"/ultra2/project/" . $MAIN_ACCOUNT1 . "/DATA/Password/dept/";
    $DEPT_PASSWORD_MD5_PATH	=	"/ultra2/project/" . $MAIN_ACCOUNT1 . "/DATA/Password/dept_MD5/";
    $LOG_PATH			=	"/ultra2/project/" . $MAIN_ACCOUNT1 . "/DATA/LOGS/";
    $LOG_PATH1			=	"/ultra2/project/" . $MAIN_ACCOUNT1 . "/DATA/";
  }else if( ($ACCOUNT_NAME == "ccmisp04") or ($ACCOUNT_NAME == "ccmisp09") ) {
    $STUDENT_PASSWORD_PATH	=	"/ultra2/project/" . $MAIN_ACCOUNT2 . "/DATA/Password/student/";
    $STUDENT_PASSWORD_MD5_PATH	=	"/ultra2/project/" . $MAIN_ACCOUNT2 . "/DATA/Password/student_MD5/";
    $DEPT_PASSWORD_PATH		=	"/ultra2/project/" . $MAIN_ACCOUNT2 . "/DATA/Password/dept/";  
    $DEPT_PASSWORD_MD5_PATH	=	"/ultra2/project/" . $MAIN_ACCOUNT2 . "/DATA/Password/dept_MD5/";
    $LOG_PATH			=	"/ultra2/project/" . $MAIN_ACCOUNT2 . "/DATA/LOGS/";
    $LOG_PATH1			=	"/ultra2/project/" . $MAIN_ACCOUNT2 . "/DATA/";
  }else{
    $STUDENT_PASSWORD_PATH	=	$DATA_PATH . "Password/student/";
    $STUDENT_PASSWORD_MD5_PATH	=	$DATA_PATH . "/Password/student_MD5/";
    $DEPT_PASSWORD_PATH		=       $DATA_PATH . "Password/dept/";
    $DEPT_PASSWORD_MD5_PATH	=       $DATA_PATH . "Password/dept_MD5/";
    $LOG_PATH			=	$DATA_PATH . "LOGS/";
    $LOG_PATH1			=	$DATA_PATH;
  }
  
  $DATABASE_TYPE		= "postgresql";
  //$DATABASE_TYPE		= "sybase";
  
  if( $ACCOUNT_NAME == $TEST_ACCOUNT ) {	// 判斷是否使用測試資料庫
    $USE_TEST_DATABASE = 1;
  }else{
    $USE_TEST_DATABASE = 0;
  }

  if( $USE_TEST_DATABASE == 1 ) {
    $DATABASE_IP		=	"140.123.30.9:4100";    // Glacier 的測試資料庫
    if( $IS_GRA == 1 ) {					    // 專班
      $DATABASE_NAME		=	"academic_gra";
    }else{							    // 一般
      $DATABASE_NAME		=	"academic";
    }
  }else{
    $DATABASE_IP		=	"140.123.30.7:4100";	// Obelisk 的正式資料庫
    if( $IS_GRA == 1 ) {					    // 專班
      $DATABASE_NAME		=	"academic_gra";
    }else{							    // 一般
      $DATABASE_NAME		=	"academic";
    }
  }
  if( $DATABASE_TYPE == "postgresql" ) {
    if( $USE_TEST_DATABASE == 1 ) {
	  $DATABASE_IP		=	"140.123.26.159";	// postgreSQL 的測試資料庫
	  //$DATABASE_IP		=	"140.123.30.12";	// postgreSQL 正式資料庫
	}else{
      $DATABASE_IP		=	"140.123.30.12";	// postgreSQL 正式資料庫
	}
  }
  
  $KIKI_DB_NAME			=	"academic_kiki";	// 選課專用資料庫
  $PUBLIC_DB_NAME		=	"public_run";		// 共同資料庫, 讀部份資料用
  $PERSONNELDB_DB_NAME	=	"personneldb";      // 人事資料庫, 教師資料  
  
  $TABLE['STD_REC']		=	"a11tstd_rec";		// 學籍 table
  $TABLE['DEPT']		=	"h0rtunit_a_";		// 系所代碼 table
  $TABLE['PASSWORD']	=	"a11vpasswd";		// 更改密碼的 view
  $TABLE['EMAIL']		=	"a11vemail";		// 更改 email 的 view
  $TABLE['NETLOG']		=	"a11tuser_netlog";	// 更改密碼的 LOG

  $DEPT_PHYSICS			=	"2204";			// 物理系
  $EARLY_WARNING_21_DEPT	=	$DEPT_PHYSICS;		// 21 學生預警功能 - 目前只有物理系

  $BG_PIC	= $HOME_URL . "Graph/ccu-sbg.jpg";
  $TITLE_PIC	= $HOME_URL . "Graph/title.gif";

  $SYSADM_EMAIL			=	"nidalap@ccu.edu.tw";  // 管理者 email 嚴重錯誤自動通知用(added 20100323)
  $USE_MD5_PASSWORD		=	0;		// 啟用MD5學生密碼，而非DES(added 20091029)
  $BAN_DURATION			=       60*60*8;        // 因不當加選而停權的時間(秒數)
  $BAN_COUNT_LIMIT		=       10;             // 超過此次數的異長加選, 才有可能被停權(需配合系統設定的黑名單開放與否)
  $REFRESH_TIME_BOOKMARK	=       180;            // bookmark.php 的自我更新時間
  $REFRESH_TIME_SYSTEM_STATE 	=       180;            // system_state.php 的自我更新時間
  $TIME_OUT_SECONDS		=	600;		// xx 秒後 session time out
  $PASSWORD_MAX_CHANGE_TIME	=	60*60*24*30*3;	// 密碼建議該更新了(三個月)(秒數)
  $PASSWORD_MAX_CHANGE_TIME2	=       30*6;		// 密碼強迫該更新了(六個月)(天數)
  $MIN_PASSWORD_LENGTH		=	4;		// 密碼最短長度
  $MAX_PASSWORD_LENGTH		=	10;		// 密碼最長長度
  
  if( $DATABASE_TYPE == "postgresql" ) {
    $charset = "utf-8";
  }else{
    $charset = "big5";
  }
  $EXPIRE_META_TAG		= "
      <meta http-equiv=\"Content-Type\" content=\"text/html; charset=" . $charset . "\">
      <META HTTP-EQUIV=\"Pragma\" CONTENT=\"NO-CACHE\">
      <META HTTP-EQUIV=\"expires\" CONTENT=\"-1\">";
  $PROPERTY_TABLE		=	array("", "必修", "選修", "通識");
  $PROPERTY_TABLE2              =       array("1" => "必修",         "2" => "選修",          "3" => "通識",
                                              "4" => "輔系",         "5" => "雙主修",        "6" => "大學部課程",
                                              "7" => "教育學程",     "8" => "不列入畢業學分",
                                              "A" => "必修(抵免)",   "B" => "選修(抵免)",
                                              "9" => "棄選"
                                        );
  if( $IS_GRA )  $PROPERTY_TABLE2["4"] = "基礎課程";		// 專班的 4 為「基礎課程」

  $LOG_IGNORE_IP		=	"140.123.26.154";	// LOG 中將此IP資訊隱藏不紀錄
  $IP_SSO_FORMAL		=	"140.123.4.205";	// SSO 正式平台 IP
  $IP_SSO_TEST			=	"140.123.4.217";	// SSO 測試平台 IP
  $IP_ACADEMIC_FORMAL		=	"";
  $IP_ACADEMIC_TEST		=	"";

///  各個截次的時間(給人參考用, 不做衝堂判斷)
$TIME_TIME              =       array(
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

$WEEKDAY		=	array("", "一","二","三","四","五","六","日");
$ATTR                   =       array( "0" => "--請選擇開課學制--",
                                       "1" => "碩士班課程",
                                       "2" => "博士班課程",
                                       "3" => "碩博合開" );


////////////////////////////////////////////////////////////////////////////////////////////////////////
/////  Determine_Account_Name()
/////  依照環境變數的 SCRIPT_FILENAME，判別此系統的所屬帳號
function Determine_Account_Name()
{
  $base_account_name = "ccmisp";
  $script_filename = getenv("SCRIPT_FILENAME");
//  print("filename = $filename<BR>\n");

  $dir = preg_split("/\//", $script_filename);

  foreach ( $dir as $subdir) {
//    print("checking $subdir...<BR>\n");
    if( preg_match("/$base_account_name/", $subdir ) ) {
      $account_name = $subdir;
      return($account_name);
    }
  }
  die("CRITICAL INTERNAL ERROR! CANNOT DETERMINE ACCOUNT NAME!");
}


////////////////////////////////////////////////////////////////////////////////////////// 
/////  is_GRA()
/////  由 global 的帳號名稱 $ACCOUNT_NAME, 判斷此子系統是否屬於專班使用
/////  2005/10/13 Nidalap :D~
function is_GRA()
{
  global $ACCOUNT_NAME, $MAIN_ACCOUNT1, $MAIN_ACCOUNT2;
  if( ($ACCOUNT_NAME == $MAIN_ACCOUNT2) or ($ACCOUNT_NAME == "ccmisp04") or ($ACCOUNT_NAME == "ccmisp09") ) {
    $is_gra = 1;    
  }else{
    $is_gra = 0;
  }
  return($is_gra);
}
/////////////////////////////////////////////////////////////////////////////////////////
/////  is_Summer()
/////  由 global 的變數 $TERM, 判斷本子系統是否暑修使用
/////  2009/07/07 Nidalap :D~  
function is_Summer()
{
  global $TERM;

  if( $TERM == 3 ) {
    $is_summer = 1;
  }else{
    $is_summer = 0;
  }
  return($is_summer);
}

/////////////////////////////////////////////////////////////////////////////////////////
/////  is_Main_System()
/////  檢查本子系統是否為正式上下學期使用(ccmisp06的一般生 和 07的專班生, 上下學期使用)
function  is_Main_System()
{
  global $ACCOUNT_NAME, $MAIN_ACCOUNT1, $MAIN_ACCOUNT2, $TEST_ACCOUNT;
  
  if( ($ACCOUNT_NAME == $MAIN_ACCOUNT1) or ($ACCOUNT_NAME == $MAIN_ACCOUNT2) ) {
    $is_main_system = 1;
  }else if( $ACCOUNT_NAME == $TEST_ACCOUNT ) {
    $is_main_system = -1;
  }else{
    $is_main_system = 0;
  }
  return($is_main_system);
}


/////////////////////////////////////////////////////////////////////////////////////////
function Get_System_State()
{
  global $ACCOUNT_NAME, $REFERENCE_PATH;
  
  /// 讀取 SysState
  $state_file = $REFERENCE_PATH . "Basic/SysState";
  $SYSSTATE = fopen($state_file, "r") or Error("Internal error: Cannot read state_file!\n");
  list($system_settings{'sysstate'})	= fscanf($SYSSTATE, "%s\n");
  fclose($SYSSTATE);

  /// 讀取 LimitNumberState
  $state_file = $REFERENCE_PATH . "Basic/LimitNumberState";
  $SYSSTATE = fopen($state_file, "r") or Error("Internal error: Cannot read limit_number_state_file!\n");
  list($system_settings{'limit_number_state'})    = fscanf($SYSSTATE, "%s\n");
  fclose($SYSSTATE);  

  /// 讀取 System_Settings.txt
  $setting_file = $REFERENCE_PATH . "System_Settings.txt";
  $SETTING = fopen($setting_file, "r") or Error("Internal error: Cannot read setting file!\n");
  while( list($key,$value) = fscanf($SETTING, "%s\t%s\n") ) {
    $system_settings{$key} = $value;
  }
  fclose($SETTING);
  
  return $system_settings;
}
//////////////////////////////////////////////////////////////////////////////////////////
  /////////////////////////////////////////////////////////////////////////////
  /////  起始並設定 Smarty
  /////  輸入值： $version 預設為 2，若為 3 則使用 Smarty 3
  function init_smarty($version=2)
  {
    global $HOME_PATH, $LIBRARY_PATH;
    if( $version == 3 ) {
      $smarty_php = $LIBRARY_PATH . "Smarty-3.1.7/libs/Smarty.class.php";
//      echo "3";
    }else{
      $smarty_php = "Smarty.class.php";
    }
//    echo "require $smarty_php";
    require_once("$smarty_php");

    $smarty = new Smarty;
    $smarty->template_dir       = $HOME_PATH . "smarty/templates";
    $smarty->compile_dir        = $HOME_PATH . "smarty/templates_c";
    $smarty->cache_dir          = $HOME_PATH . "smarty/cache";
    $smarty->config_dir         = $HOME_PATH . "smarty/configs";

    $smarty->left_delimiter     = "{{";
    $smarty->right_delimiter    = "}}";

//    if( !$SYS["system_official"] )  $smarty->caching = 0;
	
	return $smarty;
  }
//////////////////////////////////////////////////////////////////////////////////////////
/////  引用 jquery、jquery-ui、highcharts 等 javascript 套件
function Include_jQuery($include_highcharts=0)
{
  $html = '
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
	<link rel="stylesheet" href="//ajax.googleapis.com/ajax/libs/jqueryui/1.11.1/themes/smoothness/jquery-ui.css" />
    <script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.11.1/jquery-ui.min.js"></script>
  ';
  
  if( $include_highcharts == 1 ) {
    $html .= '<script src="http://code.highcharts.com/highcharts.js"></script>';
	$html .= '<script src="http://code.highcharts.com/modules/exporting.js"></script>';
  }
  return $html;
}
  

?>