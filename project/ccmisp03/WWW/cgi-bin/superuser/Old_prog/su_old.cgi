#!/usr/local/bin/perl

######### require .pm files #########
require "../library/Reference.pm";
#require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Error_Message.pm";

######### Main Program Here #########
my(%Input);
%Input=User_Input();

#print("Content-type:text/html\n\n");
$crypt_salt = "aa";
$password = Crypt($Input{password},$crypt_salt);
#print("password = $password");
$pass_result = Check_SU_Password($password, "su", "su");
#print("result = $su_result");

HTML_Head("開排選課管理系統");
ERR_HTML()  if( $pass_result eq "FALSE" );
HTML();

######### Main Program End Here #########

######### Start of sub function HTML_Head #########

sub HTML_Head
{
  my($title);
  ($title)=@_;
  print("Content-type:text/html\n\n");
  print qq( 
    <html>
      <head>
      <meta http-equiv="Content-Type" content="text/html; charset=big5">
      <title>$title</title>
      </head>
  );
}         

######### sub function HTML starts here #########

sub HTML
{
  print qq(
    <html>
      <head><title>開排選課管理系統</title></head>
      <body background=$KIKI_URL/bk.jpg>
        <center>
        <table border=0>
          <tr><th><img src=$GRAPH_URL/superuser.jpg></th></tr>
        </table>
        <hr size=2 width=50%>
        <table border=0 height=40%>
<tr>
<th>
<font size=3 color=brown>基本資料維護</font>
<th>
<form method=post action=$CGI_URL/superuser/Teacher_Menu.cgi>
<input type=hidden name=function value=select>
<input type=hidden name=password value=$password>
<input type=submit value=教師基本資料管理>          
</form>
</th>

<th>
<form method=post action=$CGI_URL/superuser/Dept_Menu.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=系所基本資料管理>          
</form>
</th>
</tr>

<tr>
<th>
<font size=3 color=red>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</font>    
<th>
<form method=post action=$CGI_URL/superuser/Classroom_Menu.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=教室基本資料管理>
</form>
</th> 

<th>
<form method=post action=$CGI_URL/superuser/Modify_Course/Login.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=課程資料管理>
</form>
</th>
</tr>  

<tr>
<th>
<font size=3 color=red>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</font>
<th>
<form method=post action=$CGI_URL/superuser/Change_ID_Password.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=學生密碼改學號>
</form>
</th> 
</tr>          

<tr>
<th>
<font size=3 color=purple>時程控管作業</font>    
<th>
<form method=post action=$CGI_URL/superuser/System_State/Open_Course_Control00.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=開課時程設定系統>
</form>
</th>

<th>
<form method=post action=$CGI_URL/superuser/System_State/Select_Class_Control.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=選課時程設定系統>
</form>
</th>
</tr>  


<tr>
<th>&nbsp</th>
<th>&nbsp</th>
<th>
<form method=post action=$CGI_URL/superuser/System_State/Sys_State_Control.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=選課系統狀態設定>
</form>
</th>
</tr>

<tr>
<th>&nbsp</th>
<th>
<form method=post action=$CGI_URL/superuser/System_State/Grade_Update.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=年級升級與否設定>
</form>
</th>
<th>
<form method=post action=$CGI_URL/superuser/System_State/Sys_Limit_Num_Control.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=限修人數控管機制>
</form>
</th>
</tr>


<tr>
<th>
<font size=3 color=green>相關公告維護</font>    
<th>
<form method=post action=$CGI_URL/superuser/Modify_login_Message.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=改選課公告之內容>
</form>
</th>

<th>
<form method=post action=$CGI_URL/superuser/Modify_Select_Course_View00.cgi>
<input type=hidden name=password value=$password>
<input type=submit value=改選課單顯示文字>
</form>
</th>
</tr>

<tr>
<th>
<font size=3 color=red>檔案批次維護</font>    
<th>
<form method=post action=$CGI_URL/superuser/Transfer_Course/Transfer_Course1.cgi>
<input type=hidden name=password value=$password>
<input type=submit value=必修與必選課轉檔>
</form>
</th>

<th>
<form method=post action=$CGI_URL/superuser/Transfer_Course/Batch_Delete_Student_Course1.cgi>
<input type=hidden name=password value=$password>
<input type=submit value=批次進行退選>
</form>
</th>
</tr>


<tr>
<th>
<font size=3 color=red></font>    
<th>
<form method=post action=$CGI_URL/superuser/Clear_open_class.cgi>
<input type=hidden name=function>
<input type=submit value=清除開課記錄[未]>
</form>
</th>

<th>
<form method=post action=$CGI_URL/superuser/Clear_select_class.cgi>
<input type=hidden name=function>
<input type=submit value=清除選課記錄[未]>
</form>
</th>
</tr> 


<tr>
<th>
<font size=3 color=red>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</font>    
<th>
<form method=post action=$CGI_URL/superuser/Dept_Menu.cgi>
<input type=hidden name=function>
<input type=submit value=課程異動作業[未]>
</form>
</th>

<th>
<form method=post action=$CGI_URL/superuser/Clear_select_class.cgi>
<input type=hidden name=function>
<input type=submit value=資料轉資料庫[未]>
</form>
</th>
</tr> 

<tr><td></td>
<th>
<form method=post action=$CGI_URL/superuser/Batch_Add_Student_Course/Batch_Add00.cgi>
<input type=hidden name=function>
<input type=submit value=同班學生批次加選[未]>
</form>
</th>

<th>
<form method=post action=$CGI_URL/superuser/Batch_Add_Student_Course/Course_Batch_Add00.cgi>
<input type=submit value=科目選課作業>
</form>
</th>
</tr>

 
<tr>
<th>
<font size=3 color=blue>資料查詢</font>
<th>
<form method=post action=$CGI_URL/superuser/Query/Login.cgi>
<input type=hidden name=function>
<input type=submit value=查詢修課學生名單>
</form>
</th>

<th>
<form method=post action=$CGI_URL/superuser/Find_Exceed.cgi>
<input type=hidden name=function>
<input type=submit value=查詢超修科目及名單>
</form>
</th>
</tr>

<tr><th>&nbsp</th>
<th>
<form method=post action=$CGI_URL/superuser/Find_All_Course.cgi>
<input type=hidden name=function>
<input type=submit value=查詢所有開課科目>
</form>
</th>

<th>
<form method=post action=$CGI_URL/superuser/Read_Logs/Read_Student_Log01.cgi>
<input type=hidden name=function>
<input type=submit value=查詢學生選課記錄LOG檔>
</form>
</th>
</tr>

</form>
</th>

<tr>
<th>
<form method=GET action="http://kiki.ccu.edu.tw/">
<input type=hidden name=function>
<input type=submit value="回開排課首頁">
</form>
</th>
</tr>

</table>
</center>
</body>
</html>
);

}
##########################################################################
sub ERR_HTML()
{
  print qq(
   <body background=$GRAPH_URL"."ccu-sbg.jpg>
    <center>
    <H1>開排選課管理系統<hr></H1>
    您輸入的密碼有誤, 請重新輸入!<br>
    <FORM>
    <input type=button onclick=history.back() value="回上一頁">
    </FORM>
       
 
  );
  exit(1);
}
