#!/usr/local/bin/perl

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Password.pm";
#require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Select_Course.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."System_Settings.pm";
require $LIBRARY_PATH."Session.pm";
#require $LIBRARY_PATH."MD5/MD5.pm";
#require $LIBRARY_PATH."Error_Message.pm";

#use Digest::MD5 qw(md5 md5_hex md5_base64);
use Digest::MD5 qw(md5 md5_hex md5_base64);

my(%Input,%Student,%Dept);
%time = gettime();

###########################################################################
#####  這一段使用 CGI.pm, 但是會跟原來的 User_Input() 搶 STDIN,
#####  所以製造一個 $fake_query_string 丟給 User_Input() 以讓兩者並存
#####  Code added on 2005/02/15, Nidalap :D~
use CGI qw(:standard);
$query = new CGI;

if(param('crypt') eq "0") {     ###  只有第一次 Login, 會對密碼做加密, 以及設定 cookie
  $crypt_salt = Read_Crypt_Salt(param('id'), "student");
  $temp_crypt_password = Crypt(param('password'), $crypt_salt);
  param(-name=>'password', -values=>$temp_crypt_password);
  $query->delete('crypt');
  $session_id = Create_Session_ID(param('id'), param('password'));
#  $session_id = Crypt($time{time_string}) . Crypt(param('id'))
#                . Crypt(param('password')) ;  ### 產生 session_id
  $cookie0 = $query->cookie(-name => 'session_id', -value=>$session_id, -expires=>'+30min');
  $cookie1 = $query->cookie(-name => 'id', -value=>param('id'), -expires=>'+30min');
  $cookie2 = $query->cookie(-name => 'password', -value=>param('password'), -expires=>'+30min');
  print $query->header(-cookie=>[$cookie0, $cookie1, $cookie2]);

  @names = $query->param;         ###  產生 fake_query_string 用來騙 User_Input()
  foreach $name (@names) {
    if( $fake_query_string eq "") { 
      $fake_query_string = $name . "=" . param($name);
    }else{
      $fake_query_string .= "&" . $name . "=" . param($name);
    }
  }

#  $cookie1 = $query->cookie(-name => 'id', -value=>param('id'), -expires=>'+1h');
#  $cookie2 = $query->cookie(-name => 'password', -value=>param('password'), -expires=>'+1h'); 
#  print $query->header(-cookie=>[$cookie1, $cookie2]);

#  print("fake_query_string = $fake_query_string<BR>\n");
#  print("temp_crypt_password = $temp_crypt_password<BR>\n");
#  @names = $query->param;
#  foreach $name (@names) {
#    $temp = param($name);
#    print("$name -> $temp<BR>\n");
#  }
#  foreach $name ($query->cookie()) {
#    $temp = $query->cookie($name);
#    print("in cookie: [$name, $temp]<BR>\n");
#  }
#  print("id = ", param('id'), "<BR>\n");

  %Input = User_Input($fake_query_string);
  $Input{session_id} = $session_id;
#  print("session_id = $session_id<BR>\n");
  Write_Session($session_id, $Input{id}, $Input{password}, 0);
#  print("[session_id, Input{id}, Input{password}] = [$session_id, $Input{id}, $Input{password}]<BR>\n");

}else{         ### 若不是第一次登錄, 則從 server-side session 取得參數
               ### 由於資料相衝問題尚未解決, 暫時仍由 form 傳 hidden value
#  $Input{id}       = $query->cookie('id');
#  $Input{password} = $query->cookie('password');
#  $session_id      = $query->cookie('session_id');
  print header;
#  print("*session_id = $session_id<BR>\n");
  @names = $query->param;         ###  產生 fake_query_string 用來騙 User_Input()
  foreach $name (@names) {
    if( $fake_query_string eq "") {
      $fake_query_string = $name . "=" . param($name);
    }else{
      $fake_query_string .= "&" . $name . "=" . param($name);
    }
  }
      
  %Input = User_Input($fake_query_string);
  $session_id = $Input{session_id};
#  if($Input{session_id}) {
     ($Input{id}, $Input{password}, $login_time, $ip_in_session, $add_course_count) = Read_Session($Input{session_id});
#     print("[session_id, Input{id}, Input{password}] = [$Input{session_id}, $Input{id}, $Input{password}]<BR>\n");
#      print("[ip, login_time, add_course_count] = [$ip_in_session, $login_time, $add_course_count]<BR>\n");

#     if($ip_in_session ne $ENV{HTTP_X_FORWARDED_FOR}) {
#       print("Fatal error!?");
#     }
#  }
}

