#!/usr/local/bin/perl
$| = 1;
print "Content-type: text/html","\n\n";

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Error_Message.pm";

my(%Input,%Course);

%Input		= User_Input();
%cge		= Read_Cge();
@all_course	= Find_All_Course($Input{dept_cd}, "", "history");

#foreach $k (keys %Input) {
#  print("$k --> $Input{$k}<br>\n");
#}

#$crypt_salt = Read_Crypt_Salt($Input{dept_cd}, "dept");
#if($Input{crypt} eq "1")
#{
# $Input{password} = Crypt($Input{password}, $crypt_salt);
#}
#print("input pass = $Input{password}<br>");

#Check_Dept_Password($Input{dept_cd}, $Input{password});

#Check_SU_Password($Input{password},"dept",$Input{dept_cd});

#if((Check_Dept_State($Input{dept_cd}) == 0) and ($SUPERUSER ne "1")){
#   SYS_NOT_ALLOWED();
#   exit();
#}     

if($Input{group} eq "") { $Input{group} = "01" };

if($Input{course_cd} eq "")
{
 $Input{course_cd} = "new";
}
if($Input{course_cd} ne "new")
{
 if($Input{course_cd}=~/new/)
 {
  ($Input{course_cd},$useless)=split(/\s/,$Input{course_cd});
  %Course = Read_Course( $Input{dept_cd}, $Input{course_cd}, $Input{group},"");
 }
 else
 {
  %Course = Read_Course( $Input{dept_cd}, $Input{course_cd}, $Input{group},"history");
 }
}else{
   $new_course_flag = 1;
}

%temp=Read_Dept($Input{dept_cd});


$|=0;
print "
<html>
<head>
<title>新增學期開課- $temp{cname}</title>
</head>";
 Add_JS();  ## function to add JavaScript Code
print "
<body bgcolor=white background=$GRAPH_URL/ccu-sbg.jpg>
<center>
<form name=form1 method=post action=Open_Course_3.cgi>
<input type=hidden name=dept_cd value=$Input{dept_cd}>
<input type=hidden name=password value=$Input{password}>
<input type=hidden name=new_course_flag value=$new_course_flag>
<table border=1>
<tr>
<th bgcolor=yellow>科目名稱(中文)</th><th>";
if($Input{course_cd} ne "new" && $SUPERUSER ne "1")
{
 print "$Course{cname}<input type=hidden name=cname value=\"$Course{cname}\">";
}
else
{
 print "<input type=text length=70 name=cname value=\"$Course{cname}\">";
}
print "
</th></tr>
<tr>
<th bgcolor=yellow>科目名稱(英文)</th><th>";
if($Input{course_cd} ne "new" && $SUPERUSER ne "1")
{
 print "$Course{ename}<input type=hidden name=ename value=\"$Course{ename}\">";
}
else
{
 print "<input type=text length=70 name=ename value=\"$Course{ename}\">";
}
print "</th></tr>
</table><br>
<table border=1>
<tr>
  <th colspan=2 rowspan=13>
  <table border=1>
  <tr>
  <th></th><th bgcolor=orange>一</th>
           <th bgcolor=orange>二</th>
           <th bgcolor=orange>三</th>
           <th bgcolor=orange>四</th>
           <th bgcolor=orange>五</th>
           <th bgcolor=orange>六</th>
           <th bgcolor=orange>日</th>
           </tr>
  ";
for($j=0;$j<=13;$j++)
{
 print "<tr><th bgcolor=orange>";
 if ($j==0)
   { print "A";}
 if ($j>=1 && $j<=4)
   { print "$j";}
 if ($j==5)
   { print "F";}
 if ($j==6)
   { print "B";}
 if ($j>=7 && $j<=10)
   { $jj=$j-2; print "$jj"; }
 if ($j==11)
   { print "C";}
 if ($j==12)
   { print "D";}
 if ($j==13)
   { print "E";}
 print "</th>";
 for($i=1;$i<=7;$i++)
 {
  $k="$i"."_$j";
  $CHECK=0;
  foreach $ele (@{$Course{time}}) {
    if($k eq "$$ele{week}_$$ele{time}" )
    {
     $CHECK=1;
     goto OUT;
    } 
  }
  OUT:
  if($CHECK == 0)
  {
   print "<td><input type=checkbox
          name=$k value=999></td>";
  }
  else
  {
   print "<td><input type=checkbox name=$k value=999 checked></td>";
  }
 }
 print "</tr>";
}
print "
</table>";
######### end of 功課表 ################
print "</th>\n";
print "<th bgcolor=yellow>開課年級</th><th><select name=grade>";
$g_string[1]="一";
$g_string[2]="二";
$g_string[3]="三";
$g_string[4]="四";

