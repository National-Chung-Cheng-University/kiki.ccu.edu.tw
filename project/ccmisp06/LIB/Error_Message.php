<?PHP
  /////////////////////////////////////////////////////////////////////////////////
  /////  Error_Message.php
  /////  放一些錯誤訊息, 以及寫入 log 的函式.
  /////  Nidalap :D~

//////////////////////////////////////////////////////////////////////////////////
/////  Update_Log
/////  從資料庫更新資料上來的 log.
/////  包括 deduct(成績抵免)
/////  Nidalap :D~
/////  2006/09/20  
function Update_Log($file, $rowcount, $time)
{
  global $LOG_PATH, $LIBRARY_PATH;
  
  include $LIBRARY_PATH . "Common_Utility.php";
    
  $LOG_FILE = $LOG_PATH . "Update.log";
  $file_handle = fopen($LOG_FILE, "a");
  
  list($ts1, $ts2) = gettime("");
  $log = $ts2 . "\t" . $file . "\t" . $rowcount . "\t" . $time . "\n";
  fputs($file_handle, $log);
  fclose($file_handle);
}
//////////////////////////////////////////////////////////////////////////////////
function Error_Msg($msg)
{
  global $EXPIRE_META_TAG, $GRAPH_URL;
  
  echo "
    <html>
      <head>
        $EXPIRE_META_TAG
        <title>資料輸入錯誤</title>
      </head>
      <body background=$GRAPH_URL/ccu-sbg.jpg>
        <center>
         <img src=$GRAPH_URL/open.jpg><P>
		 <H1>資料輸入錯誤</H1>
		 <HR>
		 $msg
		 <P>
		 <button onclick='javascript:history.back()'>回上頁</button>
	  </BODY>
	</HTML>
  ";

//  echo $msg;
  die();
}
//////////////////////////////////////////////////////////////////////////////////
function Fatal_Error($prog, $error_message)
{
  global $SYSADM_EMAIL;
  list($ts1, $ts2) = gettime("");
  $to      = $SYSADM_EMAIL;
  $subject = "選課系統嚴重錯誤訊息!";
  $message = "時間:" . $ts1 . "\n" . $prog . " - " . $error_message;
  $headers = 
     "Content-type: text/html; charset=big-5\r\n" .
     "To: " . $to . "\r\n" . 
     "From: " . $to . "\r\n" .
     "Reply-To: " . $to . "\r\n" .
     "X-Mailer: PHP/" . phpversion();
//  print_r($headers);
  mail($to, $subject, $message, $headers);
  die($message);
}

?>