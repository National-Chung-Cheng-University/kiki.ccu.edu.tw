#!/usr/local/bin/perl

#################################################################
#####  Show_all_support_course.cgi
#####  支援通識科目一覽表 -- 找出所有有支援通識的科目
#####  Coder: Nidalap
#####  Date : Nov17, 2000
#################################################################
print("Content-type: text/html\n\n");
require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Error_Message.pm";

my(%Input,%Student,%Dept);
%Input=User_Input();
%cge = Read_Cge();

print qq(
  <HTML>
    <HEAD><TITLE>支援通識科目一覽表</TITLE></HEAD>
      <BODY background="$GRAPH_URL/bk.jpg">
        <CENTER>
        <H1>支援通識科目一覽表</H1><HR>
        <FORM method="POST" action="Show_all_support_course2.cgi">
          <TABLE border=1>
            <TR><TD>
              包括通識中心所開科目
                <INPUT type="radio" name="include_cge" value=1>是
                <INPUT type="radio" name="include_cge" value=2>否
            </TD>
            <TR><TD>
            
          </TABLE>
        </FORM>  
              
);
 