#!/usr/local/bin/perl
$|=1;
print "Content-type: text/html","\n\n";
#$|=0;

require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Student.pm";
#require $LIBRARY_PATH."Password.pm";
require "Query.pm";

print qq(
  <HTML>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
);
#require $LIBRARY_PATH."Dept.pm";

### 處理使用者輸入的資料 ###
%Input = User_Input();

print qq(
  <BODY bgcolor=LIGHTGREEN>
  <FORM method=POST action="../View_Student_Course3.cgi" target=OUTPUT>
    <INPUT type=hidden name=dept value=$Input{dept}>
    <INPUT type=hidden name=password value=$Input{password}>
    請學生學號: <INPUT name=id>
    
    <INPUT type=submit>
  </FORM>
);
