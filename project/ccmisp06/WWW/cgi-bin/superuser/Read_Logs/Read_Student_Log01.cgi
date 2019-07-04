#!/usr/local/bin/perl

print("Content-type:text/html\n\n");
require "../../../../LIB/Reference.pm";

print $EXPIRE_META_TAG;
print qq(
  <HEAD><TITLE>查詢學生選課記錄</TITLE></HEAD>
  <BODY background="$GRAPH_URL//ccu-bg.jpg">
    <CENTER>
      <H1>查詢學生選課記錄</H1><HR>
      <FORM action="Read_Student_Log02.cgi" method=POST>
        請輸入要查詢的條件:\n
        <INPUT name="value">
        <P>
        <INPUT type=CHECKBOX name="NO_LOGIN">過濾登入(Login)訊息
        <INPUT type=CHECKBOX name="NO_ONLINE">過濾仍在線上(Online)訊息
        <INPUT type=CHECKBOX name="HIGHLIGHT" checked>開啟醒目提示
        <P>
        <SELECT name="LOGFILE">
          <OPTION value="online" selected>目前學生選課紀錄檔
          <OPTION value="previous">備份學生選課紀錄檔
        </SELECT>
        <P>
        <INPUT type=submit value="查詢">
      </FORM>
    </CENTER>
  </BODY>
);

