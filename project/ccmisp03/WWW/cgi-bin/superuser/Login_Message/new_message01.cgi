#!/usr/local/bin/perl
##########################################################################
#####   new_message01.cgi
#####   修改login Message公佈欄
#####   Coder: Nidalap :D~
#####   Date : 20080514
##########################################################################
print("Content-type:text/html\n\n");
require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH . "Error_Message.pm";

%Input = User_Input();

$pass_result = Check_SU_Password($Input{password}, "su", "su");
if($pass_result ne "TRUE") {
  print("密碼錯誤!");
  exit(1);
}
    
$message_id = Generate_Message_ID();

print << "END_OF_HTML"
  <HTML>
    <HEAD>
      <TITLE>修改選課公告主頁</TITLE>
      <meta http-equiv="Content-Type" content="text/html; charset=big5">
    </HEAD> 
    <BODY background="$GRAPH_URL./manager.jpg">
      <Center><H1>選課系統公告<hr></h1>
      <FORM action="new_message02.cgi" method=POST>
        <INPUT type=hidden name=password value=$Input{password}>
        <TABLE border=0> 
          <TR>
            <TD bgcolor=YELLOW>訊息id:</TD>
            <TD><INPUT name=message_id value=$message_id></TD>
          </TR>
          <TR>
            <TD bgcolor=YELLOW>標題:</TD>
            <TD><INPUT name=title></TD>
          </TR>
          <TR>
            <TD bgcolor=YELLOW>置頂:</TD>
            <TD><INPUT type=checkbox name=sticky></TD>
          </TR>
          <TR>
            <TD bgcolor=YELLOW>內容</TD>
            <TD><TEXTAREA cols=50 rows=10 name=text></TEXTAREA></TD>
          </TR>
        </TABLE>
        <br>
        <INPUT type=submit value="確定修改">
      </FORM>
    </BODY>
  </HTML>
END_OF_HTML
;

###########################################################################
sub Generate_Message_ID()
{
  my(%time, $message_file_test);
  
#  opendir(MSG, $MESSAGE_PATH) or mkdir($MESSAGE_PATH);
#  @files = readdir(MSG);
  %time = gettime();
  $time{month} = "0".$time{month}	if( $time{month} < 10);
  $time{day} = "0".$time{day}		if( $time{day} < 10);  
  $message_id = $time{year} . $time{month} . $time{day};

  return($message_id);  
}