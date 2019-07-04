#!/usr/local/bin/perl
############################################################################
#####  Show_Course_2.cgi
#####  �d�߷�Ǵ��w�}���
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
<title>�d�߾Ǵ��w�}��ظ��- $temp{cname}</title>
</head>

<body bgcolor=white background=$GRAPH_URL"."ccu-sbg.jpg>
<center>
<table border=1>
<tr>
<th bgcolor=yellow>��ئW��(����)</th><th>";
 print "$Course{cname}";
print "
</th></tr>
<tr>
<th bgcolor=yellow>��ئW��(�^��)</th><th>";
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

######### end of �\�Ҫ� ################
print "</th>\n";
print "<th bgcolor=yellow>�}�Ҧ~��</th><th>";
$g_string[1]="�@";
$g_string[2]="�G";
$g_string[3]="�T";
$g_string[4]="�|";
print "$g_string[$Input{grade}]�~��</th></tr><tr>
<th bgcolor=yellow>��ؽs��:</th><th>";
 print "$Course{id}";
print "</th></tr><tr>
<th bgcolor=yellow>�Z�O</th>
<th>$Course{group}";
print "</th>
</tr>
<tr>
<th bgcolor=yellow>�½ҦѮv</th><th>";
 foreach $teacher( @{ $Course{teacher} } )
 {
  print $Teacher_Name{ $teacher },"<br>\n";
 }
