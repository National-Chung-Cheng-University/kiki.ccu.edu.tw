#!/usr/local/bin/perl
##########################################################################
#####   Modify_login_Message01.cgi
#####   �ק綠�i��r
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
  <HEAD><TITLE>�ק綠�i���e</TITLE></HEAD>
  <BODY background="$GRAPH_URL./manager.jpg">
  <Center><H1>�ק綠�i���e<hr></h1>
  <font size=3 color=red><b>��Ƥw�ק粒��!</b></font><br><br>
  <br><br>
  <font size=3
color=black><b>�ק�L����ƱN�|���W��ܦb�ǥͿ�Һ���LOGIN�W!</b></font>  
END_OF_HTML

