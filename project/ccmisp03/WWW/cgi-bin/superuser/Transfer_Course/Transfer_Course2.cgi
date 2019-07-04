#!/usr/local/bin/perl

###########################################################################
#####   Transfer_Course2.cgi
#####   轉必修/必選課
#####   顯示某系級開的課, 讓使用者選擇轉哪一門課到哪一系級班的學生
#####   Coder: Nidalap
#####   Date : Jun,03,1999
###########################################################################
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Course.pm";
print("Content-type:text/html\n\n");

%Input = User_Input();
@dept = Find_All_Dept();
@course = Find_All_Course($Input{dept}, $Input{grade}, "");
print << "TABLE_1"
 <HEAD><TITLE>必修/必選課轉檔</TITLE></HEAD>
   <BODY background="$GRAPH_URL./ccu-sbg.jpg"><CENTER>
     <H1>必修/必選課轉檔<br>請選擇轉檔科目及學生系所,年級及班別<hr></H1>
     <FORM action="Transfer_Course3.cgi" method="POST">
       <INPUT type="hidden" name="dept" value=$Input{dept}>
       <INPUT type="hidden" name="grade" value=$Input{grade}>
       <TABLE border=1>
         <TR><TD align=center bgcolor=yellow>請選擇轉檔科目</TD>
         <TD bgcolor=yellow>請選擇轉檔學生系級班</TD></TR>
         <TR><TD><SELECT name="course" size=15>
TABLE_1
;
foreach $course (@course) {
  %course = Read_Course($Input{dept}, $$course{id}, $$course{group}, "");
  print qq(<OPTION value="$$course{id}_$$course{group}">$course{id}_$course{group} $course{cname});
}
print qq(</SELECT></TD><TD valign=top><SELECT name="stu_dept" size=10>);
foreach $dept (@dept) {
  %dept = Read_Dept($dept);
  print qq(<OPTION value="$dept">$dept{cname});
}
print qq(</SELECT><br>
  年級: <SELECT name="stu_grade">
    <OPTION value="1">一年級 <OPTION value="2">二年級
    <OPTION value="3">三年級 <OPTION value="4">四年級
  </SELECT><br>
  班級: <SELECT name="stu_class">
);
@temp = (A..E);
foreach $i (@temp) {
  print qq(<OPTION value="$i">$i);
}
print("</SELECT><br>");
print qq(
  修課屬性: <SELECT name="property">
    <OPTION value="1" selected>必修
    <OPTION value="2">選修
    <OPTION value="3">通識
  </SELECT>
);
print("</TABLE>");

print << "END_OF_HTML"
    <INPUT type=submit value="確定轉檔">
  </FORM>
  本程式不檢查重複選課, 若已經轉檔過後, 要修改屬性, 請先執行批次退選再轉檔<br>
END_OF_HTML

