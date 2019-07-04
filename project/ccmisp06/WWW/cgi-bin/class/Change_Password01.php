<?PHP
  ///////////////////////////////////////////////////////////////////////////////////////////
  /////  Change_Password01.php
  /////  檢查輸入密碼等資料，實際執行更改密碼功能
  /////  Updates:
  /////    20??/??/?? Created by Nidalap :D~
  /////    2011/03/30 修改程式不再依賴 register_globals.  Nidalap :D~
  /////    2012/05/29 密碼合法字元檢查改為白名單.  Nidalap :D~
  /////    2012/09/04 除了原有學籍外，也可由 SSO 的改密碼程式呼叫此程式。  Nidalap :D~
  /////    2012/09/06 若是從選課系統更改密碼，呼叫 Change_SSO_Password() 以同步更新 ldap 密碼。
  /////    2012/09/12 若是 ldap 密碼更新失敗，將密碼還原為未修改的值。  Nidalap :D~
  /////    2012/10/30 改採 PDO 連線資料庫。  Nidalap :D~ 
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
  
  $txt = Init_Text_Values();								///  初始化顯示文字（中文或英文）

  global $BG_PIC;
  ////////////////   讀取上一頁傳入的變數
  $session_id   = isset($_POST["session_id"]) ? $_POST["session_id"] : "";
  $id		= isset($_POST["id"]) ? $_POST["id"] : "";
  $key		= isset($_POST["key"]) ? $_POST["key"] : "";
  $email	= isset($_POST["email"]) ? $_POST["email"] : "";
  $old_password = isset($_POST["old_password"]) ? $_POST["old_password"] : "";
  $new_password	= isset($_POST["new_password"]) ? $_POST["new_password"] : "";
  $check_password = isset($_POST["check_password"]) ? $_POST["check_password"] : "";
    
//  db_connect();
  $DBH = PDO_connect($DATABASE_NAME);

  if( $session_id != "" ) {                 //  如果是從選課系統連過來的
    $from_kiki = 1;				///  從選課系統連過來的
    $session_data = Read_Session($session_id);
    $id                 = $session_data{"id"};
    $password           = $session_data{"password"};
    $login_time         = $session_data{"login_time"};
    $ip                 = $session_data{"ip"};
    $add_course_count   = $session_data{"add_course_count"};
    $student = Read_Student($id);

    Check_Password($id, $password, "", "");
    $stu = Read_Student($id);
	$dept_data = Read_Dept($stu["dept"]);
    $personid = $stu{"personal_id"};
//    $HEAD_DATA = Form_Head_Data($stu["id"], $stu["name"], $dept_data["cname2"], $stu["grade"], $stu["class"]);
    if( $IS_ENGLISH ) {
      $HEAD_DATA = Form_Head_Data($stu["id"], $stu["ename"], $dept_data["ename"], $stu["grade"], $stu["class"]);
    }else{
      $HEAD_DATA = Form_Head_Data($stu["id"], $stu["name"], $dept_data["cname2"], $stu["grade"], $stu["class"]);
    }
  }else{                                    //  不然就是從其他系統連過來的
    $referer_ip = $_SERVER["HTTP_REFERER"];
    $change00_url = preg_replace("/_new/", "", $CLASS_URL) . "Change_Password00.php";

    //echo $referer_ip . "<->" . $change00_url ;
    if( $referer_ip == $change00_url ) {
      $from_kiki = 1;			///  是從選課系統連過來的
	  if( $key != "" )
	    $from_kiki = 0;			///  從學籍系統連過來的(即使學籍，也是透過 Change_Password00.php)
	}else{
      $from_kiki = 0;			///  否則，應該是從 SSO 連過來的
	}
    Check_Key($key, $id, $old_password);		//  安全檢查: 檢查 $key 是否正確
    Check_Source_URL();					//  安全檢查: 檢查來源頁面 URL
    list($personid, $name, $dept, $dept_name, $grade, $class, $pwd_db) = Read_Personal_Data_From_Database($id);
    Check_Password_Database($id, $old_password, $pwd_db);
    //$HEAD_DATA = Form_Head_Data($id, $name, $dept_name, $grade, $class);
	if( $IS_ENGLISH ) {
      $HEAD_DATA = Form_Head_Data($id, $name, $dept_name, $grade, $class);
    }else{
      $HEAD_DATA = Form_Head_Data($id, $name, $dept_name, $grade, $class);
    }
  }
  
