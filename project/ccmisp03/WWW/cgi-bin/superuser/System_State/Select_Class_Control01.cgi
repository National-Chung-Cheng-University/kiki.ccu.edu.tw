#!/usr/local/bin/perl 

####    require these .pm modual    ####
require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
########################################

######### Main Program Here #########
%Input=User_Input();

#
#  Check Password
#

$GradeMap[1]="�j�ǳ��@�~��";
$GradeMap[2]="�j�ǳ��G�~��";
$GradeMap[3]="�j�ǳ��T�~��";
$GradeMap[4]="�j�ǳ��|�~��";
$GradeMap[5]="��s�Ҥ@�~��";
$GradeMap[6]="��s�ҤG�~�ťH�W�t�դh�Z";

$DATA="";
$DATA=READ_SELECT_DEPT();
$TIME_MAP="";
$TIME_MAP=READ_TIME_MAP();

CREAT_HTML($DATA, $TIME_MAP);
######## Sub Program Bellow ##########
######################################
sub READ_TIME_MAP
{
  my($Data)="";
  my($count)=1;

  $Data=$Data."<table border=0 width=800>\n";
  $Data=$Data."<tr><th align=left>\n";
  $Data=$Data."<input type=radio name=TimeClass value=0 checked>�����]�w�]�ȡ^\n";
  $Data=$Data."</th></tr>\n";

  $FileName=$REFERENCE_PATH."TimeMap/T".$count.".map";
  while( open(FILE,"<$FileName") ){
    my(@the_TimeClass)=<FILE>;
    $Data=$Data."<tr><th align=left>\n";
   $Data=$Data."<input type=radio name=TimeClass value=".$count.">��".$count."�ɬq";
    foreach $t(@the_TimeClass){
      $t=~s/\n//;
      my($ST, $ET)=split(/\s+/,$t);
      my($SH)=$ST/100;   my($SM)=$ST%100;
      my($EH)=$ET/100;   my($EM)=$ET%100;
      $Data=$Data."[".$SH.":".$SM."-->".$EH.":".$EM."]";
    }
    $Data=$Data."</th></tr>";
    $count++;
    $FileName=$REFERENCE_PATH."/TimeMap/T".$count.".map";
  }

  $Data=$Data."</table>\n";
  return($Data);
}
sub READ_SELECT_DEPT
{
  my(@Dept);
  my($Data)="";

  $Data=$Data."<center>\n";
  $Data=$Data."<input type=hidden name=grade value=$Input{grade}>\n";
  $Data=$Data."<font size=4>�i".$GradeMap[$Input{grade}]."�j</font><br>";
  $Data=$Data."<table width=800>\n";
  $Data=$Data."<tr>\n";

  @Dept=split(/\*:::\*/,$Input{dept});
  my($count)=1;
  foreach $dept(@Dept){
    %the_Dept=Read_Dept($dept);
    $Data=$Data."<th><font size=2>";
    $Data=$Data."<input type=hidden name=".$dept." value=".$dept.">";
#   $Data=$Data."<input type=hidden name="."dept"." value=".$dept.">";
    $Data=$Data.$the_Dept{cname2};
    $Data=$Data."</font></th>\n";
    if($count%5 == 0){
      $Data=$Data."</tr><tr>";
    }
    $count++;
  }

  $Data=$Data."</tr>\n";
  $Data=$Data."</table>\n";
  $Data=$Data."</center>\n";
  return($Data);
}
sub CREAT_HTML
{
my($Data, $TimeMap)=@_;
my($Next_Action)="Select_Class_Control02.cgi";

print << "End_of_HTML"
Content-type: text/html


<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <title>�ǥͿ�Үɵ{�]�w</title>
</head>
<body bgcolor=white text=#666666>
<center>
<form action="$Next_Action" method=post>
<font size=5 color=#777777>�ǥͿ�Үɵ{�]�w (Step2)</font>
<hr size=1>
$TimeMap
<hr size=1 width=800>
$Data
<hr size=1>
<table border=0 width=800>
<tr>
  <th align=left>
<font size=3 color=#aa5555><input type=submit value=�T�w></font>
<font size=3 color=#aa5555><input type=reset value=���m></font>
  </th>
</tr>
  <th>&nbsp</th>
  <th width=760 align=left>
  <font size=3>
  </font>
  </th>
</table>
</form>
</center>
</body>
</html>
End_of_HTML
}
#######################################

