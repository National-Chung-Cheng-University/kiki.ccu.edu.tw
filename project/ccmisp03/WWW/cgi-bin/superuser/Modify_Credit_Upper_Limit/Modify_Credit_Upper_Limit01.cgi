#!/usr/local/bin/perl
##########################################################################
#####   Modify_Credit_Upper_Limit01.cgi 
#####   �ק�ӧO�ǥͿ�ҾǤ��W��
#####   Coder: Nidalap
#####   Date : 08/29/2001
##########################################################################
print("Content-type:text/html\n\n");
require "../../library/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Password.pm";
require "./Modify_Credit_Upper_Limit.pm";

%Input = User_Input();

##  ���ˬd�K�X, �w�����|�}! victora
#print("pass = $Input{password}");
#$result = Check_SU_Password($Input{password}, "su", "su");
#if( $result ne "TRUE" ) {
#  print ("bye bye...");
#  exit(0);
#}
%upper_limit = Read_Credit_Upper_Limit_Data();
#print(%upper_limit);
$table_content = Form_Credit_Upper_Limit_Table(%upper_limit);

print << "END_OF_HTML"
  <HTML>
    <HEAD><TITLE>�ק�ӧO�ǥͿ�ҾǤ��W��</TITLE></HEAD>
    <BODY background="$GRAPH_URL./manager.jpg">
      <Center><H1>�ק�ӧO�ǥͿ�ҾǤ��W��<hr></h1>
      <FORM action="Modify_Credit_Upper_Limit02.cgi" method=POST>
        <INPUT type="hidden" name="action" value="modify">
        <TABLE border=1>
          <TR>
            <TD bgcolor=YELLOW>�Ǹ�: <INPUT size=9 name="id"></TD>
            <TD bgcolor=YELLOW>�Ǥ��W��: <INPUT size=2 name="limit"></TD>
            <TD colspan=2 align=CENTER><INPUT type=submit value="�s�W/�ק���"></TD>
          </TR>
        </TABLE>
      </FORM>
      �ثe�S��Ǥ��W���W��:
      <FORM action="Modify_Credit_Upper_Limit02.cgi" method=POST>
        <INPUT type="hidden" name="action" value="delete">
        <TABLE border=1>
          <TR><TH>�R��</TH><TH>�Ǹ�</TH><TH>�Ǥ��W��</TH></TR>
          $table_content
        </TABLE>
        <INPUT type="submit" value="�R���ӵ����">
      </FORM>
    </BODY>
  </HTML>
END_OF_HTML

