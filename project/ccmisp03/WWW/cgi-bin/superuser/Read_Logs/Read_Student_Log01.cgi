#!/usr/local/bin/perl

print("Content-type:text/html\n\n");
require "../../../../LIB/Reference.pm";

print qq(
  <HEAD><TITLE>查詢學生選課記錄</TITLE></HEAD>
  <BODY background="$GRAPH_URL//ccu-bg.jpg">
    <CENTER>
      <H1>查詢學生選課記錄</H1><HR>
      <FORM action="Read_Student_Log02.cgi" method=POST>
        請輸入要查詢的條件:\n
        <INPUT name="value">
        <P>
        <INPUT type=submit value="查詢">

      </FORM>
    </CENTER>
  </BODY>
);

