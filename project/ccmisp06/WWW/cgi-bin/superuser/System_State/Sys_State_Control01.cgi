#!/usr/local/bin/perl

####    require these .pm modual    ####
require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
########################################

######### Main Program Here #########
my(%Input);
%Input=User_Input();



  $StateMap[0]="系統關閉";
  $StateMap[1]="僅供查詢";
  $StateMap[2]="開放加退選";
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

<FONT color=RED><BLINK>重要:</BLINK>
請務必確定限修人數及升級與否設定, 否則會有大災難!<br></FONT>
<FONT size=2>Feb21,2000李永祥^^;</FONT>

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
  my($FileName)=$REFERENCE_PATH."Basic/SysState";

  open(STATE,">$FileName");
    print STATE $Input{State};
  close(STATE);
}

sub Catch_Sys_State
{
  my($FileName)=$REFERENCE_PATH."Basic/SysState";
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
  $TD .= "  <th align=left> 系統關閉 </th>\n";
  $TD .= "  <td>\n";
  $TD .= "    <ul>\n";
  $TD .= "      <li>系統完全關閉，<font color=#ff079f>使用者權限最低</font>\n";
  $TD .= "      <li>無法查詢，無法加退選\n";
  $TD .= "    </ul>\n";
  $TD .= "  </td>\n";
  $TD .= "</tr>\n";

  }elsif($S == 1){

  $TD .= "<tr>\n";
  $TD .= "  <th align=left> 僅供查詢 </th>\n";
  $TD .= "  <td>\n";
  $TD .= "    <ul>\n";
  $TD .= "      <li>系統僅部分開放，<font color=#ff079f>使用者權限中等</font>\n";
  $TD .= "      <li>所有使用者僅具備查詢之能力\n";
  $TD .= "    </ul>\n";
  $TD .= "  </td>\n";
  $TD .= "</tr>\n";


  }elsif($S == 2){

  $TD .= "<tr>\n";
  $TD .= "  <th align=left> 開放加退選 </th>\n";
  $TD .= "  <td>\n";
  $TD .= "    <ul>\n";
  $TD .= "      <li>系統全數開放，<font color=#ff079f>使用者權限最高</font>\n";
  $TD .= "      <li>使用者可以加選、退選課程，查詢選課資料\n";
  $TD .= "      <li>若使用者進入的時段錯誤，將只能進行選課結果的查詢\n";
  $TD .= "      <li>選課時段的設定，請利用<font color=#cc076f>選課時程設定系統</font>\n";
  $TD .= "    </ul>\n";
  $TD .= "  </td>\n";
  $TD .= "</tr>\n";
  }
  return($TD);
}
