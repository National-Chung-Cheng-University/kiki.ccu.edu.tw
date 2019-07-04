<?PHP
/////    2014/12/04 強迫使用 SSL 版本 by Nidalap :D~
  require_once "../library/Reference.php";
  
  /////  若使用者不是透過 SSL(https) 連進來，則轉址到 https 版本
  //if( NULL ==  $_SERVER["HTTPS"] ) {
  if( ($_SERVER["SERVER_NAME"] == "kiki.ccu.edu.tw") or ($_SERVER["SERVER_NAME"] == "140.123.30.101") ) {
    header("Location: " . $HOME_URL . "cgi-bin/superuser/index.php");
  }

?>

<HTML>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <TITLE>開排選課系統  管理系統</TITLE>
  <BODY background="../../Graph/bk.jpg">
    <Center>
     <IMG SRC="../../Graph/ma_title.gif" BORDER="0">
     <br><br><br>
     <font size=3 color=red><b>本區系統經過安全管制,非法入侵將被追蹤</b></font>
     <br><br><br>
      <FORM action="su.cgi" method=POST>
        請輸入管理者密碼 : <INPUT type="password" name=password><p>
        <br>
        <INPUT type=submit value="進入管理選單">
      </FORM>
    </Center>
  </BODY>

</HTML>