if( ($Input{dept_cd} =~ /6$/) and ($Input{dept_cd} != "7006") ) {  ###  除了通識以外的研究所
  print "<option value=1 selected>$g_string[1]年級\n";             ###  只能選一年級
}else{                                                             ###  其他系所可以選1~4年級
  for($i=1;$i<5;$i++) {
   if($i == $Input{grade}) {
     print "<option value=$i selected>$g_string[$i]年級\n";
   }else{
     print "<option value=$i>$g_string[$i]年級\n";
   }
  }
}
print "</select></th></tr><tr>
<th bgcolor=yellow>科目編號:</th><th>";
if($Input{course_cd} ne "new")
{
 print "$Course{id}<input type=hidden name=id value=$Course{id} maxlength=7>";
}
else
{
 print "<input type=text length=10 name=id>";
}
print "</th></tr><tr>
<th bgcolor=yellow>班別</th>
<th>";
print "<select name=group>";
for($i=1;$i<=40;$i++)
{
 if($i<10)
 {
   print "<option value=\"0$i\">0$i\n";
 }# end of if($i<10)
 else # $i>=10
 {
   print "<option value=\"$i\">$i\n";
 }
}
print "</select>";
print "</th>
</tr>
<tr>
<th bgcolor=yellow>授課老師</th>";

#### read teacher_code and name of this department####
print "
<th><select name=Teacher size=3 multiple onblur=\"isDelete(document.form1.Teacher)\">
<option value=99999 selected>教師未定
</select></th>
</tr>
<tr><th bgcolor=yellow>選擇授課教師</th>
<th>";
print "
<input type=button name=btn1 value=選擇任課教師 onclick=\"AddWin()\"> 
<input type=button name=btn2 value=重置 onClick=\"ClearAll(document.form1.Teacher)\">
</th></tr>
</tr>
<tr>
<th bgcolor=yellow>時數:</th>
<th><select name=total_time>";
for($i=1;$i<=12;$i++)
{
 if($i ne $Course{total_time} )
 {
  print "<option value=$i>$i";
 }
 else
 {
  print "<option value=$i selected>$i";
 }
}
print("</select>");
###########################################################################
print qq(
  <tr>
    <th bgcolor=yellow>正課/實驗實習/書報討論時數:</th>
    <th><select name=lab_time1>
);
for($i=0;$i<=12;$i++) {
 if($i ne $Course{lab_time1} ) {
   print "<option value=$i>$i";
 }else{
   print "<option value=$i selected>$i";
 }
}
print qq(</select><SELECT name="lab_time2">);      ###
for($i=0;$i<=12;$i++) {
 if($i ne $Course{lab_time2} ) {
   print "<option value=$i>$i";
 }else{
   print "<option value=$i selected>$i";
 }
}
print qq(</select><SELECT name="lab_time3">);      ###
for($i=0;$i<=12;$i++) {
 if($i ne $Course{lab_time3} ) {
   print "<option value=$i>$i";
 }else{
   print "<option value=$i selected>$i";
 }
}
print("</SELECT></TH></TR>");


###########################################################################
print "
<tr>
<th bgcolor=yellow>學分:</th>
<TH>";
#if($Course{credit} == "" )  {
if($Input{course_cd} eq "new") {      ### 新增科目才能改學分
  print("<SELECT name=credit>\n");
  for($temp=0; $temp<7; $temp++) {
    print("<OPTION>$temp\n");
  }
  print("</SELECT>");
}else{                                ### 歷年科目一律不可改
  print("$Course{credit}");
  print("<INPUT type=hidden name=credit value=$Course{credit}>");
}
#<th><select name=credit>";
#for($i=0;$i<=8;$i++)
# {
#  if($i ne $Course{credit} )
#  { print "<option value=$i>$i"; }
#  else
#  { print "<option value=$i selected>$i"; }
# }
#print "</select>";
print "
</th>
</tr>

