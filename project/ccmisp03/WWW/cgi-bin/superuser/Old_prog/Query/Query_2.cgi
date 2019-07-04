#!/usr/local/bin/perl
print "Content-type: text/html","\n\n";

require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Student.pm";
require "Query.pm";

#require $LIBRARY_PATH."Dept.pm";

### 處理使用者輸入的資料 ###
my($temp1,$temp2);
%Input = User_Input();
($temp1,$temp2)=split(/_/,$Input{course_cd});
%Course = Read_Course($Input{dept_cd},$temp1,$temp2);
$page = $Input{page};
if($page eq "") { $page = 0; }

### 讀入學生名單 ###
@Students = Student_in_Course($Input{dept_cd},$Course{id},$Course{group});
$total = @Students;
$total_page = int($total/90);

my($temp);
$temp =$page +1;
Print_Html_Header("$Course{cname} 修課學生名單第 $temp 頁","$HTTP/ccu-sbg.jpg");
@Students=sort(@Students);

$temp= $total_page+1;

## 顯示科目基本資料 ##

print "</center>";
print "科目名稱: $Course{cname}<br>";
print "科目代碼: $Course{id} , 科目班別: $Course{group}<br>";
print "修課人數: $total , 共分 $temp 頁<br>";

if( ($page+1)*90 > $total )
{ $Limit= $total; }
else { $Limit=($page+1)*90 ; }

print "<table border=0 width=100%>";
print "<tr>";
my(%student);

for($i=($page*90); $i<$Limit ; $i++ )
{
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
 print "<form method=\"post\" action=\"Query_2.cgi\">\n";
 print "<input type=\"hidden\" name=\"course_cd\" value=\"$Input{'course_cd'}\">\n";
 $Temp=$Input{'page'}-1;
 print "<input type=\"hidden\" name=\"page\" value=\"$Temp\">\n";
 print "<input type=\"submit\" value=\"翻前一頁\">\n";
 print "</form>";
}
print "<br>";
if( $total_page > $page )
{
 print "<form method=\"post\" action=\"Query_2.cgi\">\n";
 print "<input type=\"hidden\" name=\"course_cd\"
value=\"$Input{'course_cd'}\">\n"; 
 $Temp=$Input{'page'}+1;
 print "<input type=\"hidden\" name=\"page\" value=\"$Temp\">\n";
 print "<input type=\"submit\" value=\"翻下一頁\">\n";
 print "</form>";
}

print "<p><a href=\"Login.cgi\">回到查詢修課學生主選單</a><br>\n";
print "<a href=\"http://www.ccu.edu.tw\">回中正大學首頁</a>\n";