#!/usr/local/bin/perl

print "Content-type: text/html","\n\n";

require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Select_Course.pm";

%Input = User_Input();
%Dept = Read_Dept($Input{dept_id});
$dept = $Input{dept};
$course_id = $Input{course_id};
$group = $Input{group};
%Course = Read_Course($dept,$course_id,$group,"", "");

#foreach $k (keys %Input) {
#  print("$k -> $Input{$k}<br>");
#}

print qq(
  <html><head><title>科目選課作業 - $Dept{cname}</title></head>
  <body background=".$GRAPH_URL."ccu-sbg.jpg>
  <center><h1>科目選課作業</h1></center>
  科目代碼: $course_id<br>
  科目班別: $group<br>
  科目名稱: $Course{cname}<br>
  科目限修: $Course{number_limit}<br>
  <hr>
);
if($Input{add_or_delete} eq "add")  {
  Show_Add_Table();
}elsif($Input{add_or_delete} eq "delete") {
  Show_Delete_Table();
}
############################################################################
sub Show_Delete_Table()
{
  print qq(
    <TABLE border=1>
      <TR><TD colspan=3>將以下學生退選</TD></TR>
      <TR><TD>學號</TD><TD>姓名</TD><TD>退選結果</TD></TR>
  );
  foreach $key (keys %Input) {
    if($Input{$key} eq "on") {
      %student = Read_Student($key);
#      Delete_Student_Course($key,$dept,$course_id,$group);
      print("<TR><TD>$key</TD><TD>$student{name}</TD><TD>$key,$dept,$course_id,$group</TD></TR>\n");
    }
  }
  print qq(
    </TABLE>
  );
}
################################################################################
sub Show_Add_Table()
{
  print qq(
    <TABLE border=1>
      <TR><TD colspan=4>替以下學生加選</TD></TR>
      <TR><TD>學號</TD><TD>姓名</TD><TD>學分歸屬</TD><TD>加選結果</TD></TR>
  );
  @Credit_table = CREDIT_TABLE();

  for($i=0; $i<50; $i++) {
    $id       = $i . "_id";
    $property = $i . "_property";
    if( $Input{$id} ne "" ) {
      %student = Read_Student($Input{$id});
#     Add_Student_Course($Input{$id},$dept,$course_id,$group,$Input{$property});
      print("<TR><TD>$Input{$id}</TD><TD>$student{name}</TD><TD>$Credit_table[$Input{$property}]</TD>
             <TD>$Input{$id},$dept,$course_id,$group,$Input{$property}</TD></TR>");
    }
  }
  print("</TABLE>");




}

