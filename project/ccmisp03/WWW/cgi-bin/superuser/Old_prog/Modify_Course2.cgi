#!/usr/local/bin/perl

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Teacher.pm";

print("Content-type:text/html\n\n");
%input = User_Input();
%dept  = Read_Dept($input{dept_id});
@teacher = Read_Teacher_File();
%cge = Read_Cge();
@all_course = Find_All_Course($input{dept_id}, "", "history");

($request, $course_id, $course_group) = split(/:::/, $input{choice});
Check_Dept_Password($input{dept_id}, $input{password});

Print_Header();
if( $request eq "" ) {
  print("�п�ܧR���έק�Y���!");
  Links2();
  exit(1);
} 

%course= Read_Course($input{dept_id}, $course_id, $course_group, "" );
Modify_Course_Data() if( $input{choice} =~ /MODIFY/ );
Delete_Course_Data() if( $input{choice} =~ /DELETE/ );

#foreach $k (keys %input) {
#  print  ("$k --> $input{$k}<br>");
#}
#print("teacher = $course{teacher}[0]<br>\n");
Links3($input{dept_id} ,$input{grade}, $input{password});
exit(1);

############################################################################
sub Print_Header()
{
  my($choice);
  $choice="�ק�"  if($input{choice} =~ "MODIFY");
  $choice="�R��"  if($input{choice} =~ "DELETE");
  print qq(
   <html><head><title>�}�ƽҨt��--$choice���Ǵ��w�}���</title></head>
  );

  Add_JS();

  print qq(
   <body background=http://kiki.ccu.edu.tw/~ccmisp06/Graph/ccu-sbg.jpg>
     <center>
      <br>
      <table border=0 width=40%>
       <tr>
        <td>�t�O:</td><td> $dept{cname} </td>
        <td>�~��:</td><td> $input{grade} </td></tr><tr>
        <th colspan=4><H1>$choice���Ǵ��w�}���</H1></th>
       </tr>
      </table>
      <hr width=80%>
  );
}
############################################################################
sub Add_JS()
{
  print qq(
    <SCRIPT language=javascript src=\"./Classify.js\"></SCRIPT>
    <SCRIPT language=JAVASCRIPT>
      function Add_Precourse_Win()
      {
        win2=open("./Add_Precourse_Window.html","openwin","width=400,height=350");
        win2.creator=self;
      }
      // �M�����׬�ةҿ諸�Ҧ����
      function Clear_Precourse()
      {
        form1.Precourse.length=1;
        form1.Precourse.options[0].value="99999";
        form1.Precourse.options[0].text="�L";
      }
      function AddWin()
      {
        win=open("http://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/project/AddTeacherWindow.html","openwin","width=200,height=120,resizable");
        win.creator=self;
      }
    </SCRIPT>
  );
}
############################################################################
sub Delete_Course_Data()
{
  print qq(
    <table border=1>
      <tr><th>��ؽs��</th><th>��دZ�O</th><th>��ؤ���W��</th></tr>
      <tr><td>$course_id</td><td>$course_group</td><td>$course{cname}</td></tr>
    </table>

  );
  print("<br><font color=red> �z�T�w�n�R�������?</font>");
  print qq(
    <FORM action="Modify_Course3.cgi" method=POST>
      <INPUT type=hidden name=dept_id value=$input{dept_id}>
      <INPUT type=hidden name=password value=$input{password}>
      <INPUT type=hidden name=course_id value=$course_id>
      <INPUT type=hidden name=course_group value=$course_group>
      <INPUT type=hidden name=action value="delete">
      <INPUT type=submit value="�T�w�R��">
      <INPUT type=button onclick=history.back() value="�^�W�@�e��">
    </FORM>
  );

}
############################################################################
sub Modify_Course_Data()
{
  if( ($SUPERUSER eq "1") or ($course{isNEW} eq "TRUE")) {
    Print_Course_Title_For_SU();
  }else{
    Print_Course_Title();
  }

  Print_Time_Table();                              ###  �L�X�\�Ҫ�

  Print_Course_Content();
  
  Print_Note_Table();

print "<p>
<center>
<input type=\"submit\" value=\"�e�X���\">
<input type=\"reset\" value=\"���s��g\">
</form><hr>";


 
}
############################################################################
sub Print_Course_Title()
{
  print qq(
    <form name=form1 method=post action=Modify_Course3.cgi>
    <input type=hidden name=action value="modify">
    <input type=hidden name=dept_id value=$input{dept_id}>
    <input type=hidden name=password value=$input{password}>
    <table border=1>
    <tr>
    <th bgcolor=yellow>��ئW��(����)</th>
      <th>$course{cname}</th>
      <input type=hidden name=cname value=$course{cname}>
    </tr>
    <tr>
    <th bgcolor=yellow>��ئW��(�^��)</th>
      <th>$course{ename}</th>
      <input type=hidden name=ename value="$course{ename}">
    </tr>
    </table><br>
    <table border=1>
    <tr>
    <th colspan=2 rowspan=13>
  );
}

