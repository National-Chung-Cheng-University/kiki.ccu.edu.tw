#!/usr/local/bin/perl
print "Content-type: text/html","\n\n";
### header of this cgi program ###
%display=&user_input;
$PATH="/ultra2/project/ccmisp01/WWW/data";
$URL="http://kiki.ccu.edu.tw:81/~ccmisp01";
$CGI="http://kiki.ccu.edu.tw:81/~ccmisp01/cgi-bin/project";
my($MaxGrp);
$MaxGrp=40;
########### End of Header ###########
## read user data from STDIN ##

$dept_cd=$display{'dept_cd'};
$grade=$display{'grade'};
$Cur_Cd=$display{'cur_cd'};
if($Cur_Cd ne "NEW")
{
($cur_cd,$new)=split(/ /,$Cur_Cd);
}
else
{
$cur_cd="NEW";
}
$grp=$display{'grp'};
print "
<html>
<head>
</head>

<body bgcolor=orange>
<center>
<form method=\"post\" action=\"$CGI/BottomTable.cgi\"
 target=\"bottomtable\">
";
#### trans the essential variables to next CGI ####
print "
<input type=\"hidden\" name=\"dept_cd\"
       value=\"$dept_cd\">
<input type=\"hidden\" name=\"grade\"
       value=\"$grade\">
<input type=\"hidden\" name=\"flag\"
       value=\"1\">
";
###################################################
print "
<table border=1 width=400>
<tr>
<th>科目名稱（中文）:</th>";
 
if($cur_cd eq "NEW")
### user selected a new course ###
 {
  print "<td>";
  print "<input type=\"hidden\" name=\"NEW\" 
          value=\"1\">";
  print "<input type=\"text\" name=\"cur_name_c\">";
  print "</td>"; 
 }
else
 {
### user selected an old course ####
  print "<th>";
  print "<input type=\"hidden\" name=\"NEW\" 
          value=\"0\">";
  print "<input type=\"hidden\" name=\"cur_cd\"
          value=\"$cur_cd\">";

## get course data from file ##
  if( (-e "$PATH/$dept_cd/course/temp/$cur_cd"."_$grp") ==0 )
  {
   $grp="01";
  }# if this grp doesnt exist,chang grp to 01
  if($new==0)
  {
  open(FILE,"<$PATH/$dept_cd/course/$cur_cd"."_$grp");
  }
  else
  {
  open(FILE,"<$PATH/$dept_cd/course/temp/$cur_cd"."_$grp");
  }
 $cur_name_c=<FILE>;
 chop($cur_name_c);
 $cur_name_e=<FILE>;
 chop($cur_name_e);
 $classtime=<FILE>;
 chop($classtime);
 $credit=<FILE>;
 chop($credit);
 $rm_cd=<FILE>;
 chop($rm_cd);
 $rm_name=<FILE>;
 chop($rm_name);
 $cura_cd=<FILE>;
 chop($cura_cd);
close(FILE);

## end of get course data from file ##

 print "$cur_name_c";
 print "</th>"; 
 print "<input type=\"hidden\" name=\"cur_name_c\" value=\"$cur_name_c\">";
 }
 print "
<th>科目名稱:(英文)</th>";
if($cur_cd eq "NEW")
{
 print "<th><input type=\"text\" name=\"cur_name_e\"></th>";
} 
else
{
 print "<th>";
 print "$cur_name_e";
 print "</th>";
 print "<input type=\"hidden\" name=\"cur_name_e\" value=\"$cur_name_e\">";
}

print "
</tr>

<tr>
  <th colspan=2 rowspan=11>
";
#####     功課表     ##################
### read $week and $prd_cd from data ##

my($counter);
$counter=0;
my(@ClassTime,@ClassWeek);
@ClassTime=();
@ClassWeek=();
if($new == 0)
{
 open(FILE,"<$PATH/$dept_cd/course/$cur_cd"."_$grp"."_period");
}
else
{
 open(FILE,"<$PATH/$dept_cd/course/temp/$cur_cd"."_$grp"."_period");
}
$ClassWeek[$counter]=<FILE>;
while($ClassWeek[$counter] ne "")
{
 chop($ClassWeek[$counter]);
 $ClassTime[$counter]=<FILE>;
 chop($ClassTime[$counter]);
 $counter++;
 $ClassWeek[$counter]=<FILE>;
}
close(FILE);
$counter--;
print "
  <table border=1>
  <tr>
  <th></th><th>一</th>
           <th>二</th>
           <th>三</th>
           <th>四</th>
           <th>五</th>
           <th>六</th>
           <th>日</th>
           </tr>
  ";
