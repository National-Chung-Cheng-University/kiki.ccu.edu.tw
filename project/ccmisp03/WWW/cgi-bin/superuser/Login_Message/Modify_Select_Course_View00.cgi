#!/usr/local/bin/perl
##########################################################################
#####   Modify_Select_Course_View00.cgi
#####   修改學生選課單顯示文字
#####   Coder: Nidalap
#####   Date : May 31,1999
##########################################################################
print("Content-type:text/html\n\n");
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

print << "END_OF_HTML"
  <HTML>
    <HEAD><TITLE>修改學生選課單顯示文字</TITLE></HEAD>
    <BODY background="$GRAPH_URL./manager.jpg">
      <Center><H1>修改學生選課單顯示文字<hr></h1>
      請輸入/修改顯示文字:
      <FORM action="Modify_Select_Course_View01.cgi"
            method=POST>
        <TEXTAREA cols=50 rows=10 name=text>$text</TEXTAREA>
        <br>
        <INPUT type=submit value="確定修改">
      </FORM>
    </BODY>
  </HTML>
END_OF_HTML

