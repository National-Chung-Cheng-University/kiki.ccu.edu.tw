#!/usr/local/bin/perl
##########################################################################
#####   Modify_Select_Course_View00.cgi
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

%Input = User_Input();

##  本程式尚未檢查密碼, 可能是安全漏洞!  Nidalap May31,1999
#print("pass = $Input{password}");
#$result = Check_SU_Password($Input{password}, "su", "su");

$board_file = $REFERENCE_PATH."select_course_board.txt";
open(BOARD, "$board_file");
@text = <BOARD>;
close(BOARD);
$text = join("", @text);

$board_file = $REFERENCE_PATH."select_course_board_e.txt";
open(BOARD, "$board_file");
@text = <BOARD>;
close(BOARD);
$text_e = join("", @text);

print << "END_OF_HTML"
  <HTML>
    <HEAD><TITLE>修改學生選課單顯示文字</TITLE></HEAD>
    <BODY background="$GRAPH_URL./manager.jpg">
      <Center><H1>修改學生選課單顯示文字<hr></h1>
      請輸入/修改顯示文字:
      <FORM action="Modify_Select_Course_View01.cgi"
            method=POST>
		中文版
        <TEXTAREA cols=50 rows=10 name=text>$text</TEXTAREA>
		<P>
		英文版
		<TEXTAREA cols=50 rows=10 name=text_e>$text_e</TEXTAREA>
        <br>
        <INPUT type=submit value="確定修改">
      </FORM>
    </BODY>
  </HTML>
END_OF_HTML