?>

<HTML>
  <HEAD>
    <?PHP echo $EXPIRE_META_TAG ?>
    <TITLE><?PHP echo $txt['html_title'] ?></TITLE>
	<?PHP if( $IS_MOBILE >= 1 ) 	echo $MOBILE_META_TAG  ?>
  </HEAD>
  <BODY background="http://kiki.ccu.edu.tw/~ccmisp06/Graph/ccu-sbg.jpg">
    <CENTER>
	<?PHP 
	  if( $IS_MOBILE >= 1 ) 	echo Create_jQuery_Mobile_Title_Tag();
	  echo $HEAD_DATA; 
	?>
    <HR>

  <?PHP
    if( $from_kiki )  Check_Email($email);
    Check_New_Password($old_password, $new_password, $check_password, $id);

    list($flag,$flag1,$flag2, $crypted_password) = Change_Password($id, $new_password);
    if($flag > 0) {
      echo "<P><LI>" . $txt['result1'];
      if( $from_kiki ) {
        echo "<LI>" . $txt['result2'];
        echo "<FONT color=RED>$email</FONT> " . $txt['result3'];
      }else{
        echo "(SUCCEED)";
      }
      echo("<P>");
      $crypted_password = substr($crypted_password, 2, 24);
      Write_Session($session_id, $id, $crypted_password, $add_course_count);
    }else{
      if( ($flag1 == 0) and ($flag2 == 0) ) {
        $error_code = "PASS_ERROR_BOTH";
      }else if( $flag1 == 0 ) {
        $error_code = "PASS_ERROR_DB";
      }else{
        $error_code = "PASS_ERROR_KIKI";
      }

      echo "<P><LI>" . $txt['fail1'];
      Error_Please_Report($error_code);
    }
    
    if( $from_kiki ) {			//  如果是從選課系統連過來的
      $flag = Update_Email($id, $email);	//  更新 email
      if( $flag == 0 ) {
        $error_code = "EMAIL_UPDATE_ERROR";
        echo "<P><LI>" . $txt['fail2'];
        Error_Please_Report($error_code);      
      }

      if( $id != $TEST_STU_ID ) {	///  如果是測試學生帳號(999999999)，不更新 SSO 密碼
        $sso_result = Change_SSO_Password($old_password, $new_password, $check_password,$id);
//        $sso_result = "SSO chpwd fail from Nidalap!!";
        if( $sso_result != 1 ) {
          $error_code = "PASS_ERROR_SSO: " . $sso_result;
          echo "<P><LI>" . $txt['fail3'];
          Change_Password($id, $old_password, "revert");  ///  還原 kiki 與 資料庫 密碼
          Error_Please_Report($error_code);
        }
      }
    }else{				     //  如果是從其他系統連過來的
      echo "<INPUT type=button value='" . $txt["close_win"] . "' onClick=\"window.close()\">";
    }
	
    if( $IS_MOBILE >= 1 ) 	echo Create_jQuery_Mobile_Footer_Tag();
  ?>

</HTML>

<?PHP

