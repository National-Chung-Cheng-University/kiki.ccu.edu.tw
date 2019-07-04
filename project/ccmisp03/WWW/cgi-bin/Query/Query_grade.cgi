#!/usr/local/bin/perl
print "Content-type: text/html","\n\n";

#########################################################################
#####   Query.cgi 
#####   ���Ѿǥͬd�߾��~�Υ��Ǵ������Z
#####   Date: Jun 22,2000
#####   Coder: Nidalap
#####   Version: 2.0
#########################################################################
require "../../../LIB/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Course.pm";
require $LIBRARY_PATH . "Student.pm";
require $LIBRARY_PATH . "Password.pm";
require $LIBRARY_PATH . "Error_Message.pm";

%INPUT = User_Input();

#foreach $k (keys %INPUT) {
#  print("$k --> $INPUT{$k}<br>\n");
#}

$id = $INPUT{"id"};
$service = $INPUT{"service"};
$password = $INPUT{"password"};

%student = Read_Student($id);
%dept = Read_Dept($student{dept});

$crypt_salt = Read_Crypt_Salt($id, "student");
$password = Crypt($password, $crypt_salt);
Check_Student_Password($id, $password);

#&Check_For_Valid_Input($id,$dept);
#$correct_password = &Find_Password($dept,$id);
#&Check_For_Correct_Password($password,$id);

#require "Course_cname.pm";
#%Course_cname = &Find_Course_Cname();


@grades = &Get_Student_Grades($id);
%order = &Get_Student_Orders($id);

#foreach $grades (@grades) {
#  print("$$grades{cid}, $$grades{grp}, $$grades{grade}<br>\n");
#}

if   ($id =~ /^4/) {  $identity = "�j�ǳ�";  }
elsif($id =~ /^6/) {  $identity = "�Ӥh�Z";  }
elsif($id =~ /^8/) {  $identity = "�դh�Z";  }
elsif($id =~ /^5/) {  $identity = "�Ӥh�M�Z";  }
else               {  $identity = "";  }

#$service == "���Ǵ����Z�d��";

if( ($service eq "���~���Z�d��") or ($service eq "���צ��Z�d��") ) {
  &Show_Output("History");
}elsif($service eq "���Ǵ����Z�d��") {
  &Show_Output("Current");
}

