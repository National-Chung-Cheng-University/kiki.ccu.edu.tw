#!/usr/local/bin/perl

#################################################################
#####  Show_all_support_course2.cgi
#####  限本系科目一覽表 -- 找出所有有限本系修習的科目
#####  Coder: Nidalap
#####  Date : Nov22, 2000
#################################################################
print("Content-type: text/html\n\n");
require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Error_Message.pm";

my(%Input,%Student,%Dept);
@dept = Find_All_Dept();
%Input=User_Input();

print qq(
  <HTML>
    <HEAD><TITLE>限本系科目一覽表</TITLE></HEAD>
      <BODY background = $GRAPH_URL/bk.jpg>
        <CENTER>
        <H1>限本系科目一覽表</H1><HR>
        列出所有擋修系所6個以上的科目
        <TABLE border=1>
          <TR bgcolor=YELLOW><TH>開課系所</TH><TH>科目代碼</TH><TH>班別</TH><TH>科目名稱</TH><TH>限修人數</TH><TH>擋修系所</TH></TR>
);
$dept_count = @dept;
foreach $dept (sort @dept) {
  @course = Find_All_Course($dept);
  %dept = Read_Dept($dept);
  foreach $course (@course) {
    %course = Read_Course($dept, $$course{id}, $$course{group}, "", "");
    $Ban_dept_count = @{$course{ban_dept}};
    if($Ban_dept_count > 6) {
      print qq(
        <TR>
          <TD>$dept{cname2}</TD>
          <TD>$$course{id}</TD>
          <TD>$$course{group}</TD>
          <TD>$course{cname}</TD>
          <TD>$course{number_limit}</TD>
          <TD>
      );
      if($Ban_dept_count > 10) {
        print("$Ban_dept_count個");
      }else{
        foreach $ban_dept (@{$course{ban_dept}}) {
          print("$ban_dept ");
        }
      }
      print("</TD></TR>");

    }
  }
}
print("</TABLE>");

 