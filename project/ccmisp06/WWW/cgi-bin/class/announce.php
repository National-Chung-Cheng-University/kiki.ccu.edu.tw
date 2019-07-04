<?PHP 
  /////////////////////////////////////////////////////////////////////////////////
  /////  announce.php
  /////  顯示系統公告（在系統後台管理系統新增之）
  /////  Updates:
  /////    200?/??/?? Created by Nidalap :D~
  /////    2014/02/10 加入行動版相關判斷與畫面最佳化 by Nidalap :D~
  /////    2015/05/19 英文版相關修改 Nidalap :D~
  
  require_once "../library/Reference.php";
  require_once $LIBRARY_PATH . "Error_Message.php";
  require_once $LIBRARY_PATH . "Common_Utility.php";
  require_once $LIBRARY_PATH . "Session.php";
  require_once $LIBRARY_PATH . "Student.php";
  require_once $LIBRARY_PATH . "English.php";
  
  $session_id = isset($_GET['session_id']) ? $_GET['session_id'] : NULL;
  if( $session_id ) {
    $session_data = Read_Session($session_id);
    $id = $session_data{'id'};
  }
//  $identified = 0;
//  if( $session_id != "" )  $identified = 1; 
//  if( $identified == 1 ) {
//    $session_data = Read_Session($session_id);
//    $id                 = $session_data{'id'};
//    $password           = $session_data{'password'};
//  }
  $announce_id = isset($_GET['announce_id']) ? $_GET['announce_id'] : "";
  $online_help_date = Show_Online_Help("DATETIME");

  if( $IS_ENGLISH != 1 ) {
    $page_txt	= "系統公告";
    $title_txt	= "標題";
	$date_txt	= "公告日期";
  }else{
    $page_txt	= "System Announcement";
	$title_txt	= "Title";
	$date_txt	= "Date";
  }
  
  if( $announce_id != "" )  {					//  看某個公告內容
    list($title, $announce_date, $sticky, $content) = Read_Announce_Content($announce_id);
//    $announce_date = substr($announce_id, 0, 8);
	$table = "
        <TR>
          <TH bgcolor=YELLOW width=80%>$title_txt: $title</TH>
          <TH bgcolor=YELLOW>$date_txt: $announce_date $online_help_date</TH>
        </TR>
        <TR><TD colspan=2>$content</TD></TR>
    ";    
  }else{							//  看全部公告 index
    $board = Read_Announce_Index();
	
	$table = "";
/*	$table = "
	  <TR>
	    <TH colspan=2 bgcolor=YELLOW>
		  <FONT COLOR=RED><H1>學生證IC卡更新使用期限通告</H1></FONT>
		  <H3>
		  <P>
		  請同學務必於104/03/01之前至教學組、圖書館、電算中心、體育中心、大學部學生宿舍…等資訊站設置點，靠卡感應以延長有效期限至104/10/01。
		  <P>
		  <FONT color=RED>
		  如未延長學生證IC卡使用有效期者，自104/03/01起將無法出入校園大/側門、汽機車停車場、圖書館、自修室、體育中心、學生宿舍…等地點。
		  </FONT>
		  </H3>
		</TH>
	  </TR>
	  <TR><TH>&nbsp;</TH></TR>
	";
*/	
	
	
    $table .= "
        <TR>
          <TH bgcolor=YELLOW width=25%>$date_txt $online_help_date </TH>
          <TH bgcolor=YELLOW>$title_txt</TH>
        </TR>
        <TR>
          <TD>
            $board
          </TD>
        </TR>
    ";
  }

if( $IS_MOBILE >= 1 )	$width = "95%";
else					$width = "75%";
  
?>

<HTML>
  <HEAD>
    <LINK rel="stylesheet" type="text/css" href="<?PHP echo $HOME_URL ?>font.css">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<?PHP if( $IS_MOBILE >= 1 ) 	echo $MOBILE_META_TAG ?>
  </HEAD>
  <BODY background="<?PHP echo $BG_PIC ?>">
    <?PHP if( $IS_MOBILE >= 1 ) 	echo Create_jQuery_Mobile_Title_Tag();  ?>
    <CENTER>
      <SPAN class="title1"><?PHP echo $page_txt ?></SPAN>
    </CENTER>    
    <table width="100%">
      <tr>
        <td height="1" colspan="2" background="<?PHP echo $GRAPH_URL ?>dash.jpg"></td>
      </TR>
    </TABLE>
    <P>
    <CENTER>
      <TABLE border=0 width="<?PHP echo $width ?>" class=font1>
	<?php echo $table ?>
      </TABLE>
    </CENTER>
	
	<?PHP if( $IS_MOBILE >= 1 ) 	echo Create_jQuery_Mobile_Footer_Tag(); ?>
	
  </BODY>
</HTML>
  