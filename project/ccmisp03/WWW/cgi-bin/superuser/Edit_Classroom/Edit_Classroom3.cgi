#!/usr/local/bin/perl

############################################################################
#####  Edit_Classroom2.cgi
#####  �ק�ЫǸ��, �Ѷ}�Ҩt�Ψϥ�
#####  Coder: (unknown)
#####  Modify:
#####    2002/02/10  �s�W�Ыǳ̤j/�̾A�e�q, ���@��쵥���
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
  HTML_Head("���ЫǸ�Ƨ���");
  HTML_Part1();
  HTML_Ends();
}else{
  Delete_Classroom($Input{id});
  HTML_Head("�R���ЫǸ�Ƨ���");
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
 <meta http-equiv="Content-Type" content="text/html; charset=big5">
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
<th><h1>�ק�ЫǸ�Ƨ@�~����</h1></th><td><img src=$GRAPH_URL"."ccu.gif></td>
</tr></table>

<hr size=3 width=50%>

<table border=3 height=35%>
  <TR>
    <th>���</th>
    <th>���e</th>
  </TR>
  <TR>
    <th>�ЫǥN�X</th>
    <th>$Input{id}</th>
  </tr>
  <tr>
    <th>�ЫǦW��</th>
    <th>$Input{cname}</th>
  </tr>
  <TR>
    <TH>��ƺ��@���</TH>
    <TH>$Input{report_dept}</TH>
  </TR>
  <TR>
    <TH>�̾A�e�q</TH>
    <TH>$Input{size_fit}</TH>
  </TR>
  <TR>
    <TH>�̤j�e�q</TH>
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
<th><h1>�R���ЫǸ�Ƨ@�~����</h1></th><td><img src=$GRAPH_URL"."ccu.gif></td>
</tr></table>

<hr size=3 width=50%>

<table border=3 height=35%><caption>�R���ЫǸ��</cation>
<tr><th>�ЫǥN�X</th>
<th>$Input{id}</th></tr>
<tr><th>�ЫǦW��</th>
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
        <input type=submit value=�^��޲z�D���>
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
