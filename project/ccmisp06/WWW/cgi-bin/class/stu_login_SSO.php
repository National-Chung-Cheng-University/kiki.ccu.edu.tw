<?PHP
  ////////////////////////////////////////////////////////////////////////////////
  /////  stu_login_SSO.php
  /////  處理學生從 SSO 單一簽入系統登入資料
  /////  此程式驗證 SSO 所建立的 session 變數，然後從資料庫抓取學生資料，
  /////  建立與 perl 通用的 session 自訂資料，將網頁導向到選課系統首頁。
  /////  選課系統首頁也作過更改，可讀取從此頁傳過去的 session_id 資料。
  /////  Updates:
  /////    2012/08/22 Created by Nidalap :D~
  /////    2012/11/06 改採 PDO 連資料庫。 Nidalap :D~

  require_once("../library/Reference.php");
//  session_save_path("/NFS/session");
  session_start();  
  if( isset($_SESSION['verifySso']) and $_SESSION['verifySso']=='Y' ) {
    require_once("../library/Reference.php");
    require_once $LIBRARY_PATH . "Database.php";
    require_once $LIBRARY_PATH . "Student.php";
    require_once $LIBRARY_PATH . "Session.php";
    require_once $LIBRARY_PATH . "Password.php";
    require_once $LIBRARY_PATH . "Common_Utility.php";
    
    $DBH = PDO_connect($DATABASE_NAME);
    
    $id = $_SESSION["sso_personid"];
    list($personid, $name, $dept, $dept_name, $grade, $class, $password) = Read_Personal_Data_From_Database($id);
    $_SESSION["id"]	= $id;
    $salt = Read_Crypt_Salt($id);		//  讀取自訂 session 資料的 crypt salt
    $password = my_Crypt($password, $salt);	//  使用 salt 將學生密碼做 DES 編碼

    $session_id = Create_Session_ID($id, $password);
    Write_Session($session_id, $id, $password, 0);	//  寫入與 perl 通用的自訂 session 資料檔
    Student_Log("Login_SSO", $id);

    $phpsessid = session_id();
         
    $home_url = $CLASS_URL . "index.php?session_id=" . $session_id; // . "&phpsessid=" . $phpsessid;
	
	$debug = 0;
	if( $debug == 1 ) {
	  print_r($DBH->errorInfo());
	  echo "<BR>\n phpsessid = $phpsessid<BR>\n";
	  echo "[session_id, id, password] = [$session_id, $id, $password]<BR>\n";
	}else{
      header("Location: $home_url");
	}
  }else{
    echo "Login fail!";
    die();
  }  
?>