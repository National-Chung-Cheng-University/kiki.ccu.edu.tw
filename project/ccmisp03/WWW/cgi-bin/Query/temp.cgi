#!/usr/local/bin/perl
########################################################################
#####  Query_by_time1.cgi
#####  �H�}�Үɶ��d�ߥ\��
#####  Last Update:
#####   2004/03/02
########################################################################
print "Content-type: text/html","\n\n";

require "../library/Reference.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Open_Course.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Error_Message.pm";

%Input = User_Input();
#Check_SU_Password($Input{password}, "dept", $Input{dept_cd});

#if($Input{get_my_table} == 1) {
#  @my_table = Get_My_Table($Input{stu_id}, "free");
#}

@dept = Find_All_Dept();
print qq(
  <body bgcolor=white background=$GRAPH_URL/ccu-sbg.jpg>
  <center>
  <form name=form1 method=post action=Query_by_time2.cgi>
    <input type=hidden name=dept_cd value=$Input{dept_cd}>
    <input type=hidden name=password value=$Input{password}>
  <TABLE border=0>
    <TR><TD valign=TOP align=CENTER>
    <FONT size=2>
    �п�ܾǨt<BR>(��Ctrl�i�ƿ�):<BR>
    <SELECT name=dept multiple size=25>
);
foreach $dept (@dept) {
  %dept = Read_Dept($dept);
  print("  <OPTION value=\"$dept\">$dept{cname2}\n");  
}
print qq(
    </SELECT>
  </TD>
  <TD valign=TOP align=CENTER>
  �п�ܮɬq:
);

Print_Timetable_Select();

print qq(
    </TD></TR>
  </TABLE>
  <p>
  <center>
  <input type="submit" value="�e�X���">
  <input type="reset" value="���s��g">
  </form><hr>
  </center>
  </body>
  </html>
);
 
######################################################################################
