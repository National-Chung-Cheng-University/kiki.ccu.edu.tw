#!/usr/local/bin/perl
print "Content-type: text/html","\n\n";

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Teacher.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Error_Message.pm";


my(%Input,@Date,$i,@Teacher);

@Teacher = Read_Teacher_File();

$i=0;
%Input		= User_Input();
%cge		= Read_Cge();
@all_course	= Find_All_Course($Input{dept_cd}, "", "");

Check_SU_Password($Input{password}, "Open_Course_3.cgi", $Input{id});

#foreach $k (keys %Input) {
#  print("$k --> $Input{$k}<br>\n");
#}


foreach $key(%Input)
{
 if($Input{$key} eq "999")
 {
  $Date[$i++]=$key;
 }
}

if($Input{group} eq "") { $Input{group} = "01" };

%temp=Read_Dept($Input{dept_cd});

print qq(
  <html>
    <head><title>�s�W�Ǵ��}��[�}�ҽT�{]- $temp{cname} </title></head>
    <body bgcolor=white background=$GRAPH_URL/ccu-sbg.jpg>
      <center>
);
## check area ##
my($line,@error_string);
$line=0;
$error=0;
$fatal_error=0;

$time_string="A/1/2/3/4/F/B/5/6/7/8/C/D/E";
$week_string="��/�@/�G/�T/�|/��/��";     

$error_string[$line++]="<hr><font size=4 color=red>�t���ˬd�}�Ҹ�Ƶ��G�p�U</font><br>\n";
$error_string[$line++]="<font size=4 brown>[�p���Y�����~�X�{,�t�αN���������}�Ҹ��]</font><br><br>\n";

if(-e $COURSE_PATH.$Input{dept_cd}."/".$Input{id}."_".$Input{group})
{
 $error_string[$line++]="���Ǵ�����ؤw�g�}�ҧ���<br>\n";
 $error_string[$line++]="���ק��ؤ��e�ХѥD���ϥέק��Ǵ��w�}��ؤ��\\��<br>";
 $fatal_error++;
}
if($Input{id} eq "")
{
 $fatal_error++;
 $error_string[$line++]="�Y�����~: �S����J��إN�X<br>\n";
}
if($Input{cname} eq "" || $Input{ename} eq "")
{
 $fatal_error++;
 $error_string[$line++]="�Y�����~: �S����J��ئW��<br>\n";
}
#########################################################################################
if( (($Input{support_cge_number_0}+$Input{support_cge_number_1}) != 0)and($Input{support_cge_type} eq "0") ) {
  $fatal_error++;
  $error_string[$line++]="�Y�����~: �Y�䴩�q�ѽФĿ�䴩�q�ѻ��<br>\n";
}
#########################################################################################
##### �@��Ͷ}�Ҩt�ΰ��޲z�̥H�~���i�}�P�����骺��(Added Sep30, 2000, Nidalap)
if( ($SUB_SYSTEM == 1) and ($SUPERUSER != 1) ) {    ## �u�A�Ω�@��Ͷ}��
  foreach $date (@Date) {
    if( ($date =~ /^6/) or ($date =~ /^7/) ) {      ## ���i�}�P�����骺��
       $fatal_error++;
       $error_string[$line++]="�Y�����~: ���}�P�����骺�ҽЬ��аȳB!<br>\n";
    }
  }
}
#########################################################################
#####    ��إN�X�T�w��7�X
#####    Added Jan08/2001 Nidalap :D~
if( $Input{new_course_flag} == 1 )  {                   ##  �u���s��حn�ˬd
  
  my $id_length = length($Input{id});
  if( $id_length != 7 ) {
    $fatal_error++;
    $error_string[$line++]="�Y�����~: ��إN�X�����O�C�X<BR>\n";
  }
}
#########################################################################
#####    �ˬd��إN�X����
if( $Input{new_course_flag} == 1 )  {                   ##  �u���s��حn�ˬd
  @all_course = Find_All_Course($Input{dept_cd}, "", "HISTORY");
  foreach $all_course (@all_course) {
    if($Input{id} eq $$all_course{id}) {
      %collision_course = Read_Course($Input{dept_cd}, $$all_course{id}, $$all_course{group}, "HISTORY", "");
      $fatal_error++;
      $error_string[$line++]="�Y�����~: ��إN�X�P���~���<FONT color=RED>$collision_course{cname}</FONT>�Ĭ�<br>\n";
      break;
    }
  }
  ###  �H�U�ˬd��Ǵ��w�}��ؤ��i�R��
  @all_course = Find_All_Course($Input{dept_cd}, "", "");
  foreach $all_course (@all_course) {
    if($Input{id} eq $$all_course{id}) {
      %collision_course = Read_Course($Input{dept_cd}, $$all_course{id},$$all__course{group}, "HISTORY", "");
      $fatal_error++;
      $error_string[$line++]="�Y�����~: ��إN�X�P��Ǵ��w�}���<FONT color=RED>$collision_course{cname}</FONT>�Ĭ�, �ФŨϥηs�W���<br>\n";
      break;
    }
  }

}
#########################################################################

