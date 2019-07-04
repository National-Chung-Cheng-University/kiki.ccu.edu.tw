#!/usr/local/bin/perl
############################################################################
#####  su.cgi
#####  �޲z�\����, ���Ѩ�U�\�઺�ﶵ�ѳs��
#####  Coder: ???
#####  Update:2001/09/12, Nidalap :D~
############################################################################
require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Error_Message.pm";
########################## Main Program Here ###############################
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
        <H1>$SUB_SYSTEM_NAME�}�ƿ�Һ޲z�t��</H1>
        <hr size=2 width=50%>
);

TITLE("�򥻸�ƺ��@", "brown");
FORM("  �Ыǰ򥻸�ƺ޲z  ", "Edit_Classroom/Classroom_Menu.cgi");
FORM("    �ҵ{��ƺ޲z    ", "Modify_Course/Login.cgi");
FORM("   �ǥͱK�X��Ǹ�   ", "Change_ID_Password.cgi");
print("</TR><TR>");
FORM("  �q�ѻ���ƺ��@  ", "Support_cge/Support_cge.cgi");
FORM("�ק�ǥͿ�ҾǤ��W��", "Modify_Credit_Upper_Limit/Modify_Credit_Upper_Limit01.cgi");
FORM("    �s�W�ǥ͸��    ", "Add_Student/Add_Student1.cgi");
print("</TR><TR>");
FORM("    ���ͷs�ͱK�X    ", "Password/Create_Password1.cgi");
FORM("    �B���[ñ�W��    ", "Course_Upper_Limit_Immune/Course_Upper_Limit_Immune01.cgi");

TITLE("   �ɵ{���ާ@�~    ", "purple");
print("</TR><TR>");
FORM("  �}�Үɵ{�]�w�t��  ", "System_State/Open_Course_Control00.cgi");
FORM("  ��Үɵ{�]�w�t��  ", "System_State/Select_Class_Control.cgi");
FORM("  ��Ҩt�Ϊ��A�]�w  ", "System_State/Sys_State_Control.cgi");
print("</TR><TR>");
FORM("  �~�ŤɯŻP�_�]�w  ", "System_State/Grade_Update.cgi");
FORM("  ���פH�Ʊ��޾���  ", "System_State/Sys_Limit_Num_Control.cgi");
print("</TR><TR>");

TITLE("�������i���@", "green");
FORM("���Ҥ��i�����e", "Login_Message/Modify_login_Message.cgi");
FORM("���ҳ���ܤ�r", "Login_Message/Modify_Select_Course_View00.cgi");
print("</TR><TR>");

TITLE("�ɮק妸���@", "red");
FORM("���׻P���������", "Transfer_Course/Transfer_Course1.cgi");
FORM("�h��h���׻P���������", "Transfer_Course/Multi_Transfer_Course1.cgi");
FORM("�妸�i��h��", "Transfer_Course/Batch_Delete_Student_Course1.cgi");
print("</TR><TR>");
FORM("�M���}�ҰO��[��]", "Clear_open_class.cgi");
FORM("�M����ҰO��[��]", "Clear_select_class.cgi");
FORM("�ҵ{���ʧ@�~[��]", "Dept_Menu.cgi");
print("</TR><TR>");
FORM("������Ʈw[��]", "Clear_select_class.cgi");
FORM("�P�Z�ǥͧ妸�[��[��]", "Batch_Add_Student_Course/Batch_Add00.cgi");
FORM("��ؿ�ҧ@�~", "Batch_Add_Student_Course/Course_Batch_Add00.cgi");
print("</TR><TR>");

TITLE("��Ƭd��", "blue");
FORM("�d�߭׽ҾǥͦW��", "Query/Login.cgi");
FORM("�d�߶W�׬�ؤΦW��", "Find_Exceed.cgi");
FORM("�d�ߩҦ��}�Ҭ��", "Find_All_Course.cgi");
print("</TR><TR>");
FORM("�d�߾ǥͿ�ҰO��LOG��", "Read_Logs/Read_Student_Log01.cgi");
FORM("�d�߿z�ﵲ�G", "SystemChoose/Handle.cgi");
FORM("��Ǵ���ئC��", "Course_List/List_Course1.cgi");
print("</TR><TR>");
FORM("����ҾǥͦW��", "Query_No_Selection/Login.cgi");
FORM("�䴩�q�Ѭ�ؤ@����", "Support_cge/Show_all_support_course2.cgi");
FORM("�����t��ؤ@����", "Find_All_Dept_Limit.cgi");
print("</TR><TR>");

print qq(
  </TABLE>
</center>
</body>
</html>
);

}
##########################################################################
sub TITLE()
{
  my($title, $color) = @_;
  print qq(
          </TR>
        </TABLE><P>
        <TABLE border=0>
          <TR>
            <TH bgcolor=YELLOW align=CENTER colspan=4>
              <font size=3 color=$color>$title</font>
            </TH>
          </TR>
  );
}
##########################################################################
sub FORM()
{
  my($title, $url) = @_;
  print qq(
    <TD align=CENTER>
      <FORM method=POST action=$url>
        <INPUT type=hidden name=password value=$password>
        <INPUT type=submit value="$title">
      </FORM>
    </TD>
  )
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
