#!/usr/local/bin/perl

#############################################################################
#####     Create_Course_View
#####  �ѥثe�}�Ҹ�Ʋ��ͽҵ{���HTML��, �Ѿǥͬd��
#####  �ݭn���: �}�Ҹ��
#####  ��X���: ��ܨt�Ҫ�HTML�� * 1
#####            �U�Өt�Ҫ��}�Ҹ��HTML�� * n
#####  Coder   : Nidalap
#####  Date    : May 31, 2000
#####  Update  : May 15, 2001
#####		 2007/06/22 �[�J�۰� tgz �ɮ�, �åB��J zipfiles/ �ؿ�
#####		 2008/05/30 �[�J�ǵ{��سs�� -> class_new/Show_All_GRO.cgi
#####            2008/06/03 �N�ǵ{�����@�Ӿǰ|, �[�b�̥k��
#####		 2008/08/05 �W�[ Ecourse �ҵ{�j���s��
#############################################################################

$| = 1;
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH . "Common_Utility.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Course.pm";
require $LIBRARY_PATH . "Teacher.pm";
require $LIBRARY_PATH . "Classroom.pm";
require $LIBRARY_PATH . "Error_Message.pm";

Read_GRO();
$HTML_PATH = $WWW_PATH . "Course/";        ### ���ͪ�HTML�n��b�o�ӥؿ�
$fn1 = "<FONT size=3>";
$fn2 = "<FONT size=2>";
@dept = Find_All_Dept();

print("Content-type:text/html\n\n");
print("���Ͷ}�Ҹ�Ƭd�ߺ���<BR>\n");
print("���ͪ������|��b: $HTML_PATH �U<BR>\n");
print("  ���b���ͥH�U����:<BR>\n index.html");

foreach $dept (@dept) {
  $dept =~ /^(.)/;
  $changeline = $1;
  if( $old_changeline != $changeline ) {
    $old_changeline = $changeline;
    print("<BR>\n");
  }
  print(" $dept");
  $exists{$dept} = Create_Dept_Course_HTML($dept);
}
Create_Index_HTML(%exists);

#$exec_string = "lynx -reload -traversal -dump " . $HOME_URL . "Course/index.html";
#print("\n���b���� $exec_string...\n");
#system($exec_string);
$zipfile_name = $YEAR . $TERM . ".tgz";
$exec_string = "sync; cd " . $WWW_PATH . "Course/;  tar cfz zipfiles/" . $zipfile_name . " *.html";
print("���b���� $exec_string...<BR>\n");
system($exec_string);

$exec_string = "lynx -reload -traversal -dump " . $HOME_URL . "Course/index.html";
print("<BR>\n���b���� $exec_string...<BR>\n");
system($exec_string);

