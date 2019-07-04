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
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title> 選課系統狀態設定頁 </title>

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
<font size=5 color=#777777> 學生年級升級與否設定網頁</font>
<hr size=1>
<form name="SelectionStateForm" action="Grade_Update01.cgi" method=post>

<table border=1 width=640>
<tr>
  <th bgcolor=#00ffff><font color=blue>設定狀態</font></th>
  <th bgcolor=#00ffff><font color=blue>說明</font></th>
</tr>
<tr>
  <th align=left>
  <input type=radio name=State value=1>設定<font color=#ff0000>開啟</font><br>
  </th>
  <td>
    <ul>
      <li>設定開啟，所有使用者年級<font color=#ff079f>自動升級</font>
      <li>於新學年開始前使用，目的在使舊生年級自動升級。
    </ul>
  </td>
</tr>
<tr>
  <th align=left>
  <input type=radio name=State value=0 checked>設定<font color=black>關閉</font><br>
  </th>
  <td>
    <ul>
      <li>設定關閉，所有使用者年級<font color=#ff079f>皆不升級</font>
      <li>待入學新生，舊生年級更新完畢後必須將此設定關閉。
    </ul>
  </td>
</tr>

</table>
<br>
<input type=submit value="確認送出">
<input type=reset value="清除重寫">
</form>
<hr size=1>
<a href="javascript:history.back()">回上一頁</a>
</center>
</body>
</html>
End_of_HTML
}
################################################