print "</th>
</tr>
<tr>
<th bgcolor=yellow>�ɼ�:</th>
<th>$Course{total_time}";
###########################################################################
print qq(
  <tr><th bgcolor=yellow>���Үɼ�:<br>����ɼ�:<br>��߮ɼ�:</TH>
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
<th bgcolor=yellow>�Ǥ�:</th>
<th>$Course{credit}
</th>
</tr>
";
print "
<tr>
<th bgcolor=yellow>����/���/�q��</th>
<th>";
 if($Course{property}==1) { $name="����"; }
 if($Course{property}==2) { $name="���"; }
 if($Course{property}==3) { $name="�q��"; }
print "$name
</th>
</tr>";

#<tr>
#<th bgcolor=yellow>�@��/�x�V/��|</th>
#<th>";
# if($Course{suffix_cd}==0) { $suffix_cd="�@��"; }
# if($Course{suffix_cd}==1) { $suffix_cd="�x�V"; }
# if($Course{suffix_cd}==2) { $suffix_cd="��|"; }
#print "$suffix_cd
#</th>
#</tr>


print "
<tr>
<th bgcolor=yellow>�W�ұЫ�:</th>
<th>";
  %classroom=Read_Classroom($Course{classroom});
print "$classroom{cname}</th>
</tr>
<tr><th bgcolor=yellow>�z���h</th><th>\n";
my($p,@p_string);
$p_string[0]="���ݿz��";
$p_string[1]="�@���z��";
$p_string[2]="�G���z��";
print "$p_string[$Course{principle}]</th></tr></table>\n";

## draw table for �Ƶ� ##
print "<table border=1>";
print "</select></th></tr>\n";
print "<tr><th bgcolor=yellow>���פH��</th><th>\n";
if($Course{number_limit} eq "0")
{
 print "�L";
}
else
{
 print $Course{number_limit};
}
print "</th>";
### �O�d�ǥͦW�B ###
print "<th bgcolor=yellow>�O�d�W�B</th><th>\n";
if($Course{reserved_number} eq "0")
{
 print "�L";
}
else
{
 print $Course{reserved_number};
}
print "</th></tr>\n";
print "<tr><th bgcolor=yellow rowspan=2>�䴩�t��</th><th rowspan=2>\n";

my(@Dept,$dept,%Dept,$flag);

 foreach $ele(@{$Course{support_dept}})
 {
  %dept=Read_Dept($ele);
  print $dept{cname},"<br>\n";
 } 
 if($Course{support_dept} eq "") {print "�L";}
print "</th><th bgcolor=yellow>�䴩�~��</th><th>\n";
my(@g_string);
$g_string[1]="�@";
$g_string[2]="�G";
$g_string[3]="�T";
$g_string[4]="�|";
 foreach $ele(@{$Course{support_grade}})
 {
  print $g_string[$ele],"�~��<br>";
 }
 if($Course{support_grade} eq "") {print "�L";}
print "</th></tr><tr><th bgcolor=yellow>�䴩�Z��</th>\n";
print "<th>\n";
 foreach $ele( @{$Course{support_class}} )
 {
  print $ele,".";
 }
 if($Course{support_class} eq "") {print "�L";}
print "</th></tr>\n";
### �׭רt�� ###
print "<tr><th bgcolor=yellow rowspan=2>�׭רt��</th><th rowspan=2>\n";

 foreach $ele(@{$Course{ban_dept}})
 {
  %dept=Read_Dept($ele);
  print $dept{cname},"<br>\n";
 } 
 if($Course{ban_dept} eq "") {print "�L";}

print "</th><th bgcolor=yellow>�׭צ~��</th><th>\n";
my(@g_string);
$g_string[1]="�@";
$g_string[2]="�G";
$g_string[3]="�T";
$g_string[4]="�|";
 foreach $ele(@{$Course{ban_grade}})
 {
  print $g_string[$ele],"�~��<br>";
 }
 if($Course{ban_grade} eq ""){print "�L"; }
print "</th></tr><tr><th bgcolor=yellow>�׭ׯZ��</th>\n";
print "<th>";
 foreach $ele( @{$Course{ban_class}} )
 {
  print $ele,".";
 }
 if($Course{ban_class} eq "") { print "�L"; }
print "</th></tr>\n";

%cge = Read_Cge();
print "<TR><TH bgcolor=pink>�䴩�q�ѻ��</TH>
       <TH colspan=3>$cge{$Course{support_cge_type}}{sub_cge_id_show}$cge{$Course{support_cge_type}}{cge_name}</TH></TR>";
print "<TR><TH bgcolor=pink>�䴩�q�ѤH��</TH>
       <TH colspan=3>$Course{support_cge_number}</TH></TR>";
###############################################################################
print qq(
  <TR>
    <TH bgcolor=PINK>���׬��</TH>
    <TD colspan=3>
      <FONT size=-1>
);

foreach $pre_course (@{$Course{prerequisite_course}}) {
  if($$pre_course{id} eq "") {
    print ("�L");
  }else{
    %prerequisite_course = Read_Course($$pre_course{dept}, $$pre_course{id}, "01", "history");
    %predept = Read_Dept($$pre_course{dept});
    print qq(($predept{cname2})($$pre_course{id})$prerequisite_course{cname},$GRADE{$$pre_course{grade}}<BR>\n);
  }
} 

print qq(
  </TR>
  <TR>
    <TH bgcolor=PINK><FONT size=-1>���׬���޿����Y</TH>
    <TD colspan=3>$PREREQUISITE_LOGIC{$Course{prerequisite_logic}}</TD>
  </TR>
);
###############################################################################
if ($Course{distant_learning} == 1) {
  $flag_dis = "���Z�оǽҵ{";
}else{
  $flag_dis = "<FONT color=RED>�D</FONT>���Z�оǽҵ{";
}

if ($Course{english_teaching} == 1) {
  $flag_eng = "���^�y�½�";
}else{
  $flag_eng = "<FONT color=RED>�D</FONT>���^�y�½�";
}

print qq(
  <TR>
    <TH bgcolor=YELLOW>�W�Ҥ覡</TH>
    <TD colspan=3>
      $flag_dis<BR>
      $flag_eng
    </TD>
  </TR>
);


###############################################################################
print "<tr><th bgcolor=yellow>�Ƶ���</th>";
print "<th colspan=3>";
if($Course{note} eq "") { print "�L"; }
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



