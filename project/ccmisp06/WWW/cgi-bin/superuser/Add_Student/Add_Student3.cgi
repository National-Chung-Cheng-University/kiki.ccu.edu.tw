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

%stu = %Input;

$password_file = $STUDENT_PASSWORD_PATH . $stu{stu_id} . ".pwd";
#print("passfile = $password_file<BR>");
($junk, $crypt_salt) = Create_Random_Password();
$crypt_salt =~ /^(..)/;
$crypt_salt = $1;       ### 取得Random Crypt salt
$password = Crypt($stu{personal_id}, $crypt_salt);
$password = $crypt_salt . $password;

#print("($stu{personal_id}, $crypt_salt) -> $password<BR>\n");
Change_Student_Password($stu{stu_id}, $junk, $junk, $password);

Add_Student(%stu);

print qq(
  <HTML>
    <HEAD><TITLE>新增單筆學生資料</TITLE></HEAD>
    <BODY background=$GRAPH_URL/bk.jpg>
    <CENTER><H1>新增單筆學生資料</H1><HR>
    學生資料已加入!
    
);

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