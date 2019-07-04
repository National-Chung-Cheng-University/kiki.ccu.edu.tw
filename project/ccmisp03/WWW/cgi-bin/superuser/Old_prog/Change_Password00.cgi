#!/usr/local/bin/perl

######################################################################
#####  Change_Password00.cgi
#####  產生表單讓系所填寫密碼
#####  Coder: Nidalap
#####  Date : Oct 28,1999
######################################################################

printf("Content-type:text/html\n\n");
require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Error_Message.pm";

my(%Input,%Student,%Dept);

%Input=User_Input();
%Dept = Read_Dept($Input{id});


print << "End_of_HTML"
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <TITLE>開排課系統--修改密碼</TITLE>
</head>
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
   <font size=6 color=RED>修改密碼</font>
   <hr width=40%> 
  <FORM action="Change_Password01.cgi" method=POST>
    <TABLE border=0>
      <TR><TD>請輸入您原來的密碼:</TD>
          <TD><INPUT type=password name="old_password"></TD></TR>
      <TR><TD>請輸入您的新密碼:</TD>
          <TD><INPUT type=password name="new_password"></TD></TR>
      <TR><TD>請確認新的密碼:</TD>
          <TD><INPUT type=password name="check_password"></TD></TR>
    </TABLE>
    <INPUT type=hidden name="id" value="$Input{id}">
    <INPUT type="submit" value="確定更改"><p>
  </FORM>
  <hr>
End_of_HTML
;
Links1($Dept{id},$Input{grade},$Input{password});
