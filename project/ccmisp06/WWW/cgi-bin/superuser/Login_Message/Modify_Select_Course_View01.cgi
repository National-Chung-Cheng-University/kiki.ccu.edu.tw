#!/usr/local/bin/perl
##########################################################################
#####   Modify_Select_Course_View01.cgi
#####   修改學生選課單顯示文字
#####   Coder: Nidalap
#####   Upates : 
#####     1999/05/31 Created by Nidalap :D~ May 31,1999
#####	  2013/08/23 加入英文版 by Nidalap :D~
##########################################################################
print("Content-type:text/html\n\n");
print "<meta http-equiv='Content-Type' content='text/html; charset=utf-8'>";

require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Error_Message.pm";

$board_file = $REFERENCE_PATH."select_course_board.txt";
%Input = User_Input();
open(BOARD, ">$board_file") or 
     Fatal_Error("Cannot open board file in Modify_Course_View01.cgi!");

print BOARD $Input{text};
close(BOARD);

$board_file = $REFERENCE_PATH."select_course_board_e.txt";
open(BOARD, ">$board_file") or 
     Fatal_Error("Cannot open board file in Modify_Course_View01.cgi!");

print BOARD $Input{text_e};
close(BOARD);

print << "END_OF_HTML"
  <HEAD><TITLE>修改學生選課單顯示文字</TITLE></HEAD>
  <BODY background="$GRAPH_URL./manager.jpg">
  <Center><H1>修改學生選課單顯示文字<hr></h1>
  <font size=3 color=red><b>資料已修改完成!</b></font><br><br>
  <br><br>
  <font size=3
color=black><b>修改過的資料將會馬上顯示在學生檢視選課單網頁上!</b></font>  
END_OF_HTML

