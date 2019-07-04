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


my($DATA)=DEPT_TABLE();
CREAT_HTML($DATA);


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
<script language="javascript">
function OpenAll(FormObj)
{
  for(i=0; i < FormObj.length; i++){
    if(i > 0){
      if(i%2 != 0){
        FormObj.elements[i].checked=true;
      }
    }
  }
}

function CloseAll(FormObj)
{
  for(i=0; i < FormObj.length; i++){
    if(i > 0){
      if(i%2 == 0){
        FormObj.elements[i].checked=true;
      }
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
<font size=5 color=#777777>系所開排課時程設定</font>
<hr size=1>
<form name="ControlForm" action="Open_Course_Control01.cgi" method=post>

<table border=0 width=800>
<tr>
    <th align=left width=500>
<input type=button value="預設為全部關閉" onClick=CloseAll(document.ControlForm)>
<input type=reset value="重置">
<input type=button value="預設為全部開啟" onClick=OpenAll(document.ControlForm)>
    </th>
  <th align=right width=300>
  <input type=button value="確定送出選單" onClick="Check(document.ControlForm)">
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
    my($Dept1,$Dept2,$Dept3,$Dept4,$Dept5,$Dept6,$Dep7,$Dept0)="";

    $DATA = $DATA . "<table width=800 border=0>\n";
    $DATA = $DATA . "   <tr><th bgcolor=#99ffff width=133>工學院</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=133>理學院</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=134>管理學院</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=134>社會科學院</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=133>文學院</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=133>法學院</th>\n"; 
    $DATA = $DATA . "       <th bgcolor=#99ffff width=133>通識中心</th>\n"; 
    $DATA = $DATA . "       <th bgcolor=#99ffff width=133>共同科</th></tr>\n";

    $DATA = $DATA . "   <tr><th align=left><font color=red size=2>關</font>/<font color=blue size=2>開</font></th>";
    $DATA = $DATA . "   <th align=left><font color=red size=2>關</font>/<font color=blue size=2>開</font></th>";
    $DATA = $DATA . "   <th align=left><font color=red size=2>關</font>/<font color=blue size=2>開</font></th>";
    $DATA = $DATA . "   <th align=left><font color=red size=2>關</font>/<font color=blue size=2>開</font></th>"; 
    $DATA = $DATA . "   <th align=left><font color=red size=2>關</font>/<font color=blue size=2>開</font></th>"; 
    $DATA = $DATA . "   <th align=left><font color=red size=2>關</font>/<font color=blue size=2>開</font></th>";
    $DATA = $DATA . "   <th align=left><font color=red size=2>關</font>/<font color=blue size=2>開</font></th>";
    $DATA = $DATA . "   <th align=left><font color=red size=2>關</font>/<font color=blue size=2>開</font></th>";
    $DATA = $DATA . "</tr>\n";

#    $Dept0=$Dept0."<input type=radio name=\"I000\" value=\"0\">";
#    $Dept0=$Dept0."<input type=radio name=\"I000\" value=\"1\">";
#    $Dept0=$Dept0."<font size=3>"."共同科</font><br>\n";

    foreach $dept(@Dept){
      %Dept=Read_Dept($dept);
      $Dept{college} = "0"  if( $Dept{college} eq "I" );
      $text = "";
      
      $text = $text . "<input type=radio name=\"".$Dept{id}."\" value=\"0\">";
      $text = $text . "<input type=radio name=\"".$Dept{id}."\" value=\"1\">";
      $text = $text . "<font size=3>".$Dept{cname2}."</font><br>\n";

      $Dept_text[$Dept{college}] .= $text;
#      print("Dept[$Dept{college}] = $Dept[$Dept{college}]<BR>\n");      
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

