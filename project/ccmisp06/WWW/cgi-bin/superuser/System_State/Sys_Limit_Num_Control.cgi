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
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title> 是否限制修課人數設定網頁 </title>

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
<font size=5 color=#777777> 限修人數控管機制設定頁</font>
<hr size=1>
<form name="SelectionStateForm" action="Sys_Limit_Num_Control01.cgi" method=post>

<table border=1 width=640>
<tr>
  <th bgcolor=#00ffff width=200><font color=blue>系統狀態</font></th>
  <th bgcolor=#00ffff><font color=blue>說明</font></th>
</tr>
<tr>
  <th align=left>
  <input type=radio name=State value=0 $state[0]>系統不限修<br>
  </th>
  <td>
    <ul>
      <li><font color=blue>可加選人數：</font><font color=#dd2222>不限制人數</font>
      <li><font color=blue>使用時機：</font><font color=#dd2222>舊生初選截止前</font>
    </ul>
  </td>
</tr>
<tr>
  <th align=left>
  <input type=radio name=State value=1 $state[1]>考慮保留人數<br>
  </th>
  <td>
    <ul>
      <li><font color=blue>可加選人數：</font><font color=#dd2222>限修人數-保留人數</font>
      <li><font color=blue>使用時機：</font><font color=#dd2222>舊生初選截止至新生初選前</font>
    </ul>
  </td>
</tr>
<tr>
  <th align=left>
  <input type=radio name=State value=2 $state[2]>僅考慮限修人數<br>
  </th>
  <td>
    <ul>
      <li><font color=blue>可加選人數：</font><font color=#dd2222>限修人數</font>
      <li><font color=blue>使用時機：</font><font color=#dd2222>新生初選截止後</font>
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
