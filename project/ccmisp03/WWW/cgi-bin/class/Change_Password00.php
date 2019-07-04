<?PHP
  include "../php_lib/Reference.php";
  include "../php_lib/Common_Utility.php";
  include "../php_lib/Session.php";
  include "../php_lib/Password.php";
  include "../php_lib/Sybase.php";
  
  $session_id	= $_POST['session_id'];
  if( $session_id == "" )  {  $session_id   = $_GET['session_id'];  }
  
  if(isset($_POST['id']))  { $id		= $_POST['id'];  }
  if(isset($_POST['key'])) { $key		= $_POST['key']; }
  global $BG_PIC;

//  echo("[$IS_GRA]");
//  echo("id = $id<BR>\n");
 
  db_connect();
  
//  echo("session_id = $session_id<BR>\n");
  if( $session_id != "" ) {                 //  如果是從選課系統連過來的
    $session_data = Read_Session($session_id);
//    list($id, $password, $login_time, $ip, $add_course_count) = $session_data;
    $id			= $session_data{id};
    $password		= $session_data{password};
    $login_time		= $session_data{login_time};
    $ip			= $session_data{ip};
    $add_course_count	= $session_data{add_course_count};
//    print_r($session_data);

    Check_Password($id, $password);
  }else{				    //  不然就是從學籍系統連過來的
    $password = $_POST['password'];
    Check_key($key, $id, $password);		//  基本的安全檢查
    list($name, $dept, $dept_name, $grade, $class, $pwd_sybase) = Read_Personal_Data_From_Sybase($id);
//    echo("[id, personid, name, dept, dept_name, grade, class, pwd_sybase] = [$id, $personid, $name, $dept, $dept_name, $grade, $class, $pwd_sybase]<P>\n");
    Check_Password_Sybase($id, $password, $pwd_sybase);
    $HEAD_DATA = Form_Head_Data($id, $name, $dept_name, $grade, $class);
  }

//  echo("$id, $password, $login_time, $ip, $add_course_count");
  $email = Get_Email($id);


 
?>

<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <TITLE>更改密碼</TITLE>
</head>
<body background=<?PHP echo $BG_PIC; ?>>
<center>
  <?PHP echo $HEAD_DATA; ?>
  <hr>
  <FORM action="Change_Password01.php" method=POST>
    <TABLE border=0 width=75%>
      <TR><TD>
        <UL>
        <LI><FONT size=-1>即日起選課系統將與學籍, 資訊能力測驗等系統密碼整合.
                          您在這裡更改的密碼, 將會同時更新您在這幾個系統上的密碼.
                          (資訊能力測驗系統將有約五分鐘的時間差, 請稍後再登入該系統)
        <LI>若您尚未更改過密碼, 請輸入身分證號(開頭英文應為大寫).
        <LI>為確保將來系統主動通知您重要訊息, 請同時確認 email 信箱!
      </TD></TR>
    </TABLE>
    <P>
    <TABLE border=0>
      <TR><TD>請輸入您原來的密碼:</TD>
          <TD><INPUT type=password name="old_password"></TD></TR>
      <TR><TD>請輸入您的新密碼:</TD>
          <TD><INPUT type=password name="new_password"></TD></TR>
      <TR><TD>請確認新的密碼:</TD>
          <TD><INPUT type=password name="check_password"></TD></TR>
      <TR><TD>請確認您的 email:</TD>
          <TD><INPUT type=text name="email" value=<?PHP echo $email; ?>></TD></TR>
    </TABLE>
    <?PHP 
      if( $session_id == "" ) {                 //  如果是從學籍系統連過來的
        echo("<INPUT type=hidden name=id value=\"$id\">\n");
        echo("<INPUT type=hidden name=key value=\"$key\">\n");
      }
    ?>
    <INPUT type=hidden name="session_id" value="<?PHP echo $session_id; ?>">
    <INPUT type=hidden name=HEAD_DATA value="<?PHP echo $HEAD_DATA; ?>"> 
    <INPUT type="submit" value="確定更改"><p>

  </FORM>
</BODY>
</HTML>
