#!/usr/local/bin/perl
###############################################################################
#####  Find_All_Course01.cgi
#####  當學期開課明細表
#####  依照所選擇的條件, 列出當學期開課明細
#####  Updates:
#####    1999/08/05  Created
#####    2009/03/03   新增 "只列出開課教師不見了的課" 選項. Nidalap :D~
###############################################################################

require "../../../LIB/Reference.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Course.pm";
require $LIBRARY_PATH . "Common_Utility.pm";
require $LIBRARY_PATH . "System_Settings.pm";

HTML_Head("當學期開課明細表");


print qq(
  <FORM action = "Find_All_Course02.cgi">
    <SELECT name=last_semester>
);
  for( $i=0; $i<6; $i++ ) {
    ($year, $term) = Last_Semester($i);
    print("<OPTION value=$i ");
    print("SELECTED ")  if( $i==0 );
    print(">$year 學年度第 $term 學期資料</OPTION>\n");
  }
print qq(
           </SELECT>
    <P>
    <INPUT type=checkbox name="teacher_missing">只列出開課教師不見了的課
    <P>
    <INPUT type=submit>
  </FORM>
); 

################################################################################
sub HTML_Head
{
  my($title);
  ($title)=@_;
  print("Content-type: text/html\n\n");
  print qq(
        <html>
		  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
          <SCRIPT language=JAVASCRIPT>
                function Open_Update_Window(link)
                {
                  win=open(link,"openwin","width=350,height=350,resizable");
                  win.creator=self;
                }
          </SCRIPT>
          <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <title>$title</title>
          </head>
          <BODY background="../../Graph/manager.jpg">
            <CENTER>
              <H1>$title</H1>
              <HR size=2 width=50%>
  );
}
