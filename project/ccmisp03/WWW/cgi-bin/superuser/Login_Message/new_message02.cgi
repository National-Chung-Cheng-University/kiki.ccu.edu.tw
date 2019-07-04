#!/usr/local/bin/perl
##########################################################################
#####   new_message02.cgi
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
if( $Input{sticky} eq "on" ) {
  $sticky = "是";
}else{
  $Input{sticky} = "off";
  $sticky = "否";
}

$message_file = $MESSAGE_PATH . $Input{message_id} . ".txt";

while( -e $message_file ) {
#  $message_file .= "a";
  preg_replace(".txt", "a.txt", $message_file);
  print("檔案已經存在, 改名為  $message_file.<BR>");
}

open(FILE, ">$message_file");
print FILE ("$Input{title}\n");
print FILE ("$Input{sticky}\n");
print FILE $Input{text};
close(FILE);

$message_id = Generate_Message_ID();
$Input{text} =~ s/\n/<BR>/mg;

print << "END_OF_HTML"
  <HTML>
    <HEAD>
      <TITLE>修改選課公告主頁</TITLE>
      <meta http-equiv="Content-Type" content="text/html; charset=big5">
    </HEAD> 
    <BODY background="$GRAPH_URL./manager.jpg">
      <Center><H1>選課系統公告<hr></h1>
        公告已經新增完畢!<P>
        <TABLE border=0> 
          <TR>
            <TD bgcolor=YELLOW>訊息id:</TD>
            <TD>$Input{message_id}</TD>
          </TR>
          <TR>
            <TD bgcolor=YELLOW>標題:</TD>
            <TD>$Input{title}</TD>
          </TR>
          <TR>
            <TD bgcolor=YELLOW>置頂:</TD>
            <TD>$sticky</TD>
          </TR>
          <TR>
            <TD bgcolor=YELLOW>內容</TD>
            <TD>$Input{text}</TD>
          </TR>
        </TABLE>
        <br>
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