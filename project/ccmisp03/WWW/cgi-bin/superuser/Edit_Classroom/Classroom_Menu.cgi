#!/usr/local/bin/perl

######### require .pm files #########
require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";

######### Main Program Here #########
my(%Input);
%Input=User_Input();

#
#  check password here
#

 HTML_Head("�ЫǸ�ƺ޲z�t��");
 HTML();

######### Main Program End Here #########

######### Start of sub function HTML_Head #########

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

######### sub function HTML starts here #########
sub HTML
{
print "
<html>
<head>
<title>�Ыǰ򥻸�ƺ޲z</title>
</head>

<body background=$GRAPH_URL"."manager.jpg>
<center>
<table border=0>
<tr>
<th><img src=$GRAPH_URL"."classroom.jpg></th><td><img src=$GRAPH_URL"."ccu.gif></td>
</tr></table>

<hr size=2 width=50%>
<table border=0 height=40%>
<tr><th>
<form method=post action=Add_Classroom.cgi>
<input type=hidden name=function value=select>
<input type=hidden name=password value=$Input{password}>
<input type=submit value=�s�W�ЫǸ��>          
</form>
</th></tr>
<tr><th>
<form method=post action=Edit_Classroom.cgi>
<input type=hidden name=password value=$Input{password}>
<input type=submit value=�ק�P�R���ЫǸ��>          
</form>
</th></tr>
</table>
</center>
</body>
</html>";
}