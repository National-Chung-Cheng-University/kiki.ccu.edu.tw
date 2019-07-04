#!/usr/local/bin/perl

############################################################################################################
#####  su.cgi
#####  管理者主選單
#####  Updates:
#####   199?/??/?? Created by ???
#####   2010/03/02 新增字體選擇功能 Nidalap :D~

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Error_Message.pm";

my(%Input);
%Input=User_Input();

if( $Input{"do_not_crypt"} ) {
  $password = $Input{"password"};
}else{
  $crypt_salt = "aa";
  $password = Crypt($Input{password},$crypt_salt);
}
#print("password = $password");
$pass_result = Check_SU_Password($password, "su", "su");
#print("result = $su_result");
$title = "開排選課管理系統" ;
if($SUB_SYSTEM_NAME[$SUB_SYSTEM]) {
  $title = $title . " - <FONT color=RED>$SUB_SYSTEM_NAME[$SUB_SYSTEM]</FONT>";
}
HTML_Head($title);
ERR_HTML()  if( $pass_result eq "FALSE" );
HTML();


######### Start of sub function HTML_Head #########

sub HTML_Head
{
  my($title);
  ($title)=@_;
  print("Content-type:text/html\n\n");
  print qq( 
    <html>
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <LINK href="$HOME_URL/style.css" rel="stylesheet" type="text/css" media="screen" />
        <script type="text/javascript" src="$HOME_URL/javascript/jquery.js"></script>
        <title>$title</title>
      </head>
  );
}         

######### sub function HTML starts here #########