for($j=0;$j<=12;$j++)
{
 print "<tr><th>";
 if ($j==0)
   { print "A";}
 if ($j>=1 && $j<=4)
   { print "$j";}
 if ($j==5)
   { print "B";}
 if ($j>=6 && $j<=9)
   { $jj=$j-1; print "$jj"; }
 if ($j==10)
   { print "C";}
 if ($j==11)
   { print "D";}
 if ($j==12)
   { print "E";}
 print "</th>";
 for($i=1;$i<=7;$i++)
 {
  $k="$i"."_$j";
  my($counter2);
  my($CHECK);
  $CHECK=0;
  for($counter2=0;$counter2<=$counter;$counter2++)
  {
   if( ($i == $ClassWeek[$counter2]) && ($j == $ClassTime[$counter2]) )
   { $CHECK++; }
  }
  if($CHECK >0)
   { 
  print "<td><input type=\"checkbox\" 
          name=\"$k\" value=\"999\" checked></td>";
   }
  else
   {
  print "<td><input type=\"checkbox\"
          name=\"$k\" value=\"999\"></td>";
   }
 }
 print "</tr>";
}
print "
</table>";
######### end of 功課表 ################
print "
</th>
<th>科目編號:</th>";
if($cur_cd eq "NEW")
{
 print "<th><input type=\"text\" name=\"cur_cd\"
             size=8></th>";
} 
else
{
 print "<th>";
 print "$cur_cd";
 print "</th>";
 print "<input type=\"hidden\" name=\"cur_cd\" value=\"$cur_cd\">";
}
print "</tr><tr>
<th>班別</th>
<th>";
print "<select name=\"grp\">";
for($i=1;$i<=$MaxGrp;$i++)
{
 if($i<10)
 {
  if("0$i" eq $grp)
  {
   print "<option value=\"0$i\" selected>0$i\n";
  } 
  else
  {
   print "<option value=\"0$i\">0$i\n";
  }
 }# end of if($i<10)
 else # $i>=10
 {
  if("$i" eq $grp)
  {
   print "<option value=\"$i\" selected>$i\n";
  }
  else
  {
   print "<option value=\"$i\">$i\n";
  }
 }
}
print "</select>";
print "</th>
</tr>
<tr>
<th>授課老師</th>";

# if($new==0)
# { open(FILE,"<$PATH/$dept_cd/course/$cur_cd"."_$grp"."_teacher"); }
# else
# { open(FILE,"<$PATH/$dept_cd/course/temp/$cur_cd"."_$grp"."_teacher");}
# my(@STAFF);
# @STAFF=();
# my($counter);
# $counter=0;
# $STAFF[$counter]=<FILE>;
# while($STAFF[$counter] ne "")
# {
#  chop($STAFF[$counter]);
#  $counter++;
#  $STAFF[$counter]=<FILE>;
# }
# close(FILE);
# $counter--;
#### read teacher_code and name of this department####
print "<th><table border=1><tr><th>本系所授課老師</th><tr>";
print "<th><select name=\"staff\" size=4 multiple>";
open(FILE,"<$PATH/$dept_cd/teacher");
$TEACHER=<FILE>;
chop($TEACHER);
while( $TEACHER ne "")
{
 ($staff_cd,$staff_name)=split(/\s+/,$TEACHER);
#  my($CHECK);
#  $CHECK=0;
#   my($counter2);
#   for($counter2=0;$counter2<=$counter;$counter2++)
#   {
#    if($staff_cd eq $STAFF[$counter2])
#    { $CHECK++;  }
#   }
#  if($CHECK ==0)
#  {
  print "<option value=\"$staff_cd\">$staff_name\n";
#  }
#  else
#  {
#  print "<option value=\"$staff_cd\" selected>$staff_name\n";
#  }
 $TEACHER=<FILE>;
 chop($TEACHER);
}
 
