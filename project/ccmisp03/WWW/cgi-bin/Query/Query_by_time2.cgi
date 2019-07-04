#!/usr/local/bin/perl
########################################################################
#####  Query_by_time2.cgi
#####  �H�t��, �}�Ҹ`���ɶ�, ��ئW��, �Юv�m�W������, �j�M��Ǵ��}�Ҹ��.
#####  Last Update:
#####   2004/03/02
#####   2008/06/03  �s�W��ئW�ٻP�Юv�m�W�d�߿ﶵ.  Nidalap :D~
########################################################################
print "Content-type: text/html","\n\n";

require "../library/Reference.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Open_Course.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Error_Message.pm";

#Check_SU_Password($Input{password}, "dept", $Input{dept_cd});
%Input = User_Input();
$file_path = $DATA_PATH . "Course_by_time/";
print qq(
  <HTML>
    <HEAD>
      <TITLE>�i���}�Ҹ�Ƭd�� -- �}�Ҹ�ƦC��</TITLE>
      <LINK rel="stylesheet" type="text/css" href="$HOME_URL/font.css">
    </HEAD>
  <body bgcolor=white background=$GRAPH_URL/ccu-sbg.jpg>
  <center>
    <SPAN class="title1">�i���}�Ҹ�Ƭd��</SPAN>
    <BR>
    <IMG src=$TITLE_LINE>
    <P class="illustration">
);


Check_Input_Illigal($Input{course_cname});			###  �ˬd course_cname �D�k�r��
Check_Input_Illigal($Input{teacher});				###  �ˬd teacher �D�k�r��

@dept = split(/\*:::\*/, $Input{dept});

if( @dept == 0 ) {
  print("�Цܤֿ�ܤ@�Өt��!");
  exit();
}

foreach $dept (@dept) {
  $dept_selected{$dept} = 1;
}
Check_Dept(@dept);

$i = 0;
foreach $time (keys %Input) {
  next if( $time !~ /^\d_/);
  $file = $file_path . $time;
#  print("file = $file<BR>\n");
  next if( not -e $file );
  open(TIMEFILE, $file);
#  @{$course[$i]} = <TIMEFILE>;
  @line = <TIMEFILE>;
  foreach $line (@line) {
    ($dept, $dept_cname2, $grade, $id, $grp, $total_time, @junk) = split(/\t/, $line);
    $id = $id . "_" . $grp;
    $course{$time}{$id} = 1;
    $total_time{$id} = $total_time;
    $content{$id} = $line;
#    print("$time, $id, $course{$time}{$id}<BR>\n");
  }
  $i++;
}

$j = 0;
foreach $time (keys %course) {
  foreach $course (%{$course{$time}}) {
    if($time =~ /[A-J]$/) {
      $count{$course} += 1.5;
    }else{
      $count{$course}++;
    }
  }
  $j++;
}

$hits = 0;
$content = "";
foreach $course (sort keys %count) {
  if( $Input{query_type} == 1 ) {
    next if( $count{$course} != $total_time{$course} );
  }
  
  ($dept, $dept_cname2, $grade, $c_id, $c_grp, $total_time, $time_string, $number_limit, $classroom, $teacher, $note, $cname)
     = split(/\t/, $content{$course});
#  next if($dept ne $Input{dept});
  next if($dept_selected{$dept} != 1);						###  �p�G�S�惡�t, next
  if( $Input{course_cname} ne "" ) {						###  �p�G����J��ئW��, �z�蠟
    if( $cname !~ /$Input{course_cname}/ ) {
      next;
    }else{
      $cname =~ s/$Input{course_cname}/<FONT color=RED>$Input{course_cname}<\/FONT>/g;
    }
  }
  
  if( $Input{teacher} ne "" ) {							###  �p�G����J�Юv�m�W, �z�蠟
    if( $teacher !~ /$Input{teacher}/ ) {
      next;
    }else{
      $teacher =~ s/$Input{teacher}/<FONT color=RED>$Input{teacher}<\/FONT>/g;
    }
  }
  
  
  if( $last_dept ne $dept ) {
    if($high_light =~ /FFFFFF/) {
      $high_light = "bgcolor = FFFF77";
    }else{
      $high_light = "bgcolor = FFFFFF";
    }
  }
  if( $note == 0 ) {
    $note = "�L";
  }else{
    $note = "<A href=\"$CLASS_URL" . "ShowNote.cgi?&dept=" . $dept . "&course=" . $c_id . "&group=" . $c_grp . "\" target=NEW>��</A>";
  }
  $content .= "<TR align=CENTER $high_light><TD>$dept_cname2</TD><TD>$grade</TD><TD>$c_id</TD><TD>$c_grp</TD><TD align=LEFT>$cname</TD><TD>$total_time{$course}</TD>";
  $content .= "<TD>$time_string</TD><TD>$teacher</TD><TD>$classroom</TD><TD>$number_limit</TD><TD>$note</TD></TR>";
#  $content .= "<TR><TD rowspan=2>$dept_cname2</TD><TD rowspan=2>$c_id</TD><TD rowspan=2>$c_grp</TD><TD colspan=5>$cname</TD></TR>";
#  $content .= "<TD>$total_time{$course}</TD><TD>$time_string</TD><TD>$classroom</TD><TD>$number_limit</TD></TR>";

  $hits ++;
  $last_dept = $dept;
#  print("$course, $count{$course}, $total_time{$course}<BR>\n");
}


print qq(
    <SPAN class="font1">
      <CENTER>�@�� $hits ���}�Ҹ�ƲŦX����
    <form name=form1 method=post action=Query_by_time2.cgi>
      <input type=hidden name=dept value=$Input{dept}>
      <input type=hidden name=password value=$Input{password}>
      <TABLE border=1 class=font1 width=800>
        <TR>
          <TH>�}�Ҩt��</TH><TH>�~��</TH><TH>��إN�X</TH><TH>�Z�O</TH><TH>��ئW��</TH>
          <TH>�ɼ�</TH><TH>�W�Үɶ�</TH>
          <TH>�½ұЮv</TH><TH>�W�ұЫ�</TH><TH>����<BR>�H��</TH><TH>��L<BR>����</TH>
        </TR>
        $content
        </TR>
      </TABLE>
    <p>
  </body>
  </html>
);
 
######################################################################################
sub Check_Dept()
{
  my(@dept) = @_;
  my($message);
  
#  if( @dept > 7 ) {
#    print("���קK�t�έt���L�j, �ФŤ@���d�߶W�L�C�Өt��, ����!<BR>\n");
#    exit();
#  }
}