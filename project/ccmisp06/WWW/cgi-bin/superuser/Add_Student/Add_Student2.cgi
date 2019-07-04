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
    print("密碼錯誤!");
    exit(1);
  }
}
############################################################################
sub Check_For_Noncomplete_Input()
{
  if( ($Input{stu_id} eq "")or($Input{personal_id} eq "")or($Input{name} eq "") ) {
    print("輸入資料不完全!<BR>");
    exit(1);
  }
}
############################################################################
sub Check_For_Already_Exists()
{
  %student = Read_Student($Input{stu_id});
  if($student{name} ne "") {
    print("學生資料早已存在, 學號$Input{stu_id}屬於$student{name}所有!<BR>");
    exit(1);
  }
}
############################################################################
sub Print_Confirm_HTML()
{
  %dept = Read_Dept($Input{dept});

  print qq(
    <HTML>
      <HEAD><TITLE>新增單筆學生資料</TITLE></HEAD>
      <BODY background=$GRAPH_URL/bk.jpg>
      <CENTER><H1>新增單筆學生資料</H1><HR>
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
            <TD align=RIGHT>學號:</TD>
            <TD>$Input{stu_id}</TD>
          </TR>
          <TR>
            <TD align=RIGHT>姓名:</TD>
            <TD>$Input{name}</TD>
          </TR>
          <TR>
            <TD align=RIGHT>身份證號:</TD>
            <TD>$Input{personal_id}</TD>
          </TR>
          <TR>
            <TD align=RIGHT>系所:</TD>
            <TD>($Input{dept})$dept{cname2}</TD>
          <TR>
            <TD align=RIGHT>年級:</TD>
            <TD>$Input{grade}</TD>
          </TR>
          <TR>
            <TD align=RIGHT>班別:</TD>
            <TD>$Input{class}</TD>
          </TR>
        </TABLE><P>
        <INPUT type="SUBMIT" value="寫入資料"><BR>
        <FONT color=RED size=-1>NOTE: 身份證號為預設密碼</FONT>
      </FORM>
      </BODY>
    </HTML>
  );
}