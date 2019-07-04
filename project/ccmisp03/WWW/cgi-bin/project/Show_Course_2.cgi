#!/usr/local/bin/perl
############################################################################
#####  Show_Course_2.cgi
#####  查詢當學期已開科目
############################################################################

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Teacher.pm";

my(%Input,%Course,@Teacher);

%Input = User_Input();
@Teacher = Read_Teacher_File();

($Input{id},$Input{group})=split(/_/,$Input{id_group});

if($Input{group} eq "") { $Input{group} = "01" };

%Course=Read_Course( $Input{dept_cd}, $Input{id}, $Input{group} );
%temp=Read_Dept($Input{dept_cd});

print "Content-type: text/html","\n\n";

#foreach $k (keys %Course) {
#  print("$k --> $Course{$k}<br>\n");
#}


print "
<html>
<head>
<title>查詢學期已開科目資料- $temp{cname}</title>
</head>

<body bgcolor=white background=$GRAPH_URL"."ccu-sbg.jpg>
<center>
<table border=1>
<tr>
<th bgcolor=yellow>科目名稱(中文)</th><th>";
 print "$Course{cname}";
print "
</th></tr>
<tr>
<th bgcolor=yellow>科目名稱(英文)</th><th>";
 print "$Course{ename}";
print qq(
    </th></tr>
  </table><br>
  <table border=1>
  <tr>
    <th colspan=2 rowspan=13>
);

%time_table_cells = Format_Time(@{$Course{time}});
$time_table = Print_Timetable(%time_table_cells);
print $time_table;

######### end of 功課表 ################
print "</th>\n";
print "<th bgcolor=yellow>開課年級</th><th>";
$g_string[1]="一";
$g_string[2]="二";
$g_string[3]="三";
$g_string[4]="四";
print "$g_string[$Input{grade}]年級</th></tr><tr>
<th bgcolor=yellow>科目編號:</th><th>";
 print "$Course{id}";
print "</th></tr><tr>
<th bgcolor=yellow>班別</th>
<th>$Course{group}";
print "</th>
</tr>
<tr>
<th bgcolor=yellow>授課老師</th><th>";
 foreach $teacher( @{ $Course{teacher} } )
 {
  print $Teacher_Name{ $teacher },"<br>\n";
 }
print "</th>
</tr>
<tr>
<th bgcolor=yellow>時數:</th>
<th>$Course{total_time}";
###########################################################################
print qq(
  <tr><th bgcolor=yellow>正課時數:<br>實驗時數:<br>實習時數:</TH>
    <th>$Course{lab_time1}<br>
        $Course{lab_time2}<br>
        $Course{lab_time3}</th>
  </tr>
);
###########################################################################
print "
</th>
</tr>
<tr>
<th bgcolor=yellow>學分:</th>
<th>$Course{credit}
</th>
</tr>
";
print "
<tr>
<th bgcolor=yellow>必修/選修/通識</th>
<th>";
 if($Course{property}==1) { $name="必修"; }
 if($Course{property}==2) { $name="選修"; }
 if($Course{property}==3) { $name="通識"; }
print "$name
</th>
</tr>";

#<tr>
#<th bgcolor=yellow>一般/軍訓/體育</th>
#<th>";
# if($Course{suffix_cd}==0) { $suffix_cd="一般"; }
# if($Course{suffix_cd}==1) { $suffix_cd="軍訓"; }
# if($Course{suffix_cd}==2) { $suffix_cd="體育"; }
#print "$suffix_cd
#</th>
#</tr>


print "
<tr>
<th bgcolor=yellow>上課教室:</th>
<th>";
  %classroom=Read_Classroom($Course{classroom});
print "$classroom{cname}</th>
</tr>
<tr><th bgcolor=yellow>篩選原則</th><th>\n";
my($p,@p_string);
$p_string[0]="不需篩選";
$p_string[1]="一次篩選";
$p_string[2]="二次篩選";
print "$p_string[$Course{principle}]</th></tr></table>\n";

## draw table for 備註 ##
print "<table border=1>";
print "</select></th></tr>\n";
print "<tr><th bgcolor=yellow>限修人數</th><th>\n";
if($Course{number_limit} eq "0")
{
 print "無";
}
else
{
 print $Course{number_limit};
}
print "</th>";
### 保留學生名額 ###
print "<th bgcolor=yellow>保留名額</th><th>\n";
if($Course{reserved_number} eq "0")
{
 print "無";
}
else
{
 print $Course{reserved_number};
}
print "</th></tr>\n";
print "<tr><th bgcolor=yellow rowspan=2>支援系所</th><th rowspan=2>\n";

