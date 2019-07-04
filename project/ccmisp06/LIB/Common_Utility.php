<?PHP

//////////////////////////////////////////////////////////////////////////////////////////
/////  印出顯示 OnlineHelp 的 Javascript 程式碼
/////  updated 2009/10/28  Nidalap :D~
function ShowOnlineHelpJS()
{
  echo "
  <SCRIPT language='javascript'>
    function OnlineHelp(anchor)
    {
       var link= '../../online_help.html#' + anchor;
       window.open(link, 'ExplainWindow', 'resizable=yes, width=450,height=400, scrollbars=yes, resizable=yes');
    }
  </SCRIPT>
  ";
}
//////////////////////////////////////////////////////////////////////////////////////////
/////  傳回兩個 time_string 傳回值, 分別給 kiki 的 Student.log, 
/////  以及資料庫的 NETLOG 使用.
/////  2005/08/28 Nidalap :D~
function gettime($login_time = NULL)
{
  if( floor(phpversion()) >= 5 ) {
    date_default_timezone_set("Asia/Taipei");
  }
  if( $login_time == NULL ) {
    $time = localtime();
  }else{
    $time = localtime($login_time);
  }
//  print_r($time);

  $year		= $time[5] + 1900;
  $month	= $time[4] + 1;
  $mday		= $time[3];
  $hour		= $time[2];
  $min		= $time[1];
  $sec		= $time[0];
  
/*  if( $hour >12 ) {
    $hour2 = $hour - 12;
    $ampm  = "pm";
  }else{
    $hour2 = $hour;
    $ampm  = "am";
  }
*/  
  if( strlen($min) == 1 ) { $min = "0" . $min; };
  if( strlen($hour) == 1 ) { $hour = "0" . $hour; };
  
  $time_string = $month . "/" . $mday . "/" . $year . " " . $hour . ":" . $min;
  $time_string2 = $year . "/" . $month . "/" . $mday . " " . $hour . ":" . $min . ":" . $sec;
  $time_string3 = $year . "/" . $month . "/" . $mday;
/*
  echo("time_string = $time_string<BR>\n");
  echo("time_string2 = $time_string2<BR>\n");
*/  
  return array ($time_string, $time_string2, $time_string3);
}
//////////////////////////////////////////////////////////////////////////////////////////
function Form_Head_Data($id, $name, $dept, $grade, $class)
{
  global $IS_ENGLISH;
  if( $IS_ENGLISH ) {
    $cols = array("Name", "Student ID", "Department", "Year Standing", "Class");
  }else{
    $cols = array("姓名", "學號", "系所", "年級", "班別");
  }
  $HEAD_DATA = "<table width=800 border=0>
  <tr>
    <th>" . $cols[0] . ": $name</th>
    <th>" . $cols[1] . ": $id</th>
    <th>" . $cols[2] . ": $dept</th>
    <th>" . $cols[3] . ": $grade</th>
    <th>" . $cols[4] . ": $class</th>
  </tr>
  </table>";
  
  return($HEAD_DATA);
}

//////////////////////////////////////////////////////////////////////////////////////////
function Error_Please_Report($error_code)
{
//  echo("<P><LI><FONT color=RED>密碼更改失敗!</FONT> 您的密碼沒有完全更新成功! ");
  echo("<LI>請勿關閉此畫面, 立即聯絡系統管理人員, 告知底下的錯誤碼!<P>");
  echo("錯誤碼: <FONT color=RED>$error_code</FONT><P>");
  Print_Contact("fatal");
  exit();
}

//////////////////////////////////////////////////////////////////////////////////////////
function Print_Contact($reason)
{
  echo("<LI>電算中心: 李永祥(分機: 14203, email: nidalap@ccu.edu.tw)<BR>");
  echo("<LI>教務處: 11207, 11212, 11213<BR>");
}

