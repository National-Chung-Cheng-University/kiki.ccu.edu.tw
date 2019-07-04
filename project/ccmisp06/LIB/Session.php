<?PHP

///////////////////////////////////////////////////////////////////////////////////////
/////  Session.php
/////  所有關於 Session 的函式, 都在這裡
///////////////////////////////////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////////////////////////////////
/////  Create_Session_ID
/////  以 [時間, 學號, 密碼] 加上 crypt 方式, 產生 session id
/////  2007 改寫 php 版本
/////  Nidalap :D~
function Create_Session_ID($id, $password)
{
  global $SESSION_PATH;
//  $session_file = $SESSION_PATH . $session_id;

  if( floor(phpversion()) >= 5 ) {             
    date_default_timezone_set("Asia/Taipei");  
  }
  $time = localtime();

  $hour         = $time[2];
  $min          = $time[1];

  if( $hour >12 ) {
    $hour2 = $hour - 12;
  }

  if( strlen($min) == 1 ) { $min = "0" . $min; };
  if( strlen($hour) == 1 ) { $hour = "0" . $hour; };
 

  $salt = "pa";
//  $session_id = $hour.$min
//                . $id
//                . $password;

  //  2008/02/20 加上三個 random 數字, 避免 collision
  $session_id = crypt($hour.$min, $salt)
                . crypt($id, $salt)
                . crypt($password, $salt)
                . rand(0,9)
                . rand(0,9)
                . rand(0,9)
                ;                                  

//  print("session id = $session_id<BR>\n");
  
  $pattern[0]	= '/\./';						// 尚無法轉換 '\'
  $pattern[1]	= '/\//';
  $pattern[2]	= '/\\\\/';						// 轉換 \\
  $placement	= 'A';
  $session_id = preg_replace($pattern, $placement, $session_id);	//  轉換為一個合法的 unix 檔名
  $session_id = preg_replace("/pa/", "", $session_id);
//  print("session id = $session_id<BR>\n");
  //  print_r($pattern);
  
  for($retry=0; $retry<=5; $retry++) {
    $session_file_to_be = $SESSION_PATH . $session_id;
    if( file_exists($session_file_to_be) ) {
//      echo("Collision happened! $session_id\n");
      $session_id .= rand(0,9);
    }
  }
  
  return($session_id);
}

///////////////////////////////////////////////////////////////////////////////////////  

///////////////////////////////////////////////////////////////////////////////////////  
/////  Write_Session
/////  寫入 session 資料檔
/////  2007/02 改寫 php 版本
/////  Nidalap :D~
function Write_Session($session_id, $id, $password, $add_course_count)
{
    global $SESSION_PATH;
    $session_file = $SESSION_PATH . $session_id;

    $id = $id . "\n";
    $password = $password . "\n";
    $ip = getenv('REMOTE_ADDR') . "\n";
    $login_time = time() . "\n";
    $add_course_count = $add_course_count . "\n";
    
//    echo("-> $session_file<BR>\n");
    $file_handle = fopen($session_file, "w");
    fputs($file_handle, $id);
    fputs($file_handle, $password);
    fputs($file_handle, $login_time);
    fputs($file_handle, $ip);
    fputs($file_handle, $add_course_count);
    
    fclose($file_handle);
    chmod($session_file, 0666);
}

///////////////////////////////////////////////////////////////////////////////////////  
/////  Read_Session
/////  讀取 session 資料檔
/////  2007/02 改寫 php 版本
/////  Nidalap :D~
/////  此版本部份流程與 perl 版本不同，請注意
function Read_Session($session_id)
{
  global $SESSION_PATH, $TIME_OUT_SECONDS;
  $session_file = $SESSION_PATH . $session_id;
  //  檢查 session id 合法性, 不得有特殊字元如 ~ ; \ . ` "
  $illegal_chars = array('~', ';', '\\\\', '\\.', '\\`', '"');
  foreach ($illegal_chars as $ch) {
    $ch = "/" . $ch . "/";
    if( preg_match($ch, $session_id) ) {
      Session_Illegal();
    }
  }
  $file_stat = stat($session_file);				// 讀取 session file 上次存取時間
  $mtime = $file_stat["mtime"];
  $now = time();
  $diff_time = $now - $mtime;
  if( $file_handle = fopen($session_file, "r") ) {
    list($session{'id'})                   = fscanf($file_handle, "%s\n");
    list($session{'password'})             = fscanf($file_handle, "%s\n");
    list($session{'login_time'})           = fscanf($file_handle, "%s\n");
    list($session{'ip'})                   = fscanf($file_handle, "%s\n");
    list($session{'add_course_count'})     = fscanf($file_handle, "%s\n");
    fclose($file_handle);
  }else{
    Session_Not_Found();					// 找不到 session file
  }
  if( $diff_time > $TIME_OUT_SECONDS ) {                        // Timeout 自動登出
//    fclose($file_handle);
    Destroy_Session($session_id, $session["id"]);
    Session_Not_Found();
  }
  return($session);
}

///////////////////////////////////////////////////////////////////////////////////////
/////  刪除 session 資料(登出)
/////  2007/02 改寫 php 版本
/////  Nidalap :D~
function Destroy_Session($session_id, $student_id) 
{
  global $SESSION_PATH;
  $session_file = $SESSION_PATH . $session_id;
  
  if( file_exists($session_file) )  {
    Student_Log("TimeOut", $student_id);
    if( unlink($session_file) ) {
      return(1);
    }else{
      return(0);
    }
  }else{
    return(-1);
  }  
}
///////////////////////////////////////////////////////////////////////////////////////
/////  更新 Session file 時間
function Renew_Session($session_id)
{
  global $SESSION_PATH;
  $session_file = $SESSION_PATH . $session_id;

//  echo "touch $session_file<BR>\n";

  touch($session_file);
}

