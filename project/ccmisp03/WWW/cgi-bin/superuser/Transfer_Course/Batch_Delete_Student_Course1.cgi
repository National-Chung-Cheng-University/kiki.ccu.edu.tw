#!/usr/local/bin/perl

###########################################################################
#####   Batch_Delete_Student_Course1.cgi
#####   �妸�h��
#####   ���ͺ���, ��ܬ�بt�ҤΦ~��
#####   Coder: Nidalap
#####   Date : Jun,02,1999
###########################################################################
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student.pm";
@grade = (1,2,3,4);

print("Content-type:text/html\n\n");

@dept = Find_All_Dept();
print << "TABLE_1"
  <HEAD><TITLE>�妸�h��</TITLE></HEAD>
  <BODY background="$GRAPH_URL./ccu-sbg.jpg">
    <CENTER>
      <H1>�妸�h��<br>�п�ܬ�ة��ݨt��<hr></H1>
      <FORM action="Batch_Delete_Student_Course2.cgi" method="POST">
      <TABLE border=0>
        <TR>
          <TD>
            �t�ҧO:<SELECT name="course_dept">
TABLE_1
;

foreach $dept (@dept) {
  %dept = Read_Dept($dept);
  print qq(<OPTION value=$dept>$dept{cname});
}
print << "TABLE_2"
            
            </SELECT>
          </TD>
        </TR>
      </TABLE>
TABLE_2
;
print qq(<INPUT type="submit" value="�D��Z��"></FORM>);


