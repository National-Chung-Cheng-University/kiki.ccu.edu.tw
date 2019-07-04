#!/usr/local/bin/perl

############################################################################
#####  Edit_Classroom2.cgi
#####  修改教室資料, 供開課系統使用
#####  Coder: (unknown)
#####  Modify:
#####    2002/02/10  新增教室最大/最適容量, 維護單位等欄位
############################################################################

######### require .pm files #########
require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
#require $LIBRARY_PATH."Teacher.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Classroom.pm";
#require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Error_Message.pm";

######### Main Program Starts Here #########
%Input = User_Input();
#@DEPT = Find_All_Dept();
@Classroom = Find_All_Classroom();

#
#  Check Password Here 
#

if( $Input{function} eq "edit" ){
  Check_Error();
  Delete_Classroom($Input{id});
  Add_Classroom(%Input);
  HTML_Head("更改教室資料完成");
  HTML_Part1();
  HTML_Ends();
}else{
  Delete_Classroom($Input{id});
  HTML_Head("刪除教室資料完成");
  HTML_Part2();
  HTML_Ends();
}

######### Main Program Ends Here #########

######### sub function HTML_Head #########
sub HTML_Head
{
 my($title);
 ($title)=@_;
 print << "HTML_HEAD"
Content-type: text/html


<html>
<head>
 <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
 <title>$title</title>
</head>
HTML_HEAD
}

######### sub function HTML_Part1 Starts Here #########
sub HTML_Part1
{
print "
 <body background=$GRAPH_URL"."bg98.jpg>
<center>

<table border=0>
<tr><td><img src=$GRAPH_URL"."ccu.gif><td>
<th><h1>修改教室資料作業完成</h1></th><td><img src=$GRAPH_URL"."ccu.gif></td>
</tr></table>

<hr size=3 width=50%>

<table border=3 height=35%>
  <TR>
    <th>欄位</th>
    <th>內容</th>
  </TR>
  <TR>
    <th>教室代碼</th>
    <th>$Input{id}</th>
  </tr>
  <tr>
    <th>教室名稱</th>
    <th>$Input{cname}</th>
  </tr>
  <TR>
    <TH>資料維護單位</TH>
    <TH>$Input{report_dept}</TH>
  </TR>
  <TR>
    <TH>最適容量</TH>
    <TH>$Input{size_fit}</TH>
  </TR>
  <TR>
    <TH>最大容量</TH>
    <TH>$Input{size_max}</TH>
  </TR>
  
</table><br>
<hr size=3 width=50%>
";
}

######### sub function HTML_Part2 Starts Here #########
sub HTML_Part2
{
 print "
 <body background=$GRAPH_URL"."bg98.jpg>
<center>

<table border=0>
<tr><td><img src=$GRAPH_URL"."ccu.gif><td>
<th><h1>刪除教室資料作業完成</h1></th><td><img src=$GRAPH_URL"."ccu.gif></td>
</tr></table>

<hr size=3 width=50%>

<table border=3 height=35%><caption>刪除教室資料</cation>
<tr><th>教室代碼</th>
<th>$Input{id}</th></tr>
<tr><th>教室名稱</th>
<th>$Input{cname}</th></tr>
</table><br>
<hr size=3 width=50%>
";
}
######### sub function HTML_Ends Starts Here #########
sub HTML_Ends
{
  print qq(
      <form method=post action="../su.cgi" target=_top>
        <input type=hidden name=password value=$Input{password}>
        <input type=submit value=回到管理主選單>
      </form>
      </center>
    </body>
    </html>
  );
}

######### sub function Check_Error Starts Here #########
sub Check_Error
{
  my($item);
  foreach $item(@CLASSROOM) {
    if($item eq $Input{id})  {
      Error("教室代碼:$item 已經存在, 無法新增!");
    }
  }
  if( ($Input{size_fit} =~ /\D+/) or ($Input{size_fit} <= 0) ) {
    Error("最適容量應為大於 0 的正數!");
  }
  if( ($Input{size_max} =~ /\D+/) or ($Input{size_max} <= 0) ) {
    Error("最大容量應為大於 0 的正數!");
  }
  if( $Input{size_fit} > $Input{size_max} ) {
    Error("最大容量應該大於等於最適容量!");
  }
}
