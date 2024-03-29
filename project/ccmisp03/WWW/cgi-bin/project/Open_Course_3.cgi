#!/usr/local/bin/perl
########################################################################
#####  Open_Course_3.cgi
#####  開課介面
#####  Last Update:
#####   2002/03/14 加入 75 分鐘課程, 修改功課表, 修改檢核 (Nidalap :D~)
########################################################################

print "Content-type: text/html","\n\n";

require "../library/Reference.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."Open_Course.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Teacher.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Error_Message.pm";

my(%Input,@Date,$i,@teacher);

@teacher = Read_Teacher_File();

$i=0;
%Input		= User_Input();
%cge		= Read_Cge();
@all_course	= Find_All_Course($Input{dept_cd}, "", "");

Check_SU_Password($Input{password}, "dept", $Input{dept_cd});
%classroom = Read_Classroom($Input{classroom});
  
#foreach $k (keys %Input) {
#  print("$k --> $Input{$k}<br>\n");
#}
@selected_time = Find_Selected_Time();

foreach $selected_time (@selected_time) { 
  if($$selected_time{time} >= 1) {           ### 如果是數字截次 -> 1 hr
    $total_selected_time ++;
  }else{                                     ### 如果是英文截次 -> 1.5 hr
    $total_selected_time += 1.5;
  }
}
# print("total selected = $total_selected_time<BR>\n");

if($Input{group} eq "") { $Input{group} = "01" };

%temp=Read_Dept($Input{dept_cd});
$su_flag = "(SU)"  if($SUPERUSER == 1);

#####  非管理者, 若有限修, 則 限修人數 == 教室最適容量
#####  added 2002/11/19, Nidalap :D~
if( $SUPERUSER != 1 ) {                    ###  非管理者
  if( $Input{principle} == 0 ) {           ###   若不限修
    $Input{number_limit_0} = $Input{number_limit_1} = $Input{number_limit_2} = 0;
  }else{                                   ###   若有限修
    ($Input{number_limit_0}, $Input{number_limit_1}, $Input{number_limit_2})
        = Numeric_to_chars($classroom{size_fit}); 
  }
}else{                                     ###  管理者
    ### (do nothing)
}                    
#############################################################################
print qq(
  <html>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <head><title>新增學期開課[開課確認]- $temp{cname} $su_flag</title></head>
    <body bgcolor=white background=$GRAPH_URL/ccu-sbg.jpg>
      <center>
        <H1>新增當學期開課資料(開課資料確認)<HR></H1>
);
## check area ##
my($line,@error_string);
$line=0;
$error=0;
$fatal_error=0;

#$time_string="A/1/2/3/4/F/B/5/6/7/8/C/D/E";
#$week_string="日/一/二/三/四/五/六";     

($warning_count, $error_count, @error_message) = 
                          Check_Open_Course_Restrictions("add", %Input);

if( $warning_count + $error_count > 0) {
  print("<FONT size=4 color=red>系統檢查開課資料結果如下</FONT><BR>\n");
  print("<TABLE border=0 size=85%>");
  print("  <TR><TD><OL>");
  foreach $error (@error_message) {
    print("<LI>$error");
    $temp++;
  }
  print("</TD></TR></TABLE>");
  if( $error_count > 0 ) {
    exit(1);
  }
}

#$temp=join("*:::*",@Date);
$temp = "";
@selected_time = sort by_time @selected_time;
foreach $time (@selected_time) {
  if( $temp ne "" ) {
    $temp .= "*:::*";
  }
  $temp = $temp . $$time{week} . "_" . $$time{time};
}
$Input{cname_show} = $Input{cname};
$Input{ename_show} = $Input{ename};

$Input{cname} =~ s/\"/”/g;
$Input{ename} =~ s/\"/”/g;

print qq(
  <hr>
  <form method=post action=Open_Course_4.cgi>
    <input type=hidden name=grade value=$Input{grade}>
    <input type=hidden name=dept_cd value=$Input{dept_cd}>
    <input type=hidden name=date value=$temp>
    <table border=1>
      <tr>
        <th bgcolor=yellow>科目名稱(中文)</th>
        <th>$Input{cname_show}<input type=hidden name=cname value="$Input{cname}">
        </th>
      </tr>
      <tr>
        <th bgcolor=yellow>科目名稱(英文)</th>
        <th>$Input{ename_show}<input type=hidden name=ename value="$Input{ename}"></th>
      </tr>
    </table><br>
    <table border=1>
      <tr>
        <th colspan=2 rowspan=13>
);
%time_table_cells = Format_Time(@selected_time);
$time_table = Print_Timetable(%time_table_cells);
print $time_table;

