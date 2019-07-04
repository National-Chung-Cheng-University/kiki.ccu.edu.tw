#!/usr/local/bin/perl

######################################################################
#####  Change_Password01.cgi
#####  系所修改密碼
#####  Coder: Nidalap
#####  Date : Nov 01,1999
######################################################################

printf("Content-type:text/html\n\n");
require "../library/Reference.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Error_Message.pm";

my(%Input,%Dept);

%Input=User_Input();
%Dept=Read_Dept($Input{id});

#while( ($k, $v)=each(%Input) ) {
#  print("$k ---> $v<br>\n");
#}

$crypt_salt = Read_Crypt_Salt($Input{id}, "dept");
#print("salt = $crypt_salt<br>\n");
$Input{old_password} = Crypt($Input{old_password}, $crypt_salt);
Check_Dept_Password($Input{id}, $Input{old_password});

print qq(
   <HTML><HEAD><TITLE>修改密碼結果</TITLE></HEAD>
   <body bgcolor=white background=$GRAPH_URL//ccu-sbg.jpg>
   <center>
    <table border=0 width=50%>
     <tr>
      <td>系別:</td><td> $Dept{cname} </td>
      <td>年級:</td><td> $Input{grade} </td>
      <td>$YEAR年度第$TERM學期</td>
     </tr>
    </table>
   <hr width=40%>
    <font color=RED size=6>修改密碼結果</font>
   <hr width=40%>
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

#$salt = "pa";
#$Input{new_password} = Crypt($Input{new_password}, $salt);
#$Input{new_password} = $salt . $Input{new_password};

$new = Change_Dept_Password($Input{id}, $Input{old_password}, $Input{new_password});
print("<br>您的密碼已經修改, 請牢記您的密碼!<br>\n");

$new =~ s/^..//;

END:
  print("<br><hr>\n");
  Links1($Dept{id},$Input{grade},$new);  
  exit(1);
