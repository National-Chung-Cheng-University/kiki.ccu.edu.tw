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

#$crypt_salt = Read_Crypt_Salt($Input{dept_cd}, "dept");
#if($Input{crypt} ne "1")
#{
# $Input{password} = Crypt($Input{password}, $crypt_salt);
#}
#print("input pass = $Input{password}<br>");

###  Check_Cashier_Password

Print_Header();

Check_Cashier_Password($Input{dept_cd},$Input{password});

#if((Check_Dept_State($Input{dept_cd}) == 0) and ($SUPERUSER ne "1")){
#   SYS_NOT_ALLOWED();
#   exit();
#}

#%Dept=Read_Dept($Input{dept_cd});
$su_flag = "(SU)"  if($SUPERUSER == 1);

## Begin of HTML ##

if( $TERM == 3 ) {
  $show_term = "";
}else{
  $show_term = join("", "第", $TERM, "學期");
}

#Print_Header();

print qq(
   <FORM action="Query/Query_Cashier.cgi" method="POST">
     <INPUT type=hidden name=dept_id value=$Input{dept_cd}>
     <INPUT type=hidden name=password value=$Input{password}>
     <INPUT type=submit value="查詢修課學生名單">
   </FORM>
   &nbsp<P>
   <hr>
    [<A href="http://www.ccu.edu.tw">中正大學首頁</A>| 
     <A href=$HOME_URL>開排選課系統首頁</A>
    ]
    <br>
   </center>
   </body>
  </html>
);
############################################################################################

sub SYS_NOT_ALLOWED
{
  if($Input{grade} eq "") {$Input{grade}=1;}
  
  %Dept=Read_Dept($Input{dept_cd});
  $su_flag = "(SU)"  if($SUPERUSER == 1);

  Print_Header();  
  print qq(
    <font size=5 color=#cc4444>目前並非開課或課程異動時間！！<br>
    請向教學組確認開排課及課程異動時間，謝謝<br></font>

       <FORM action="View_Student_Course1.cgi" method="POST">
         <INPUT type=hidden name=password value=$Input{password}>
         <INPUT type=hidden name=id value=$Dept{id}>
         <INPUT type=hidden name=grade value=$Input{grade}>
         <INPUT type=submit value="檢視學生選課資料">
       </FORM>
    </center>
    </body>
    </html>
  );
}

############################################################################################           

sub Print_Header
{
  print qq(
   <html>
     <head>
      <title> $SUB_SYSTEM_NAME開排選課系統功\能選單 $su_flag</title>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
     </head>
     <body background=$GRAPH_URL/ccu-sbg.jpg>
     <center>
      <br>
      <table border=0 width=40%>
       <tr>
        <td bgcolor=eeeeee>單位別:</td><td bgcolor=eeeeee> 出納組 </td>
       </tr><tr>
        <th colspan=4>$YEAR年度$show_term<FONT color=RED>$SUB_SYSTEM_NAME</FONT>開排選課系統</th>
       </tr>
      </table>
     <br>
     <hr width=40%>
    <font size=5 color=brown>功\能選單</font>
     <br>
     <hr width=40%><br><br>
);



}