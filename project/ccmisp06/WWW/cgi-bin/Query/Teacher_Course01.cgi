#!/usr/local/bin/perl
############################################################################
#####  Teacher_Course01.cgi
#####  教師查詢當學期一般生與碩士在職專班授課明細
#####  此功能不從教師專業系統連結過來，因為該系統不給兼任教師使用。
#####  Updates: 
#####	2016/01/12 Created by Nidalap :D~
############################################################################
print "Content-type: text/html","\n\n";

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Select_Course.pm";
require $LIBRARY_PATH . "Common_Utility.pm";
require $LIBRARY_PATH . "System_Settings.pm";

%Input = User_Input();
#foreach $key (keys %Input) {
#  print("$key -> $Input{$key}<BR>\n");
#}

$sel_semester_html = Create_Select_Semester_HTML();
#$sel_semester_html = "";

print qq(
    <html>
      <head>
        $EXPIRE_META_TAG
        <title>教師查詢當學期授課明細</title>
      </head>
      <body background=$GRAPH_URL/ccu-sbg.jpg>
        <center>
         <img src=$GRAPH_URL/open.jpg>
		 <H1>教師查詢當學期授課明細</H1>
		 <P>
		 <FORM action='Teacher_Course02.php' method='POST'>
           請輸入您的身分證號：<INPUT type='password' name='teacher_id'><P>
		   $sel_semester_html
		   <INPUT type='submit' value='查詢當學期授課明細'>
		 </FORM>
	  </BODY>
	</HTML>
);

######################################################################################
sub Create_Select_Semester_HTML
{
  $MAX_SEMESTERS = 3;
  my $html = "";
  
  #($year, $term) = Last_Semester(1);
  %system_settings = Read_System_Settings();
  if( $system_settings{redirect_to_query} == 1 ) {			###  如果系統目前正在開新學期的課
    $selected1 = "";							###    那就預設選擇上學期資料
    $selected2 = "selected=\"selected\"";
  }else{
    $selected1 = "selected=\"selected\"";
    $selected2 = "";
  }

  $html .= "<SELECT name='last_semester'>";
  
  for( $i=0; $i<$MAX_SEMESTERS; $i++ ) {
    ($year, $term) = Last_Semester($i);
    $html .= "<OPTION value=$i ";
    $html .=  "SELECTED "  if( $i==0 );
    $html .=  ">$year 學年度第 $term 學期資料</OPTION>\n";
  }
  
  $html .= "</SELECT><P>";
  return $html;
  
}
