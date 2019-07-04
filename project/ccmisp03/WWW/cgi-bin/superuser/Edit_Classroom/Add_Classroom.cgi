#!/usr/local/bin/perl

############################################################################
#####  Add_Classroom.cgi
#####  �s�W�ЫǸ��, �Ѷ}�Ҩt�Ψϥ�
#####  Coder: (unknown)
#####  Modify:
#####    2002/02/10  �s�W�Ыǳ̤j/�̾A�e�q, ���@��쵥���
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
  HTML_Head("�s�W�ЫǸ�Ƨ���");
print "
 <body background=$GRAPH_URL"."manager.jpg>
<center>
<table border=0><tr>
<td><img src=$GRAPH_URL"."ccu.gif></td>
<th><h1>�����s�W���ЫǸ��</h1></th>
<td><img src=$GRAPH_URL"."ccu.gif></td></tr></table>
<hr size=2 width=50%>
";

#foreach $key (keys %Input) {
#  print("$key: $Input{$key}<BR>\n");
#}

print "
<table border=0>
  <tr>
    <td>�ЫǥN�X:</td>
    <td>$Input{id}</td>
  </tr>
  <tr>
    <td>�ЫǦW��:</td>
    <td>$Input{cname}</td>
  </tr>
  <TR>
    <TD>��ƺ��@���</TD>
    <TD>$Input{report_dept}</TD>
  </TR>
  <TR>
    <TD>�Ыǳ̾A�e�q</TD>
    <TD>$Input{size_fit}</TD>
  </TR>
  <TR>
    <TD>�Ыǳ̤j�e�q</TD>
    <TD>$Input{size_max}</TD>
  </TR>
</table> 
 </form>
<hr size=2 width=50%>
<form method=post action=Classroom_Menu.cgi>
<input type=hidden name=password value=>
<input type=submit value=�^��ЫǸ�ƺ޲z�D���>
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
      Error("�ЫǥN�X:$item �w�g�s�b, �L�k�s�W!"); 
    }
  }
  if( ($Input{size_fit} =~ /\D+/) or ($Input{size_fit} <= 0) ) {
    Error("�̾A�e�q�����j�� 0 ������!");
  }
  if( ($Input{size_max} =~ /\D+/) or ($Input{size_max} <= 0) ) {
    Error("�̤j�e�q�����j�� 0 ������!");
  }
  if( $Input{size_fit} > $Input{size_max} ) {
    Error("�̤j�e�q���Ӥj�󵥩�̾A�e�q!");
  }
}

######### Start of sub function HTML_For_Selection() ##########

sub HTML_For_Selection
{
 HTML_Head("�s�W�ЫǸ��");
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
 <meta http-equiv="Content-Type" content="text/html; charset=big5">
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
<th><h1>�s�W�ЫǸ��</h1></th>
<td><img src=$GRAPH_URL"."ccu.gif></td></tr></table>
<form method=post action=Add_Classroom.cgi>
<input type=hidden name=function value=add>
<hr size=2 width=50%>
<table border=0>
  <tr>
    <td>�п�J�s�W�ЫǥN�X:</td>
    <td><input type=text name=id length=6 maxlength=6></td>
  </tr>
  <tr>
    <td>�п�J�s�W�Ыǥ��W:</td>
    <td><input type=text name=cname></td>
  </tr>
  <TR>
    <TD>��ƺ��@���</TD>
    <TD><INPUT name=report_dept></TD>
  </TR>
  <TR> 
    <TD>�Ыǳ̾A�e�q</TD>
    <TD><INPUT length=2 name=size_fit></TD>
  </TR>
  <TR> 
    <TD>�Ыǳ̤j�e�q</TD>
    <TD><INPUT length=2 name=size_max></TD>
  </TR>

<tr><th colspan=2><input type=submit value=�s�W���Ы�></th></tr>
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
 HTML_Head("�s�W�Ыǧ���");
   print "
<body background=$GRAPH_URL"."manager.jpg>
<center>
<table border=0><tr>
<td><img src=$GRAPH_URL"."ccu.gif></td>
<th><h1>�s�W�ЫǸ�Ƨ���</h1></th>
<td><img src=$GRAPH_URL"."ccu.gif></td></tr></table>
<br><hr>
<table border=1>
  <tr>
    <th>�ЫǥN�X</th>
    <th>$c</th>
  </tr>
  <tr>
    <th>�ЫǦW��</th>
    <th>$dept{cname}</th>
  </tr>
<br><hr>
<form method=post action=$CGI_URL"."superuser/Classroom_Menu.cgi>
<input type=hidden name=password value=>
<input type=submit value=�^��ЫǺ޲z�t��>
</form>

<a href= $CGI_URL"."superuser/>�^��޲z�̿��</a>
</body></html>"; 

}
######## Start of sub function Check_Errors #########
#sub Check_Errors
#{
# my($c_id,$c_n,@CLASSROOM,$classroom);
# my(%classroom); 
# ($c_id,$c_n)=@_;
# 
# if($x_id eq "") { Error("�z�S����J�ЫǥN�X"); }
# if($c_n eq "") { Error("�z�S����ܱЫǦW��"); }
# @CLASSROOM=Read_Classroom_File();
# foreach $classroom(@CLASSROOM)
# {
#  if($classroom eq $c_id)
#  {
#   %classroom=Read_Classroom($c_id);
#   Error("�z��J���ЫǥN�X: $classroom �w�g�s�b\n<br>
#<table border=3><tr><td></td><th>�s�W���</th><th>�즳���</th></tr>
#<tr><td>�ЫǦW��</td><th>$t_n</th><th>$Classroom_Name{$classroom}</th></tr>
#</table>"); 
#  }
# }
#}