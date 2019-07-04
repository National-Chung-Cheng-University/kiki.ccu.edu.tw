#!/usr/local/bin/perl
print "Content-type: text/html","\n\n";

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Student_Course.pm"; 
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Teacher.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."System_Settings.pm";

my(%Input,@Dept,@Course,%Dept);

%Input = User_Input();
%system_flags = Read_System_Settings();
%Dept = Read_Dept($Input{dept_cd});

if( $Input{semester} eq "last" ) {
  ($year, $term) = Last_Semester("1");
  $yearterm = $year . $term;
}else{
  $yearterm = "";
}

#print("semester, yearterm = $Input{semester}, $yearterm<BR>\n");

@Course = Find_All_Course( $Dept{id},"",$yearterm );
@teacher = Read_Teacher_File();

require $LIBRARY_PATH."Select_Course.pm";
$sys_state = Whats_Sys_State();
if( $sys_state == 0 ) {
  print qq(
    <html>
      <head><title>�ĤG���}�ƽҨt��</title></head>
      <body background=$GRAPH_URL/ccu-sbg.jpg>
        <center>
         <img src=$GRAPH_URL/open.jpg><P>
         <h4>�d�߭׽ҾǥͦW��\\��</h4><HR>
         �ثe�t�μȤ��}��d��!
  );
  exit(1);
}

if( $Input{query_count} == 1 ) {
  Show_Count_List();
}else{
  Show_Course_Select();
}
############################################################################
#####  Show_Count_List
#####  ��ܸӨt�ҷ��Ǵ��Ҧ��}�]��ت��ثe��ҤH��, �̦~��->��إN�X�Ƨ�
#####  Added 2003/01/08, Nidalap :D~
sub Show_Count_List()
{
  print qq(
    <html>
      <head>
        <title>�d�߭׽ҾǥͦW��- $Dept{cname}</title>
      </head>
      <body background=$GRAPH_URL/ccu-sbg.jpg>
        <center><h1>
          <img src=$GRAPH_URL/open.jpg>
        </h1>
        <p>
        <TABLE border=1>
          <TR>
            <TH>��إN�X</TH><TH>��دZ�O</TH><TH>��ئW��</TH>
            <TH>���פH��</TH><TH>�ثe�׽ҤH��</TH>
            <TH>�½ұЮv</TH><TH>�W�ұЫ�</TH><TH>�W�Үɶ�</TH>
          </TR>
  );
  for($grade=1..4) {
    @course = Find_All_Course($Dept{id}, $grade, $yearterm);
    foreach $course (@course) {
      %course = Read_Course($Dept{id}, $$course{id}, $$course{group}, $yearterm, "");
      $count = Student_in_Course($Dept{id}, $course{id}, $course{group}, $yearterm);
      $teacher_string =  "";
      foreach $teacher (@{$course{teacher}} ) {
        $teacher_string .= "<BR>"  if($teacher_string ne "");
        $teacher_string .= $Teacher_Name{$teacher};
      }
      $time_string = Format_Time_String($course{time});
      %Room=Read_Classroom($course{classroom});    
      print qq(
        <TR>
          <TD>$course{id}</TD>
          <TD>$course{group}</TD>
          <TD>$course{cname}</TD>
          <TD>$course{number_limit}</TD>
          <TD>$count</TD>
          <TD>$teacher_string</TD>
          <TD>$Room{cname}</TD>
          <TD>$time_string</TD>
        </TR>
      );
    }
  }
  print("</TABLE>");
}
############################################################################
#####  Show_Course_Select
#####  ��ܸӨt�ҷ��Ǵ��Ҧ��}�]��دZ�O, �ѿ�ܬd�ߦW��
sub Show_Course_Select()
{
  print qq( 
    <html>
      <head>
        <title>�d�߭׽ҾǥͦW��- $Dept{cname}</title>
      </head>
      <body background=$GRAPH_URL/ccu-sbg.jpg>
        <center><h1>
          <img src=$GRAPH_URL/open.jpg>
        </h1>
       <p>
       <h4>�d�߭׽ҾǥͦW��\\�� Version 2.000</i></h4><p>
       <h4>�п�ܱ��d�ߤ����</h4><p><br>
         <form method=post action=Query_2.cgi>
         <table border=0>
           <tr>
             <th><h3>���:</h3></th><td><select name=course_cd>
  );

  my($course,%temp,$i,$count);
  $count = @Course;
  for($i=0;$i < $count;$i++) {
    %temp = Read_Course($Dept{id},$Course[$i]{id},$Course[$i]{group}, $yearterm);
    print"<option value=$temp{id}_$temp{group}>[$temp{id}-$temp{group}]$temp{cname}\n";
  }

  print qq(
        </select>
          <input type=hidden name=dept_cd value=$Dept{id}>
          <input type=hidden name=dept_name value=$Dept{cname}> 
        </td>
      </tr>
    </table>
    <INPUT type=hidden name=yearterm value=$yearterm>
    <INPUT type=RADIO name="last_select" value=0 CHECKED>�d�ߥثe��ҦW��<BR>
  );
  if( ($system_flags{allow_query_last_select_namelist} == 1) and ($yearterm eq "")  ) {
    print qq(
      <INPUT type=RADIO name="last_select" value=1>�d�ߤW���z�粒��W��<BR>
    );
  }
  print qq(
      <input type=\"submit\" value=\"��ƶ�g����\">
      <input type=\"reset\" value=\"���s��g���\">
    </form>
    </center>
    </body>
    </html>
  );
}