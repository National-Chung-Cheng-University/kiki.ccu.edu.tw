#!/usr/local/bin/perl

############################################################################
#####  Edit_Classroom.cgi
#####  �ק�/�R���ЫǸ��, �Ѷ}�Ҩt�Ψϥ�
#####  Coder: (unknown)
#####  Modify:
#####    2002/02/10  �s�W�Ыǳ̤j/�̾A�e�q, ���@��쵥���
############################################################################

######### require .pm files #########
require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
#require $LIBRARY_PATH."Teacher.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Classroom.pm";
#require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Error_Message.pm";

######### Main Program Starts Here #########
#my(%Input,@DEPT);

### Read data in ###
%Input = User_Input();
#@DEPT = Find_All_Dept();
@Classroom = Find_All_Classroom();

 HTML_Head("�ק�ΧR���ЫǸ��");
 HTML();
 HTML_End();  # print HTML endings 

######### Main Program Ends Here #########

######### sub function HTML_Head Ends Here #########
sub HTML_Head
{
 my($title);
 ($title)=@_;
 print << "HTML_HEAD"
Content-type: text/html


<html>
<head>
 <meta http-equiv="Content-Type" content="text/html; charset=big5">
 <title>$title</title>
</head>
HTML_HEAD
}   

######### sub function HTML_Part1 Starts Here #########
sub HTML_Part1
{
 print "
 <body background=$GRAPH_URL"."bg98.jpg>
 <center>
<hr size=3 width=50%>";
}

sub HTML
{
 HTML_Part1();
 HTML_Part2();
 HTML_Options();
 HTML_Part3();
}

######### sub function HTML_Part2 Starts Here #########
sub HTML_Part2
{
 print "
 <form method=post action=Edit_Classroom2.cgi>
 <table border=0 height=50%>
 <caption><font color=brown>�п�ܱ��ק�ΧR�����Ы�</font></caption>
 <tr><td align=center>
   <select name=id>";
}

######### sub function HTML_Options Starts Here #########
sub HTML_Options
{
 my($classroom);
 foreach $classroom(@Classroom)
 {
  my(%classroom);
  %classroom=Read_Classroom($classroom);
  print "<option value=$classroom{id}>$classroom{cname}\n";
 }
}
######### sub function HTML_Part3 Starts Here #########
sub HTML_Part3
{
  print "
   </select></td>
 </tr>
<tr><th><font color=brown>�п�ܭק�ΧR���ЫǸ��</font></th></tr>
<tr><th><select name=function size=2>
<option value=edit selected>�ק�ЫǸ��
<option value=delete>�R���ЫǸ��
</select></th></tr> 
 </table>
 <input type=submit value=�e�X���>
 <hr size=3 width=50%>
 </form>";
}

######### sub function HTML_End Starts Here #########
sub HTML_End
{
  print qq(
      <form method=post action="../su.cgi" target=_top>
        <input type=hidden name=password value=$Input{password}>
        <input type=submit value=�^��޲z�D���>
      </form>
      </center>
    </body>
    </html>
  );
}