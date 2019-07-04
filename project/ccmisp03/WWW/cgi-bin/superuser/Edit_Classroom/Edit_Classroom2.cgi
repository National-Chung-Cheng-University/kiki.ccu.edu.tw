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
#my(%Input);

%Input= User_Input();
#@DEPT = Find_All_Dept();
@Classroom = Find_All_Classroom();

#
#  check password here
#

 Check_Input();
if($Input{function} eq "delete")
{ 
 HTML_Head("�R���ЫǸ��");
 Display_For_Delete(); 
}

if($Input{function} eq "edit")
{ 
 HTML_Head("�ק�ЫǸ��"); 
 Display_For_Edit();
}

######### Main Program Ends Here #########

#TEST();
#sub TEST{ print "<body>Teacher_Code=$Input{Teacher_Code}</body>"; }


######### sub function Check_Input Starts Here #########
sub Check_Input
{
 if($Input{id} eq "")
 {
  Error("�z�S����ܱЫǥN�X");
 }
}
######### sub function HTML_Head Starts Here #########
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

######### sub function Display_For_Edit Starts Here #########
sub Display_For_Edit
{
 HTML_Part1();
# HTML_Options();
 HTML_Part2();
 HTML_Ends();
}

######### sub function Display_For_Delete Starts here #########
sub Display_For_Delete
{
 HTML_Part3();
 HTML_Ends();
}
######### sub function HTML_Part1 Starts Here #########
sub HTML_Part1
{
# my(%dept);
 %classroom=Read_Classroom($Input{id});

 print qq(
   <body background=$GRAPH_URL"."bg98.jpg>
   <center>
     <table border=0>
       <tr>
         <td><img src=$GRAPH_URL"."ccu.gif><td>
         <th><h1>�ק�ЫǸ��</h1></th><td><img src=$GRAPH_URL"."ccu.gif></td>
       </tr>
     </table>
     <hr size=3 width=50%>
     <form method=post action=Edit_Classroom3.cgi>
       <input type=hidden name=function value=edit>
       <input type=hidden name=id value=$classroom{id}>

       <table border=3 height=35%>
         <tr>
           <th>�ЫǥN�X</th>
           <th>$classroom{id}</th>
         <tr>
           <th>�ЫǦW��</th>
           <th><input type=text name=cname value=$classroom{cname}></th>
         </tr>
         <TR>
           <TH>��ƺ��@���</TH>
           <TH><INPUT name=report_dept value=$classroom{report_dept}></TH>
         </TR>
         <TR>
           <TH>�Ыǳ̾A�e�q</TH>
           <TH><INPUT name=size_fit length=2 value=$classroom{size_fit}></TH>
         </TR>
         <TR>
           <TH>�Ыǳ̤j�e�q</TH>
           <TH><INPUT name=size_max length=2 value=$classroom{size_max}></TH>
         </TR>

);
}

######### sub function HTML_Part2 Starts Here #########
sub HTML_Part2
{
 print "
</select></th></tr>
<tr><td align=center colspan=2><input type=submit value=�T�w�ק惡�ЫǸ��></td></tr>
</table><br>
<hr size=3 width=50%>
</form>
";
}

######### sub function HTML_Ends Starts Here #########
sub HTML_Ends 
{
  print qq( 
    <br>
    <form method=post action="../su.cgi" target=_top>
      <input type=hidden name=password value=$Input{password}>
      <input type=submit value=�^��޲z�D���>
    </form>
    </center>
    </body>
    </html>
  );
}

######### sub function HTML_Part3 Starts Here #########
sub HTML_Part3
{
 %classroom = Read_Classroom( $Input{id} );
 
  print "
<body background=$GRAPH_URL"."bg98.jpg>
<center>

<table border=0>
<tr><td><img src=$GRAPH_URL"."ccu.gif><td>
<th><h1>�R���ЫǸ��</h1></th><td><img src=$GRAPH_URL"."ccu.gif></td>
</tr></table>

<hr size=3 width=50%>

<form method=post action=Edit_Classroom3.cgi>
<input type=hidden name=function value=delete>
<input type=hidden name=id value=$classroom{id}>
<input type=hidden name=cname value=$classroom{cname}>
<table border=3 height=35%>
<tr><th>�ЫǥN�X</th><th>$classroom{id}</th></tr>
<tr><th>�ЫǦW��</th><th>$classroom{cname}</th></tr>
<tr><td align=center colspan=2><input type=submit value=�T�w�R�����ЫǸ��></td></tr>
</table><br>
<hr size=3 width=50%>
</form>
";
}