if($Input{Teacher} eq "")
{
 $error++;
 $error_string[$line++]="���~: �S���]�w�½ұЮv, �N�]���Юv���w, �t�Τ��������}�Ҹ��<br>\n";
 $Input{Teacher}="99999";
}
if($Input{total_time} eq "" || $Input{credit} eq "")
{
 $fatal_error++;
 $error_string[$line++]="�Y�����~: �S���]�W�ҮɼƩξǤ�<br>\n";
}
if($Input{classroom} eq "")
{
 $error++;
 $error_string[$line++]="���~: �S���]�w�W�ұЫ�, �N�]���Ыǥ��w, �t�Τ��������}�Ҹ��<br>\n";
 $Input{classroom}="E0000";
}
if($Input{property} eq "")
{
 $error++;
 $error_string[$line++]="���~: �S���]�w����ݩ�, �N�w������, �t�Τ��������}�Ҹ��<br>\n";
 $Input{property}="0";
}
if($Input{principle} eq "")
{
 $error++;
 $error_string[$line++]="���~: �S���]�w�z���h, �N�w�������z��, �t�Τ��������}�Ҹ��<br>\n";
}
if($Input{total_time} ne $i)
{
 $fatal_error++;
 $error_string[$line++]="�Y�����~: �W�ҮɼƻP�ɶ���W���ĮɼƤ��X.<br>\n";
}
#################     Apr 21,2000 Nidalap     ##############################
if($Input{total_time} != $Input{lab_time1} + $Input{lab_time2} + $Input{lab_time3} ) {
 $fatal_error++;
 $error_string[$line++]="�Y�����~: �W�Үɼ������󥿽�+������+�ѳ��Q�׮ɼ�.<br>\n";
}
############################################################################


my(@Course,$Course_Number,$j,%course);
@Course = Find_All_Course($Input{dept_cd});
$Course_Number = @Course;
for($j=0;$j<$Course_Number;$j++)
{
 if($Course[$j]{id} ne $Input{id} || $Course[$j]{group} ne $Input{group})
 {
  %course=Read_Course($Input{dept_cd},$Course[$j]{id},$Course[$j]{group});
  my($k,$classroom_error,$teacher_error);
  for($k=0;$k < $course{total_time};$k++)
  {
   for($l=0;$l < $i;$l++)
   {
    ### �s�W��خɶ��P�¦���خɶ��ۦP�� ###
    if( join("_",$course{time}[$k]{week},$course{time}[$k]{time})
        eq $Date[$l] )
    {
     @temp = split(/\*:::\*/,$Input{Teacher});
     foreach $temp(@temp)
     {
      foreach $temp2( @{$course{teacher}} )
      {
       if($temp eq $temp2 && $temp ne "99999")
       {
        ($temp3,$temp4)=split(/_/,$Date[$l]);
        $error++;
        my($temp5);
        $temp5= (split("/",$week_string))[$temp3];
        $temp5=$temp5.(split("/",$time_string))[$temp4];

$error_string[$line++]="���~:�½ұЮv<font color=brown>$Teacher_Name{$temp}</font>
�½Үɶ�<font color=red>[$temp5]</font>�P$course{cname}�Z�O$course{group}�İ�A�t�Τ��������}�Ҹ��<br>\n";
       }
      }
     }
      ### end of �Юv�İ��ˬd ###
      ### begin �Ыǽİ��ˬd ###
     if( $course{classroom} eq $Input{classroom} )
     {
       ($temp3,$temp4)=split(/_/,$Date[$l]);
        $error++;
        my($temp5);
        $temp5= (split("/",$week_string))[$temp3];
        $temp5=$temp5.(split("/",$time_string))[$temp4];
        my(%temp6);
        %temp6=Read_Classroom($Input{classroom});
$error_string[$line++]="���~:�Ы�<font color=brown>$temp6{cname}</font>
�P$course{cname}�Z�O$course{group}��<font color=red>[$temp5]</font>�Ыǽİ�<br>";
     }
    }
   }
  }
 }
}

