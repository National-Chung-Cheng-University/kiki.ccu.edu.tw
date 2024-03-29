#!/usr/local/bin/perl
###############################################################################
#####  Add_Course_00.cgi
#####  加選功能 -- 選擇科目的系所年級
#####  動態列出四個年級和所有系所供選擇
#####  Coder   : Nidalap :D~
#####  Modified: May 23, 2002
###############################################################################
#$| = 1;
#print("Content-type:text/html\n\n");
#$| = 0;

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Password.pm";
#require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Select_Course.pm";
require $LIBRARY_PATH."Student.pm";
#require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."System_Settings.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Session.pm";

###########################################################################
#####  這一段使用 CGI.pm, 但是會跟原來的 User_Input() 搶 STDIN,
#####  所以製造一個 $fake_query_string 丟給 User_Input() 以讓兩者並存
#####  Code added on 2005/02/15, Nidalap :D~
use CGI qw(:standard);
$query = new CGI;

@names = $query->param;
foreach $name (@names) {
#  $temp = param($name);
#  print("[key, value] = [$name, $temp]<BR>\n");
  if( $fake_query_string eq "") {
    $fake_query_string = $name . "=" . param($name);
  }else{
    $fake_query_string .= "&" . $name . "=" . param($name);
  }
}
#$cookie3 = $query->cookie(-name => 'crypt', -value=>'1', -expires=>'+1h');
#if( $query->param('crypt') eq "0" ) {
  $cookie2 = $query->cookie(-name=>'password', -value=>param('password'), -expires=>'+1h');
#}
#
#print $query->header(-cookie=>[$cookie2]);
print header;

#foreach $name ($query->cookie()) {
#  $temp = $query->cookie($name);
#  print("in cookie: $name -> $temp;<BR>\n");
#}

#print("password = ", param('password'), "<BR>\n");

%Input = User_Input($fake_query_string);

($Input{id}, $Input{password}, $login_time, $ip) = Read_Session($Input{session_id});

#$Input{id}       = $query->cookie('id');
#$Input{password} = $query->cookie('password');
#%Input=User_Input();
###########################################################################


my(%Student,%Dept);

#%Input=User_Input();
%Student=Read_Student($Input{id});
%Dept=Read_Dept($Student{dept});
%system_flags = Read_System_Settings();
%system_settings = %system_flags;

#print("settings = $system_flags{show_last_total}<br>\n");
#print("session_id, id, pass = $Input{session_id}, $Input{id}, $Input{password}<BR>");
Check_Student_Password($Input{id}, $Input{password});
########    若非選課時間則顯示不可進入  #########
if($SUPERUSER != 1){     ## 非 superuser 的使用者
  if( (Whats_Sys_State()==0)or(Whats_Sys_State()==1) ){
    Enter_Menu_Sys_State_Forbidden($HEAD_DATA);
  }
}

my($HEAD_DATA)=Head_of_Individual($Student{name},$Student{id},$Dept{cname},$Student{grade},$Student{class});
print qq(
  <html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <TITLE>加選分類表</TITLE>
  </head>
  <body background="$GRAPH_URL./ccu-sbg.jpg">
  <center>
    $HEAD_DATA
    <hr>
);                    

##### 檢核是否需要先確認畢業資格審查表. 若必須確認卻尚未確認, 則不給選課
##### 2005/09/07 Nidalap :D~
if( Verify_For_Graduate_pdf($Student{id}, $Student{grade}) == 2 ) {
  if( not if_Confirmed_For_Graduate_pdf($Student{id}) ) {
    print("<P>請先確認您的畢業資格審查表, 再進行加退選!<BR>");
    my($LINK)=Select_Course_Link($Input{id},$Input{password});
    print("$LINK");

    exit();
  }
}

my($DATA)=DEPT_TABLE();
SELECT_MENU($HEAD_DATA,$Student{id},$Student{password},$DATA);

