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
print"<h4>�d�ߥ��׽ҾǥͦW��\\�� </i></h4><p>
<h4>�п�ܬO�_�]�t�s��</h4<br>

<form method=post action=Query_1.cgi>
<table border=0>
<select name=flag>
  <option selected value=1>�]�t�s��(��s��+�j�ǳ�)
  <option value=0>���]�t�s��(��s��+�j�ǳ�)
  <option value=2>���]�t��s���¥�(�j�ǳ�+��ҷs��)
  <option value=3>�Ȭd�ߤj�ǳ��¥�
</select><P>
</TD></TR>
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