#%Input=User_Input();
###########################################################################

#print header;
#print("Content-type:text/html\n\n");

%Student=Read_Student($Input{id});
%Dept=Read_Dept($Student{dept});
%system_settings = Read_System_Settings();

#$key = Generate_Key($Input{id});
  
#use CGI qw(:standard);
#$query = new CGI; 


#if(not defined $Input{Flag}){
if( $Input{crypt} eq "0" ) {
  $use_default_password_flag = Check_For_Unencoded_Password();
#  print("password is now $Input{password}<BR>\n");
#  $query->param('password', $Input{password});
  $query->param(-name=>'password', -value=>$Input{password});
  $Input{Flag} = 0  if($Input{view_warning} ne "on");      ### "我要先看篩選及異動訊息" 是否勾選
}else{
  Check_Student_Password($Input{id}, $Input{password});
}

my($HEAD_DATA)=Head_of_Individual($Student{name},$Student{id},$Dept{cname},$Student{grade},$Student{class});

if($SUPERUSER != 1){     ## 非 superuser 的使用者
  ##  warning message 不存在
#  print(" flag = $use_default_password_flag<BR>\n");
  if( $use_default_password_flag eq "DEFAULT_PASSWORD" ) {
    Enter_Menu_Change_Password($HEAD_DATA, $Student{id},$Input{password}, $use_default_password_flag);
  }elsif( $use_default_password_flag eq "DEFAULT_PASSWORD2" ) {
    Enter_Menu_Change_Password($HEAD_DATA, $Student{id},$Input{password}, $use_default_password_flag);
  }elsif( Need_To_Change_Password($Student{id}, $Input{password}) ) {
    Enter_Menu_Change_Password($HEAD_DATA, $Student{id},$Input{password}, $use_default_password_flag);
  }
  ##  Check the System Status !!  Added by hanchu @ 1999/9/10
  if(Whats_Sys_State() == 0){
    Enter_Menu_Sys_State_Forbidden($HEAD_DATA);
  }elsif(Whats_Sys_State() == 2){
    if(Check_Time_Map(%Student)==1){
      MenuHTML($HEAD_DATA,$Student{id},$Input{password});
    }else{
      MenuHTML_2($HEAD_DATA,$Student{id},$Input{password});
    }
  }elsif(Whats_Sys_State() == 1){
    MenuHTML_2($HEAD_DATA,$Student{id},$Input{password});
  }else{
    Enter_Menu_Error($HEAD_DATA);
  }
}else{                   ## superuser 的使用者
  MenuHTML($HEAD_DATA,$Student{id},$Input{password});
}
###########################################################################
#####  Form_System_Choose_Data_Table()
#####  產生並傳回篩選結果的 HTML Table 碼
###########################################################################
sub Form_System_Choose_Data_Table()
{
  my($FILENAME)=$DATA_PATH."Student_warning/".$Student{id}."_warning";
  my($Table_Data, @WARN);
  if(-e $FILENAME){
    open(FILE,"<$FILENAME");
    @WARN=<FILE>;
    close(FILE);
    $Table_Data .= "您選修的科目經過系統篩選結果如下(若篩選結果未選中,則此科目已經由系統幫您退選)<br>";
    $Table_Data .= "<FONT color=RED>選課資料以選課清單為主, 請至主選單中\"檢視已選修科目\"確認選課結果</FONT>";
    $Table_Data .= "<table border=1 width=90%><tr>";
    $Table_Data .= " <th bgcolor=yellow>開課系所</th><th bgcolor=yellow>科目代碼</th>";
    $Table_Data .= " <th bgcolor=yellow>科目名稱</th>";
    $Table_Data .= " <th bgcolor=yellow>班別</th><th bgcolor=yellow>篩選結果</th></tr>";

    foreach $warn(@WARN){
      $warn=~s/\n//;
      ($dept,$the_id,$group,$state)=split(/\s+/,$warn);
      %the_Dept=Read_Dept($dept);
      %the_Course=Read_Course($dept,$the_id,$group,"",$id);
      $Table_Data .= "<tr>";
      $Table_Data .= "<th>".$the_Dept{cname2}."</th>";
      $Table_Data .= "<th>".$the_id."</th>";
      $Table_Data .= "<th>".$the_Course{cname}."</th>";
      $Table_Data .= "<th>".$group."</th>";
      if($state == 0){
        $Table_Data .= "<th><font color=red>".$State[$state]."</font></th>";
      }else{
        $Table_Data .= "<th><font color=blue>".$State[$state]."</font></th>";
      }
      $Table_Data .= "</tr>";
    }
    $Table_Data .= "</table>";
  }else{
    $Table_Data = "系統篩選對您並無影響.";
  }
  return($Table_Data);
}
#########################################################################
#####  Form_Course_Change_Data_Table()
#####  產生並傳回科目異動的 HTML Table 碼
#########################################################################
sub Form_Course_Change_Data_Table()
{
  my($FILENAME2)=$DATA_PATH."Student_warning/".$Student{id}."_change";
  my($Table_Data, @Change);
  if(-e $FILENAME2)  {
    $Table_Data .= 
    "
      您選修的科目經過科目異動影響如下<br>
        <Table border=1 width=90%>
          <tr>
            <th colspan=9 bgcolor=yellow><font size=4>異動前</th>
            <th colspan=4 bgcolor=orange><font size=4>異動後</th>
          </tr>
          <tr>
            <th bgcolor=yellow>異動屬性</th><th bgcolor=yellow>開課系所</th>
            <th bgcolor=yellow>科目代碼</th>
            <th bgcolor=yellow>科目班別</th><th bgcolor=yellow>科目名稱</th>
            <th bgcolor=yellow>授課教師</th><th bgcolor=yellow>科目屬性</th>
            <th bgcolor=yellow>上課時間</th><th bgcolor=yellow>上課教室</th>
            <th bgcolor=orange>授課教師</th><th bgcolor=orange>科目屬性</th>
            <th bgcolor=orange>上課時間</th><th bgcolor=orange>上課教室</th>
          </tr>
    ";
    open(FILE,"<$FILENAME2");
    @Change=<FILE>;
    close(FILE);
    chop(@Change);
    foreach $change(@Change) {
      $Table_Data .="<tr>";
      @Temp = split("###",$change);
      $count=(@Temp);

      for($i=0;$i<$count;$i++)  {
        $Table_Data .="<th>$Temp[$i]</th>";
      }
      $Table_Data .="</tr>";
    }
    $Table_Data .= "
      </TABLE>
      若科目異動屬性為取消,則此科目已經由系統幫您退選<br>
      若異動後欄位空白代表該欄位並未異動，與異動前內容相同<br><hr size=1>
    ";
  }else{
    $Table_Data = "無影響\n<P>";
  }
  $Table_Data .= "<HR size=1>";
  return($Table_Data);
}
########################################################################
#####  Form_Course_Change_Conflict_Data_Table()
#####  產生並傳回異動造成衝堂的 HTML Table 碼
########################################################################
sub Form_Course_Change_Conflict_Data_Table()
{
  my(@Courses,$course,$i,$j,$k,$l,%temp1,%temp2,$flag, $Table_Data3);
  @Courses = Course_of_Student($Student{id});
  $count = (@Courses);
  my $Table_exists_flag = 0;
  
  for($i=0;$i< $count-1;$i++)  {
    for($j=$i+1;$j< $count;$j++)  {
      %temp1=Read_Course($Courses[$i]{dept},$Courses[$i]{id},$Courses[$i]{group});
      %temp2=Read_Course($Courses[$j]{dept},$Courses[$j]{id},$Courses[$j]{group});
      $flag=0;
      
#      for($k=0;$k<$temp1{total_time} && $flag eq "0";$k++)  {
#        for($l=0;$l<$temp2{total_time} && $flag eq "0";$l++)  {
#          if($temp1{time}[$k]{week} eq $temp2{time}[$l]{week} && $temp1{time}[$k]{time} eq $temp2{time}[$l]{time}) {
#            $flag++;
#          }
#        }
#      }
      if($flag ne "0")  {
        if($Table_exists_flag == 0) {     ###  如果Table不存在, 先印出 Table
          $Table_Data3 .= "
               以下每列之左右兩欄科目彼此時間衝堂<br>
               <table border=1 width=90%>
                 <tr>
                   <th colspan=3 bgcolor=yellow><font size=4>衝堂科目</th>
                   <th colspan=3 bgcolor=orange><font size=4>衝堂科目</th>
                 </tr>
                 <tr>
                   <th bgcolor=yellow>科目代碼</th>
                   <th bgcolor=yellow>科目班別</th><th bgcolor=yellow>科目名稱</th>
                   <th bgcolor=orange>科目代碼</th>
                   <th bgcolor=orange>科目班別</th><th bgcolor=orange>科目名稱</th>
                 </tr>
           ";
           $Table_exists_flag = 1;
        }
        $Table_Data3.="<TR><th>$temp1{id}</th><th>$temp1{group}</th><th>$temp1{cname}</th>";
        $Table_Data3.="<th>$temp2{id}</th><th>$temp2{group}</th><th>$temp2{cname}</th></TR>";
      }
    }
  }
  if( $Table_Data3 eq "" ) {
    $Table_Data3 .= "無影響<P>";
  }else{
    $Table_Data3 .= "</TABLE>";
  }
  return($Table_Data3);
}
########################################################################
#####  Form_Prerequisite_Course_Data_Table()
#####  產生並傳回因科目先修條件造成退選的 HTML Table 碼
########################################################################
sub Form_Prerequisite_Course_Data_Table()
{
  my($Table_Data4, @lines, $cou, $pre);

  my $Table_exists_flag = 0;
  my $pre_file = $DATA_PATH . "Student_warning/" . $Student{id} . "_prerequisite";
  
  if(-e $pre_file) {
    $Table_Data4 = "
        <TABLE border=1 width=90%>
          <tr>
            <th bgcolor=yellow><font size=4>被退選科目(代碼,班別)</th>
            <th bgcolor=orange><font size=4>不合先修條件科目(未修習或不及格)</th>
          </tr>
    ";
    open(PREFILE, $pre_file);
    @lines = <PREFILE>;
    close(PREFILE);
    foreach $line (@lines) {
      $line =~ s/\n/<br>\n/;
      ($cou, $pre) = split(/\t/, $line);
      $Table_Data4 .= "<TR><TD>$cou</TD><TD>$pre</TD></TR>";
    }
    $Table_Data4 .= "</TABLE>";
  }else{
    $Table_Data4 = "無<P>"
  }
  return($Table_Data4);
}
########################################################################
#####  Form_Duplicate_Course_Data_Table()
#####  產生並傳回因重複修習造成退選的 HTML Table 碼
########################################################################
sub Form_Duplicate_Course_Data_Table()
{
  my($Table_Data5, @lines, $cou, $pre);

  my $Table_exists_flag = 0;
  my $dup_file = $DATA_PATH . "Student_warning/" . $Student{id} . "_duplicate";
  my($c_id, $c_group, $c_name);

  if(-e $dup_file) {
    $Table_Data5 = "
        <TABLE border=1 width=90%>
          <tr>
            <th bgcolor=yellow><font size=4>被退選科目(代碼,班別)</th>
          </tr>
    ";
    open(DUPFILE, $dup_file);
    @lines = <DUPFILE>;
    close(DUPFILE);
    foreach $line (@lines) {
      $line =~ s/\n//;
      ($c_id, $c_group, $c_name) = split(/\t/, $line);
      $Table_Data5 .= "<TR><TD>$c_name($c_id, $c_group)</TD></TR>";
    }
    $Table_Data5 .= "</TABLE>";
  }else{
    $Table_Data5 = "無<P>"
  }
  return($Table_Data5);
}

