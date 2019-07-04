<?PHP
  include "../library/Reference.php";
  include $LIBRARY_PATH . "Error_Message.php";
  include $LIBRARY_PATH . "Common_Utility.php";
  include $LIBRARY_PATH . "Password.php";
  include $LIBRARY_PATH . "Session.php";
  include $LIBRARY_PATH . "Student.php";
  include $LIBRARY_PATH . "Select_Course.php";
  include $LIBRARY_PATH . "System_Settings.php";
   
  $system_settings = Get_System_State();

  if( isset($_POST['session_id'])  ) {						//  如果是自己 reload
    $session_data	= Read_Session( $_POST['session_id']);
    $id			= $session_data{'id'};
    $password		= $session_data{'password'};
    $temp = "POST";
  }else if( isset($_GET['session_id'])  ) {					//  用 GET reload
    $session_data	= Read_Session( $_GET['session_id']);
    $id			= $session_data{'id'};
    $password		= $session_data{'password'};
    $temp = "GET";
  }else{								//  如果剛登入
//    $session_id = Create_Session_ID($id, $password);
//    echo("new session<BR>\n");
    $id			= $_POST{'id'};
    $password		= $_POST{'password'};
    $session_id = Create_Session_ID($id, $password);
    
    $salt = Read_Crypt_Salt($id);           
    $password = my_Crypt($password, $salt);  
   
    Write_Session($session_id, $id, $password, 0);
    $session_data       = Read_Session($session_id);
        
//    $salt = Read_Crypt_Salt($_POST['id']);
//    $password = my_Crypt($_POST['password'], $salt);
//    $password_validation = Check_Password($id, $password, "new");
  }
  
//  echo("temp = $temp<BR>\n");
//  print_r($session_data);

/*  $salt = Read_Crypt_Salt($_POST['id']);
  $password = my_Crypt($_POST['password'], $salt);
  $password_validation = Check_Password($id, $password, "new");
*/
  $password_validation = Check_Password($id, $password, "new");
  $student = Read_Student($id);

  $ban_res_time = Read_Ban_Record($id);							// 讀取停權剩餘時間
//  $ban_res_time = 1223;
  $ban_flag = 0;
  if( ( $system_settings{'black_list'} == 1) and ( $ban_res_time > 0 ) )  $ban_flag = 1;	// 停權與否
  
?>
<HTML>
  <HEAD>
  <meta http-equiv="Content-Type" content="text/html; charset=big5">
  <META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE">
  <meta http-equiv="refresh" content="<?PHP echo $REFRESH_TIME_BOOKMARK ?>; 
        URL=bookmark.php?session_id=<?PHP echo $session_id ?>">
  <TITLE>主選單</TITLE>
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

 <BODY leftmargin="0" topmargin="0" marginheight="0" marginwidth="0"  onResize="if (navigator.family == 'nn4') window.location.reload()">
