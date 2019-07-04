#!/usr/local/bin/perl
##########################################################################
#####   Open_Course_Restriction_Immune02.cgi
#####   開課檢核迴避加簽 page #2
#####   
#####   Coder: Nidalap
#####   Date : 04/16/2002
##########################################################################
print("Content-type:text/html\n\n");
require "../../library/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Open_Course.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Course.pm";
require $LIBRARY_PATH . "Password.pm";
require $LIBRARY_PATH . "Error_Message.pm";
#require "./Open_Course_Restriction_Immune.pm";

%Input   = User_Input();

$pass_result = Check_SU_Password($Input{password}, "su", "su");
if($pass_result ne "TRUE") {
  print("密碼錯誤!");
  exit(1);
}

print qq(
  <HTML>
    <HEAD><TITLE>開課檢核迴避加簽</TITLE></HEAD>
    <BODY background="$GRAPH_URL./manager.jpg">
      <Center><H1>開課檢核迴避加簽<hr></h1>
);

if( $Input{action} eq "add" ) {
  if( ($Input{course_id} eq "") or ($Input{course_group} eq "")) {
    print("輸入資料不完整!!<BR>\n");
    exit(1);
  }
  if( length($Input{course_id}) != 7 ) {
    print("錯誤: 科目代號需為 7 碼!<BR>\n");
    exit(1);
  }
  if( ($Input{r1} != "1") and ($Input{r2} != "1") and
      ($Input{r3} != "1") and ($Input{r4} != "1") )   {
    print("沒有勾選任何迴避規則, 請回上頁確認!<BR>\n");
    exit(1);
  }

  $result = Add_Immune_Record($Input{course_id}, $Input{course_group},
            $Input{r1}, $Input{r2}, $Input{r3}, $Input{r4});
  if($result eq "TRUE") {
    print qq(
      <TABLE border=1>
        <TR>
          <TD>科目代碼</TD>
          <TD>班別</TD>
          <TD>連續三小時</TD>
          <TD>跨區段</TD>
          <TD>一三五/二四</TD>
          <TD>跨天則同截次</TD>
        </TR>
        <TR>
          <TD>$Input{course_id}</TD>
          <TD>$Input{course_group}</TD>
          <TD>$Input{r1}</TD>
          <TD>$Input{r2}</TD>
          <TD>$Input{r3}</TD>
          <TD>$Input{r4}</TD>
        </TR>
      </TABLE>
    );
    print("資料已存入.<BR>\n");
  }elsif($result eq "FALSE") {
    print("該資料早已存在, 資料未存入!<BR>\n");
  }else{
    print("內部錯誤, 請洽系統程式管理者!!\n");
    exit(0);
  }
}elsif( $Input{action} eq "delete" ) {
  ($course_id, $course_group) = split(/_/, $Input{del_param});
  Delete_Immune_Record($course_id, $course_group);
}


