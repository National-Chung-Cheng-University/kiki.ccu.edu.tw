#!/usr/local/bin/perl

###########################################################################
#####   Transfer_Course4.cgi
#####   多對多轉必修/必選課
#####   列出五個系級班的選擇, 依照亂數轉入五個班別.
#####   Coder: Nidalap
#####   Updates:
#####     2001/09/04  Created by Nidalap :D~
#####     2010/09/01  增加了 $SUPERUSER 變數，以方便 Student_Log 紀錄  Nidalap :D~
###########################################################################
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Course.pm";
print("Content-type:text/html\n\n");


$SUPERUSER = 1;					###  紀錄 Student_Log 時會用到
%Input = User_Input();
@dept = Find_All_Dept();
@course = Find_All_Course($Input{dept}, $Input{grade}, "");

print qq(
 <HEAD>
   $EXPIRE_META_TAG
   <TITLE>多對多必修/必選課轉檔</TITLE>
 </HEAD>
 <BODY background="$GRAPH_URL./ccu-sbg.jpg"><CENTER>
   <H1>多對多必修/必選課轉檔<br>轉檔結果<hr></H1>
);
#     <TABLE border=1>
#       <TR><TH bgcolor=YELLOW>科目</TH><TH bgcolor=YELLOW>學生</TH></TR>
#);

foreach $key (sort keys %Input) {
#  print("$key -> $Input{$key}<BR>\n");
  if( $key =~ /......._../ ) {              ### 科目代碼_班別
    ($course_id, $course_group) = split(/_/, $key);
    @student = split(/_/, $Input{$key});
#    print qq(
#      <TR>
#        <TD>$course_id, $course_group</TD>
#        <TD>@student</TD>
#      </TR>
#    );
    $num = 0;
	print("正在加選: ");
    foreach $student (@student) {
      $num ++;
      Add_Student_Course($student,$Input{dept},$course_id,$course_group,$Input{property});
	  print(" $student");
#      print("Add: $student,$Input{dept},$course_id,$course_group,$Input{property}<BR>");
    }
    print("<P>\n科目 $course_id _ $course_group 共 $num 人加選完成!<BR>\n"); 
  }
}