close(FILE);
#################################
## NOTICE : ADD by ionic 3/18 ###
##      教師代聘 state        ###
#################################
print "<option value=\"99999\">教師待聘\n";

print "
</select>
</th></tr>
<tr><th>外系所授課老師</th></tr>
<tr><th>";
open(FILE,"<$PATH/teacher.txt");
$TEACHER=<FILE>;
print "<select name=\"staff\" size=4 multiple>";
while($TEACHER ne "")
{
 $TEACHER=~/(\S+)\s+(\S+)\s+(\S+.*)/;
 $teacher_dept=$1;
 $teacher_code=$2;
 $teacher_name=$3;
 if($dept_cd ne "I000" && $teacher_dept ne "I000")
 {
  if(($teacher_dept/10) ne ($dept_cd/10))
  {
  print "<option value=\"$teacher_code\">$teacher_name\n";
  }
 }
 else
 {
  if($dept_cd eq "I000" && $teacher_dept ne "I000")
  {
   print "<option value=\"$teacher_code\">$teacher_name\n";
  }
 }
 $TEACHER=<FILE>;
}
close(FILE);
print "</select></th></tr>
</table></th>
</tr>

<tr>
<th>時數:</th>
<th><select name=\"classtime\">";
for($i=1;$i<=10;$i++)
{
 if($i == $classtime)
 { print "<option value=\"$i\" SELECTED>$i"; }
 else
 { print "<option value=\"$i\">$i";}
}
print "
</select>
</th>
</tr>
<tr>
<th>學分:</th>
<th>";
if($cur_cd eq "NEW")
{
print "<select name=\"credit\">";
 for($i=0;$i<=8;$i++)
 { print "<option value=\"$i\">$i"; }
print "</select>";
}
else
{
print"<input type=\"hidden\" name=\"credit\"
       value=\"$credit\">"; 
print "$credit";
}

print "
</th>
</tr>

<tr>
<th>必修/選修/通識</th>
<th><select name=\"cura_cd\">";
for($i=1;$i<=3;$i++)
{
 if($i==1) { $name="必修"; }
 if($i==2) { $name="選修"; }
 if($i==3) { $name="通識"; }
 if($i == $cura_cd)
 { print "<option value=\"$i\" SELECTED>$name"; }
 else
 { print "<option value=\"$i\">$name"; }
}

print "
</select>
</th>
</tr>
<tr>
<th>上課教室:</th>
<th><select name=\"rm_cd\">";

## read class room data from file ##
open(FILE,"<$PATH/ClassRoom");
$ROOM=<FILE>;
chop($ROOM);
while($ROOM ne "")
{
 ($Rm_Cd,$Rm_Name)=split(/\s+/,$ROOM);
  ## set default rm_cd ##
  if($Rm_Cd eq $rm_cd)
  {
   print "<option value=\"$Rm_Cd $Rm_Name\" Selected>$Rm_Name\n";
  }
  else
  {
   print "<option value=\"$Rm_Cd $Rm_Name\">$Rm_Name\n";
  }
 $ROOM=<FILE>;
 chop($ROOM);
}
close(FILE);
## end of read class room data from file ##

print "</select></th>
</tr>
</table>";

## draw table for 備註 ##
print "<p>
<center>
<table border=0>
<tr><td>備註：</td></tr>
<tr rowspan=2><th align=left>1.有限修人數？</th> 
    <td><table border=0><tr>
    <td>是</td><td>否</td>
    <center>
    <td>百</td><td>十</td><td>個</td></tr>
    </center>
    <tr>
