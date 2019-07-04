#!/usr/local/bin/perl

###########################################################################
#####   Same_Course_Transfer2.cgi
#####   上下學期原班批次加選
#####   產生網頁, 選擇上學期的科目班別, 以及這學期的科目班別
#####   Coder: Nidalap
#####   Date : 2004/12/22
#####   後來發現本功能早在 Batch_Add_Student_Course 做了 XD~
###########################################################################
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Course.pm";
@grade = (1,2,3,4);
@class = (A,B,C,D,E,F,G,H);

print("Content-type:text/html\n\n");

%Input = User_Input();
@dept = Find_All_Dept();
@Course_last = Find_All_Course($Input{dept}, "", "LAST");
@Course_this = Find_All_Course($Input{dept});

print qq(
  <HEAD><TITLE>上下學期原班批次加選 -- 選擇科目</TITLE></HEAD>
   <BODY background="$GRAPH_URL./ccu-sbg.jpg">
   <CENTER><H1>上下學期原班批次加選<br>請選擇科目<hr></H1>
    <FORM action="Same_Course_Transfer3.cgi" method=POST>
      <TABLE border=0>
        <TR><TD>
);
print qq(<INPUT type="hidden" name=dept value="$Input{dept}">);
print qq(請選擇上學期的科目:<SELECT name="course_id_last">);
foreach $course (@Course_last) {
  %course = Read_Course($Input{dept},$$course{id},$$course{group}, "HISTORY");
  print qq(<OPTION value="$$course{id}_$$course{group}">[$$course{id}_$$course{group}]$course{cname});
}
print ("</SELECT></TD></TR>");

print qq(<TR><TD>請選擇本學期的科目:<SELECT name="course_id_this">);
foreach $course (@Course_this) {
  %course = Read_Course($Input{dept},$$course{id},$$course{group});
  print qq(<OPTION value="$$course{id}_$$course{group}">[$$course{id}_$$course{group}]$course{cname});
}
print ("</SELECT></TD></TR>");

print ("</SELECT></TD></TR>");    

print qq(
  </TABLE>
  <INPUT type="submit" value="進入確認畫面">
  </FORM>
);