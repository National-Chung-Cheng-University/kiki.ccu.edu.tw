#!/usr/local/bin/perl
$|=1;
print "Content-type: text/html","\n\n";
$|=0;
require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Dept.pm";
my(%Input,@Dept,@Course,%Dept);

%Input = User_Input();
%Dept = Read_Dept($Input{dept_id});
@Course = Find_All_Course( $Dept{id},"","history" );

print "
<html>
<head>
<title>同班學生批次加選 - $Dept{cname}</title>
</head>
<body background=".$GRAPH_URL."ccu-sbg.jpg>
<center>
<h1>";
print "
<img src=".$GRAPH_URL."open.jpg>
</h1>
<p>
";
print"<h4>同班學生批次加選</h4><p>
<h4>請選擇上學期科目及班別</h4><p><br>

<form method=post action=Batch_Add02.cgi>
<table border=0>
<tr>
<th><h3>科目:</h3></th><td><select name=course_id>";

 my($course,%temp,$i,$count);
 $count = @Course;
 for($i=0;$i < $count;$i++)
 {
  %temp = Read_Course($Dept{id},$Course[$i]{id},$Course[$i]{group},"history","");
  print"<option value=$temp{id}_$temp{group}>[$temp{id}-$temp{group}]$temp{cname}\n";
 }

print "
</select>
<input type=hidden name=dept_cd value=$Dept{id}>
<input type=hidden name=dept_name value=$Dept{cname}>
</td>
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
