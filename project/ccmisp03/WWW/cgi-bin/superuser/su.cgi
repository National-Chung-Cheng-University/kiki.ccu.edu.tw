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
      <head><title>$SUB_SYSTEM_NAME�}�ƿ�Һ޲z�t��</title></head>
      <body background="../../Graph/bk.jpg">
        <center>
        <table border=0>
          <tr><th><H1>$SUB_SYSTEM_NAME�}�ƿ�Һ޲z�t��</H1>
          <!img src=$GRAPH_URL/superuser.jpg></th></tr>
        </table>
        <hr size=2 width=50%>
        <table border=0 height=40%>
<tr>
<th>
<font size=3 color=brown>�򥻸�ƺ��@</font>
<th>
<form method=post action=Edit_Classroom/Classroom_Menu.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=�Ыǰ򥻸�ƺ޲z>
</form>
</th> 

<th>
<form method=post action=Update/Update_Index.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=�t�ΰѦҸ�Ƨ�s>
</form>
</th>
</tr>  

<tr>
<th>
<font size=3 color=red>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</font>
<th>
<form method=post action=Change_ID_Password.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=�ǥͱK�X��Ǹ�>
</form>
</th> 

<th>
<form method=post action=Support_cge/Support_cge.cgi>
<input type=hidden name=password value=$password>
<input type=submit value="�q�ѻ���ƺ��@">
</form>
</th>
</tr>

<tr>
<th>
<font size=3 color=red>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</font>
<th>
<form method=post action=Modify_Credit_Upper_Limit/Modify_Credit_Upper_Limit01.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=�ק�ӧO�ǥͿ�ҾǤ��W��>
</form>
</th>

<th>
<form method=post action=Add_Student/Add_Student1.cgi>
<input type=hidden name=password value=$password>
<input type=submit value="�s�W�ǥ͸��">
</form>
</th>
</tr>

<tr>
<th>
<font size=3 color=red>&nbsp;</font>
<th>
<form method=post action=Password/Create_Password1.cgi>
<input type=hidden name=password value=$password>
<input type=submit value=���ͷs�ͱK�X>
</form>
</th>

<th>
<form method=post action=Course_Upper_Limit_Immune/Course_Upper_Limit_Immune01.cgi>
  <input type=hidden name=password value=$password>
  <input type=submit value="�B���[ñ�W��">
</form>
</th>
</tr>

<tr>
<th>
<font size=3 color=red>&nbsp;</font>
<th>
<form method=post action=Open_Course_Restriction_Immune/Open_Course_Restriction_Immune01.cgi>
<input type=hidden name=password value=$password>
<input type=submit value=�}���ˮְj�ץ[ñ>
</form>
</th>

<th>
<form method=get action=http://140.123.30.31/~ccmisp08/cgi-bin/superuser/Grade/grade_output.now.php>
  <input type=hidden name=password value=$password>
  <input type=submit value="��s�ǥͦ��Z���">
</form>
</th>

</tr>


<tr>
<th>
<font size=3 color=purple>�ɵ{���ާ@�~</font>    
<th>
<form method=post action=System_State/Open_Course_Control00.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=�}�Үɵ{�]�w�t��>
</form>
</th>

<th>
<form method=post action=System_State/Select_Class_Control.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=��Үɵ{�]�w�t��>
</form>
</th>
</tr>  

<tr>
<th>&nbsp</th>
<th>
<form method=post action=System_State/System_Controls.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=��Ҩt�ά����]�w>
</form>
</th>

<th>
<form method=post action=System_State/Sys_State_Control.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=��Ҩt�Ϊ��A�]�w>
</form>
</th>
</tr>

<tr>
<th>&nbsp</th>
<th>
<form method=post action=System_State/Grade_Update.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=�~�ŤɯŻP�_�]�w>
</form>
</th>
<th>
<form method=post action=System_State/Sys_Limit_Num_Control.cgi>
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
<form method=post action=Login_Message/Modify_login_Message.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit value=���Ҥ��i�����e>
</form>
</th>

<th>
<form method=post action=Login_Message/Modify_Select_Course_View00.cgi>
<input type=hidden name=password value=$password>
<input type=submit value=���ҳ���ܤ�r>
</form>
</th>
</tr>

<tr>
<th>
<font size=3 color=red>�ɮק妸���@</font>    
<th>
<form method=post action=Transfer_Course/Transfer_Course1.cgi>
<input type=hidden name=password value=$password>
<input type=submit value=���׻P���������>
</form>
</th>

