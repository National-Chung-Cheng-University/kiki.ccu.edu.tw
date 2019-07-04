#!/usr/local/bin/perl 

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Checking_State_Map.pm";

my(%Input,%Dept);
my($crypt_salt);

print "Content-type: text/html"."\n\n";
%Input= User_Input();

#print("$Input{password}\n");
#print("$Input{crypt}\n");

$crypt_salt = Read_Crypt_Salt($Input{dept_cd}, "dept");
if($Input{crypt} ne "1")
{
 $Input{password} = Crypt($Input{password}, $crypt_salt);
}
#print("input pass = $Input{password}<br>");

Check_Dept_Password($Input{dept_cd}, $Input{password});

if((Check_Dept_State($Input{dept_cd}) == 0) and ($SUPERUSER ne "1")){
   SYS_NOT_ALLOWED();
   exit();
}


if($Input{grade} eq "") {$Input{grade}=1;}

%Dept=Read_Dept($Input{dept_cd});

## Begin of HTML ##

print qq(
 <html>
   <head>
    <title> $SUB_SYSTEM_NAME�}�ƽҨt�Υ\\���� </title>
   </head>
   <body background=$GRAPH_URL/ccu-sbg.jpg>
   <center>
    <br>
    <table border=0 width=40%>
     <tr>
      <td bgcolor=eeeeee>�t�O:</td><td bgcolor=eeeeee> $Dept{cname} </td>
      <td bgcolor=eeeeee>�~��:</td><td bgcolor=eeeeee> $Input{grade} </td></tr><tr>
      <th colspan=4>$YEAR�~�ײ�$TERM�Ǵ�<FONT color=RED>$SUB_SYSTEM_NAME</FONT>�}�Ҩt��</th>
     </tr>
    </table>
   <br>
   <hr width=40%>
    <font size=5 color=brown>�\\����</font>
   <br>
   <hr width=40%><br><br>
   
   <form action=Open_Course_1.cgi method=post>
   <input type=hidden name=dept_cd value=$Dept{id}>
   <input type=hidden name=grade value=$Input{grade}>
   <input type=hidden name=password value=$Input{password}>
   <input type=submit value=�s�W��Ǵ��}�Ҭ��>
   </form>   
    <FORM action="Modify_Course.cgi" method=POST>
       <input type=hidden name=dept_id value=$Dept{id}>
       <input type=hidden name=grade   value=$Input{grade}>
       <input type=hidden name=password value=$Input{password}>
       <input type=submit value="�ק�ΧR����Ǵ��w�}���">
    </FORM>
    <form action=Show_Course_1.cgi method=post>
    <input type=hidden name=dept_cd value=$Dept{id}>
   <input type=hidden name=grade value=$Input{grade}>
   <input type=hidden name=password value=$Input{password}>
   <input type=submit value=�d�߷�Ǵ��w�}���>
   </form>
   <FORM action="Print_Course.cgi" method="POST">
     <INPUT type=hidden name=dept_id value=$Dept{id}>
     <INPUT type=hidden name=grade   value=$Input{grade}>
     <INPUT type=hidden name=password value=$Input{password}>
     <INPUT type=submit value=�C�L��Ǵ��w�}���>
   </FORM>
   <FORM action="Query/Query_1.cgi" method="POST">
     <INPUT type=hidden name=dept_cd value=$Dept{id}>
     <INPUT type=hidden name=grade   value=$Input{grade}>
     <INPUT type=hidden name=password value=$Input{password}>
     <INPUT type=submit value="�d�߭׽ҾǥͦW��">
   </FORM>
   <FORM action="Change_Password00.cgi" method="POST">
     <INPUT type=hidden name=password value=$Input{password}>
     <INPUT type=hidden name=id value=$Dept{id}>
     <INPUT type=hidden name=grade value=$Input{grade}>
     <INPUT type=submit value="�ק�K�X">
   </FORM>

   <FONT size=-1 color=RED>�Y�}�Үɦ��ݭn�]�w���ױ���, �ФŨϥ�Netscape�s����!</FONT><BR>
    <IMG src="$GRAPH_URL/new1.gif">
    [<a href=$HOME_URL/UserGuide/>�}�Ҩt�ξާ@��U</a>|
    <A href=$HOME_URL/UserGuide/project/faq.html><fontcolor=RED>�������g�Ьݳo</font></font>]
    <br><br>
   <hr>
    [<A href="http://www.ccu.edu.tw">�����j�ǭ���</A>| 
     <A href=$HOME_URL>�}�ƿ�Ҩt�έ���</A>
    ]
    <br>
   </center>
   </body>
  </html>
);


sub SYS_NOT_ALLOWED
{
print << "End_of_HTML";
Content-type: text/html


<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <title>���~�T��</title>
<style>
  <!--
     A  {
           text-decoration: none;
           color:#0070A6
        }
        -->
</style>

</head>
<body bgcolor=white>
<center>
<font size=5 color=#cc4444>�ثe�ëD�}�ҩνҵ{���ʮɶ��I�I<br>
�ЦV�оǲսT�{�}�ƽҤνҵ{���ʮɶ��A����<br></font>
</center>
</body>
</html>
End_of_HTML
}

