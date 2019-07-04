#!/usr/local/bin/perl
########################################################################
#####  Open_Course_2.cgi
#####  �}�Ҥ���
#####  Last Update:
#####   2002/03/14 �[�J 75 �����ҵ{, �ק�\�Ҫ� (Nidalap :D~)
########################################################################
$| = 1;
print "Content-type: text/html","\n\n";

require "../library/Reference.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Open_Course.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Error_Message.pm";

my(%Input);

%Input		= User_Input();
%cge		= Read_Cge();
@all_course	= Find_All_Course($Input{dept_cd}, "", "history");

Check_SU_Password($Input{password}, "dept", $Input{dept_cd});

if($Input{group} eq "") { $Input{group} = "01" };

if($Input{course_cd} eq "")  {
  $Input{course_cd} = "new";
}
if($Input{course_cd} ne "new") {
  if($Input{course_cd}=~/new/)  {
    ($Input{course_cd},$useless)=split(/\s/,$Input{course_cd});
    %Course = Read_Course( $Input{dept_cd}, $Input{course_cd}, $Input{group},"");
  }else{
    %Course = Read_Course( $Input{dept_cd}, $Input{course_cd}, $Input{group},"history");
  }
}else{
   $new_course_flag = 1;
}
%temp=Read_Dept($Input{dept_cd});

$|=0;
print qq(
  <html>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <head><title>�s�W�Ǵ��}��- $temp{cname}</title></head>
);
Add_JS();  ## function to add JavaScript Code

print qq(
  <body bgcolor=white background=$GRAPH_URL/ccu-sbg.jpg>
  <center>
  <form name=form1 method=post action=Open_Course_3.cgi>
    <input type=hidden name=dept_cd value=$Input{dept_cd}>
    <input type=hidden name=password value=$Input{password}>
    <input type=hidden name=new_course_flag value=$new_course_flag>
    <table border=1>
      <tr>
      <th bgcolor=yellow>��ئW�١]����^</th><th>
);
if($Input{course_cd} ne "new" && $SUPERUSER ne "1") {
  print "$Course{cname}<input type=hidden name=cname value=\"$Course{cname}\">";
}else{
  print "<input type=text length=70 name=cname value=\"$Course{cname}\">";
}
print qq(
    </th></tr>
  <tr>
    <th bgcolor=yellow>��ئW�١]�^��^</th><th>
);
#$Course{cname} =~ s/"/\"/g;
#$Course{ename} =~ s/"/\"/g;
if($Input{course_cd} ne "new" && $SUPERUSER ne "1") {
  print qq($Course{ename}<input type=hidden name=ename value="$Course{ename}">);
}else{
  print qq(<input type=text length=70 name=ename value="$Course{ename}">);
}
print qq(
    </th></tr></table><br>
    <table border=1>
      <tr>
        <th colspan=2 rowspan=12 valign=TOP>
);
Print_Timetable_Select();

######### end of �\�Ҫ� ################
print "</th>\n";
print "<th bgcolor=yellow>�}�Ҧ~��</th><th><select name=grade>";
$g_string[1]="�@";
$g_string[2]="�G";
$g_string[3]="�T";
$g_string[4]="�|";

if( ($Input{dept_cd} =~ /6$/) and ($Input{dept_cd} != "7006") ) {  ###  ���F�q�ѥH�~����s��
  print "<option value=1 selected>$g_string[1]�~��\n";             ###  �u���@�~��
}else{                                                             ###  ��L�t�ҥi�H��1~4�~��
  for($i=1;$i<5;$i++) {
   if($i == $Input{grade}) {
     print "<option value=$i selected>$g_string[$i]�~��\n";
   }else{
     print "<option value=$i>$g_string[$i]�~��\n";
   }
  }
}
print "</select></th></tr><tr>
<th bgcolor=yellow>��ؽs��:</th><th>";
if($Input{course_cd} ne "new")
{
 print "$Course{id}<input type=hidden name=id value=$Course{id} maxlength=7>";
}
else
{
 print "<input type=text length=10 name=id>";
}
print "</th></tr><tr>
<th bgcolor=yellow>�Z�O</th>
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
<th bgcolor=yellow>�½ҦѮv</th>";

