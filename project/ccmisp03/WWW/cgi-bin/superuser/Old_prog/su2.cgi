#!/usr/local/bin/perl
############################################################################
#####  su.cgi
#####  管理功能選單, 提供到各功能的選項供連結
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
      <head><title>$SUB_SYSTEM_NAME開排選課管理系統</title></head>
      <body background="../../Graph/bk.jpg">
        <center>
        <H1>$SUB_SYSTEM_NAME開排選課管理系統</H1>
        <hr size=2 width=50%>
);

TITLE("基本資料維護", "brown");
FORM("  教室基本資料管理  ", "Edit_Classroom/Classroom_Menu.cgi");
FORM("    課程資料管理    ", "Modify_Course/Login.cgi");
FORM("   學生密碼改學號   ", "Change_ID_Password.cgi");
print("</TR><TR>");
FORM("  通識領域資料維護  ", "Support_cge/Support_cge.cgi");
FORM("修改學生選課學分上限", "Modify_Credit_Upper_Limit/Modify_Credit_Upper_Limit01.cgi");
FORM("    新增學生資料    ", "Add_Student/Add_Student1.cgi");
print("</TR><TR>");
FORM("    產生新生密碼    ", "Password/Create_Password1.cgi");
FORM("    額滿加簽名單    ", "Course_Upper_Limit_Immune/Course_Upper_Limit_Immune01.cgi");

TITLE("   時程控管作業    ", "purple");
print("</TR><TR>");
FORM("  開課時程設定系統  ", "System_State/Open_Course_Control00.cgi");
FORM("  選課時程設定系統  ", "System_State/Select_Class_Control.cgi");
FORM("  選課系統狀態設定  ", "System_State/Sys_State_Control.cgi");
print("</TR><TR>");
FORM("  年級升級與否設定  ", "System_State/Grade_Update.cgi");
FORM("  限修人數控管機制  ", "System_State/Sys_Limit_Num_Control.cgi");
print("</TR><TR>");

TITLE("相關公告維護", "green");
FORM("改選課公告之內容", "Login_Message/Modify_login_Message.cgi");
FORM("改選課單顯示文字", "Login_Message/Modify_Select_Course_View00.cgi");
print("</TR><TR>");

TITLE("檔案批次維護", "red");
FORM("必修與必選課轉檔", "Transfer_Course/Transfer_Course1.cgi");
FORM("多對多必修與必選課轉檔", "Transfer_Course/Multi_Transfer_Course1.cgi");
FORM("批次進行退選", "Transfer_Course/Batch_Delete_Student_Course1.cgi");
print("</TR><TR>");
FORM("清除開課記錄[未]", "Clear_open_class.cgi");
FORM("清除選課記錄[未]", "Clear_select_class.cgi");
FORM("課程異動作業[未]", "Dept_Menu.cgi");
print("</TR><TR>");
FORM("資料轉資料庫[未]", "Clear_select_class.cgi");
FORM("同班學生批次加選[未]", "Batch_Add_Student_Course/Batch_Add00.cgi");
FORM("科目選課作業", "Batch_Add_Student_Course/Course_Batch_Add00.cgi");
print("</TR><TR>");

TITLE("資料查詢", "blue");
FORM("查詢修課學生名單", "Query/Login.cgi");
FORM("查詢超修科目及名單", "Find_Exceed.cgi");
FORM("查詢所有開課科目", "Find_All_Course.cgi");
print("</TR><TR>");
FORM("查詢學生選課記錄LOG檔", "Read_Logs/Read_Student_Log01.cgi");
FORM("查詢篩選結果", "SystemChoose/Handle.cgi");
FORM("當學期科目列表", "Course_List/List_Course1.cgi");
print("</TR><TR>");
FORM("未選課學生名單", "Query_No_Selection/Login.cgi");
FORM("支援通識科目一覽表", "Support_cge/Show_all_support_course2.cgi");
FORM("限本系科目一覽表", "Find_All_Dept_Limit.cgi");
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
    <H1>開排選課管理系統<hr></H1>
    您輸入的密碼有誤, 請重新輸入!<br>
    <FORM>
    <input type=button onclick=history.back() value="回上一頁">
    </FORM>
       
 
  );
  exit(1);
}
