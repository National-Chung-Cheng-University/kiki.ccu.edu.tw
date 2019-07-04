#!/usr/local/bin/perl
##########################################################################
#####   modify_message02.cgi
#####   修改login Message公佈欄
#####   Coder: Nidalap :D~
#####   Updates : 
#####     2008/05/14  Created by Nidalap :D~
#####     2015/05/19  新增英文版欄位及檔案 Nidalap :D~
##########################################################################
print("Content-type:text/html\n\n");
print("<meta http-equiv='Content-Type' content='text/html; charset=utf-8'>");

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

$message_id = $Input{message_id};
$message_file = $MESSAGE_PATH . $Input{message_id} . ".txt";
if( $Input{sticky} eq "" ) {
  $Input{sticky} = "off";
}

#print("message_id, file = $message_id; $message_file<BR>\n");
open(FILE, ">$message_file");
print FILE ("$Input{title}\n");
print FILE ("$Input{sticky}\n");
print FILE $Input{text};

$message_file = $MESSAGE_PATH . $Input{message_id} . "_e.txt";
open(FILE, ">$message_file");
print FILE ("$Input{title_e}\n");
print FILE ("$Input{sticky}\n");
print FILE $Input{text_e};
close(FILE);

$Input{text} =~ s/\n/<BR>/mg;
$Input{text_e} =~ s/\n/<BR>/mg;

print << "END_OF_HTML"
  <HTML>
    <HEAD>
      <TITLE>修改選課公告主頁</TITLE>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    </HEAD> 
    <BODY background="$GRAPH_URL./manager.jpg">
      <Center><H1>選課系統公告<hr></h1>
        公告已經修改完畢!<P>
        <TABLE border=0> 
          <TR>
            <TD bgcolor=YELLOW>訊息id:</TD>
            <TD>$Input{message_id}</TD>
          </TR>
          <TR>
            <TD bgcolor=YELLOW>標題:</TD>
            <TD>
			  中：$Input{title}
			  英：$Input{title_e}
			</TD>
          </TR>
          <TR>
            <TD bgcolor=YELLOW>內容</TD>
            <TD>$Input{text}</TD>
          </TR>
          <TR>
            <TD bgcolor=YELLOW>英文版內容</TD>
            <TD>$Input{text_e}</TD>
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