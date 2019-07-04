#!/usr/local/bin/perl
##########################################################################
#####   Modify_Credit_Upper_Limit01.cgi 
#####   修改個別學生選課學分上限
#####   Coder: Nidalap
#####   Date : 08/29/2001
##########################################################################
print("Content-type:text/html\n\n");
require "../../library/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Password.pm";
require "./Modify_Credit_Upper_Limit.pm";

%Input = User_Input();

##  未檢查密碼, 安全有漏洞! victora
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
    <HEAD><TITLE>修改個別學生選課學分上限</TITLE></HEAD>
    <BODY background="$GRAPH_URL./manager.jpg">
      <Center><H1>修改個別學生選課學分上限<hr></h1>
      <FORM action="Modify_Credit_Upper_Limit02.cgi" method=POST>
        <INPUT type="hidden" name="action" value="modify">
        <TABLE border=1>
          <TR>
            <TD bgcolor=YELLOW>學號: <INPUT size=9 name="id"></TD>
            <TD bgcolor=YELLOW>學分上限: <INPUT size=2 name="limit"></TD>
            <TD colspan=2 align=CENTER><INPUT type=submit value="新增/修改資料"></TD>
          </TR>
        </TABLE>
      </FORM>
      目前特殊學分上限名單:
      <FORM action="Modify_Credit_Upper_Limit02.cgi" method=POST>
        <INPUT type="hidden" name="action" value="delete">
        <TABLE border=1>
          <TR><TH>刪除</TH><TH>學號</TH><TH>學分上限</TH></TR>
          $table_content
        </TABLE>
        <INPUT type="submit" value="刪除該筆資料">
      </FORM>
    </BODY>
  </HTML>
END_OF_HTML