//////////////////////////////////////////////////////////////////////////////////////////
/////  Generate_Key()
/////  由學號, 密碼, 與大略的時間產生一個 md5 過的 key, 作為基本的安全保護,
/////  避免有心者直接連結改密碼網頁, 看到學生的部份個人資訊.
/////  輸入：[使用者學號, 系統間約定好的通關密碼 (, 是否上一個時間區間, 上一頁產生時的 timestamp)]
/////  Coder: Nidalap :D~, 2006/05/19
function Generate_Key($id, $password, $last_time_period=0, $time)
{
  $debug_flag = 0;
  
  if( !isset($time) )  {				//  如果上一頁有傳 timestamp，則不切除
	$time = time();
	$time = substr($time, 0, 7);		//  切掉後三碼的 timestamp, 允許約 16 分鐘的時間差
  }  
  
  if( $last_time_period == 1 ) {	//  無此參數時，若上個系統的網頁與現在時間不在同一區間，會 key error
    $time--;						//  若此參數=1，可抓取上一個區間的時間，供額外判斷用。  2014/07/01 Nidalap :D~
  }

  if( $password == "" ) {		//  如果沒有傳入 password, 使用預設密碼 
    $password = "ThiS_is_pAsswOrd_for_InfOtEst";
  }
  $key = $id . $time . $password;
  $key = md5($key);
  
  if( $debug_flag == 1 ) {
    echo("[ id,time,password,key ] = [ $id,$time,$password,$key ]<BR>\n");
  }

  return $key;
}
//////////////////////////////////////////////////////////////////////////////////////////
/////  依照 $id, $password 產生秘密 $key，檢查 $key 是否正確
/////  2014/07/01 加入 in_key2 的判別，避免 key_error 訊息 by Nidalap :D~
function Check_Key($key, $id, $password)
{
  global $EXPIRE_META_TAG;
  $in_key  = Generate_Key($id, $password);
  $in_key2 = Generate_Key($id, $password, 1);
  $debug_flag = 0;

  if( !( ($in_key==$key) or ($in_key2==$key) )  ) {
    global $BG_PIC;

    echo("<HTML><HEAD>$EXPIRE_META_TAG<TITLE>輸入資訊錯誤</TITLE></HEAD>");
    echo("<BODY background=$BG_PIC>");
    echo("<Center><H1>輸入資訊錯誤<hr></H1>");
    echo("您輸入的資訊有誤, 若見到此訊息, <BR>請於上班時間電洽教務處教學組或電算中心, 並告知底下的錯誤訊息:<p>");
    echo("錯誤訊息: <FONT color=RED>KEY_ERROR</FONT><P>");
    if( $debug_flag == 1 ) {
      echo("[in_key, key] = [$in_key, $key]<BR>\n");
    }
    exit(2);
  }else{
    return;
  }
}
///////////////////////////////////////////////////////////////////////////////////////////
/////  Check_HTTP_REFERER
/////  從外部系統連過來的, 檢查哪些來源是安全的
/////  目前可能連過來的系統:
/////    學籍
/////  Nidalap 2015/02/26  :D~
function Check_HTTP_REFERER()
{
  $referer = $_SERVER["HTTP_REFERER"];
  $check_succeed_flag = 0;
  
  print_r($_SERVER);

  $allowed_referers = array(
    'http://mis.cc.ccu.edu.tw/~paccount01/profession/'
  );

  foreach( $allowed_referers as $ip ) {
    if(preg_match("/$ip/", $referer))   $check_succeed_flag = 1;
    echo("$referer <-> $ip: $check_succeed_flag<BR>\n");
  }

#  return($check_succeed_flag);
  return(1);
  
}
/////////////////////////////////////////////////////////////////////////////////////////////
function Check_Sourse_URL()
{
  
}
///////////////////////////////////////////////////////////////////////////////////////////
/////  Read_Announce_Board
/////  讀取系統公佈欄

function Read_Announce_Board()
{
  global $REFERENCE_PATH;
  $board_file = $REFERENCE_PATH . "Login_Message.txt";
  if( file_exists($board_file) ) {
    $text = file_get_contents($board_file);
//    $text = preg_replace("/\n/", "<BR>", $text);
    return($text);
  }else{
    echo("內部錯誤: 無法讀取系統公佈欄! 請洽系統管理人員!<P>\n");
    return;
  }

/*  open(BOARD, $board_file) or
      Fatal_Error("Cannot read file $board_file in Modify_login_Message.cgi!");
  @temp = <BOARD>;
  close(BOARD);
  $text = join("", @temp);
  $text =~ s/\n/<br>\n/g;
  return $text;
*/
}

