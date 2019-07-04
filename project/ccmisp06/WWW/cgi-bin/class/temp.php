<?PHP
  //////////////////////////////////////////////////////////////////////////////////////////////////////////
  /////  bookmark.php
  /////  選課主選單（左側）
  /////  此網頁有可能是從 login.php 使用 POST 連過來，或是在 $REFRESH_TIME_BOOKMARK 秒後自行 reload
  /////  Updates:
  /////    200?/??/?? 偷用某個 tree 的 javascript 建構而成  Nidalap :D~
  /////    2010/04/21 若密碼太太久沒更新，強迫更新之。 若 email 為空，亦強迫更新之。 Nidalap :D~
  /////    2011/07/29 僅供查詢期間可點「加簽」網頁，實際連至加選第一頁選擇系所年級。  Nidalap :D~
  /////    2012/02/15 不開放查詢期間可點選「加簽」、「我的加簽單」等網頁。  Nidalap :D~
  /////    2012/11/05 改採 PDO 連線資料庫。  Nidalap :D~
  /////    2013/04/15 開放時間可點選「棄選」選項。 Nidalap :D~
  /////    2013/07/11 英文版相關增修：將顯示文字拉到 Init_Text_Values() 中設定。 Nidalap :D~
  /////    2013/08/28 加入2013選課改制意見調查表，舊生可以填，或是必須要填過才會顯示其他功能。 Nidalap :D~
  /////    2013/10/01 加入行動版相關判斷與畫面 by Nidalap :D~
  
  require_once "../library/Reference.php";
  require_once $LIBRARY_PATH . "Error_Message.php";
  require_once $LIBRARY_PATH . "Common_Utility.php";
  require_once $LIBRARY_PATH . "Password.php";
  require_once $LIBRARY_PATH . "Session.php";
  require_once $LIBRARY_PATH . "Student.php";
  require_once $LIBRARY_PATH . "Database.php";
  require_once $LIBRARY_PATH . "Select_Course.php";
  require_once $LIBRARY_PATH . "System_Settings.php";
  require_once $LIBRARY_PATH . "English.php";
  
  session_start();
  
  $system_settings = Get_System_State();
  
  list($year, $term) = Last_Semester(1);  

  if( isset($_POST["session_id"])  ) {						//  如果是自己 reload
    $session_data	= Read_Session( $_POST["session_id"]);
    $id			= $session_data{"id"};
    $password		= $session_data{"password"};
    $session_id		= $_POST["session_id"];
    $temp = "POST";
    $student = Read_Student($id);
  }else if( isset($_GET["session_id"])  ) {					//  用 GET reload
    $session_data	= Read_Session( $_GET["session_id"]);

//    echo "session_data = ";
//    print_r($session_data);
    
    $id			= $session_data{"id"};
    $password		= $session_data{"password"};
    $session_id		= $_GET["session_id"];
    $temp = "GET";
    $student = Read_Student($id);
    //$salt = Read_Crypt_Salt($_POST['id']);
    //$password = my_Crypt($_POST['password'], $salt);
    $password_validation = Check_Password($id, $password, "new");    
  }else{									//  如果剛登入
    $id			= $_POST{"id"};
    $password		= $_POST{"password"};
    Validate_Input($id, "id");
    Validate_Input($password, "password");
    $session_id = Create_Session_ID($id, $password);
    
    $password_original = $password;
    if( $USE_MD5_PASSWORD == 1 ) {
      $password = MD5($password);
    }else{
      $salt = Read_Crypt_Salt($id);           
      $password = my_Crypt($password, $salt);  
    }

    Write_Session($session_id, $id, $password, 0);
    $session_data       = Read_Session($session_id);
    $student = Read_Student($id);

    $password_validation = Check_Password($id, $password, "new", $password_original);
  }
  
  if( isset($_GET["session_id"]) ) {
    Student_Log("Online ", $id);	///  若是本頁自己 reload -> 紀錄 Online
  }else{
    Student_Log("Login  ", $id);	///  若是由密碼輸入頁面連結過來 -> 紀錄 Login
  }

  if( $USE_MD5_PASSWORD == 1 ) {
    $default_password = MD5($student{"personal_id"});
  }else{
    if( !isset($salt) )  $salt = "";
    $default_password = my_Crypt($student{"personal_id"}, $salt);
  }
