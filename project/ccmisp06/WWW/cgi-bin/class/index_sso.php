<?PHP
  //////////////////////////////////////////////////////////////////////////////////////////
  /////  index_sso.php
  /////  從 SSO 登入進來的頁面
  /////  Updates:
  /////    2012/06/28  因應 SSO 製作此頁面，判斷登入資料後轉址至選課系統內部網頁. Nidalap :D~

  session_start();
  if( !( empty($_POST) AND isset($_SESSION['verifySso']) AND trim($_SESSION['verifySso'])=='Y' ) ) {
    header("index.php");    
  }else{
    die("非請勿進！");
  }
