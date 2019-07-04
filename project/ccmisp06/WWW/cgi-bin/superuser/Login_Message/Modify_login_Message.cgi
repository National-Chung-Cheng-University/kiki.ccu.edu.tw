#!/usr/local/bin/perl
##########################################################################
#####   Modify_lgoin_Message.cgi
#####   修改login Message公佈欄
#####   Coder: victora
#####   Date : 6/9,1999
#####   Modified: 
#####		2008/06/04 改為條列式呈現, 改得面目全非  Nidalap :D~
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
    
opendir(MSGDIR, $MESSAGE_PATH) or mkdir($MESSAGE_PATH);
@files = readdir(MSGDIR);

print qq(
  <HTML>
    <HEAD>
      <TITLE>修改選課公告主頁</TITLE>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    </HEAD>
    <BODY background="$GRAPH_URL./manager.jpg">
      <Center><H1>選課系統公告<hr></h1>
      <FORM action="new_message01.cgi" method=POST>
        <INPUT type=hidden name=password value=$Input{password}>
        <INPUT type=submit value="新增選課公告">
      </FORM>
      <TABLE border=0 width=75%>
        <TR bgcolor=YELLOW>
          <TH bgcolor=YELLOW>修改</TH><TH bgcolor=YELLOW>刪除</TH>
          <TH bgcolor=YELLOW>公告ID</TH><TH>置頂</TH><TH bgcolor=YELLOW width=60%>標題</TH>
        </TR>
);

foreach $file (@files) {
  next if( ($file eq ".") or ($file eq "..") );
  $file_open = $MESSAGE_PATH . $file;
  $message_id = $file;
  $message_id =~ s/.txt//; 
  open(FILE, $file_open);
  $title = <FILE>;
  $sticky = <FILE>;
  $sticky =~ s/\n//;
  if( $sticky eq "on" ) {
    $sticky = "<FONT color=RED>是</FONT>";
  }else{
    $sticky = "&nbsp";
  }
  print qq(
    <TR>
      <TD><A href="modify_message01.cgi?message_id=$message_id&password=$Input{password}">修改</A></TD>
      <TD><A href="delete_message01.cgi?message_id=$message_id&password=$Input{password}">刪除</A></TD>
      <TD>$message_id</TD><TD>$sticky</TD><TD>$title</TD>
    </TR>\n
  );
}


print << "END_OF_HTML"
      </TABLE>
    </BODY>
  </HTML>
END_OF_HTML

