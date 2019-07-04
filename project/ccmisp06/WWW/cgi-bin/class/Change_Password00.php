<?PHP
  ///////////////////////////////////////////////////////////////////////////////////////////
  /////  Change_Password01.php
  /////  提供更改密碼與 email 表單
  /////  Updates:
  /////    20??/??/?? Created by Nidalap :D~
  /////    2013/08/08 英文版相關增修：將顯示文字拉到 Init_Text_Values() 中設定。 Nidalap :D~
  /////    2014/02/10 加入行動版相關判斷與畫面最佳化 by Nidalap :D~
  
  require_once "../php_lib/Reference.php";
  require_once $LIBRARY_PATH . "Common_Utility.php";
  require_once $LIBRARY_PATH . "Session.php";
  require_once $LIBRARY_PATH . "Password.php";
  require_once $LIBRARY_PATH . "Database.php";
  require_once $LIBRARY_PATH . "Student.php";
  require_once $LIBRARY_PATH . "Dept.php";
  require_once $LIBRARY_PATH . "English.php";

  $session_id	= in_array("session_id", $_POST) ? $_POST["session_id"] : $_GET["session_id"];
  
  if(isset($_POST["id"]))  { $id		= $_POST["id"];  }
  if(isset($_POST["key"])) { $key		= $_POST["key"]; }
  global $BG_PIC;
 
//  echo("[$IS_GRA]");
//  echo("id = $id<BR>\n");
 
//  db_connect("","");
  $DBH = PDO_connect($DATABASE_NAME);
  $txt = Init_Text_Values();								///  初始化顯示文字（中文或英文）
  
//  echo("session_id = $session_id<BR>\n");
  if( $session_id != "" ) {                 //  如果是從選課系統連過來的
    $session_data = Read_Session($session_id);
//    list($id, $password, $login_time, $ip, $add_course_count) = $session_data;
    $id			= $session_data{"id"};
    $password		= $session_data{"password"};
    $login_time		= $session_data{"login_time"};
    $ip			= $session_data{"ip"};
    $add_course_count	= $session_data{"add_course_count"};
    $student = Read_Student($id);
    $dept = Read_Dept($student{"dept"});
//    print_r($student);
//    $HEAD_DATA = Form_Head_Data($id, $student{"name"}, $dept{"cname"}, $student{"grade"}, $student{"class_"});
  if( $IS_ENGLISH ) {
    $HEAD_DATA = Form_Head_Data($id, $student{"ename"}, $dept{"ename"}, $student{"grade"}, $student{"class_"});
  }else{
    $HEAD_DATA = Form_Head_Data($id, $student{"name"}, $dept{"cname"}, $student{"grade"}, $student{"class_"});
  }
  	
//    $HEAD_DATA = Form_Head_Data($id, $student{name}, $dept{cname}, $student{grade}, $student{class});
    Check_Password($id, $password, "", "");
  }else{				    //  不然就是從學籍系統連過來的
    $password = $_POST["password"];
    Check_Key($key, $id, $password);		//  基本的安全檢查
    list($personid, $name, $dept, $dept_name, $grade, $class, $pwd_db) = Read_Personal_Data_From_Database($id);
//    echo("[id, personid, name, dept, dept_name, grade, class, pwd_db] = [$id, $personid, $name, $dept, $dept_name, $grade, $class, $pwd_db]<P>\n");
    Check_Password_Database($id, $password, $pwd_db);
    $HEAD_DATA = Form_Head_Data($id, $name, $dept_name, $grade, $class);
  }

//  echo("$id, $password, $login_time, $ip, $add_course_count");
//  $HEAD_DATA = Form_Head_Data($id, $student{name}, $dept_name, $grade, $class);
  $email = Get_Email($id);


 
?>

<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <TITLE><?PHP echo $txt['html_title'] ?></TITLE>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
	<?PHP if( $IS_MOBILE >= 1 ) 	echo $MOBILE_META_TAG  ?>