my(@Dept,$dept,%Dept,$flag);

 foreach $ele(@{$Course{support_dept}})
 {
  %dept=Read_Dept($ele);
  print $dept{cname},"<br>\n";
 } 
 if($Course{support_dept} eq "") {print "無";}
print "</th><th bgcolor=yellow>支援年級</th><th>\n";
my(@g_string);
$g_string[1]="一";
$g_string[2]="二";
$g_string[3]="三";
$g_string[4]="四";
 foreach $ele(@{$Course{support_grade}})
 {
  print $g_string[$ele],"年級<br>";
 }
 if($Course{support_grade} eq "") {print "無";}
print "</th></tr><tr><th bgcolor=yellow>支援班級</th>\n";
print "<th>\n";
 foreach $ele( @{$Course{support_class}} )
 {
  print $ele,".";
 }
 if($Course{support_class} eq "") {print "無";}
print "</th></tr>\n";
### 擋修系所 ###
print "<tr><th bgcolor=yellow rowspan=2>擋修系所</th><th rowspan=2>\n";

 foreach $ele(@{$Course{ban_dept}})
 {
  %dept=Read_Dept($ele);
  print $dept{cname},"<br>\n";
 } 
 if($Course{ban_dept} eq "") {print "無";}

print "</th><th bgcolor=yellow>擋修年級</th><th>\n";
my(@g_string);
$g_string[1]="一";
$g_string[2]="二";
$g_string[3]="三";
$g_string[4]="四";
 foreach $ele(@{$Course{ban_grade}})
 {
  print $g_string[$ele],"年級<br>";
 }
 if($Course{ban_grade} eq ""){print "無"; }
print "</th></tr><tr><th bgcolor=yellow>擋修班級</th>\n";
print "<th>";
 foreach $ele( @{$Course{ban_class}} )
 {
  print $ele,".";
 }
 if($Course{ban_class} eq "") { print "無"; }
print "</th></tr>\n";

%cge = Read_Cge();
print "<TR><TH bgcolor=pink>支援通識領域</TH>
       <TH colspan=3>$cge{$Course{support_cge_type}}{sub_cge_id_show}$cge{$Course{support_cge_type}}{cge_name}</TH></TR>";
print "<TR><TH bgcolor=pink>支援通識人數</TH>
       <TH colspan=3>$Course{support_cge_number}</TH></TR>";
###############################################################################
print qq(
  <TR>
    <TH bgcolor=PINK>先修科目</TH>
    <TD colspan=3>
      <FONT size=-1>
);

foreach $pre_course (@{$Course{prerequisite_course}}) {
  if($$pre_course{id} eq "") {
    print ("無");
  }else{
    %prerequisite_course = Read_Course($$pre_course{dept}, $$pre_course{id}, "01", "history");
    %predept = Read_Dept($$pre_course{dept});
    print qq(($predept{cname2})($$pre_course{id})$prerequisite_course{cname},$GRADE{$$pre_course{grade}}<BR>\n);
  }
} 

print qq(
  </TR>
  <TR>
    <TH bgcolor=PINK><FONT size=-1>先修科目邏輯關係</TH>
    <TD colspan=3>$PREREQUISITE_LOGIC{$Course{prerequisite_logic}}</TD>
  </TR>
);
###############################################################################
if ($Course{distant_learning} == 1) {
  $flag_dis = "遠距教學課程";
}else{
  $flag_dis = "<FONT color=RED>非</FONT>遠距教學課程";
}

if ($Course{english_teaching} == 1) {
  $flag_eng = "全英語授課";
}else{
  $flag_eng = "<FONT color=RED>非</FONT>全英語授課";
}

print qq(
  <TR>
    <TH bgcolor=YELLOW>上課方式</TH>
    <TD colspan=3>
      $flag_dis<BR>
      $flag_eng
    </TD>
  </TR>
);


###############################################################################
print "<tr><th bgcolor=yellow>備註欄</th>";
print "<th colspan=3>";
if($Course{note} eq "") { print "無"; }
else 
{
 $Course{note} =~tr/\n/<br>/;
 print $Course{note}; }
print "</th></tr>
</table><hr>
";
Links1($Input{dept_cd},$Input{grade},$Input{password});
print "<p>
</center>
</body>
</html>";
 

## end of html file ##



