<?PHP
  /////////////////////////////////////////////////////////////////////////////////
  /////  system_state.php
  /////  顯示系統狀態（學年學期、開放與否等）
  /////  Updates:
  /////    200?/??/?? Created by Nidalap :D~
  /////    2014/02/10 加入行動版相關判斷與畫面最佳化 by Nidalap :D~
  
  require_once "../library/Reference.php";
  require_once $LIBRARY_PATH . "English.php";
  require_once $LIBRARY_PATH . "Error_Message.php";
  require_once $LIBRARY_PATH . "Common_Utility.php";
  require_once $LIBRARY_PATH . "Session.php";
  require_once $LIBRARY_PATH . "Student.php";

  $system_settings			= Get_System_State();
  list ($time_string, $time_string2)	= gettime("");
  
//  $system_settings{'sysstate'} = 2;
//  $system_settings{'limit_number_state'} = 0;
  

  if( !$IS_ENGLISH ) {
    $year_term = $YEAR . " 學年度";
    if( $TERM == 3 ) {
      $year_term .= "暑修";
    }else{
      $year_term .=  "第 " . $TERM . " 學期";
    }
  }else{
    $year_term = Year_Term_English();
  }
  
  if( !$IS_ENGLISH ) {
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
  }else{
    if( $system_settings{'sysstate'} == 0 ) {
      $statestring = "NOT available for course selection nor browsing.";
      $bgcolor	 = "RED";
    }else if( $system_settings{'sysstate'} == 1 ) {
      $statestring = "NOT available for course selection.";
      $bgcolor	 = "YELLOW";
    }else if( $system_settings{'sysstate'} == 2 ) { 
      $statestring = "Available for course selection";
      $bgcolor	 = "lightGREEN";
    }
  }
  
  if( !$IS_ENGLISH ) {
    if( $system_settings{'limit_number_state'} == 0 ) {
      $limit_state = "系統暫不限修, 將執行篩選";
      $limit_state_anchor = "LIMIT_STATE_0";
    }else{
      $limit_state = "先搶先贏, 額滿為止";
      $limit_state_anchor = "LIMIT_STATE_1";
    }
  }else{
    if( $system_settings{'limit_number_state'} == 0 ) {
      $limit_state = "Courses are subject to screening.";
      $limit_state_anchor = "LIMIT_STATE_0";
    }else{
      $limit_state = "First-come first-served period for course selection.";
      $limit_state_anchor = "LIMIT_STATE_1";
    }
  }

  $online_help = Show_Online_Help($limit_state_anchor);
//  $temp = $system_settings{'black_list'};
//  print("black_list = $temp\n");
?>
<HEAD>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <META http-equiv="refresh" content="<?PHP echo $REFRESH_TIME_SYSTEM_STATE ?>">
  <?PHP if( $IS_MOBILE >= 1 ) 	echo $MOBILE_META_TAG; ?>
</HEAD>

<?PHP if( $IS_MOBILE >= 1 ) 	echo Create_jQuery_Mobile_Title_Tag();  ?>

  <TABLE border=1 width=100%>
    <TR>
      <TD>
            <TABLE border=0 width=100% align=CENTER cellpadding=0 cellspacing=0>
              <TR><TH bgcolor=<?PHP echo $bgcolor ?>><FONT size=2>
			    <?PHP 
			      if( !$IS_ENGLISH )	echo "目前系統狀態";
				  else					echo "System Status";
                  echo $online_help;
				?>
                </TH></TR>
              <TR><TD>
                <FONT size=2>
                <IMG src="<?PHP echo $GRAPH_URL ?>green_ball.gif">
                <FONT color=GREEN>
				  <?PHP 
				    if( !$IS_ENGLISH )	echo "系統時間:";
					else				echo "System time:";
					echo $time_string2 
				  ?>
				</FONT>
              </TD></TR>
              <TR><TD>
                <FONT size=2>
                <IMG src="<?PHP echo $GRAPH_URL ?>green_ball.gif">
                <FONT color=GREEN><?PHP echo $year_term ?></FONT>
              </TD></TR>
              <TR><TD>
                <FONT size=2>
                <IMG src="<?PHP echo $GRAPH_URL ?>green_ball.gif">
                <FONT color=GREEN><?PHP echo $statestring ?></FONT>
              </TD></TR>
              <?PHP if( $system_settings{'sysstate'} == 2 ) {  ?>
                <TR><TD>
                  <FONT size=2>
                  <IMG src="<?PHP echo $GRAPH_URL ?>green_ball.gif">
                  <FONT color=GREEN><?PHP echo $limit_state ?></FONT>
                </TD></TR>
              <?PHP } ?>
            </TABLE>
      </TD>
    </TR>
  </TABLE>
  <P>
  
  <?PHP if( $IS_MOBILE >= 1 ) 	echo Create_jQuery_Mobile_Footer_Tag(); ?>
  