#!/usr/local/bin/perl
##########################################################################
#####   Open_Course_Restriction_Immune01.cgi
#####   開課檢核迴避加簽
#####   允許系所開課時迴避某些開課檢核. 
#####   Coder: Nidalap
#####   Date : 04/16/2002
##########################################################################
print("Content-type:text/html\n\n");
require "../../library/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Open_Course.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Password.pm";
require $LIBRARY_PATH . "Course.pm";
require $LIBRARY_PATH . "Error_Message.pm";
#require "./Open_Course_Restriction_Immune.pm";

%Input = User_Input();
@dept = Find_All_Dept();

$pass_result = Check_SU_Password($Input{password}, "su", "su");
if($pass_result ne "TRUE") {
  print("密碼錯誤!");
  exit(1);
}
$table_content = Form_Open_Course_Restriction_Immune_Table();

print qq(
  <HTML>
    <HEAD><TITLE>開課檢核迴避加簽名單</TITLE></HEAD>
    <BODY background="$GRAPH_URL./manager.jpg">
      <Center><H1>開課檢核迴避加簽名單<hr></h1>
      <FORM action="Open_Course_Restriction_Immune02.cgi" method=POST>
        <INPUT type="hidden" name="password" value="$Input{password}">
        <INPUT type="hidden" name="action" value="add">
        <TABLE border=1>
          <TR>
            <TD bgcolor=YELLOW colspan=2>科目代碼: <INPUT size=7 name="course_id"></TD>
            <TD bgcolor=YELLOW colspan=2>科目班別: <INPUT size=2 name="course_group"></TD>
          </TR>
          <TR>
            <TD>連續三小時</TD>
            <TD>跨區段</TD>
            <TD>一三五/二四</TD>
            <TD>跨天則同截次</TD>
          </TR>
          <TR>
            <TD><INPUT type=CHECKBOX name=r1 value=1></TD>
            <TD><INPUT type=CHECKBOX name=r2 value=1></TD>
            <TD><INPUT type=CHECKBOX name=r3 value=1></TD>
            <TD><INPUT type=CHECKBOX name=r4 value=1></TD>
          <TR>
            <TD bgcolor=YELLOW colspan=4 align=CENTER>
              <INPUT type=submit value="新增/修改資料">
            </TD>
          </TR>
        </TABLE>
      </FORM>
      目前額滿加簽名單:
      <FORM action="Open_Course_Restriction_Immune02.cgi" method=POST>
        <INPUT type="hidden" name="password" value="$Input{password}">
        <INPUT type="hidden" name="action" value="delete">
        <TABLE border=1>
          <TR>
            <TH>刪除</TH>
            <TH>科目代碼</TH>
            <TH>班別</TH>
            <TD>連續三小時</TD>
            <TD>跨區段</TD>
            <TD>一三五/二四</TD>
            <TD>跨天則同截次</TD>
          </TR>
          $table_content
        </TABLE>
        <INPUT type="submit" value="刪除該筆資料">
      </FORM>
    </BODY>
  </HTML>
);

