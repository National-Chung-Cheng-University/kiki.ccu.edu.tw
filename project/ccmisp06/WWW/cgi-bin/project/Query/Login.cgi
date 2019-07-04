#!/usr/local/bin/perl
print "Content-type: text/html","\n\n";

require "../../library/Reference.pm";
require $LIBRARY_PATH."Dept.pm";

print "
<html>
<head>
$EXPIRE_META_TAG
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
print"<h4>查詢修課學生名單功\能 Version 2.000</i></h4><hr><p>";

#Show_Ban();
Show_html();

sub Show_Ban() {
  print qq(目前不提供查詢功\能, 請於規定時間上網查詢, 謝謝!<br>\n);
}

sub Show_html() {
  print qq(
    <h4>請選擇系所</h4><p><br>
    <form method=post action=Query_1.cgi>
    <table border=0>
    <tr>
    <th><h3>系別:</h3></th><td><select name=dept_cd>
  );
  my(@Dept,$dept,%Dept);
  @Dept=Find_All_Dept();
  foreach $dept(@Dept)
  {
   %Dept=Read_Dept($dept);
   print "<option value=$Dept{id}>$Dept{cname}\n";
  }
  #print "<option value=\"sys\">Sys Manager";
  print qq(
    </select>
    </td>
    </tr>
    </table>
    <input type="submit" value="資料填寫完畢">
    <input type="reset" value="重新填寫資料">
    </form>
    <p>
    <img src=".$GRAPH_URL."net4.jpg>
    <i>強烈建議使用Netscape4.x以上版本的瀏覽器</i>
    </center>
    </body>
    </html>
  );
}
