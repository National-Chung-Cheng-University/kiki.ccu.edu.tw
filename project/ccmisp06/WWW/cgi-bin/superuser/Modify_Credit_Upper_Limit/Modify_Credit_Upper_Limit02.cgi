#!/usr/local/bin/perl
##############################################################################################
#####   Modify_Credit_Upper_Limit02.cgi 
#####   修改個別學生選課學分上限 page #2
#####   Coder: Nidalap
#####   Date : 
#####     2001/09/04 Created by Nidalap :D~
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

#Print_Hash(%Input);

 $su_flag = Check_SU_Password($Input{password}, "su");
 if( $su_flag ne "TRUE" ) {
   print("Password check error! system logged!!\n");
   exit();
 }

%student = Read_Student($Input{id});

%upper_limit = Read_Credit_Upper_Limit_Data();
$table_content = Form_Credit_Upper_Limit_Table(%upper_limit);

if( $Input{action} eq "modify" ) {
  Modify_Credit_Upper_Limit_Form();
}elsif( $Input{action} eq "delete" ) {
  Delete_Credit_Upper_Limit_Form();
}

print qq(
  <form method=post action=Modify_Credit_Upper_Limit01.cgi>
    <input type=hidden name=password value=$Input{password}>
    <input class=big type=submit value=回上頁>
  </form>
);
##########################################################################
sub Modify_Credit_Upper_Limit_Form
{
#  print("modify");
  print qq(
    <HTML>
      <HEAD>
        <TITLE>修改個別學生選課學分上限</TITLE>
        <LINK href="http://kiki.ccu.edu.tw/~ccmisp08//style.css" rel="stylesheet" type="text/css" media="screen" />
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      </HEAD>
      <BODY background="$GRAPH_URL./manager.jpg">
        <Center><H1>修改個別學生選課學分上限<hr></h1>
        <H2>學生 $Input{id}($student{name})的學分上限更改為 $Input{limit}<BR>
  );
  Modify_Credit_Upper_Limit($Input{id}, $Input{limit});
}
##########################################################################
sub Delete_Credit_Upper_Limit_Form
{
  print qq(
    <HTML>
      <HEAD><TITLE>修改個別學生選課學分上限</TITLE></HEAD>
      <BODY background="$GRAPH_URL./manager.jpg">
        <Center><H1>修改個別學生選課學分上限<hr></h1>
  );
  Delete_Credit_Upper_Limit($Input{delete});
}

