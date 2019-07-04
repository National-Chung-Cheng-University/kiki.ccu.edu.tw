#!/usr/local/bin/perl 

####    require these .pm modual    ####
require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
########################################

######### Main Program Here #########
print("Content-type:text/html\n\n");
my(%Input);
%Input=User_Input();

#
#  Check Password
#

WRITE_MAP();
my($DATA)=VIEW_MAP_RESULT();
CREAT_HTML($DATA);

######## Sub Program Bellow ##########
######################################
sub CREAT_HTML
{
my($DATA)=@_;
print << "End_of_HTML"
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <title>系所開排課時程管理</title>
<style>
        <!--
        A  {
           text-decoration: none;
           color:#0070A6
        }
        -->
</style>
</head>
<body bgcolor=white text=#666666>
<center>
<font size=5 color=#777777>系所開排課時程設定結果</font>
<hr size=1>
$DATA
<hr size=1>
<table border=0 width=800>
<tr>
  <th align=left width=40>
<font size=3 color=#aa5555>說明</font><br>
  </th>
</tr>
  <th>&nbsp</th>
  <th width=760 align=left>
  <font size=3>
  <ol>
    <li>以上為目前各系所開排課的狀態。"開啟"表示目前該系所可以使用開排課系統；
        "關閉"表示目前該系所無法使用開排課系統。
    <li>如果您覺得這樣的設定不滿意，可以<a href=javascript:history.back()>回到上一頁</a>，重新使用系所開排課時程設定"。
    <li>或者您也可以選擇回到開排選課管理系統。
  </ol>
  </font>
  </th>
</table>
</center>
</body>
</html>
End_of_HTML
}
#######################################
sub WRITE_MAP
{
    my(@Dept)=Find_All_Dept();
    my($FileName)=$REFERENCE_PATH."Dept_Control.map";

    open(FILE,">$FileName") 
                        or die("Cannot open file $FileName!\n");
    foreach $dept(@Dept){
        print FILE << "End_of_Print_to_File"
$dept \t $Input{$dept}
End_of_Print_to_File
    }
}
################################################
sub VIEW_MAP_RESULT
{
    my(@Dept)=Find_All_Dept();
    my($DATA)="";
    my($Dept1,$Dept2,$Dept3,$Dept4,$Dept5,$Dept6,$Dept7,$Dept0)="";
    my($FileName)=$REFERENCE_PATH."Dept_Control.map";
    open(FILE,"<$FileName")
                     or die("Cannot open file $FileName!\n");
    my(@MAP)=<FILE>;
    close(FILE);

    foreach $map(@MAP){
        $map=~s/\n//;
        ($dept,$state)=split(/\s+/,$map);
        $DeptMap{$dept}=$state;
    }

    $DATA = $DATA . "<table width=800 border=0>\n";
    $DATA = $DATA . "   <tr><th bgcolor=#99ffff width=133>工學院</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=133>理學院</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=134>管理學院</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=134>社會科學院</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=133>文學院</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=133>法學院</th>\n";  
    $DATA = $DATA . "       <th bgcolor=#99ffff width=133>通識中心</th>\n";  

    $DATA = $DATA . "       <th bgcolor=#99ffff width=133>共同科</th></tr>\n";

    foreach $dept(@Dept){
      %Dept=Read_Dept($dept);
      $Dept{college} = "0"  if( $Dept{college} eq "I" );
#      $flag = ($DeptMap{$Dept{id}}==1) ? "開啟" : "關閉";
      if($DeptMap{$Dept{id}}==1) {
        $flag = "<FONT color=RED size=2>開啟</FONT>";
      }else{
        $flag = "<FONT color=BLUE size=2>關閉</FONT>";
      }
      $text = "<font color=blue size=2>$flag</font>";
      $text = $text . "<font size=3>".$Dept{cname2}."</font><br>\n";

      $Dept_text[$Dept{college}] .= $text;
    }

    $DATA = $DATA ."<tr>\n";
    $DATA = $DATA ."    <td valign=top>".$Dept_text[4]."</td>\n";
    $DATA = $DATA ."    <td valign=top>".$Dept_text[2]."</td>\n";
    $DATA = $DATA ."    <td valign=top>".$Dept_text[5]."</td>\n";
    $DATA = $DATA ."    <td valign=top>".$Dept_text[3]."</td>\n";
    $DATA = $DATA ."    <td valign=top>".$Dept_text[1]."</td>\n";
    $DATA = $DATA ."    <td valign=top>".$Dept_text[6]."</td>\n";   
    $DATA = $DATA ."    <td valign=top>".$Dept_text[7]."</td>\n";   
    $DATA = $DATA ."    <td valign=top>".$Dept_text[0]."</td>\n";
    $DATA = $DATA ."</tr>\n";
    $DATA = $DATA . "   </table>\n";

    return($DATA);
}