////////////////////////////////////////////////////////////////////////////////////////////
function Read_Announce_Index()
{
  global $MESSAGE_PATH, $IS_ENGLISH;
  $DIR = opendir($MESSAGE_PATH);
  
  while( $announce_id = readdir($DIR) ) {
    if( ($announce_id == ".") or ($announce_id == "..") )	continue;		/// 過濾系統目錄檔案
	if( preg_match("/_e\.txt$/", $announce_id) )			continue;		/// 暫先過濾英文公告檔案
    $date = substr($announce_id, 0, 8);
    $date = preg_replace("/^(....)(..)(..)/", "$1/$2/$3", $date);
    
	
	$announce_id = preg_replace("/.txt/", "", $announce_id);
	$file_e = $MESSAGE_PATH . $announce_id . "_e.txt";
	$file_c = $MESSAGE_PATH . $announce_id . ".txt";
	
//	echo "announce_id = $announce_id<BR>\n";
//	echo "file_c = $file_c<BR>\n";
//	echo "file_e = $file_e<P>\n";
	
	if( $IS_ENGLISH ) { 
	  if( file_exists($file_e) ) {
	    $handle = fopen($file_e, "r");
	  }else{
		$handle = fopen($file_c, "r");
	  }
	}else{
	  $handle = fopen($file_c, "r");
	}
    $title = fgets($handle);   $title = trim($title, "\n");
    $sticky = fgets($handle);  $sticky = trim($sticky, "\n");
    
	//echo "[title, sticky] = [$title, $sticky]<BR>";
	
    $announce[$sticky][$announce_id]["announce_id"] = $announce_id;
    $announce[$sticky][$announce_id]["date"] = $date;
    $announce[$sticky][$announce_id]["title"] = $title;
  }
  
  rsort($announce["off"]);
//  print_r($announce);
//  print_r($announce["on"]);
//  echo "<HR>\n";
//  print_r($announce["off"]);

  $text = "";  
  $sticky_text = $IS_ENGLISH ? "sticky" : "置頂";
  
  foreach ($announce["on"] as $item) {					###  置頂
      $announce_id = $item["announce_id"];  
      $date = $item["date"];
      $title = $item["title"];
      $text .= "<TR><TD align=CENTER>$date</TD>";
      $text .= "<TD><FONT color=RED>($sticky_text)</FONT><A href=\"announce.php?announce_id=$announce_id&e=$IS_ENGLISH\">$title</A></TD></TR>";
  }
  
  foreach ($announce["off"] as $item) {                                  ###  沒置頂
      $announce_id = $item["announce_id"];   
      $date = $item["date"]; 
      $title = $item["title"]; 
      $text .= "<TR><TD align=CENTER>$date</TD>";        
      $text .= "<TD><FONT color=RED></FONT><A href=\"announce.php?announce_id=$announce_id&e=$IS_ENGLISH\">$title</A></TD></TR>";
  }

  return($text);
}
////////////////////////////////////////////////////////////////////////////////////////////
function Read_Announce_Content($announce_id)
{
  global $MESSAGE_PATH, $IS_ENGLISH;

  $announce_id = addslashes($announce_id);  		// 基本的安全檢查
  
  ///  判斷讀取中文或者英文資料
  if( $IS_ENGLISH )	$file = $MESSAGE_PATH . $announce_id . "_e.txt";
  else				$file = $MESSAGE_PATH . $announce_id . ".txt";
  
  //echo "trying to get file $file...<BR>\n";
  if( file_exists($file) ) {

    $handle = fopen($file, "r");
    $title = fgets($handle);
    $sticky = fgets($handle);
    $date = substr($announce_id, 0, 8);
    $date = preg_replace("/^(....)(..)(..)/", "$1/$2/$3", $date);
    
    $content = "<PRE>";
    while( $line = fgets($handle) ) {
      $content .= $line;
//      $content .= "<BR>";
    }
    $content .= "</PRE>\n";
	
	$back = $IS_ENGLISH ? "BACK" : "回上一頁";
    $content .= "<CENTER><A href=\"announce.php?e=$IS_ENGLISH&m=$IS_MOBILE\">$back</A></CENTER>";
          
  }
  return array($title, $date, $sticky, $content);
}