<tr>
<th bgcolor=yellow>必修/選修/通識</th>
<th><select name=property>";
for($i=1;$i<=3;$i++)
{
 if($i==1) { $name="必修"; }
 if($i==2) { $name="選修"; }
 if($i==3) { $name="通識"; }
 if($i eq $Course{property} )
 { print "<option value=$i selected>$name"; }
 else
 { print "<option value=$i>$name"; } 
}

#print "
#</select>
#<tr>
#<th bgcolor=yellow>一般/軍訓/體育</th>
#<th><select name=suffix_cd>";
#for($i=0;$i<=2;$i++)
#{
# if($i==0) { $suffix_cd="一般"; }
# if($i==1) { $suffix_cd="軍訓"; }
# if($i==2) { $suffix_cd="體育"; }
# if($i eq $Course{suffix_cd} )
# { print "<option value=$i selected>$suffix_cd"; }
# else
# { print "<option value=$i>$suffix_cd"; }
#}

print "
</select>
</th>
</tr>
<tr>
<th bgcolor=yellow>上課教室:</th>
<th><select name=classroom>";
 @Classroom=Find_All_Classroom();
 foreach $Classroom(@Classroom)
 {
  %classroom=Read_Classroom($Classroom);
  if( $classroom{id} eq $Course{classroom} )
  { print "<option value=$Classroom selected>$classroom{cname}\n"; }
  else
  { print "<option value=$Classroom>$classroom{cname}\n"; }
 }
print "</select></th>
</tr>
<tr><th bgcolor=yellow>篩選原則</th><th><select name=principle>\n";
my($p,@p_string);
$p_string[0]="不需篩選";
$p_string[1]="一次篩選";
$p_string[2]="二次篩選";
for($p=0;$p<3;$p++)
{
 if($p ne $Course{principle})
 { print "<option value=$p>$p_string[$p]\n"; }
 else
 { print "<option value=$p selected>$p_string[$p]\n"; }
}
print "</select></th></tr></table>\n";

## draw table for 備註 ##
print "<table border=1>";
print "</select></th></tr>\n";
print "<tr><th bgcolor=yellow>限修人數</th><th><table border=0>\n";
print "<tr><td>百</td><td>十</td><td>個</td></tr>\n";
print "<tr><td><select name=number_limit_2>";
my($i,$j);
$j= $Course{number_limit} / 100;
for($i=0;$i<10;$i++)
{
 if($i ne $j)
 { print "<option value=$i>$i\n"; }
 else
 { print "<option value=$i selected>$i\n"; }
}
print "</select></td><td><select name=number_limit_1>";
$j= ( $Course{number_limit} % 100 ) /10;
for($i=0;$i<10;$i++)
{
 if($i ne $j)
 { print "<option value=$i>$i\n"; }
 else
 { print "<option value=$i selected>$i\n"; }
}
print "</select></td><td><select name=number_limit_0>";

$j= $Course{number_limit} % 10;
for($i=0;$i<10;$i++)
{
 if($i ne $j)
 { print "<option value=$i>$i\n"; }
 else
 { print "<option value=$i selected>$i\n"; }
}
print "</select></td></tr></table></th>";
### 保留學生名額 ###
print "<th bgcolor=yellow>保留新生名額</th><th><table border=0>\n";
print "<tr><td>百</td><td>十</td><td>個</td></tr>\n";
print "<tr><td><select name=reserved_number_2>";
my($i,$j);
$j= $Course{reserved_number} / 100;
for($i=0;$i<10;$i++)
{
 if($i ne $j)
 { print "<option value=$i>$i\n"; }
 else
 { print "<option value=$i selected>$i\n"; }
}
print "</select></td><td><select name=reserved_number_1>";
$j= ( $Course{reserved_number} % 100 ) /10;
for($i=0;$i<10;$i++)
{
 if($i ne $j)
 { print "<option value=$i>$i\n"; }
 else
 { print "<option value=$i selected>$i\n"; }
}
print "</select></td><td><select name=reserved_number_0>";

