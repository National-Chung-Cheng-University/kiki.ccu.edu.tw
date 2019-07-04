<?PHP
  include "../php_lib/Reference.php";
  include "../php_lib/Common_Utility.php";
  include "../php_lib/Session.php";
  include "../php_lib/Password.php";
  include "../php_lib/Sybase.php";

  global $BG_PIC;
  $session_id   = $_POST['session_id'];
  if(isset($_POST['id']))  { $id                = $_POST['id'];  }
  if(isset($_POST['key'])) { $key               = $_POST['key']; }
    
  db_connect();

  if( $session_id != "" ) {                 //  如果是從選課系統連過來的
//    list($id, $password, $login_time, $ip, $add_course_count) =Read_Session($session_id);
    $session_data = Read_Session($session_id);
//    list($id, $password, $login_time, $ip, $add_course_count) = $session_data;         
    $id                 = $session_data{id};
    $password           = $session_data{password};
    $login_time         = $session_data{login_time};
    $ip                 = $session_data{ip};
    $add_course_count   = $session_data{add_course_count};

    Check_Password($id, $password);
  }else{                                    //  不然就是從學籍系統連過來的
    // 別忘了做安全檢查
    Check_key($key, $id, $old_password);            //  基本的安全檢查
//    list($name, $dept, $dept_name, $grade, $class, $pwd_sybase) = Read_Personal_Data_From_Sybase($id);
    list($name, $dept, $dept_name, $grade, $class, $pwd_sybase) = Read_Personal_Data_From_Sybase($id);
    //    echo("[id, personid, name, dept, dept_name, grade, class, pwd_sybase] = [$id, $personid, $name, $dept, $dept_name, $grade, $class, $pwd_sybase]<P>\n
//    echo("$name, $dept, $dept_name, $grade, $class, $pwd_sybase<BR>\n");
  }
  
?>

<HTML>
  <HEAD><TITLE>更改密碼結果</TITLE></HEAD>
  <BODY background="http://kiki.ccu.edu.tw/~ccmisp06/Graph/ccu-sbg.jpg">
    <CENTER><?PHP echo $HEAD_DATA; ?>
    <HR>

  <?PHP
//    Check_New_Password($old_password, $new_password, $check_password);
    Check_Email($email);
//    echo("$name, $dept, $dept_name, $grade, $class, $pwd_sybase<BR>\n");
    Check_New_Password($old_password, $new_password, $check_password);

    list($flag,$flag1,$flag2, $crypted_password) = Change_Password($id, $new_password);
    if($flag > 0) {
      echo("<P><LI>密碼更改完成, 請牢記您的密碼, 此密碼同時適用於選課與學籍系統.");
      echo("<LI>將來系統若有重要訊息公告, 可能透過 email 通知您在");
      echo("<FONT color=RED>$email</FONT> 的信箱.");
      echo("<P>");
      $crypted_password = substr($crypted_password, 2, 20);
      Write_Session($session_id, $id, $crypted_password, $add_course_count);
    }else{
      if( ($flag1 == 0) and ($flag2 == 0) ) {
        $error_code = "PASS_ERROR_BOTH";
      }else if( $flag1 == 0 ) {
        $error_code = "PASS_ERROR_DB";
      }else{
        $error_code = "PASS_ERROR_KIKI";
      }

      echo("<P><LI><FONT color=RED>密碼更改失敗!</FONT> 您的密碼沒有完全更新成功! ");
      Error_Please_Report($error_code);
    }
    $flag = Update_Email($id, $email);
    if( $flag == 0 ) {
      $error_code = "EMAIL_UPDATE_ERROR";
      echo("<P><LI><FONT color=RED>email 更改失敗!</FONT> 您的 email 沒有完全更新成功! ");
      Error_Please_Report($error_code);      
    }

    if($session_id != "" ) {                 //  如果是從選課系統連過來的
      echo("<FORM action = \"Main.cgi\" method=POST>
          <INPUT type=hidden name=session_id value=$session_id>
          <INPUT type=submit value=\"回選課主選單\">
        </FORM>");                
    }else{				     //  如果是從學籍系統連過來的
      echo("<INPUT type=button value=\"關閉視窗\" onClick=\"window.close()\">");
    }
    
  ?>

</HTML>

<?PHP

  function Check_New_Password($old_password, $new_password, $check_password)
  {
    global $id, $session_id, $pwd_sybase;
    $error_count = 0;
//    echo("$old_password, $new_password, $check_password<BR>\n");

    if( $session_id != "" ) {                 //  如果是從選課系統連過來的
      $crypt_salt = Read_Crypt_Salt($id);                                                    
      $old_password = my_Crypt($old_password, $crypt_salt);
//      echo("salt, oldpass = [$crypt_salt, $old_password]<BR>\n");
      Check_Password($id, $old_password);
    }else{                                    //  不然就是從學籍系統連過來的
//      echo("from 學籍, $id, $old_password, $pwd_sybase<BR>\n");
      Check_Password_Sybase($id, $old_password, $pwd_sybase);
    }
            
    $illegal_chars = array ('\\', '\/', '\"', '\'', '\|', '\`', ' ');
    foreach( $illegal_chars as $char ) {
      $char2 = "/" . $char . "/";
//      $char = substr($char, 1, 1);
      if( preg_match($char2,$new_password) ) {
        echo("密碼中請勿使用 <FONT color=RED>$char</FONT> 符號!<BR>");
        $error_count++;
      }
    }

    if( $new_password != $check_password ) {
      echo("您輸入的新密碼及確認密碼不符合!<BR>");
      $error_count++;
    }

    if( strlen($new_password) < 5 ) {
      echo("新密碼請勿少於5個字元!<BR>");
      $error_count++;
    }

    if( strlen($new_password) > 10 ) {
      echo("新密碼請勿多於10個字元!<BR>");
      $error_count++;
    } 
    
    if( $new_password == $id ) {
      echo("請勿以學號為密碼!<BR>");
      $error_count++;
    }

    //  另外還要檢查以身分證, 生日的密碼
    
    if( $error_count != 0 ) {
      exit;
    }else{
      return;
    }
  }
  /////////////////////////////////////////////////////////////////////////////
  function Check_Email($email)
  {
    $error_count = 0;

    $illegal_chars = array ('\\', '\/', '\"', '\'', '\|', '\`');
//    $illegal_chars = array ('X', ';');   
    
    foreach( $illegal_chars as $char ) {
      $char = "/" . $char . "/";
      if( preg_match($char,$email) ) {
//        echo("illegal --->  $char<BR>\n");
        echo("請輸入正確的 email 信箱!");
        $error_count++;
      }
    }
    
    if( !preg_match('/@/', $email) ) {
      echo("請輸入完整的 email 信箱!");
      $error_count++;
    }
    
    if( $error_count != 0 ) {
      exit;
    }else{
      return;
    }
                            
  }

?>