<HTML>
<?PHP
  include "../library/Reference.php";
  include $LIBRARY_PATH . "Error_Message.php";
  include $LIBRARY_PATH . "Session.php";

  $session_id = $_GET['session_id'];
  $success = Destroy_Session($session_id);
  
  $message = "您已經成功登出!";


?>

<HEAD>
  <TITLE>LOGOUT</TITLE>
  <meta http-equiv="refresh" content="1; URL=index.html">
  <meta http-equiv="Content-Type" content="text/html; charset=big5"> 
<BODY background=<?PHP echo $BG_PIC ?>>
  <!IMG src=<?PHP echo $TITLE_PIC ?>>
  <H1>
  <CENTER>
  <?PHP echo("$message<BR>\n");  ?>
  <A href="index.html" target=_top>重新登入</A>
  </FORM>
 </BODY>
</HTML>