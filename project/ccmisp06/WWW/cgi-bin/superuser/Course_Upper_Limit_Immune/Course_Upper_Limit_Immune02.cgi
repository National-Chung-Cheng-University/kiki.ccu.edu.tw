#!/usr/local/bin/perl
##########################################################################
#####   Course_Upper_Limit_Immune02.cgi
#####   額滿加簽 page #2
#####   允許學生加選單一科目, 不受該科目限修額滿人數限制(仍需受其他限制)
#####   Coder: Nidalap
#####   Date : 09/13/2001
##########################################################################
print("Content-type:text/html\n\n");
require "../../library/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
#require $LIBRARY_PATH . "Student.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Course.pm";
require $LIBRARY_PATH . "Password.pm";
require "./Course_Upper_Limit_Immune.pm";
require $LIBRARY_PATH . "System_Settings.pm";
require $LIBRARY_PATH . "Student.pm";
require $LIBRARY_PATH."Error_Message.pm";


%Input   = User_Input();
%student = Read_Student($Input{stu_id});

$pass_result = Check_SU_Password($Input{password}, "su", "su");
if($pass_result ne "TRUE") {
  print("密碼錯誤!");
  exit(1);
}

print qq(
  <HTML>
    <HEAD>
      <TITLE>額滿加簽名單</TITLE>
      <LINK href="http://kiki.ccu.edu.tw/~ccmisp08//style.css" rel="stylesheet" type="text/css" media="screen" />
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    </HEAD>
    <BODY background="$GRAPH_URL./manager.jpg">
      <Center><H1>額滿加簽名單<hr></h1>
      <H2>
);

if( $Input{action} eq "add" ) {
  if( ($Input{stu_id} eq "") or ($Input{course_id} eq "") or ($Input{course_group} eq "")) {
    print("輸入資料不完整!!<BR>\n");
    exit(1);
  }
  if( length($Input{stu_id}) != 9 ) {
    print("錯誤: 學生學號必須為 9 碼!<BR>\n");
    exit(1);
  }
  if( length($Input{course_id}) != 7 ) {
    print("錯誤: 科目代號需為 7 碼!<BR>\n");
    exit(1);
  }
  print("學生 $Input{stu_id}($student{name}) 加簽科目 $Input{course_id}, 班別 $Input{course_group}<BR>\n");
  if($student{name} eq "") {
    print("<FONT color=RED>警告</FONT>! 找不到學生的學籍資料!!<BR>\n");
  }
  $result = Add_Immune_Record($Input{course_id},
                              $Input{course_group}, $Input{stu_id});
  if($result eq "TRUE") {
    print("資料已存入.<BR>\n");
  }elsif($result eq "FALSE") {
    print("該生資料早已存在, 資料未存入!<BR>\n");
  }else{
    print("內部錯誤, 請洽系統程式管理者!!\n");
    exit(0);
  }
}elsif( $Input{action} eq "delete" ) {
  ($course_id, $course_group, $stu_id) = split(/_/, $Input{del_param});
  Delete_Immune_Record($course_id, $course_group, $stu_id);
}

print qq(
  <FORM action="Course_Upper_Limit_Immune01.cgi" method=POST>
    <INPUT type="hidden" name="password" value="$Input{password}">
    <INPUT class=big type=submit value="回上頁">
  </FORM>
);
#print("<input type='button' value='上一頁' onClick='history.back( );'<BR>\n");
