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
$sys_state = Catch_Sys_State();
$state[$sys_state] = "checked";

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
    <title> �O�_����׽ҤH�Ƴ]�w���� </title>

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
<font size=5 color=#777777> ���פH�Ʊ��޾���]�w��</font>
<hr size=1>
<form name="SelectionStateForm" action="Sys_Limit_Num_Control01.cgi" method=post>

<table border=1 width=640>
<tr>
  <th bgcolor=#00ffff width=200><font color=blue>�t�Ϊ��A</font></th>
  <th bgcolor=#00ffff><font color=blue>����</font></th>
</tr>
<tr>
  <th align=left>
  <input type=radio name=State value=0 $state[0]>�t�Τ�����<br>
  </th>
  <td>
    <ul>
      <li><font color=blue>�i�[��H�ơG</font><font color=#dd2222>������H��</font>
      <li><font color=blue>�ϥήɾ��G</font><font color=#dd2222>�¥ͪ��I��e</font>
    </ul>
  </td>
</tr>
<tr>
  <th align=left>
  <input type=radio name=State value=1 $state[1]>�Ҽ{�O�d�H��<br>
  </th>
  <td>
    <ul>
      <li><font color=blue>�i�[��H�ơG</font><font color=#dd2222>���פH��-�O�d�H��</font>
      <li><font color=blue>�ϥήɾ��G</font><font color=#dd2222>�¥ͪ��I��ܷs�ͪ��e</font>
    </ul>
  </td>
</tr>
<tr>
  <th align=left>
  <input type=radio name=State value=2 $state[2]>�ȦҼ{���פH��<br>
  </th>
  <td>
    <ul>
      <li><font color=blue>�i�[��H�ơG</font><font color=#dd2222>���פH��</font>
      <li><font color=blue>�ϥήɾ��G</font><font color=#dd2222>�s�ͪ��I���</font>
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

sub Catch_Sys_State
{
  my($FileName)=$REFERENCE_PATH."Basic/LimitNumberState";
  my(@data)="";
  my(@StateMap);


  if(-e $FileName){
    open(STATE,"<$FileName");
      @data=<STATE>;
    close(STATE);
  }else{
    die("Couldn't open the file $FileName!\n");
  }

  return($data[0]);
}
