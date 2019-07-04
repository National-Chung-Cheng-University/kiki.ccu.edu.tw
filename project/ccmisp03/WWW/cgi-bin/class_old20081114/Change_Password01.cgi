#!/usr/local/bin/perl

printf("Content-type:text/html\n\n");
require "../library/Reference.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Select_Course.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Session.pm";

my(%Student,%Dept);

%Input=User_Input();
($Input{id}, $Input{password}, $login_time, $ip) = Read_Session($Input{session_id});
#print("session_id, id, pass = $Input{session_id}, $Input{id}, $Input{password}<BR>"); 

%Student=Read_Student($Input{id});
%Dept=Read_Dept($Student{dept});

#while( ($k, $v)=each(%Input) ) {
#  print("$k ---> $v<br>\n");
#}

$crypt_salt = Read_Crypt_Salt($Input{id}, "student");
$Input{old_password} = Crypt($Input{old_password}, $crypt_salt);
Check_Student_Password($Input{id}, $Input{old_password});

my($HEAD_DATA)=Head_of_Individual($Student{name},$Student{id},$Dept{cname},$Student{grade},$Student{class});

print qq(
  <HTML><HEAD><TITLE>修改密碼結果</TITLE></HEAD>
  <BODY background="$GRAPH_URL./ccu-sbg.jpg">
    <Center>$HEAD_DATA<hr>\n
    <h1>
);
if( $Input{new_password} ne $Input{check_password} ) {
  print("您輸入的新密碼及確認密碼不符合!");
  goto END;
}
if( length($Input{new_password})<5 ) {
  print("新密碼請勿少於5個字元!");
  goto END;
}
if( length($Input{new_password})>10 ) {
  print("新密碼請勿多於10個字元!");
  goto END;
}
if( $Input{new_password} eq $Student{personal_id} ) {
  print("請勿以身份證號做為密碼!\n");
  goto END;
}
if( $Input{new_password} eq $Input{id} ) {
  print("請勿以學號做為密碼!\n");
  goto END;
}

$salt = "aa";
$Input{new_password} = Crypt($Input{new_password}, $salt);
Write_Session($Input{session_id}, $Input{id}, $Input{new_password}, 0);
$Input{new_password} = $salt . $Input{new_password};
Change_Student_Password($Input{id},$Student{dept},$Input{old_password},$Input{new_password});

print("密碼修改完成!<br>\n");

$Input{password} = $Input{new_password};
$Input{password} =~ s/^..//;

END:
  my($LINK)=Select_Course_Link($Input{id},$Input{password});
  print("</h1>$LINK");
  exit(1);