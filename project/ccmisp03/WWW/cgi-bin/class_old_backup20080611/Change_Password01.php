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

  if( $session_id != "" ) {                 //  �p�G�O�q��Ҩt�γs�L�Ӫ�
//    list($id, $password, $login_time, $ip, $add_course_count) =Read_Session($session_id);
    $session_data = Read_Session($session_id);
//    list($id, $password, $login_time, $ip, $add_course_count) = $session_data;         
    $id                 = $session_data{id};
    $password           = $session_data{password};
    $login_time         = $session_data{login_time};
    $ip                 = $session_data{ip};
    $add_course_count   = $session_data{add_course_count};

    Check_Password($id, $password);
  }else{                                    //  ���M�N�O�q���y�t�γs�L�Ӫ�
    // �O�ѤF���w���ˬd
    Check_key($key, $id, $old_password);            //  �򥻪��w���ˬd
//    list($name, $dept, $dept_name, $grade, $class, $pwd_sybase) = Read_Personal_Data_From_Sybase($id);
    list($name, $dept, $dept_name, $grade, $class, $pwd_sybase) = Read_Personal_Data_From_Sybase($id);
    //    echo("[id, personid, name, dept, dept_name, grade, class, pwd_sybase] = [$id, $personid, $name, $dept, $dept_name, $grade, $class, $pwd_sybase]<P>\n
//    echo("$name, $dept, $dept_name, $grade, $class, $pwd_sybase<BR>\n");
  }
  
?>

<HTML>
  <HEAD><TITLE>���K�X���G</TITLE></HEAD>
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
      echo("<P><LI>�K�X��粒��, �Шc�O�z���K�X, ���K�X�P�ɾA�Ω��һP���y�t��.");
      echo("<LI>�N�Өt�έY�����n�T�����i, �i��z�L email �q���z�b");
      echo("<FONT color=RED>$email</FONT> ���H�c.");
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

      echo("<P><LI><FONT color=RED>�K�X��異��!</FONT> �z���K�X�S��������s���\! ");
      Error_Please_Report($error_code);
    }
    $flag = Update_Email($id, $email);
    if( $flag == 0 ) {
      $error_code = "EMAIL_UPDATE_ERROR";
      echo("<P><LI><FONT color=RED>email ��異��!</FONT> �z�� email �S��������s���\! ");
      Error_Please_Report($error_code);      
    }

    if($session_id != "" ) {                 //  �p�G�O�q��Ҩt�γs�L�Ӫ�
      echo("<FORM action = \"Main.cgi\" method=POST>
          <INPUT type=hidden name=session_id value=$session_id>
          <INPUT type=submit value=\"�^��ҥD���\">
        </FORM>");                
    }else{				     //  �p�G�O�q���y�t�γs�L�Ӫ�
      echo("<INPUT type=button value=\"��������\" onClick=\"window.close()\">");
    }
    
  ?>

</HTML>

<?PHP

  function Check_New_Password($old_password, $new_password, $check_password)
  {
    global $id, $session_id, $pwd_sybase;
    $error_count = 0;
//    echo("$old_password, $new_password, $check_password<BR>\n");

    if( $session_id != "" ) {                 //  �p�G�O�q��Ҩt�γs�L�Ӫ�
      $crypt_salt = Read_Crypt_Salt($id);                                                    
      $old_password = my_Crypt($old_password, $crypt_salt);
//      echo("salt, oldpass = [$crypt_salt, $old_password]<BR>\n");
      Check_Password($id, $old_password);
    }else{                                    //  ���M�N�O�q���y�t�γs�L�Ӫ�
//      echo("from ���y, $id, $old_password, $pwd_sybase<BR>\n");
      Check_Password_Sybase($id, $old_password, $pwd_sybase);
    }
            
    $illegal_chars = array ('\\', '\/', '\"', '\'', '\|', '\`', ' ');
    foreach( $illegal_chars as $char ) {
      $char2 = "/" . $char . "/";
//      $char = substr($char, 1, 1);
      if( preg_match($char2,$new_password) ) {
        echo("�K�X���ФŨϥ� <FONT color=RED>$char</FONT> �Ÿ�!<BR>");
        $error_count++;
      }
    }

    if( $new_password != $check_password ) {
      echo("�z��J���s�K�X�νT�{�K�X���ŦX!<BR>");
      $error_count++;
    }

    if( strlen($new_password) < 5 ) {
      echo("�s�K�X�ФŤ֩�5�Ӧr��!<BR>");
      $error_count++;
    }

    if( strlen($new_password) > 10 ) {
      echo("�s�K�X�ФŦh��10�Ӧr��!<BR>");
      $error_count++;
    } 
    
    if( $new_password == $id ) {
      echo("�ФťH�Ǹ����K�X!<BR>");
      $error_count++;
    }

    //  �t�~�٭n�ˬd�H������, �ͤ骺�K�X
    
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
        echo("�п�J���T�� email �H�c!");
        $error_count++;
      }
    }
    
    if( !preg_match('/@/', $email) ) {
      echo("�п�J���㪺 email �H�c!");
      $error_count++;
    }
    
    if( $error_count != 0 ) {
      exit;
    }else{
      return;
    }
                            
  }

?>