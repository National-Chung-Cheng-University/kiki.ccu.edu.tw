#!/usr/local/bin/perl
print "Content-type: text/html","\n\n";

require "../../library/Reference.pm";
require $LIBRARY_PATH."Dept.pm";

print "
<html>
<head>
<title>�ĤG���}�ƽҨt��</title>
</head>
<body background=".$GRAPH_URL."ccu-sbg.jpg>
<center>
<h1>";
print "
<img src=".$GRAPH_URL."open.jpg>
</h1>
<p><font size=4><blink>
";
print"</blink></font>";
print"<h4>�d�ߩҦ��ǥͭײ߾Ǥ��\\�� </i></h4><p>

<form method=post action=Query_student_credit2.cgi>
<table border=0>
 <TR><TD>
  �O�_���ͯ¤�r����: <Input type=\"checkbox\" name=\"plaintext\">
 </td>
</tr>
</table>
<br>
<p>
<input type=\"submit\" value=\"�}�l�d��\">
<p>

</form>
<p>

<img src=".$GRAPH_URL."net4.jpg>
<i>
�j�P��ĳ�ϥ�Netscape4.x�H�W�������s����
</i>
</center>
</body>
</html>
";
