#!/usr/local/bin/perl
###################################################################################
#####  Batch_Transfer00.cgi
#####  原班學生批次加選至另一班
#####  Updates:
#####   2012/02/21 Coded by Nidalap :D~

print "Content-type: text/html","\n\n";

require "../../library/Reference.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."GetInput.pm";

%Input = User_Input();

print "
<html>
<head>
  $EXPIRE_META_TAG
  <title>第二版開排課系統 管理系統</title>
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
print"<h4>原班學生批次加選至另一班</h4><p>
  將「本學期」已選修某課程的學生，批次加選到另一班，
  偶爾系所開課錯誤可以用。
  <p>

  <form method=post action=Batch_Transfer01.cgi>
  <table border=0>
  <tr>
  <th><h3>系別:</h3></th><td><select name=dept_id>
";

my(@Dept,$dept,%Dept);

@Dept=Find_All_Dept();

foreach $dept(@Dept)
{
  %Dept=Read_Dept($dept);
  print "<option value=$Dept{id}>$Dept{cname}\n";
}

#print "<option value=\"sys\">Sys Manager";

print "
</select>
</td>
</tr>
<INPUT type=hidden name=password value=$Input{password}>
</table>
<input type=\"submit\" value=\"資料填寫完畢\">
<input type=\"reset\" value=\"重新填寫資料\">

</form>
<p>

<img src=".$GRAPH_URL."net4.jpg>
</center>
</body>
</html>
";