print("<P><H1>�������ͧ���!<P>\n");
############################################################################
sub Create_Index_HTML()
{
  my(%exists) = @_;		### �Y�t�O�_���}�Ҫ� flag

  mkdir($HTML_PATH, 0755)  if( not -e $HTML_PATH );
  $index_file = $HTML_PATH . "index.html";
  open(INDEX, ">$index_file") or die("Cannot create index file $index_file!\n");
  
  print INDEX qq(
    <HTML>
      <HEAD>
        <meta http-equiv="Content-Type" content="text/html; charset=big5">
        <META HTTP-EQUIV="Pragma" CONTENT="NO-CACHE">
        <META HTTP-EQUIV="expires" CONTENT="-1">
        <TITLE>��ߤ����j��$SUB_SYSTEM_NAME�}�ƿ�Ҩt�� $YEAR�Ǧ~�ײ�$TERM�Ǵ��ҵ{��</TITLE>
      </HEAD>
      <BODY background="$GRAPH_URL/bk.jpg">
        <CENTER><H1><FONT face="�з���">
          ��ߤ����j��$SUB_SYSTEM_NAME�}�ƿ�Ҩt��<BR>
          $YEAR�Ǧ~��$TERM_NAME�ҵ{��</FONT></H1>
        <HR>
  );
  $dept_table = Dept_Table(%exists);
  print INDEX $dept_table;
  %time = gettime();
  ($year_last, $term_last) = Last_Semester(1);
  $zipfile	= "zipfiles/" . $YEAR . $TERM . ".tgz";
  $zipfile_last	= "zipfiles/" . $year_last . $term_last . ".tgz";
  print INDEX qq(
    <P>
    <center>
      <FONT color=GREEN size=-1>
        <LI>���ҵ{���ȨѬd�߷��Ǵ��}�Ҹ�ƥ�, �Y�n��ҽШϥ�<A href="http://kiki.ccu.edu.tw/">��Ҩt��</A>.
        <LI>�o�̪���ƬO [$time{time_string}] ���ͪ�, ��ز��ʩηs�¾Ǵ��������, �i��|�X�{�¸��, �i�� Ctrl + F5 ���sŪ���H��s��T.
      </FONT>
      <BR>
      <FONT size=+1>
        [
          <A href="$CGI_URL/Query/Query_by_time1.cgi">�i���}�Ҹ�Ƭd��</A> |
          <A href="$CLASS_URL/Show_All_GRO.cgi">�Ҧ�����ǵ{</A> |
          <A href="$HOME_URL/Update_Course.html">�˵��Ҧ����ʬ��</A>
        ]
        <BR>
        </FONT><FONT size=-1>
        [
          �}�Ҹ�����Y�ɤU��: 
          <A href="$zipfile">���Ǵ�</A> | 
          <A href="$zipfile_last">�W�Ǵ�</A> |
          <A href="zipfiles/">��L�Ǵ�(�ɮצW�٬O�Ǧ~�Ǵ�)</A>
        ]
    </center>
  );
  close(INDEX);
}
############################################################################
sub Create_Dept_Course_HTML()
{
  ($dept) = @_;
  my $exists;				## �^�ǥ��t�O�_���}�Ҹ�ƪ� flag
  $html_file = $HTML_PATH . $dept . ".html";
  open(HTML, ">$html_file") or die("Cannot create index file $html_file!\n");

  @course = Find_All_Course($dept, "", "");
  $exists = @course;
  %dept = Read_Dept($dept);
  %time = gettime();
  print HTML qq(
    <HTML>
      <HEAD>
        <meta http-equiv="Content-Type" content="text/html; charset=big5">    
        <META HTTP-EQUIV="Pragma" CONTENT="NO-CACHE">                
        <META HTTP-EQUIV="expires" CONTENT="-1">
        <TITLE>��ߤ����j��$SUB_SYSTEM_NAME�}�ƿ�Ҩt�� $YEAR�Ǧ~�ײ�$TERM�Ǵ��ҵ{��--$dept{cname}</TITLE>
      </HEAD>
      <BODY background="$GRAPH_URL/bk3.jpg">
      <CENTER><H1><FONT face="�з���">
         ��ߤ����j��$SUB_SYSTEM_NAME�}�ƿ�Ҩt��<BR>
         $YEAR�Ǧ~��$TERM_NAME  �ҵ{��<BR>
         �t�ҧO: $dept{cname}</FONT></H1>
      <HR>
      <FONT size=-1><A href="http://kiki.ccu.edu.tw/ccu_timetable.doc" target=NEW>�W�Үɶ���</A><BR>
      �o�̪���ƬO [$time{time_string}] ���ͪ�, ��ز��ʩηs�¾Ǵ��������, �i��|�X�{�¸��, �i�� Ctrl ���sŪ���H��s��T. </FONT>
      <TABLE border=1>
        <TR bgcolor=YELLOW>
            <TH>$fn1�~��</TH><TH>$fn1�s��</TH>
            <TH>$fn1�Z�O</TH><TH>$fn1��ئW��</TH>
            <TH>$fn1���ұб�</TH><TH>$fn1�W�Үɼ�<BR>����/������/�ѳ��Q��</TH>
            <TH>$fn1�Ǥ�</TH><TH>$fn1�沈</TH>
            <TH>$fn1�W�Үɶ�</TH><TH>$fn1�W�Ҧa�I</TH>
            <TH>$fn1���פH��</TH>
            <TH>$fn1�ҵ{�j��</TH>
            <TH>$fn1�Ƶ�</TH>
        </TR>
  );
  foreach $course (@course) {
#    print("$dept -> $$course{id}, $$course{group}\n");
    %course = Read_Course($dept, $$course{id}, $$course{group}, "", "���Ͷ}�Ҹ��HTML");
    @bgcolor = ("", "#F4B780", "#D39F71", "#C09067", "#AE8662");
    %classroom = Read_Classroom($course{classroom});
    $teacher_string = "";
    foreach $t (@{$course{teacher}}) {
      Read_Teacher_File();
      $teacher_string .= $Teacher_Name{$t};
      $teacher_string .= " ";
    }
    my $time_string = "";
    $time_string = Format_Time_String($course{time});
    
    my $link_to_ecourse = "<A href=\"" . $ECOURSE_QUERY_COURSE_URL
                          . "&courseno=" . $$course{id} . "_" . $$course{group}
                          . "&year=" . $YEAR . "&term=" . $TERM . "\" target=NEW>"
                          . "�s��</A>";
    
    my $note_string = "";
    $note_string = Format_Note_String(%course);

    $note_dis = $note_eng = "";
    if( $course{distant_learning} == 1 ) {
      $note_dis = "<FONT color=RED>(����ج����Z�оǽҵ{)";
    }
    if( $course{english_teaching} == 1 ) {
      $note_eng= "<FONT color=RED>(����ج����^�y�½�)";
    }
    
    foreach $gro_cour (@gro_cour) {
#      print("$course{id} eq $$gro_cour{cour_cd}?\n");
      next if($$gro_cour{gro_no} eq "80");		### �w�g���ϥΪ���� added 20080822
      if( $course{id} eq $$gro_cour{cour_cd} ) {
        $note_string .= "<A href=\"" . $CLASS_URL . "Show_All_GRO.cgi\">���ҵ{�ݩ�";
        $note_string .= $gro_name{$$gro_cour{gro_no}}{gro_name};
        $note_string .= "</A>";
      }
    }
    
    print HTML qq(
      <TR>
        <TD bgcolor=$bgcolor[$course{grade}]>$fn1$course{grade}</TD>
        <TD>$fn1$$course{id}</TD>
        <TD>$fn1$$course{group}</TD>
        <TD>$fn1$course{cname}<br>$course{ename}<BR>$note_dis $note_eng</TD>
        <TD>$fn1$teacher_string</TD>
        <TD align=center>$fn1$course{total_time}<BR>
            $course{lab_time1}/$course{lab_time2}/$course{lab_time3}</TD>
        <TD>$fn1$course{credit}</TD>
        <TD>$fn1$PROPERTY_TABLE[$course{property}]</TD>
        <TD>$fn1$time_string</TD>
        <TD>$fn1$classroom{cname}</TD>
        <TD>$fn1$course{number_limit}</TD>
        <TD align=CENTER>$fn1$link_to_ecourse</TD>
        <TD>$fn1$note_string</TD>        
      </TR>
    );
  }
  print HTML ("</TABLE>");
  
  print HTML qq(<P><CENTER><A href="index.html">�^�W��</A>);
  return($exists);
}

###########################################################################
sub Format_Note_String()
{
  my(%course) = @_;
  my $note_string = "";
  my($temp_dept);
  my(@grade) = ("", "�@�~��", "�G�~��", "�T�~��", "�|�~��");

#  if( ${$course{prerequisite_course}}[0] ne "" ) {
#    $note_string .= "���׬��:";
#    foreach $pre_course (@{$course{prerequisite_course}}) {
#      %temp_course  = Read_Course($course{dept}, $pre_course, "01","history", "");
#      $note_string .= "($temp_course{id})$temp_course{cname} ";
#    }
#  }
  if( (${${$course{prerequisite_course}}[0]}{dept} ne "99999") and (${${$course{prerequisite_course}}[0]}{dept} ne "") ) {
    $note_string .= "<b>���׬��</b>";
    foreach $pre_course (@{$course{prerequisite_course}}) {
      %pre_course = Read_Course( $$pre_course{dept}, $$pre_course{id}, "01" ,"history");
      $note_string = $note_string . "(" . $$pre_course{id} . ")" . $pre_course{cname} . "(" . $GRADE{$$pre_course{grade}} . ")" . " ";
    }
    if( $course{prerequisite_logic} and defined(${${$course{prerequisite_course}}[1]}{dept}) ) {
      $note_string .= "($PREREQUISITE_LOGIC{$course{prerequisite_logic}})";
    }
  }

  if ( $course{reserved_number} != 0 ) {
    $note_string .= "�O�d�s��$course{reserved_number}�H; ";
  }
  if( ${$course{support_dept}}[0] ne "" ) {
    $note_string .= "�䴩";
    foreach $dept (@{$course{support_dept}}) {
      %temp_dept = Read_Dept($dept);
      $note_string .= $temp_dept{cname2};
    }
    foreach $grade (@{$course{support_grade}}) {
      $note_string .= $grade[$grade];
    }
    foreach $class (@{$course{support_class}}) {
      $note_string .= $class;
      $note_string .= "�Z";
    }
    $note_string .= "; ";
  }
  $note_string =~ s/;\s$//;
  $note_string .= "."  if($note_string =~ /��/);
  $ban_num = @{$course{ban_dept}};
  if( ($ban_num > 50) and ( ($SUB_SYSTEM==1)or($SUB_SYSTEM==1)) ) {
     $note_string .= "�����t�ͭ�.";         ### �v�y���pNidalap,May11,1999
#     if( $course{dept} !~ /[25].../) {      ### �z, �ް|����ܼW�[20%���~�t��r
#     $note_string .= "��[�h������}��ѥ~�t���;";		###  2007/09/21 ����
#     }
#     $note_string .= $course{note};
  }
#  if( $course{distant_learning} == 1 ) {
#    $note_string .= "����ج����Z�оǽҵ{;";
#  }
#  if( $course{english_teaching} == 1 ) {
#    $note_string .= "����ج����^�y�½�;";
#  }
  
  $note_string .= $course{note};
  return $note_string;
}

###########################################################################
sub Dept_Table()
{
    my(%exists) = @_;

    my(@Dept)=Find_All_Dept();
    foreach $gro_name (keys %gro_name) {				###  �N����ǵ{�����t��
      if( $gro_name{$gro_name}{gro_name} ne "" ) {
#        print("pushing $gro_name ( $gro_name{$gro_name}{gro_name} ) into dept...\n");
        push(@Dept, $gro_name);
      }
    }
    my($DATA)="";
    my($Dept1,$Dept2,$Dept3,$Dept4,$Dept5,$Dept6,$Dept7,$Dept0)="";

    $DATA = $DATA . "<table width=90% border=0>\n";
    $DATA = $DATA . "   <tr><th bgcolor=#99ffff>$fn2��ǰ|</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff>$fn2�z�ǰ|</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff>$fn2���|��Ǿǰ|</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff>$fn2�u�ǰ|</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff>$fn2�޲z�ǰ|</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff>$fn2�k�ǰ|</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff>$fn2�Ш|�ǰ|</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff>$fn2��L</th>\n";
    $DATA = $DATA . "	    <th bgcolor=#99ffff>$fn2����ǵ{</th>\n";
    $DATA = $DATA . "   </tr>\n";

#    $Dept0 .= "<A href=I000.html>";
#    $Dept0 .= "�@�P��</A><br>\n";

    foreach $dept (@Dept){
#      print("now processing dept $dept...\n");
        if( length($dept) == 2 ) {		###  ����ǵ{�N�X�O��X
          %Dept=("id"=>"$dept", "cname2"=>"$gro_name{$dept}{gro_name}");
        }else{					###  �@��t�ҥN�X�O�|�X
          %Dept=Read_Dept($dept);
        }
        $link = 1;
        $link = 0  if( $exists{$dept} == 0 );
        
        if( length($dept) == 2 ) {				###  if ����ǵ{
#          print("adding $dept into Dept8\n");
          $gro_link = $CLASS_URL . "Show_All_GRO.cgi?gro_no=" . $dept;
          $Dept8 .= "<A href=$gro_link>$gro_name{$dept}{gro_name}</A><br>\n";
        }else{							###  else �@��t��
#          print("adding $dept into dept0~7\n");
          if( ($Dept{id} == 0) or ($Dept{id} eq "7006") ){
              $Dept0 .= "<A href=$Dept{id}.html>" if $link;
              $Dept0 .= $fn2.$Dept{cname2}."</A><br>\n";
          }else{
            if( $Dept{id}/1000 >= 7 ){
              $Dept7 .= "<A href=$Dept{id}.html>" if $link;
              $Dept7 .= $fn2.$Dept{cname2}."</A><br>\n";
            }elsif($Dept{id}/1000 >= 6){
              $Dept6 .= "<A href=$Dept{id}.html>" if $link;
              $Dept6 .= $fn2.$Dept{cname2}."</A><br>\n";
            }elsif($Dept{id}/1000 >= 5){
              $Dept5 .= "<A href=$Dept{id}.html>" if $link;
              $Dept5 .= $fn2.$Dept{cname2}."</A><br>\n";
            }elsif($Dept{id}/1000 >= 4){
              $Dept4 .= "<A href=$Dept{id}.html>" if $link;
              $Dept4 .= $fn2.$Dept{cname2}."</A><br>\n";
            }elsif($Dept{id}/1000 >= 3){
              $Dept3 .= "<A href=$Dept{id}.html>" if $link;
              $Dept3 .= $fn2.$Dept{cname2}."</A><br>\n";
            }elsif($Dept{id}/1000 >= 2){
              $Dept2 .= "<A href=$Dept{id}.html>" if $link;
              $Dept2 .= $fn2.$Dept{cname2}."</A><br>\n";
            }elsif($Dept{id}/1000 >= 1){
              $Dept1 .= "<A href=$Dept{id}.html>" if $link;
              $Dept1 .= $fn2.$Dept{cname2}."</A><br>\n";
            }
          }
        }
    }

#    $DATA = $DATA ."<tr>\n";
#    $DATA = $DATA ."    <td valign=top>".$Dept4."</td>\n";
#    $DATA = $DATA ."    <td valign=top>".$Dept2."</td>\n";
#    $DATA = $DATA ."    <td valign=top>".$Dept5."</td>\n";
#    $DATA = $DATA ."    <td valign=top>".$Dept3."</td>\n";
#    $DATA = $DATA ."    <td valign=top>".$Dept1."</td>\n";
#    $DATA = $DATA ."    <td valign=top>".$Dept6."</td>\n";
#    $DATA = $DATA ."    <td valign=top>".$Dept7."</td>\n";
#    $DATA = $DATA ."    <td valign=top>".$Dept0."</td>\n";
#    $DATA = $DATA ."</tr>\n";
#    $DATA = $DATA . "   </table>\n";
    
    $DATA = $DATA ."<tr>\n";
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept1."</td>\n";         # ��
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept2."</td>\n";         # �z
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept3."</td>\n";         # ��
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept4."</td>\n";         # �u
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept5."</td>\n";         # ��
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept6."</td>\n";         # �k
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept7."</td>\n";         # ��
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept0."</td>\n";         # ��L
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept8."</td>\n";         # ����ǵ{
    $DATA = $DATA ."</tr>\n";
    $DATA = $DATA . "   </table>\n";


    return($DATA);
                    
}


