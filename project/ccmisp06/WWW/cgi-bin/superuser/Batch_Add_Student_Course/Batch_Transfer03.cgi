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
$course_id_to  = $Input{course_id_to};
$group_to      = $Input{course_group_to};

$property = 1;

print qq(
  <html><head><title>原班學生批次加選至另一班 - $Dept{cname}</title></head>
  <body background=GRAPH_URL/ccu-sbg.jpg>
  <center>
  <h1>原班學生批次加選至另一班 - 批次加選結果</h1>
  <hr>      
);

@student = Student_in_Course($dept, $course_id_from, $group_from);

$i=0;

foreach $student (@student) {
  @cou = Course_of_Student($student);
  foreach $cou (@cou) {
#    print $$cou{id} . " - " .  $$cou{group} . "<BR>\n";
    if( ($$cou{id} eq $course_id_from) and ($$cou{group} eq $group_from) ) {
      $property = $$cou{property};
      last;
    }
  }
  
  print("加選: $student,$dept,$course_id_to,$group_to,$property<BR>\n");
  Add_Student_Course($student,$dept,$course_id_to,$group_to,$property);
}

print qq(
  加選完成!
);
