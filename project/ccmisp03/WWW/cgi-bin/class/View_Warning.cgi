#!/usr/local/bin/perl
###########################################################################
#####  View_Warning.cgi
#####  �˵��z�綠�i
#####  ���өM Main.cgi ��b�@�_, ���~�}�l�⥦�W�ߥX��.
#####  Nidalap :D~
#####  2005/02/17

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

my(%Student,%Dept);
%time = gettime();

###########################################################################
#####  �o�@�q�ϥ� CGI.pm, ���O�|���Ӫ� User_Input() �m STDIN,
#####  �ҥH�s�y�@�� $fake_query_string �ᵹ User_Input() �H����̨æs
#####  Code added on 2005/02/15, Nidalap :D~
use CGI qw(:standard);
$query = new CGI;

#  $Input{id}       = $query->cookie('id');
#  $Input{password} = $query->cookie('password');
#  $session_id      = $query->cookie('session_id');
print header;
#  print("*session_id = $session_id<BR>\n");
@names = $query->param;         ###  ���� fake_query_string �Ψ��F User_Input()
foreach $name (@names) {
  if( $fake_query_string eq "") {
    $fake_query_string = $name . "=" . param($name);
  }else{
    $fake_query_string .= "&" . $name . "=" . param($name);
  }
}
      
%Input = User_Input($fake_query_string);
($Input{id}, $Input{password}, $login_time, $ip) = Read_Session($Input{session_id});
#print("session_id, id, pass = $Input{session_id}, $Input{id}, $Input{password}<BR>"); 

#%Input=User_Input();
###########################################################################

%Student=Read_Student($Input{id});
%Dept=Read_Dept($Student{dept});
%system_settings = Read_System_Settings();

Check_Student_Password($Input{id}, $Input{password});
my($HEAD_DATA)=Head_of_Individual($Student{name},$Student{id},$Dept{cname},$Student{grade},$Student{class});

if($SUPERUSER != 1){     ## �D superuser ���ϥΪ�
  ##  warning message ���s�b
#  print(" flag = $use_default_password_flag<BR>\n");
  ##  Check the System Status !!  Added by hanchu @ 1999/9/10
  if(Whats_Sys_State() == 0){
    Enter_Menu_Sys_State_Forbidden($HEAD_DATA);
  }else{
    VIEW_WARNING($Input{id}, $Input{password});
  }
}else{                   ## superuser ���ϥΪ�
  VIEW_WARNING($Input{id}, $Input{password});
}
###########################################################################
#####  Form_System_Choose_Data_Table()
#####  ���ͨöǦ^�z�ﵲ�G�� HTML Table �X
###########################################################################
sub Form_System_Choose_Data_Table()
{
  my($FILENAME)=$DATA_PATH."Student_warning/".$Student{id}."_warning";
  my($Table_Data, @WARN);
  if(-e $FILENAME){
    open(FILE,"<$FILENAME");
    @WARN=<FILE>;
    close(FILE);
    $Table_Data .= "�z��ת���ظg�L�t�οz�ﵲ�G�p�U(�Y�z�ﵲ�G���襤,�h����ؤw�g�Ѩt�����z�h��)<br>";
    $Table_Data .= "<FONT color=RED>��Ҹ�ƥH��ҲM�欰�D, �ЦܥD��椤\"�˵��w��׬��\"�T�{��ҵ��G</FONT>";
    $Table_Data .= "<table border=1 width=90%><tr>";
    $Table_Data .= " <th bgcolor=yellow>�}�Ҩt��</th><th bgcolor=yellow>��إN�X</th>";
    $Table_Data .= " <th bgcolor=yellow>��ئW��</th>";
    $Table_Data .= " <th bgcolor=yellow>�Z�O</th><th bgcolor=yellow>�z�ﵲ�G</th></tr>";

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
    $Table_Data = "�t�οz���z�õL�v�T.";
  }
  return($Table_Data);
}
#########################################################################
#####  Form_Course_Change_Data_Table()
#####  ���ͨöǦ^��ز��ʪ� HTML Table �X
#########################################################################
sub Form_Course_Change_Data_Table()
{
  my($FILENAME2)=$DATA_PATH."Student_warning/".$Student{id}."_change";
  my($Table_Data, @Change);
  if(-e $FILENAME2)  {
    $Table_Data .= 
    "
      �z��ת���ظg�L��ز��ʼv�T�p�U<br>
        <Table border=1 width=90%>
          <tr>
            <th colspan=9 bgcolor=yellow><font size=4>���ʫe</th>
            <th colspan=4 bgcolor=orange><font size=4>���ʫ�</th>
          </tr>
          <tr>
            <th bgcolor=yellow>�����ݩ�</th><th bgcolor=yellow>�}�Ҩt��</th>
            <th bgcolor=yellow>��إN�X</th>
            <th bgcolor=yellow>��دZ�O</th><th bgcolor=yellow>��ئW��</th>
            <th bgcolor=yellow>�½ұЮv</th><th bgcolor=yellow>����ݩ�</th>
            <th bgcolor=yellow>�W�Үɶ�</th><th bgcolor=yellow>�W�ұЫ�</th>
            <th bgcolor=orange>�½ұЮv</th><th bgcolor=orange>����ݩ�</th>
            <th bgcolor=orange>�W�Үɶ�</th><th bgcolor=orange>�W�ұЫ�</th>
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
      �Y��ز����ݩʬ�����,�h����ؤw�g�Ѩt�����z�h��<br>
      �Y���ʫ����ťեN�������å����ʡA�P���ʫe���e�ۦP<br><hr size=1>
    ";
  }else{
    $Table_Data = "�L�v�T\n<P>";
  }
  $Table_Data .= "<HR size=1>";
  return($Table_Data);
}
########################################################################
#####  Form_Course_Change_Conflict_Data_Table()
#####  ���ͨöǦ^���ʳy���İ� HTML Table �X
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
        if($Table_exists_flag == 0) {     ###  �p�GTable���s�b, ���L�X Table
          $Table_Data3 .= "
               �H�U�C�C�����k�����ة����ɶ��İ�<br>
               <table border=1 width=90%>
                 <tr>
                   <th colspan=3 bgcolor=yellow><font size=4>�İ���</th>
                   <th colspan=3 bgcolor=orange><font size=4>�İ���</th>
                 </tr>
                 <tr>
                   <th bgcolor=yellow>��إN�X</th>
                   <th bgcolor=yellow>��دZ�O</th><th bgcolor=yellow>��ئW��</th>
                   <th bgcolor=orange>��إN�X</th>
                   <th bgcolor=orange>��دZ�O</th><th bgcolor=orange>��ئW��</th>
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
    $Table_Data3 .= "�L�v�T<P>";
  }else{
    $Table_Data3 .= "</TABLE>";
  }
  return($Table_Data3);
}
########################################################################
#####  Form_Prerequisite_Course_Data_Table()
#####  ���ͨöǦ^�]��إ��ױ���y���h�諸 HTML Table �X
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
            <th bgcolor=yellow><font size=4>�Q�h����(�N�X,�Z�O)</th>
            <th bgcolor=orange><font size=4>���X���ױ�����(���ײߩΤ��ή�)</th>
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
    $Table_Data4 = "�L<P>"
  }
  return($Table_Data4);
}
########################################################################
#####  Form_Duplicate_Course_Data_Table()
#####  ���ͨöǦ^�]���ƭײ߳y���h�諸 HTML Table �X
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
            <th bgcolor=yellow><font size=4>�Q�h����(�N�X,�Z�O)</th>
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
    $Table_Data5 = "�L<P>"
  }
  return($Table_Data5);
}

