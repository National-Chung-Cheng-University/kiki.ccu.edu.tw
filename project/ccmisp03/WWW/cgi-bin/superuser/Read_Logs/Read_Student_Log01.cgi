#!/usr/local/bin/perl

print("Content-type:text/html\n\n");
require "../../../../LIB/Reference.pm";

print qq(
  <HEAD><TITLE>�d�߾ǥͿ�ҰO��</TITLE></HEAD>
  <BODY background="$GRAPH_URL//ccu-bg.jpg">
    <CENTER>
      <H1>�d�߾ǥͿ�ҰO��</H1><HR>
      <FORM action="Read_Student_Log02.cgi" method=POST>
        �п�J�n�d�ߪ�����:\n
        <INPUT name="value">
        <P>
        <INPUT type=submit value="�d��">

      </FORM>
    </CENTER>
  </BODY>
);

