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
$course_id_now  = $Input{course_id_now};
$group_now      = $Input{course_group_now};

$property = 1;

print qq(
  <html><head><title>同班學生批次加選 - $Dept{cname}</title></head>
  <body background=GRAPH_URL/ccu-sbg.jpg>
  <center>
  <h1>同班學生批次加選 - 批次加選結果</h1>
  <hr>      
);

@student = Student_in_Course($dept, $course_id_last, $group_last, "last_semester");

$i=0;

foreach $student (@student) {
  print("加選: $student,$dept,$course_id_now,$group_now,$property<BR>\n");
  Add_Student_Course($student,$dept,$course_id_now,$group_now,$property);
}

print qq(
  加選完成!
);
