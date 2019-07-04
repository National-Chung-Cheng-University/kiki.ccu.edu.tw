#!/usr/local/bin/perl
print "Content-type: text/html","\n\n";

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Teacher.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Common_Utility.pm";

require "Query.pm";
require $LIBRARY_PATH."Select_Course.pm";

$sys_state = Whats_Sys_State();
if( $sys_state == 0 ) {
  print qq(
    <html>
      <head><title>第二版開排課系統</title></head>
      <body background=$GRAPH_URL/ccu-sbg.jpg>
        <center>
         <img src=$GRAPH_URL/open.jpg><P>
         <h4>查詢修課學生名單功\能</h4><HR>
         目前系統暫不開放查詢!
  );
  exit(1);
}

### 處理使用者輸入的資料 ###
my($temp1,$temp2);
%Input = User_Input();
($temp1,$temp2)=split(/_/,$Input{course_cd});
%Course = Read_Course($Input{dept_cd},$temp1,$temp2, $Input{yearterm});
$page = $Input{page};
if($page eq "") { $page = 0; }

#foreach $k (keys %Input) {
#  print("$k --> $Input{$k}<BR>\n");
#}

###  處理授課教師顯示字串
my $teacher_string = "";
@Teachers=Read_Teacher_File();
$T=@{$Course{teacher}};
for($teacher=0; $teacher < $T; $teacher++){
  if($Course{teacher}[$teacher] != 99999){
    $teacher_string .= $Teacher_Name{$Course{teacher}[$teacher]};
  }else{
    $teacher_string = "教師未定";
  }
  if($teacher != $T-1){
    $teacher_string .= ", ";
  }
}
###  處理上課時間顯示字串
$time_string = Format_Time_String($Course{time});

### 讀取教室資料
%Room=Read_Classroom($Course{classroom});
### 讀入學生名單 ###
if( $Input{last_select} == 1 ) {
  $list_title = "上次篩選後名單";
  @Students = Student_in_Course($Input{dept_cd},$Course{id},$Course{group}, "last");  
}else{
  $list_title = "目前選課名單";
  @Students = Student_in_Course($Input{dept_cd},$Course{id},$Course{group}, $Input{yearterm});
}
$total = @Students;
$total_page = int($total/90);

my($temp);
$temp =$page +1;
Print_Html_Header("$Course{cname} 修課學生名單第 $temp 頁","$GRAPH_URL/ccu-sbg.jpg");
@Students=sort(@Students);

$temp= $total_page+1;

## 顯示科目基本資料 ##

print "</center>";
print "科目名稱: $Course{cname}<br>";
print "科目代碼: $Course{id} , 科目班別: $Course{group}<br>";
print "授課教師: $teacher_string<BR>";
print "上課時間: $time_string<BR>";
print "上課教室: $Room{cname}<BR>";
print "修課人數: $total , 共分 $temp 頁<br>";
print("本名單是 <FONT color=RED>$list_title</FONT>");

if( ($page+1)*90 > $total )
{ $Limit= $total; }
else { $Limit=($page+1)*90 ; }

print "<table border=0 width=100%>";
print "<tr>";
my(%student);

#print("page = $page; total = $total, Limit = $Limit<BR>\n");
for($i=($page*90); $i<$Limit ; $i++ )
{
# print("$i<BR>\n");
 if($i %30 ==0 )
 { print "<td valign=top><table border=1>\n"; }
 
 %student = Read_Student($Students[$i]);  
 %dept = Read_Dept($student{dept});
 print "<tr><th align=left>$dept{cname2}</th>";
 print "<td>$student{id}</td><th align=left>$student{name}</th></tr>\n";
 
 if( ($i+1) % 30 ==0 || $i ==($Limit-1) )
 { print "</table></td>"; }
}
print "</tr></table>\n";

if( $page ne "" && $page ne "0" )
{
 $Temp=$Input{'page'}-1;
 print qq(
   <form method="post" action="Query_2.cgi">
     <input type="hidden" name="dept_cd" value="$Input{'dept_cd'}">
     <input type="hidden" name="course_cd" value="$Input{'course_cd'}">
     <input type="hidden" name="page" value="$Temp">
     <input type="hidden" name="last_select" value="$Input{last_select}">
     <input type="hidden" name="yearterm" value="$Input{yearterm}">
     <input type="submit" value="翻前一頁">
   </form>
 );
}
print "<br>";
if( $total_page > $page )
{
 $Temp=$Input{'page'}+1;
 print qq(
   <form method="post" action="Query_2.cgi">       
     <input type="hidden" name="dept_cd" value="$Input{'dept_cd'}">             
     <input type="hidden" name="course_cd" value="$Input{'course_cd'}">             
     <input type="hidden" name="page" value="$Temp">             
     <input type="hidden" name="last_select" value="$Input{last_select}">
     <input type="hidden" name="yearterm" value="$Input{yearterm}">
     <input type="submit" value="翻下一頁">
   </form>       
 );
}

print "<p><a href=\"Login.cgi\">回到查詢修課學生主選單</a><br>\n";
print "<a href=\"http://www.ccu.edu.tw\">回中正大學首頁</a>\n";