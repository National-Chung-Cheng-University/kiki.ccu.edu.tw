<HTML>
<!-- script type="text/javascript" src="acpwd.js"></script> -->
<SCRIPT type="text/javascript" src="../../javascript/jquery.js"></SCRIPT>
<script language="JavaScript">
  //  這一段是從學籍系統的登入網頁抄來的 Added 2005/09/13 Nidalap :D~
  function f_action(field) {
	popup_ask_passwd=window.open("http://miswww1.cc.ccu.edu.tw/academic/lost_passwd.htm", "遺失密碼", "width =600, height =600, scrollbars=yes");
	popup_ask_passwd.name = "lost_passwd";
	return true;
  }

  function f_action_gra(field) {
        popup_ask_passwd=window.open("http://miswww1.cc.ccu.edu.tw/academic/gra/lost_passwd.htm", "遺失密碼", "width =600, height =600, scrollbars=yes");
        popup_ask_passwd.name = "lost_passwd";
        return true;
  }
  
  /////  點選PC中文版、行動版、英文版以後，透過轉址呼叫自己產生不同畫面
  $(document).ready(function() {
    $('#chinese').click(function() {
	  window.top.location = "index.php?e=0&m=0";
	});
	$('#english').click(function() {
	  window.top.location = "index.php?e=1";
	});
	$('#mobile').click(function() {
	  window.top.location = "index.php?m=1";
	});
  })

</SCRIPT>

<?PHP
  require_once "../library/Reference.php";
  require_once $LIBRARY_PATH . "Error_Message.php";
  require_once $LIBRARY_PATH . "English.php";
//  require_once $LIBRARY_PATH . "Mobile-Detect/Mobile_Detect.php";

  $system_settings = Get_System_State();
  $txt = Init_Text_Values();
  //print_r($system_settings);
?>

 <HEAD>
   <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
   <?PHP
     if( $IS_MOBILE >= 1 ) 
	   echo "<meta name='viewport' content='width=device-width, initial-scale=1.0, user-scalable=no, minimum-scale=1.0, maximum-scale=1.0' />
	   <CENTER>
	   <IMG src='../../Graph/mobile/title310px.gif'>
	   <P>
	   ";
   ?>
   
   <TITLE>LOGIN</TITLE>
 </HEAD>
  <BODY background="<?PHP echo $BG_PIC ?>">

  <FONT size=2>
  <CENTER>
  
  <?PHP

    //echo "deviceType = $deviceType<BR>\n";

    if( $system_settings['redirect_to_query'] == 1 ) {   // 如果資料已經清掉
      echo("<CENTER>$YEAR 學年度第 $TERM 學期開課中, 欲查詢本學期選課資料, 請在登入後點選 <FONT color=RED>資料查詢 -> 上學期功課表</FONT></CENTER>");
    }
  ?>
  <FORM name="form1" action="bookmark.php" method=POST>
  <TABLE border=0 width=100%>
    <TR>
	  <TD colspan=2>
	    <?PHP
		  if( $IS_ENGLISH == 1 ) 									///  英文版
		    $checked = array("", "checked='yes'", "");
		  else if( $IS_MOBILE >= 1 )								///  行動版
			$checked = array("", "", "checked='yes'");
		  else														///  (PC)中文版
			$checked = array("checked='yes'", "", "");
		  echo "<INPUT type='radio' name='version' id='chinese' value=0 " . $checked[0] . ">PC中文版<BR>\n";
		  if( $system_settings['allow_mobile'] == 1 ) {
		    echo "<INPUT type='radio' name='version' id='mobile' value=1 " . $checked[2] . ">行動版(beta version)<BR>\n";
		  }
		  echo "<INPUT type='radio' name='version' id='english' value=1 " . $checked[1] . ">English version<BR>\n";
		?>
	  </TD>
	</TR>
	<TR>
      <TD><FONT size=2>
	    <?PHP 
		  echo $txt{"sid"} . ":";
		?>
	  </TD>
      <TD>
	    <!-- 
        <!input class="MyInput" onmouseover="this.className='MyInput2';" onmouseout="this.className='MyInput';"  type="text" name="temp_count" size="12" onkeyup="star();" onBlur="key_end();">
        <!input type="hidden" name="id">
		-->
        <INPUT name="id" size=12 maxlength=9>
      </TD>
    </TR>
    <TR>
      <TD><FONT size=2>
	    <?PHP
	      echo $txt{"password"} . ":";
		?>
	  </TD>
      <TD>
        <INPUT size=10 type=password name=password>
      </TD>
    </TR>
    <TR>
      <TD colspan=2>
        <FONT size=2>
        <INPUT type=RADIO name=term checked >
		  <?PHP 
		    if( $IS_ENGLISH != 1 )  {
		      echo $YEAR . " 學年度";
              if( $TERM == 3 ) {
                echo("暑修<BR>");
              }else{
                echo("第 $TERM 學期<BR>");
              }
			  
			}else{
			  echo Year_Term_English();
			  echo "<INPUT type='hidden' name='e' value='1'>";
			}
			if( $IS_MOBILE >= 1 ) {
			  echo "<INPUT type='hidden' name='m' value='1'>";
			}else{
			  echo "<INPUT type='hidden' name='m' value='0'>";
			}
          ?>
      </TD>
    </TR>
    <TR><TD colspan=2><HR></TD></TR>
    <TR>
      <TD colspan=2 ALIGN="center"><INPUT type=submit value="<?PHP echo $txt{"login"} ?>">&nbsp;&nbsp;&nbsp;
      <?PHP
	    echo "<input type='button' value='" . $txt{'lost_pass'} . "' name='bt_lost_passwd'";
        if( is_GRA() == 1 ) {
          echo "onClick='return f_action_gra(this)'></TD>";
        }else{
          echo "onClick='return f_action(this)'></TD>";
        }
		echo "</TD>";
      ?>
    </TR>
  </TABLE>
  </FORM>
 </BODY> 
</HTML>
<?PHP
  //////////////////////////////////////////////////////////////////////////////////////////////
  /////  因應英文版本，將所有要顯示的文字在此整理，依照 $IS_ENGLISH 自動判別  2013/07/10
  function Init_Text_Values()
  {
    global $IS_ENGLISH, $KIKI_URL, $HOME_URL, $CLASS_URL, $QUERY_URL;
	global $student, $ban_res_time, $password_last_time;
	global $system_settings, $year, $term;
		
	$sname = $IS_ENGLISH ? $student['ename'] : $student['name'];
	$last_term_get_str = '';
	if( $system_settings['redirect_to_query'] == 1 ) {
	  $last_term_get_str = '&year=' . $year . '&term=' . $term;
	}
	
	$txtall = array(
	  'login'		=> array('c'=>'登入系統', 'e'=>'Login'),
	  'lost_pass'	=> array('c'=>'遺失密碼', 'e'=>'Lost Password'),
	  'sid'			=> array('c'=>'學號', 'e'=>'Student ID'),
	  'password'	=> array('c'=>'密碼', 'e'=>'Password') 
	);

	foreach( $txtall as $k=>$v ) {
	  if( $IS_ENGLISH )	{
	    $txt[$k] = $v['e'];
		if( isset($v['url']) ) {
		  if( strstr($v['url'], "?") )
		    $txt[$k."_url"] = $v['url'] . "&e=1";
		  else
		    $txt[$k."_url"] = $v['url'] . "?e=1";
		}
	  }else{
	    $txt[$k] = $v['c'];
		if( isset($v['url']) )
		  $txt[$k."_url"] = $v['url'];
	  }
	}	
    return $txt;
  }

?>