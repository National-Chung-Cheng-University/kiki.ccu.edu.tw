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
print"<h4>查詢未修課學生名單功\能 </i></h4><p>
<h4>請選擇是否包含新生</h4<br>

<form method=post action=Query_1.cgi>
<table border=0>
<select name=flag>
  <option selected value=1>包含新生(研究所+大學部)
  <option value=0>不包含新生(研究所+大學部)
  <option value=2>不包含研究所舊生(大學部+研所新生)
  <option value=3>僅查詢大學部舊生
</select><P>
</TD></TR>
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
