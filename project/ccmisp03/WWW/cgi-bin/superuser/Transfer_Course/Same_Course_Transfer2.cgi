#!/usr/local/bin/perl

###########################################################################
#####   Same_Course_Transfer2.cgi
#####   �W�U�Ǵ���Z�妸�[��
#####   ���ͺ���, ��ܤW�Ǵ�����دZ�O, �H�γo�Ǵ�����دZ�O
#####   Coder: Nidalap
#####   Date : 2004/12/22
#####   ��ӵo�{���\�ভ�b Batch_Add_Student_Course ���F XD~
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
  <HEAD><TITLE>�W�U�Ǵ���Z�妸�[�� -- ��ܬ��</TITLE></HEAD>
   <BODY background="$GRAPH_URL./ccu-sbg.jpg">
   <CENTER><H1>�W�U�Ǵ���Z�妸�[��<br>�п�ܬ��<hr></H1>
    <FORM action="Same_Course_Transfer3.cgi" method=POST>
      <TABLE border=0>
        <TR><TD>
);
print qq(<INPUT type="hidden" name=dept value="$Input{dept}">);
print qq(�п�ܤW�Ǵ������:<SELECT name="course_id_last">);
foreach $course (@Course_last) {
  %course = Read_Course($Input{dept},$$course{id},$$course{group}, "HISTORY");
  print qq(<OPTION value="$$course{id}_$$course{group}">[$$course{id}_$$course{group}]$course{cname});
}
print ("</SELECT></TD></TR>");

print qq(<TR><TD>�п�ܥ��Ǵ������:<SELECT name="course_id_this">);
foreach $course (@Course_this) {
  %course = Read_Course($Input{dept},$$course{id},$$course{group});
  print qq(<OPTION value="$$course{id}_$$course{group}">[$$course{id}_$$course{group}]$course{cname});
}
print ("</SELECT></TD></TR>");

print ("</SELECT></TD></TR>");    

print qq(
  </TABLE>
  <INPUT type="submit" value="�i�J�T�{�e��">
  </FORM>
);