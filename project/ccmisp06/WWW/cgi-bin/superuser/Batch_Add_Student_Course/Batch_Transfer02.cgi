#!/usr/local/bin/perl 

print "Content-type: text/html","\n\n";
require "../../library/Reference.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Dept.pm";

%Input = User_Input();
%Dept = Read_Dept($Input{dept_id});
$dept = $Input{dept_id};
$course_id_from = $Input{course_id_from};
$group_from     = $Input{course_group_from};
$temp		= $Input{course_id_to};
($course_id_to, $group_to) = split(/_/, $temp);

$record_per_line = 5;

print qq(
  <html>
    <head>
	  $EXPIRE_META_TAG
	  <title>原班學生批次加選至另一班 - $Dept{cname}</title>
	</head>
  <body background=$GRAPH_URL/ccu-sbg.jpg>
  <center>
  <h1>原班學生批次加選至另一班 - 請確認學生名單</h1>
  <hr>
  <TABLE border=1>
    <TR>
      <TH colspan=2>科目系所: $dept</TH>
    </TR>
    <TR>
      <TD>從本學期科目班別</TD>
      <TD> $course_id_from _  $group_from</TD>
    </TR>
    <TR>
      <TD>到本學期科目班別</TD>
      <TD> $course_id_to _  $group_to</TD>
    </TR>
  </TABLE> 
      
);

@student = Student_in_Course($dept, $course_id_from, $group_from);

print qq(
  <CENTER>
    <TABLE border=1>
);
$i=0;
foreach $student (@student) {
  if( $i%$record_per_line == 0 ) {
    print("<TR>");
  }
  print("<TD>$student</TD>\n");
  if( ($i%$record_per_line == (record_per_line-1)) ) {
    print("</TR>");
  }
  $i++;
}
print qq(
    </TABLE>
  共有 $i 個學生<BR>
  加選科目屬性將採用原先學生所選之科目屬性<BR>
  <FORM action=Batch_Transfer03.cgi method=POST>
    <INPUT type=hidden name=dept_id value="$dept">
    <INPUT type=hidden name=course_id_to value="$course_id_to">
    <INPUT type=hidden name=course_group_to value="$group_to">
    <INPUT type=hidden name=course_id_from value="$course_id_from">
    <INPUT type=hidden name=course_group_from value="$group_from">
    <INPUT type=SUBMIT value="確認批次加選">
  </FORM>
);