//  echo "personal_id = ", $student{'personal_id'}, "<BR>\n";
  
  if( $password == $default_password  ) {                                    //  如果使用預設密碼
    $use_default_password = 1;
    //echo "salt = ", $salt, "<BR>\n";
    //echo("$password <-> $default_password <BR>\n");
  }   
  
  $ban_res_time = Read_Ban_Record($id);							// 讀取停權剩餘時間
//  $ban_res_time = 1223;
  $ban_flag = 0;
  if( ( $system_settings{"black_list"} == 1) and ( $ban_res_time > 0 ) )  $ban_flag = 1;	// 停權與否
  list($concent_form_allowed, $cf_msg)	= Apply_Form_Allowed("concent");		### 目前是否允許申請加簽
  list($withdrawal_form_allowed, $wf_msg)	= Apply_Form_Allowed("withdrawal");	### 目前是否允許申請棄選
  
  $txt = Init_Text_Values();								///  初始化顯示文字（中文或英文）
?>

<HTML>
  <HEAD>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE">
  <?PHP 
    if( $IS_MOBILE ) 
	   echo "<meta name='viewport' content='width=device-width, initial-scale=1.0, user-scalable=no, minimum-scale=1.0, maximum-scale=1.0' />\n";
	   
  ?>
  <meta http-equiv="refresh" content="<?PHP echo $REFRESH_TIME_BOOKMARK ?>; 
        URL=bookmark.php?session_id=<?PHP echo $session_id; if($IS_ENGLISH) echo "&e=1"; if($IS_MOBILE) echo "&m=1";?> ">
  <TITLE><?PHP echo $txt['menu']  ?></TITLE>
  <STYLE>
   SPAN.TreeviewSpanArea A {
     font-size: 10pt; 
     font-family: verdana,helvetica; 
     text-decoration: none;
     color: BLACK
   SPAN.TreeviewSpanArea A:hover {
     color: '#820082';}
   BODY {
     background-color: white;}
   TD {
     font-size: 10pt; 
     font-family: verdana,helvetica;}
  </STYLE>
  <SCRIPT>
  function getQueryString(index) {
    var paramExpressions;
    var param
    var val
    paramExpressions = window.location.search.substr(1).split("&");
    if (index < paramExpressions.length) {
      param = paramExpressions[index]; 
      if (param.length > 0) {
        return eval(unescape(param));
      }
    }
    return ""
  }

  </SCRIPT>

 </HEAD>

 <BODY leftmargin="0" topmargin="0" marginheight="0" marginwidth="0"  onResize="if (navigator.family == 'nn4') window.location.reload()"
   background=<?PHP echo $BG_PIC ?>>
  <SCRIPT src="../../javascript/ua.js"></SCRIPT>
  <SCRIPT src="../../javascript/ftiens4.js"></SCRIPT>

  <SCRIPT>
USETEXTLINKS = 1
STARTALLOPEN = 1
USEFRAMES = 0
USEICONS = 0
WRAPTEXT = 1
PRESERVESTATE = 1
HIGHLIGHT = 1

//
// The following code constructs the tree.
//
  foldersTree = gFld("<b><?PHP echo $txt['menu'] ?></b>", "")
  aux2 = insFld(foldersTree, gFld("<?PHP echo $txt['announce']; ?>", ""))
    <?PHP
	  echo InsDoc('R', 'announce');		///  系統公告
    ?>
  aux2 = insFld(foldersTree, gFld("<?PHP echo $txt['about']; ?>", ""))
    <?PHP 
      $add_word = $txt['add'];
      $add_flag = 0;					// 用來判斷是否可點選加退選
      if( ($system_settings{"sysstate"} == 2) and Check_Time_Map($student)  ) {
        $add_flag = 1;
        if( $concent_form_allowed == 1 )	if(!$IS_ENGLISH)  $add_word .= "及加簽";
      }
      if( $concent_form_allowed == 1 ) {
        if( $system_settings{"sysstate"} <= 1 )  {	// 若系統設定為「僅供查詢(1)」或「不可查詢(0)」
          $add_flag = 2;				  // 如果可以加簽，則顯示加簽選項
          if(!$IS_ENGLISH)  $add_word = "加簽";
        }
      }

      $css = Find_Change_School_Student("");
      if( $system_settings{"restrict_stdno"} ) {	//  如果有開啟「限制可選課學號」
        $temp = $system_settings{"restrict_stdno"};
        //if( !preg_match("/^.$temp.+/", $student{"id"}) and !($css{$student{"id"}} == 1) ) {
		//if( !preg_match("/^.$temp.+/", $student{"id"}) and !(array_key_exists($student{"id"}, $css) ) ) {
		if( ( $temp != substr($student{"id"},1,2) ) and !(array_key_exists($student{"id"}, $css) ) ) {
          $add_flag = 0;			 	  //  只有限制可選課學號者，或轉學生可選課
        }
      }
	  //if( $student{'enrollnum'} == 0 )    $add_flag = 0;			///  違章建築，限制註冊次數0次的不可選課 2013/06/20 Nidalap :D~
	  
      if( $SUPERUSER == 1 )		$add_flag = 1;	//  管理者登入一律視為可加選
      
//      echo "add_flag = $add_flag!\n";
      
      if ( $add_flag ) {
        if( $ban_flag and !($SUPERUSER) ) {							//  被停權
          //echo "insDoc(aux2, gLnk('R', '" . $txt['ban_msg'] . "', 'Show_Ban_Message.php?ban_res_time=" . $ban_res_time . "'))\n";
	      if( !$IS_MOBILE ) {
		    echo InsDoc('R', 'ban_msg');					///  停權公告
		  }else{
		    $m_txt['ban'] = "<A href='Show_Ban_Message.php?ban_res_time=$ban_res_time&m=1'>停權公告</A>";
		  }
        }else{											//  沒有被停權
          if( !$IS_MOBILE ) {
		    echo "insDoc(aux2, gLnk('R', '$add_word', '" . $txt['add_url'] . "'))\n";
		    if( $add_flag == 1 )
			  echo InsDoc('R', 'del'); 					///  退選
		  }else{
		    $m_txt['add'] = "<A href='Add_Course00.cgi?session_id=$session_id&m=1'>" . $add_word . "</A>";
			if( $add_flag == 1 )
			  $m_txt['del'] = "<A href='Del_Course00.cgi?session_id=$session_id&m=1'>退選</A>";
		  }
        }
      }
	  if( $withdrawal_form_allowed == 1 ) {
		if( !$IS_MOBILE ) {
		  echo InsDoc('R', 'withdrawal');					///  申請棄選
		  echo InsDoc('R', 'my_withdrawal');				///  我的棄選單
		}else{
		  ///  行動版目前不開放此功能
		}
      }
      if( ($system_settings{'sysstate'} >= 1 ) or ($SUPERUSER == 1)) {
		if( !$IS_MOBILE ) {
		  echo InsDoc('R', 'view');						///  檢視已選修科目
		  if( !$IS_GRA ) {
		    echo InsDoc('R', 'my_plan');					///  我的選課計畫
		  }
		}else{
		  $m_txt['view'] = "<A href='Selected_View00.cgi?session_id=$session_id&m=1'>檢視已選修科目</A>";
		}
      }
	  
      if( !$IS_MOBILE ) {
	    echo InsDoc('R', 'view_warning');					///  檢視篩選公告
	  }else{
	    $m_txt['view_warning'] = "<A href='View_Warning.cgi?session_id=$session_id&m=1'>檢視篩選公告</A>";
	  }
	  
      if ( ( ($system_settings{'allow_print_graduate_pdf'} == 1) or ($SUPERUSER == 1))  
           and ($student{'grade'} >=3) and ( preg_match("/^[49]/", $student{'id'}) ) ) {  
        if( !$IS_MOBILE ) {
		  echo InsDoc('R', 'graduate');					///  檢視畢業資格審查表
		}else{
		  ///  行動版目前不開放此功能
		}
      }
      if ( ($system_settings{'allow_print_pdf'} == 1) or ($SUPERUSER == 1) ) {
        if( !$IS_MOBILE ) {
		  echo InsDoc('R', 'view_pdf');					///  檢視選課結果單PDF
		}else{
		  ///  行動版目前不開放此功能
		}
	  }
      if( ($concent_form_allowed == 1)or($system_settings{"current_system_timeline"}>=5) ) {
        if( !$IS_MOBILE ) {
		  echo InsDoc('R', 'my_concent');					///  我的加簽單
		}else{
		  $m_txt['view_warning'] = "<A href='My_Concent_Forms.php?session_id=$session_id&m=1'>我的加簽單</A>";
		}
      }
	  
	  if( !$IS_MOBILE ) {
		echo InsDoc('R', 'print');						///  列印選課單
	    echo InsDoc('R', 'change_pwd');					///  更改密碼
	  }else{
		$m_txt['change_pwd'] = "<A href='Change_Password00.php?session_id=$session_id&m=1'>更改密碼</A>";
	  }
	  
    ?>

    aux2 = insFld(foldersTree, gFld("<?PHP echo $txt['query']; ?>", ""))
    <?PHP
	  if( !$IS_MOBILE ) {
	    echo InsDoc('R', 'query_course');				///  查詢開課資料
	    echo InsDoc('R', 'query_adv');					///  進階開課資料查詢
        echo InsDoc('R', 'support');					///  支援本班課程
	    echo InsDoc('R', 'show_gro');					///  跨領域學程
	    echo InsDoc('R', 'update_course');				///  所有異動科目
	    echo InsDoc('R', 'query_grade');				///  成績查詢
	    echo InsDoc('R', 'print_last');					///  上學期功課表
	    echo InsDoc('R', 'view_last');					///  上學期選課單
	  }else{
	    ///  行動版目前不開放此功能
	  }
    ?>
	
	aux2 = insFld(foldersTree, gFld("<?PHP echo $txt['qa']; ?>", ""))
	
	<?PHP
	  if( !$IS_MOBILE ) {
	    echo InsDoc('R', 'general_qa');		/// 一般問題
	    echo InsDoc('R', 'manual');			/// 系統操作手冊
	    echo InsDoc('R', 'doc');			/// 課表 doc 檔
	  }else{
	    ///  行動版目前不開放此功能
	  }
	  
	//aux2 = insFld(foldersTree, gFld("其他系統服務", ""))
    //insDoc(aux2, gLnk("B", "教務處", "http://www.ccu.edu.tw/oaa/oaa/index.php"))
    //insDoc(aux2, gLnk("B", "學籍資料登錄系統", "http://mis.cc.ccu.edu.tw/academic/"))
    //insDoc(aux2, gLnk("B", "資訊能力檢定", "http://infotest.ccu.edu.tw/"))
    //insDoc(aux2, gLnk("B", "英文能力檢定", "http://lconline.ccu.edu.tw/"))
	?>
  
   
  
foldersTree.treeID = "FramelessHili"


  </SCRIPT> 
  <!SCRIPT src="bookmark.js"><!/SCRIPT>
  
  <TABLE border=0> 
    <TR>
      <TD valign=TOP>
  <FONT size=2>
  <?PHP 
    echo $txt['welcome'];

//    echo "login time = " . $session_data{login_time} . "<BR>\n";
    list($time_string, $time_string2) = gettime($session_data{'login_time'});
    echo("[$time_string2]<BR></FONT>\n");
  ?>
  <BR>
  <A target=_top href="logout.php?session_id=<?PHP echo $session_id ?>">
  <IMG border=0 src="<?PHP echo $GRAPH_URL ?>logout.jpg" alt="我要登出系統"></A>
  </FONT>
  <?PHP 
    
    $password_last_time = Password_Too_Old($student["id"]);
	$txt = Init_Text_Values();								///  再一次初始化顯示文字（中文或英文）

    if( $password_last_time > $PASSWORD_MAX_CHANGE_TIME2 ) {		//  密碼太太久，強迫更新
	  //$msg =  "<FONT color=RED>您的密碼已經有 " . $password_last_time . " 天沒有更新了!";
	  //$msg .= "請先更新密碼後再選課!</FONT>";
	  //$msg .= "<P><A href='Change_Password00.php?session_id=$session_id' target=basefrm>更新密碼與email信箱</A><P>";
	  //Show_Special_Message("=>" . $password_last_time);
	  Show_Special_Message($txt['pwd_remind2']);
      if( ($SUPERUSER!= 1) and ($id != "999999999") )  exit();
    }else if( $password_last_time != 0 ) {							//  密碼太久，建議更新
      //$msg =  "提醒您, 選課密碼請定期更新(最好三個月一次), 以策安全!<BR>";
	  //$msg .= "您的密碼已經有 " . $password_last_time . " 天沒有更新了!";
	  //Show_Special_Message("-> " . $password_last_time);
	  Show_Special_Message($txt['pwd_remind']);
    }

	if( !$DEBUG20130916 ) {
	  /////  2013/08/28 若目前設定為可填寫2013選課改制問卷，則要求舊生一定要填寫
	  $DBH_kiki = PDO_connect($KIKI_DB_NAME);
	  $sql = "SELECT count(*) FROM questionnaire2013 WHERE stu_id = ?";
	  $STH = $DBH_kiki->prepare($sql);
	  $STH->execute(array($student["id"]));
	  $ques = $STH->fetch(PDO::FETCH_NUM);
	}else{
	  $ques[0] = 1;
	}
	
	
	if( $system_settings['questionnaire2013'] >= 1 ) {
	  if( $student{'enrollnum'} > 1 ) {										///  舊生可填
	    if( 0==$ques[0] ) {														/// 尚未填寫：給填寫的訊息	    
		  $msg =  "<FONT color=RED>同學您好：<BR>";
		  $msg .= "選課制度將有重大變革，煩請";
		  $msg .= "<A href='Questionnaire2013_1.php?session_id=$session_id' target=basefrm>填寫意見調查表！</A></FONT>";
		}else{																	/// 已經填寫：給可以修改的訊息
		  $msg =  "<FONT color=RED>如同學欲更改問卷內容，請於選課截止9月30日晚上10點前完成修改。<BR>";
		  $msg .= "<A href='Questionnaire2013_1.php?session_id=$session_id' target=basefrm>更改意見調查表！</A></FONT>";
		}
		Show_Special_Message($msg);
			
		if( (0==$ques[0]) and ($system_settings['questionnaire2013'] == 2) ) {			///  尚未填過且設定要求必填
		  if( ($SUPERUSER!= 1) and ($IS_ENGLISH != "1") )  {
			echo "<A href='Questionnaire2013_0.php?session_id=$session_id' target=basefrm>加選</A></FONT><BR>\n";
			echo "<A href='Questionnaire2013_0.php?session_id=$session_id' target=basefrm>退選</A></FONT><BR>\n";
		    exit();
		  }
		}
	  }
	}

	/////  2013/06/20 疑似拖慢速度，暫時先隱藏起來 Nidalap :D~  <--- 看似不是它的問題，解除封鎖！
    
	$email = Get_Email($id);
    if( isset($use_default_password) or($email == "")  ) {		//  如果使用預設密碼 or Email 信箱無資料
      //$msg =  "<FONT color=RED size=-1>您使用預設密碼或是尚未填寫 email 信箱，請先 ";
	  //$msg .= "<A target=basefrm href='Change_Password00.php?session_id=" . $session_id . "'>更新您的密碼</A><FONT>\n";
	  Show_Special_Message($txt['pwd_default']);
      if( ($SUPERUSER != 1) and ($id != "999999999") )  exit();
    }    
	
    if( Need_Special_Message($student{'id'}) ) {
      echo("<TABLE border=0><TR><TD><HR></TD></TR><TR><TD bgcolor=YELLOW>");
      echo("<FONT color=RED size=-1><A href=\"special_message.html\" target=basefrm>" . $txt['new_msg'] . "</A><FONT>");
      echo("</TD></TR><TR><TD><HR></TD></TR></TABLE>");
    }
  ?>

 <TABLE cellpadding="0" cellspacing="0" border="0">
  <TR>
   <TD valign="top">

    <TABLE cellpadding="0" cellspacing="0" border="0" width="100%">
     <TR>
      <TD bgcolor="#ECECD9">

        <TABLE cellspacing="0" cellpadding="2" border="0" width="100%">
         <TR>
          <TD bgcolor="white">

<?PHP if( $IS_MOBILE ) {  Show_Mobile_Menu();  }  ?>
		  
 <TABLE border=0><TR><TD><FONT size=-2><A href="http://www.treemenu.net/" target=_blank></A></FONT></TD></TR></TABLE>

 <SPAN class=TreeviewSpanArea>
  <SCRIPT>initializeDocument()</SCRIPT>
  <NOSCRIPT>
   A tree for site navigation will open here if you enable JavaScript in your browser.
  </NOSCRIPT>
 </SPAN>

          </TD>
         </TR>
        </TABLE>

       </TD>
      </TR>
     </TABLE>

    </TD>
    <TD bgcolor="white" valign="top">

     <TABLE cellpadding="10" cellspacing="0" border="0" width="100%">
      <TR>
       <TD>


       </TD>
      </TR>
     </TABLE>

    </TD>
   </TR>
  </TABLE>

      </TD>
      <TD valign=TOP>
        <!IMG src="pic/vline.jpg">
      </TD>
    </TR>
  </TABLE>

 </BODY>

</HTML>

<?PHP
  //////////////////////////////////////////////////////////////////////////////////////////////
  /////  印出 treeview 所需的 javascript 程式碼
  function InsDoc($type, $key)
  {
    global $txt;
    $html = "insDoc(aux2, gLnk('" . $type . "', '" . $txt[$key] . "', '" . $txt[$key . '_url'] . "'))\n";
	return $html;
  }
  //////////////////////////////////////////////////////////////////////////////////////////////
  function Show_Special_Message($text) 
  {
    echo "<CENTER><TABLE border=0><TR><TD><HR></TD></TR><TR><TD bgcolor=YELLOW>";
    echo $text;
    echo "</TD></TR><TR><TD><HR></TD></TR></TABLE></CENTER>";
  }
  //////////////////////////////////////////////////////////////////////////////////////////////
  /////  顯示行動化版本主選單
  function Show_Mobile_Menu()
  {
    global $m_txt, $session_id;
/*	
	if( ($system_settings{'sysstate'} >= 1 ) or ($SUPERUSER == 1)) { }
	
	if ( $add_flag >= 1) {
      if( $ban_flag and !($SUPERUSER) ) {							//  被停權
        $ban_html = "<SPAN>停權公告</SPAN>";
	    $add_html = "<SPAN class='unavailable'>加選</SPAN>";
	    $del_html = "<SPAN class='unavailable'>退選</SPAN>";
      }else{											//  沒有被停權
		$ban_html = "";
	    $add_html = "<SPAN class='unavailable'><A href='Add_Course00.cgi?session_id=$session_id'>加選</A></SPAN>";
	    $del_html = "<SPAN class='unavailable'><A href='Del_Course00.cgi?session_id=$session_id'>退選</A></SPAN>";
      }
    }
*/
	$m_txt['daily_course'] = "<A href='Daily_Course.php?session_id=$session_id&m=1'>今日課表</A>";
	
	
	echo "
	  <CENTER>
	  <IMG src='../../Graph/title.gif'>
	  <TABLE border=1 width=75%>
	    <TR>
		  <TD width=50%>" . $m_txt['daily_course'] . "</TD>
		  <TD width=50%>" . $m_txt['view'] . "</TD>
		</TR>
		<TR><TD colspan=2>&nbsp;</TD></TR>
		<TR>
		  <TD>" . $m_txt['add'] . "</TD>
		  <TD>" . $m_txt['del'] . "</TD>
		</TR>
	    <TR>
		  <TD>系統狀態</TD>
		  <TD>系統公告</TD>
		</TR>
	    <TR>
		  <TD>" . $m_txt['change_pwd'] . "</TD>
		  <TD>我的加簽單</TD>
		</TR>
		<TR><TD colspan=2>&nbsp;</TD></TR>
		<TR><TD colspan=2>登出</TD></TR>
	  </TABLE>
	  <CENTER>
	";
	
	die();
  
  }
  
  //////////////////////////////////////////////////////////////////////////////////////////////
  /////  因應英文版本，將所有要顯示的文字在此整理，依照 $IS_ENGLISH 自動判別  2013/07/10
  function Init_Text_Values()
  {
    global $IS_ENGLISH, $KIKI_URL, $HOME_URL, $CLASS_URL, $QUERY_URL;
	global $session_id, $student, $ban_res_time, $password_last_time;
	global $system_settings, $year, $term;
		
	$sname = $IS_ENGLISH ? $student['ename'] : $student['name'];
	$last_term_get_str = '';
	if( $system_settings['redirect_to_query'] == 1 ) {
	  $last_term_get_str = '&year=' . $year . '&term=' . $term;
	}
	
	$txtall = array(
	  'welcome'		=> array('c'=>$sname . ' 同學, 歡迎!<BR>您本次的登入時間是:', 
						'e'=>'Welcome, ' . $sname . '!<BR>Login time:'), 
	  'menu'		=> array('c'=>'主選單', 'e'=>'Main Menu'),
	  'db_fail'		=> array('c'=>'資料庫連線錯誤', 'e'=>'Failed connecting to database'),
	  'announce'	=> array('c'=>'選課系統公告', 'e'=>'Announcement', 
						'url'=>'announce.php?session_id=' . $session_id),
	  'about'		=> array('c'=>'選課系統相關', 'e'=>'Course Selection Menu'),
	  'add'			=> array('c'=>'加選', 'e'=>'Add', 
						'url'=> 'Add_Course00.cgi?session_id=' . $session_id),
	  'del'			=> array('c'=>'退選', 'e'=>'Drop',
						'url'=> 'Del_Course00.cgi?session_id=' . $session_id),
	  'view'		=> array('c'=>'檢視已選修科目', 'e'=>'Preview Courses Selected', 
						'url'=> 'Selected_View00.cgi?session_id=' . $session_id),
	  'view_warning'=> array('c'=>'檢視篩選公告', 'e'=>'View Course Screening Result',
						'url'=> 'View_Warning.cgi?session_id=' . $session_id),
	  'view_pdf'	=> array('c'=>'檢視選課結果單PDF', 'e'=>'View Final Courses Selection List',
						'url'=> 'Print_Course_pdf.cgi?session_id=' . $session_id),
	  'my_concent'	=> array('c'=>'我的加簽單', 'e'=>'View Add Permission Form',
						'url'=> 'My_Concent_Forms.php?session_id=' . $session_id),
	  'print'		=> array('c'=>'列印選課單', 'e'=>'Print Final Course Selection List',
						'url'=> 'Print_Course.cgi?session_id=' . $session_id),
	  'change_pwd'	=> array('c'=>'更改密碼', 'e'=>'Change Password',
						'url'=> 'Change_Password00.php?session_id=' . $session_id),
	  'support'		=> array('c'=>'支援本班課程', 'e'=>'Courses with Priority Screening',
						'url'=> 'Support_Courses.cgi?session_id=' . $session_id),
	  'query'		=> array('c'=>'資料查詢', 'e'=>'Search'),
	  'query_course'=> array('c'=>'查詢開課資料', 'e'=>'Browse Courses',
						'url'=> $HOME_URL . 'Course/index.html'),
	  'query_adv'	=> array('c'=>'進階開課資料查詢', 'e'=>'Advanced Course Search',
						'url'=> '../Query/Query_by_time1.cgi?session_id=' . $session_id . '&get_my_table=1'),
	  'show_gro'	=> array('c'=>'跨領域學程', 'e'=>'Interdisciplinary Courses', 
						'url'=> 'Show_All_GRO.cgi?session_id=' . $session_id),
	  'update_course'=> array('c'=>'所有異動科目', 'e'=>'Courses with Recent Revision',
						'url'=> 'Update_Course.php'),
	  'query_grade'	=> array('c'=>'成績查詢', 'e'=>'Grade Inquiry',
						'url'=> '../Query/index.html'),
	  'print_last'	=> array('c'=>'上學期功課表', 'e'=>'Course Schedule(Last Semester)',
						'url'=>'Selected_View00.cgi?year=' . $year . '&term=' . $term . '&session_id=' . $session_id),
	  'view_last'	=> array('c'=>'上學期選課單', 'e'=>'Course List(Last Semester)',
						'url'=>'Print_Course.cgi?year=' . $year . '&term=' . $term . '&session_id=' . $session_id),
	  'qa'			=> array('c'=>'問題與表單下載', 'e'=>'Q&A and Download'),
	  'general_qa'	=> array('c'=>'一般問題', 'e'=>'General Q&A',
						'url'=> $KIKI_URL . 'contact.html'),
	  'manual'		=> array('c'=>'系統操作手冊', 'e'=>'User Manual',
						'url'=> $KIKI_URL . 'user_manual/user_manual.htm'),
	  'doc'			=> array('c'=>'課表doc檔', 'e'=>'Schedule Template(doc file)',
						'url'=> $KIKI_URL . 'ccu_timetable.doc'),
	  'pwd_remind'	=> array('c'=>'提醒您, 選課密碼請定期更新(最好三個月一次), 以策安全!<BR>' 
							. '您的密碼已經有 ' . $password_last_time . ' 天沒有更新了!',
						'e'=>'You have not changed your password for ' . $password_last_time 
							. ' days. Please do it now before you login to the system.'),
	  'pwd_default'	=> array('c'=>'<FONT color=RED size=-1>您使用預設密碼或是尚未填寫 email 信箱，請先 '
							. '<A target=basefrm href="Change_Password00.php?session_id=' . $session_id . '">更新您的密碼</A><FONT>', 
						'e'=>'You are now either still using the default password or havn\'t'
							. ' provided your E-mail address, please change your password first.'),
	  'pwd_remind2'	=> array('c'=>'<FONT color=RED>您的密碼已經有 ' . $password_last_time . ' 天沒有更新了!'
							. '請先更新密碼後再選課!</FONT>' 
							. '<P><A href="Change_Password00.php?session_id=' . $session_id . '" target=basefrm>更新密碼與email信箱</A><P>', 
						'e'=>'You have not changed your password for ' . $password_last_time 
							. ' days. Please do it now before you login to the system.'),

	  'new_msg'		=> array('c'=>'您有一封來自系統的訊息!!', 'e'=>'You have a new message!!'),
	  'ban_msg'		=>array('c'=>'停權公告', 'e'=>'Ban Message',
						'url'=>'Show_Ban_Message.php?ban_res_time=' . $ban_res_time),
	  'withdrawal'	=> array('c'=>'申請棄選', 'e'=>'Withdrawal Application',
						'url'=>'Selected_View00.cgi?session_id=' . $session_id . $last_term_get_str),
	  'my_withdrawal'	=> array('c'=>'我的棄選單', 'e'=>'My Withdrawal Application Form',
						'url'=>'My_Withdrawal_Form.php?session_id=' . $session_id),
	  'my_plan'		=> array('c'=>'<SPAN style="background:YELLOW; color:RED">我的選課計畫</SPAN>', 
						'e'=>'<SPAN style="background:YELLOW; color:RED">My Course Plans</SPAN>',
						'url'=>'My_Plan_Course?session_id=' . $session_id),
	  'graduate'	=> array('c'=>'檢視畢業資格審查表', 'e'=>'檢視畢業資格審查表',
						'url'=>'Print_Graduate_pdf.cgi?session_id=' . $session_id),
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