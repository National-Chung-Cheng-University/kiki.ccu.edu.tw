<?php

$host = "www.ccu.edu.tw";
$host = "140.123.10.202";
//$host = "harmonica.cc.ccu.edu.tw";

$page = "/main_index.php";
$page = "/CCU_Center/Infotest/ShowRecState2.php";
//$page = "/index2.html";

////////////////////////////////////////////////////////////////////////////////////////////////
function Validate($key)
{
  $right_key = "kerokero";
  if( strcmp($key, $right_key) ) {
    echo("Wrong key!");
    exit(0);
  }
}

////////////////////////////////////////////////////////////////////////////////////////////////
function Retrieve_page($host, $page) {
  $fp = fsockopen($host, 80, $errno, $errstr, 30);
  if (!$fp) {
     echo "$errstr ($errno)<br />\n";
  } else {
     $out = "GET " . $page . " HTTP/1.1\r\n";
     $out = $out . "Host: " . $host . "\r\n";
     $out .= "User-Agent: Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.2.1) ";
     $out .= "Connection: Close\r\n\r\n";

     fwrite($fp, $out);
     $header_parsed = 0;
     
     while (!feof($fp)) {
       $content = fgets($fp, 4096);
       // 還要想辦法把 <HTML> 之前的那些 header 清掉, 不顯示
       if( preg_match('/<html>/', $content) ) {
         $header_parsed = 1;
       }
       if( $header_parsed == 1 ) {
         echo $content;
       }
     }
     fclose($fp);
  }
}
?> 

<HTML>
  <BODY>
  <FORM action = "fsockopen.php" method=POST>
    Enter student id: <INPUT name = "id"><BR>
    Enter key password: <INPUT type=password name = "key"><P>
    <INPUT type=SUBMIT>
  </FORM>
  <?PHP
    $page = $page . "?id=" . $id;
    Validate($key);
    
  ?>

  <CENTER>
  <TABLE border=3 width=85%>
    <TR bgcolor=LIGHTYELLOW>
      <TD>Now retrieving: http://<?PHP echo("$host$page"); ?></TD>
    </TR>
    <TR>
      <TD>
        <?PHP Retrieve_page($host, $page);  ?>
      </TD>
    </TR>
  </TABLE>

  </BODY>
</HTML>                                                  