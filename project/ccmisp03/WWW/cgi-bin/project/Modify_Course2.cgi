#!/usr/local/bin/perl

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Open_Course.pm";
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
%classroom = Read_Classroom($Input{classroom});

Print_Header();
if( $request eq "" ) {
  print("請選擇刪除或修改某科目!");
  Links2();
  exit(1);
} 

%Course = Read_Course($input{dept_id}, $course_id, $course_group, "" );

Modify_Course_Data() if( $input{choice} =~ /MODIFY/ );
Delete_Course_Data() if( $input{choice} =~ /DELETE/ );

#foreach $k (keys %input) {
#  print  ("$k --> $input{$k}<br>");
#}
#print("teacher = $Course{teacher}[0]<br>\n");
Links3($input{dept_id} ,$input{grade}, $input{password});
exit(1);

############################################################################
sub Print_Header()
{
  my($choice);
  $choice="修改"  if($input{choice} =~ "MODIFY");
  $choice="刪除"  if($input{choice} =~ "DELETE");
  print qq(
   <html><head><title>開排課系統--$choice當學期已開科目</title></head>
  );

  Add_JS();

  print qq(
   <body background=$GRAPH_URL/ccu-sbg.jpg>
     <center>
      <br>
      <table border=0 width=40%>
       <tr>
        <td>系別:</td><td> $dept{cname} </td>
        <td>年級:</td><td> $input{grade} </td></tr><tr>
        <th colspan=4><H1>$choice當學期已開科目</H1></th>
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
      // 清除先修科目所選的所有資料
      function Clear_Precourse()
      {
        form1.Precourse.length=1;
        form1.Precourse.options[0].value="99999";
        form1.Precourse.options[0].text="無";
      }
      function AddWin()
      {
        win=open("AddTeacherWindow.html","openwin","width=200,height=350,resizable");
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
      <tr><th>科目編號</th><th>科目班別</th><th>科目中文名稱</th></tr>
      <tr><td>$course_id</td><td>$course_group</td><td>$Course{cname}</td></tr>
    </table>

  );
  print("<br><font color=red> 您確定要刪除此科目?</font>");
  print qq(
    <FORM action="Modify_Course3.cgi" method=POST>
      <INPUT type=hidden name=dept_id value=$input{dept_id}>
      <INPUT type=hidden name=password value=$input{password}>
      <INPUT type=hidden name=id value=$course_id>
      <INPUT type=hidden name=course_group value=$course_group>
      <INPUT type=hidden name=action value="delete">
      <INPUT type=submit value="確定刪除">
      <INPUT type=button onclick=history.back() value="回上一畫面">
    </FORM>
  );

}
############################################################################
sub Modify_Course_Data()
{
#  if( ($SUPERUSER eq "1") or ($Course{isNEW} eq "TRUE")) {
  if( $SUPERUSER eq "1" ) {
    Print_Course_Title_For_SU();
  }else{
    Print_Course_Title();
  }

  Print_Timetable_Select(@{$Course{time}});                      ###  印出功課表

  Print_Course_Content();
  
  Print_Note_Table();

print "<p>
<center>
<input type=\"submit\" value=\"送出資料\">
<input type=\"reset\" value=\"重新填寫\">
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
    <th bgcolor=yellow>科目名稱(中文)</th>
      <th>$Course{cname}</th>
      <input type=hidden name=cname value="$Course{cname}">
    </tr>
    <tr>
    <th bgcolor=yellow>科目名稱(英文)</th>
      <th>$Course{ename}</th>
      <input type=hidden name=ename value="$Course{ename}">
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
    <th bgcolor=yellow>科目名稱(中文)</th>
      <th><input type=text length=70 name=cname value=\"$Course{cname}\"></th>
    </tr>
    <tr>
    <th bgcolor=yellow>科目名稱(英文)</th>
      <th>
      <input type=text length=70 name=ename value=\"$Course{ename}\">
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
             <th bgcolor=orange>一</th>
             <th bgcolor=orange>二</th>
             <th bgcolor=orange>三</th>
             <th bgcolor=orange>四</th>
             <th bgcolor=orange>五</th>
             <th bgcolor=orange>六</th>
             <th bgcolor=orange>日</th>
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
      foreach $ele (@{$Course{time}}) {
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
  print("<th bgcolor=yellow>開課年級</th><th><select name=grade>");
  
  @g_string = ("", "一", "二", "三", "四");

  if( ($input{dept_id} =~ /6$/) and ($input{dept_id} ne "7006") ) {
    print "<option value=1 selected>$g_string[1]年級\n";
  }else{
    for($i=1;$i<5;$i++) {
     if($i == $input{grade}) {
       print "<option value=$i selected>$g_string[$i]年級\n";
     }else{
#       print "<option value=$i>$g_string[$i]年級\n";   ### 修改年級有BUG
     }
    }
  }

  print("</select></th></tr><tr><th bgcolor=yellow>科目編號:</th>");
  print qq(
    <td>$course_id</td></tr>
    <input type=hidden name=id value=$course_id>
    <tr><th bgcolor=yellow>班別</th><th>
    $course_group</th></tr>
    <input type=hidden name=group value=$course_group>
  );
  print("<tr><th bgcolor=yellow>授課老師</th>");
  ##### read teacher_code and name of this department####
  print qq(
    <th>

    <select name=Teacher size=3 multiple onblur=\"isDelete(document.form1.Teacher)\">
  );
  if( $Course{teacher}[0] eq "" ) {
    print("<option value=99999 selected>教師未定");
  }else{
    $i=0;
    while( $Course{teacher}[$i] ne "" ) {
       print qq( <option value=$Course{teacher}[$i] selected>$Teacher_Name{$Course{teacher}[$i]} );
       $i++;
    }
  }
  print qq(
    </select>

    </th></tr>
    <tr><th bgcolor=yellow>選擇授課老師</th><th>);
  print qq(

    <input type=button name=btn1 value=新增任課教師 onclick=\"AddWin()\">
    <input type=button name=btn2 value=重置 onClick=\"ClearAll(document.form1.Teacher)\">

    </th></tr></tr><tr>
    <th bgcolor=yellow>時數:</th>
    <th><select name=total_time>);
  for($i=1;$i<=12;$i++) {
    if($i ne $Course{total_time} ) {
      print "<option value=$i>$i";
    }else{
      print "<option value=$i selected>$i";
    }
  }
  print("</SELECT>");
#############################################################################
  print qq(
    <tr><th bgcolor=yellow>正課/實驗實習/書報討論時數:</th>
    <th><select name=lab_time1>
  );
  for($i=0;$i<=12;$i++) {
    if($i ne $Course{lab_time1} ) {
      print "<option value=$i>$i";
    }else{
      print "<option value=$i selected>$i";
    }
  }
  print("</SELECT><SELECT name=lab_time2>");   ###
  for($i=0;$i<=12;$i++) {
    if($i ne $Course{lab_time2} ) {
      print "<option value=$i>$i";
    }else{
      print "<option value=$i selected>$i";
    }
  }
  print("</SELECT><SELECT name=lab_time3>");   ###
  for($i=0;$i<=12;$i++) {
    if($i ne $Course{lab_time3} ) {
      print "<option value=$i>$i";
    }else{
      print "<option value=$i selected>$i";
    }
  }
#############################################################################
  print qq(
    </select></th></tr><tr><th bgcolor=yellow>學分:</th>
    <th>$Course{credit}</th>
    <input type=hidden name=credit value=$Course{credit}>
  );
  print qq(
    </select></th></tr><tr><th bgcolor=yellow>必修/選修/通識</th>
    <th><select name=property>
  );
  for($i=1;$i<=3;$i++) {
    if($i==1) { $name="必修"; }
    if($i==2) { $name="選修"; }
    if($i==3) { $name="通識"; }
    if($i eq $Course{property} ) { 
      print "<option value=$i selected>$name";
    }else{
      print "<option value=$i>$name"; 
    }
  }
######################################################################
#  print qq(
#    </select></th></tr><tr><th bgcolor=yellow>一般/軍訓/體育</th>
#    <th><select name=suffix_cd>
#  );
#  for($i=0;$i<=2;$i++) {
#    if($i==0) { $suffix_cd="一般"; }
#    if($i==1) { $suffix_cd="軍訓"; }
#    if($i==2) { $suffix_cd="體育"; }
#    if($i eq $Course{suffix_cd} ) {
#      print "<option value=$i selected>$suffix_cd";
#    }else{
#      print "<option value=$i>$suffix_cd";
#    }
#  }
######################################################################
  print qq(
    </select></th></tr><tr><th bgcolor=yellow>上課教室:</th>
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
    </select></th></tr><tr><th bgcolor=yellow>篩選原則</th>
    <th><select name=principle>\n);
  my($p,@p_string);
  @p_string = ("不需篩選", "一次篩選", "二次篩選");
  for($p=0;$p<3;$p++) {
    ### 只有研究所會有 "不需篩選"(通識 7006 也不可有 "不需篩選)
    if( $SUPERUSER != 1 ) { 
      if( ($input{dept_id} !~ /6$/) or ($input{dept_id} eq "7006") ) {
        next if( $p == 0 );                 ###  2002/11/20 Nidalap :D~     
      }
    }
    if( $TERM == 2 ) {                      ###  第二學期選課, 只有 "一次篩選"
      next if($p == 2);                     ###  2002/12/02, Nidalap :D~
#    }elsif( $TERM == 1 ) {                  ###  第一學期選課, 只有 "二次篩選"
#      next if($p == 1);                     ###  2005/04/12, Nidalap :D~
    }
    if($p ne $Course{principle}){ 
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
print "<tr><th bgcolor=yellow>限修人數</th><th>";

if( $SUPERUSER == 1 ) {                    #####  管理者, 可以修改限修人數   
  print "<table border=0>\n<tr><td>百</td><td>十</td><td>個</td></tr>\n";
  print "<tr><td><select name=number_limit_2>";
  my($i,$j);
  $j = int($Course{number_limit}/100);
  #$j= ($Course{number_limit}-$Course{number_limit}%100)/100;
  for($i=0;$i<10;$i++) {
    if($i ne $j) { 
      print "<option value=$i>$i\n"; 
    }else{
      print "<option value=$i selected>$i\n"; 
    }
  }
  print "</select></td><td><select name=number_limit_1>";
  $j= int(( $Course{number_limit} % 100 ) /10);
  for($i=0;$i<10;$i++) {
    if($i ne $j) {
      print "<option value=$i>$i\n"; 
    }else{ 
      print "<option value=$i selected>$i\n"; 
    }
  }
  print "</select></td><td><select name=number_limit_0>";

  $j= $Course{number_limit} % 10;
  for($i=0;$i<10;$i++) {
    if($i ne $j) { 
      print "<option value=$i>$i\n"; 
    }else{ 
      print "<option value=$i selected>$i\n"; 
    }
  }
  print "</select></td></tr></table>";
}elsif( $Course{number_limit} == 0 ) {         #####  不限修
  print("無");
}else{                                         #####  有限修
  print("$Course{number_limit}(由教室容量決定)<BR>");
}

print "</th>";
### 保留學生名額 ###
print "<th bgcolor=yellow>保留新生名額</th><th><table border=0>\n";
print "<tr><td>百</td><td>十</td><td>個</td></tr>\n";
print "<tr><td><select name=reserved_number_2>";
my($i,$j);
$j= ($Course{reserved_number}-$Course{reserved_number}%100)/100;
for($i=0;$i<10;$i++)
{
 if($i ne $j)
 { print "<option value=$i>$i\n"; }
 else
 { print "<option value=$i selected>$i\n"; }
}
print "</select></td><td><select name=reserved_number_1>";
$j= int (( $Course{reserved_number} % 100 ) /10);
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
  if($cge eq $Course{support_cge_type}) {
    print("<OPTION value=$cge SELECTED>$cge{$cge}{sub_cge_id_show} $cge{$cge}{cge_name}");
  }else{
    print("<OPTION value=$cge>$cge{$cge}{sub_cge_id_show} $cge{$cge}{cge_name}");
  }
}
###########################   支援通識人數
$support_cge_number_0 = $Course{support_cge_number} % 10;  ## 個位數
$support_cge_number_1 = ($Course{support_cge_number} - $support_cge_number_0) / 10;  ## 十位數

print qq(
  </SELECT></TH></TR>
  <TR><TH bgcolor=PINK>支援通識人數</TH>
      <TH colspan=3 align=left>
        <TABLE>
          <tr><td>十</td><td>個</td></tr>
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
    <TH bgcolor=PINK>先修科目</TH>
    <TD colspan=3 align=left>
      <SELECT name=Precourse size=3 multiple>
);

foreach $precourse (@{$Course{prerequisite_course}}) {
  if( ($$precourse{dept} eq "99999") or ($$precourse{dept} eq "")) {
    print qq(<OPTION value="99999">無);
    next;
  }
  %predept = Read_Dept($$precourse{dept});
  %precourse = Read_Course($$precourse{dept}, $$precourse{id}, "01", "history");
  $course_string_to_select = $predept{cname2} . ":[" . $$precourse{id} . "]" . $precourse{cname} . "-" . $GRADE{$$precourse{grade}};

  $course_string_hidden = join(":", $$precourse{dept}, $$precourse{id}, $$precourse{grade});
  print qq(<OPTION value=$course_string_hidden SELECTED>$course_string_to_select\n);
}

$default_pre_and = "SELECTED";
$default_pre_or  = "";
if( $Course{prerequisite_logic} eq "OR" ) {
  $default_pre_and = "";
  $default_pre_or  = "SELECTED";
}
print qq(
      </SELECT>
      <BR>
      <!CENTER>
      <INPUT type=button name=select_precourse value=選擇先修科目 onclick="Add_Precourse_Win()">
      <INPUT type=button name=select_precourse2 value=重置 onclick="Clear_Precourse()"><BR>
      <SELECT name=prerequisite_logic>
        <OPTION value="AND" $default_pre_and>$PREREQUISITE_LOGIC{AND}
        <OPTION value="OR"  $default_pre_or>$PREREQUISITE_LOGIC{OR}
      </SELECT>
    </TD>
  </TR>
);


##################################################################
print "<tr><th bgcolor=yellow>上課方式</th>";

$checked_dis = "CHECKED"  if( $Course{distant_learning} == 1 );
$checked_eng = "CHECKED"  if( $Course{english_teaching} == 1 );

print qq(
  <TD colspan=3>
    <INPUT type=checkbox name=distant_learning $checked_dis> 遠距教學課程<BR>
    <INPUT type=checkbox name=english_teaching $checked_eng> 全英語授課<BR>
  </TD>   
);

###################################################################
            
print "<tr><th bgcolor=yellow>備註欄</th>";
print "<th colspan=3><textarea name=note rows=3 cols=40>";
print $Course{note};
print "</textarea></th></tr>
</table>
";




}