<?PHP
/*
  $system_settings = Get_System_State();
//  print_r($system_settings);
  
  $salt = Read_Crypt_Salt($_POST['id']);
  $password = my_Crypt($_POST['password'], $salt);
  $password_validation = Check_Password($id, $password, "new");
  
//  echo("SUPERUSER = $SUPERUSER<P>");
  
  if( $_POST['session_id'] != "" ) {
    $session_data = Read_Session( $_POST['session_id']);
  }else if( $_GET['session_id'] != "" ) {
    $session_data = Read_Session( $_GET['session_id']);
  }else{
    $session_id = Create_Session_ID($id, $password);
    Write_Session($session_id, $id, $password, 0); 
    $session_data = Read_Session($session_id);
    echo("new session<BR>\n");
  }
    print_r($session_data);

//  print("session_id = $session_id<BR>\n"); 

  $student = Read_Student($id);
*/
?>
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
foldersTree = gFld("<b>主選單</b>", "")
  aux2 = insFld(foldersTree, gFld("系統公告", ""))
    <?PHP
       echo "insDoc(aux2, gLnk(\"R\", \"選課系統公告\", \"announce.php?session_id=" .  $session_id . "\"))\n";
    ?>

  aux2 = insFld(foldersTree, gFld("選課系統相關", ""))
    <?PHP 
      $add_flag = 0;					//  用來判斷是否可加退選
      if( ($system_settings{'sysstate'} == 2) and Check_Time_Map($student)  )	$add_flag = 1;
      if( $SUPERUSER == 1 )							$add_flag = 1;      
      
      if ( $add_flag ) {
        if( $ban_flag and !($SUPERUSER) ) {							//  被停權
          echo "insDoc(aux2, gLnk(\"R\", \"停權公告\", \"Show_Ban_Message.php?ban_res_time=" . $ban_res_time . "\"))\n";
        }else{											//  沒有被停權
          echo "insDoc(aux2, gLnk(\"R\", \"加選\", \"Add_Course00.cgi?session_id=" . $session_id . "\"))\n";
          echo "insDoc(aux2, gLnk(\"R\", \"支援本班課程\", \"Support_Courses.cgi?session_id=" . $session_id . "\"))\n";
          echo "insDoc(aux2, gLnk(\"R\", \"退選\", \"Del_Course00.cgi?session_id=" . $session_id . "\"))\n";
        }
      } 
      if( ($system_settings{'sysstate'} >= 1 ) or ($SUPERUSER == 1)) {
        echo "insDoc(aux2, gLnk(\"R\", \"檢視已選修科目\", \"Selected_View00.cgi?session_id=" .  $session_id . "\"))\n";
      }
      echo "insDoc(aux2, gLnk(\"R\", \"檢視篩選公告\", \"View_Warning.cgi?session_id=" . $session_id . "\"))\n";
      if ( ( ($system_settings{'allow_print_graduate_pdf'} == 1) or ($SUPERUSER == 1))
           and ($student{'grade'} >=3) and ( preg_match("/^4/", $student{'id'}) ) ) {  
        echo "insDoc(aux2, gLnk(\"R\", \"檢視畢業資格審查表\", \"Print_Graduate_pdf.cgi?session_id=" . $session_id . "\"))\n";
      }
      if ( ($system_settings{'allow_print_pdf'} == 1) or ($SUPERUSER == 1) ) {
        echo "insDoc(aux2, gLnk(\"R\", \"檢視選課結果單pdf\", \"Print_Course_pdf.cgi?session_id=" . $session_id . "\"))\n";
      }
    ?>
    insDoc(aux2, gLnk("R", "列印選課單", "Print_Course.cgi?session_id=<?PHP echo $session_id ?>"))
    insDoc(aux2, gLnk("R", "更改密碼", "Change_Password00.php?session_id=<?PHP echo $session_id ?>"))

  aux2 = insFld(foldersTree, gFld("資料查詢", ""))
    <?PHP
      list($year, $term) = Last_Semester(1);
      
      echo "insDoc(aux2, gLnk(\"R\", \"查詢開課資料\", \"" . $HOME_URL . "Course/\"))\n";
      echo "insDoc(aux2, gLnk(\"R\", \"以時間查詢開課資料\", \"" . $QUERY_URL . "Query_by_time1.cgi\"))\n";
      echo "insDoc(aux2, gLnk(\"R\", \"檢視所有異動科目\", \"" . $HOME_URL . "Update_Course.html\"))\n";
      echo "insDoc(aux2, gLnk(\"R\", \"成績查詢\", \"" . $QUERY_URL . "\"))\n";
      echo "insDoc(aux2, gLnk(\"R\", \"上學期功\課表\", \"Selected_View00.cgi?year=" . $year . "&term=" . $term . "&session_id=" .  $session_id . "\"))\n";
      echo "insDoc(aux2, gLnk(\"R\", \"上學期選課單\", \"Print_Course.cgi?year=" . $year . "&term=" . $term . "&session_id=" . $session_id . "\"))\n";
    ?>

  aux2 = insFld(foldersTree, gFld("問題與表單下載", ""))
    insDoc(aux2, gLnk("R", "一般問題", "http://kiki.ccu.edu.tw/contact.html"))
    insDoc(aux2, gLnk("R", "系統操作手冊", "http://kiki.ccu.edu.tw/user_manual/user_manual.htm"))
    insDoc(aux2, gLnk("B", "課表 doc 檔", "http://kiki.ccu.edu.tw/ccu_timetable.doc"))

  aux2 = insFld(foldersTree, gFld("其他系統服務", ""))
    insDoc(aux2, gLnk("B", "教務處", "http://www.ccu.edu.tw/oaa/oaa_english/index.php"))
    insDoc(aux2, gLnk("B", "學籍資料登錄系統", "http://mis.cc.ccu.edu.tw/academic/"))
    insDoc(aux2, gLnk("B", "資訊能力檢定", "http://infotest.ccu.edu.tw/"))
    insDoc(aux2, gLnk("B", "英文能力檢定", "http://lconline.ccu.edu.tw/"))

foldersTree.treeID = "FramelessHili"


  </SCRIPT> 
  <!SCRIPT src="bookmark.js"><!/SCRIPT>
      
  <TABLE border=0> 
    <TR>
      <TD valign=TOP>
  <FONT size=2>
  <?PHP 
//    $name = $student{name};
//    echo name ;
//    echo($student{dept});
    echo($student{'name'});
  
  ?> 同學, 歡迎!<BR>
  您本次的登入時間是:<BR>
  <?PHP
//    echo "login time = " . $session_data{login_time} . "<BR>\n";
    list($time_string, $time_string2) = gettime($session_data{'login_time'});
    echo("[$time_string2]<BR></FONT>\n");
  ?>
  <BR>
  <A target=_top href="logout.php?session_id=<?PHP echo $session_id ?>">
  <IMG border=0 src="<?PHP echo $GRAPH_URL ?>logout.jpg" alt="我要登出系統"></A>
  </FONT>
  <?PHP 
    if( Need_Special_Message($student{'id'}) ) {
      echo("<TABLE border=0><TR><TD><HR></TD></TR><TR><TD bgcolor=YELLOW>");
      echo("<FONT color=RED><A href=\"special_message.html\" target=basefrm>您有一封來自系統的訊息!!</A><FONT>");
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


 <TABLE border=0><TR><TD><FONT size=-2><A style="font-size:7pt;text-decoration:none;color:silver" href="http://www.treemenu.net/" target=_blank></A></FONT></TD></TR></TABLE>

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