sub Print_Course_Title_For_SU()
{
  print "
    <form name=form1 method=post action=Modify_Course3.cgi>
    <input type=hidden name=action value=modify>
    <input type=hidden name=dept_id value=$input{dept_id}>
    <input type=hidden name=password value=$input{password}>
    <table border=1>
    <tr>
    <th bgcolor=yellow>��ئW��(����)</th>
      <th><input type=text length=70 name=cname value=\"$course{cname}\"></th>
    </tr>
    <tr>
    <th bgcolor=yellow>��ئW��(�^��)</th>
      <th>
      <input type=text length=70 name=ename value=\"$course{ename}\">
      </th>
    </tr>
    </table><br>
    <table border=1>
    <tr>
    <th colspan=2 rowspan=13>";
}
############################################################################
sub Print_Time_Table()
{
  print qq(
        <table border=1>
           <tr>
             <th></th>
             <th bgcolor=orange>�@</th>
             <th bgcolor=orange>�G</th>
             <th bgcolor=orange>�T</th>
             <th bgcolor=orange>�|</th>
             <th bgcolor=orange>��</th>
             <th bgcolor=orange>��</th>
             <th bgcolor=orange>��</th>
           </tr>
  );
  for($j=0;$j<=13;$j++) {
    print "<tr><th bgcolor=orange>";
    if ($j==0)			{ print "A";}
    if ($j>=1 && $j<=4)		{ print "$j";}
    if ($j==5)			{ print "F";}
    if ($j==6)			{ print "B";}
    if ($j>=7 && $j<=10)	{ $jj=$j-2; print "$jj"; }
    if ($j==11)			{ print "C";}
    if ($j==12)			{ print "D";}
    if ($j==13)			{ print "E";}
    print "</th>";
    for($i=1;$i<=7;$i++) {
      $k="$i"."_$j";
      $CHECK=0;
      foreach $ele (@{$course{time}}) {
        if($k eq "$$ele{week}_$$ele{time}" ) {
          $CHECK=1;
          goto OUT;
        }
      }
      OUT:
      if($CHECK == 0) {
        print "<td><input type=checkbox name=$k value=999></td>";
      }else{
        print "<td><input type=checkbox name=$k value=999 checked></td>";
      }
    }
    print "</tr>";
  }
  print "</table>";
}
###########################################################################
sub Print_Course_Content()
{
  print("<th bgcolor=yellow>�}�Ҧ~��</th><th><select name=grade>");
  
  @g_string = ("", "�@", "�G", "�T", "�|");

  if( ($input{dept_id} =~ /6$/) and ($input{dept_id} ne "7006") ) {
    print "<option value=1 selected>$g_string[1]�~��\n";
  }else{
    for($i=1;$i<5;$i++) {
     if($i == $input{grade}) {
       print "<option value=$i selected>$g_string[$i]�~��\n";
     }else{
       print "<option value=$i>$g_string[$i]�~��\n";
     }
    }
  }

  print("</select></th></tr><tr><th bgcolor=yellow>��ؽs��:</th>");
  print qq(
    <td>$course_id</td></tr>
    <input type=hidden name=course_id value=$course_id>
    <tr><th bgcolor=yellow>�Z�O</th><th>
    $course_group</th></tr>
    <input type=hidden name=group value=$course_group>
  );
  print("<tr><th bgcolor=yellow>�½ҦѮv</th>");
  ##### read teacher_code and name of this department####
  print qq(
    <th>

    <select name=Teacher size=3 multiple onblur=\"isDelete(document.form1.Teacher)\">
  );
  if( $course{teacher}[0] eq "" ) {
    print("<option value=99999 selected>�Юv���w");
  }else{
    $i=0;
    while( $course{teacher}[$i] ne "" ) {
       print qq( <option value=$course{teacher}[$i] selected>$Teacher_Name{$course{teacher}[$i]} );
       $i++;
    }
  }
  print qq(
    </select>

    </th></tr>
    <tr><th bgcolor=yellow>��ܱ½ҦѮv</th><th>);
  print qq(

    <input type=button name=btn1 value=�s�W���ұЮv onclick=\"AddWin()\">
    <input type=button name=btn2 value=���m onClick=\"ClearAll(document.form1.Teacher)\">

    </th></tr></tr><tr>
    <th bgcolor=yellow>�ɼ�:</th>
    <th><select name=total_time>);
  for($i=1;$i<=12;$i++) {
    if($i ne $course{total_time} ) {
      print "<option value=$i>$i";
    }else{
      print "<option value=$i selected>$i";
    }
  }
  print("</SELECT>");
#############################################################################
  print qq(
    <tr><th bgcolor=yellow>����/������/�ѳ��Q�׮ɼ�:</th>
    <th><select name=lab_time1>
  );
  for($i=0;$i<=12;$i++) {
    if($i ne $course{lab_time1} ) {
      print "<option value=$i>$i";
    }else{
      print "<option value=$i selected>$i";
    }
  }
  print("</SELECT><SELECT name=lab_time2>");   ###
  for($i=0;$i<=12;$i++) {
    if($i ne $course{lab_time2} ) {
      print "<option value=$i>$i";
    }else{
      print "<option value=$i selected>$i";
    }
  }
  print("</SELECT><SELECT name=lab_time3>");   ###
  for($i=0;$i<=12;$i++) {
    if($i ne $course{lab_time3} ) {
      print "<option value=$i>$i";
    }else{
      print "<option value=$i selected>$i";
    }
  }
#############################################################################
  print qq(
    </select></th></tr><tr><th bgcolor=yellow>�Ǥ�:</th>
    <th>$course{credit}</th>
    <input type=hidden name=credit value=$course{credit}>
  );
  print qq(
    </select></th></tr><tr><th bgcolor=yellow>����/���/�q��</th>
    <th><select name=property>
  );
  for($i=1;$i<=3;$i++) {
    if($i==1) { $name="����"; }
    if($i==2) { $name="���"; }
    if($i==3) { $name="�q��"; }
    if($i eq $course{property} ) { 
      print "<option value=$i selected>$name";
    }else{
      print "<option value=$i>$name"; 
    }
  }
######################################################################
#  print qq(
#    </select></th></tr><tr><th bgcolor=yellow>�@��/�x�V/��|</th>
#    <th><select name=suffix_cd>
#  );
#  for($i=0;$i<=2;$i++) {
#    if($i==0) { $suffix_cd="�@��"; }
#    if($i==1) { $suffix_cd="�x�V"; }
#    if($i==2) { $suffix_cd="��|"; }
#    if($i eq $course{suffix_cd} ) {
#      print "<option value=$i selected>$suffix_cd";
#    }else{
#      print "<option value=$i>$suffix_cd";
#    }
#  }
######################################################################
  print qq(
    </select></th></tr><tr><th bgcolor=yellow>�W�ұЫ�:</th>
    <th><select name=classroom>
  );
  @Classroom=Find_All_Classroom();
  foreach $Classroom(@Classroom) {
    %classroom=Read_Classroom($Classroom);
    if( $classroom{id} eq $course{classroom} ) { 
      print "<option value=$Classroom selected>$classroom{cname}\n";
    }else{
      print "<option value=$Classroom>$classroom{cname}\n"; 
    }
  }
  print qq(
    </select></th></tr><tr><th bgcolor=yellow>�z���h</th>
    <th><select name=principle>\n);
  my($p,@p_string);
  @p_string = ("���ݿz��", "�@���z��", "�G���z��");
  for($p=0;$p<3;$p++) {
    if($p ne $course{principle}){ 
      print "<option value=$p>$p_string[$p]\n"; 
    }else{ 
      print "<option value=$p selected>$p_string[$p]\n"; 
    }
  }
  print "</select></th></tr></table>\n";
}
###########################################################################
sub Print_Note_Table()
{
print "<table border=1>";
print "</select></th></tr>\n";
print "<tr><th bgcolor=yellow>���פH��</th><th><table border=0>\n";
print "<tr><td>��</td><td>�Q</td><td>��</td></tr>\n";
print "<tr><td><select name=number_limit_2>";
my($i,$j);
$j = int($course{number_limit}/100);
#$j= ($course{number_limit}-$course{number_limit}%100)/100;
for($i=0;$i<10;$i++)
{
 if($i ne $j)
 { print "<option value=$i>$i\n"; }
 else
 { print "<option value=$i selected>$i\n"; }
}
print "</select></td><td><select name=number_limit_1>";
$j= int(( $course{number_limit} % 100 ) /10);
for($i=0;$i<10;$i++)
{
 if($i ne $j)
 { print "<option value=$i>$i\n"; }
 else
 { print "<option value=$i selected>$i\n"; }
}
print "</select></td><td><select name=number_limit_0>";

$j= $course{number_limit} % 10;
for($i=0;$i<10;$i++)
{
 if($i ne $j)
 { print "<option value=$i>$i\n"; }
 else
 { print "<option value=$i selected>$i\n"; }
}
print "</select></td></tr></table></th>";
### �O�d�ǥͦW�B ###
print "<th bgcolor=yellow>�O�d�s�ͦW�B</th><th><table border=0>\n";
print "<tr><td>��</td><td>�Q</td><td>��</td></tr>\n";
print "<tr><td><select name=reserved_number_2>";
my($i,$j);
$j= ($course{reserved_number}-$course{reserved_number}%100)/100;
for($i=0;$i<10;$i++)
{
 if($i ne $j)
 { print "<option value=$i>$i\n"; }
 else
 { print "<option value=$i selected>$i\n"; }
}
print "</select></td><td><select name=reserved_number_1>";
$j= int (( $course{reserved_number} % 100 ) /10);
for($i=0;$i<10;$i++)
{
 if($i ne $j)
 { print "<option value=$i>$i\n"; }
 else
 { print "<option value=$i selected>$i\n"; }
}
print "</select></td><td><select name=reserved_number_0>";

$j= $course{reserved_number} % 10;
for($i=0;$i<10;$i++)
{
 if($i ne $j)
 { print "<option value=$i>$i\n"; }
 else
 { print "<option value=$i selected>$i\n"; }
}
print "</select></td></tr></table></th></tr>\n";
print "<tr><th bgcolor=yellow rowspan=2>�䴩�t��</th><th rowspan=2>\n";
print "<select name=support_dept size=4 multiple>\n";

my(@Dept,$dept,%Dept,$flag);

@Dept=Find_All_Dept();
foreach $dept(@Dept)
{
 %Dept=Read_Dept($dept);
 $flag=0;
 foreach $ele(@{$course{support_dept}})
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
 foreach $ele(@{$course{support_grade}})
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
 foreach $ele( @{$course{support_class}} )
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
 foreach $ele(@{$course{ban_dept}})
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
 foreach $ele(@{$course{ban_grade}})
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
 foreach $ele( @{$course{ban_class}} )
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
  if($cge eq $course{support_cge_type}) {
    print("<OPTION value=$cge SELECTED>$cge{$cge}{sub_cge_id_show} $cge{$cge}{cge_name}");
  }else{
    print("<OPTION value=$cge>$cge{$cge}{sub_cge_id_show} $cge{$cge}{cge_name}");
  }
}
###########################   �䴩�q�ѤH��
$support_cge_number_0 = $course{support_cge_number} % 10;  ## �Ӧ��
$support_cge_number_1 = ($course{support_cge_number} - $support_cge_number_0) / 10;  ## �Q���

print qq(
  </SELECT></TH></TR>
  <TR><TH bgcolor=PINK>�䴩�q�ѤH��</TH>
      <TH colspan=3 align=left>
        <TABLE>
          <tr><td>�Q</td><td>��</td></tr>
          <tr><td><select name=support_cge_number_1>
);
my($i);
for($i=0;$i<10;$i++) {
   if($i ne $support_cge_number_1)
     { print "<option value=$i>$i\n"; }
   else
     { print "<option value=$i selected>$i\n"; }
}
print("</select></td><td><select name=support_cge_number_0>");

for($i=0;$i<10;$i++) {
   if($i ne $support_cge_number_0)
     { print "<option value=$i>$i\n"; }
   else
     { print "<option value=$i selected>$i\n"; }
}
print("</SELECT></TD></TR></TABLE></TD></TR>");
##################################################################
print qq(
  <TR>
    <TH bgcolor=PINK>���׬��</TH>
    <TD colspan=3 align=left>
      <SELECT name=Precourse size=3 multiple>
);

foreach $precourse (@{$course{prerequisite_course}}) {
  if( ($$precourse{dept} eq "99999") or ($$precourse{dept} eq "")) {
    print qq(<OPTION value="99999">�L);
    next;
  }
  %predept = Read_Dept($$precourse{dept});
  %precourse = Read_Course($$precourse{dept}, $$precourse{id}, "01", "history");
  $course_string_to_select = $predept{cname2} . ":[" . $$precourse{id} . "]" . $precourse{cname} . "-" . $GRADE{$$precourse{grade}};

  $course_string_hidden = join(":", $$precourse{dept}, $$precourse{id}, $$precourse{grade});
  print qq(<OPTION value=$course_string_hidden SELECTED>$course_string_to_select\n);
}

print qq(
      </SELECT>
      <BR>
      <!CENTER>
      <INPUT type=button name=select_precourse value=��ܥ��׬�� onclick="Add_Precourse_Win()">
      <INPUT type=button name=select_precourse2 value=���m onclick="Clear_Precourse()"><BR>
      <SELECT name=prerequisite_logic>
        <OPTION value="AND">$PREREQUISITE_LOGIC{AND}
        <OPTION value="OR">$PREREQUISITE_LOGIC{OR}
      </SELECT>
    </TD>
  </TR>
);


##################################################################
print "<tr><th bgcolor=yellow>�Ƶ���</th>";
print "<th colspan=3><textarea name=note rows=3 cols=40>";
print $course{note};
print "</textarea></th></tr>
</table>
";




}