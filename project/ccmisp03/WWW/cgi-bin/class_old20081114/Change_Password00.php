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
  if( $session_id != "" ) {                 //  �p�G�O�q��Ҩt�γs�L�Ӫ�
    $session_data = Read_Session($session_id);
//    list($id, $password, $login_time, $ip, $add_course_count) = $session_data;
    $id			= $session_data{id};
    $password		= $session_data{password};
    $login_time		= $session_data{login_time};
    $ip			= $session_data{ip};
    $add_course_count	= $session_data{add_course_count};
//    print_r($session_data);

    Check_Password($id, $password);
  }else{				    //  ���M�N�O�q���y�t�γs�L�Ӫ�
    $password = $_POST['password'];
    Check_key($key, $id, $password);		//  �򥻪��w���ˬd
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
    <TITLE>���K�X</TITLE>
</head>
<body background=<?PHP echo $BG_PIC; ?>>
<center>
  <?PHP echo $HEAD_DATA; ?>
  <hr>
  <FORM action="Change_Password01.php" method=POST>
    <TABLE border=0 width=75%>
      <TR><TD>
        <UL>
        <LI><FONT size=-1>�Y��_��Ҩt�αN�P���y, ��T��O���絥�t�αK�X��X.
                          �z�b�o�̧�諸�K�X, �N�|�P�ɧ�s�z�b�o�X�Өt�ΤW���K�X.
                          (��T��O����t�αN�������������ɶ��t, �еy��A�n�J�Өt��)
        <LI>�Y�z�|�����L�K�X, �п�J�����Ҹ�(�}�Y�^�������j�g).
        <LI>���T�O�N�Өt�ΥD�ʳq���z���n�T��, �ЦP�ɽT�{ email �H�c!
      </TD></TR>
    </TABLE>
    <P>
    <TABLE border=0>
      <TR><TD>�п�J�z��Ӫ��K�X:</TD>
          <TD><INPUT type=password name="old_password"></TD></TR>
      <TR><TD>�п�J�z���s�K�X:</TD>
          <TD><INPUT type=password name="new_password"></TD></TR>
      <TR><TD>�нT�{�s���K�X:</TD>
          <TD><INPUT type=password name="check_password"></TD></TR>
      <TR><TD>�нT�{�z�� email:</TD>
          <TD><INPUT type=text name="email" value=<?PHP echo $email; ?>></TD></TR>
    </TABLE>
    <?PHP 
      if( $session_id == "" ) {                 //  �p�G�O�q���y�t�γs�L�Ӫ�
        echo("<INPUT type=hidden name=id value=\"$id\">\n");
        echo("<INPUT type=hidden name=key value=\"$key\">\n");
      }
    ?>
    <INPUT type=hidden name="session_id" value="<?PHP echo $session_id; ?>">
    <INPUT type=hidden name=HEAD_DATA value="<?PHP echo $HEAD_DATA; ?>"> 
    <INPUT type="submit" value="�T�w���"><p>

  </FORM>
</BODY>
</HTML>
