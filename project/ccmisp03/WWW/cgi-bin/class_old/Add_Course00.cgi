#!/usr/local/bin/perl
###############################################################################
#####  Add_Course_00.cgi
#####  �[��\�� -- ��ܬ�ت��t�Ҧ~��
#####  �ʺA�C�X�|�Ӧ~�ũM�Ҧ��t�Ҩѿ��
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
#####  �o�@�q�ϥ� CGI.pm, ���O�|���Ӫ� User_Input() �m STDIN,
#####  �ҥH�s�y�@�� $fake_query_string �ᵹ User_Input() �H����̨æs
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
########    �Y�D��Үɶ��h��ܤ��i�i�J  #########
if($SUPERUSER != 1){     ## �D superuser ���ϥΪ�
  if( (Whats_Sys_State()==0)or(Whats_Sys_State()==1) ){
    Enter_Menu_Sys_State_Forbidden($HEAD_DATA);
  }
}

my($HEAD_DATA)=Head_of_Individual($Student{name},$Student{id},$Dept{cname},$Student{grade},$Student{class});
print qq(
  <html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <TITLE>�[�������</TITLE>
  </head>
  <body background="$GRAPH_URL./ccu-sbg.jpg">
  <center>
    $HEAD_DATA
    <hr>
);                    

##### �ˮ֬O�_�ݭn���T�{���~���f�d��. �Y�����T�{�o�|���T�{, �h�������
##### 2005/09/07 Nidalap :D~
if( Verify_For_Graduate_pdf($Student{id}, $Student{grade}) == 2 ) {
  if( not if_Confirmed_For_Graduate_pdf($Student{id}) ) {
    print("<P>�Х��T�{�z�����~���f�d��, �A�i��[�h��!<BR>");
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
    <FONT size=2 color=RED>��s�Ҷ}�]��ؽп�ܤ@�~��</FONT><BR>
    <table border=0>
    <tr>
      <th bgcolor=pink>�~<br>��</th>
      <td width=100> <input type=radio name=grade value=1 checked>�@�~�� </td>
      <td width=100> <input type=radio name=grade value=2>�G�~�� </td>
      <td width=100> <input type=radio name=grade value=3>�T�~�� </td>
      <td width=100> <input type=radio name=grade value=4>�|�~�� </td>
      <td>&nbsp </td>
      <td>&nbsp </td>
    </tr>
    <tr>
    <th bgcolor=pink>�t<br><br><br><br><br><br>��</th>
    <td colspan=6>$DATA</td>
    </tr>
    </table>
    <input type=submit value="��ݸӨt�Ҷ}�Ҹ��">
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
    $DATA = $DATA . "	<tr><th bgcolor=#99ffff width=12%>�u�ǰ|</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=12%>�z�ǰ|</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=12%>�޲z�ǰ|</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=12%>���|��ǰ|</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=12%>��ǰ|</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=12%>�k�ǰ|</th>\n";  
    $DATA = $DATA . "       <th bgcolor=#99ffff width=12%>�Ш|�ǰ|</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=12%>�@�P��</th><TR>\n";        

    foreach $dept(@Dept){
      %Dept=Read_Dept($dept);
      if( ($SUB_SYSTEM==3) or ($SUB_SYSTEM==4) ) {    ###  �M�Z�t�Τ��C�X�j�ǳ�
        next  if($dept =~ /4$/);
      }
      #####  �Ĥ@���q��Ү�, �ƾǨt�Ҷ}�]���ҵ{�ĥ����Ĺ�B�������, �t�αĤ��P�ѿ�Ҧ]����
      if( $system_flags{allow_select_math} == 1 ) {     ###  �u�}��D�ƾǨt�ҵ{
        next if( is_Math_Dept($Dept{id}) );
      }elsif( $system_flags{allow_select_math} == 2 ) { ###  �u�}��ƾǨt�ҵ{
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