########################################################################
#####  VIEW_WARNING()
#####  ��ܿz��, ����, �β��ʾɭP�İ󵥰T��
########################################################################
sub VIEW_WARNING
{
  my($id,$password)=@_;
  my($ACTION)="Main.cgi";
  my($Table_Data)="";
  my($Table_Data2)="";
  my($Table_Data3)="";
  my(@Change,@Temp,$i,$count);
  $State[0]="����W";
  $State[1]="��W";

  $Table_Data  = Form_System_Choose_Data_Table();
  $Table_Data2 = Form_Course_Change_Data_Table();
  $Table_Data3 = Form_Course_Change_Conflict_Data_Table();
  $Table_Data4 = Form_Prerequisite_Course_Data_Table();
  $Table_Data5 = Form_Duplicate_Course_Data_Table();

  print << "End_of_HTML"
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <title>�ǥͿ�Ҩt�Τ��G��</title>
</head>
<body background="$GRAPH_URL/ccu-sbg.jpg">
<center>
$HEAD_DATA<hr size=1>
<FONT color=GREEN>�ثe�ɶ��O: $time{time_string}</FONT><BR>
<font color=#dd2222 size=4>�t�οz�綠�i</font><p>
$Table_Data

<hr size=1>
<font color=#dd2222 size=4>��ز��ʤ��i</font><p>
  $Table_Data2

<font color=#dd2222 size=4>��ز��ʼv�T�ɭP��ؽİ�</font><p>
$Table_Data3

<FONT color=#dd2222 size=4>�]���Ŭ�إ��ױ���ɭP�h��</FONT><P>
$Table_Data4

<FONT color=#dd2222 size=4>�]���ƭײߦP�@��ؾɭP�h��</FONT><P>
$Table_Data5

<form action="$ACTION" method="post">
    <input type=hidden name="session_id" value="$Input{session_id}">
    <input type=submit value="�^���ҥD���">
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
    <title>��ߤ����j��$SUB_SYSTEM_NAME��Ҩt��--��ҥD���</title>
</head>
<body background="$GRAPH_URL./ccu-sbg.jpg">
<center>
  $ID_DATA
  <hr>
  <br>
  <b><font size=5>�ǥͿ�Ҩt�ΥD���</font></b>
  <br>
);

  ButtonAction("add", $id, $password);
  ButtonAction("delete", $id, $password);
  ButtonAction("view", $id, $password);
  ButtonAction("update", $id, $password);
  ButtonAction("print", $id, $password);
  if( ($system_settings{allow_print_pdf} == 1) or ($SUPERUSER == 1) ) {
    ButtonAction("print2", $id, $password);
  }
  if( ($system_settings{allow_print_graduate_pdf} == 1) or ($SUPERUSER == 1) ) {
#    if( ($TEMP_RESTRICT_DEPT == 1) and 
#        (($Dept{id} eq "1104")or($Dept{id} eq "3304")or($Dept{id} eq "4104") ) )  {
      ButtonAction("print3", $id, $password);
#    }
  }
  ButtonAction("passwd", $id, $password);