$j= $Course{reserved_number} % 10;
for($i=0;$i<10;$i++)
{
 if($i ne $j)
 { print "<option value=$i>$i\n"; }
 else
 { print "<option value=$i selected>$i\n"; }
}
print "</select></td></tr></table></th></tr>\n";
print "<tr><th bgcolor=yellow rowspan=2>支援系所</th><th rowspan=2>\n";
print "<select name=support_dept size=4 multiple>\n";

my(@Dept,$dept,%Dept,$flag);

@Dept=Find_All_Dept();
foreach $dept(@Dept)
{
 %Dept=Read_Dept($dept);
 $flag=0;
 foreach $ele(@{$Course{support_dept}})
 {
  if( $ele eq $dept)
  { $flag = 1; break; }
 } 
 if( $flag == 1 )
 {
  print "<option value=$Dept{id} selected>$Dept{cname}\n";
 } 
 else 
 {
  print "<option value=$Dept{id}>$Dept{cname}\n";
 }
}          
print "</select></th><th bgcolor=yellow>支援年級</th><th>\n";
print "<select name=support_grade size=2 multiple>";
my(@g_string);
$g_string[1]="一";
$g_string[2]="二";
$g_string[3]="三";
$g_string[4]="四";
for($i=1;$i<=4;$i++)
{
 $flag=0;
 foreach $ele(@{$Course{support_grade}})
 {
  if($ele eq $i)
  { $flag=1; break; }
 }
 if($flag == 1)
 { print "<option value=$i selected>$g_string[$i]年級\n"; }
 else
 { print "<option value=$i>$g_string[$i]年級\n"; } 
}
print "</select></th></tr><tr><th bgcolor=yellow>支援班級</th>\n";
print "<th><select name=support_class size=2 multiple>\n";
$g_string[0]="A";
$g_string[1]="B";
$g_string[2]="C";
$g_string[3]="D";
$g_string[4]="E";
$g_string[5]="F";
for($i=0;$i <=5;$i++)
{
 $flag=0;
 foreach $ele( @{$Course{support_class}} )
 {
  if($ele eq $g_string[$i])
  { $flag=1; break; }
 }
 if($flag == 1)
 {
  print "<option value=$g_string[$i] selected>$g_string[$i]\n";
 }
 else
 {
  print "<option value=$g_string[$i]>$g_string[$i]\n";
 }
}
print "</select></th></tr>\n";
### 擋修系所 ###
print "<tr><th bgcolor=YELLOW rowspan=2>擋修系所</th><th rowspan=2>\n";
print "<select name=ban_dept size=4 multiple>\n";

my(@Dept,$dept,%Dept,$flag);

@Dept=Find_All_Dept();
foreach $dept(@Dept)
{
 %Dept=Read_Dept($dept);
 $flag=0;
 foreach $ele(@{$Course{ban_dept}})
 {
  if( $ele eq $dept)
  { $flag = 1; break; }
 } 
 if( $flag == 1 )
 {
  print "<option value=$Dept{id} selected>$Dept{cname}\n";
 } 
 else 
 {
  print "<option value=$Dept{id}>$Dept{cname}\n";
 }
}          
print "</select></th><th bgcolor=YELLOW>擋修年級</th><th>\n";
print "<select name=ban_grade size=2 multiple>";
my(@g_string);
$g_string[1]="一";
$g_string[2]="二";
$g_string[3]="三";
$g_string[4]="四";
for($i=1;$i<=4;$i++)
{
 $flag=0;
 foreach $ele(@{$Course{ban_grade}})
 {
  if($ele eq $i)
  { $flag=1; break; }
 }
 if($flag == 1)
 { print "<option value=$i selected>$g_string[$i]年級\n"; }
 else
 { print "<option value=$i>$g_string[$i]年級\n"; } 
}
print "</select></th></tr><tr><th bgcolor=YELLOW>擋修班級</th>\n";
print "<th><select name=ban_class size=2 multiple>\n";
$g_string[0]="A";
$g_string[1]="B";
$g_string[2]="C";
$g_string[3]="D";
$g_string[4]="E";
$g_string[5]="F";
for($i=0;$i <=5;$i++)
{
 $flag=0;
 foreach $ele( @{$Course{ban_class}} )
 {
  if($ele eq $g_string[$i])
  { $flag=1; break; }
 }
 if($flag == 1)
 {
  print "<option value=$g_string[$i] selected>$g_string[$i]\n";
 }
 else
 {
  print "<option value=$g_string[$i]>$g_string[$i]\n";
 }
}
print "</select></th></tr>\n";