########################################################################
#####  VIEW_WARNING()
#####  顯示篩選, 異動, 及異動導致衝堂等訊息
########################################################################
sub VIEW_WARNING
{
  my($id,$password)=@_;
  my($ACTION)="Main.cgi";
  my($Table_Data)="";
  my($Table_Data2)="";
  my($Table_Data3)="";
  my(@Change,@Temp,$i,$count);
  $State[0]="未選上";
  $State[1]="選上";

  $Table_Data  = Form_System_Choose_Data_Table();
  $Table_Data2 = Form_Course_Change_Data_Table();
  $Table_Data3 = Form_Course_Change_Conflict_Data_Table();
  $Table_Data4 = Form_Prerequisite_Course_Data_Table();
  $Table_Data5 = Form_Duplicate_Course_Data_Table();

  print << "End_of_HTML"
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <title>學生選課系統公佈欄</title>
</head>
<body background="$GRAPH_URL/ccu-sbg.jpg">
<center>
$HEAD_DATA<hr size=1>
<FONT color=GREEN>目前時間是: $time{time_string}</FONT><BR>
<font color=#dd2222 size=4>系統篩選公告</font><p>
$Table_Data

<hr size=1>
<font color=#dd2222 size=4>科目異動公告</font><p>
  $Table_Data2

<font color=#dd2222 size=4>科目異動影響導致科目衝堂</font><p>
$Table_Data3

<FONT color=#dd2222 size=4>因不符科目先修條件導致退選</FONT><P>
$Table_Data4

<FONT color=#dd2222 size=4>因重複修習同一科目導致退選</FONT><P>
$Table_Data5

<form action="$ACTION" method="post">
    <input type=hidden name="id" value="$id">
    <input type=hidden name="password" value="$password">
    <input type=hidden name="Flag" value="0">
    <input type=submit value="進入選課主選單">
</form>
</center>
</body>
End_of_HTML
}
#-----------------------------------------------------------------------
sub Check_For_Unencoded_Password()
{
  my($personal_id, $use_default_password_flag);
#  $crypt_salt = Read_Crypt_Salt($Input{id}, "student");
#  if($Input{crypt} eq "0") {
#    $Input{password} = Crypt($Input{password}, $crypt_salt);
#  }
  $personal_id = Crypt($Student{personal_id}, $crypt_salt);
  $use_default_password_flag 
    = Check_Student_Password($Input{id}, $Input{password}, $personal_id);
#  print("Check_Student_Password($Input{id}, $Input{password}, $personal_id)<BR>\n");
#  print(" flag = $use_default_password_flag<BR>\n");
  return($use_default_password_flag);
}
#-----------------------------------------------------------------------
sub MenuHTML
{
my($ID_DATA,$id,$password)=@_;

print qq(
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <title>國立中正大學$SUB_SYSTEM_NAME選課系統--選課主選單</title>
</head>
<body background="$GRAPH_URL./ccu-sbg.jpg">
<center>
  $ID_DATA
  <hr>
  <br>
  <b><font size=5>學生選課系統主選單</font></b>
  <br>
);

  if( $system_settings{black_list} == 1 ) {     ### 如果開啟黑名單功能
    $ban_time = Read_Ban_Record($id, $BAN_COUNT_LIMIT);		### 停權尚須多久恢復(大於0就是停權中)
    if($ban_time > 0) {
      Show_Ban_Message($ban_time, 0);
    }					  ### 即使關閉此功能, 系統仍會紀錄 log 
    if( $ban_time <= 0 ) {		  ### 差別在於是否顯示警訊和是否給加退選
      ButtonAction("add", $session_id, $id, $password);
      ButtonAction("delete", $session_id, $id, $password);
    }
  }else{                                        ### 如果關閉黑名單功能
    ButtonAction("add", $session_id, $id, $password);
    ButtonAction("delete", $session_id, $id, $password);
  }
  ButtonAction("view", $session_id, $id, $password);
  ButtonAction("warning", $session_id, $id, $password);
#  ButtonAction("update", $session_id, $id, $password);
  ButtonAction("print", $session_id, $id, $password);
  if( ($system_settings{allow_print_pdf} == 1) or ($SUPERUSER == 1) ) {
    ButtonAction("print2", $session_id, $id, $password);
  }
  if( Verify_For_Graduate_pdf($Student{id}, $Student{grade}) ) {
      ButtonAction("print3", $session_id, $id, $password);
  }
  if( ($IS_MAIN_SYSTEM == 1) or ($IS_MAIN_SYSTEM == -1) ) {
    ButtonAction("passwd", $session_id, $id, $password);
  }
  
#  print("[is_gra, is_main, ACCOUNT_NAME] = [$IS_GRA, $IS_MAIN_SYSTEM, $ACCOUNT_NAME]<BR>\n");

#require $LIBRARY_PATH."Error_Message.pm";
#  use MD5;

  $key = Generate_Key($id, "");
#  $key = "1243";
  Show_Message($id, $key) if( $IS_GRA != 1 );


if( $TEMP_FLAG_20040225 ) {
  Show_20040225_warning($id);
}
if( $TEMP_INFOTEST_MSG ) {
  Show_Infotest_Msg($id);
}

print qq(
  <HR>
);
#print qq(
#  <HR>
#  <SCRIPT language="javascript">
#    messageWindow = open('infotest_msg.html','messageWindow', 'resizable=yes, width=750, height=400');
#  </SCRIPT>
#);

#########  違章建築程式碼 2005/03/04
#####  2005/05/04 另外設計黑名單功能, 此部分已經廢除不用
#if( $system_settings{black_list} == 1 ) {     
#  @warning_id = Read_Black_List();
#  foreach $warning_id (@warning_id) {
#    if($warning_id eq $id) {
#      print qq(
#        <SCRIPT language="javascript">
#          messageWindow = open('warning.html','messageWindow', 'resizable=yes, width=400, height=400');
#        </SCRIPT>
#      ); 
#    }
#  }
#} 
###############################################################################

print qq(
  <FONT size=2>
    [ 選課系統資料查詢:
     <A href="../Query/Query_by_time1.cgi" target=NEW>以上課時間查詢開課資料</A> |
     <A href="../../Course/">開課資料查詢</A> | 
     <A href="../../Update_Course.html">檢視所有異動科目</A>
    ]
    <P>
    [ 選課系統說明:
     <A href="$KIKI_URL/contact.html">問題諮詢</A> |
     <A href="$KIKI_URL/user_manual/user_manual.htm">選課系統使用手冊</A> |
     <A href="http://kiki.ccu.edu.tw/ccu_timetable.doc">50/75分鐘課表</A> |
     <A href="../../math.html">選修數學系(所)開設之課程請參閱\本說明</A>
    ]
    <P>
);

#print qq(
#  [ 93學年第二學期資訊能力測驗: 
#     <a href="http://infotest.ccu.edu.tw/reports/93_2department.doc" 
#        target="_blank">各科系時間表</a> |
#     <a href="http://infotest.ccu.edu.tw/olp/reports/932post.doc"
#        target="_blank">大二統一檢測公告</a> |
#     <a href="http://infotest.ccu.edu.tw/olp/reports/93_2all_infotest.doc"
#        target="_blank">各梯次時間表</a> |
#     <a href="http://infotest.ccu.edu.tw/olp/reports/93newrule.doc"
#        target="_blank">收費須知</a>
#    ]
#);

print qq(
  </FONT>
  <br>
</center>

</body>
</html>
);
}
####################################################################################
sub MenuHTML_2
{
my($ID_DATA,$id,$password)=@_;

print qq(
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <title>選課主選單</title>
</head>
<body background="$GRAPH_URL./ccu-sbg.jpg">
<center>
  $ID_DATA
  <hr>
  <br>
  <b><font size=5>學生選課系統主選單</font></b>
  <br>
  <FONT size=2 color=RED>目前選課系統關閉中, 請於系統開放時間進入本系統!</FONT>
);
  ButtonAction("view", $session_id, $id, $password);
  ButtonAction("warning", $session_id, $id, $password);
#  ButtonAction("update", $session_id, $id, $password);
  ButtonAction("print", $session_id, $id, $password);
  ButtonAction("print2", $session_id, $id, $password)  if($system_settings{allow_print_pdf} == 1);
  if( ($system_settings{allow_print_graduate_pdf} == 1) or ($SUPERUSER == 1)) {
    if( ($Student{grade} >= 3) and ($Student{id} =~ /^4/) ) {
      ButtonAction("print3", $session_id, $id, $password); 
    } 
  }
#  ButtonAction("print3", $session_id, $id, $password)  if($system_settings{allow_print_graduate_pdf} == 1);

  if( ($IS_MAIN_SYSTEM == 1) or ($IS_MAIN_SYSTEM == -1) ) {
      ButtonAction("passwd", $session_id, $id, $password);
  }
  if( $TEMP_INFOTEST_MSG ) {
    Show_Infotest_Msg($id);
  }
  Show_Message($id, $key) if( $IS_GRA != 1 );

print qq(
  </FORM>
  <FONT size=2>
    [ 選課系統資料查詢:
     <A href="../Query/Query_by_time1.cgi" target=NEW>以上課時間查詢開課資料</A> |
     <A href="../../Course/">開課資料查詢</A> |
     <A href="../../Update_Course.html">檢視所有異動科目</A>
    ]
    <P>
    [ 選課系統說明:
     <A href="$KIKI_URL/contact.html">問題諮詢</A> |
     <A href="$KIKI_URL/user_manual/user_manual.htm">選課系統使用手冊</A> |
     <A href="http://kiki.ccu.edu.tw/ccu_timetable.doc">50/75分鐘課表</A> |
     <A href="../../math.html">選修數學系(所)開設之課程請參閱\本說明</A>
    ]
  </FONT>

  <BR>
 </center>
 <CENTER>
   <BLINK><FONT color=RED>--&gt</FONT></BLINK>
     <A href="http://kiki.ccu.edu.tw/ccu_timetable.doc">50/75分鐘新制課表</A>
   <BLINK><FONT color=RED>&lt--</FONT></BLINK>
   <BR>
 </CENTER>
</body>
</html>
);

}
##############################################################################
sub Enter_Menu_Change_Password()
{
  my($ID_DATA,$id,$password,$use_default_password_flag)=@_;

  print qq(
    <html>
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=big5">
      <title>選課主選單</title>
    </head>
    <body background="$GRAPH_URL./ccu-sbg.jpg">
    <center>
      $ID_DATA
      <hr>
      <br>
      <b><font size=5>學生選課系統主選單</font></b>
      <br>
  );
  if( $use_default_password_flag eq "DEFAULT_PASSWORD2" ) {
    print qq(
       <FONT size=2 color=RED>您目前使用生日做為密碼,
       為確保您選課帳號的安全,  請先更改後再進行加退選等動作!</FONT>
    );
  }else{
    print qq(
      <FONT size=2 color=RED>即日起選課系統密碼將與學籍系統密碼整合,<BR>
      為確保您選課帳號的安全, 請先更改密碼後再進行加退選等動作!</FONT>
    );
#    print qq(
#       <FONT size=2 color=RED>您使用身份證號做為密碼,
#       為確保您選課帳號的安全,  請先更改後再進行加退選等動作!</FONT>
#    );
  }
#  ButtonAction("view", $session_id, $id, $password);
#  ButtonAction("update", $session_id, $id, $password);
#  ButtonAction("print", $session_id, $id, $password);
  if( ($IS_MAIN_SYSTEM == 1) or ($IS_MAIN_SYSTEM == -1) ) {
    ButtonAction("passwd", $session_id, $id, $password);
  }

  print qq(
    </FORM>
    <P>
    <HR>
    <FONT size=2>
      [<A href="../../Course/">開課資料查詢</A> |
       <A href="../../Update_Course.html">檢視所有異動科目</A> |
       <A href="$KIKI_URL/contact.html">問題諮詢</A> |
       <A href="$KIKI_URL/user_manual/user_manual.htm">選課系統使用手冊</A> |
       <A href="$KIKI_URL/cc_printer.html">電腦教室印表機管理辦法</A>
      ]<P>
    </FONT>

    <BR>
   </center>
   <CENTER>
     <BLINK><FONT color=RED>--&gt</FONT></BLINK>
       <A href="http://kiki.ccu.edu.tw/ccu_timetable.doc">50/75分鐘新制課表</A>
     <BLINK><FONT color=RED>&lt--</FONT></BLINK>
     <BR>
   </CENTER>
  </body>
  </html>
  );
  exit();
}