# print "</th>";
# for($i=1;$i<=7;$i++)
# {
#  $k="$i"."_$j";
#  $CHECK=0;
#  foreach $ele (@Date) {
#    if($k eq $ele)
#    {
#     $CHECK=1;
#     goto OUT;
#    } 
#  }
#  OUT:
#  if($CHECK==1)
#  {
#   print "<th><img src=$GRAPH_URL"."Scheck.gif></th>\n";
#  }
#  else
#  {
#   print "<th>&nbsp</th>\n";
#  }
# }
# print "</tr>";
#}
#print "
#</table>";
######### end of 功課表 ################
print "
</th>
<th bgcolor=yellow>開課年級</th><th>";
$g_string[1]="一";
$g_string[2]="二";
$g_string[3]="三";
$g_string[4]="四";
print "$g_string[$Input{grade}]年級</th></tr><tr>
<th bgcolor=yellow>科目編號:</th><th>";
 print "$Input{id} <input type=hidden name=id value=$Input{id}>";
print "</th></tr><tr>
<th bgcolor=yellow>班別</th>
<th>$Input{group}</th><input type=hidden name=group value=\"$Input{group}\">";
print "</th>
</tr>
<tr>
<th bgcolor=yellow>授課老師</th><th>";
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
<th bgcolor=yellow>時數:</th>
<th>$Input{total_time}
<input type=hidden name=total_time value=$Input{total_time}></TH></TR>";
############################################################################
print qq(
  <tr><th bgcolor=yellow>正課/實驗實習/書報討論時數:</th>
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
<th bgcolor=yellow>學分:</th>
<th>$Input{credit}
<input type=hidden name=credit value=$Input{credit}>";
print "
</th>
</tr>

<tr>
<th bgcolor=yellow>必修/選修/通識</th>
<th>";
 if($Input{property}==1) { $name="必修"; }
 if($Input{property}==2) { $name="選修"; }
 if($Input{property}==3) { $name="通識"; }
print $name;
print "<input type=hidden name=property value=$Input{property}>";

#print "
#<tr>
#<th bgcolor=yellow>一般/軍訓/體育</th>
#<th>";
# if($Input{suffix_cd}==0) { $suffix_cd="一般"; }
# if($Input{suffix_cd}==1) { $suffix_cd="軍訓"; }
# if($Input{suffix_cd}==2) { $suffix_cd="體育"; }
#print "$suffix_cd"; 
#print "<input type=hidden name=suffix_cd value=$Input{suffix_cd}>";

print qq(
  </th>
  </tr>
  <tr>
  <th bgcolor=yellow>上課教室:</th>
  <th>
);
print "[$classroom{id}]$classroom{cname}";
print "<input type=hidden name=classroom value=\"$classroom{id}\">\n";
print "</th>
</tr>
<tr><th bgcolor=yellow>篩選原則</th><th>\n";

my($p,@p_string);
$p_string[0]="不需篩選";
$p_string[1]="一次篩選";
$p_string[2]="二次篩選";
print "$p_string[$Input{principle}]";
print "<input type=hidden name=principle value=$Input{principle}>";
print "</th></tr></table>\n";

## draw table for 備註 ##
print "<table border=1>";
print "</select></th></tr>\n";
print "<tr><th bgcolor=yellow>限修人數</th><th>\n";

$temp = $Input{number_limit_2}*100+$Input{number_limit_1}*10+$Input{number_limit_0};

if($temp ne "0") {
  print "$temp 人";
}else{
  print "無";
}

print "<input type=hidden name=number_limit value=$temp>\n";
print "</th>";
### 保留學生名額 ###
print "<th bgcolor=yellow>保留新生名額</th><th>\n";
$temp=$Input{reserved_number_2}*100+$Input{reserved_number_1}*10+$Input{reserved_number_0};
if($temp ne "0")
{
 print "$temp 人";
}
else
{
 print "無";
}
print "<input type=hidden name=reserved_number value=$temp>\n";
print "</th></tr>\n";
print "<tr><th bgcolor=yellow rowspan=2>支援系所</th><th rowspan=2>\n";
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
 print "無";
}
print "</th><th bgcolor=yellow>支援年級</th><th>\n";
my(@g_string);
$g_string[1]="一";
$g_string[2]="二";
$g_string[3]="三";
$g_string[4]="四";
if($Input{support_grade} ne "")
{
 @temp=split(/\*:::\*/,$Input{support_grade});
 foreach $temp(@temp)
 {
  print $g_string[$temp],"年級<br>";
 }
}
else
{
 print "無";
}
print "</th></tr><tr><th bgcolor=yellow>支援班級</th><th>\n";
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
 print "無";
}
print "</th>";
print "<input type=hidden name=support_dept value=$Input{support_dept}>\n";
print "<input type=hidden name=support_grade value=$Input{support_grade}>\n";
print "<input type=hidden name=support_class value=$Input{support_class}>\n";
print "</th></tr>\n";
### 擋修系所 ###
print "<tr><th bgcolor=YELLOW rowspan=2>擋修系所</th><th rowspan=2>\n";
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
 print "無";
}
print "</th><th bgcolor=YELLOW>限修年級</th><th>\n";
my(@g_string);
$g_string[1]="一";
$g_string[2]="二";
$g_string[3]="三";
$g_string[4]="四";
if($Input{ban_grade} ne "")
{
 @temp=split(/\*:::\*/,$Input{ban_grade});
 foreach $temp(@temp)
 {
  print $g_string[$temp],"年級<br>";
 }
}
else
{
 print "無";
}
print "</th></tr><tr><th bgcolor=YELLOW>限修班級</th><th>\n";
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
 print "無";
}
print "</th>";
print "<input type=hidden name=ban_dept value=$Input{ban_dept}>\n";
print "<input type=hidden name=ban_grade value=$Input{ban_grade}>\n";
print "<input type=hidden name=ban_class value=$Input{ban_class}>\n";
print "</th></tr>\n";
####################  支援通識  ####################################
$Input{support_cge_number} = $Input{support_cge_number_1} * 10 + $Input{support_cge_number_0};
print("<INPUT type=hidden name=support_cge_type   value=$Input{support_cge_type}>\n");
print("<INPUT type=hidden name=support_cge_number value=$Input{support_cge_number}>\n");
print qq(
  <TR><TH bgcolor=PINK>支援通識領域</TH>
     <TH colspan=3>$cge{$Input{support_cge_type}}{sub_cge_id_show} $cge{$Input{support_cge_type}}{cge_name}</TH>
  </TR>
  <TR><TH bgcolor=PINK>支援通識人數</TH>
      <TH colspan=3>$Input{support_cge_number}</TH>
  </TR>
);
######################################################################
print qq(
  <TR>
    <TH bgcolor=PINK>先修科目</TH>
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
  print "無<BR>";
}
print("<input type=hidden name=Precourse value=$Input{Precourse}>\n");
print("($PREREQUISITE_LOGIC{$Input{prerequisite_logic}}<BR>)\n");
print("</TD></TR>");

