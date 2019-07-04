#!/usr/local/bin/perl

############################################################################
#####  Add_Classroom.cgi
#####  新增教室資料, 供開課系統使用
#####  Coder: (unknown)
#####  Modify:
#####    2002/02/10  新增教室最大/最適容量, 維護單位等欄位
############################################################################

######### require .pm #########
require "../../library/Reference.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Error_Message.pm";
######### Main Program Here #########

%Input= User_Input();

@CLASSROOM = Find_All_Classroom();

#  check password here

if($Input{function} eq "select") {
  HTML_For_Selection();
}
if($Input{function} eq "add") {
  Check_Error(%Input);
  Add_Classroom(%Input);
  HTML();
}

######### End of Main Program ########

######### sub function HTML Starts Here ########
sub HTML
{
  HTML_Head("新增教室資料完成");
print "
 <body background=$GRAPH_URL"."manager.jpg>
<center>
<table border=0><tr>
<td><img src=$GRAPH_URL"."ccu.gif></td>
<th><h1>完成新增的教室資料</h1></th>
<td><img src=$GRAPH_URL"."ccu.gif></td></tr></table>
<hr size=2 width=50%>
";

#foreach $key (keys %Input) {
#  print("$key: $Input{$key}<BR>\n");
#}

print "
<table border=0>
  <tr>
    <td>教室代碼:</td>
    <td>$Input{id}</td>
  </tr>
  <tr>
    <td>教室名稱:</td>
    <td>$Input{cname}</td>
  </tr>
  <TR>
    <TD>資料維護單位</TD>
    <TD>$Input{report_dept}</TD>
  </TR>
  <TR>
    <TD>教室最適容量</TD>
    <TD>$Input{size_fit}</TD>
  </TR>
  <TR>
    <TD>教室最大容量</TD>
    <TD>$Input{size_max}</TD>
  </TR>
</table> 
 </form>
<hr size=2 width=50%>
<form method=post action=Classroom_Menu.cgi>
<input type=hidden name=password value=>
<input type=submit value=回到教室資料管理主選單>
</center>
</body>
</html>";
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

######### Start of sub function HTML_For_Selection() ##########

sub HTML_For_Selection
{
 HTML_Head("新增教室資料");
 HTML_Part1();
} 

######### Start of sub function HTML_Head #########

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
######### End of sub function HTML_Head #########

######### Start of sub function HTML_Part1 #########

sub HTML_Part1
{
  print "
<body background=$GRAPH_URL"."manager.jpg>
<center>
<table border=0><tr>
<td><img src=$GRAPH_URL"."ccu.gif></td>
<th><h1>新增教室資料</h1></th>
<td><img src=$GRAPH_URL"."ccu.gif></td></tr></table>
<form method=post action=Add_Classroom.cgi>
<input type=hidden name=function value=add>
<hr size=2 width=50%>
<table border=0>
  <tr>
    <td>請輸入新增教室代碼:</td>
    <td><input type=text name=id length=6 maxlength=6></td>
  </tr>
  <tr>
    <td>請輸入新增教室全名:</td>
    <td><input type=text name=cname></td>
  </tr>
  <TR>
    <TD>資料維護單位</TD>
    <TD><INPUT name=report_dept></TD>
  </TR>
  <TR> 
    <TD>教室最適容量</TD>
    <TD><INPUT length=2 name=size_fit></TD>
  </TR>
  <TR> 
    <TD>教室最大容量</TD>
    <TD><INPUT length=2 name=size_max></TD>
  </TR>

<tr><th colspan=2><input type=submit value=新增此教室></th></tr>
</table> 
 </form>
<hr size=2 width=50%>
</center>
</body>
</html>";
}

######## Start of sub function Add_Teacher #########

#sub Add_Classroom
#{
#  Check_Errors(@_);
#  Write_Classroom_File(@_);
#  HTML_Finish_Add(@_); 
#}

######## Start of sub HTML_Finish_Add #########

sub HTML_Finish_Add
{
 my($c,$d,%classroom);
 ($c,$d)=@_;
 %classroom=Read_Classroom($d);
 HTML_Head("新增教室完成");
   print "
<body background=$GRAPH_URL"."manager.jpg>
<center>
<table border=0><tr>
<td><img src=$GRAPH_URL"."ccu.gif></td>
<th><h1>新增教室資料完成</h1></th>
<td><img src=$GRAPH_URL"."ccu.gif></td></tr></table>
<br><hr>
<table border=1>
  <tr>
    <th>教室代碼</th>
    <th>$c</th>
  </tr>
  <tr>
    <th>教室名稱</th>
    <th>$dept{cname}</th>
  </tr>
<br><hr>
<form method=post action=$CGI_URL"."superuser/Classroom_Menu.cgi>
<input type=hidden name=password value=>
<input type=submit value=回到教室管理系統>
</form>

<a href= $CGI_URL"."superuser/>回到管理者選單</a>
</body></html>"; 

}
######## Start of sub function Check_Errors #########
#sub Check_Errors
#{
# my($c_id,$c_n,@CLASSROOM,$classroom);
# my(%classroom); 
# ($c_id,$c_n)=@_;
# 
# if($x_id eq "") { Error("您沒有輸入教室代碼"); }
# if($c_n eq "") { Error("您沒有選擇教室名稱"); }
# @CLASSROOM=Read_Classroom_File();
# foreach $classroom(@CLASSROOM)
# {
#  if($classroom eq $c_id)
#  {
#   %classroom=Read_Classroom($c_id);
#   Error("您輸入的教室代碼: $classroom 已經存在\n<br>
#<table border=3><tr><td></td><th>新增資料</th><th>原有資料</th></tr>
#<tr><td>教室名稱</td><th>$t_n</th><th>$Classroom_Name{$classroom}</th></tr>
#</table>"); 
#  }
# }
#}