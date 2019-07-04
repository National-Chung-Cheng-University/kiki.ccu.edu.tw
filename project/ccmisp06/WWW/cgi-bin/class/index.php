<?PHP
  ///////////////////////////////////////////////////////////////////////////
  /////  index.php
  /////  系統登入/內部主畫面
  /////  Updates: 
  /////    200?/??/?? Created by Nidalap :D~
  /////    2013/06/?? 英文版相關增修 by Nidalap :D~
  /////    2013/10/01 行動版相關增修 by Nidalap :D~
  /////    2014/12/04 強迫使用 SSL 版本 by Nidalap :D~
  /////    2015/08/17 修正行動裝置即使選擇電腦版也只能看行動版的 BUG。  Nidalap :D~
  
  require_once "../library/Reference.php";
  require_once $LIBRARY_PATH . "English.php";  
  
  /////  若使用者不是透過 SSL(https) 連進來，則轉址到 https 版本
  //if( NULL ==  $_SERVER["HTTPS"] ) {
  if( $_SERVER["SERVER_NAME"] == "kiki.ccu.edu.tw" ) {
    header("Location: " . $CLASS_URL);
  }
  
  if( isset($_POST["session_id"] ) )	$session_id = $_POST["session_id"];
  else if( isset($_GET["session_id"]) )	$session_id = $_GET["session_id"];
  
//  if( isset($_POST["phpsessid"] ) )	$session_id = $_POST["phpsessid"];
//  else if( isset($_GET["phpsessid"]) )	$session_id = $_GET["phpsessid"];
    

  $login_php_url = "login.php";		/// 如果是直接連線，登入分頁先到 login.php 要求帳密
  $login_php_has_input = 0;
  if( $session_id ) {			/// 如果是從 SSO 進來，登入分頁直接連到 bookmark.php
    $login_php_url = "bookmark.php?session_id=" . $session_id; // . "&phpsessid=" . $phpsessid;
	$login_php_has_input = 1;
    if( $IS_ENGLISH == 1 ) 
	  $login_php_url .= "&e=1";
  }else{
    if( $IS_ENGLISH == 1 ) {
	  $login_php_url .= "?e=1";
	  $login_php_has_input = 1;
	}
  }
  $system_state_url	= "system_state.php";
  $header_url		= "header.php";
  $announce_url		= "announce.php";
  if( $IS_ENGLISH == 1 ) {				///  英文版：設定所有 URL 加上 "e=1" 參數
    $system_state_url	.= "?e=1";
	$header_url			.= "?e=1";
	$announce_url		.= "?e=1";
  }
  
  if( $IS_MOBILE == 0 ) {				///  強制電腦版：設定所有 URL 加上 "m=0" 參數
    $system_state_url	.= "?m=0";
	$header_url			.= "?m=0";
	$announce_url		.= "?m=0";
	if( $login_php_has_input == 0) {
	  $login_php_url		.= "?m=0";
	}else{
	  $login_php_url		.= "&m=0";
	}
  }
  
//  if( ($DEVICE_TYPE == 'tablet') or ($DEVICE_TYPE == 'phone') ) {
//	header("Location: " . $login_php_url . "?m=1");	///  使用行動裝置：比照行動版執行
//  }
  if( $IS_MOBILE >= 1 ) {							///  行動版：不使用 frame，直接轉址到登入畫面
	if( $login_php_has_input == 0) {
	  $login_php_url		.= "?m=1";
	}else{
	  $login_php_url		.= "&m=1";
	}	
	header("Location: " . $login_php_url);
  }
?>
 
<HTML>
  <META http-equiv="" content="">
  <META name="DESCRIPTION" content="">
  <META name="KEYWORDS" content="">
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  
  <HEAD><TITLE>
    <?PHP 
	  if( $IS_ENGLISH )
	    echo "CCU Course Selection System";
	  else
	    echo "國立中正大學  選課系統";
	?>
  </TITLE></HEAD>
  <FRAMESET cols="220,80%" border=0>
    <FRAMESET rows="130,80%" border=0>
      <FRAME src="<?PHP echo $system_state_url ?>" NAME="system_state">
      <FRAME src="<?PHP echo $login_php_url; ?>" NAME="bookmark">
    </FRAMESET>
    <FRAMESET rows="120,80%" border=0>
      <FRAME src="<?PHP echo $header_url; ?>" NAME="header">
      <FRAME src="<?PHP echo $announce_url; ?>" NAME="basefrm">
    </FRAMESET>
  </FRAMESET>
</HTML>