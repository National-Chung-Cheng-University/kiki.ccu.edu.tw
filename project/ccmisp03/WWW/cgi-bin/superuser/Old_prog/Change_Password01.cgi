#!/usr/local/bin/perl

######################################################################
#####  Change_Password01.cgi
#####  �t�ҭק�K�X
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
   <HTML><HEAD><TITLE>�ק�K�X���G</TITLE></HEAD>
   <body bgcolor=white background=$GRAPH_URL//ccu-sbg.jpg>
   <center>
    <table border=0 width=50%>
     <tr>
      <td>�t�O:</td><td> $Dept{cname} </td>
      <td>�~��:</td><td> $Input{grade} </td>
      <td>$YEAR�~�ײ�$TERM�Ǵ�</td>
     </tr>
    </table>
   <hr width=40%>
    <font color=RED size=6>�ק�K�X���G</font>
   <hr width=40%>
);
if( $Input{new_password} ne $Input{check_password} ) {
  print("�z��J���s�K�X�νT�{�K�X���ŦX!");
  goto END;
}
if( length($Input{new_password})<5 ) {
  print("�s�K�X�ФŤ֩�5�Ӧr��!");
  goto END;
}
if( length($Input{new_password})>10 ) {
  print("�s�K�X�ФŦh��10�Ӧr��!");
  goto END;
}

#$salt = "pa";
#$Input{new_password} = Crypt($Input{new_password}, $salt);
#$Input{new_password} = $salt . $Input{new_password};

$new = Change_Dept_Password($Input{id}, $Input{old_password}, $Input{new_password});
print("<br>�z���K�X�w�g�ק�, �Шc�O�z���K�X!<br>\n");

$new =~ s/^..//;

END:
  print("<br><hr>\n");
  Links1($Dept{id},$Input{grade},$new);  
  exit(1);
