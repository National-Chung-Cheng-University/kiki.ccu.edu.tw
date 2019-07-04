#!/usr/local/bin/perl
##########################################################################
#####   Create_Password1.cgi
#####   批次產生新生密碼
#####   Coder: Nidalap
#####   Date : 2001/08/09
#####   Note : 原政策是產生隨機密碼, 今年改為預設為身份證號
#####          系統讀取由學籍資料轉來的 student.txt,
#####          為沒密碼的學生產生密碼檔.
##########################################################################
print("Content-type:text/html\n\n");
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Student.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Password.pm";
require $LIBRARY_PATH . "Error_Message.pm";
$fs = "<FONT size=2>";

%Input = User_Input();

##########################  檢查SU密碼是否正確 ###################
$result = Check_SU_Password($Input{password}, "su", "su");
if( $result ne "TRUE" ) {
  print("Password Check Error!!");
  exit(0);
}

##########################  產生請稍後的HTML #####################
print qq (
  <HEAD><TITLE>產生新生密碼</TITLE></HEAD>
  <BODY background=$GRAPH_URL/bk.jpg>
    <CENTER>
      <H1>產生新生密碼</H1>
      <HR>
      密碼產生中, 請稍後...
);
$| = 1;
print "";
###########################
%S = Read_All_Student_Data();
@student = Find_All_Student();

$junk = "";
$count = 0;
foreach $student (@student) {
  $password_file = $STUDENT_PASSWORD_PATH . $student . ".pwd";
  if( not (-e $password_file) ) {
#    print("$student -> $$S{$student}{name} $$S{$student}{personal_id}<BR>\n");
    ($junk, $crypt_salt) = Create_Random_Password();
    $crypt_salt =~ /^(..)/;
    $crypt_salt = $1;       ### 取得Random Crypt salt

    $password = Crypt($$S{$student}{personal_id}, $crypt_salt);
    $password = $crypt_salt . $password;

#    print("($$S{$student}{personal_id}, $crypt_salt) -> $password<BR>\n");
    Change_Student_Password($student, $junk, $junk, $password);
    $count++;
  }
}

############################ JOB FINISHED ########################
print qq(
  共產生 $count 筆新生密碼資料.
);
