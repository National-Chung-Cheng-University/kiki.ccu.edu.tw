#!/usr/local/bin/perl
##########################################################################
#####   Modify_Credit_Upper_Limit02.cgi 
#####   �ק�ӧO�ǥͿ�ҾǤ��W�� page #2
#####   Coder: Nidalap
#####   Date : 09/04/2001
##########################################################################
print("Content-type:text/html\n\n");
require "../../library/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Password.pm";
require $LIBRARY_PATH . "Student.pm";
require $LIBRARY_PATH . "Error_Message.pm";
require "./Modify_Credit_Upper_Limit.pm";

%Input = User_Input();
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
    <!input type=hidden name=password value=$password>
    <input type=submit value=�^�W��>
  </form>
);
##########################################################################
sub Modify_Credit_Upper_Limit_Form()
{
#  print("modify");
  print qq(
    <HTML>
      <HEAD><TITLE>�ק�ӧO�ǥͿ�ҾǤ��W��</TITLE></HEAD>
      <BODY background="$GRAPH_URL./manager.jpg">
        <Center><H1>�ק�ӧO�ǥͿ�ҾǤ��W��<hr></h1>
        �ǥ� $Input{id}($student{name})���Ǥ��W����אּ $Input{limit}<BR>
  );
  Modify_Credit_Upper_Limit($Input{id}, $Input{limit});
}
##########################################################################
sub Delete_Credit_Upper_Limit_Form()
{
  print qq(
    <HTML>
      <HEAD><TITLE>�ק�ӧO�ǥͿ�ҾǤ��W��</TITLE></HEAD>
      <BODY background="$GRAPH_URL./manager.jpg">
        <Center><H1>�ק�ӧO�ǥͿ�ҾǤ��W��<hr></h1>
  );
  Delete_Credit_Upper_Limit($Input{delete});
}