######################################################################
#print qq(
#  <TR>
#    <TH bgcolor=PINK>先修科目邏輯關係</TH>
#    <TD colspan=3>$Input{prerequisite_logic}</TD>
#  </TR>
#  <INPUT type=hidden name=prerequisite_logic value=$Input{prerequisite_logic}>
#);

######################################################################

if ($Input{distant_learning} eq "on") {
  $flag_dis = "遠距教學課程";
  $Input{distant_learning} = 1;
}else{
  $flag_dis = "<FONT color=RED>非</FONT>遠距教學課程";
  $Input{distant_learning} = 0;
}

if ($Input{english_teaching} eq "on") {
  $flag_eng = "全英語授課";
  $Input{english_teaching} = 1;
}else{
  $flag_eng = "<FONT color=RED>非</FONT>全英語授課";
  $Input{english_teaching} = 0;
}
    
print qq(
  <TR>
    <TH bgcolor=YELLOW>上課方式</TH>
    <TD colspan=3>
      $flag_dis<BR>
      $flag_eng
    </TD>
  </TR>
  <INPUT type=hidden name=distant_learning value=$Input{distant_learning}>
  <INPUT type=hidden name=english_teaching value=$Input{english_teaching}>
);
#######################################################################
print "<tr><th bgcolor=yellow>備註欄</th>";
print "<th colspan=3>";
print $Input{note};
print "<input type=hidden name=note value=\"$Input{note}\">";
print "<input type=hidden name=password value=$Input{password}>";
print "</th></tr>
</table>
";
print "<p>
<center>
<input type=\"submit\" value=\"確定以此資料開課\">
</form>";
END:
print "
<form>
<input type=button onclick=history.back() value=回到上一頁修改資料>
</form>
<hr>";
Links1($Input{dept_cd},$Input{grade},$Input{password});
print "
</center>
</body>
</html>";
 

## end of html file ##


############################################################################
#####  Find Selected_Time
#####  讀取上一頁所選取的開課截次
############################################################################
sub Find_Selected_Time
{
  my(@time, $i, $week, $time);
  $i = 0;
  foreach $key (sort %Input) {
    if($Input{$key} eq "999") {
#      print("$key<BR>\n");
      ($week, $time) = split(/_/, $key);
      $time[$i]{week} = $week;
      $time[$i]{time} = $time;
      $i++;
    }
  }
  return(@time);
}
############################################################################
sub by_time()
{
  if( $$a{week} eq $$b{week} ) {
    if( ($$a{time} =~ /[A-Z]/) or ($$b{time} =~ /[A-Z]/) ) {
      return( $$a{time} cmp $$b{time} );
    }else{
      return( $$a{time} <=> $$b{time} );
    }
  }else{
    return( $$a{week} <=> $$b{week} );
  }
}
#############################################################################