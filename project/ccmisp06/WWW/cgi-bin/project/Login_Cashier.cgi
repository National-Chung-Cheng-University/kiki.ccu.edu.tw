#!/usr/local/bin/perl
print "Content-type: text/html","\n\n";

require "../library/Reference.pm";
require $LIBRARY_PATH."Dept.pm";

print "
<html>
<head>
<title>國立中正大學 $SUB_SYSTEM_NAME開排選課系統</title>
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
print"<h4>歡迎使用<i>國立中正大學$SUB_SYSTEM_NAME開排選課系統</i></h4><p>
<h4>請填入以下基本資料</h4><p><br>

<form method=post action=Cashier_Menu.cgi>
<table border=0>
<tr>
<th><h3>單位別:</h3></th><td><select name=dept_cd>";

 print "<option value=\"cashier\">出納組\n";

#print "<option value=\"sys\">Sys Manager";

print "
</select>
</td>
</tr>
<tr>
<th><h3>密碼:</h3></th><td><input type=password name=password></td>
</tr>
</table>
<input type=\"submit\" value=\"資料填寫完畢\">
<input type=\"reset\" value=\"重新填寫資料\">

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
