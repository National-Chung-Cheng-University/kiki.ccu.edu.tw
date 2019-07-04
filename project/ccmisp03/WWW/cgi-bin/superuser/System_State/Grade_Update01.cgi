#!/usr/local/bin/perl

####    require these .pm modual    ####
require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
########################################

######### Main Program Here #########
my(%Input);
%Input=User_Input();

  $StateMap[0]="設定<font color=black><b>關閉</b></font>";
  $StateMap[1]="設定<font color=red><b>開放</b></font>";
  $DATA="";

Modify_Grade_State();
$state=Catch_Grade_State();
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

sub Modify_Grade_State
{
  my($FileName)=$REFERENCE_PATH."Basic/GradeState";

  open(STATE,">$FileName");
    print STATE $Input{State};
  close(STATE);
}

sub Catch_Grade_State
{
  my($FileName)=$REFERENCE_PATH."Basic/GradeState";
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

  if($S eq 0){

  $TD .= "<tr>\n";
  $TD .= "  <td align=left> $StateMap[$S] </td>\n";
  $TD .= "  <td>\n";
  $TD .= "    <ul>\n";
  $TD .= "      <li>設定關閉，所有使用者年級<font color=#ff079f>皆不升級</font>\n";
  $TD .= "      <li>待入學新生，舊生年級更新完畢後必須將此設定關閉。\n";
  $TD .= "    </ul>\n";
  $TD .= "  </td>\n";
  $TD .= "</tr>\n";
  }elsif($S eq 1){

  $TD .= "<tr>\n";
  $TD .= "  <td align=left> $StateMap[$S] </td>\n";
  $TD .= "  <td>\n";
  $TD .= "    <ul>\n";
  $TD .= "      <li>設定開啟，所有使用者年級<font color=#ff079f>自動升級</font>\n";
  $TD .= "      <li>於新學年開始前使用，目的在使舊生年級自動升級。\n";
  $TD .= "    </ul>\n";
  $TD .= "  </td>\n";
  $TD .= "</tr>\n";
  }elsif($S eq 2){

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