if( $TEMP_FLAG_20040225 ) {
  Show_20040225_warning($id);
}
if( $TEMP_INFOTEST_MSG ) {
  Show_Infotest_Msg($id);
}
print qq(
  <HR>
  <SCRIPT language="javascript">
    messageWindow = open('infotest_msg.html','messageWindow', 'resizable=yes, width=750, height=400');
  </SCRIPT>
  <FONT size=2>
    [ ��Ҩt�θ�Ƭd��:
     <A href="../../Course/">�}�Ҹ�Ƭd��</A> | 
     <A href="../../Update_Course.html">�˵��Ҧ����ʬ��</A>
    ]
    <P>
    [ ��Ҩt�λ���:
     <A href="$KIKI_URL/contact.html">���D�Ը�</A> |
     <A href="$KIKI_URL/user_manual/user_manual.htm">��Ҩt�ΨϥΤ�U</A> |
     <A href="http://kiki.ccu.edu.tw/ccu_timetable.doc">50/75�����Ҫ�</A> |
     <A href="../../math.html">��׼ƾǨt(��)�}�]���ҵ{�аѾ\\������</A>
    ]
    <P>
    [ 93�Ǧ~�Ĥ@�Ǵ���T��O����: 
     <a href="http://infotest.ccu.edu.tw/olp/reports/93_1department.doc" 
        target="_blank">�U��t�ɶ���</a> |
     <a href="http://infotest.ccu.edu.tw/olp/reports/931post.doc"
        target="_blank">�w�����礽�i</a> |
     <a href="http://infotest.ccu.edu.tw/olp/reports/93_1all_infotest.doc"
        target="_blank">�U�覸�ɶ���</a> |
     <a href="http://infotest.ccu.edu.tw/olp/reports/93newrule.doc"
        target="_blank">���O����</a>
    ]
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
    <title>��ҥD���</title>
</head>
<body background="$GRAPH_URL./ccu-sbg.jpg">
<center>
  $ID_DATA
  <hr>
  <br>
  <b><font size=5>�ǥͿ�Ҩt�ΥD���</font></b>
  <br>
  <FONT size=2 color=RED>�ثe��Ҩt��������, �Щ�t�ζ}��ɶ��i�J���t��!</FONT>
);
  ButtonAction("view", $id, $password);
  ButtonAction("update", $id, $password);
  ButtonAction("print", $id, $password);
  ButtonAction("print2", $id, $password)  if($system_settings{allow_print_pdf} == 1);
  if( ($system_settings{allow_print_graduate_pdf} == 1) or ($SUPERUSER == 1)) {
#    if( ($TEMP_RESTRICT_DEPT == 1) and
#        (($Dept{id} eq "1104")or($Dept{id} eq "3304")or($Dept{id} eq "4104") ) )  {
      ButtonAction("print3", $id, $password);
#    }
  }
#  ButtonAction("print3", $id, $password)  if($system_settings{allow_print_graduate_pdf} == 1);

  ButtonAction("passwd", $id, $password);
  if( $TEMP_INFOTEST_MSG ) {
    Show_Infotest_Msg($id);
  }

