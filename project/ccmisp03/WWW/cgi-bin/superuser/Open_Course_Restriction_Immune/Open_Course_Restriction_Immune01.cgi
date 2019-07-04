#!/usr/local/bin/perl
##########################################################################
#####   Open_Course_Restriction_Immune01.cgi
#####   �}���ˮְj�ץ[ñ
#####   ���\�t�Ҷ}�Үɰj�׬Y�Ƕ}���ˮ�. 
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
  print("�K�X���~!");
  exit(1);
}
$table_content = Form_Open_Course_Restriction_Immune_Table();

print qq(
  <HTML>
    <HEAD><TITLE>�}���ˮְj�ץ[ñ�W��</TITLE></HEAD>
    <BODY background="$GRAPH_URL./manager.jpg">
      <Center><H1>�}���ˮְj�ץ[ñ�W��<hr></h1>
      <FORM action="Open_Course_Restriction_Immune02.cgi" method=POST>
        <INPUT type="hidden" name="password" value="$Input{password}">
        <INPUT type="hidden" name="action" value="add">
        <TABLE border=1>
          <TR>
            <TD bgcolor=YELLOW colspan=2>��إN�X: <INPUT size=7 name="course_id"></TD>
            <TD bgcolor=YELLOW colspan=2>��دZ�O: <INPUT size=2 name="course_group"></TD>
          </TR>
          <TR>
            <TD>�s��T�p��</TD>
            <TD>��Ϭq</TD>
            <TD>�@�T��/�G�|</TD>
            <TD>��ѫh�P�I��</TD>
          </TR>
          <TR>
            <TD><INPUT type=CHECKBOX name=r1 value=1></TD>
            <TD><INPUT type=CHECKBOX name=r2 value=1></TD>
            <TD><INPUT type=CHECKBOX name=r3 value=1></TD>
            <TD><INPUT type=CHECKBOX name=r4 value=1></TD>
          <TR>
            <TD bgcolor=YELLOW colspan=4 align=CENTER>
              <INPUT type=submit value="�s�W/�ק���">
            </TD>
          </TR>
        </TABLE>
      </FORM>
      �ثe�B���[ñ�W��:
      <FORM action="Open_Course_Restriction_Immune02.cgi" method=POST>
        <INPUT type="hidden" name="password" value="$Input{password}">
        <INPUT type="hidden" name="action" value="delete">
        <TABLE border=1>
          <TR>
            <TH>�R��</TH>
            <TH>��إN�X</TH>
            <TH>�Z�O</TH>
            <TD>�s��T�p��</TD>
            <TD>��Ϭq</TD>
            <TD>�@�T��/�G�|</TD>
            <TD>��ѫh�P�I��</TD>
          </TR>
          $table_content
        </TABLE>
        <INPUT type="submit" value="�R���ӵ����">
      </FORM>
    </BODY>
  </HTML>
);

