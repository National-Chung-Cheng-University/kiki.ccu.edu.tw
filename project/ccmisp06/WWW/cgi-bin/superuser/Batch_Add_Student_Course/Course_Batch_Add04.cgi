#!/usr/local/bin/perl

print "Content-type: text/html","\n\n";

require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Common_Utility.pm";    
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Select_Course.pm";
require $LIBRARY_PATH."System_Settings.pm";

%Input = User_Input();
%Dept = Read_Dept($Input{dept_id});
$dept = $Input{dept};
$course_id = $Input{course_id};
$group = $Input{group};
%Course = Read_Course($dept,$course_id,$group,"", "");
$SUPERUSER = 1;

#foreach $k (sort keys %Input) {
#  print("$k -> $Input{$k}<br>");
#}

print qq(
  <html>
    <head>
      $EXPIRE_META_TAG
      <title>科目批次選課作業 - $Dept{cname}</title>
    </head> 
    <body background="$GRAPH_URL/ccu-sbg.jpg">
      <center>
      <img src="$GRAPH_URL/open.jpg"><p>

  <center><h1>科目選課作業</h1></center>
  科目代碼: $course_id<br>
  科目班別: $group<br>
  科目名稱: $Course{cname}<br>
  科目限修: $Course{number_limit}<br>
  <hr>
);
if($Input{add_or_delete} =~ /add/)  {
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
      Delete_Student_Course($key,$dept,$course_id,$group);
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
  my($id, $property, $i);
  print qq(
    <TABLE border=1>
      <TR><TD colspan=4>替以下學生加選</TD></TR>
      <TR><TD>學號</TD><TD>姓名</TD><TD>學分歸屬</TD><TD>加選結果</TD></TR>
  );
  @Credit_table = CREDIT_TABLE();

#  if($Input{add_or_delete} eq "add2")  {
#    my(@student_id) = split(/\s+/, $Input{id_list});
#    my $maxcount = @student_id;
#  }else{
#    $maxcount=50;
#  }

  $maxcount = $Input{maxcount};
#  print("max = $maxcount<BR>\n");
  for($i=0; $i<$maxcount; $i++) {
    $id       = $i . "_id";
    $property = $i . "_property";
        
#    print("Input{$id} from $Input{$id} to ");
    if( $Input{add_or_delete} eq "add1" ) {
      $Input{$id} =~ /^(\d+)/;
      $Input{$id} = $1;
    }else{
      $Input{$id} =~ /(\d+)$/;
      $Input{$id} = $1;
    }
#    print("$Input{$id}<BR>\n");

    if( $Input{$id} ne "" ) {
      %student = Read_Student($Input{$id});
      $add_result = Add_Student_Course($Input{$id},$dept,$course_id,$group,$Input{$property});
      if( $add_result == 1 ) {
        $add_result = "成功!";
      }else{
        $add_result = "<FONT color=RED>失敗!可能是因為該學生早已選過此課程</FONT>";
      }
      print("<TR><TD>$Input{$id}</TD><TD>$student{name}</TD><TD>$Credit_table[$Input{$property}]</TD>
             <TD>$Input{$id},$dept,$course_id,$group,$Input{$property} : $add_result</TD></TR>");
    }
  }
  print("</TABLE>");
}

################################################################################