sub SELECT_MENU
{
my($HEAD_DATA,$id,$password,$DATA)=@_;

print << "End_of_HTML"
    <br>
    <form action="Add_Course01.cgi" method="post">
    <input type=hidden name="session_id" value="$Input{session_id}">
    <input type=hidden name="page" value=0>
    <FONT size=2 color=RED>研究所開設科目請選擇一年級</FONT><BR>
    <table border=0>
    <tr>
      <th bgcolor=pink>年<br>級</th>
      <td width=100> <input type=radio name=grade value=1 checked>一年級 </td>
      <td width=100> <input type=radio name=grade value=2>二年級 </td>
      <td width=100> <input type=radio name=grade value=3>三年級 </td>
      <td width=100> <input type=radio name=grade value=4>四年級 </td>
      <td>&nbsp </td>
      <td>&nbsp </td>
    </tr>
    <tr>
    <th bgcolor=pink>系<br><br><br><br><br><br>所</th>
    <td colspan=6>$DATA</td>
    </tr>
    </table>
    <input type=submit value="察看該系所開課資料">
    </form>
</center>
</body>
</html>
End_of_HTML
}

sub DEPT_TABLE
{
    my(@Dept)=Find_All_Dept();
    my($DATA)="";
    my($Dept1,$Dept2,$Dept3,$Dept4,$Dept5,$Dept6,$Dept7,$DeptI)="";

    $DATA = $DATA . "<table width=100% border=0>\n";
    $DATA = $DATA . "	<tr><th bgcolor=#99ffff width=12%>工學院</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=12%>理學院</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=12%>管理學院</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=12%>社會科學院</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=12%>文學院</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=12%>法學院</th>\n";  
    $DATA = $DATA . "       <th bgcolor=#99ffff width=12%>教育學院</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=12%>共同科</th><TR>\n";        

    foreach $dept(@Dept){
      %Dept=Read_Dept($dept);
      if( ($SUB_SYSTEM==3) or ($SUB_SYSTEM==4) ) {    ###  專班系統不列出大學部
        next  if($dept =~ /4$/);
      }
      #####  第一階段選課時, 數學系所開設之課程採先選先贏額滿為止制, 系統採不同天選課因應之
      if( $system_flags{allow_select_math} == 1 ) {     ###  只開放非數學系課程
        next if( is_Math_Dept($Dept{id}) );
      }elsif( $system_flags{allow_select_math} == 2 ) { ###  只開放數學系課程
        next if( not is_Math_Dept($Dept{id}) );
      }
      if    ($Dept{college} eq "I") {
        $DeptI=$DeptI."<input type=radio name=dept value=\"".$Dept{id}."\">";
        $DeptI=$DeptI.$Dept{cname2}."<BR>\n";
      }elsif($Dept{college} eq "7") {
        $Dept7=$Dept7."<input type=radio name=dept value=\"".$Dept{id}."\">";
        $Dept7=$Dept7.$Dept{cname2}."<br>\n";
      }elsif($Dept{college} eq "6") {
        $Dept6=$Dept6."<input type=radio name=dept value=\"".$Dept{id}."\">";
        $Dept6=$Dept6.$Dept{cname2}."<br>\n";
      }elsif($Dept{college} eq "5"){
        $Dept5=$Dept5."<input type=radio name=dept value=\"".$Dept{id}."\">";
        $Dept5=$Dept5.$Dept{cname2}."<br>\n";
      }elsif($Dept{college} eq "4"){
        $Dept4=$Dept4."<input type=radio name=dept value=\"".$Dept{id}."\">";
        $Dept4=$Dept4.$Dept{cname2}."<br>\n";
      }elsif($Dept{college} eq "3"){
        $Dept3=$Dept3."<input type=radio name=dept value=\"".$Dept{id}."\">";
        $Dept3=$Dept3.$Dept{cname2}."<br>\n";
      }elsif($Dept{college} eq "2"){
        $Dept2=$Dept2."<input type=radio name=dept value=\"".$Dept{id}."\">";
        $Dept2=$Dept2.$Dept{cname2}."<br>\n";
      }elsif($Dept{college} eq "1"){
        $Dept1=$Dept1."<input type=radio name=dept value=\"".$Dept{id}."\">";
        $Dept1=$Dept1.$Dept{cname2}."<br>\n";
      }
    }

    $DATA = $DATA ."<tr>\n";
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept4."</td>\n";
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept2."</td>\n";
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept5."</td>\n";
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept3."</td>\n";
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept1."</td>\n";
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept6."</td>\n"; 
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept7."</td>\n"; 
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$DeptI."</td>\n";
    $DATA = $DATA ."</tr>\n";
    $DATA = $DATA . "   </table>\n";

    return($DATA);
}

