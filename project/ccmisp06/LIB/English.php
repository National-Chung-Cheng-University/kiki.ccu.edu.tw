<?PHP
  //////////////////////////////////////////////////////////////////////////////
  /////  English.php
  /////  英文版、行動版選課系統相關函式
  /////  Updates:
  /////    2012/01/24 Created by Nidalap :D~
  /////    2013/10/01 加入行動版判斷相關程式碼 by Nidalap :D~

  require_once $LIBRARY_PATH . "Mobile-Detect/Mobile_Detect.php";  
  $MOBILE_ICON_WIDTH	= 60;				///  智慧型手機按鈕為這個大小的正方形(px)
  $PAD_ICON_WIDTH		= 120;				///  平板電腦的按鈕大小
  $MOBILE_META_TAG = "<meta name='viewport' content='width=device-width, initial-scale=1.0, " 
						. "user-scalable=yes, minimum-scale=1.0' />\n" . Create_jQuery_Mobile_Script();
  
  ///  偵測是否為行動裝置，設定變數 $DEVICE_TYPE
  $DEBUG_M = 0;
  $detect = new Mobile_Detect;
  $DEVICE_TYPE = ($detect->isMobile() ? ($detect->isTablet() ? 'tablet' : 'phone') : 'computer');
  
  
/*  echo "GET[m], POST[m] = " . $_GET["m"] . ", " . $_POST["m"] . "<BR>\n";
  if(isset($_GET['m']) and !$_GET['m']) {
	  echo "ccc";	  
  }
*/
  /////  判別是否行動版，設定變數 IS_MOBILE
  if( (isset($_GET['m']) and $_GET['m']) or (isset($_POST['m']) and $_POST['m']) ) {
    $IS_MOBILE		=	1;
  }else if( (isset($_GET['m']) and !$_GET['m']) or (isset($_POST['m']) and !$_POST['m']) ) {
    $IS_MOBILE		=	0;
  }else if( ($DEVICE_TYPE == 'tablet') or ($DEVICE_TYPE == 'phone') )  {
    $IS_MOBILE		=	1;

  }else{
    $IS_MOBILE		=	0;
  }
  
  if( $IS_MOBILE == 1) {
    if ($DEVICE_TYPE == 'tablet')  {
      $IS_MOBILE = 2;
	  $ICON_WIDTH = $PAD_ICON_WIDTH;
	}else{
      $IS_MOBILE = 1;
	  $ICON_WIDTH = $MOBILE_ICON_WIDTH;
	  $TITLE_PIC = $HOME_URL . "Graph/mobile/title310px.gif";
	}
  }
  if( $DEBUG_M == 1 ) {
	if( !preg_match("/index\.php$/", $_SERVER["PHP_SELF"]) )  {
	  //echo "self = " . $_SERVER["PHP_SELF"] . "<BR>\n";
	  echo "[DEVICE_TYPE, IS_MOBILE] = [$DEVICE_TYPE, $IS_MOBILE]<P>\n";	  
	  echo "GET[m], POST[m] = " . $_GET["m"] . ", " . $_POST["m"] . "<BR>\n";
	}
  }
  
  /////  判別是否英文版，設定變數 IS_ENGLISH
  if( (isset($_GET['e']) and $_GET['e']) or (isset($_POST['e']) and $_POST['e']) )
    $IS_ENGLISH		=	1;
  else
    $IS_ENGLISH		=	0;
	
  //echo "is english = $IS_ENGLISH<BR>\n";
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  /////  顯示學年學期文字資訊(英文版不使用學年，而是用西元年)
  function Year_Term_English()
  {
    global $YEAR, $TERM;
	
	if( 1 == $TERM ) {			///  上學期
	  $year = date("Y");
	  $term = "Fall";
	}else if( 2 == $TERM ) {	///  下學期
	  $year = date("Y");
	  $term = "Spring";
	}else{						///  暑修(3)
	  $year = date("Y");
	  $term = "Summer";			///  ???
	}
	return $term . " semester of " . $year;
  }
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  /////  顯示行動板需要的 jQuery Mobile 引用程式碼
  function Create_jQuery_Mobile_Script()
  {
/*      return '
        <link rel="stylesheet" href="http://code.jquery.com/mobile/1.0a1/jquery.mobile-1.0a1.min.css" />
        <script src="http://code.jquery.com/jquery-1.4.3.min.js"></script>
        <script src="http://code.jquery.com/mobile/1.0a1/jquery.mobile-1.0a1.min.js"></script>
	  ';
*/
    global $HOME_URL;
	return "
      <meta name='viewport' content='width=device-width, initial-scale=1.0, user-scalable=yes, minimum-scale=1.0' />
      <link rel='stylesheet' href='" . $HOME_URL . "javascript/jquery_mobile/jquery.mobile.css' />
	  <link rel='stylesheet' href='" . $HOME_URL . "javascript/jquery_mobile/kiki.css' />
	  <script src='" . $HOME_URL . "javascript/jquery.js' /></script>
	  <script src='" . $HOME_URL . "javascript/jquery_mobile/jquery.mobile.js' /></script>
    ";
  }
  ///////////////////////////////////////////////////////////////////////////////////////
  function Create_jQuery_Mobile_Title_Tag()
  {
    return "
	  <DIV data-role='page'>
	  <CENTER>
	  <DIV data-role='header' data-theme='a'>
	    <IMG src='../../Graph/mobile/title310px.gif'>
	  </DIV>
	  <DIV data-role='content'>
	"; 
  }	
  ////////////////////////////////////////////////////////////////////////////////////////
  function Create_jQuery_Mobile_Footer_Tag()
  {
    global $student, $id, $session_id;
	if( !isset($student) )  {
	  if( !isset($id) ) {
	    if( !isset($session_id) ) {
		  $session_id = isset($_POST['session_id']) ? $_POST['session_id'] : $_GET['session_id'];
		}
	    $session_data = Read_Session($session_id);
		$id	= $session_data{"id"};
	  }
	  $student = Read_Student($id);
	  
	}
	
	list($time_string, $time_string2) = gettime($session_data{'login_time'});	
	$welcome_msg  =  $student['name'] . "同學，歡迎！<BR>\n";
	$welcome_msg .= "您本次的登入時間是:[$time_string2]";
    $footer = 
	  "</DIV>
	     <DIV data-role='footer'  data-theme='a'>
	       $welcome_msg
	     </DIV>
	     </CENTER>
	   </DIV>  <!-- page -->
	  ";
	return $footer;
  }
?>