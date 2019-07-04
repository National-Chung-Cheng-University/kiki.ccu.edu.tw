#!/usr/local/bin/perl
######################################################################################################
#####  Login.cgi
#####  開課登入網頁
#####  Updates:
#####    ????/??/??
#####    2009/06/04  為 Find_All_Dept 加上 "NO_COM_DEPT" 參數，只讀取可以開課的系所 Nidalap :D~
#####    2010/04/20  系所下拉選單加入 optgroup 以示區別學院 Nidalap :D~
######################################################################################################
print "Content-type: text/html","\n\n";

require "../library/Reference.pm";
require $LIBRARY_PATH."Dept.pm";

print "
<html>
$EXPIRE_META_TAG
<head>
<title>國立中正大學 $SUB_SYSTEM_NAME開排課系統</title>
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
print"<h4>歡迎使用<i>國立中正大學$SUB_SYSTEM_NAME開排課系統</i></h4><p>
<h4>請填入以下基本資料</h4><p><br>

<form method=post action=Class_Menu.cgi>
<table border=0>
<tr>
<th><h3>系別:</h3></th><td><select name=dept_cd>";
my(@Dept,$dept,%Dept);

@Dept=Find_All_Dept("NO_COM_DEPT");
%college = Read_College(); 

$last_college = "";
foreach $dept (@Dept)
{
  %Dept=Read_Dept($dept);
  if( is_GRA() == 1 ) {
    next if( $dept !~ /6$/ );
  }
  if( $last_college ne $Dept{college} ) {
    print qq[</optgroup>]  if( $last_college ne "" );
    print qq[<optgroup label="$college{$Dept{college}}">];
  }
  $last_college = $Dept{college};
  print("<option value=$Dept{id}>$Dept{cname2}\n");
}

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