";
if($new)
{
 open(CHECK,"<$PATH/$dept_cd/course/temp/$cur_cd"."_$grp"."_check");
 @Note=<CHECK>;
 close(CHECK);
 chop(@Note);
}
if($Note[0] eq "")
{
print "
    <td><input type=\"radio\" name=\"ask_p\" value=\"1\"></td>
    <td><input type=\"radio\" name=\"ask_p\" value=\"0\" checked></td>";
}
else
{
print "
    <td><input type=\"radio\" name=\"ask_p\" value=\"1\" checked></td>
    <td><input type=\"radio\" name=\"ask_p\" value=\"0\"></td>";
 $Temp=$Note[0];
 $Digit[0]=0; $Digit[1]=0; $Digit[2]=0;
 while($Temp>=0)
 { $Temp-=100; $Digit[0]++; }
 $Digit[0]--;
 $Temp=$Note[0]%100;
 while($Temp>=0)
 { $Temp-=10; $Digit[1]++; }
 $Digit[1]--;
 $Temp=$Note[0]%10;
 while($Temp>=0)
 { $Temp--; $Digit[2]++; }
 $Digit[2]--;
}
my($i,$j);
for($i=0;$i<=2;$i++)
{
 print "<td><select name=\"number_$i\">";
 for($j=0;$j<=9;$j++)
 {
  if($Note[0] !=0 && $Digit[$i] == $j)
  { print "<option value=\"$j\" selected>$j"; }
  else
  { print "<option value=\"$j\">$j"; }
 }
 print "</select></td>"
}

print
"</tr></table></td>
</tr>
<tr rowspan=2><th align=left>2.支援某系所？</th>
<td><table border=0><tr>
<td>是</td><td>否</td><tr>
";
if($Note[1] eq "")
{
print "
    <td><input type=\"radio\" name=\"support_p\" value=\"1\"></td>
    <td><input type=\"radio\" name=\"support_p\" value=\"0\" checked></td>";
}
else
{
print "
    <td><input type=\"radio\" name=\"support_p\" value=\"1\" checked></td>
    <td><input type=\"radio\" name=\"support_p\" value=\"0\"></td>";
}
print "
<td>
<table border=0>
<select name=\"supply_dept\" size=3 multiple>";
open(FILE,"<$PATH/Dept");
my($DEPT,$dept,$dept_name);
$DEPT=<FILE>;
while($DEPT ne "")
{
$DEPT=~/(\S+)\s+(\S+\S*)\s*/;
$dept=$1;
$dept_name=$2;
if($Note[1] ne "" && $Note[1]=~/$dept_name /)
{ print "<option value=\"$dept_name a\" selected>$dept_name\n"; }
else
{ print "<option value=\"$dept_name a\">$dept_name\n"; }
$DEPT=<FILE>;
}
close(FILE);
print"</select></td></tr><tr><td>
<select name=\"supply_grade\" size=2 multiple>";
if($Note[1] ne "" && $Note[1]=~/1/)
{ print "<option value=\"1 a\" selected>一年級\n"; }
else
{ print "<option value=\"1 a\">一年級\n"; }
if($Note[1] ne "" && $Note[1]=~/2/)
{ print "<option value=\"2 a\" selected>二年級\n"; }
else
{ print "<option value=\"2 a\">二年級\n"; }
if($Note[1] ne "" && $Note[1]=~/3/)
{ print "<option value=\"3 a\" selected>三年級\n"; }
else
{ print "<option value=\"3 a\">三年級\n"; }
if($Note[1] ne "" && $Note[1]=~/4/)
{ print "<option value=\"4 a\" selected>四年級\n"; }
else
{ print "<option value=\"4 a\">四年級\n"; }
print "
</select></td></tr>";
print
"</table></td></table></tr>
</tr></tr>
";
print
"
<tr rowspan=4><th align=left>3.有不得選修此科目作為通識之院/系？</th>
<td><table border=0><tr>
<td>是</td><td>否</td><tr>
";
if($Note[2] eq "")
{
 print " <td><input type=\"radio\" name=\"other_p\" value=\"1\"></td>
    <td><input type=\"radio\" name=\"other_p\" value=\"0\" checked></td>";
}
else
{ print "
  <td><input type=\"radio\" name=\"other_p\" value=\"1\" checked></td>
    <td><input type=\"radio\" name=\"other_p\" value=\"0\"></td>
  ";
}
print "
<td>
<table border=0>
<tr><td>
<select name=\"for_dept\" size=3 multiple>";
open(FILE,"<$PATH/Dept");
my($DEPT,$dept,$dept_name);
$DEPT=<FILE>;
while($DEPT ne "")
{
$DEPT=~/(\S+)\s+(\S+\S*)\s*/;
$dept=$1;
$dept_name=$2; 
if($Note[2] ne "" && $Note[2]=~/$dept_name /)
{
 print "<option value=\"$dept_name b\" selected>$dept_name\n";
}
else
{
print "<option value=\"$dept_name b\">$dept_name\n";
}
$DEPT=<FILE>;
}
close(FILE);
if($Note[2] ne "" && $Note[2]=~/工學院 /)
{
 print "<option value=\"工學院 b\" selected>工學院\n";
} 
else
{
print "<option value=\"工學院 b\">工學院\n";
}
if($Note[2] ne "" && $Note[2]=~/理學院 /)
{
 print "<option value=\"理學院 b\" selected>理學院\n";
} 
else
{
print "<option value=\"理學院 b\">理學院\n";
}
if($Note[2] ne "" && $Note[2]=~/管理學院 /)
{
 print "<option value=\"管理學院 b\" selected>管理學院\n";
} 
else
{
print "<option value=\"管理學院 b\">管理學院\n";
}
if($Note[2] ne "" && $Note[2]=~/社會科學院 /)
{
 print "<option value=\"社會科學院 b\" selected>社會科學院\n";
} 
else
{
print "<option value=\"社會科學院 b\">社會科學院\n";
}
if($Note[2] ne "" && $Note[2]=~/文學院 /)
{
 print "<option value=\"文學院 b\" selected>文學院\n";
} 
else
{
print "<option value=\"文學院 b\">文學院\n";
}
print "
</select></td></tr>
<tr><td>
<select name=\"other_grade\" size=2 multiple>
";
if($Note[2] ne "" && $Note[2]=~/1/)
{ print "<option value=\"1 b\" selected>一年級\n"; }
else
{ print "<option value=\"1 b\">一年級\n"; }
if($Note[2] ne "" && $Note[2]=~/2/)
{ print "<option value=\"2 b\" selected>二年級\n"; }
else
{ print "<option value=\"2 b\">二年級\n"; }
if($Note[2] ne "" && $Note[2]=~/3/)
{ print "<option value=\"3 b\" selected>三年級\n"; }
else
{ print "<option value=\"3 b\">三年級\n"; }
if($Note[2] ne "" && $Note[2]=~/4/)
{ print "<option value=\"4 b\" selected>四年級\n"; }
else
{ print "<option value=\"4 b\">四年級\n"; }
print "

