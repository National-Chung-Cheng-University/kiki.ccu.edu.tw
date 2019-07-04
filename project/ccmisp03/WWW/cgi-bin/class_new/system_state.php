
<?PHP
  include "../library/Reference.php";
  include $LIBRARY_PATH . "Error_Message.php";
  include $LIBRARY_PATH . "Common_Utility.php";

  $system_settings			= Get_System_State();
  list ($time_string, $time_string2)	= gettime("");
  
//  $system_settings{'sysstate'} = 2;
//  $system_settings{'limit_number_state'} = 0;
  
  $year_term = $YEAR . " 學年度第 " . $TERM . " 學期";
  
  if( $system_settings{'sysstate'} == 0 ) {
    $statestring = "暫不開放查詢";
    $bgcolor	 = "RED";
  }else if( $system_settings{'sysstate'} == 1 ) {
    $statestring = "僅供查詢, 不開放選課";
    $bgcolor	 = "YELLOW";
  }else if( $system_settings{'sysstate'} == 2 ) { 
    $statestring = "開放選課中";
    $bgcolor	 = "lightGREEN";
  }
  
  if( $system_settings{'limit_number_state'} == 0 ) {
    $limit_state = "系統暫不限修, 將執行篩選";
    $limit_state_anchor = "LIMIT_STATE_0";
  }else{
    $limit_state = "先搶先贏, 額滿為止";
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
              <TR><TH bgcolor=<? echo $bgcolor ?>><FONT size=2>目前系統狀態
                <A href="javascript:OnlineHelp('<? echo $limit_state_anchor ?>')">
                <FONT color=BLUE>[?]</FONT></A>
                </FONT></TH></TR>
              <TR><TD>
                <FONT size=2>
                <IMG src="<? echo $GRAPH_URL ?>green_ball.gif">
                <FONT color=GREEN>系統時間: <? echo $time_string2 ?></FONT>
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