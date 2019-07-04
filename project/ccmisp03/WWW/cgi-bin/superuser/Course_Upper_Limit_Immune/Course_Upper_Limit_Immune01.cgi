#!/usr/local/bin/perl
##########################################################################
#####   Course_Upper_Limit_Immune01.cgi
#####   �B���[ñ
#####   ���\�ǥͥ[���@���, �����Ӭ�ح����B���H�ƭ���(���ݨ���L����)
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
  print("�K�X���~!");
  exit(1);
}
$table_content = Form_Course_Upper_Limit_Immune_Table();

print qq(
  <HTML>
    <HEAD><TITLE>�B���[ñ�W��</TITLE></HEAD>
    <BODY background="$GRAPH_URL./manager.jpg">
      <Center><H1>�B���[ñ�W��<hr></h1>
      <FORM action="Course_Upper_Limit_Immune02.cgi" method=POST>
        <INPUT type="hidden" name="password" value="$Input{password}">
        <INPUT type="hidden" name="action" value="add">
        <TABLE border=1>
          <TR>
            <TD bgcolor=YELLOW>�Ǹ�: <INPUT size=9 name="stu_id"></TD>
            <TD bgcolor=YELLOW>��إN�X: <INPUT size=7 name="course_id"></TD>
            <TD bgcolor=YELLOW>��دZ�O: <INPUT size=2 name="course_group"></TD>
          </TR>
          <TR>
            <TD bgcolor=YELLOW colspan=4 align=CENTER>
              <INPUT type=submit value="�s�W/�ק���">
            </TD>
          </TR>
        </TABLE>
      </FORM>
      �ثe�B���[ñ�W��:
      <FORM action="Course_Upper_Limit_Immune02.cgi" method=POST>
        <INPUT type="hidden" name="password" value="$Input{password}">
        <INPUT type="hidden" name="action" value="delete">
        <TABLE border=1>
          <TR>
            <TH>�R��</TH>
            <TH>��إN�X</TH>
            <TH>�Z�O</TH>
            <TH>�ǥ�</TH>
          </TR>
          $table_content
        </TABLE>
        <INPUT type="submit" value="�R���ӵ����">
      </FORM>
    </BODY>
  </HTML>
);

