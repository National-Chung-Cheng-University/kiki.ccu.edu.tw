#!/usr/local/bin/perl

####    require these .pm modual    ####
require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
########################################

######### Main Program Here #########
my(%Input);
%Input=User_Input();

$DATA="";

CREAT_HTML($DATA);

######################################
sub CREAT_HTML
{
my($DATA)=@_;
print << "End_of_HTML"
Content-type: text/html


<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <title> ��Ҩt�Ϊ��A�]�w�� </title>

<style>
        <!--
        A  {
           text-decoration: none;
           color:#0070A6
        }
        -->
</style>
</script>
</head>
<body bgcolor=white text=#666666>
<center>
<font size=5 color=#777777> �ǥͦ~�ŤɯŻP�_�]�w����</font>
<hr size=1>
<form name="SelectionStateForm" action="Grade_Update01.cgi" method=post>

<table border=1 width=640>
<tr>
  <th bgcolor=#00ffff><font color=blue>�]�w���A</font></th>
  <th bgcolor=#00ffff><font color=blue>����</font></th>
</tr>
<tr>
  <th align=left>
  <input type=radio name=State value=1>�]�w<font color=#ff0000>�}��</font><br>
  </th>
  <td>
    <ul>
      <li>�]�w�}�ҡA�Ҧ��ϥΪ̦~��<font color=#ff079f>�۰ʤɯ�</font>
      <li>��s�Ǧ~�}�l�e�ϥΡA�ت��b���¥ͦ~�Ŧ۰ʤɯšC
    </ul>
  </td>
</tr>
<tr>
  <th align=left>
  <input type=radio name=State value=0 checked>�]�w<font color=black>����</font><br>
  </th>
  <td>
    <ul>
      <li>�]�w�����A�Ҧ��ϥΪ̦~��<font color=#ff079f>�Ҥ��ɯ�</font>
      <li>�ݤJ�Ƿs�͡A�¥ͦ~�ŧ�s�����ᥲ���N���]�w�����C
    </ul>
  </td>
</tr>

</table>
<br>
<input type=submit value="�T�{�e�X">
<input type=reset value="�M�����g">
</form>
<hr size=1>
<a href="javascript:history.back()">�^�W�@��</a>
</center>
</body>
</html>
End_of_HTML
}
################################################


