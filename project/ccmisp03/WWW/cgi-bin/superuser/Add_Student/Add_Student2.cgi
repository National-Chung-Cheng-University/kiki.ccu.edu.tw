#!/usr/local/bin/perl

######### require .pm #########

require "../../library/Reference.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Error_Message.pm";

######### Main Program Here #########
my(%Input);
%Input=User_Input();
@dept = Find_All_Dept();

print("Content-type:text/html\n\n");

Check_For_Password();
Check_For_Noncomplete_Input();
Check_For_Already_Exists();
Print_Confirm_HTML();
############################################################################
sub Check_For_Password()
{
  $pass_result = Check_SU_Password($Input{password}, "su", "su");
  if($pass_result ne "TRUE") {
    print("�K�X���~!");
    exit(1);
  }
}
############################################################################
sub Check_For_Noncomplete_Input()
{
  if( ($Input{stu_id} eq "")or($Input{personal_id} eq "")or($Input{name} eq "") ) {
    print("��J��Ƥ�����!<BR>");
    exit(1);
  }
}
############################################################################
sub Check_For_Already_Exists()
{
  %student = Read_Student($Input{stu_id});
  if($student{name} ne "") {
    print("�ǥ͸�Ʀ��w�s�b, �Ǹ�$Input{stu_id}�ݩ�$student{name}�Ҧ�!<BR>");
    exit(1);
  }
}
############################################################################
sub Print_Confirm_HTML()
{
  %dept = Read_Dept($Input{dept});

  print qq(
    <HTML>
      <HEAD><TITLE>�s�W�浧�ǥ͸��</TITLE></HEAD>
      <BODY background=$GRAPH_URL/bk.jpg>
      <CENTER><H1>�s�W�浧�ǥ͸��</H1><HR>
      <FORM action="Add_Student3.cgi" method=POST>
        <INPUT type=hidden name=password value="$Input{password}">
        <INPUT type=hidden name=stu_id value="$Input{stu_id}">
        <INPUT type=hidden name=name value="$Input{name}">
        <INPUT type=hidden name=personal_id value="$Input{personal_id}">
        <INPUT type=hidden name=dept value="$Input{dept}">
        <INPUT type=hidden name=grade value="$Input{grade}">
        <INPUT type=hidden name=class value="$Input{class}">
        
        <TABLE border=0>
          <TR>
            <TD align=RIGHT>�Ǹ�:</TD>
            <TD>$Input{stu_id}</TD>
          </TR>
          <TR>
            <TD align=RIGHT>�m�W:</TD>
            <TD>$Input{name}</TD>
          </TR>
          <TR>
            <TD align=RIGHT>�����Ҹ�:</TD>
            <TD>$Input{personal_id}</TD>
          </TR>
          <TR>
            <TD align=RIGHT>�t��:</TD>
            <TD>($Input{dept})$dept{cname2}</TD>
          <TR>
            <TD align=RIGHT>�~��:</TD>
            <TD>$Input{grade}</TD>
          </TR>
          <TR>
            <TD align=RIGHT>�Z�O:</TD>
            <TD>$Input{class}</TD>
          </TR>
        </TABLE><P>
        <INPUT type="SUBMIT" value="�g�J���"><BR>
        <FONT color=RED size=-1>NOTE: �����Ҹ����w�]�K�X</FONT>
      </FORM>
      </BODY>
    </HTML>
  );
}