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

$pass_result = Check_SU_Password($Input{password}, "su", "su");
if($pass_result ne "TRUE") {
  print("�K�X���~!");
  exit(1);
}

print qq(
  <HTML>
    <HEAD><TITLE>�s�W�浧�ǥ͸��</TITLE></HEAD>
    <BODY background=$GRAPH_URL/bk.jpg>
      <CENTER><H1>�s�W�浧�ǥ͸��</H1><HR>
      <FORM action="Add_Student2.cgi" method=POST>
        <INPUT type=hidden name=password value="$Input{password}">
        <TABLE border=0>
          <TR>
            <TD align=RIGHT>�Ǹ�:</TD>
            <TD><INPUT name="stu_id" size=10></TD>
          </TR>
          <TR>
            <TD align=RIGHT>�m�W:</TD>
            <TD><INPUT name="name" size=10></TD>
          </TR>
          <TR>
            <TD align=RIGHT>�����Ҹ�:</TD>
            <TD><INPUT name="personal_id" size=10></TD>
          </TR>
          <TR>
            <TD align=RIGHT>�t��:</TD>
            <TD><SELECT name="dept">
);
foreach $dept (@dept) {
  %dept = Read_Dept($dept);
  print qq(   <OPTION value="$dept">($dept)$dept{cname2});
}
print qq(
            </SELECT></TD>
          <TR>
            <TD align=RIGHT>�~��:</TD>
            <TD>
              <SELECT name="grade">
                <OPTION value=1>1
                <OPTION value=2>2
                <OPTION value=3>3
                <OPTION value=4>4
              </SELECT>
            </TD>
          </TR>
          <TR>
            <TD align=RIGHT>�Z�O:</TD>
            <TD>
              <SELECT name="class">
                <OPTION value=A>A
                <OPTION value=B>B
                <OPTION value=C>C
                <OPTION value=D>D
              </SELECT>
            </TD>
          </TR>
        </TABLE><P>
        <INPUT type="SUBMIT" value="�i�J�T�{���"><BR>
        <FONT color=RED size=-1>NOTE: �����Ҹ����w�]�K�X</FONT>
      </FORM>
    </BODY>
  </HTML>
);