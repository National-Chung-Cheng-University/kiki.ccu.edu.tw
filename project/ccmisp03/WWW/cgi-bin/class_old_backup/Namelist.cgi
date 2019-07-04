#!/usr/local/bin/perl

#########################################################################
#####  Namelist.cgi
#####  (��u�t�ݨD)
#####  ������إN�X�ίZ�O, ���͸ӯZ�׽ҦW�����,
#####  �ñN��Ʊa��php�{��(��u�t�}�o)
#####  Coder: Nidalap
#####  Last Update: Aug 22, 2001
#####  2002/02/20  �̷ӻݨD�[�J�Ѽ� prog ���P�_ (Nidalap :D~)
#########################################################################

print("Content-type:text/html\n\n");

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Error_Message.pm";

Read_All_Student_Data();
%Input    = User_Input();
if( $Input{prog} eq "" ) {
  $target_prog = "http://" . $Input{host} . "/php/TSImportInsert2.php";
}else{
  $target_prog = "http://" . $Input{host} . $Input{prog};
}
$bg = "http://" . $Input{host} . "/images/img/bg.gif";

if( $Input{version} eq "E" ) {
  $TITLE		= "Import Student Data";
  $NAME_TITLE		= "ID&nbsp;&nbsp;Name";
  $SUBMIT_TITLE		= "Confirm";
}else{
  $TITLE		= "�פJ��Ҿǥ͸��";
  $NAME_TITLE		= "�Ǹ�&nbsp;&nbsp;�m�W";
  $SUBMIT_TITLE		= "�T�{�פJ";
}

if( ($Input{course_id} =~ /^4105/) or ($Input{course_id} =~ /^4108/) ) {
  $dept = "4106";
}elsif( $Input{course_id} =~ /^7/ ) {
  $dept = "7006";
}else{
  $dept = "4104";
}

#foreach $key (keys %Input) {
#  print("$key -> $Input{$key}<BR>\n");
#}

@Student_in_Course = Student_in_Course($dept, $Input{course_id}, $Input{group}, "");
$number_of_student = @Student_in_Course;

print qq(
  <HTML>
   <BODY background="$bg">
    <FORM method=POST action="$target_prog">
      <INPUT type="hidden" name="PHPSESSID" value="$Input{PHPSESSID}">
      <CENTER>
      <H1>$TITLE</H1>
      <table border=2 cellspacing=4 cellpadding=4 bgcolor=#00a0a0>
);

for($i=0; $i<5; $i++) {
  print("<TH bgcolor=#008080>$NAME_TITLE</TH>");
}
$i=0;
foreach $student (@Student_in_Course) {
  if( ($i % 5) == 0 ) {
    print("<TR>");
  }
  print("<TD><FONT size=2>$student $$S{$student}{name}</TD>\n");
  print qq(<INPUT type="hidden" name="id[$i]" value="$student">\n);
  print qq(<INPUT type="hidden" name="name[$i]" value="$$S{$student}{name}">\n);
  $i++;
} 

print qq(
      </TABLE>
      <P>
      <INPUT type=submit value="$SUBMIT_TITLE">
    </FORM>
    Total: $i students
  </BODY>
);