</select>
</td></tr>
</table>



</td>
</td></table>
</tr>
<tr><pre> </pre></tr>
<tr>
<th align=\"center\" colspan=2>其他備註</th>
</tr>
<tr rowspan=6 colspan=2>
<th colspan=2>
<textarea name=\"note\" clos=30 rows=5>";
$Size=@Note;
if($Size>3)
{
 for($i=3;$i<$Size;$i++)
 { print "$Note[$i]\n"; }
}
print "</textarea>
</th>
</tr>
</table>
</center>
<p>
<input type=\"hidden\" name=\"ShowIndex\" value=0>
<input type=\"hidden\" name=\"Edit\" value=\"$display{'Edit'}\">
<input type=\"submit\" value=\"送出資料\">
<input type=\"reset\" value=\"重新填寫\">

</form>
</center>
</body>
</html>";
 

## end of html file ##



#############################################
## begin of function ##
 sub user_input
{
 local ($buffer,@datas,$data,$name,$value,%FORM);
$ENV{'REQUEST_METHOD'}=~ tr/a-z/A-Z/;
if($ENV{'REQUEST_METHOD'} eq "POST")
 {
  read(STDIN,$buffer,$ENV{'CONTENT_LENGTH'});
 } else {
  $buffer=$ENV{'QUERY_STRING'};
}
@datas=split(/&/,$buffer);
foreach $data(@datas)
{
 ($name,$value)=split(/=/,$data);
 $value=~ tr/+/ /;
 $value=~ s/%(..)/pack("C",hex($1))/eg;
 $FORM{$name}=$value;
}
%FORM;
}
