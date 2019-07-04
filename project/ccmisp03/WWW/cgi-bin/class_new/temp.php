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

  if( isset($_POST['session_id'])  ) {						//  �p�G�O�ۤv reload
    $session_data	= Read_Session( $_POST['session_id']);
    $id			= $session_data{'id'};
    $password		= $session_data{'password'};
    $temp = "POST";
  }else if( isset($_GET['session_id'])  ) {					//  �� GET reload
    $session_data	= Read_Session( $_GET['session_id']);
    $id			= $session_data{'id'};
    $password		= $session_data{'password'};
    $temp = "GET";
  }else{								//  �p�G��n�J
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

  $ban_res_time = Read_Ban_Record($id);							// Ū�����v�Ѿl�ɶ�
//  $ban_res_time = 1223;
  $ban_flag = 0;
  if( ( $system_settings{'black_list'} == 1) and ( $ban_res_time > 0 ) )  $ban_flag = 1;	// ���v�P�_
  
?>
<HTML>
  <HEAD>
  <meta http-equiv="Content-Type" content="text/html; charset=big5">
  <META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE">
  <meta http-equiv="refresh" content="<?PHP echo $REFRESH_TIME_BOOKMARK ?>; 
        URL=bookmark.php?session_id=<?PHP echo $session_id ?>">
  <TITLE>�D���</TITLE>
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
foldersTree = gFld("<b>�D���</b>", "")
  aux2 = insFld(foldersTree, gFld("�t�Τ��i", ""))
    <?PHP
       echo "insDoc(aux2, gLnk(\"R\", \"��Ҩt�Τ��i\", \"announce.php?session_id=" .  $session_id . "\"))\n";
    ?>

  aux2 = insFld(foldersTree, gFld("��Ҩt�ά���", ""))
    <?PHP 
      $add_flag = 0;					//  �ΨӧP�_�O�_�i�[�h��
      if( ($system_settings{'sysstate'} == 2) and Check_Time_Map($student)  )	$add_flag = 1;
      if( $SUPERUSER == 1 )							$add_flag = 1;      
      
      if ( $add_flag ) {
        if( $ban_flag and !($SUPERUSER) ) {							//  �Q���v
          echo "insDoc(aux2, gLnk(\"R\", \"���v���i\", \"Show_Ban_Message.php?ban_res_time=" . $ban_res_time . "\"))\n";
        }else{											//  �S���Q���v
          echo "insDoc(aux2, gLnk(\"R\", \"�[��\", \"Add_Course00.cgi?session_id=" . $session_id . "\"))\n";
          echo "insDoc(aux2, gLnk(\"R\", \"�䴩���Z�ҵ{\", \"Support_Courses.cgi?session_id=" . $session_id . "\"))\n";
          echo "insDoc(aux2, gLnk(\"R\", \"�h��\", \"Del_Course00.cgi?session_id=" . $session_id . "\"))\n";
        }
      } 
      if( ($system_settings{'sysstate'} >= 1 ) or ($SUPERUSER == 1)) {
        echo "insDoc(aux2, gLnk(\"R\", \"�˵��w��׬��\", \"Selected_View00.cgi?session_id=" .  $session_id . "\"))\n";
      }
      echo "insDoc(aux2, gLnk(\"R\", \"�˵��z�綠�i\", \"View_Warning.cgi?session_id=" . $session_id . "\"))\n";
      if ( ( ($system_settings{'allow_print_graduate_pdf'} == 1) or ($SUPERUSER == 1))
           and ($student{'grade'} >=3) and ( preg_match("/^4/", $student{'id'}) ) ) {  
        echo "insDoc(aux2, gLnk(\"R\", \"�˵����~���f�d��\", \"Print_Graduate_pdf.cgi?session_id=" . $session_id . "\"))\n";
      }
      if ( ($system_settings{'allow_print_pdf'} == 1) or ($SUPERUSER == 1) ) {
        echo "insDoc(aux2, gLnk(\"R\", \"�˵���ҵ��G��pdf\", \"Print_Course_pdf.cgi?session_id=" . $session_id . "\"))\n";
      }
    ?>
    insDoc(aux2, gLnk("R", "�C�L��ҳ�", "Print_Course.cgi?session_id=<?PHP echo $session_id ?>"))
    insDoc(aux2, gLnk("R", "���K�X", "Change_Password00.php?session_id=<?PHP echo $session_id ?>"))

  aux2 = insFld(foldersTree, gFld("��Ƭd��", ""))
    <?PHP
      list($year, $term) = Last_Semester(1);
      
      echo "insDoc(aux2, gLnk(\"R\", \"�d�߶}�Ҹ��\", \"" . $HOME_URL . "Course/\"))\n";
      echo "insDoc(aux2, gLnk(\"R\", \"�H�ɶ��d�߶}�Ҹ��\", \"" . $QUERY_URL . "Query_by_time1.cgi\"))\n";
      echo "insDoc(aux2, gLnk(\"R\", \"�˵��Ҧ����ʬ��\", \"" . $HOME_URL . "Update_Course.html\"))\n";
      echo "insDoc(aux2, gLnk(\"R\", \"���Z�d��\", \"" . $QUERY_URL . "\"))\n";
      echo "insDoc(aux2, gLnk(\"R\", \"�W�Ǵ��\\�Ҫ�\", \"Selected_View00.cgi?year=" . $year . "&term=" . $term . "&session_id=" .  $session_id . "\"))\n";
      echo "insDoc(aux2, gLnk(\"R\", \"�W�Ǵ���ҳ�\", \"Print_Course.cgi?year=" . $year . "&term=" . $term . "&session_id=" . $session_id . "\"))\n";
    ?>

  aux2 = insFld(foldersTree, gFld("���D�P���U��", ""))
    insDoc(aux2, gLnk("R", "�@����D", "http://kiki.ccu.edu.tw/contact.html"))
    insDoc(aux2, gLnk("R", "�t�ξާ@��U", "http://kiki.ccu.edu.tw/user_manual/user_manual.htm"))
    insDoc(aux2, gLnk("B", "�Ҫ� doc ��", "http://kiki.ccu.edu.tw/ccu_timetable.doc"))

  aux2 = insFld(foldersTree, gFld("��L�t�ΪA��", ""))
    insDoc(aux2, gLnk("B", "�аȳB", "http://www.ccu.edu.tw/oaa/oaa_english/index.php"))
    insDoc(aux2, gLnk("B", "���y��Ƶn���t��", "http://mis.cc.ccu.edu.tw/academic/"))
    insDoc(aux2, gLnk("B", "��T��O�˩w", "http://infotest.ccu.edu.tw/"))
    insDoc(aux2, gLnk("B", "�^���O�˩w", "http://lconline.ccu.edu.tw/"))

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
  
  ?> �P��, �w��!<BR>
  �z�������n�J�ɶ��O:<BR>
  <?PHP
//    echo "login time = " . $session_data{login_time} . "<BR>\n";
    list($time_string, $time_string2) = gettime($session_data{'login_time'});
    echo("[$time_string2]<BR></FONT>\n");
  ?>
  <BR>
  <A target=_top href="logout.php?session_id=<?PHP echo $session_id ?>">
  <IMG border=0 src="<?PHP echo $GRAPH_URL ?>logout.jpg" alt="�ڭn�n�X�t��"></A>
  </FONT>
  <?PHP 
    if( Need_Special_Message($student{'id'}) ) {
      echo("<TABLE border=0><TR><TD><HR></TD></TR><TR><TD bgcolor=YELLOW>");
      echo("<FONT color=RED><A href=\"special_message.html\" target=basefrm>�z���@�ʨӦۨt�Ϊ��T��!!</A><FONT>");
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