#!/usr/local/bin/perl

###################################################################################################################
#####  Select_Class_Control.cgi
#####  學生選課時程設定 (step 1/3)
#####  顯示年級與系所供選擇，以設定該系所該年級是否可選課
#####  Updates:
#####    199?/??/??  Created
#####    2009/09/08  為避免管理者疏忽，在此頁的年級欄上方顯示該年級可選課的系所數量  Nidalap :D~ 

print("Content-type: text/html\n\n");

require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Select_Course.pm";

$t_size		= "90%";					###  TABLE size(相對應於視窗)
$width		= "11%";					###  TABLE cell width(相對應於 table)

my(%Input);
%Input=User_Input();
%time_map = Read_Time_Map();					###  讀取各年級系所開課設定

foreach $grade (sort keys %time_map) {				###  統計各年級有幾個系所開放
  foreach $dept (keys %{$time_map{$grade}}) {
    if( $time_map{$grade}{$dept} != 0 ) {
      $time_map_count{$grade}++;
    }else{
      $time_map_count{$grade}+=0;
    }
  }
}

$DATA=GREAD_SELECT();
$DATA=$DATA."<HR SIZE=1 WIDTH=7400>";
$DATA=$DATA.DEPT_TABLE();
CREAT_HTML($DATA);


######################################
sub CREAT_HTML
{
my($DATA)=@_;
print << "End_of_HTML"
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title> 學生選課時程 </title>

<style>
        <!--
        A  {
           text-decoration: none;
           color:#0070A6
        }
        -->
</style>
<script language="javascript">
function SelectAll(FormObj)
{
  for(i=0; i < FormObj.length; i++){
    if(i > 0){
      if(FormObj.elements[i].name=="dept"){
        FormObj.elements[i].checked=true;
      }
    }
  }
}

function CheckGrade(FormObj)
{
  var Grade=0;
  for(i=0; i < FormObj.length; i++){
    if(FormObj.elements[i].name=="grade"){
      if(FormObj.elements[i].checked){
        Grade=FormObj.elements[i].value;
      }
    }
  }
  for(i=0; i < FormObj.length; i++){
    if(i > 0){
      if(FormObj.elements[i].name=="dept"){
        if(Grade <= 4){
          if(FormObj.elements[i].value%10 <= 4){
            FormObj.elements[i].checked=true;
          }else{
            FormObj.elements[i].checked=false;
          }
        }else{
          if(FormObj.elements[i].value%10 > 4){
            FormObj.elements[i].checked=true;
          }else{
            FormObj.elements[i].checked=false;
          }
        }
      }
    }
  }
}

function ClearDept(FormObj)
{
  for(i=0; i < FormObj.length; i++){
    if(FormObj.elements[i].name=="dept"){
      FormObj.elements[i].checked=false;
    }
  }
}

function Check(FormObj)
{
  FormObj.submit();
}
</script>
</head>

<body bgcolor=white text=#666666>
<center>
<font size=5 color=#777777> 學生選課時程設定</font>
<hr size=1>
<form name="DeptForm" action="Select_Class_Control01.cgi" method=post>

<table border=0 width=800>
<tr>
  <th>
  <input type=button value="全選" onClick="CheckGrade(document.DeptForm)">
  <input type=button value="重置" onClick="reset()">
  </th>
  <th align=right width=300>
  <input type=button value="設定被選取系所學生選課時段   (Step 1/N)" onClick="Check(document.DeptForm)">
  </th>
</tr>
</table>

$DATA
</form>
<hr size=1>
<a href="javascript:history.back()">回上一頁</a>
</center>
</body>
</html>
End_of_HTML
}

