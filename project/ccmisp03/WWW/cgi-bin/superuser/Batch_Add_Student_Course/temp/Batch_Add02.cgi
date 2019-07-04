#!/usr/local/bin/perl 

print "Content-type: text/html","\n\n";
require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Dept.pm";

%Input = User_Input();
%Dept = Read_Dept($Input{dept_id});
$dept = $Input{dept};
($course_id,$group) = split(/_/,$Input{course_id});

#@Course = Find_All_Course( $Dept{id},"","history" );

print qq(
  <html><head><title>�P�Z�ǥͧ妸�[�� - $Dept{cname}</title></head>
  <body background=".$GRAPH_URL."ccu-sbg.jpg>
  <center>
  <h1>�P�Z�ǥͧ妸�[�� - �п�ܾǥ�</h1>
  <hr>
);

@student = Student_in_Course($dept, $course_id, $group, "history");
foreach $student (@student) {
  print("$student<br>\n");
}