print qq(
  </FORM>
  <FONT size=2>
    [<A href="../../Course/">�}�Ҹ�Ƭd��</A> |
     <A href="../../Update_Course.html">�˵��Ҧ����ʬ��</A> |
     <A href="$KIKI_URL/contact.html">���D�Ը�</A> |
     <A href="$KIKI_URL/user_manual/user_manual.htm">��Ҩt�ΨϥΤ�U</A> |
     <A href="$KIKI_URL/cc_printer.html">�q���ЫǦL�����޲z��k</A>
    ]<P>
  </FONT>

  <BR>
 </center>
 <CENTER>
   <BLINK><FONT color=RED>--&gt</FONT></BLINK>
     <A href="http://kiki.ccu.edu.tw/ccu_timetable.doc">50/75�����s��Ҫ�</A>
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
      <title>��ҥD���</title>
    </head>
    <body background="$GRAPH_URL./ccu-sbg.jpg">
    <center>
      $ID_DATA
      <hr>
      <br>
      <b><font size=5>�ǥͿ�Ҩt�ΥD���</font></b>
      <br>
  );
  if( $use_default_password_flag eq "DEFAULT_PASSWORD2" ) {
    print qq(
       <FONT size=2 color=RED>�z�ثe�ϥΥͤ鰵���K�X,
       ���T�O�z��ұb�����w��,  �Х�����A�i��[�h�ﵥ�ʧ@!</FONT>
    );
  }else{
    print qq(
       <FONT size=2 color=RED>�z�ϥΨ����Ҹ������K�X,
       ���T�O�z��ұb�����w��,  �Х�����A�i��[�h�ﵥ�ʧ@!</FONT>
    );
  }
#  ButtonAction("view", $id, $password);
#  ButtonAction("update", $id, $password);
#  ButtonAction("print", $id, $password);
  ButtonAction("passwd", $id, $password);

  print qq(
    </FORM>
    <FONT size=2>
      [<A href="../../Course/">�}�Ҹ�Ƭd��</A> |
       <A href="../../Update_Course.html">�˵��Ҧ����ʬ��</A> |
       <A href="$KIKI_URL/contact.html">���D�Ը�</A> |
       <A href="$KIKI_URL/user_manual/user_manual.htm">��Ҩt�ΨϥΤ�U</A> |
       <A href="$KIKI_URL/cc_printer.html">�q���ЫǦL�����޲z��k</A>
      ]<P>
    </FONT>

    <BR>
   </center>
   <CENTER>
     <BLINK><FONT color=RED>--&gt</FONT></BLINK>
       <A href="http://kiki.ccu.edu.tw/ccu_timetable.doc">50/75�����s��Ҫ�</A>
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
    <title>��ҥD���</title>
</head>
<body background="$GRAPH_URL./ccu-sbg.jpg">
<center>
  $ID_DATA
  <hr>
  <font size=3>�ثe��Ҩt��������, �Щ�t�ζ}��ɶ��i�J���t��!</font>
</center>
</body>
</html>
MenuHTML

}
##############################################################################
sub ButtonAction()
{
  my %map;
  %{$map{"add"}}	= ( "name" => "�[��", "action" => "Add_Course00.cgi" );
  %{$map{"delete"}}	= ( "name" => "�h��", "action" => "Del_Course00.cgi" );
  %{$map{"passwd"}}	= ( "name" => "���K�X", "action" => "Change_Password00.php" );
  %{$map{"view"}}	= ( "name" => "�˵��w��׬��", "action" => "Selected_View00.cgi" );
  %{$map{"update"}}	= ( "name" => "�˵��Ҧ����ʬ��", "action" => "../../Update_Course.html" );
  %{$map{"print"}}	= ( "name" => "�C�L��ҳ�", "action" => "Print_Course.cgi" );
  %{$map{"print2"}}     = ( "name" => "�C�L��ҵ��G��", "action" => "Print_Course_pdf.cgi" );
  %{$map{"print3"}}     = ( "name" => "�˵����~���f�d��", "action" => "Print_Graduate_pdf.cgi" );
 
  my ($selection, $id, $password) = @_;
  
  if( $selection ne "update" ) {
    print qq(
      <FORM method=POST action="$map{$selection}{action}">
      <input type=hidden name="id" value="$id">
      <input type=hidden name="password" value="$password">
    );
  }else{
    print qq(
      <FORM method=GET action="$map{$selection}{action}">
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
        �ѩ� 92 �Ǧ~�ײĤG�Ǵ���Ҩt�Τ������~, �v�T���ɦP�ǥH�U��Ҭ����Q�h��:
        <PRE>@lines</PRE>
        �ЦP�ǩ󥻾Ǵ��Ĥ@���q��Ү�, �ۦ�[��H�W���, �H��o�u���z�ﶶ��.<BR>
        ps. �Y�P�Ǥw��W�Ǵ��[ñ��W�Ӭ��, �Щ��������i.
        <P>
        �����s��: 
        [ <A href="$explain_file" target=NEW>�q�⤤�߹D�p�Ҩ�</A> |
          <A href="$remedy_file" target=NEW>��Ҩt�ο��~�ɱϤ�k</A>
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
   print("<FONT color=RED>�Y�z�|���q�L��T��O����, �иԾ\\");
   print("<A href=\"http://infotest.ccu.edu.tw/reports/msg.php\" target=NEW>��T��O���礽�i</A></FONT><P>\n");
  }
}