################################################
sub DEPT_TABLE
{
    my(@Dept)=Find_All_Dept();
    my($DATA)="";
    my($Dept1,$Dept2,$Dept3,$Dept4,$Dept5,$Dept6,$Dept7,$Dept0)="";

    $DATA = $DATA . "<table width=$t_size border=0>\n";
    $DATA = $DATA . "   <tr><th bgcolor=#99ffff width=$width><font size=2>工學院</font></th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=$width><font size=2>理學院</font></th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=$width><font size=2>管理學院</font></th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=$width><font size=2>社會科學院</font></th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=$width><font size=2>文學院</font></th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=$width><font size=2>法學院</font></th>\n";    
    $DATA = $DATA . "       <th bgcolor=#99ffff width=$width><font size=2>通識中心</font></th>\n";    
    $DATA = $DATA . "       <th bgcolor=#99ffff width=$width><font size=2>共同科</font></th></tr>\n";

    $Dept0=$Dept0."<input type=checkbox name=dept value=\"I000\">";
    $Dept0=$Dept0."<font size=2>"."共同科</font><br>\n";


    foreach $dept(@Dept){
        %Dept=Read_Dept($dept);
        if($Dept{id} != "I000"){
          if($Dept{id}/1000 >= 7){
        $Dept7=$Dept7."<input type=checkbox name =dept value=\"".$Dept{id}."\">";
        $Dept7=$Dept7."<font size=2>".$Dept{cname2}."</font><br>\n";
          }
          elsif($Dept{id}/1000 >= 6){
        $Dept6=$Dept6."<input type=checkbox name=dept value=\"".$Dept{id}."\">";
        $Dept6=$Dept6."<font size=2>".$Dept{cname2}."</font><br>\n";
          } 
          elsif($Dept{id}/1000 >= 5){
        $Dept5=$Dept5."<input type=checkbox name=dept value=\"".$Dept{id}."\">";
        $Dept5=$Dept5."<font size=2>".$Dept{cname2}."</font><br>\n";
          } 
          elsif($Dept{id}/1000 >= 4){
        $Dept4=$Dept4."<input type=checkbox name=dept value=\"".$Dept{id}."\">";
        $Dept4=$Dept4."<font size=2>".$Dept{cname2}."</font><br>\n";
          }
          elsif($Dept{id}/1000 >= 3){
        $Dept3=$Dept3."<input type=checkbox name=dept value=\"".$Dept{id}."\">";
        $Dept3=$Dept3."<font size=2>".$Dept{cname2}."</font><br>\n";
          }
          elsif($Dept{id}/1000 >= 2){
        $Dept2=$Dept2."<input type=checkbox name=dept value=\"".$Dept{id}."\">";
        $Dept2=$Dept2."<font size=2>".$Dept{cname2}."</font><br>\n";
          }
          elsif($Dept{id}/1000 >= 1){
        $Dept1=$Dept1."<input type=checkbox name=dept value=\"".$Dept{id}."\">";
        $Dept1=$Dept1."<font size=2>".$Dept{cname2}."</font><br>\n";
          }
        }
    }

    $DATA = $DATA ."<tr>\n";
    $DATA = $DATA ."    <td valign=top>".$Dept4."</td>\n";
    $DATA = $DATA ."    <td valign=top>".$Dept2."</td>\n";
    $DATA = $DATA ."    <td valign=top>".$Dept5."</td>\n";
    $DATA = $DATA ."    <td valign=top>".$Dept3."</td>\n";
    $DATA = $DATA ."    <td valign=top>".$Dept1."</td>\n";
    $DATA = $DATA ."    <td valign=top>".$Dept6."</td>\n"; 
    $DATA = $DATA ."    <td valign=top>".$Dept7."</td>\n"; 
    $DATA = $DATA ."    <td valign=top>".$Dept0."</td>\n";
    $DATA = $DATA ."</tr>\n";
    $DATA = $DATA . "   </table>\n";

    return($DATA);
}
sub GREAD_SELECT
{
    my($Grade_Select)="";

    $Grade_Select=$Grade_Select."<table width=$t_size border=0>\n";
    $Grade_Select=$Grade_Select."<tr bgcolor=#dddddd>\n";
    
    $Grade_Select=$Grade_Select." <td><input type=\"radio\" name=grade value=1 checked onClick=\"ClearDept(document.DeptForm)\">
        <B><font size=>大一<FONT color=RED>($time_map_count{1}個系所開放)</font></B></td>\n";
    $Grade_Select=$Grade_Select." <td><input type=\"radio\" name=grade value=2 onClick=\"ClearDept(document.DeptForm)\">
        <B><font size=3>大二<FONT color=RED>($time_map_count{2}個系所開放)</font></B></td>\n";
    $Grade_Select=$Grade_Select." <td><input type=\"radio\" name=grade value=3 onClick=\"ClearDept(document.DeptForm)\">
        <B><font size=3>大三<FONT color=RED>($time_map_count{3}個系所開放)</font></B></td>\n";
    $Grade_Select=$Grade_Select." <td><input type=\"radio\" name=grade value=4 onClick=\"ClearDept(document.DeptForm)\">
        <B><font size=3>大四<FONT color=RED>($time_map_count{4}個系所開放)</font></B></td>\n";
    $Grade_Select=$Grade_Select." <td><input type=\"radio\" name=grade value=5 onClick=\"ClearDept(document.DeptForm)\">
        <B><font size=3>研究所一年級<FONT color=RED>($time_map_count{5}個系所開放)</font></B></td>\n";
    $Grade_Select=$Grade_Select." <td><input type=\"radio\" name=grade value=6 onClick=\"ClearDept(document.DeptForm)\">
        <B><font size=3>研究所二年級含博士班<FONT color=RED>($time_map_count{6}個系所開放)</font></B></td>\n";
    $Grade_Select=$Grade_Select."</tr>\n";
    $Grade_Select=$Grade_Select."</table>\n";

    return($Grade_Select);
}

