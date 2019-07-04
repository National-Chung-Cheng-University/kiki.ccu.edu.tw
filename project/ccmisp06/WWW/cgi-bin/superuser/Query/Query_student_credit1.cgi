#!/usr/local/bin/perl
print "Content-type: text/html","\n\n";

require "../../library/Reference.pm";
require $LIBRARY_PATH."Dept.pm";

print "
<html>
<head>
<title>第二版開排課系統</title>
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
print"<h4>查詢所有學生修習學分功\能 </i></h4><p>

<form method=post action=Query_student_credit2.cgi>
<table border=0>
 <TR><TD>
  是否產生純文字網頁: <Input type=\"checkbox\" name=\"plaintext\">
 </td>
</tr>
</table>
<br>
<p>
<input type=\"submit\" value=\"開始查詢\">
<p>

</form>
<p>

<img src=".$GRAPH_URL."net4.jpg>
<i>
強烈建議使用Netscape4.x以上版本的瀏覽器
</i>
</center>
</body>
</html>
";
