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

HTML_Head("�}�ƿ�Һ޲z�t��");
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
      <head><title>�}�ƿ�Һ޲z�t��</title></head>
      <body background=$KIKI_URL/bk.jpg>
        <center>
        <table border=0>
          <tr><th><img src=$GRAPH_URL/superuser.jpg></th></tr>
        </table>
        <hr size=2 width=50%>
        <table border=0 height=40%>
<tr>
<th>
<font size=3 color=brown>�򥻸�ƺ��@</font>
<th>
<form method=post action=$CGI_URL/superuser/Teacher_Menu.cgi>
<input type=hidden name=function value=select>
<input type=hidden name=password value=$password>
<input type=submit value=�Юv�򥻸�ƺ޲z>          
</form>
</th>

<th>
<form method=post action=$CGI_URL/superuser/Dept_Menu.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=�t�Ұ򥻸�ƺ޲z>          
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
<input type=submit value=�Ыǰ򥻸�ƺ޲z>
</form>
</th> 

<th>
<form method=post action=$CGI_URL/superuser/Modify_Course/Login.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=�ҵ{��ƺ޲z>
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
<input type=submit value=�ǥͱK�X��Ǹ�>
</form>
</th> 
</tr>          

<tr>
<th>
<font size=3 color=purple>�ɵ{���ާ@�~</font>    
<th>
<form method=post action=$CGI_URL/superuser/System_State/Open_Course_Control00.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=�}�Үɵ{�]�w�t��>
</form>
</th>

<th>
<form method=post action=$CGI_URL/superuser/System_State/Select_Class_Control.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=��Үɵ{�]�w�t��>
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
<input type=submit value=��Ҩt�Ϊ��A�]�w>
</form>
</th>
</tr>

<tr>
<th>&nbsp</th>
<th>
<form method=post action=$CGI_URL/superuser/System_State/Grade_Update.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=�~�ŤɯŻP�_�]�w>
</form>
</th>
<th>
<form method=post action=$CGI_URL/superuser/System_State/Sys_Limit_Num_Control.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=���פH�Ʊ��޾���>
</form>
</th>
</tr>


<tr>
<th>
<font size=3 color=green>�������i���@</font>    
<th>
<form method=post action=$CGI_URL/superuser/Modify_login_Message.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=���Ҥ��i�����e>
</form>
</th>

<th>
<form method=post action=$CGI_URL/superuser/Modify_Select_Course_View00.cgi>
<input type=hidden name=password value=$password>
<input type=submit value=���ҳ���ܤ�r>
</form>
</th>
</tr>

<tr>
<th>
<font size=3 color=red>�ɮק妸���@</font>    
<th>
<form method=post action=$CGI_URL/superuser/Transfer_Course/Transfer_Course1.cgi>
<input type=hidden name=password value=$password>
<input type=submit value=���׻P���������>
</form>
</th>

<th>
<form method=post action=$CGI_URL/superuser/Transfer_Course/Batch_Delete_Student_Course1.cgi>
<input type=hidden name=password value=$password>
<input type=submit value=�妸�i��h��>
</form>
</th>
</tr>


<tr>
<th>
<font size=3 color=red></font>    
<th>
<form method=post action=$CGI_URL/superuser/Clear_open_class.cgi>
<input type=hidden name=function>
<input type=submit value=�M���}�ҰO��[��]>
</form>
</th>

<th>
<form method=post action=$CGI_URL/superuser/Clear_select_class.cgi>
<input type=hidden name=function>
<input type=submit value=�M����ҰO��[��]>
</form>
</th>
</tr> 


<tr>
<th>
<font size=3 color=red>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</font>    
<th>
<form method=post action=$CGI_URL/superuser/Dept_Menu.cgi>
<input type=hidden name=function>
<input type=submit value=�ҵ{���ʧ@�~[��]>
</form>
</th>

<th>
<form method=post action=$CGI_URL/superuser/Clear_select_class.cgi>
<input type=hidden name=function>
<input type=submit value=������Ʈw[��]>
</form>
</th>
</tr> 

<tr><td></td>
<th>
<form method=post action=$CGI_URL/superuser/Batch_Add_Student_Course/Batch_Add00.cgi>
<input type=hidden name=function>
<input type=submit value=�P�Z�ǥͧ妸�[��[��]>
</form>
</th>

<th>
<form method=post action=$CGI_URL/superuser/Batch_Add_Student_Course/Course_Batch_Add00.cgi>
<input type=submit value=��ؿ�ҧ@�~>
</form>
</th>
</tr>

 
<tr>
<th>
<font size=3 color=blue>��Ƭd��</font>
<th>
<form method=post action=$CGI_URL/superuser/Query/Login.cgi>
<input type=hidden name=function>
<input type=submit value=�d�߭׽ҾǥͦW��>
</form>
</th>

<th>
<form method=post action=$CGI_URL/superuser/Find_Exceed.cgi>
<input type=hidden name=function>
<input type=submit value=�d�߶W�׬�ؤΦW��>
</form>
</th>
</tr>

<tr><th>&nbsp</th>
<th>
<form method=post action=$CGI_URL/superuser/Find_All_Course.cgi>
<input type=hidden name=function>
<input type=submit value=�d�ߩҦ��}�Ҭ��>
</form>
</th>

<th>
<form method=post action=$CGI_URL/superuser/Read_Logs/Read_Student_Log01.cgi>
<input type=hidden name=function>
<input type=submit value=�d�߾ǥͿ�ҰO��LOG��>
</form>
</th>
</tr>

</form>
</th>

<tr>
<th>
<form method=GET action="http://kiki.ccu.edu.tw/">
<input type=hidden name=function>
<input type=submit value="�^�}�ƽҭ���">
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
    <H1>�}�ƿ�Һ޲z�t��<hr></H1>
    �z��J���K�X���~, �Э��s��J!<br>
    <FORM>
    <input type=button onclick=history.back() value="�^�W�@��">
    </FORM>
       
 
  );
  exit(1);
}