#########################################################################
#####  �N�̫᪺�Ҧ���ƥH HTML �ƪ� Show �X
#####  �� Table ���  &Print_Grade_Tables_Current() ��
#####                 &Print_Grade_Tables_History() �Өq
#########################################################################
sub Show_Output()
{
  my($service) = @_;
  my($i);
  $i = 0;

  print qq(
    <HTML>
      <HEAD><TITLE>��ߤ����j��  �ǥͦ��Z�d�ߨt��</TITLE></HEAD>
      <BODY background=$GRAPH_URL/bk.jpg>
        <Center>
          <H1>��ߤ����j��  �ǥͦ��Z�d�ߨt��</H1><HR>
 
          <table border=1 width=75%>
            <TR><th bgcolor=YELLOW>�m�W:$student{name}</th>
               <th bgcolor=YELLOW>�Ǹ�:$id</th>
               <th bgcolor=YELLOW>�t�ҦW��: $dept{cname} $identity</th>
          </table>
  );

  &Print_Grade_Tables_Current() if($service eq "Current");
  &Print_Grade_Tables_History() if( ($service eq "History") or
                                    ($service eq "Summer" )    );
}
#########################################################################
#####  Show �X�Ҧ������Z�ά�� Table
#########################################################################
sub Print_Grade_Tables_History()
{
  my($last_year, $last_sem, $term);

  for($i=0; $grades[$i]{year} ne ""; $i++) {
#    %course = Read_History_Course($grades[$i]{cid}, $grades[$i]{grp});
    $new_table = "FALSE";
    if( ($last_year ne $grades[$i]{year}) or ($last_sem ne $grades[$i]{term}) ) {
       $new_table = "TRUE";
    }
    if( $new_table eq "TRUE" ) {
       if( $grades[$i]{term} == 3 ) {
         $term = "����";
       }else{
         $term = "��" . $grades[$i]{term} . "�Ǵ�";
       }
       print("</table><P>");
       print("$grades[$i]{year}�Ǧ~$term");
       print("(�� $order{$grades[$i]{year}}{$grades[$i]{term}} �W)<BR>");
       print("<table border=1 width=75%>");
       print("<tr><th>��إN�X</th><th>�Z�O</th>
                  <th>��ئW��</th><TH>��ҾǤ��ݩ�</TH><th>�Ǥ�</th><th>���Z</th>");
    }
    $grades[$i]{grade} = "I" if($grades[$i]{grade} eq "");
    print("<tr>");
    print("<td>$grades[$i]{cid}</td>");
    print("<td>$grades[$i]{grp}</td>");
    print("<td>$grades[$i]{course_cname}</td>");
    print("<td align=CENTER>$PROPERTY_TABLE2{$grades[$i]{course_attr}}</TD>");
    print("<td>$grades[$i]{credit}</td>");
    print("<td>$grades[$i]{grade}</td>");
#    print("<td></td>");
    $last_year = $grades[$i]{year};
    $last_sem  = $grades[$i]{term};
  }
  print("</table>");
}

############################################################################
sub Print_Grade_Tables_Current()
{
  print("$grades[$i]{year}�Ǧ~��$grades[$i]{term}�Ǵ�");
  print("(�� $order{$grades[$i]{year}}{$grades[$i]{term}} �W)<BR>");
  print("<table border=1 width=75%>");
  print("<tr><th>��إN�X</th><th>�Z�O</th>
             <th>��ئW��</th><TH>��ҾǤ��ݩ�</TH><th>�Ǥ�</th><th>���Z</th>");
  for($i=0; $grades[$i]{year} ne ""; $i++) {
#     %course = Read_History_Course($grades[$i]{cid}, $grades[$i]{grp});
     $grades[$i]{grade} = "I" if($grades[$i]{grade} eq "");
     print("<tr>");
     print("<td>$grades[$i]{cid}</td>");
     print("<td>$grades[$i]{grp}</td>");
     print("<td>$grades[$i]{course_cname}</td>");
     print("<td align=CENTER>$PROPERTY_TABLE2{$grades[$i]{course_attr}}</TD>");
     print("<td>$grades[$i]{credit}</td>");
     print("<td>$grades[$i]{grade}</td>");

#     print("<td></td>");
  }
  print("</table>");
}
############################################################################
#####  ��Get_Student_Grades()Ū�X���X�ǥͦ��Z(�@��@�檺)
#####  ���X�ǥͪ����Z
############################################################################
#sub Read_Out_Grades()
#{
#  my(@lines, $i, $junk);
#  @lines = @_;
#
#  $i = 0;
#  foreach $line (@lines) {
#    $line =~ s/\n//;
#    ($junk,$year[$i],$sem[$i],$course_id[$i],$grp[$i],
#               $course_time[$i],$course_attr[$i],$grade[$i],$credit[$i]) = split(/\t/,$line);
##    print("$line ---> $junk<br>\n");
##    print("$course_id[$i] $grade[$i] <br>\n");
##    if($grade[$i] eq "
#    if( (($course_time[$i] eq '1')or($course_time[$i] eq '2'))  and
#        (($course_attr[$i] eq '1')or($course_attr[$i] eq 'A'))    )  {
#      if   ( $grade[$i] == "4" )  {  $grade[$i] = "��";  }
#      elsif( $grade[$i] == "3" )  {  $grade[$i] = "�A";  }
#      elsif( $grade[$i] == "2" )  {  $grade[$i] = "��";  }
#      elsif( $grade[$i] == "1" )  {  $grade[$i] = "�B";  }
#      elsif( $grade[$i] == "0" )  {  $grade[$i] = "��";  }
#    }
#    $i++;
#  }
#
#}
#
############################################################################
sub Check_For_Correct_Password()
{ 
  my($password,$id) = @_;
  my($su_password_file, $su_password);

  $salt = Read_Crypt_Salt($id, "student");
  $password = Crypt($password, $salt);

  Check_Student_Password($id, $password);

#  return if($password eq $su_password);
#  return if($password eq $correct_password);    
  
#  &Error_Message("PASSWORD");
}

############################################################################
#####  ���ɮ�Ū�X�ǥͦ��Z����T

sub Get_Student_Grades()
{
  my($id) = @_;
  my($grade_file,@grades,@id_grades, @line);
  my($tmp, $course_time, $course_attr, @GRA, $i);
  my $tmpfile = "/tmp/" . $id . ".grade";

  if($service eq "���~���Z�d��") {
     $grade_file = $DATA_PATH . "Grade/all.txt";
  }elsif($service eq "���Ǵ����Z�d��") {
     $grade_file = $DATA_PATH . "Grade/now.txt";
  }elsif($service eq "���צ��Z�d��") {
     $grade_file = $DATA_PATH . "Grade/summer.txt";
  }  

  system("grep $id $grade_file > $tmpfile");

  open(TMP, $tmpfile);
  @line = <TMP>;
  close(TMP);
  unlink $tmpfile;

#  open(GRADE_FILE,$grade_file) or die("Cannot open file $grade_file!\n");
#  @grades = <GRADE_FILE>;
#  close(GRADE_FILE);
#  foreach $grade (@grades) {
#    if($grade =~ $id) {
#      push(@line,$grade);
#    }
#  }  
  for($i=0; defined($line[$i]); $i++) {
    ($tmp, $GRA[$i]{year}, $GRA[$i]{term}, $GRA[$i]{cid}, $GRA[$i]{grp},
     $GRA[$i]{course_time}, $GRA[$i]{course_attr}, $GRA[$i]{grade}, $GRA[$i]{credit}, $GRA[$i]{course_cname} )
    = split(/\t/,$line[$i]);

    if( $GRA[$i]{course_attr} == "9" )  {             ###  �ݩ���==9, �O�����
      $GRA[$i]{grade} = "���";
    }
    ###  ���F�ީʥH�~, �w�g�S�����Ĩ�F. �n�X�~�e���Ʊ�, �{�b�o�{.  2008/02/13 Nidalap :D~
#    if( (($GRA[$i]{course_time} eq '1')or($GRA[$i]{course_time} eq '2'))  and
#        (($GRA[$i]{course_attr} eq '1')or($GRA[$i]{course_attr} eq 'A'))    )  {
#      if   ( $GRA[$i]{grade} eq "4" )  {  $GRA[$i]{grade} = "��";  }
#      elsif( $GRA[$i]{grade} eq "3" )  {  $GRA[$i]{grade} = "�A";  }
#      elsif( $GRA[$i]{grade} eq "2" )  {  $GRA[$i]{grade} = "��";  }
#      elsif( $GRA[$i]{grade} eq "1" )  {  $GRA[$i]{grade} = "�B";  }
#      elsif( $GRA[$i]{grade} eq "0" )  {  $GRA[$i]{grade} = "��";  }
#    }
  } 
  return(@GRA);
}
############################################################################
#####  Get_Student_Orders
#####  ���ɮ�Ū���ǥͪ��C�Ǵ��ƦW
#####  Added Mar/16,2001
#####  Nidalap :D~
############################################################################
sub Get_Student_Orders()
{
  my($input_id) = @_;
  my(@lines, $year, $sem, $id, $order, %order );
  
  $order_file = $DATA_PATH . "Grade/std_orders.txt";
  open(ORDER_FILE, $order_file) or print("Error opening file $order_file!\n");
  
  @lines = <ORDER_FILE>;
  close(ORDER_FILE);
  foreach $line (@lines) {
    $line =~ s/\n//;
    ($year, $sem, $id, $order) = split(/\s+/, $line);
    if($id eq $input_id) {
      $order{$year}{$sem} = $order;
    }
  }
  return(%order);  
}
############################################################################

sub Check_For_Valid_Input()
{
  my($id,$dept,$message) = @_;
  if($dept eq "") {
     $message = "1";
     &Error_Message_($message);
  }
}
############################################################################
sub Error_Message_()
{
  my($message) = @_;
  if($message eq "1") {
    $message = "�t�Χ䤣��z���Ǹ�, �нT�{�Ǹ��S������!"; 
  }elsif($message eq "2") {
    $message = "�z�èS����J�Ǹ�, �Э��s��J!";
  }elsif($message eq "PASSWORD") {
    $message = "�z���K�X�����T, �Э��s��J!";
  }

  print("<HTML><BODY><CENTER><H1>�n�J���~</H1><hr>");
  print("$message");
  print qq (<p><A href="http://kiki.ccu.edu.tw/~ccmisp04/">�^�W��</A>);    
  exit(1);
}

############################################################################
