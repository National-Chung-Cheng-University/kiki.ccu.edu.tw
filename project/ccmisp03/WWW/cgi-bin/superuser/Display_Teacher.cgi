#!/usr/local/bin/perl

######### require .pm files #########
require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Teacher.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";

######### Main Program Starts Here #########
my(%Input,@DEPT,$Number_Of_Teacher);

### Read data in ###
%Input = User_Input();
@DEPT = Find_All_Dept();
if( $Input{Teacher_Dept} eq "" ) { $Input{Teacher_Dept} = $DEPT[0]; }
@Teacher = Read_Teacher_File();

$Number_Of_Teacher = Count_Teacher($Input{Teacher_Dept});

HTML_Head("");  # print HTML header

HTML_Part1($Input{Teacher_Dept});

if($Number_Of_Teacher > 0) # this is not a Dept. with no teacher
{
 HTML_With_Teacher($Input{Teacher_Dept}); 
}
else # no teachers in this Dept. 
{
 HTML_No_Teacher();
}

HTML_End();  # print HTML endings 
######### Main Program Ends Here #########

######### sub function HTML_Head Ends Here #########
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

######### sub function Count_Teacher #########
sub Count_Teacher
{
 my($count,$teacher,$dept);
 ($dept)=@_;
 $count=0;
 foreach $teacher(@Teacher)
 {
  if( $Teacher_Dept{$teacher} eq $dept )
  { $count++ }
 }
 return $count;
}

######### sub function HTML_Part1 Starts Here #########
sub HTML_Part1
{
 my(%dept,$Dept);
 ($Dept)=@_;
 %dept=Read_Dept($Dept);
 print "
 <body background=$GRAPH_URL"."bg98.jpg>
 <center>

<table border=0>
<tr><td><img src=$GRAPH_URL"."ccu.gif><td>
<th><h1>$dept{cname2} �Юv�򥻸��</h1></th>
<td><img src=$GRAPH_URL"."ccu.gif></td>
</tr></table>
<hr size=3 width=50%>";
}

######### sub function HTML_No_Teacher Starts Here #########
sub HTML_No_Teacher
{
 print "<font color=red size=4><p>���t�ҨS���Юv��ƥi�ѭק�ΧR��</font><p>";
 print "<hr size=3 width=50%>"; 
}

######### sub function HTML_With_Teacher Starts Here #########
sub HTML_With_Teacher
{
 my($Dept);
 ($Dept)=@_;
 HTML_Part2();
 HTML_Options($Dept);
 HTML_Part3();
}

######### sub function HTML_Part2 Starts Here #########
sub HTML_Part2
{
 print "
 <form method=post action=Edit_Teacher.cgi>
 <table border=0 height=50%>
 <caption><font color=brown>�п�ܱ��ק�ΧR�����Юv</font></caption>
 <tr><td align=center>
   <select name=Teacher_Code>";
}

######### sub function HTML_Options Starts Here #########
sub HTML_Options
{
 my($teacher,$Dept);
 ($Dept)=@_;
 foreach $teacher(@Teacher)
 {
  if( $Teacher_Dept{$teacher} eq $Dept )
  {
   print "<option value=$teacher>[$teacher]$Teacher_Name{$teacher}\n";
  }
 }
}
######### sub function HTML_Part3 Starts Here #########
sub HTML_Part3
{
  print "
   </select></td>
 </tr>
<tr><th><font color=brown>�п�ܭק�ΧR���Юv���</font></th></tr>
<tr><th><select name=function size=2>
<option value=edit selected>�ק�Юv���
<option value=delete>�R���Юv���
</select></th></tr> 
 </table>
 <input type=submit value=�e�X���>
 <hr size=3 width=50%>
 </form>";
}

######### sub function HTML_End Starts Here #########
sub HTML_End
{
 print "
<form method=post action=Teacher_Menu.cgi target=_top>
<input type=hidden name=password value=>
<input type=submit value=�^��Юv��ƺ޲z�D���>
</form>
</center>
</body>
</html>";
}