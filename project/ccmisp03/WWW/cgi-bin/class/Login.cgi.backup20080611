#!/usr/local/bin/perl
#print "Content-type: text/html","\n\n";

require "../library/Reference.pm";
require $LIBRARY_PATH . "System_Settings.pm";
require $LIBRARY_PATH . "Dept.pm";

#####  Code added on 2005/02/16, Nidalap :D~
use CGI qw(:standard);
$query = new CGI;
$cookie1 = $query->cookie(-name => 'id', -value=>'', -expires=>'+1h');
$cookie2 = $query->cookie(-name => 'password', -value=>'', -expires=>'+1h');
#$cookie3 = $query->cookie(-name => 'crypt', -value=>'0', -expires=>'+1h');
print $query->header(-cookie=>[$cookie1, $cookie2]);
################################################


$text = Read_Board();
%system_flags = Read_System_Settings();
####################################################################################
sub Read_Board()
{
  my($text, $board_file, @temp);
  $board_file = $REFERENCE_PATH."Login_Message.txt";
  open(BOARD, $board_file) or
      Fatal_Error("Cannot read file $board_file in Modify_login_Message.cgi!");
  @temp = <BOARD>;
  close(BOARD);
  $text = join("", @temp);
  $text =~ s/\n/<br>\n/g;
  return $text;               
}
####################################################################################

if( $system_flags{redirect_to_query} == 1 ) {
  $redirect = "<CENTER>" . $YEAR . " 學年度第 " .
              $TERM ."學期開課中, 欲查詢本學期選課資料, 請點選<BR>" .
              "<A href=\"http://kiki.ccu.edu.tw/query_class.html\">查詢系統</A>" .
              "</CENTER>";
}

if( $IS_GRA == 1 ) {
  $lost_password_url = "http://mis.cc.ccu.edu.tw/academic/gra/lost_passwd.htm";
}else{
  $lost_password_url = "http://mis.cc.ccu.edu.tw/academic/lost_passwd.htm";
}

print qq(

<html>

<script language="JavaScript">
//  這一段是從學籍系統的登入網頁抄來的 Added 2005/09/13 Nidalap :D~
  function f_action(field) {
//	var user=document.fm_login.uid.value;
//	var passwd=document.fm_login.password.value;

	popup_ask_passwd=window.open("$lost_password_url", "遺失密碼", "width =600, height =400, scrollbars=yes");
	popup_ask_passwd.name = "lost_passwd";
	return true;
  }
</SCRIPT>

<head>
  <meta http-equiv="Content-Type" content="text/html; charset=big5">
  <title>國立中正大學$SUB_SYSTEM_NAME選課系統--$YEAR學年度第$TERM學期</title>
</head>
<body background="$GRAPH_URL/ccu-sbg.jpg">
<center>
    <!img src="$GRAPH_URL/select.jpg"> 
    <H1><FONT face="標楷體">中正大學<FONT color=RED>$SUB_SYSTEM_NAME</FONT>選課系統</FONT>
        <IMG src="$GRAPH_URL/mouse.gif">
        <HR>
    </H1>
</center>
    <pre>
    $text
    </pre>
	<center>
    $redirect
    <form action="Main.cgi" method="POST">
        <table border=0>
            <tr>
                <th>學號：</th><td><input type=text name=id></td>
            </tr>
            <tr>
                <th>密碼：</th><td><input type=password name=password></td>
            </tr>
                <th colspan=2>
                    &nbsp<P>
                    <input type=hidden name=crypt value="0">
                    <input type=hidden name=crypt2 value="0">
                    <input type=submit value="確定">&nbsp&nbsp
                    <input type="button" value="密碼查詢" name="bt_lost_passwd" onClick="return f_action(this)">
                </th>
            </tr>

        </table>
        <br>
    </form>
</center>
</body>
</html>

);