#### read teacher_code and name of this department####
print "
<th><select name=Teacher size=3 multiple onblur=\"isDelete(document.form1.Teacher)\">
<option value=99999 selected>�Юv���w
</select></th>
</tr>
<tr><th bgcolor=yellow>��ܱ½ұЮv</th>
<th>";
print "
<input type=button name=btn1 value=��ܥ��ұЮv onclick=\"AddWin()\"> 
<input type=button name=btn2 value=���m onClick=\"ClearAll(document.form1.Teacher)\">
</th></tr>
</tr>
<tr>
<th bgcolor=yellow>�ɼ�:</th>
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
    <th bgcolor=yellow>����/<BR>������/<BR>�ѳ��Q�׮ɼ�:</th>
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
<th bgcolor=yellow>�Ǥ�:</th>
<TH>";
#if($Course{credit} == "" )  {
if($Input{course_cd} eq "new") {      ### �s�W��ؤ~���Ǥ�
  print("<SELECT name=credit>\n");
  for($temp=0; $temp<7; $temp++) {
    print("<OPTION>$temp\n");
  }
  print("</SELECT>");
}else{                                ### ���~��ؤ@�ߤ��i��
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
<th bgcolor=yellow>����/���/�q��</th>
<th><select name=property>";
for($i=1;$i<=3;$i++)
{
 if($i==1) { $name="����"; }
 if($i==2) { $name="���"; }
 if($i==3) { $name="�q��"; }
 if($i eq $Course{property} )
 { print "<option value=$i selected>$name"; }
 else
 { print "<option value=$i>$name"; } 
}

#print "
#</select>
#<tr>
#<th bgcolor=yellow>�@��/�x�V/��|</th>
#<th><select name=suffix_cd>";
#for($i=0;$i<=2;$i++)
#{
# if($i==0) { $suffix_cd="�@��"; }
# if($i==1) { $suffix_cd="�x�V"; }
# if($i==2) { $suffix_cd="��|"; }
# if($i eq $Course{suffix_cd} )
# { print "<option value=$i selected>$suffix_cd"; }
# else
# { print "<option value=$i>$suffix_cd"; }
#}

print qq(
  </select>
  </th>
  </tr>
  <tr>
  <th bgcolor=yellow>�W�ұЫ�:</th>
  <th><select name=classroom>
);

%classroom = Read_All_Classroom();
foreach $classroom_id (sort keys %classroom) {
  if( $classroom_id eq $Course{classroom} ) {
    print "<option value=$classroom_id SELECTED>
           $classroom{$classroom_id}{cname}($classroom{$classroom_id}{size_fit})\n"; 
  }else{ 
    print "<option value=$classroom_id>
           $classroom{$classroom_id}{cname}($classroom{$classroom_id}{size_fit})\n"; 
  }
}

print qq(
    </select></th>
  </tr>
  </TABLE>
);

########################  �H�U�O�\�Ҫ��U������� #######################

print qq(
  <TABLE border=1>
    <TR>
      <TH bgcolor=yellow>�H�ƿz��</TH>
      <TH colspan=2 align=RIGHT>�z���h: <select name=principle>\n
);
my($p,@p_string);
$p_string[0]="���ݿz��";
$p_string[1]="�@���z��";
$p_string[2]="�G���z��";
for($p=0;$p<3;$p++) {
  ### �u����s�ҷ|�� "���ݿz��"(�q�� 7006 �]���i�� "���ݿz��)
  if( $SUPERUSER != 1 ) {
    if( ($Input{dept_cd} !~ /6$/) or ($Input{dept_cd} eq "7006") ) {
      next if( $p == 0 );                 ###  2002/11/20 Nidalap :D~
    }
  }
  if( $TERM == 2 ) {                      ###  �ĤG�Ǵ����, �u�� "�@���z��"
    next if($p == 2);                     ###  2002/12/02, Nidalap :D~
#  }elsif( $TERM == 1 ) {                  ###  �Ĥ@�Ǵ����, �u�� "�G���z��"
#    next if($p == 1);                     ###  2005/04/12, Nidalap :D~
  }
  if($p ne $Course{principle}) { 
    print "<option value=$p>$p_string[$p]\n";
  }else{
    print "<option value=$p selected>$p_string[$p]\n"; 
  }
}
print qq(
      </SELECT><BR>
    ���פH��: 
);
if($SUPERUSER != 1) {           #####  �D�޲z��, ����קﭭ�פH��
  print("(���W�ұЫǿﶵ��A��)<BR>");
}else{                          #####  �޲z��, �i�H�קﭭ�פH��
  print qq( <select name=number_limit_2> );
  my($i, @limit_chars);
  @limit_chars = Numeric_to_chars($Course{number_limit});
  for($i=0;$i<10;$i++) {
   if($i ne $limit_chars[2]) { 
     print "<option value=$i>$i\n"; 
   }else{ 
     print "<option value=$i selected>$i\n"; 
   }
  }
  print "</SELECT><SELECT name=number_limit_1>";
  for($i=0;$i<10;$i++) {
   if($i ne $limit_chars[1]) { 
     print "<option value=$i>$i\n"; 
   }else{
     print "<option value=$i selected>$i\n"; 
   }
  }
  print "</select><select name=number_limit_0>";
  for($i=0;$i<10;$i++) {
    if($i ne $limit_chars[0]) { 
      print "<option value=$i>$i\n"; 
    }else{ 
      print "<option value=$i selected>$i\n"; 
    }
  }
  print "</SELECT><BR>";
}
### �O�d�ǥͦW�B ###
print "�O�d�s�ͦW�B: <SELECT name=reserved_number_2>";
my($i, @limit_chars);
@reserved_chars = Numeric_to_chars($Course{reserved_number});

for($i=0;$i<10;$i++) {
 if($i ne $reserved_chars[2]) { 
   print "<option value=$i>$i\n"; 
 }else{ 
   print "<option value=$i selected>$i\n"; 
 }
}
print "</select><select name=reserved_number_1>";
for($i=0;$i<10;$i++) {
 if($i ne $reserved_chars[1]) { 
   print "<option value=$i>$i\n"; 
 }else{ 
   print "<option value=$i selected>$i\n"; 
 }
}
print "</select><select name=reserved_number_0>";
for($i=0;$i<10;$i++) {
 if($i ne $reserved_chars[0]) { 
   print "<option value=$i>$i\n"; 
 }else{ 
   print "<option value=$i selected>$i\n"; 
 }
}
print "</select></th></tr>\n";
print "<tr><th bgcolor=yellow rowspan=2>�䴩�t��</th><th rowspan=2>\n";
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
print "</select></th><th bgcolor=yellow>�䴩�~��</th><th>\n";
print "<select name=support_grade size=2 multiple>";
my(@g_string);
$g_string[1]="�@";
$g_string[2]="�G";
$g_string[3]="�T";
$g_string[4]="�|";
for($i=1;$i<=4;$i++)
{
 $flag=0;
 foreach $ele(@{$Course{support_grade}})
 {
  if($ele eq $i)
  { $flag=1; break; }
 }
 if($flag == 1)
 { print "<option value=$i selected>$g_string[$i]�~��\n"; }
 else
 { print "<option value=$i>$g_string[$i]�~��\n"; } 
}
print "</select></th></tr><tr><th bgcolor=yellow>�䴩�Z��</th>\n";
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
### �׭רt�� ###
print "<tr><th bgcolor=YELLOW rowspan=2>�׭רt��</th><th rowspan=2>\n";
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
print "</select></th><th bgcolor=YELLOW>�׭צ~��</th><th>\n";
print "<select name=ban_grade size=2 multiple>";
my(@g_string);
$g_string[1]="�@";
$g_string[2]="�G";
$g_string[3]="�T";
$g_string[4]="�|";
for($i=1;$i<=4;$i++)
{
 $flag=0;
 foreach $ele(@{$Course{ban_grade}})
 {
  if($ele eq $i)
  { $flag=1; break; }
 }
 if($flag == 1)
 { print "<option value=$i selected>$g_string[$i]�~��\n"; }
 else
 { print "<option value=$i>$g_string[$i]�~��\n"; } 
}
print "</select></th></tr><tr><th bgcolor=YELLOW>�׭ׯZ��</th>\n";
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

################### �䴩�q�ѻ��ΤH�� ###########################
print qq(
  <TR><TH bgcolor=PINK>�䴩�q�ѻ��</TH>
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
  <TR><TH bgcolor=PINK>�䴩�q�ѤH��</TH>
      <TH colspan=3 align=left>
        <TABLE>
          <tr><td>�Q</td><td>��</td></tr>
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
########################   ���׬��   ##############################
print qq(
  <TR>
    <TH bgcolor=PINK>���׬��</TH>
    <TD colspan=3 align=left>
      <SELECT name=Precourse size=3 multiple>
        <OPTION value=99999 selected>�L�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@
      </SELECT>
      <BR>
      <!CENTER>
      <INPUT type=button name=select_precourse value=��ܥ��׬�� onclick="Add_Precourse_Win()"> 
      <INPUT type=button name=select_precourse2 value=���m onclick="Clear_Precourse()"><BR>
      <SELECT name=prerequisite_logic>
        <OPTION value="AND" SELECTED>$PREREQUISITE_LOGIC{AND}
        <OPTION value="OR">$PREREQUISITE_LOGIC{OR}
      </SELECT>
    </TD>
  </TR>                              
);

##################################################################
print "<tr><th bgcolor=yellow>�W�Ҥ覡</th>";

$checked_dis = "CHECKED"  if( $Course{distant_learning} == 1 );
$checked_eng = "CHECKED"  if( $Course{english_teaching} == 1 );

print qq(
  <TD colspan=3>
    <INPUT type=checkbox name=distant_learning $checked_dis> ���Z�оǽҵ{<BR>
    <INPUT type=checkbox name=english_teaching $check_eng> ���^�y�½�<BR>
  </TD>   
);
###################################################################

print "<tr><th bgcolor=yellow>�Ƶ���</th>";
print "<th colspan=3><textarea name=note rows=3 cols=40>";
print $Course{note};
print "</textarea></th></tr>
</table>
";
print "<p>
<center>
<input type=\"submit\" value=\"�e�X���\">
<input type=\"reset\" value=\"���s��g\">
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

    // �M�����׬�ةҿ諸�Ҧ����
    function Clear_Precourse()
    {
       form1.Precourse.length=1;
       form1.Precourse.options[0].value="99999";
       form1.Precourse.options[0].text="�L";
    }
                                    
  </SCRIPT>
);
}
######################################################################################