################### 支援通識領域及人數 ###########################
print qq(
  <TR><TH bgcolor=PINK>支援通識領域</TH>
      <TH colspan=3 align=left><SELECT name="support_cge_type">
);
foreach $cge (sort keys %cge) {
  if($cge eq "0") {
    print("<OPTION value=$cge SELECTED>$cge{$cge}{sub_cge_id_show} $cge{$cge}{cge_name}");
  }else{
    print("<OPTION value=$cge>$cge{$cge}{sub_cge_id_show} $cge{$cge}{cge_name}");
  }
}
print qq(
  </SELECT></TH></TR>
  <TR><TH bgcolor=PINK>支援通識人數</TH>
      <TH colspan=3 align=left>
        <TABLE>
          <tr><td>十</td><td>個</td></tr>
          <tr><td><select name=support_cge_number_1>
);
my($i,$j);
$j = $Course{support_cge_number} / 10;
  for($i=0;$i<10;$i++) {
   if($i ne $j)
     { print "<option value=$i>$i\n"; }
   else
     { print "<option value=$i selected>$i\n"; }
  }
print("</select></td><td><select name=support_cge_number_0>");
  $j= $Course{support_cge_number} % 10;
  for($i=0;$i<10;$i++) { 
   if($i ne $j)
     { print "<option value=$i>$i\n"; }
   else
     { print "<option value=$i selected>$i\n"; }
  }
print("</SELECT></TD></TR></TABLE></TD></TR>");
########################   先修科目   ##############################
print qq(
  <TR>
    <TH bgcolor=PINK>先修科目</TH>
    <TD colspan=3 align=left>
      <SELECT name=Precourse size=3 multiple>
        <OPTION value=99999 selected>無　　　　　　　　　　　　　　　　　　
      </SELECT>
      <BR>
      <!CENTER>
      <INPUT type=button name=select_precourse value=選擇先修科目 onclick="Add_Precourse_Win()"> 
      <INPUT type=button name=select_precourse2 value=重置 onclick="Clear_Precourse()"><BR>
      <SELECT name=prerequisite_logic>
        <OPTION value="AND" SELECTED>$PREREQUISITE_LOGIC{AND}
        <OPTION value="OR">$PREREQUISITE_LOGIC{OR}
      </SELECT>
    </TD>
  </TR>                              
);

##################################################################
print "<tr><th bgcolor=yellow>備註欄</th>";
print "<th colspan=3><textarea name=note rows=3 cols=40>";
print $Course{note};
print "</textarea></th></tr>
</table>
";
print "<p>
<center>
<input type=\"submit\" value=\"送出資料\">
<input type=\"reset\" value=\"重新填寫\">
</form><hr>";
Links1($Input{dept_cd},$Input{grade},$Input{password});
print "
</center>
</body>
</html>";
 

## end of html file ##

sub Add_JS()
{
print qq(
  <SCRIPT language=javascript src=\"./Classify.js\"></SCRIPT>
  <SCRIPT language=JAVASCRIPT>
    function Add_Precourse_Win()
    {
      win2=open("./Add_Precourse_Window.html","openwin","width=400,height=450");
      win2.creator=self; 
    }

    // 清除先修科目所選的所有資料
    function Clear_Precourse()
    {
       form1.Precourse.length=1;
       form1.Precourse.options[0].value="99999";
       form1.Precourse.options[0].text="無";
    }
                                    
  </SCRIPT>
);
}

