#!/usr/local/bin/perl

require "../../../LIB/Reference.pm";
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

($request, $course_id, $course_group) = split(/:::/, $input{choice});
Check_Dept_Password($input{dept_id}, $input{password});

Print_Header();
if( $request eq "" ) {
  print("請選擇刪除或修改某科目!");
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
print "
<script language=javascript src=\"$PROJECT_URL/Classify.js\">
</script>
 ";

print << "End_JS"
<script language=javascript>

function AddWin()
{
 win=open("$PROJECT_URL/AddTeacherWindow.html","openwin","width=200,height=120,resizable");
 win.creator=self;
}

</script>

End_JS
}
############################################################################
sub Delete_Course_Data()
{
  print qq(
    <table border=1>
      <tr><th>科目編號</th><th>科目班別</th><th>科目中文名稱</th></tr>
      <tr><td>$course_id</td><td>$course_group</td><td>$course{cname}</td></tr>
    </table>

  );
  print("<br><font color=red> 您確定要刪除此科目?</font>");
  print qq(
    <FORM action="Modify_Course3.cgi" method=POST>
      <INPUT type=hidden name=dept_id value=$input{dept_id}>
      <INPUT type=hidden name=password value=$input{password}>
      <INPUT type=hidden name=course_id value=$course_id>
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
  if($SUPERUSER ne "1")
  {
   Print_Course_Title();
  }
  else
  {
   Print_Course_Title_For_SU();
  }
  Print_Time_Table();                              ###  印出功課表

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
      <th>$course{cname}</th>
      <input type=hidden name=cname value=$course{cname}>
    </tr>
    <tr>
    <th bgcolor=yellow>科目名稱(英文)</th>
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
    <th bgcolor=yellow>科目名稱(中文)</th>
      <th><input type=text length=70 name=cname value=\"$course{cname}\"></th>
    </tr>
    <tr>
    <th bgcolor=yellow>科目名稱(英文)</th>
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
             <th bgcolor=orange>一</th>
             <th bgcolor=orange>二</th>
             <th bgcolor=orange>三</th>
             <th bgcolor=orange>四</th>
             <th bgcolor=orange>五</th>
             <th bgcolor=orange>六</th>
             <th bgcolor=orange>日</th>
           </tr>
  );
  for($j=0;$j<=12;$j++) {
    print "<tr><th bgcolor=orange>";
    if ($j==0)			{ print "A";}
    if ($j>=1 && $j<=4)		{ print "$j";}
    if ($j==5)			{ print "B";}
    if ($j>=6 && $j<=9)		{ $jj=$j-1; print "$jj"; }
    if ($j==10)			{ print "C";}
    if ($j==11)			{ print "D";}
    if ($j==12)			{ print "E";}
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
  print("<th bgcolor=yellow>開課年級</th><th><select name=grade>");
  
  @g_string = ("", "一", "二", "三", "四");
  for($i=1;$i<5;$i++) {
    if($i == $input{grade}){
      print "<option value=$i selected>$g_string[$i]年級\n";
    }else{
      print "<option value=$i>$g_string[$i]年級\n";
    }
  }
  print("</select></th></tr><tr><th bgcolor=yellow>科目編號:</th>");
  print qq(
    <td>$course_id</td></tr>
    <input type=hidden name=course_id value=$course_id>
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
  if( $course{teacher}[0] eq "" ) {
    print("<option value=99999 selected>教師未定");
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
    <tr><th bgcolor=yellow>選擇授課老師</th><th>);
  print qq(

    <input type=button name=btn1 value=新增任課教師 onclick=\"AddWin()\">
    <input type=button name=btn2 value=重置 onClick=\"ClearAll(document.form1.Teacher)\">

    </th></tr></tr><tr>
    <th bgcolor=yellow>時數:</th>
    <th><select name=total_time>);
  for($i=1;$i<=10;$i++) {
    if($i ne $course{total_time} ) {
      print "<option value=$i>$i";
    }else{
      print "<option value=$i selected>$i";
    }
  }
  print qq(
    </select></th></tr><tr><th bgcolor=yellow>學分:</th>
    <th>$course{credit}</th>
    <input type=hidden name=credit value=$course{credit}>
  );
  print qq(
    </select></th></tr><tr><th bgcolor=yellow>必修/選修/通識</th>
    <th><select name=property>
  );
  for($i=1;$i<=3;$i++) {
    if($i==1) { $name="必修"; }
    if($i==2) { $name="選修"; }
    if($i==3) { $name="通識"; }
    if($i eq $course{property} ) { 
      print "<option value=$i selected>$name";
    }else{
      print "<option value=$i>$name"; 
    }
  }
  print qq(
    </select></th></tr><tr><th bgcolor=yellow>上課教室:</th>
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
    </select></th></tr><tr><th bgcolor=yellow>篩選原則</th>
    <th><select name=principle>\n);
  my($p,@p_string);
  @p_string = ("不需篩選", "一次篩選", "二次篩選");
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
print "<tr><th bgcolor=yellow>限修人數</th><th><table border=0>\n";
print "<tr><td>百</td><td>十</td><td>個</td></tr>\n";
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
### 保留學生名額 ###
print "<th bgcolor=yellow>保留名額</th><th><table border=0>\n";
print "<tr><td>百</td><td>十</td><td>個</td></tr>\n";
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
print "<tr><th bgcolor=yellow rowspan=2>支援系所</th><th rowspan=2>\n";
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
 foreach $ele(@{$course{support_grade}})
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
### 擋修系所 ###
print "<tr><th bgcolor=pink rowspan=2>擋修系所</th><th rowspan=2>\n";
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
print "</select></th><th bgcolor=pink>擋修年級</th><th>\n";
print "<select name=ban_grade size=2 multiple>";
my(@g_string);
$g_string[1]="一";
$g_string[2]="二";
$g_string[3]="三";
$g_string[4]="四";
for($i=1;$i<=4;$i++)
{
 $flag=0;
 foreach $ele(@{$course{ban_grade}})
 {
  if($ele eq $i)
  { $flag=1; break; }
 }
 if($flag == 1)
 { print "<option value=$i selected>$g_string[$i]年級\n"; }
 else
 { print "<option value=$i>$g_string[$i]年級\n"; }
}
print "</select></th></tr><tr><th bgcolor=pink>擋修班級</th>\n";
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
print "<tr><th bgcolor=yellow>備註欄</th>";
print "<th colspan=3><textarea name=note rows=3 cols=40>";
print $course{note};
print "</textarea></th></tr>
</table>
";




}
