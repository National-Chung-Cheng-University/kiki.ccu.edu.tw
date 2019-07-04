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
  <FORM method=POST action="Course_Batch_Add04.cgi">
);
foreach $key (sort keys %Input) {
#  print("$key: $Input{$key}<BR>\n");
  print("<INPUT type=hidden name=$key value=$Input{$key}>\n");
}

if($Input{add_or_delete} eq "add1")  {
  Show_Add_Table1();
}elsif($Input{add_or_delete} eq "add2")  {
  Show_Add_Table2();
}elsif($Input{add_or_delete} eq "delete") {
  Show_Delete_Table();
}else{
  print("請選擇要替哪一邊的名單加選!");
  exit();
}
print qq(
  </FORM>
);
###############################################################################
sub Show_Delete_Table()
{
  print qq(
    <TABLE border=1>
      <TR><TD colspan=2>將以下學生退選</TD></TR>
      <TR><TD>學號</TD><TD>姓名</TD></TR>
  );
  foreach $key (keys %Input) {
    if($Input{$key} eq "on") {
      %student = Read_Student($key);
      print("<TR><TD>$key</TD><TD>$student{name}</TD></TR>\n");
    }
  }
  print qq(
    </TABLE>
    <INPUT type=submit value="確認退選">
  );
}
###############################################################################

sub Show_Add_Table1()
{
  my $count;
  print qq(
    <TABLE border=1>
      <TR><TD colspan=3>替以下學生加選</TD></TR>
      <TR><TD>學號</TD><TD>姓名</TD><TD>學分歸屬</TD></TR>
  );
  @Credit_table = CREDIT_TABLE();  
  
  for($i=0; $i<50; $i++) {
    $id       = $i . "_id";
    $property = $i . "_property"; 
    if( $Input{$id} ne "" ) {
      %student = Read_Student($Input{$id});
      $error_flag++   if($student{name} eq "");
      $error_flag++   if($Input{$property} == 0);
      if( ($Input{$id} !~ /^4/) and ($dept =~ /4$/) and ($Input{$property} != 8) ) {
        $error_flag++;
      }
      print("<TR><TD>$Input{$id}</TD><TD>$student{name}</TD><TD>$Credit_table[$Input{$property}]</TD></TR>");
    }else{
      $count = $i;
      last;
    }
  }
  print("</TABLE>");
  if( $error_flag > 0 ) {
    print("<FONT color=RED>以上資料共有 $error_flag 筆有問題(學號錯誤或學分歸屬)!!");
  }
  print qq(
    <INPUT type=hidden name=maxcount value=$count>
    <p><INPUT type=submit value="確認加選">
  );
};
###############################################################################
sub Show_Add_Table2()
{
  print qq(
    <TABLE border=1>
      <TR><TD colspan=3>替以下學生加選</TD></TR>
      <TR><TD>學號</TD><TD>姓名</TD><TD>學分歸屬</TD></TR>
  );

#  print("$Input{id_list}<P>\n");

  my(@student_id) = split(/\s+/, $Input{id_list});
  my $count = @student_id;

  my $i = 0;
  foreach $id (@student_id) {
    %student = Read_Student($id);
    $error_flag++   if($student{name} eq "");

    $id_id    = $i . "_id";
    $property = $i . "_property";
    print("<INPUT type=hidden name=$id_id value=$id>");
    if( $i>=50 ) {					###  add1只做到 50 筆資料
      print("<INPUT type=hidden name=$property value=$Input{property}>");
    }
    print("<TR><TD>$id</TD><TD>$student{name}</TD><TD>$PROPERTY_TABLE2{$Input{property}}</TD></TR>");
    $i++
  }
  print("</TABLE>");
  print("<INPUT type=hidden name=maxcount value=$count>");
  print("共 $count 筆資料<BR>");
  if( $error_flag > 0 ) {
    print("<FONT color=RED>以上資料共有 $error_flag 筆有問題(學號錯誤或學分歸屬)!!");
  }
  print qq(
    <p><INPUT type=submit value="確認加選">
  );
}


