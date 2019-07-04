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
<font size=5 color=#777777> 學生選課系統狀態設定</font>
<hr size=1>
<form name="SelectionStateForm" action="Sys_State_Control01.cgi" method=post>

<table border=1 width=640>
<tr>
  <th bgcolor=#00ffff><font color=blue>系統狀態</font></th>
  <th bgcolor=#00ffff><font color=blue>說明</font></th>
</tr>
<tr>
  <th align=left>
  <input type=radio name=State value=0>系統關閉<br>
  </th>
  <td>
    <ul>
      <li>系統完全關閉，<font color=#ff079f>使用者權限最低</font>
      <li>無法查詢，無法加退選
    </ul>
  </td>
</tr>
<tr>
  <th align=left>
  <input type=radio name=State value=1>僅供查詢<br>
  </th>
  <td>
    <ul>
      <li>系統僅部分開放，<font color=#ff079f>使用者權限中等</font>
      <li>所有使用者僅具備查詢之能力
    </ul>
  </td>
</tr>
<tr>
  <th align=left>
  <input type=radio name=State value=2>開放加退選<br>
  </th>
  <td>
    <ul>
      <li>系統全數開放，<font color=#ff079f>使用者權限最高</font>
      <li>使用者可以加選、退選課程，查詢選課資料
      <li>若使用者進入的時段錯誤，將只能進行選課結果的查詢
      <li>選課時段的設定，請利用<font color=#cc076f>選課時程設定系統</font>
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