///////////////////////////////////////////////////////////////////////////////////////////
/////  Read_Special_Announce
/////  讀取特定公告內容
/////  2008/05/27, Nidalap :D~
function Read_Special_Announce($type)
{
  global $REFERENCE_PATH; 
  $announce_map =  array(
    "lang_msg"          => "lang_msg.txt",
    "physical_msg"      => "physical_msg.txt",
    "military_msg"      => "military_msg.txt",              
    "edu_msg"           => "edu_msg.txt",
    "prerequisite_msg"  => "prerequisite_msg.txt"
                      );

  $announce_file = $REFERENCE_PATH . $announce_map{$type};
//  echo("reading file $announce_file...<BR>\n");
  
  $SPECIAL_ANNOUNCE = fopen($announce_file, "r");
  $title = fgets($SPECIAL_ANNOUNCE);

  while ($line =fgets($SPECIAL_ANNOUNCE)) {
    $announce .= preg_replace("/\n/", "<BR>\n", $line);
  }
  fclose(SPECIAL_ANNOUNCE);                  

  return array($title, $announce);
}

////////////////////////////////////////////////////////////////////////////////////////////
/////  Last_Semester
/////  傳回上 n 個學期的學年學期值
/////  Updates:
/////    2007/06/05 Created by Nidalap :D~
/////    2009/12/29 可輸入參數 $n，用來傳回上 n 個學期的學年學期  Nidalap :D~
function Last_Semester($n)
{
  global $YEAR, $TERM;

  $year = $YEAR; $term = $TERM;
  for($i=0; $i<$n; $i++) {
    $term--;
    if( $term == 0 ) {
      $year--;
      $term = 2;
    }
  }
  return array($year, $term);
}

////////////////////////////////////////////////////////////////////////////////////// 
///// Recent_Semesters
///// 傳回最近 $n 個學期的學年學期陣列(由早到晚)
///// 若 $m 不為空，則傳回前 $n 個學期 ~ 後 $m 個學期的陣列
///// ex: 若 $n=1  傳回三個值的陣列： [上學期、本學期、下學期]
/////     若 $n=2, $m=1 : 傳回 [上學期、本學期、下學期、下下學期]
///// Updates:
/////  2016/02/03  從課程地圖系統複製過來 by Nidalap :D~
function Recent_Semesters($n, $m=NULL)
{
    global $SYS;
    $j=0;
    if( !isset($m) ) {
      for($i=$n; $i>=-$n; $i--, $j++) {
        list($y,$t) = Last_Semester($i);
        $yearterm[$j]["y"] = $y;
        $yearterm[$j]["t"] = $t;
      }
    }else{
      for($i=$m; $i>=-$n; $i--, $j++) {
        list($y,$t) = Last_Semester($i);
        $yearterm[$j]["y"] = $y;
        $yearterm[$j]["t"] = $t;
      }
    }
    return $yearterm;
}

