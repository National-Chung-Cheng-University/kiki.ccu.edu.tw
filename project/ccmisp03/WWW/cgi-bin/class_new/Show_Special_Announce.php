<?PHP 
  include "../library/Reference.php";
  include $LIBRARY_PATH . "Error_Message.php";
  include $LIBRARY_PATH . "Common_Utility.php";
  include $LIBRARY_PATH . "Session.php";
  include $LIBRARY_PATH . "Student.php";
  
  $type = $_GET['type'];
  list($title, $announce) = Read_Special_Announce($type);
    $table = "
        <TR><TH bgcolor=YELLOW width=25%>$title</TH>
        <TR>
          <TD>
            $announce
          </TD>
        </TR>
    ";
  
  
?>

<HTML>
  <HEAD>
  
  </HEAD>
  <BODY background=<?PHP echo $BG_PIC ?>>
    <CENTER>
      <H2>系統公告</H2>
    </CENTER>
    <table width=100%>
      <tr>
        <td height="1" colspan="2" background="<?PHP echo $GRAPH_URL ?>dash.jpg"></td>
      </TR>
    </TABLE>
    <P>
    <CENTER>
      <TABLE border=0 width=85%>
	<?php echo $table ?>
      </TABLE>
    </CENTER>
  </BODY>
</HTML>
  