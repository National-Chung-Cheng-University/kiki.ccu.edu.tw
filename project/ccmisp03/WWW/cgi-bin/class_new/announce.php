<?PHP 
  include "../library/Reference.php";
  include $LIBRARY_PATH . "Error_Message.php";
  include $LIBRARY_PATH . "Common_Utility.php";
  include $LIBRARY_PATH . "Session.php";
  include $LIBRARY_PATH . "Student.php";
  
//  $session_id = $_GET['session_id'];
//  $identified = 0;
//  if( $session_id != "" )  $identified = 1; 
//  if( $identified == 1 ) {
//    $session_data = Read_Session($session_id);
//    $id                 = $session_data{'id'};
//    $password           = $session_data{'password'};
//  }
  $announce_id = $_GET['announce_id'];

  $online_help_date = Show_Online_Help("DATETIME");

  if( $announce_id != "" )  {					//  看某個公告內容
    list($title, $announce_date, $sticky, $content) = Read_Announce_Content($announce_id);
//    $announce_date = substr($announce_id, 0, 8);
    $table = "
        <TR>
          <TH bgcolor=YELLOW width=80%>標題: $title</TH>
          <TH bgcolor=YELLOW>公告日期: $announce_date $online_help_date</TH>
        </TR>
        <TR><TD colspan=2>$content</TD></TR>
    ";    
  }else{							//  看全部公告 index
    $board = Read_Announce_Index();
    $table = "
        <TR>
          <TH bgcolor=YELLOW width=25%>公告日期 $online_help_date </TH>
          <TH bgcolor=YELLOW>標題</TH>
        </TR>
        <TR>
          <TD>
            $board
          </TD>
        </TR>
    ";
  }
  
  
?>

<HTML>
  <HEAD>
    <LINK rel="stylesheet" type="text/css" href="<?PHP echo $HOME_URL ?>font.css">
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
  </HEAD>
  <BODY background="<?PHP echo $BG_PIC ?>">
    <CENTER>
      <SPAN class="title1">系統公告</SPAN>
    </CENTER>    
    <table width="100%">
      <tr>
        <td height="1" colspan="2" background="<?PHP echo $GRAPH_URL ?>dash.jpg"></td>
      </TR>
    </TABLE>
    <P>
    <CENTER>
      <TABLE border=0 width="75%" class=font1>
	<?php echo $table ?>
      </TABLE>
    </CENTER>
  </BODY>
</HTML>
  