#!/usr/local/bin/perl
###############################################################################################
#####   Modify_Credit_Upper_Limit01.cgi 
#####   修改個別學生選課學分上限
#####   Coder: Nidalap
#####   Updates : 
#####     2001/08/29 Created by Nidalap
#####     2010/02/26 怎麼沒有加入密碼檢查！？該打！ 另，加入學生姓名與增加字體大小 Nidalap :D~
###############################################################################################
print("Content-type:text/html\n\n");
require "../../library/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Password.pm";
require $LIBRARY_PATH . "Student.pm";
require $LIBRARY_PATH . "Common_Utility.pm";
require $LIBRARY_PATH . "Error_Message.pm";
require $LIBRARY_PATH . "System_Settings.pm";
require $LIBRARY_PATH . "Dept.pm";
require "./Modify_Credit_Upper_Limit.pm";

%Input = User_Input();

 $su_flag = Check_SU_Password($Input{password}, "su");
 if( $su_flag ne "TRUE" ) {
   print("Password check error! system logged!!\n");
   exit();
 }

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
    <HEAD>
      <TITLE>修改個別學生選課學分上限</TITLE>
      <LINK href="$HOME_URL/style.css" rel="stylesheet" type="text/css" media="screen" />
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    </HEAD>
    <BODY background="$GRAPH_URL./manager.jpg">
      <Center><H1>修改個別學生選課學分上限<hr></h1>
      <FORM action="Modify_Credit_Upper_Limit02.cgi" method=POST>
        <INPUT type="hidden" name="action" value="modify">
        <INPUT type="hidden" name="password" value="$Input{password}">
        <TABLE border=1>
          <TR>
            <TD bgcolor=YELLOW>學號: <INPUT class=big size=9 name="id"></TD>
            <TD bgcolor=YELLOW>學分上限: <INPUT class=big size=2 name="limit"></TD>
            <TD colspan=2 align=CENTER><INPUT class=big type=submit value="新增/修改資料"></TD>
          </TR>
        </TABLE>
      </FORM>
      <H2>目前特殊學分上限名單:</H2>
      <FORM action="Modify_Credit_Upper_Limit02.cgi" method=POST>
        <INPUT type="hidden" name="action" value="delete">
        <INPUT type="hidden" name="password" value="$Input{password}">
        <TABLE border=1>
          <TR><TH>刪除</TH><TH>學號</TH><TH>系所</TH><TH>姓名</TH><TH>學分上限</TH></TR>
          $table_content
        </TABLE>
        <INPUT class=big type="submit" value="刪除該筆資料">
      </FORM>
    </BODY>
  </HTML>
END_OF_HTML

