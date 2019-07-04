#!/usr/local/bin/perl

################################################################################################
#####  View_Student_Course2.cgi
#####  檢視學生選課資料與畢業資格審查表 - 列出學生清單
#####  Coder: Nidalap :D~
#####  Updates:
#####    2006/09/11 Created by Nidalap :D~
#####    2010/03/25 加入「檢視畢業資格審查表PDF檔案」功能 -> View_Student_Course_pdf.cgi Nidalap :D~
#####    2012/02/17 加入 Determine_Dept_Student_Dept() 以轉換系所合一造成的代碼不一致 Nidalap :D~
###############################################################################################

printf("Content-type:text/html\n\n");
require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."System_Settings.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH . "Common_Utility.pm";

print("<HTML><HEAD> $EXPIRE_META_TAG");
my(%Input,%Student,%Dept);

%Input=User_Input();
%Dept = Read_Dept($Input{id});
$dept = $Dept{id};
$dept_s = Determine_Dept_Student_Dept($dept);

#Print_Hash(%Input);

Check_Dept_Password($Dept{id}, $Input{password});

($year, $term) = Last_Semester($Input{semester});

if( $TERM == 3 ) {
  $show_term = "";
}else{
  $show_term = join("", "第", $term, "學期");
}

@student = Find_All_Student($dept_s);
if( not is_Undergraduate_Dept($dept) ) {
   $dept_tmp = $dept_s;
   $dept_tmp =~ s/.$/8/;
  @student_tmp = Find_All_Student($dept_tmp);
}
@student = (@student, @student_tmp);

foreach $student (@student) {
  %student = Read_Student($student);
#  $stu{$student{grade}}{$student}{id}	= $student;
  $stu{$student{grade}}{$student}	= $student{name};
#  print("[$student, $student{name}, $student{grade}];<BR>\n");
}

$Input{view_type} = "stu_course" if( $Input{view_type} eq "" );
$selection = Make_Selection($Input{view_type});

print qq(

    <TITLE>開排課系統--檢視學生選課資料與畢業資格審查表</TITLE>
</head>
 <body bgcolor=white background=$GRAPH_URL/ccu-sbg.jpg>
   <center>
    <table border=0 width=50%>
     <tr>
      <td>系別:</td><td> $Dept{cname} </td>
      <td>年級:</td><td> $Input{grade} </td>
      <td>$year學年度$show_term <FONT color=RED>$SUB_SYSTEM_NAME[$SUB_SYSTEM]</FONT></td>
     </tr>
     <TR>
      <TH colspan=5><H1>檢視學生選課資料與畢業資格審查表</H1></TH>
     </TR>
    </table>
    $selection
    <HR>
    <P>
    <table border=1 width=90%>
);


foreach $grade (sort keys %stu) {
  print("<TR><TH bgcolor=YELLOW>$grade 年級</TH><TD><FONT size=-1>");
  foreach $id (sort keys %{$stu{$grade}}) {
    $url = "?dept=$dept&password=$Input{password}&id=$id&year=$year&term=$term&view_type=$Input{view_type}";
    if( $Input{view_type} eq "pdf" ) {
      $url = "View_Student_Course_pdf.cgi" . $url;
    }else{
      $url = "View_Student_Course3.cgi" . $url; 
    }
    print qq(<A href="$url" target="NEW">);
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
############################################################################################
sub Make_Selection
{
  my($current_view_type) = @_;
  my $selection, $url, $url1, $url2;

  $url = "View_Student_Course2.cgi?password=$Input{password}&dept_cd=$Input{dept_cd}" .
         "&id=$Input{id}&grade=$Input{grade}&semester=$Input{semester}";
  $url1 = $url . "&view_type=stu_course";
  $url2 = $url . "&view_type=pdf";

  if( $current_view_type eq "pdf" ) {
    $selection =  qq[
      我要檢視： \[ 
      <A href=$url1>當學期選課資料</A>
      | 
      <b>該學生畢業資格審查檔(PDF)</b>
      \]
    ];
  }else{
    $selection =  qq[
      我要檢視： \[ 
      <b>當學期選課資料</b>
      | 
      <A href=$url2>該學生畢業資格審查檔(PDF)</A>
      \]
    ];
  }
  return $selection;
}
############################################################################################