if($fatal_error>0)
{
 foreach $error_string(@error_string)
 {
  print $error_string;
 }
 goto END;
}

if($error ne 0)
{
 foreach $error_string(@error_string)
 {
  print $error_string;
 }
}

#if($error==0)
#{
# print "�S���o�{���~";
#}

## end of check area ##
$temp=join("*:::*",@Date);
print "<hr>
<form method=post action=Open_Course_4.cgi>
<input type=hidden name=grade value=$Input{grade}>
<input type=hidden name=dept_cd value=$Input{dept_cd}>
<input type=hidden name=date value=$temp>
<table border=1>
<tr>
<th bgcolor=yellow>��ئW��(����)</th><th>";
 print "$Input{cname}<input type=hidden name=cname value=\"$Input{cname}\">";
print "
</th></tr>
<tr>
<th bgcolor=yellow>��ئW��(�^��)</th><th>";
 print "$Input{ename}<input type=hidden name=ename value=\"$Input{ename}\">";
print "</th></tr>
</table><br>
<table border=1>
<tr>
  <th colspan=2 rowspan=13>
  <table border=12>
  <tr>
  <th></th><th bgcolor=orange>�@</th>
           <th bgcolor=orange>�G</th>
           <th bgcolor=orange>�T</th>
           <th bgcolor=orange>�|</th>
           <th bgcolor=orange>��</th>
           <th bgcolor=orange>��</th>
           <th bgcolor=orange>��</th>
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
  foreach $ele (@Date) {
    if($k eq $ele)
    {
     $CHECK=1;
     goto OUT;
    } 
  }
  OUT:
  if($CHECK==1)
  {
   print "<th><img src=$GRAPH_URL"."Scheck.gif></th>\n";
  }
  else
  {
   print "<th>&nbsp</th>\n";
  }
 }
 print "</tr>";
}
print "
</table>";
######### end of �\�Ҫ� ################
print "
</th>
<th bgcolor=yellow>�}�Ҧ~��</th><th>";
$g_string[1]="�@";
$g_string[2]="�G";
$g_string[3]="�T";
$g_string[4]="�|";
print "$g_string[$Input{grade}]�~��</th></tr><tr>
<th bgcolor=yellow>��ؽs��:</th><th>";
 print "$Input{id} <input type=hidden name=id value=$Input{id}>";
print "</th></tr><tr>
<th bgcolor=yellow>�Z�O</th>
<th>$Input{group}</th><input type=hidden name=group value=\"$Input{group}\">";
print "</th>
</tr>
<tr>
<th bgcolor=yellow>�½ҦѮv</th><th>";
# print "Input{Teacher} = $Input{Teacher}<br>";
 @temp = split(/\*:::\*/,$Input{Teacher});
 foreach $temp(@temp)
 {
  print $Teacher_Name{"$temp"},"<br>\n";
#  print $temp;
 }
 $Input{Teacher} = join(" ",@temp);
 print "<input type=hidden name=teacher value=\"$Input{Teacher}\">";
print "</th>
</tr>
<tr>
<th bgcolor=yellow>�ɼ�:</th>
<th>$Input{total_time}
<input type=hidden name=total_time value=$Input{total_time}></TH></TR>";
############################################################################
print qq(
  <tr><th bgcolor=yellow>����/������/�ѳ��Q�׮ɼ�:</th>
      <th>$Input{lab_time1}/$Input{lab_time2}/$Input{lab_time3}</th>
  <input type=hidden name=lab_time1 value=$Input{lab_time1}>
  <input type=hidden name=lab_time2 value=$Input{lab_time2}>
  <input type=hidden name=lab_time3 value=$Input{lab_time3}>
);
############################################################################