<th>
<form method=post action=Transfer_Course/Multi_Transfer_Course1.cgi>
<input type=submit value=�h��h���׻P���������>
</form>
</th>
</tr>


<TR>
<TH>&nbsp;</TH>
<th>
<form method=post action=Transfer_Course/Batch_Delete_Student_Course1.cgi>
<input type=hidden name=password value=$password>
<input type=submit value=�妸�i��h��>
</form>
</th>


</tr>

<tr>
<th>
<font size=3 color=red></font>    
<th>
<form method=post action=Clear_open_class.cgi>
<input type=hidden name=function>
<input type=submit value=�M���}�ҰO��[��]>
</form>
</th>

<th>
<form method=post action=Clear_select_class.cgi>
<input type=hidden name=function>
<input type=submit value=�M����ҰO��[��]>
</form>
</th>
</tr> 


<tr>
<th>
<font size=3 color=red>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</font>    
<th>
<form method=post action=Dept_Menu.cgi>
<input type=hidden name=function>
<input type=submit value=�ҵ{���ʧ@�~[��]>
</form>
</th>

<th>
<form method=post action=Clear_select_class.cgi>
<input type=hidden name=function>
<input type=submit value=������Ʈw[��]>
</form>
</th>
</tr> 

<tr><td></td>
<th>
<form method=post action=Batch_Add_Student_Course/Batch_Add00.cgi>
<input type=hidden name=function>
<input type=submit value=�W�U�Ǵ���Z�妸�[��(�L�n��)>
</form>
</th>

<th>
<form method=post action=Batch_Add_Student_Course/Course_Batch_Add00.cgi>
<input type=submit value=��ؿ�ҧ@�~>
</form>
</th>
</tr>

 
<tr>
<th>
<font size=3 color=blue>��Ƭd��</font>
<th>
<form method=post action=Query/Login.cgi>
<input type=hidden name=function>
<input type=submit value=�d�߭׽ҾǥͦW��>
</form>
</th>

<th>
<form method=post action=Find_Exceed.cgi>
<input type=hidden name=function>
<input type=submit value=�d�߶W�׬�ؤΦW��>
</form>
</th>
</tr>

<tr><th>&nbsp</th>
<th>
<form method=post action=Find_All_Course.cgi>
<input type=hidden name=function>
<input type=submit value=�d�ߩҦ��}�Ҭ��>
</form>
</th>

<th>
<form method=post action=Find_All_Course2.cgi> 
<input type=hidden name=function>   
<input type=submit value=��Ǵ��}�ҩ��Ӫ�>
</form>
</th>
</tr>

<tr><th>&nbsp</th>
<th>
<form method=post action=Ban_List/Ban_List.cgi>
<input type=hidden name=function> 
<input type=hidden name=password value=$password>
<input type=submit value=���v�W��>
</form>
</th>

<th>
<form method=post action=Read_Logs/Read_Student_Log01.cgi>
<input type=hidden name=function>
<input type=submit value=�d�߾ǥͿ�ҰO��LOG��>
</form>
</th>
</tr>

<tr><th>&nbsp</th>
<th>
<form method=post action=SystemChoose/Handle.cgi>
<input type=hidden name=function>
<input type=submit value=�d�߿z�ﵲ�G>
</form>
</th>


<th>
<form method=post action=Course_List/List_Course1.cgi>
<input type=hidden name=function>
<input type=submit value=��Ǵ���ئC��>
</form>
</th>
</tr>

<tr><th>&nbsp</th>
<th>
<form method=post action=Query_No_Selection/Login.cgi>
<input type=hidden name=function>
<input type=submit value=����ҾǥͦW��>
</form>
</th>

<th>
<form method=post action=Support_cge/Show_all_support_course2.cgi>
<input type=hidden name=function>
<input type=submit value=�䴩�q�Ѭ�ؤ@����>
</form>
</th>
</tr>


<tr><th>&nbsp</th>
<th>
<form method=post action=Find_All_Dept_Limit.cgi>
<input type=hidden name=function>
<input type=submit value=�����t��ؤ@����>
</form>
</th>

<th>
<form method=post action=Statistics.cgi>
<input type=hidden name=function>
<input type=submit value=�t�Ϊ��A>
</form>
</th>
</tr>

<tr><th>&nbsp</th>
<th>
<form method=post action=Query/Student_Course_list.cgi>
<input type=hidden name=function>
<input type=submit value=�H�Ǹ��ƧǪ���Ҹ�ƦC��>
</form>
</th>




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
