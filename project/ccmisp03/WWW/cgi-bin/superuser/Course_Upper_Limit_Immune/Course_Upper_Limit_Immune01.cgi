#!/usr/local/bin/perl
##########################################################################
#####   Course_Upper_Limit_Immune01.cgi
#####   額滿加簽
#####   允許學生加選單一科目, 不受該科目限修額滿人數限制(仍需受其他限制)
#####   Coder: Nidalap
#####   Date : 09/13/2001
##########################################################################
print("Content-type:text/html\n\n");
require "../../library/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Password.pm";
require "./Course_Upper_Limit_Immune.pm";
require $LIBRARY_PATH . "Student.pm";
require $LIBRARY_PATH . "Error_Message.pm";

%Input = User_Input();
@dept = Find_All_Dept();

$pass_result = Check_SU_Password($Input{password}, "su", "su");
if($pass_result ne "TRUE") {
  print("密碼錯誤!");
  exit(1);
}
$table_content = Form_Course_Upper_Limit_Immune_Table();

print qq(
  <HTML>
    <HEAD><TITLE>額滿加簽名單</TITLE></HEAD>
    <BODY background="$GRAPH_URL./manager.jpg">
      <Center><H1>額滿加簽名單<hr></h1>
      <FORM action="Course_Upper_Limit_Immune02.cgi" method=POST>
        <INPUT type="hidden" name="password" value="$Input{password}">
        <INPUT type="hidden" name="action" value="add">
        <TABLE border=1>
          <TR>
            <TD bgcolor=YELLOW>學號: <INPUT size=9 name="stu_id"></TD>
            <TD bgcolor=YELLOW>科目代碼: <INPUT size=7 name="course_id"></TD>
            <TD bgcolor=YELLOW>科目班別: <INPUT size=2 name="course_group"></TD>
          </TR>
          <TR>
            <TD bgcolor=YELLOW colspan=4 align=CENTER>
              <INPUT type=submit value="新增/修改資料">
            </TD>
          </TR>
        </TABLE>
      </FORM>
      目前額滿加簽名單:
      <FORM action="Course_Upper_Limit_Immune02.cgi" method=POST>
        <INPUT type="hidden" name="password" value="$Input{password}">
        <INPUT type="hidden" name="action" value="delete">
        <TABLE border=1>
          <TR>
            <TH>刪除</TH>
            <TH>科目代碼</TH>
            <TH>班別</TH>
            <TH>學生</TH>
          </TR>
          $table_content
        </TABLE>
        <INPUT type="submit" value="刪除該筆資料">
      </FORM>
    </BODY>
  </HTML>
);