///////////////////////////////////////////////////////////////////////////////////////////////////
  function Check_New_Password($old_password, $new_password, $check_password,$id)
  {
    global $session_id, $pwd_db,$MIN_PASSWORD_LENGTH,$MAX_PASSWORD_LENGTH;
    global $personid, $txt;
    global $USE_MD5_PASSWORD;
    $error_count = 0;
//    echo("Checking passwords: [old,new,check] = [$old_password, $new_password, $check_password]<BR>\n");

    if( $session_id != "" ) {                 //  如果是從選課系統連過來的
      if( $USE_MD5_PASSWORD == 1 ) {
        $old_password = MD5($old_password);
      }else{
        $crypt_salt = Read_Crypt_Salt($id);                                                    
        $old_password = my_Crypt($old_password, $crypt_salt);
      }
      Check_Password($id, $old_password, "", "");
    }else{                                    //  不然就是從學籍系統連過來的
//      echo("from 學籍, $id, $old_password, $pwd_db<BR>\n");
      Check_Password_Database($id, $old_password, $pwd_db);
    }
            
//    $illegal_chars = array ('\\\\', '\/', '\"', '\'', '\|', '\`', ' ');
//    $illegal_chars = array ('\\', ' '); //  '\"', '\'', '\|', '\`', ' ');
//    $legal_chars = array('!','@','/$','^','_','-');
    
    if( !Check_Password_Legal_Chars($new_password) ) {
//    foreach( $illegal_chars as $char ) {
//      $char2 = "/" . $char . "/";
//      $char = substr($char, 1, 1);
//      echo "Validating character $char2<BR>\n";
      echo $txt['illegal_pass1'] . "<BR>\n";
      $error_count++;
    }

    if( $new_password != $check_password ) {
      echo $txt['illegal_pass2'] . "<BR>\n";
      $error_count++;
    }

    if( strlen($new_password) < $MIN_PASSWORD_LENGTH ) {
      echo $txt['illegal_pass1'] . "<BR>\n";
      $error_count++;
    }

    ###  crypt 最多支援 8 bytes, 學籍系統欄位是 10 bytes	Nidalap 2009/03/23
    if( strlen($new_password) > $MAX_PASSWORD_LENGTH ) {
      echo $txt['illegal_pass1'] . "<BR>\n";
      $error_count++;
    } 
    
    if( $new_password == $id ) {
      echo $txt['illegal_pass3'] . "<BR>\n";
      $error_count++;
    }
//    global $student;
    if( $new_password == $personid ) {		///  Added 2010/09/09 Nidalap :D~
      echo $txt['illegal_pass4'] . "<BR>\n";
      $error_count++;
    }

    if( $error_count != 0 ) {
      exit;
    }else{
      return;
    }
  }
  
  /////////////////////////////////////////////////////////////////////////////
  function Check_Password_Legal_Chars($new_password)
  {
    $legal_chars = array('!','@','$','^','&','_','-');
    $chars = str_split($new_password);
    foreach( $chars as $char ) {
      $ascii = ord($char);
      if     ( ($ascii >=48) and ($ascii <=57) )	continue;  //  0~9
      else if( ($ascii >=65) and ($ascii <=90) )	continue;  //  A~Z
      else if( ($ascii >=97) and ($ascii <=122) )	continue;  //  a~z
      else if( in_array($char, $legal_chars) )		continue;  //  檢查其他字元白名單
      else 						return(0);
    }
    return 1;
  }

  
  /////////////////////////////////////////////////////////////////////////////
  function Check_Email($email)
  {
    global $txt;
	$error_count = 0;
	
    $illegal_chars = array ('\\\\', '\/', '\"', '\'', '\|', '\`');
//    $illegal_chars = array ('X', ';');   
    
    foreach( $illegal_chars as $char ) {
      $char = "/" . $char . "/";
      if( preg_match($char,$email) ) {
//        echo("illegal --->  $char<BR>\n");
        echo $txt['illegal_email'] . "<BR>\n";
        $error_count++;
      }
    }
    
/*    if( !preg_match('/@/', $email) ) {
      echo("請輸入完整的 email 信箱!");
      $error_count++;
    }
*/
    
    ///  從 regexlib.com 抄來的，允許以 , 或是 ; 分隔的多個信箱 2010/04/21 Nidalap :D~
    if( !preg_match("/\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*([,;]\s*\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*)*/", $email) ) {
      echo $txt['illegal_email'] . "<BR>\n";
      $error_count++;
    }
    
    if( $error_count != 0 ) {
      exit;
    }else{
      return;
    }
                            
  }
  //////////////////////////////////////////////////////////////////////////////
  function Check_Source_URL()
  {
    global $LOG_IGNORE_IP, $CLASS_URL;
//    $ip = getenv("HTTP_X_FORWARDED_FOR");
//    if( $ip == "" )   { $ip = getenv("REMOTE_ADDR"); }
//    $ip = preg_replace("/, $LOG_IGNORE_IP/", "", $ip);
    $ip = $_SERVER["HTTP_REFERER"];
//    $ip = preg_replace("/^http:\/\//", "");
    
	//$CLASS_URL = "140.123.30.101/~ccmisp12/";
	
	$class_url = preg_replace("/_new/", "", $CLASS_URL);
    
	
    $allowed_source = array(
      $CLASS_URL . "Change_Password00.php",				// 選課系統自己的上一頁
      $class_url . "Change_Password00.php",				
      "http://140.123.26.151/academic01/change_pwd.php",		// 學籍測試
      "http://miswww1.cc.ccu.edu.tw/academic/change_pwd.php",		// 學籍正式
//      "http://osa.ccu.edu.tw/~porihuang/pw.php",
      "http://osa.ccu.edu.tw/~porihuang/ajax/apply_acc_ajax.php",	// SSO 測試平台
      "http://portal.ccu.edu.tw/ajax/apply_acc_ajax.php"		// SSO 正式平台
//      "140.123.4.10"
    );
    
    $allowed = 0;
    foreach($allowed_source as $url) {
      if( $ip == $url ) {
        $allowed = 1;
      }
    }
    preg_match("", "");
    
    if( $allowed )  return 1;
    else{
      die("Source NOT allowed for URL $ip!");
    }    
  }
  ///////////////////////////////////////////////////////////////////////////////
  function Change_SSO_Password($old_password, $new_password, $check_password,$id)
  {
    global $USE_TEST_DATABASE;
    
    $key = Generate_Key($id, $old_password);
    $aes = new Crypt_SSOpw();
    $id = $aes->encrypt($id);
    $old_password = $aes->encrypt($old_password);
    $new_password = $aes->encrypt($new_password);
    $check_password = $aes->encrypt($check_password);
    $key = $aes->encrypt($key);

    if( $USE_TEST_DATABASE == 1 ) {
//      echo "use test database...<BR>\n";
      $toURL = 'http://osa.ccu.edu.tw/~porihuang/ldapPWchange.php';	// SSO測試平台
    }else{
      $toURL = 'http://portal.ccu.edu.tw/ldapPWchange.php';		// SSO 正式
    }
    
    $post = array(
        'id' => $id,
        'old_password' => $old_password,
        'new_password' => $new_password,
        'check_password' => $check_password,
        'key' => $key
    );
    
//    print_r($post);
    
    $ch = curl_init();
    $options = array(
        CURLOPT_URL=>$toURL,
        CURLOPT_POST=>true,
        CURLOPT_RETURNTRANSFER=>true,
        CURLOPT_REFERER=>"http://" . $_SERVER['SERVER_NAME'] . preg_replace("/_new/", "", $_SERVER['PHP_SELF']),
        CURLOPT_POSTFIELDS=>http_build_query($post)
    );
    curl_setopt_array($ch, $options);
    for( $i=0; $i<5; $i++ ) {
      $result = curl_exec($ch);
      curl_close($ch);
      //判斷ldap端修改密碼成功或失敗
      if(!(strpos($result, 'SUCCEED') === FALSE)) {
        echo "<FONT COLOR='#FFF'>($i)</FONT>";
        return(1);				/// 修改成功
      }
    }
    return($result);				/// 連續三次修改失敗
  }
  //////////////////////////////////////////////////////////////////////////
  class Crypt_SSOpw {
    private $cipher     = 'rijndael-128';
    private $mode       = 'cbc';
    private $key        = '#sSoPW14!405_';
    private $iv         = 'Spw#aTo#ken84';
    private $pkey       = 'SsO_8Ccu135_';
    private $piv        = '#lDapPa3s!s';

    function __construct() {
                $td     = mcrypt_module_open($this->cipher, '', $this->mode, '');
                $key_size = mcrypt_enc_get_key_size($td);
                $iv_size = mcrypt_enc_get_iv_size($td);
                mcrypt_module_close($td);
        $this->iv = substr(md5($this->piv),0,$iv_size);
        $this->key = substr(md5($this->pkey),0,$key_size);
    }

    function encrypt($str) {
                $td     = mcrypt_module_open($this->cipher, '', $this->mode, '');
        mcrypt_generic_init($td, $this->key, $this->iv);
        $cyper_text = mcrypt_generic($td, $str);
        $r = bin2hex($cyper_text);
        mcrypt_generic_deinit($td);
                mcrypt_module_close($td);
        return $r;
    }

    function decrypt($str) {
                $td     = mcrypt_module_open($this->cipher, '', $this->mode, '');
        mcrypt_generic_init($td, $this->key, $this->iv);
        $decrypted_text = mdecrypt_generic($td, $this->hex2bin($str));
        $r = $decrypted_text;
        mcrypt_generic_deinit($td);
                mcrypt_module_close($td);
        return $r;
    }
    private function hex2bin($hexdata) {
        $bindata = '';
        for($i=0; $i<strlen($hexdata); $i+=2) {
            $bindata .= chr(hexdec(substr($hexdata, $i, 2)));
        }
        return $bindata;
    }
  }

  //////////////////////////////////////////////////////////////////////////////////////////////
  /////  因應英文版本，將所有要顯示的文字在此整理，依照 $IS_ENGLISH 自動判別  2013/08/08
  function Init_Text_Values()
  {
    global $IS_ENGLISH, $MIN_PASSWORD_LENGTH, $MAX_PASSWORD_LENGTH;
	//global $session_id, $student, $ban_res_time, $password_last_time;
	//global $year, $term;
	
	$sname = $student['name'];
	
	$txtall = array(
	  'html_title'	=> array('c'=>'更改密碼結果', 'e'=>'Change Password'), 
	  'result1'		=> array('c'=>'密碼更改完成, 請牢記您的密碼, 此密碼同時適用於選課與學籍系統.',
						     'e'=>'Your password has been updated.'),
	  'result2'		=> array('c'=>'將來系統若有重要訊息公告, 可能透過 email 通知您在', 
							 'e'=>'將來系統若有重要訊息公告, 可能透過 email 通知您在'),							 
	  'result3'		=> array('c'=>'的信箱', 
							 'e'=>'的信箱'),
	  'fail1'		=> array('c'=>'<FONT color=RED>密碼更改失敗!</FONT> 您的密碼沒有完全更新成功!', 
							 'e'=>'<FONT color=RED>Password update failed!</FONT> Please try again.'),
	  'fail2'		=> array('c'=>'<FONT color=RED>email 更改失敗!</FONT> 您的 email 沒有更新成功!', 
							 'e'=>'<FONT color=RED>Password update failed!</FONT> Please try again.'),
	  'fail3'		=> array('c'=>'<FONT color=RED>密碼更改失敗!</FONT> 您的密碼沒有完全更新成功!', 
							 'e'=>'<FONT color=RED>Password update failed!</FONT> Please try again.'),
	  'close_win'	=> array('c'=>'關閉視窗', 
							 'e'=>'Close Window'),

	  'illegal_pass1'=> array('c'=>'密碼規範：長度介於 ' . $MIN_PASSWORD_LENGTH . ' 到 ' . $MAX_PASSWORD_LENGTH . ' 之間， 
								請使用大小寫英文、數字、及以下特殊字元組合 「! @ $ ^ _ -」', 
							 'e'=>'Password Rule: ' . $MIN_PASSWORD_LENGTH . ' to ' . $MAX_PASSWORD_LENGTH . ' digits, mixing capital and 
								uncapitalized letters, number and special characters (!@$^_-).'),
	  'illegal_pass2'=> array('c'=>'您輸入的新密碼及確認密碼不符合', 
							 'e'=>'您輸入的新密碼及確認密碼不符合'),
	  'illegal_pass3'=> array('c'=>'請勿以學號為密碼！', 
							 'e'=>'請勿以學號為密碼！'),
	  'illegal_pass4'=> array('c'=>'請勿以身份證號為密碼！', 
							 'e'=>'請勿以身份證號為密碼！'),
	  'illegal_email'=> array('c'=>'請輸入正確的 email 信箱!', 
							 'e'=>'Please enter a correct e-mail address!'),

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