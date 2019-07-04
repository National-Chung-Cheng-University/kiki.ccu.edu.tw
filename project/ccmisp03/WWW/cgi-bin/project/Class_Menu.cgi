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
$su_flag = "(SU)"  if($SUPERUSER == 1);

## Begin of HTML ##

if( $TERM == 3 ) {
  $show_term = "";
}else{
  $show_term = join("", "第", $TERM, "學期");
}

Print_Header();

print qq(
   <form action=Open_Course_1.cgi method=post>
   <input type=hidden name=dept_cd value=$Dept{id}>
   <input type=hidden name=grade value=$Input{grade}>
   <input type=hidden name=password value=$Input{password}>
   <input type=submit value=新增當學期開課科目>
   </form>   
    <FORM action="Modify_Course.cgi" method=POST>
       <input type=hidden name=dept_id value=$Dept{id}>
       <input type=hidden name=grade   value=$Input{grade}>
       <input type=hidden name=password value=$Input{password}>
       <input type=submit value="修改及刪除當學期已開科目">
    </FORM>
    <form action=Show_Course_1.cgi method=post>
    <input type=hidden name=dept_cd value=$Dept{id}>
   <input type=hidden name=grade value=$Input{grade}>
   <input type=hidden name=password value=$Input{password}>
   <input type=submit value=查詢當學期已開科目>
   </form>
   <FORM action="Print_Course.cgi" method="POST">
     <INPUT type=hidden name=dept_id value=$Dept{id}>
     <INPUT type=hidden name=grade   value=$Input{grade}>
     <INPUT type=hidden name=password value=$Input{password}>
     <INPUT type=submit value=列印當學期已開科目>
   </FORM>
   <FORM action="Query/Query_1.cgi" method="POST">
     <INPUT type=hidden name=dept_cd value=$Dept{id}>
     <INPUT type=hidden name=grade   value=$Input{grade}>
     <INPUT type=hidden name=password value=$Input{password}>
     <INPUT type=submit value="查詢修課學生名單">
   </FORM>
   <FORM action="Change_Password00.cgi" method="POST">
     <INPUT type=hidden name=password value=$Input{password}>
     <INPUT type=hidden name=id value=$Dept{id}>
     <INPUT type=hidden name=grade value=$Input{grade}>
     <INPUT type=submit value="更改密碼">
   </FORM>
   <FORM action="View_Student_Course1.cgi" method="POST">
     <INPUT type=hidden name=password value=$Input{password}>
     <INPUT type=hidden name=id value=$Dept{id}>
     <INPUT type=hidden name=grade value=$Input{grade}>
     <INPUT type=submit value="檢視學生選課資料">
   </FORM>
   <FORM action="View_Change.cgi" method="POST">
     <INPUT type=hidden name=dept_cd value=$Dept{id}>
     <INPUT type=hidden name=grade   value=$Input{grade}>
     <INPUT type=hidden name=password value=$Input{password}>
     <INPUT type=submit value="課程異動一覽表">
   </FORM>
                             
   <FONT size=-1 color=RED>若開課時有需要設定先修條件, 請勿使用Netscape瀏覽器!</FONT><BR>
    <IMG src="$GRAPH_URL/new1.gif">
    [<a href=$HOME_URL/UserGuide/project.doc>開課系統操作手冊</a>|
    <A href=$HOME_URL/UserGuide/project/faq.html><fontcolor=RED>疑難雜症請看這</font></font>]
    <br><br>
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
      <title> $SUB_SYSTEM_NAME開排課系統功\能選單 $su_flag</title>
     </head>
     <body background=$GRAPH_URL/ccu-sbg.jpg>
     <center>
      <br>
      <table border=0 width=40%>
       <tr>
        <td bgcolor=eeeeee>系別:</td><td bgcolor=eeeeee> $Dept{cname} </td>
        <td bgcolor=eeeeee>年級:</td><td bgcolor=eeeeee> $Input{grade} </td></tr><tr>
        <th colspan=4>$YEAR年度$show_term<FONT color=RED>$SUB_SYSTEM_NAME</FONT>開課系統</th>
       </tr>
      </table>
     <br>
     <hr width=40%>
    <font size=5 color=brown>功\能選單</font>
     <br>
     <hr width=40%><br><br>
);



}