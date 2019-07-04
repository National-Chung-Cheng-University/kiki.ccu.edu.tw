#!/usr/local/bin/perl
##########################################################################
#####   Modify_login_Message01.cgi
#####   修改公告文字
#####   Coder: victora
#####   Date : 6/9,1999
##########################################################################
print("Content-type:text/html\n\n");
require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Error_Message.pm";

$board_file = $REFERENCE_PATH."Login_Message.txt";

%Input = User_Input();
open(BOARD, ">$board_file") or 
     Fatal_Error("Cannot open board file in Modify_Course_View01.cgi!");

print BOARD $Input{text};
close(BOARD);

print << "END_OF_HTML"
  <HEAD><TITLE>修改公告內容</TITLE></HEAD>
  <BODY background="$GRAPH_URL./manager.jpg">
  <Center><H1>修改公告內容<hr></h1>
  <font size=3 color=red><b>資料已修改完成!</b></font><br><br>
  <br><br>
  <font size=3
color=black><b>修改過的資料將會馬上顯示在學生選課網頁LOGIN上!</b></font>  
END_OF_HTML

