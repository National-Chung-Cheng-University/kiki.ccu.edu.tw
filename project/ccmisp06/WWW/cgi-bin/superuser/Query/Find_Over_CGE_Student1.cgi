#!/usr/local/bin/perl
##############################################################################
#####  找出所有選修太多通識的學生名單
#####  Updates:
#####   2012/09/27 Created by Nidalap :D~

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
my(%S, @Students);

%Input=User_Input();
$password = $Input{password};
$pass_result = Check_SU_Password($password, "su", "su");

$YEAR_TERM_SELECT = Make_Year_Term_Select_HTML();
$MAX_CGE_SELECT   = Make_Max_CGE_Select_HTML();

print $EXPIRE_META_TAG2;
print qq{
  <H1>列出所有選修通識超過 $MAX_CGE 門課的學生</H1><HR>
  <FORM action="Find_Over_CGE_Student2.cgi" method="POST">
    顯示資料學年學期：$YEAR_TERM_SELECT <P>
    顯示選修超過 $MAX_CGE_SELECT (含)通識課的學生名單<P>
    <INPUT type="hidden" name="password" value="$password">
    <INPUT type="submit" value="檢視名單">
  </FORM>
};

####################################
sub Make_Year_Term_Select_HTML()
{
  my $html;
  my $year_start = $YEAR;
  my $year_end = 100;
  #my @years = ("104", "103", "102", "101", "100", "99", "98", "97");
  #print ("YEAR = $YEAR<BR>\n");
  
  for( $y=$year_start, $i=0; $y>=$year_end; $y--, $i++ ) {
    #print("y = $y<BR>\n");
	$years[$i] = $y;
  }
  
  
  $html = "<SELECT name='year'>";
  foreach $year (@years) {
    $html .= "  <OPTION value='$year'>$year\n";
  }
  $html .= "</SELECT>";
  
  if( $TERM == 1 )  {
    $default_term[1] = "selected";
  }else{
    $default_term[2] = "selected";
  }
  
  $html .= "<SELECT name='term'>";
  $html .= "  <OPTION value=1 " . $default_term[1] . ">1";
  $html .= "  <OPTION value=2 " . $default_term[2] . ">2";
  $html .= "</SELECT>";
  
  return $html;
}
####################################
sub Make_Max_CGE_Select_HTML()
{
  my $html;
  my @credits = (1..9);
  
  $html = "<SELECT name='max_cge'>";
  foreach $c (@credits) {
    $html .= "  <OPTION value='$c'>$c\n";
  }
  $html .= "</SELECT>";
  return $html;
}


