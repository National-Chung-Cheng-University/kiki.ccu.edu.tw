#!/usr/local/bin/perl

####    require these .pm modual    ####
require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
########################################

######### Main Program Here #########
my(%Input);
%Input=User_Input();



  $StateMap[0]="系統不限修";
  $StateMap[1]="考慮保留人數";
  $StateMap[2]="僅考慮限修人數";
  $DATA="";

Modify_Sys_State();
$state=Catch_Sys_State();
$DATA=Creat_Table_DATA($state);
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
<font size=5 color=#777777> 學生選課系統狀態設定</font>
<hr size=1>

<table border=1 width=640>
<tr>
  <th bgcolor=#00ffff><font color=blue>系統狀態</font></th>
  <th bgcolor=#00ffff><font color=blue>說明</font></th>
</tr>
$DATA
</table>
<br>
<hr size=1>
<a href="javascript:history.back()">回上一頁</a>
</center>
</body>
</html>
End_of_HTML
}

################################################

sub Modify_Sys_State
{
  my($FileName)=$REFERENCE_PATH."Basic/LimitNumberState";

  open(STATE,">$FileName");
    print STATE $Input{State};
  close(STATE);
}

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

sub Creat_Table_DATA
{
  my($S)=@_;
  $TD="";

  if($S == 0){

  $TD .= "<tr>\n";
  $TD .= "  <th align=left>".$StateMap[$S]."</th>\n";
  $TD .= "  <td>\n";
  $TD .= "    <ul>\n";
  $TD .= "      <li><font color=blue>可加選人數：</font><font color=#dd2222>不限制人數</font>\n";
  $TD .= "      <li><font color=blue>使用時機：</font><font color=#dd2222>舊生初選截止前</font>\n";
  $TD .= "    </ul>\n";
  $TD .= "  </td>\n";
  $TD .= "</tr>\n";

  }elsif($S == 1){

  $TD .= "<tr>\n";
  $TD .= "  <th align=left>".$StateMap[$S]."</th>\n";
  $TD .= "  <td>\n";
  $TD .= "    <ul>\n";
  $TD .= "      <li><font color=blue>可加選人數：</font><font color=#dd2222>限修人數-保留人數</font>\n";
  $TD .= "      <li><font color=blue>使用時機：</font><font color=#dd2222>舊生初選截止至新生初選前</font>\n";
  $TD .= "    </ul>\n";
  $TD .= "  </td>\n";
  $TD .= "</tr>\n";


  }elsif($S == 2){

  $TD .= "<tr>\n";
  $TD .= "  <th align=left>".$StateMap[$S]."</th>\n";
  $TD .= "  <td>\n";
  $TD .= "    <ul>\n";
  $TD .= "      <li><font color=blue>可加選人數：</font><font color=#dd2222>限修人數</font>\n";
  $TD .= "      <li><font color=blue>使用時機：</font><font color=#dd2222>新生初選截止後</font>\n";
  $TD .= "    </ul>\n";
  $TD .= "  </td>\n";
  $TD .= "</tr>\n";
  }
  return($TD);
}
