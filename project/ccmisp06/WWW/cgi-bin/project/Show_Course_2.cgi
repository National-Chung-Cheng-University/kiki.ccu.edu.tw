#!/usr/local/bin/perl
##########################################################################################
#####  Show_Course_2.cgi
#####  查詢當學期已開科目
#####  Updates:
#####   2009/05/05 加入暑修課程類型 remedy 欄位 (1為一般，2為補救)  Nidalap :D~
#####   2009/05/05 兩門以上先修科目，才顯示先修科目邏輯關係  Nidalap :D~
#####   2010/03/19 加入 教師專長與授課科目是否符合 $s_match 欄位 Nidalap :D~
#####   2010/04/08 體育中心和軍訓開課，不顯示 s_match 欄位  Nidalap :D~
#####   2010/05/25 s_match 出現與否，改為交給 Need_s_match() 判斷  Nidalap :D~
#####   2010/11/24 加入 gender_eq, env_edu 兩個欄位  Nidalap :D~
#####   2012/05/09 加入開課學制 attr 欄位  Nidalap :D~
#####   2015/04/16 因應文學院需求-委由各系實際執行開課，新增 $open_dept 變數  Nidalap :D~
##########################################################################################

print "Content-type: text/html","\n\n";

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Open_Course.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Teacher.pm";

my(%Input,%Course,@Teacher);

%Input = User_Input();

@Teacher = Read_Teacher_File();
($Input{id},$Input{group})=split(/_/,$Input{id_group});

if($Input{group} eq "") { $Input{group} = "01" };

%Course=Read_Course( $Input{dept_cd}, $Input{id}, $Input{group});
%Dept=Read_Dept($Input{dept_cd});

#Print_Hash(%Dept);

if( $Dept{id} eq $DEPT_LAN ) {                                                  ### 語言中心可開通識外語課
  if( $Input{grade} eq "cge_lan" ) {
    $cge_lan_flag = 2;                                                                  ###  語言中心，且選擇了通識外語課
  }else{
    $cge_lan_flag = 1;                                                                  ###  語言中心，尚未選擇通識外語課
  }
}


#foreach $k (keys %Course) {
#  print("$k --> $Course{$k}<br>\n");
#}
#foreach $k (keys %Input) {
#  print("$k ---> $Input{$k}<br>");
#}

$title = $SUB_SYSTEM_NAME . "開排課系統-- 查詢當學期已開科目";
print Print_Open_Course_Header(\%Input, \%Dept, $title);

print "
  <table border=1>
    <tr>
      <th bgcolor=yellow>科目名稱(中文)</th><th>" . $Course{cname} . "</th>
	</tr>
	<tr>
	  <th bgcolor=yellow>科目名稱(英文)</th><th>" . $Course{ename} . "
    </th></tr>
  </table><br>
  <table border=1>
  <tr>
    <th colspan=2 rowspan=13>
";

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
print "</th></tr>";
############################################################################
#####  教師專長與授課科目是否符合
if(  Need_s_match($Input{dept_cd}) ) {
  print qq(
    <tr><th bgcolor=yellow>教師專長與授課科目是否符合</th><th>$S_MATCH{$Course{s_match}}</th></tr>
    <input type=hidden name=s_match value=$Input{s_match}>
  );
}
############################################################################

print "
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
<th bgcolor=yellow>上課教室</th>
<th>";
  %classroom=Read_Classroom($Course{classroom});
print "$classroom{cname}</th>
</tr>
<tr><th bgcolor=yellow>篩選原則</th><th>\n";
my($p,@p_string);
$p_string[0]="不需篩選";
$p_string[1]="一次篩選";
$p_string[2]="二次篩選";
print "$p_string[$Course{principle}]</th></tr>";

#####  顯示「開課學制」欄位(非專班的研究所)  2012/05/09  Nidalap :D~
if( !$IS_GRA and !is_Undergraduate_Dept($Dept{id}) and !is_Exceptional_Dept($Dept{id}) ) {
  $show_attr = 1;
  print "<tr><th bgcolor=yellow>開課學制</th><th>" . $ATTR{$Course{attr}} . "</th>";
}

print "</table>\n";

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

if( @{$Course{prerequisite_course}} >= 2 ) {			### 兩門以上先修科目，才顯示此欄位
  print("<BR>$PREREQUISITE_LOGIC{$Course{prerequisite_logic}}");
}
print("</TD></TR>");
#print qq(
#  </TR>
#  <TR>
#    <TH bgcolor=PINK><FONT size=-1>先修科目邏輯關係</TH>
#    <TD colspan=3>$PREREQUISITE_LOGIC{$Course{prerequisite_logic}}</TD>
#  </TR>
#);
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
if ($Course{gender_eq} == 1) {
  $flag_gen = "性別平等教育課程";
}else{
  $flag_gen = "<FONT color=RED>非</FONT>性別平等教育課程";
}

if ($Course{env_edu} == 1) {
  $flag_env = "環境教育相關課程";
}else{
  $flag_env = "<FONT color=RED>非</FONT>環境教育相關課程";
}


print qq(
  <TR>
    <TH bgcolor=YELLOW>上課方式</TH>
    <TD colspan=3>
      $flag_dis<BR>
      $flag_eng<BR>
      $flag_gen<BR>
      $flag_env
    </TD>
  </TR>
);

########################################################################
#####  Added 2009/05/05  Nidalap :D~
#####  暑期授課辦法修訂，暑期所開授之課程分為以下兩類： 
#####  第一類課程：經系（所、中心）課程委員會議審議通過之選修課程。
#####  第二類課程：曾開授之課程，以補救教學為原則。 
#####  請於暑期開排課系統增加選項，排課人員得勾選課程類別，
#####  以利後端課務系統計算最低開課人數、課程收費標準等計算教師鐘點資料。

#if( is_Summer() ) {
if( is_Summer() and !is_GRA() ) {       ### 只作用於「一般生暑修」
  @flag_remedy = ("",
      "第一類課程：經系（所、中心）課程委員會議審議通過之選修課程",
      "第二類課程：曾開授之課程，以補救教學為原則");
  print qq( 
    <tr><th bgcolor=yellow>暑修課程類型</th>
      <td colspan=3>
        $flag_remedy[$Course{remedy}]
      </TD>
    </TR>
    <INPUT type=hidden name=remedy value=$Input{remedy}>
  );
}


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
if( $Input{cge_lan_flag} == 2 ) { $Input{dept_cd} = $DEPT_LAN;  $Input{grade} = 1}  ### 若是語言中心開通識外語課，還原系所代碼為語言中心

Links1($Input{dept_cd},$Input{grade},$Input{password});
print "<p>
</center>
</body>
</html>";
 

## end of html file ##



