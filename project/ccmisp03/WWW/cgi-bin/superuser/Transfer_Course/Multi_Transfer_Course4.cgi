#!/usr/local/bin/perl

###########################################################################
#####   Transfer_Course4.cgi
#####   �h��h�ॲ��/�����
#####   �C�X���Өt�ůZ�����, �̷Ӷü���J���ӯZ�O.
#####   Coder: Nidalap
#####   Date : 09/04/2001
###########################################################################
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Course.pm";
print("Content-type:text/html\n\n");

%Input = User_Input();
@dept = Find_All_Dept();
@course = Find_All_Course($Input{dept}, $Input{grade}, "");

print qq(
 <HEAD><TITLE>�h��h����/���������</TITLE></HEAD>
   <BODY background="$GRAPH_URL./ccu-sbg.jpg"><CENTER>
     <H1>�h��h����/���������<br>���ɵ��G<hr></H1>
);
#     <TABLE border=1>
#       <TR><TH bgcolor=YELLOW>���</TH><TH bgcolor=YELLOW>�ǥ�</TH></TR>
#);

foreach $key (sort keys %Input) {
#  print("$key -> $Input{$key}<BR>\n");
  if( $key =~ /......._../ ) {              ### ��إN�X_�Z�O
    ($course_id, $course_group) = split(/_/, $key);
    @student = split(/_/, $Input{$key});
#    print qq(
#      <TR>
#        <TD>$course_id, $course_group</TD>
#        <TD>@student</TD>
#      </TR>
#    );
    $num = 0;
    foreach $student (@student) {
      $num ++;
      Add_Student_Course($student,$Input{dept},$course_id,$course_group,$Input{property});
#      print("Add: $student,$Input{dept},$course_id,$course_group,$Input{property}<BR>");
    }
    print("��� $course_id _ $course_group �@ $num �H�[�粒��!<BR>\n"); 
  }
}