</head>
<body background=<?PHP echo $BG_PIC; ?>>
<center>
  <?PHP 
    if( $IS_MOBILE >= 1 ) 	echo Create_jQuery_Mobile_Title_Tag();
	else					echo $HEAD_DATA; 
  ?>
  <hr>
  <FORM action="Change_Password01.php" method=POST id="form1">
    <?PHP 
	  if( $IS_MOBILE >= 1 )	$width = "95%";
	  else					$width = "75%";
	  echo "<TABLE border=0 width=$width><TR><TD><UL>";
	  
	  if( $IS_MOBILE == 0 ) {
	    echo "<LI><FONT size=-1>" . $txt['note1'] . "\n";
	    echo "<LI>" . $txt['note2'] . "\n";
	    echo "<LI>" . $txt['note3'] . "\n";
	  }
	  echo "<LI>" . $txt['note4'] . "\n";
	  
	  echo "</TD></TR></TABLE>";
	?>
    <P>
    <TABLE border=0>
      <TR><TD><?PHP echo $txt['old_pass'] ?></TD>
          <TD><INPUT type=password name="old_password"></TD></TR>
      <TR><TD><?PHP echo $txt['new_pass'] ?></TD>
          <TD><INPUT type=password name="new_password"></TD></TR>
      <TR><TD><?PHP echo $txt['confirm_pass'] ?></TD>
          <TD><INPUT type=password name="check_password"></T D></TR>
      <TR><TD><?PHP echo $txt['email'] ?></TD>
          <TD><INPUT type=text name="email" value=<?PHP echo $email; ?>></TD></TR>
    </TABLE>
    <?PHP 
      if( $session_id == "" ) {                 //  如果是從學籍系統連過來的
        echo("<INPUT type=hidden name=id value=\"$id\">\n");
        echo("<INPUT type=hidden name=key value=\"$key\">\n");
      }
	  if( $IS_ENGLISH ) {
	    echo "<INPUT type=hidden name='e' value='1'>\n";
	  }
    ?>
    <INPUT type=hidden name="session_id" value="<?PHP echo $session_id; ?>">
    <INPUT type=hidden name=HEAD_DATA value="<?PHP echo $HEAD_DATA; ?>"> 
    <INPUT type="submit" value="<?PHP echo $txt['submit'] ?>" id="submit"><p>

  </FORM>
  <?PHP if( $IS_MOBILE >= 1 ) 	echo Create_jQuery_Mobile_Footer_Tag(); ?>
</BODY>
  <!--  <script type="text/javascript" src="https://www.google.com/jsapi"></script>  -->
  <SCRIPT type="text/javascript" src="../../javascript/jquery.js"></SCRIPT>
  <script type="text/javascript" language="JavaScript">
//    google.load("jquery", "1.6.2");   
//    alert("ccc");
    $(document).ready(function(){
      $('#my_form').preventDoubleSubmit();
      jQuery.fn.preventDoubleSubmit = function() {
        jQuery(this).submit(function() {
          if (this.beenSubmitted)
            return false;
          else
           this.beenSubmitted = true;
        });
      };
//      $("#submit").click(function(){
//        $(this).attr("disabled", "disabled");
//        alert("ccc");
//        return true;
        
//        $("#form1").submit();
//        $(this).attr("disabled", "disabled");
//        alert("ddd");
//      })
    });
  </SCRIPT>
</HTML>

<?PHP
  //////////////////////////////////////////////////////////////////////////////////////////////
  /////  因應英文版本，將所有要顯示的文字在此整理，依照 $IS_ENGLISH 自動判別  2013/08/08
  function Init_Text_Values()
  {
    global $IS_ENGLISH, $MIN_PASSWORD_LENGTH, $MAX_PASSWORD_LENGTH;
	//global $session_id, $student, $ban_res_time, $password_last_time;
	//global $year, $term;
	
	$sname = $student['name'];
	
	$txtall = array(
	  'html_title'	=> array('c'=>'更改密碼', 'e'=>'Change Password'), 
	  'note1'		=> array('c'=>'即日起選課系統將與學籍, 資訊能力測驗等系統密碼整合.
								您在這裡更改的密碼, 將會同時更新您在這幾個系統上的密碼.
								(資訊能力測驗系統將有約五分鐘的時間差, 請稍後再登入該系統)',
						     'e'=>'The Course Selection system has been integrated with 
							    CCU Registration and IT Examination System.
								Your password change will apply to the other two systems as well 
								(IT Examination System may have 5-minute delay).'),
	  'note2'		=> array('c'=>'若您尚未更改過密碼, 請輸入身分證號(開頭英文應為大寫). ', 
							 'e'=>'If you have not change your password, please type in the 
							    password you use for Student Academic Record Entry System.'),
	  'note3'		=> array('c'=>'為確保將來系統主動通知您重要訊息, 請同時確認 email 信箱! ', 
							 'e'=>'In order to make sure you will receive information and 
							    future notice, please confirm your email address'),
	  'note4'		=> array('c'=>'密碼規範：長度介於 ' . $MIN_PASSWORD_LENGTH . ' 到 ' . $MAX_PASSWORD_LENGTH . ' 之間， 
								請使用大小寫英文、數字、及以下特殊字元組合 「! @ $ ^ _ -」', 
							 'e'=>'Password Rule: ' . $MIN_PASSWORD_LENGTH . ' to ' . $MAX_PASSWORD_LENGTH . ' digits, mixing capital and 
								uncapitalized letters, number and special characters (!@$^_-).'),
	  'old_pass'	=> array('c'=>'原來的密碼: ', 
							 'e'=>'Please enter your old password: '),
	  'new_pass'	=> array('c'=>'新密碼: ', 
							 'e'=>'Please enter your new password: '),
	  'confirm_pass'=> array('c'=>'確認新密碼: ', 
							 'e'=>'Please confirm new password: '),
	  'email'		=> array('c'=>'確認 e-mail:  ', 
							 'e'=>'Please confirm your e-mail: '),
	  'submit'		=> array('c'=>'確認更改', 
							 'e'=>'Change My Password')
 
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
