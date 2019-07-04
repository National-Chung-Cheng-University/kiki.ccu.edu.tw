#!/usr/local/bin/perl

######################################################################
#####  View_Student_Course1.cgi
#####  檢視學生選課資料 - 列出學生清單
#####  Coder: Nidalap :D~
#####  Date : 2006/09/11
######################################################################

printf("Content-type:text/html\n\n");
require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Error_Message.pm";

my(%Input,%Student,%Dept);

%Input=User_Input();
%Dept = Read_Dept($Input{id});
$dept = $Dept{id};

if( $TERM == 3 ) {
  $show_term = "";
}else{
  $show_term = join("", "第", $TERM, "學期");
}

@student = Find_All_Student_In_Dept($dept);

foreach $student (@student) {
  %student = Read_Student($student);
#  $stu{$student{grade}}{$student}{id}	= $student;
  $stu{$student{grade}}{$student}	= $student{name};
#  print("[$student, $student{name}, $student{grade}];<BR>\n");
}

print qq(
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <TITLE>開排課系統--檢視學生選課資料</TITLE>
</head>
 <body bgcolor=white background=$GRAPH_URL//ccu-sbg.jpg>
   <center>
    <table border=0 width=50%>
     <tr>
      <td>系別:</td><td> $Dept{cname} </td>
      <td>年級:</td><td> $Input{grade} </td>
      <td>$YEAR年度$show_term <FONT color=RED>$SUB_SYSTEM_NAME[$SUB_SYSTEM]</FONT></td>
     </tr>
    </table>
    <HR>
    <P>
    <table border=1 width=90%>
);


foreach $grade (keys %stu) {
  print("<TR><TH bgcolor=YELLOW>$grade 年級</TH><TD><FONT size=-1>");
  foreach $id (sort keys %{$stu{$grade}}) {
    print qq(<A href="View_Student_Course2.cgi?dept=$dept&password=$Input{password}&id=$id" target=NEW> );
    print("$id $stu{$grade}{$id}</A>;\n ");
  }
  print("</TD></TR>\n");
}
#foreach $student (@{student[1]}) {
#  print(" $student; ");
#}

print qq(      
     </tr>
    </table>
  </FORM>
  <hr>
);
Links1($Dept{id},$Input{grade},$Input{password});
