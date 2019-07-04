#!/usr/local/bin/perl
########################################################################
#####  Query_by_name1.cgi
#####  以科目名稱查詢功能
#####  Last Update:
#####   2008/05/30
########################################################################
print "Content-type: text/html","\n\n";

require "../library/Reference.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Open_Course.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Error_Message.pm";


%Input = User_Input();
#Check_SU_Password($Input{password}, "dept", $Input{dept_cd});

if($Input{get_my_table} == 1) {
  @my_table = Get_My_Table($Input{stu_id}, "free");
}

@dept = Find_All_Dept();
print qq(
  <HEAD>
    <TITLE>以科目名稱查詢開課資料 -- 請選擇條件</TITLE>
    <LINK rel="stylesheet" type="text/css" href="$HOME_URL/font.css">
  </HEAD>
  <body bgcolor=white background=$GRAPH_URL/ccu-sbg.jpg>
  <center>
    <SPAN class="title1">以科目名稱查詢開課資料</SPAN>
    <IMG src=$TITLE_LINE>
  <form name=form1 method=post action=Query_by_time2.cgi>
    <input type=hidden name=dept_cd value=$Input{dept_cd}>
    <input type=hidden name=password value=$Input{password}>
  <TABLE border=0>
    <TR><TD valign=TOP align=CENTER>
    <FONT size=2>
    請選擇學系<BR>(按Ctrl可複選):<BR>
    <SELECT name=dept multiple size=25>
);
foreach $dept (@dept) {
  %dept = Read_Dept($dept);
  print("  <OPTION value=\"$dept\">$dept{cname2}\n");  
}
print qq(
    </SELECT>
  </TD>
  <TD valign=CENTER align=CENTER>
    <TABLE border=1>
      <TR><TD>科目名稱</TD><TD><INPUT name="course_cname"></TD></TR>
      <TR><TD>教師姓名</TD><TD><INPUT name="teacher_name"></TD></TR>
);


print qq(
    </TABLE>  
    </TD></TR>
    <TR>
      <TD colspan=2>
        <INPUT type=RADIO name=query_type value=1 CHECKED>查詢所有 "只" 使用到這些時段的科目<BR>
        <INPUT type=RADIO name=query_type value=2>查詢所有使用到這些時段的科目
      </TD>
    </TR>
  </TABLE>
  <p>
  <center>
  <input type="submit" value="送出資料">
  <input type="reset" value="重新填寫">
  </form><hr>
  </center>
  </body>
  </html>
);
 
######################################################################################
