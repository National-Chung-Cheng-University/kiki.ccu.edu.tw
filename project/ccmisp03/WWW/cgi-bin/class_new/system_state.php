
<?PHP
  include "../library/Reference.php";
  include $LIBRARY_PATH . "Error_Message.php";
  include $LIBRARY_PATH . "Common_Utility.php";

  $system_settings			= Get_System_State();
  list ($time_string, $time_string2)	= gettime("");
  
//  $system_settings{'sysstate'} = 2;
//  $system_settings{'limit_number_state'} = 0;
  
  $year_term = $YEAR . " �Ǧ~�ײ� " . $TERM . " �Ǵ�";
  
  if( $system_settings{'sysstate'} == 0 ) {
    $statestring = "�Ȥ��}��d��";
    $bgcolor	 = "RED";
  }else if( $system_settings{'sysstate'} == 1 ) {
    $statestring = "�ȨѬd��, ���}����";
    $bgcolor	 = "YELLOW";
  }else if( $system_settings{'sysstate'} == 2 ) { 
    $statestring = "�}���Ҥ�";
    $bgcolor	 = "lightGREEN";
  }
  
  if( $system_settings{'limit_number_state'} == 0 ) {
    $limit_state = "�t�μȤ�����, �N����z��";
    $limit_state_anchor = "LIMIT_STATE_0";
  }else{
    $limit_state = "���m��Ĺ, �B������";
    $limit_state_anchor = "LIMIT_STATE_1";
  }
  
//  $temp = $system_settings{'black_list'};
//  print("black_list = $temp\n");
?>
<HEAD>
  <meta http-equiv="Content-Type" content="text/html; charset=big5">
  <META http-equiv="refresh" content="<?PHP echo $REFRESH_TIME_SYSTEM_STATE ?>">
</HEAD>

  <TABLE border=1 width=100%>
    <TR>
      <TD>
            <TABLE border=0 width=100% align=CENTER cellpadding=0 cellspacing=0>
              <TR><TH bgcolor=<? echo $bgcolor ?>><FONT size=2>�ثe�t�Ϊ��A
                <A href="javascript:OnlineHelp('<? echo $limit_state_anchor ?>')">
                <FONT color=BLUE>[?]</FONT></A>
                </FONT></TH></TR>
              <TR><TD>
                <FONT size=2>
                <IMG src="<? echo $GRAPH_URL ?>green_ball.gif">
                <FONT color=GREEN>�t�ήɶ�: <? echo $time_string2 ?></FONT>
              </TD></TR>
              <TR><TD>
                <FONT size=2>
                <IMG src="<? echo $GRAPH_URL ?>green_ball.gif">
                <FONT color=GREEN><? echo $year_term ?></FONT>
              </TD></TR>
              <TR><TD>
                <FONT size=2>
                <IMG src="<? echo $GRAPH_URL ?>green_ball.gif">
                <FONT color=GREEN><? echo $statestring ?></FONT>
              </TD></TR>
              <? if( $system_settings{'sysstate'} == 2 ) {  ?>
                <TR><TD>
                  <FONT size=2>
                  <IMG src="<? echo $GRAPH_URL ?>green_ball.gif">
                  <FONT color=GREEN><? echo $limit_state ?></FONT>
                </TD></TR>
              <? } ?>
            </TABLE>
      </TD>
    </TR>
  </TABLE>