sub HTML
{
  print qq'
    <html>
      <head>
	    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<title>$title</title>
	  </head>
      <body background="$GRAPH_URL/manager.jpg">
        <center>
        <table border=0>
          <tr><th><H1>$title</H1>
          <!img src=$GRAPH_URL/superuser.jpg></th></tr>
        </table>
        <hr size=2 width=50%>
        <table border=0 height=40%>
<tr>
<th>
<font color=brown>基本資料維護</font>
<th>
<form method=post action=Edit_Classroom/Classroom_Menu.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input class=medium type=submit value=教室基本資料管理>
</form>
</th> 

<th>
<form method=post action=Update/Update_Index.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit class=medium value=系統參考資料更新>
</form>
</th>
</tr>  

<tr>
<th>
<font color=red>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</font>
<th>
<form method=post action=Change_ID_Password.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit class=medium value=學生密碼改學號>
</form>
</th> 

<th>
<form method=post action=Support_cge/Support_cge.cgi>
<input type=hidden name=password value=$password>
<input type=submit class=medium value="通識領域資料維護">
</form>
</th>
</tr>

<tr>
<th>
<font color=red>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</font>
<th>
<form method=post action=Modify_Credit_Upper_Limit/Modify_Credit_Upper_Limit01.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit class=medium value=修改個別學生選課學分上限>
</form>
</th>

<th>
<!--
<form method=post action=Add_Student/Add_Student1.cgi>
<input type=hidden name=password value=$password>
<input type=submit class=medium value="新增學生資料">
</form>
-->
</th>
</tr>

<tr>
<th>
<font color=red>&nbsp;</font>
<th>
<form method=post action=Password/Create_Password1.cgi>
<input type=hidden name=password value=$password>
<input type=submit class=medium value=產生新生密碼>
</form>
</th>

<th>
<!form method=post action=Concent_Form_Approval.php>
  <!input type=hidden name=password value=$password>
  <!input type=submit class=medium value="加簽單審核">
<!/form>
&nbsp;
</th>
</tr>


<tr>
<th>
<font color=red>&nbsp;</font>
<th>
<form method=post action=Concent_Form_Approval.php>
  <input type=hidden name=password value=$password>
  <input type=submit class=medium value="加簽單審核">
</form>
</th>

<th>
<form method=post action=Withdrawal_Form_Approval.php>
  <input type=hidden name=password value=$password>
  <input type=submit class=medium value="棄選單審核">
</form>
</th>
</tr>

<tr>
<th>
<font color=red>&nbsp;</font>
<th>
<form method=post action=Open_Course_Restriction_Immune/Open_Course_Restriction_Immune01.cgi>
<input type=hidden name=password value=$password>
<input type=submit class=medium value=開課檢核迴避加簽>
</form>
</th>

<th>
<form method=post action=My_Program_Approval.php>
  <input type=hidden name=password value=$password>
  <input type=submit class=medium value="客製化學程審核">
</form>
</th>
</tr>

<th>
<!--form method=get action=http://140.123.30.31/~ccmisp08/cgi-bin/superuser/Grade/grade_output.now.php>
  <input type=hidden name=password value=$password>
  <input type=submit class=medium value="更新學生成績資料">
</form> -->
</th>
</tr>

<tr>
<th>
<font color=red>&nbsp;</font>
<th>
<form method=post action=Create_Pages/index.cgi>
<input type=hidden name=password value=$password>
<input type=submit class=medium value=產生靜態開課網頁>
</form>
</th>

<th>
&nbsp;
</th>




<tr>
<th>
<font color=purple>時程控管作業</font>    
<th>
<form method=post action=System_State/Open_Course_Control00.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit class=medium value=開課時程設定系統>
</form>
</th>

<th>
<form method=post action=System_State/Select_Class_Control.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit class=medium value=選課時程設定系統>
</form>
</th>
</tr>  

<tr>
<th>&nbsp</th>
<th>
<form method=post action=System_State/System_Controls.php>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit class=medium value=選課系統相關設定>
</form>
</th>

<th>
<form method=post action=System_State/Sys_State_Control.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit class=medium value=選課系統狀態設定>
</form>
</th>
</tr>

<tr>
<th>&nbsp</th>
<th>
<form method=post action=System_State/Sys_Limit_Num_Control.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit class=medium value=限修人數控管機制>
</form>
</th>
</tr>


<tr>
<th>
<font  color=green>相關公告維護</font>    
<th>
<form method=post action=Login_Message/Modify_login_Message.cgi>
<input type=hidden name=function>
<input type=hidden name=password value=$password>
<input type=submit class=medium value=改選課公告之內容>
</form>
</th>

<th>
<form method=post action=Login_Message/Modify_Select_Course_View00.cgi>
<input type=hidden name=password value=$password>
<input type=submit class=medium value=改選課單顯示文字>
</form>
</th>
</tr>

<tr>
<th>
<font color=red>檔案批次維護</font>    
<th>
<form method=post action=Transfer_Course/Transfer_Course1.cgi>
<input type=hidden name=password value=$password>
<input type=submit class=medium value=必修與必選課轉檔>
</form>
</th>

<th>
<form method=post action=Transfer_Course/Multi_Transfer_Course1.cgi>
<input type=submit class=medium value=多對多必修與必選課轉檔>
</form>
</th>
</tr>


<TR>
<TH>&nbsp;</TH>
<th>
<form method=post action=Transfer_Course/Batch_Delete_Student_Course1.cgi>
<input type=hidden name=password value=$password>
<input type=submit class=medium value=批次進行退選>
</form>
</th>

<th>
<form method=post action="Batch_Add_Student_Course/Batch_Add_English_Course01.cgi">
<input type=hidden name=password value=$password>
<input type=submit class=medium value="新生通識英語課程批次載入">
</form>
</th>


</tr>

<tr>
<!--
<th>
<font color=red></font>    
<th>
<form method=post action=Clear_open_class.cgi>
<input type=hidden name=function>
<input type=submit class=medium value=清除開課記錄[未]>
</form>
-->
</th>

<th>
<!--
<form method=post action=Clear_select_class.cgi>
<input type=hidden name=function>
<input type=submit class=medium value=清除選課記錄[未]>
</form>
-->
</th>
</tr> 


<tr>
<th>
<!--
<font color=red>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</font>    
<th>
<form method=post action=Dept_Menu.cgi>
<input type=hidden name=function>
<input type=submit class=medium value=課程異動作業[未]>
</form>
-->
</th>

<th>
<!--
<form method=post action=Clear_select_class.cgi>
<input type=hidden name=function>
<input type=submit class=medium value=資料轉資料庫[未]>
</form>
-->
</th>
</tr> 

<tr><td></td>
<th>
<form method=post action=Batch_Add_Student_Course/Batch_Add00.cgi>
<input type=hidden name=function>
<input type=submit class=medium value=上下學期原班批次加選(微積分)>
</form>
</th>

<th>
<form method=post action=Batch_Add_Student_Course/Course_Batch_Add00.cgi>
<input type=submit class=medium value=科目選課作業>
</form>
</th>
</tr>

<tr><td></td>
<th>
<form method=post action=Batch_Add_Student_Course/Batch_Transfer00.cgi>
<input type=hidden name=function>
<input type=submit class=medium value="原班學生批次加選至另一班">
</form>
</th>

<th>
&nbsp;
</th>
</tr>

 
<tr>
<th>
<font color=blue>資料查詢</font>
<th>
<form method=post action=Query/Login.cgi>
<input type=hidden name=function>
<input type=submit class=medium value=查詢修課學生名單>
</form>
</th>

<th>
<form method=post action=Find_Exceed.cgi>
<input type=hidden name=function>
<input type=submit class=medium value=查詢超修科目及名單>
</form>
</th>
</tr>

<tr><th>&nbsp</th>
<th>
<form method=post action=Find_All_Course01.cgi>
<input type=hidden name=function>
<input type=submit class=medium value=當學期開課明細表>
</form>
</th>

<th>
<form method=post action=Check_Time_Collision.cgi>
<input type=hidden name=function>
<input type=submit class=medium value=所有選課衝堂的學生>
</form>
</th>
</tr>

<tr><th>&nbsp</th>
<th>
<form method=post action=Course_Collision.cgi>
<input type=hidden name=function>
<input type=submit class=medium value=教師與教室衝堂檢核>
</form>
</th>

<th>
<!form method=post action=Check_Time_Collision.cgi>
<!input type=hidden name=function>
<!input type=submit class=medium value=所有選課衝堂的學生>
<!/form>
</th>
</tr>

<tr><th>&nbsp</th>
<th>
<form method=post action=Ban_List/Ban_List.cgi>
<input type=hidden name=function> 
<input type=hidden name=password value=$password>
<input type=submit class=medium value=停權名單>
</form>
</th>

<th>
<form method=post action=Read_Logs/Read_Student_Log01.cgi>
<input type=hidden name=function>
<input type=submit class=medium value=查詢學生選課記錄LOG檔>
</form>
</th>
</tr>

<tr><th>&nbsp</th>
<th>
<form method=post action=SystemChoose/Handle.cgi>
<input type=hidden name=function>
<input type=submit class=medium value=查詢篩選結果>
</form>
</th>


<th>
<form method=post action=Course_List/List_Course1.cgi>
<input type=hidden name=function>
<input type=submit class=medium value=當學期科目列表>
</form>
</th>
</tr>

<tr><th>&nbsp</th>
<th>
<form method=post action=Query_No_Selection/Login.cgi>
<input type=hidden name=function>
<input type=submit class=medium value=未選課學生名單>
</form>
</th>

<th>
<form method=post action=Support_cge/Show_all_support_course2.cgi>
<input type=hidden name=function>
<input type=submit class=medium value=支援通識科目一覽表>
</form>
</th>
</tr>


<tr><th>&nbsp</th>
<th>
<form method=post action=Find_All_Dept_Limit.cgi>
<input type=hidden name=function>
<input type=submit class=medium value=限本系科目一覽表>
</form>
</th>

<th>
<form method=post action=System_State/System_State.cgi>
<input type=hidden name=function>
<input type=submit class=medium value=系統狀態>
</form>
</th>
</tr>

<tr><th>&nbsp</th>
<th>
<form method=post action=Query/Student_Course_list01.cgi>
<input type=hidden name=function>
<input type=submit class=medium value=所有選課資料列表>
</form>
</th>

<th>
<form method=post action=Query/Find_Over_CGE_Student1.cgi>
<input type=hidden name=function>
<input type=submit class=medium value=選修太多通識的學生>
</form>
</th>
</tr>

<tr><th>&nbsp</th>
<th>
<form method=post action=Questionnaire2013stat.php>
<input type=hidden name=password value=$password>
<input type=submit class=medium value=2013選課改制意見調查統計>
</form>
</th>

<th>
<form method=post action=Dept_Open_Course_List.php>
<input type=hidden name=password value=$password>
<input type=submit class=medium value=各系開課狀態一覽表>
</form>
</th>
</tr>
</th>

<tr><th>&nbsp</th>
<th>
<form method=post action=Statistics/Student_Log_Stat01.php>
<input type=hidden name=password value=$password>
<input type=submit class=medium value="學生LOG紀錄檔分析 - 使用版本分析">
</form>
</th>

<th>
<form method=post action="Statistics/SystemChoose_Analyze01.php">
<input type=hidden name=password value=$password>
<input type=submit class=medium value="課程需求分析（依限修篩選紀錄）">
</form>
</th>
</tr>
</th>


<tr>
<th>
<form method=GET action="http://kiki.ccu.edu.tw/">
<input type=hidden name=function>
<input type=submit class=medium value="回開排課首頁">
</form>
</th>
</tr>

</table>
</center>
</body>
</html>
';

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
