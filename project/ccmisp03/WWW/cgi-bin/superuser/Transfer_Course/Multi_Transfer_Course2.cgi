#!/usr/local/bin/perl

###########################################################################
#####   Transfer_Course2.cgi
#####   多對多轉必修/必選課
#####   列出五個系級班的選擇, 依照亂數轉入五個班別.
#####   Coder: Nidalap
#####   Date : 09/04/2001
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
 <HEAD><TITLE>多對多必修/必選課轉檔</TITLE></HEAD>
   <BODY background="$GRAPH_URL./ccu-sbg.jpg"><CENTER>
     <H1>多對多必修/必選課轉檔<br>請選擇轉檔科目及學生系所,年級及班別<hr></H1>
     <FORM action="Multi_Transfer_Course3.cgi" method="POST">
       <INPUT type="hidden" name="dept" value=$Input{dept}>
       <INPUT type="hidden" name="grade" value=$Input{grade}>
       <TABLE border=1>
         <TR><TD align=center bgcolor=yellow>請選擇轉檔科目(複選)</TD>
         <TD bgcolor=yellow>請選擇轉檔學生系級班(複選)</TD></TR>
         <TR><TD>
           科目代碼班別:<BR>
           <SELECT name="course" size=6 multiple>
               
TABLE_1
;
foreach $course (@course) {
  %course = Read_Course($Input{dept}, $$course{id}, $$course{group}, "");
  print qq(<OPTION value="$$course{id}_$$course{group}">$course{id}_$course{group} $course{cname});
}
print qq(
    </SELECT>
  </TD>
  <TD valign=top>
    <TABLE border=0>
      <TR>
        <TD><SELECT name="stu_dept" size=4 multiple>
);
foreach $dept (@dept) {
  %dept = Read_Dept($dept);
  print qq(<OPTION value="$dept">$dept{cname2});
}
print qq(
    </SELECT>
  </TD>
  <TD>
    <SELECT name="stu_grade" size=4 multiple>
      <OPTION value="1">一年級 <OPTION value="2">二年級
      <OPTION value="3">三年級 <OPTION value="4">四年級
    </SELECT>
  </TD>
  <TD>
    <SELECT name="stu_class" size=4 multiple>
);
@temp = (A..E);
foreach $i (@temp) {
  print qq(<OPTION value="$i">$i);
}
print qq(
        </SELECT>
      </TD>
    </TR>
  </TABLE>
);
print qq(
  修課屬性: <SELECT name="property">
    <OPTION value="1" selected>必修
    <OPTION value="2">選修
    <OPTION value="3">通識
  </SELECT>
  <BR>
  是否限制學號: <SELECT name="stu_id_filter">
    <OPTION value="1" selected>不設限
    <OPTION value="2">只有奇數
    <OPTION value="3">只有偶數
  </SELECT>
);
print("</TABLE>");

print << "END_OF_HTML"
    <INPUT type=submit value="進入確認選單">
  </FORM>
  本程式不檢查重複選課, 若已經轉檔過後, 要修改屬性, 請先執行批次退選再轉檔<br>
END_OF_HTML