print "
</th>
</tr>
<tr>
<th bgcolor=yellow>�Ǥ�:</th>
<th>$Input{credit}
<input type=hidden name=credit value=$Input{credit}>";
print "
</th>
</tr>

<tr>
<th bgcolor=yellow>����/���/�q��</th>
<th>";
 if($Input{property}==1) { $name="����"; }
 if($Input{property}==2) { $name="���"; }
 if($Input{property}==3) { $name="�q��"; }
print $name;
print "<input type=hidden name=property value=$Input{property}>";

#print "
#<tr>
#<th bgcolor=yellow>�@��/�x�V/��|</th>
#<th>";
# if($Input{suffix_cd}==0) { $suffix_cd="�@��"; }
# if($Input{suffix_cd}==1) { $suffix_cd="�x�V"; }
# if($Input{suffix_cd}==2) { $suffix_cd="��|"; }
#print "$suffix_cd"; 
#print "<input type=hidden name=suffix_cd value=$Input{suffix_cd}>";

print "
</th>
</tr>
<tr>
<th bgcolor=yellow>�W�ұЫ�:</th>
<th>";
  %classroom=Read_Classroom($Input{classroom});
print "[$classroom{id}]$classroom{cname}";
print "<input type=hidden name=classroom value=\"$classroom{id}\">\n";
print "</th>
</tr>
<tr><th bgcolor=yellow>�z���h</th><th>\n";
my($p,@p_string);
$p_string[0]="���ݿz��";
$p_string[1]="�@���z��";
$p_string[2]="�G���z��";
print "$p_string[$Input{principle}]";
print "<input type=hidden name=principle value=$Input{principle}>";
print "</th></tr></table>\n";

