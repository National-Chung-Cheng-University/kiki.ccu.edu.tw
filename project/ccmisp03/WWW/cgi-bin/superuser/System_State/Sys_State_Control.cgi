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
<font size=5 color=#777777> �ǥͿ�Ҩt�Ϊ��A�]�w</font>
<hr size=1>
<form name="SelectionStateForm" action="Sys_State_Control01.cgi" method=post>

<table border=1 width=640>
<tr>
  <th bgcolor=#00ffff><font color=blue>�t�Ϊ��A</font></th>
  <th bgcolor=#00ffff><font color=blue>����</font></th>
</tr>
<tr>
  <th align=left>
  <input type=radio name=State value=0>�t������<br>
  </th>
  <td>
    <ul>
      <li>�t�Χ��������A<font color=#ff079f>�ϥΪ��v���̧C</font>
      <li>�L�k�d�ߡA�L�k�[�h��
    </ul>
  </td>
</tr>
<tr>
  <th align=left>
  <input type=radio name=State value=1>�ȨѬd��<br>
  </th>
  <td>
    <ul>
      <li>�t�ζȳ����}��A<font color=#ff079f>�ϥΪ��v������</font>
      <li>�Ҧ��ϥΪ̶Ȩ�Ƭd�ߤ���O
    </ul>
  </td>
</tr>
<tr>
  <th align=left>
  <input type=radio name=State value=2>�}��[�h��<br>
  </th>
  <td>
    <ul>
      <li>�t�Υ��ƶ}��A<font color=#ff079f>�ϥΪ��v���̰�</font>
      <li>�ϥΪ̥i�H�[��B�h��ҵ{�A�d�߿�Ҹ��
      <li>�Y�ϥΪ̶i�J���ɬq���~�A�N�u��i���ҵ��G���d��
      <li>��Үɬq���]�w�A�ЧQ��<font color=#cc076f>��Үɵ{�]�w�t��</font>
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



