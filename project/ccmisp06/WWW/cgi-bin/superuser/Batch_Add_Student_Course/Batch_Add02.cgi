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
$course_id_last = $Input{course_id_last};
$group_last     = $Input{course_group_last};
$temp		= $Input{course_id_now};
($course_id_now, $group_now) = split(/_/, $temp);

$record_per_line = 5;

print qq(
  <html>
    <head>
	  <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
      <title>同班學生批次加選 - $Dept{cname}</title>
	</head>
  <body background=$GRAPH_URL/ccu-sbg.jpg>
  <center>
  <h1>同班學生批次加選 - 請確認學生名單</h1>
  <hr>
  <TABLE border=1>
    <TR>
      <TH colspan=2>科目系所: $dept</TH>
    </TR>
    <TR>
      <TD>上學期科目班別</TD>
      <TD> $course_id_last _  $group_last</TD>
    </TR>
    <TR>
      <TD>本學期科目班別</TD>
      <TD> $course_id_now _  $group_now</TD>
    </TR>
  </TABLE> 
      
);

@student = Student_in_Course($dept, $course_id_last, $group_last, "last_semester");

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
  科目屬性固定為 "必修"<BR>
  <FORM action=Batch_Add03.cgi method=POST>
    <INPUT type=hidden name=dept_id value="$dept">
    <INPUT type=hidden name=course_id_now value="$course_id_now">
    <INPUT type=hidden name=course_group_now value="$group_now">
    <INPUT type=hidden name=course_id_last value="$course_id_last">
    <INPUT type=hidden name=course_group_last value="$group_last">
    <INPUT type=SUBMIT value="確認批次加選">
  </FORM>
);
