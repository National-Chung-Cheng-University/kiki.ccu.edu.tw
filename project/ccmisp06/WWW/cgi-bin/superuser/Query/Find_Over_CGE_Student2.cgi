#!/usr/local/bin/perl
##############################################################################
#####  找出所有選修太多通識的學生名單
#####  Updates:
#####   2012/09/27 Created by Nidalap :D~
#####   2014/03/18 新增依年級統計的表格 by Nidalap :D~

print "Content-type: text/html","\n\n";
print '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">';

require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."System_Settings.pm";
require $LIBRARY_PATH."Common_Utility.pm";

%Input=User_Input();
$password = $Input{password};
$pass_result = Check_SU_Password($password, "su", "su"); 
$year = $Input{year};
$term = $Input{term};

@course = Determine_All_Course();
$max_cge = $Input{max_cge};

foreach $cou (@course) {
#  print "checking $$cou{id} $$cou{group}...<BR>\n";
  @student = Student_in_Course($DEPT_CGE, $$cou{id}, $$cou{group}, $year, $term);
  next if( $$cou{id} !~ /^7[2-5]0....$/ );			###  只算通識第二到第五領域
  foreach $stu (@student) {
#    print "$stu  " . $$cou{id} . "<BR>\n";
    $stu_cge{$stu}++;
  }
#  if( $cge_count >= $max_cge ) {  Print_HTML($stu, $cge_count); }
}

print "<H1>列出 $year 學年度第 $term 學期所有選修通識超過 $max_cge 門課的學生</H1><HR>";
print "共 " . (keys %stu_cge) . " 名學生<BR>\n";

Print_Statistics();

print "以下是名單:<BR>\n";
print "<TABLE>"; 
print "<TR><TH>學號</TH><TH>姓名</TH><TH>年級</TH><TH>學系</TH><TH>選課數</TH></TR>";

foreach $stu (sort {$stu_cge{$b} <=> $stu_cge{$a}} keys %stu_cge) {

  if( $stu_cge{$stu} >= $max_cge ) {
    Print_Student_Data($stu, $stu_cge{$stu});
  }
#  print $stu . " -> " . $stu_cge{$stu} . "<BR>\n";
}


##############################################################################
sub Determine_All_Course()
{
  my @course;
  if( ($year == $YEAR) and ($term == $TERM ) ) {
    @course = Find_All_Course($DEPT_CGE, "");
  }else{
    @course = Find_All_Course($DEPT_CGE, "", $year, $term);
  }
  return @course;
}
##############################################################################

sub Print_Student_Data()
{
  my($id, $count) = @_;
  %stu = Read_Student($id);
  %dept = Read_Dept($stu{dept});
  
  $color = "RED";
  if($count <= 4) { $color = "#000"; }
  if($count == 5) { $color = "#400"; }
  if($count == 6) { $color = "#800"; }
  if($count >= 7) { $color = "#A00"; }

  print qq"
   <TR>
     <TD>$id</TD>
     <TD>$stu{name}</TD>
     <TD>$stu{grade}</TD>
     <TD>$dept{cname2}</TD>
     <TD><FONT color=$color>$count</FONT></TD>
   </TR>
  ";
}
################################################################################
sub Print_Statistics()
{
  my(%count, $total_count, $course_count);
  my(%by_grade);

  foreach $sid (keys %stu_cge) {
    %stu = Read_Student($sid);
    $course_count = $stu_cge{$sid};
    $count{$course_count}++;		###  依人數
    
#    print $sid . " - " . $stu{grade} . "<BR>\n";
    $by_grade{$course_count}{$stu{grade}}++;		###  依年級
    $total_count++
  }
  #####  依人數
  print "依人數統計<BR>\n";
  print "<TABLE border=1>";
  print "<TR><TH>&nbsp;</TH><TH>人數</TH><TH>比例</TH><TH>累積比例</TH></TR>";
  foreach $course_count (sort {$a <=> $b} keys %count) {
    $percent = sprintf("%.1f", 100 * $count{$course_count} / $total_count++);
    $percent2 += $percent;
    print qq'
      <TR>
        <TD>$course_count門通識</TD>
        <TD>$count{$course_count}</TD>
        <TD>$percent %</TD>
        <TD>$percent2 %</TD>
      </TR>
    ';
	
	
  }
  print "</TABLE><P>";
  
  #####  依年級
  print "依年級統計<BR>\n";
  print "<TABLE border=1>";
  print "<TR><TH>&nbsp;</TH><TH>大一</TH><TH>大二</TH><TH>大三</TH><TH>大四</TH></TR>";
  foreach $c_count (sort {$a <=> $b} keys %by_grade) {
    print "
	  <TR><TD>選修 $c_count 門課</TD>
        <TD>" . $by_grade{$c_count}{1} . "</TD>
		<TD>" . $by_grade{$c_count}{2} . "</TD>
		<TD>" . $by_grade{$c_count}{3} . "</TD>
		<TD>" . $by_grade{$c_count}{4} . "</TD>
	</TR>
    ";
  }  
  print "</TABLE><P>";
}