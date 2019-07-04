#!/usr/local/bin/perl
print "Content-type: text/html","\n\n";

require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Student.pm";
#require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Dept.pm";
my(%Input, %S, @Students);

%Input = User_Input();

%S = Read_All_Student_Data();
@Student = Find_All_Student();

if($Input{flag} eq "1" ) { $flag_string = "�]�t�s��"; }
if($Input{flag} eq "0" ) { $flag_string = "���]�t�s��"; }
if($Input{flag} eq "2" ) { $flag_string = "���]�t��s���¥�"; }
if($Input{flag} eq "3" ) { $flag_string = "�Ȭd�ߤj�ǳ��¥�"; }

$page = $Input{page};

### ��X����Ҿǥ� ###

my( @Student_Queue , $total );
$total = 0;
foreach $student (@Student)
{
 if( $Input{"flag"} eq "1" || ($Input{"flag"} eq "0" && $$S{$student}{grade} ne "1") 
     || ($Input{"flag"} eq "3" 
       && Is_Graduate($$S{$student}{dept}) eq "0" || $$S{$student}{grade} eq "1")
     || ($Input{"flag"} eq "4"
       && Is_Graduate($$S{$student}{dept}) eq "0" && $$S{$student}{grade} ne "1") 
   )
 {
  if( !(-e $STUDENT_PATH."$student") || (-z $STUDENT_PATH."$student") )
  { $Student_Queue[$total++] = $student; }
 }
}

if($Input{plaintext} eq "on") {
  Print_plaintext();
}else{
  Print_HTML();
}
##############################################################################
sub Print_plaintext()
{
  foreach $student (@Student_Queue) {
#    %student = Read_Student($student);
    %dept = Read_Dept($$S{$student}{dept});
    print("$$S{$student}{dept}  $dept{cname2}  $student  $$S{$student}{name}<br>\n");
#    print("$dept{id}  $dept{cname2}  $student  $student{name}<br>\n");
  }

}
##############################################################################

sub Print_HTML()
{
  $total_page = int($total/90);

  my($temp);
  $temp =$page +1;
  ###Print_Html_Header("�d�ߥ��׽ҾǥͦW��� $temp ��","$HTTP/ccu-sbg.jpg");
  ### Html Header ###
  print "
  <html>
  <head>
  <title>�d�ߥ��׽ҾǥͦW��� $temp ��- $flag_string</title>
  </head>
  <body background=".$GRAPH_URL."ccu-sbg.jpg>
  <center>
  <h1>";
  print "
  <img src=".$GRAPH_URL."open.jpg>
  </h1>
  <p>
  ";
  @Student_Queue=sort(@Student_Queue);

  $temp= $total_page+1;

  ## ��ܬ�ذ򥻸�� ##

  print "����ҤH��: $total , �@�� $temp ��<br>";

  if( ($page+1)*90 > $total )
  { $Limit= $total; }
  else { $Limit=($page+1)*90 ; }

  print "<table border=0 width=100%>";
  print "<tr>";

  for($i=($page*90); $i<$Limit ; $i++ )
  {
   if($i %30 ==0 )
   { print "<td valign=top><table border=1>\n"; }
 
   %dept = Read_Dept($$S{$Student_Queue[$i]}{dept});
   print "<tr><th align=left>$dept{cname2}</th>";
    $TTT = $$S{$Student_Queue[$i]}{dept};
    $TTTT = Is_Graduate($TTT);
   print "<td>$Student_Queue[$i],$TTT,$TTTT</td>\n
  <th align=left>$$S{$Student_Queue[$i]}{name}</th></tr>\n";
 
   if( ($i+1) % 30 ==0 || $i ==($Limit-1) )
   { print "</table></td>"; }
  }
  print "</tr></table>\n";

  if( $page ne "" && $page ne "0" )
  {  
   print "<form method=\"post\" action=\"Query_1.cgi\">\n";
   print "<input type=\"hidden\" name=\"flag\" value=\"$Input{'flag'}\">\n";
   $Temp=$Input{'page'}-1;
   print "<input type=\"hidden\" name=\"page\" value=\"$Temp\">\n";
   print "<input type=\"submit\" value=\"½�e�@��\">\n";
   print "</form>";
  }
  print "<br>";
  if( $total_page > $page )
  {
   print "<form method=\"post\" action=\"Query_1.cgi\">\n";
   print "<input type=\"hidden\" name=\"flag\" value=\"$Input{'flag'}\">\n"; 
   $Temp=$Input{'page'}+1;
   print "<input type=\"hidden\" name=\"page\" value=\"$Temp\">\n";
   print "<input type=\"submit\" value=\"½�U�@��\">\n";
   print "</form>";
  }

  print "<p><a href=\"Login.cgi\">�^��d�߭׽ҾǥͥD���</a><br>\n";
  print "<a href=\"http://www.ccu.edu.tw\">�^�����j�ǭ���</a>\n";
}

###### Sub-function Is_Graduate ######

sub Is_Graduate($dept)
{
 $dept =~ /(\d)$/;
 if( $1 ne "4" ) { return 1; }
 else { return 0; }
}