## draw table for �Ƶ� ##
print "<table border=1>";
print "</select></th></tr>\n";
print "<tr><th bgcolor=yellow>���פH��</th><th>\n";
$temp=$Input{number_limit_2}*100+$Input{number_limit_1}*10+$Input{number_limit_0};
if($temp ne "0")
{
print "$temp �H";
}
else
{
 print "�L";
}
print "<input type=hidden name=number_limit value=$temp>\n";
print "</th>";
### �O�d�ǥͦW�B ###
print "<th bgcolor=yellow>�O�d�s�ͦW�B</th><th>\n";
$temp=$Input{reserved_number_2}*100+$Input{reserved_number_1}*10+$Input{reserved_number_0};
if($temp ne "0")
{
 print "$temp �H";
}
else
{
 print "�L";
}
print "<input type=hidden name=reserved_number value=$temp>\n";
print "</th></tr>\n";
print "<tr><th bgcolor=yellow rowspan=2>�䴩�t��</th><th rowspan=2>\n";
my(@temp,$temp,%temp);
if($Input{support_dept} ne "")
{
 @temp=split(/\*:::\*/,$Input{support_dept});
 foreach $temp(@temp)
 {
  %dept=Read_Dept($temp);
  print $dept{cname},"<br>";
 }
}
else
{
 print "�L";
}
print "</th><th bgcolor=yellow>�䴩�~��</th><th>\n";
my(@g_string);
$g_string[1]="�@";
$g_string[2]="�G";
$g_string[3]="�T";
$g_string[4]="�|";
if($Input{support_grade} ne "")
{
 @temp=split(/\*:::\*/,$Input{support_grade});
 foreach $temp(@temp)
 {
  print $g_string[$temp],"�~��<br>";
 }
}
else
{
 print "�L";
}
print "</th></tr><tr><th bgcolor=yellow>�䴩�Z��</th><th>\n";
if($Input{support_class} ne "")
{
 @temp=split(/\*:::\*/,$Input{support_class});
 foreach $temp(@temp)
 {
  print $temp,".";
 }
}
else
{
 print "�L";
}
print "</th>";
print "<input type=hidden name=support_dept value=$Input{support_dept}>\n";
print "<input type=hidden name=support_grade value=$Input{support_grade}>\n";
print "<input type=hidden name=support_class value=$Input{support_class}>\n";
print "</th></tr>\n";
### �ɭרt�� ###
print "<tr><th bgcolor=YELLOW rowspan=2>�ɭרt��</th><th rowspan=2>\n";
if($Input{ban_dept} ne "")
{
 @temp=split(/\*:::\*/,$Input{ban_dept});
 foreach $temp(@temp)
 {
  %dept=Read_Dept($temp);
  print $dept{cname},"<br>";
 }
}
else
{
 print "�L";
}
print "</th><th bgcolor=YELLOW>���צ~��</th><th>\n";
my(@g_string);
$g_string[1]="�@";
$g_string[2]="�G";
$g_string[3]="�T";
$g_string[4]="�|";
if($Input{ban_grade} ne "")
{
 @temp=split(/\*:::\*/,$Input{ban_grade});
 foreach $temp(@temp)
 {
  print $g_string[$temp],"�~��<br>";
 }
}
else
{
 print "�L";
}
print "</th></tr><tr><th bgcolor=YELLOW>���ׯZ��</th><th>\n";
if($Input{ban_class} ne "")
{
 @temp=split(/\*:::\*/,$Input{ban_class});
 foreach $temp(@temp)
 {
  print $temp,".";
 }
}
else
{
 print "�L";
}
print "</th>";
print "<input type=hidden name=ban_dept value=$Input{ban_dept}>\n";
print "<input type=hidden name=ban_grade value=$Input{ban_grade}>\n";
print "<input type=hidden name=ban_class value=$Input{ban_class}>\n";
print "</th></tr>\n";
####################  �䴩�q��  ####################################
$Input{support_cge_number} = $Input{support_cge_number_1} * 10 + $Input{support_cge_number_0};
print("<INPUT type=hidden name=support_cge_type   value=$Input{support_cge_type}>\n");
print("<INPUT type=hidden name=support_cge_number value=$Input{support_cge_number}>\n");
print qq(
  <TR><TH bgcolor=PINK>�䴩�q�ѻ��</TH>
     <TH colspan=3>$cge{$Input{support_cge_type}}{sub_cge_id_show} $cge{$Input{support_cge_type}}{cge_name}</TH>
  </TR>
  <TR><TH bgcolor=PINK>�䴩�q�ѤH��</TH>
      <TH colspan=3>$Input{support_cge_number}</TH>
  </TR>
);
######################################################################
print qq(
  <TR>
    <TH bgcolor=PINK>���׬��</TH>
    <TD colspan=3>
);
if($Input{Precourse} ne "99999") {
  @temp=split(/\*:::\*/,$Input{Precourse});
  print("<FONT size=-1>\n");
  foreach $temp(@temp) {
    ($predept, $precourse, $pregrade) = split(/:/, $temp);
    %dept_temp = Read_Dept($predept);
    %prerequisite_course = Read_Course($predept, $precourse, "01", "history");
    print("($dept_temp{cname2})($precourse)$prerequisite_course{cname} - $GRADE{$pregrade}<BR> ");
  }
} else {
  print "�L<BR>";
}
print("<input type=hidden name=Precourse value=$Input{Precourse}>\n");
print("($PREREQUISITE_LOGIC{$Input{prerequisite_logic}}<BR>)\n");
print("</TD></TR>");

######################################################################
#print qq(
#  <TR>
#    <TH bgcolor=PINK>���׬���޿����Y</TH>
#    <TD colspan=3>$Input{prerequisite_logic}</TD>
#  </TR>
#  <INPUT type=hidden name=prerequisite_logic value=$Input{prerequisite_logic}>
#);

######################################################################
print "<tr><th bgcolor=yellow>�Ƶ���</th>";
print "<th colspan=3>";
print $Input{note};
print "<input type=hidden name=note value=\"$Input{note}\">";
print "<input type=hidden name=password value=$Input{password}>";
print "</th></tr>
</table>
";
print "<p>
<center>
<input type=\"submit\" value=\"�T�w�H����ƶ}��\">
</form>";
END:
print "
<form>
<input type=button onclick=history.back() value=�^��W�@���ק���>
</form>
<hr>";
Links1($Input{dept_cd},$Input{grade},$Input{password});
print "
</center>
</body>
</html>";
 

## end of html file ##