##############################################################################
sub Enter_Menu_Error
{
my($HEAD_DATA)=@_;
print << "MenuHTML"
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <title>選課主選單</title>
</head>
<body background="$GRAPH_URL./ccu-sbg.jpg">
<center>
  $ID_DATA
  <hr>
  <font size=3>目前選課系統關閉中, 請於系統開放時間進入本系統!</font>
</center>
</body>
</html>
MenuHTML

}
##############################################################################
sub ButtonAction()
{
  my %map;
  %{$map{"add"}}	= ( "name" => "加選", "action" => "Add_Course00.cgi" );
  %{$map{"delete"}}	= ( "name" => "退選", "action" => "Del_Course00.cgi" );
  %{$map{"passwd"}}	= ( "name" => "更改密碼", "action" => "Change_Password00.php" );
  %{$map{"view"}}	= ( "name" => "檢視已選修科目", "action" => "Selected_View00.cgi" );
  %{$map{"update"}}	= ( "name" => "檢視所有異動科目", "action" => "../../Update_Course.html" );
  %{$map{"print"}}	= ( "name" => "列印選課單", "action" => "Print_Course.cgi" );
  %{$map{"print2"}}     = ( "name" => "列印選課結果單", "action" => "Print_Course_pdf.cgi" );
  %{$map{"print3"}}     = ( "name" => "檢視畢業資格審查表", "action" => "Print_Graduate_pdf.cgi" );
  %{$map{"warning"}}	= ( "name" => "檢視篩選公告", "action" => "View_Warning.cgi" );
 
  my ($selection, $session_id, $id, $password) = @_;

  if( $selection ne "update" ) {
    print qq(
      <FORM method=POST action="$map{$selection}{action}">
      <input type=hidden name="session_id" value="$session_id">
    );
#      <input type=hidden name="id" value="$id">
#      <input type=hidden name="password" value="$password">
#    );
  }else{
    print qq(
      <FORM method=GET action="$map{$selection}{action}">
    );
  }

  if( $selection eq "passwd" ) {
    print qq(
      <INPUT type=hidden name=HEAD_DATA value="$HEAD_DATA">
    );
  }
  
  print qq(
      <input type=submit value="$map{$selection}{name}"><BR>
    </FORM>
  );
}
##############################################################################
sub Show_20040225_warning()
{
  my($warning_file, @lines);  
  my($id) = @_;
  
  $warning_file = $DATA_PATH . "20040224/" . $id;
  $explain_file = $HOME_URL . "20040224/index.html";
  $remedy_file  = $HOME_URL . "20040224/remedy.html";

  if( -e $warning_file ) {
    open(WARNING, $warning_file);
    @lines = <WARNING>;
    close(WARNING);
    print qq(
      <TABLE BORDER=0>
        <TR><TD bgcolor=LIGHTYELLOW>
        <CENTER>
        由於 92 學年度第二學期選課系統內部錯誤, 影響當時同學以下選課紀錄被退選:
        <PRE>@lines</PRE>
        請同學於本學期第一階段選課時, 自行加選以上科目, 以獲得優先篩選順序.<BR>
        ps. 若同學已於上學期加簽選上該科目, 請忽略此公告.
        <P>
        相關連結: 
        [ <A href="$explain_file" target=NEW>電算中心道歉啟事</A> |
          <A href="$remedy_file" target=NEW>選課系統錯誤補救方法</A>
        ]
        </TD></TR>
      </TABLE>
      &nbsp<P>
    );
  }
}
####################################################################################
sub Show_Infotest_Msg()
{
  my($id) = @_;

  if( $id =~ /^49[^0]/ ) {
   print("<FONT color=RED>若您尚未通過資訊能力測驗, 請詳閱\");
   print("<A href=\"http://infotest.ccu.edu.tw/reports/msg.php\" target=NEW>資訊能力測驗公告</A></FONT><P>\n");
  }
}
