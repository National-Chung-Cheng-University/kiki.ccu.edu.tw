#!/usr/local/bin/perl
##########################################################################
#####   Modify_Select_Course_View00.cgi
#####   �ק�ǥͿ�ҳ���ܤ�r
#####   Coder: Nidalap
#####   Date : May 31,1999
##########################################################################
print("Content-type:text/html\n\n");
require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";

%Input = User_Input();

##  ���{���|���ˬd�K�X, �i��O�w���|�}!  Nidalap May31,1999
#print("pass = $Input{password}");
#$result = Check_SU_Password($Input{password}, "su", "su");

$board_file = $REFERENCE_PATH."select_course_board.txt";
open(BOARD, "$board_file");
@text = <BOARD>;
close(BOARD);
$text = join("", @text);

print << "END_OF_HTML"
  <HTML>
    <HEAD><TITLE>�ק�ǥͿ�ҳ���ܤ�r</TITLE></HEAD>
    <BODY background="$GRAPH_URL./manager.jpg">
      <Center><H1>�ק�ǥͿ�ҳ���ܤ�r<hr></h1>
      �п�J/�ק���ܤ�r:
      <FORM action="Modify_Select_Course_View01.cgi"
            method=POST>
        <TEXTAREA cols=50 rows=10 name=text>$text</TEXTAREA>
        <br>
        <INPUT type=submit value="�T�w�ק�">
      </FORM>
    </BODY>
  </HTML>
END_OF_HTML

