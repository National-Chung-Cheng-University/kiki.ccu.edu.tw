#!/usr/local/bin/perl

####    require these .pm modual    ####
require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
########################################

######### Main Program Here #########
my(%Input);
%Input=User_Input();


$DATA=GREAD_SELECT();
$DATA=$DATA."<HR SIZE=1 WIDTH=740>";
$DATA=$DATA.DEPT_TABLE();
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
    <title> �ǥͿ�Үɵ{ </title>

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
<font size=5 color=#777777> �ǥͿ�Үɵ{�]�w</font>
<hr size=1>
<form name="DeptForm" action="Select_Class_Control01.cgi" method=post>

<table border=0 width=800>
<tr>
  <th>
  <input type=button value="����" onClick="CheckGrade(document.DeptForm)">
  <input type=button value="���m" onClick="reset()">
  </th>
  <th align=right width=300>
  <input type=button value="�]�w�Q����t�ҾǥͿ�Үɬq   (Step 1/N)" onClick="Check(document.DeptForm)">
  </th>
</tr>
</table>

$DATA
</form>
<hr size=1>
<a href="javascript:history.back()">�^�W�@��</a>
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

    $DATA = $DATA . "<table width=800 border=0>\n";
    $DATA = $DATA . "   <tr><th bgcolor=#99ffff width=135><font size=2>�u�ǰ|</font></th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=135><font size=2>�z�ǰ|</font></th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=135><font size=2>�޲z�ǰ|</font></th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=135><font size=2>���|��ǰ|</font></th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=135><font size=2>��ǰ|</font></th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=135><font size=2>�k�ǰ|</font></th>\n";    
    $DATA = $DATA . "       <th bgcolor=#99ffff width=135><font size=2>�q�Ѥ���</font></th>\n";    
    $DATA = $DATA . "       <th bgcolor=#99ffff width=135><font size=2>�@�P��</font></th></tr>\n";

    $Dept0=$Dept0."<input type=checkbox name=dept value=\"I000\">";
    $Dept0=$Dept0."<font size=2>"."�@�P��</font><br>\n";


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

    $Grade_Select=$Grade_Select."<table width=800 border=0>\n";
    $Grade_Select=$Grade_Select."<tr bgcolor=#dddddd>\n";
    $Grade_Select=$Grade_Select." <td><input type=\"radio\" name=grade value=1 checked onClick=\"ClearDept(document.DeptForm)\"><font size=2>�j�@</font></td>\n";
    $Grade_Select=$Grade_Select." <td><input type=\"radio\" name=grade value=2 onClick=\"ClearDept(document.DeptForm)\"><font size=2>�j�G</font></td>\n";
    $Grade_Select=$Grade_Select." <td><input type=\"radio\" name=grade value=3 onClick=\"ClearDept(document.DeptForm)\"><font size=2>�j�T</font></td>\n";
    $Grade_Select=$Grade_Select." <td><input type=\"radio\" name=grade value=4 onClick=\"ClearDept(document.DeptForm)\"><font size=2>�j�|</font></td>\n";
    $Grade_Select=$Grade_Select." <td><input type=\"radio\" name=grade value=5 onClick=\"ClearDept(document.DeptForm)\"><font size=2>��s�Ҥ@�~��</font></td>\n";
    $Grade_Select=$Grade_Select." <td><input type=\"radio\" name=grade value=6 onClick=\"ClearDept(document.DeptForm)\"><font size=2>��s�ҤG�~�ŧt�դh�Z</font></td>\n";
    $Grade_Select=$Grade_Select."</tr>\n";
    $Grade_Select=$Grade_Select."</table>\n";

    return($Grade_Select);
}