///////////////////////////////////////////////////////////////////////////////////////
/////  Session_Not_Found
/////  找不到 session file, 顯示此 session 是無效的錯誤訊息.
/////  因為會有 crontab 定期清除, 這是使用者最容易見到的 time out message
/////  Updated: 
/////    2007/02/26 改寫 php 版本 Nidalap :D~
/////    2009/10/26 Session 過期(Time_Out)也會呼叫此函式  Nidalap :D~
function Session_Not_Found()
{
  global $GRAPH_URL, $SUB_SYSTEM_NAME, $IS_ENGLISH;
  
  if( $IS_ENGLISH ) {
    $txt = array("Re-login", "CCU Course Selection System", "CCU Course Selection System",
				 "Session timeout.", "You have been logged out!");
  }else{
    $txt = array("我要重新登入", "國立中正大學選課系統", 
	             "中正大學<FONT color=RED></FONT>" . $SUB_SYSTEM_NAME . "選課系統", 
				 "您本次的登入已經無效!", "可能是因為太久沒有動作, 系統已經幫您登出!");
  }
  
  $link = "<A href=\"index.php\" target=_top>" . $txt[0] . "</A>";

  echo '
    <html>
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>' . $txt[1] . '</title>
      </head>
      <body background="$GRAPH_URL/ccu-sbg.jpg">
        <center>
        <H1><FONT face="標楷體">' . $txt[2] . '
        <IMG src="$GRAPH_URL/mouse.gif">
        <BR><HR></H1>
           <font size=3 face="標楷體">
            ' . $txt[3] . '<BR>
            ' . $txt[4] . '<P>
            ' . $link . '
      </BODY>
    </HTML>
  ';
  exit();
}

///////////////////////////////////////////////////////////////////////////////////////////////
/////  Session_Illegal
/////  不合法的 session id
function Session_Illegal()
{
  global $GRAPH_URL, $SUB_SYSTEM_NAME;
  
  //  這裡最好還要加入 LOG

  echo ("
    <html>
      <head>
        <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">
        <title>國立中正大學選課系統</title>
      </head>
      <body background=\"$GRAPH_URL/ccu-sbg.jpg\">
        <center>
        <H1><FONT face=\"標楷體\">中正大學<FONT color=RED></FONT>$SUB_SYSTEM_NAME選課系統</FONT>
        <IMG src=\"$GRAPH_URL/mouse.gif\">
        <BR><HR></H1>
           <font size=3 face=\"標楷體\">
            您輸入的資料有嚴重錯誤(一般情況下, 應該不會出現),<P>
            <A href=\"mailto:nidalap\@ccu.edu.tw\">請洽程式設計者 校內分機 14203 李永祥</A>
      </BODY>
    </HTML>
  ");
  exit();
}

///////////////////////////////////////////////////////////////////////////////////////
/////  Read_Ban_Record()
/////  讀取停權名單, 看某學生是否在停權名單中
/////  傳回值若大於 0 則是停權中.
/////  Date: 2007/02/25 改寫 php 版本
function Read_Ban_Record($id)
{
  global $BAN_LIST_PATH, $BAN_COUNT_LIMIT, $BAN_DURATION;
  $res_time	= 0;
  $ban_count	= 0;

  $ban_file = $BAN_LIST_PATH . $id . ".ban";
  if( file_exists($ban_file) ) {
    $now = time();
    $fp = fopen($ban_file, "r");
    
    while( $line = fgets($fp) ) {
      $ban_count++;
      list($bantime1, $bantime, $id, $ip) = preg_split("/, /", $line);
    }
//    echo("{$bantime1}, $bantime, $id, $ip<BR>\n");
    $diff_time = $now - $bantime1;			// 現在和停權開始時間的差
    $res_time = $BAN_DURATION - $diff_time;		// 停權剩餘時間    
    if( $ban_count >= $BAN_COUNT_LIMIT ) {		// 若異長加選超過 $BAN_COUNT_LIMIT 次
      return($res_time);
    }else{
      return(0);					// 沒超過的話, 繼續觀察不停權
    }
  }else{
    return(0);						// 該學生沒有被停權過
  }
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////
/////  Show_Ban_Message()
/////  顯示停權訊息給學生看
/////  輸入值: [停權恢復尚需秒數]
/////  Date: 2005/04/29
function Show_Ban_Message($ban_res_time)
{
  $ban_res_time = round($ban_res_time / 60, 0);

  $message = "系統偵測到您異連續多次加選, 嚴重影響系統效能與其他同學權益, ";
  $message .= "<FONT color=RED>依據第81次教務會議決議, 停權八小時</FONT>.";
  $message .= "我們已經開始嚴密監控您的選課行為, 請自重!<P>";
  $message .= "<CENTER>您大約在 ";
  $message .= $ban_res_time;
  $message .= " 分鐘後才可以加退選.</CENTER><P>";
  $message .= "若系統誤判, 同學可在上班時間電洽教務處教學組, 或在任何時候 email: nidalap\@ccu.edu.tw";

  echo "
    <CENTER>
    <TABLE border=1 width=50%>
      <TR><TD bgcolor=YELLOW>
        $message
      </TD></TR>
    </TABLE>  
  ";
}


        




?>