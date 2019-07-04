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
  <html><head><title>��ؿ�ҧ@�~ - $Dept{cname}</title></head>
  <body background=".$GRAPH_URL."ccu-sbg.jpg>
  <center><h1>��ؿ�ҧ@�~</h1></center>
  ��إN�X: $course_id<br>
  ��دZ�O: $group<br>
  ��ئW��: $Course{cname}<br>
  ��ح���: $Course{number_limit}<br>
  <hr>
  <FORM method=POST action="Course_Batch_Add04.cgi">
);
foreach $key (keys %Input) {
  print("<INPUT type=hidden name=$key value=$Input{$key}>\n");
}

if($Input{add_or_delete} eq "add")  {
  Show_Add_Table();
}elsif($Input{add_or_delete} eq "delete") {
  Show_Delete_Table();
}
print qq(
  </FORM>
);
###############################################################################
sub Show_Delete_Table()
{
  print qq(
    <TABLE border=1>
      <TR><TD colspan=2>�N�H�U�ǥͰh��</TD></TR>
      <TR><TD>�Ǹ�</TD><TD>�m�W</TD></TR>
  );
  foreach $key (keys %Input) {
    if($Input{$key} eq "on") {
      %student = Read_Student($key);
      print("<TR><TD>$key</TD><TD>$student{name}</TD></TR>\n");
    }
  }
  print qq(
    </TABLE>
    <INPUT type=submit value="�T�{�h��">
  );
}
###############################################################################
sub Show_Add_Table()
{
  print qq(
    <TABLE border=1>
      <TR><TD colspan=3>���H�U�ǥͥ[��</TD></TR>
      <TR><TD>�Ǹ�</TD><TD>�m�W</TD><TD>�Ǥ��k��</TD></TR>
  );
  @Credit_table = CREDIT_TABLE();  
  
  for($i=0; $i<50; $i++) {
    $id       = $i . "_id";
    $property = $i . "_property"; 
    if( $Input{$id} ne "" ) {
      %student = Read_Student($Input{$id});
      $error_flag++   if($student{name} eq "");
      $error_flag++   if($Input{$property} == 0);
      print("<TR><TD>$Input{$id}</TD><TD>$student{name}</TD><TD>$Credit_table[$Input{$property}]</TD></TR>");
    }
  }
  print("</TABLE>");
  if( $error_flag > 0 ) {
    print("<FONT color=RED>�H�W��Ʀ@�� $error_flag �������D(�Ǹ����~�ξǤ��k��)!!");
  }
  print qq(
    <p><INPUT type=submit value="�T�{�[��">
  );


};


