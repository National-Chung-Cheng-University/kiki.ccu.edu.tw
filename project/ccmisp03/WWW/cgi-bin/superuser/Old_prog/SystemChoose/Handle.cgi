#!/usr/local/bin/perl 

require "../../library/Reference.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."GetInput.pm";


HTML_Head("�d�ߨt�οz�ﵲ�G");
HTML();

sub HTML
{
 print "<body background=$GRAPH_URL"."ccu-sbg.jpg>\n";
 print "<form method=post action=Handle2.cgi>\n";
 print "<center><hr>\n";
 print "<font color=brown size=4>�п�ܱ���ݤ����</font><br>\n";
 print "<select name=course size=10>\n";
 Make_Options(); 
 print "</select><br>\n";
 print "<input type=submit name=submit value=��ݸӬ�ؿz�ﵲ�G>\n";
 print "</form>\n";
}


sub Make_Options
{
 my($dept,$count,$i,$flag);

 open(LOG,"< $BIN_PATH"."SystemChoose/Filter.Full");
  @Courses = <LOG>;
  chop(@Courses);
 close(LOG);

 foreach $course(@Courses)
 {
  ($dept,$id,$group,$temp) = split(/\s+/,$course);
  %course = Read_Course($dept,$id,$group);
  print "<option value=\"$dept $id $group $course{cname}\">[$id-$group]$course{cname}\n";
 }
}

sub HTML_Head
{
 my($title);
 ($title)=@_;
 print "Content-type: text/html


<html>
<head>
 <meta http-equiv=\"Content-Type\" content=\"text/html; charset=big5\">
 <title>$title</title>
</head>"; 
}