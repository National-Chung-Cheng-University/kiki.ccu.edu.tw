#!/usr/local/bin/perl
##########################################################################
#####   Create_Password1.cgi
#####   批次產生新生密碼
#####   Coder: Nidalap
#####   Date : 2001/08/09
#####   Note : 原政策是產生隨機密碼, 今年改為預設為身份證號
#####          系統讀取各系所預定學號範圍, 然後依照該範圍產生新生密碼.
##########################################################################
print("Content-type:text/html\n\n");
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Password.pm";
$fs = "<FONT size=2>";

%Input = User_Input();

#$result = Check_SU_Password($Input{password}, "su", "su");
#if( $result ne "TRUE" ) {
#  print("Password Check Error!!");
#  exit(0);
#}

print qq (
  <HEAD><TITLE>產生新生密碼</TITLE></HEAD>
  <BODY>
    <CENTER>
      <H1>產生新生密碼 -- 步驟1/3</H1>
      <HR>
      <FORM action="Create_Password2.cgi" method=POST>
      
      請在以下欄位中輸入各系所預計起訖學號:
      <TABLE border=0><TR><TD width=80%>
      
      <TABLE border=0>
        <TR>
          <TH width=50% bgcolor=YELLOW>各系所預計起訖學號</TH>
          <TH width=50% bgcolor=YELLOW>格式範例</TH>
        </TR>
        <TR>
          <TD><TEXTAREA name="input" rows=15 cols=50></TEXTAREA></TD>
          <TD valign=TOP>
          <FONT size=2 color=RED>
           * 一行為一個起訖, 系統將產生起號到迄號間所有密碼.<BR>
           * 系所與學號之間要用一個或多個半形空白隔開.<BR>
           * 學號起訖以 "~" 分隔, 不可含空白字元<BR>
          </FONT>
          <HR>
          $fs
          中文系  &nbsp&nbsp&nbsp488110055~488110063<BR>
          外文系  &nbsp&nbsp&nbsp488115055~488115062<BR>
          資工系  &nbsp&nbsp&nbsp488410055~488410066<BR>
          機械系  &nbsp&nbsp&nbsp488420102~488420115<BR>
          化工系  &nbsp&nbsp&nbsp488425054~488425062<BR>
          經濟系  &nbsp&nbsp&nbsp488510067~488510085<BR>
          資管系  &nbsp&nbsp&nbsp488530057~488530065<BR>
          法律系法制組    &nbsp&nbsp&nbsp488620047~488620055<BR>
          法律系法學組    &nbsp&nbsp&nbsp488610048~488610058<BR>
          </TD>
        </TR>
      </TABLE>

      </TD></TR></TABLE>
      
      <INPUT type=SUBMIT value="進入確認畫面">
);
