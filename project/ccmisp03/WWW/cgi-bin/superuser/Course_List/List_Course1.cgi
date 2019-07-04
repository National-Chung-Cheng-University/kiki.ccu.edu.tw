#!/usr/local/bin/perl
print("Content-type:text/html\n\n");

require "../../library/Reference.pm";

print qq(
  <BODY background=$GRAPH_URL/bk.jpg>
    <CENTER><H1>當學期開課科目列表</H1><HR>
    請選擇列表科目限制:
    
    <FORM action="List_Course2.cgi" method=POST>
      限修人數: <INPUT type=checkbox name=number_limit><br>
      
      <INPUT type=submit value="顯示列表">
    </FORM>


);