##############################################################################
#####  Show_Online_Help
#####  產生前往線上說明 javascript 的連結
#####  2008/06/043, Nidalap :D~
function Show_Online_Help($anchor)
{
  ShowOnlineHelpJS();
  $show = "<A href=\"javascript:OnlineHelp('$anchor')\"><FONT color=BLUE>[?]</FONT></A>";
  return($show);
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////  檢查使用者輸入資料
/////  Updates:
/////    2009/10/07 Created by Nidalap :D~
function Validate_Input($field, $type)
{
  global $MAX_PASSWORD_LENGTH, $MIN_PASSWORD_LENGTH;
  $valid_errors = 0;                            ///  預設通過

  $field = quotes($field);
  switch($type) {
    case "id":                                  ///  檢查學號
      if( strlen($field)!=9 )  {                        //  長度必須為九碼
        $valid_errors++;
        $valid_error[] = "學號應為九碼半形數字";
      }
      if( !preg_match("/^[4,5,6,8,9]/", $field) ) {	//  必須以 4,5,6,8,9 開頭
        $valid_errors++;
        $valid_error[] = "請輸入正確學號";
      }
      break;
    case "password":
      if( (strlen($field)>$MAX_PASSWORD_LENGTH) or (strlen($field)<$MIN_PASSWORD_LENGTH) ) {
        $valid_errors++;				//  密碼長度過長或過短
        $valid_error[] = "密碼長度過長或過短";
      }
      break;

  }
  /////  檢查錯誤數量，顯示錯誤訊息
  if( $valid_errors > 0 ) {
    Show_Input_Error_Message($valid_error);
  }
  return;
}
////////////////////////////////////////////////////////////////////////////////////////////////
/////  Compare_Dates()
/////  將 "yyyy/mm/dd" 字串型態的兩個日期做比較
/////  輸入：[$date1, $date2] = [日期1, 日期二]
/////  輸出：[1,0,-1] = [前者大，兩者相等，後者大]
function Compare_Dates($date1, $date2)
{
  list($y1, $m1, $d1) = explode("/",$date1);
  list($y2, $m2, $d2) = explode("/",$date2);

  if( $y1 > $y2 ) {             return 1;
  }else if( $y1 < $y2 ){          return -1;
  }else{
    if( $m1 > $m2 ){            return 1;
    }else if( $m1 < $m2 ){        return -1;
    }else{
      if( $d1 > $d2 ){          return 1;
      }else if( $d1 < $d2){       return -1;
      }else{            return 0;  }
    }
  }
}

////////////////////////////////////////////////////////////////////////////////////////////////
/////  Apply_Form_Allowed
/////  目前時間是否可申請加簽/棄選單
/////  依照系統設定的加簽/棄選開始、截止日期，以及目前時間判斷
/////  傳回值：($allow, $msg) = (可否申請, 錯誤訊息) 
/////          其中 $allow 的值為 [0,1,-1] = [尚未開放, 開放中, 已截止]
/////  2011/07/29 Nidalap :D~
/////  2013/04/15 將原先的 Concent_Form_Allowed() 改為 Apply_Form_Allowed，可接受「加簽」、「棄選」兩種判斷。 Nidalap :D~
/////  2013/04/19 將原先 $allow 只有 0,1 改為 0,1,-1  Nidalap :D~
/////  2015/09/23 將此函式複製到課程地圖系統，作為申請客製化學程時間判斷用 by Nidalap :D~
function Apply_Form_Allowed($form_type)
{
  $start_hour	= 12;		///  開放日幾點開始才算開放
  $end_hour	= 17;		///  截止日幾點開始才算截止
  $allowed_forms	=	array("concent", "withdrawal");			///  目前只允許加簽與棄選單
  if( !in_array($form_type, $allowed_forms) )  die("內部錯誤：無此表單 $form_type！");
  
  list($now1, $now2, $now3) = gettime("");
  $ss = Get_System_State();

  ///  依據傳入參數判斷要抓取加簽還是棄選的開始/結束日期設定
  $start_date	= $ss[$form_type . "_form_start"];
  $end_date		= $ss[$form_type . "_form_end"];
//  echo "now = $now1, $now2, $now3<BR>\n";
//  echo "start = " . $start_date . "; end = " . $end_date . "<BR>\n";

  if( Compare_Dates($now3, $start_date) == -1 ) 
    return array(0,"加簽尚未開放");		///  現在 < 開放時間
  else if( Compare_Dates($now3, $start_date) == 0 ){
    list($date, $nowtime) = explode(" ", $now2);
    list($nowhour, $temp) = explode(":", $nowtime);
    if( $nowhour < $start_hour )
      return array(0,"加簽尚未開放"); 
    else
      return array(1,"");
  }else if( Compare_Dates($now3, $end_date) == -1 )
    return array(1,"");				///  開放時間 < 現在 < 關閉時間：  開放
  else if( Compare_Dates($now3, $end_date) == 1 )
    return array(-1,"加簽已截止");		///  關閉時間 < 現在：             已截止
  else{				///  現在 = 關閉日期：             判斷時間
    list($date, $nowtime) = explode(" ", $now2);
    list($nowhour, $temp) = explode(":", $nowtime);
    if( $nowhour < $end_hour )  
      return array(1,"");
    else
      return array(-1,"加簽已截止");
  }
}
////////////////////////////////////////////////////////////////////////////////////////////////
/////  顯示輸入資料錯誤的網頁錯誤訊息
/////  2009/10/09 Nidalap :D~
function Show_Input_Error_Message($error_array)
{
  global $BG_PIC, $EXPIRE_META_TAG;

  $msg =  "<HTML><HEAD>" . $EXPIRE_META_TAG . " <TITLE>輸入資料有誤</TITLE></HEAD>";
  $msg .= "<BODY background=" . $BG_PIC . ">";
  $msg .= "<Center><FONT color=RED>輸入資料有誤</FONT><hr>";
  $msg .= "<FONT size=-1>" . $error_array[0] . "<BR>請重新輸入!<p>";
  $msg .= "<A href=\"login.php\">重新登入</A>";
  
 // echo iconv("big5", "utf-8", $msg);
  echo $msg;
  
  exit(2);

}

  //////////////////////////////////////////////////////////////////////
  /////  Format_Time_String
  /////  將選課節次時間資料, 轉為單一可閱讀字串(ex: 一6三5,6)
  function Format_Time_String($rtime)
  {
    global $WEEKDAY;
    $time_string = "";
    $last_day = "";
    foreach($rtime as $ele ) {
      if( $ele{"week"} != $last_day ) {
        $time_string .= $WEEKDAY[$ele{"week"}];
      }else{
        $time_string .= ",";
      }
      $time_string .= $ele{"time"};
      $last_day = $ele{"week"};
    }
    return($time_string);
  }
  ///////////////////////////////////////////////////////////////////////
  /////  抄來的 getIP()
  /**
  * HTTP_X_FORWARDED_FOR只有使用Transparent Proxy(#1)時,裡面才會有東西
  * 否則裡面的資料是空的,使用Anonymous(#2),High Anonymity Proxy(#3)也是空的
  *
  * #1 透明代理伺服器,Transparent Proxy(Hinet的Proxy是Transparent Proxy)
  * #2 匿名代理伺服器,Anonymous Proxy
  * #3 高隱匿代理伺服器,High Anonymity Proxy
  */
  function getIP() {
	if(!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
		$route = $_SERVER['HTTP_X_FORWARDED_FOR'];
		$ip = split(',', $route);
	} else {
		$route = '';
	}
	$ip = (empty($route)) ? $_SERVER['REMOTE_ADDR'] : $ip[0];
	return $ip;
  }
  //////////////////////////////////////////////////////////////////////
  /////  檢核特殊字元, 在前面加上 back-slash, 以避免 SQL injection 攻擊
  /////  2006/11/23  抄自網路上找到的程式. Nidalap :D~ 
  /////  2011/05/30  新增 strip_tags 和 htmlspecialchars.   Nidalap :D~
  function quotes($content)
  {
    $advanced_mode = 1; 
    if (get_magic_quotes_gpc()) {               // 如果 magic_quotes_gpc=On
      // 系統會自動加 quote, 程式不做處理
    }else{                                      // 如果 magic_quotes_gpc=Off
      if (is_array($content)) {                 // 判斷$content是否陣列
        foreach ($content as $key=>$value) {
          if( $advanced_mode == 1 ) {
            $content[$key] = strip_tags(htmlspecialchars(addslashes($value)));
          }else{
            $content[$key] = addslashes($value);
          }
        }
      }else{                                    //如果$content不是陣列
        if( $advanced_mode == 1 ) {
          $content = strip_tags(htmlspecialchars(addslashes($content)));
        }else{
          $content = addslashes($content);
        }
      }
    }
    return $content;
  }
  /////////////////////////////////////////////////////////////////////////////////////
  /////  檢查特定資料是否合法，以補 quotes() 之不足。本身即包含 quotes()。
  /////  輸入：[要驗證的資料，它應該是哪種類型，檢查失敗時顯示的欄位名稱，額外參數1(依類型定義), 額外參數2(依類型定義)]
  /////  2016/01/12 從課程地圖的 main.php 中複製改來 by Nidalap :D~
  function Verify_Specific_Data($data, $type="text", $data_name=NULL, $param1=NULL, $param2=NULL)
  {
	global $SYS;
	$data = quotes($data);
	$pass = 0;

	switch( $type ) {
	  case "int":											///  一般數字：$param1 是長度(位數)，$param2 若為 1 則可允許負號
	    if( is_numeric($data) ) {
		  $data_len = strlen($data);
		  if( $param2 ) {
		    if( $data[0] == "-" ) {
			  $data_len = $data_len - 1;
			}else if( preg_match("/^\d$/", $data[0]) ) {
			  ///  do nothing
			}else{
			  $pass = 0;
			  break;
			}
		  }
		  if( $param1 ) {
			if( $data_len == $param1 )  $pass = 1;
		  }else{
		    $pass = 1;
		  }		  
		}
	    break;
	  case "year":											///  學年度
	    if( is_numeric($data) and ((strlen($data)==2) or (strlen($data)==3)) ) 	$pass = 1;
		break;
	  case "term":											///  學期
	  case "semester":
	    if( is_numeric($data) and ($data>=1) and ($data<=3) ) 	$pass = 1;
		break;
	  case "deptcd":										///  系所代碼
	  case "dept_id":
		if( strlen($data) == 4 )			$pass = 1;
		break;
	  case "college":										///  學院代碼。$param1 若為 1，代表允許 0 代表全校
	    if( ($data>=1) and ($data<=7) )     $pass = 1;
		if( ($param1==1) and ($data==0) )	$pass = 1;
	    break;
	  case "student_id":									///  學號
	  case "std_no":
	    if( strlen($data) == 9 ) {
		  if( preg_match("/^[45689]\n[8]$/", $data) )  $pass = 1;
		}
		break;
	  case "person_id":										///  身份證號(檢查正確後，順手將英文部分轉大寫)
	    if( strlen($data) == 10 ) {
		  if( preg_match("/^[0-9a-zA-Z]{10}$/", $data) )  {
			$pass = 1;
			$data = strtoupper($data);
		  }
		}
		break;
	  case "course_id":										///  科目代碼
	    if( strlen($data) == 7 ) {
		  if( preg_match("/^[1-9][0-9A]{6}$/", $data) )  $pass = 1;
		}
		break;
	  case "grp":											///  班別
	  case "group":	
	    if( strlen($data) == 2 ) {
	      if( preg_match("/^[0-5][0-9]{1}$/", $data) )	$pass = 1;
	    }
	    break;
	  case "cid_grp":
	    if( strlen($data) == 10 ) {							///  科目代碼 _ 班別
		  if( preg_match("/^[1-9][0-9A]{6}_[0-5][0-9]$/", $data) )  $pass = 1;
		}
	    break;
	  case "curattr":										///  學分歸屬
	    if( strlen($data) == 1 ) {
	      if( preg_match("/^[1-3]$/", $data) )			$pass = 1;
	    }
	    break;
	  case "date":											///  日期
	    if( preg_match("/[0-9\/]{8,10}/", $data) )		$pass = 1;
		break;
		
	  case "password":
	  default:												///  若無指定（一般文字），$param1 為最大 byte 數
		if( ($param1 == NULL) or (strlen($data) <= $param1) )	$pass = 1;
	}
    if( $pass == 0 ) {
	  //Error_Msg("lalala");
	  //Error_Msg("錯誤：欄位 " . $type . " 不可為 " .  $data);
	  Error_Msg("$data_name 欄位不可為： " .  $data);

	  echo  $SYS["HTML_META_TAG"];
//	  print_r($SYS);
	  echo "錯誤：欄位 $type 不可為 $data";
	  die();
	  //die("Error input: $data, $type, $param1");
	  //header("Location:index.php");
	}else{
	  return $data;
	}
  }
  

?>