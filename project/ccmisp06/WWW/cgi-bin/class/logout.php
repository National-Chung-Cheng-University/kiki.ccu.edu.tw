<?PHP

  /////  2013/07/25 英文版相關增修：將顯示文字拉到 Init_Text_Values() 中設定。 Nidalap :D~
  require_once "../library/Reference.php";
  require_once $LIBRARY_PATH . "Error_Message.php";
  require_once $LIBRARY_PATH . "English.php";
  require_once $LIBRARY_PATH . "Session.php";
  require_once $LIBRARY_PATH . "Student.php";
  require_once $LIBRARY_PATH . "Common_Utility.php";

//session_save_path("/NFS/session");
  session_start();
 
  $session_id	= $_GET["session_id"] ? $_GET["session_id"] : $_POST["session_id"];
  $session_data	= Read_Session($session_id);
  $id		= $session_data["id"];
    
//  echo "session = ";
//  print_r($_SESSION);
//  echo "<P>my session($session_id) = ";
//  print_r($session_data);

  if( isset($_SESSION['verifySso']) and $_SESSION['verifySso']=='Y' ) {
    echo "<SCRIPT type='text/JavaScript'>window.close()</SCRIPT>";
    $_SESSION = array();
    die();
  }
  
//  print_r($_SESSION);

  $txt = Init_Text_Values();								///  初始化顯示文字（中文或英文）
  $success = Destroy_Session($session_id, $id);
  Student_Log("Logout ", $id, "");
  $message = $txt['logout_success'];
  
//  echo "<P>my session($session_id) = ";
//  print_r($session_data);
  
  $_SESSION = array();
?>

<HTML>
<HEAD>
  <?PHP if( $IS_MOBILE >= 1 )  echo $MOBILE_META_TAG; ?>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"> 
  <TITLE>LOGOUT</TITLE>
<BODY background=<?PHP echo $BG_PIC ?>>
  <CENTER>
  <IMG src=<?PHP echo $TITLE_PIC ?>>
  <HR>&nbsp;</P>
  <H1>  
  <?PHP 
    //echo "IS MOBILE = $IS_MOBILE<BR>\n";
	echo("$message<BR>\n");  
  ?>
  <A href="index.php" target=_top><?PHP echo $txt['re_login']; ?></A>
  </FORM>
 </BODY>
</HTML>



<?PHP
  //////////////////////////////////////////////////////////////////////////////////////////////
  /////  因應英文版本，將所有要顯示的文字在此整理，依照 $IS_ENGLISH 自動判別  2013/07/10
  function Init_Text_Values()
  {
    global $IS_ENGLISH, $KIKI_URL, $HOME_URL, $CLASS_URL, $QUERY_URL;
	global $session_id, $student, $ban_res_time, $password_last_time;
	global $year, $term;
	
	$sname = $student['name'];
	
	$txtall = array(
	  'logout_success'	=> array('c'=>'您已經成功登出!', 
								 'e'=>'Logout successful!'), 
	  're_login'		=> array('c'=>'點此重新登入', 'e'=>'Click to re-login')
	);

	foreach( $txtall as $k=>$v ) {
	  if( $IS_ENGLISH )	{
	    $txt[$k] = $v['e'];
	  }else{
	    $txt[$k] = $v['c'];
	  }
	}	
    return $txt;
  }

?>