#!/usr/local/bin/perl 
###########################################################################
#####  Update_Course.pl
#####  Ū����Ʈw�ǤW�Ӫ��}�Ҿ��v��(allcourse.txt), �s�@�۹����ɮפΥؿ�
#####  Updates:
#####   1999/04/21 Created by Nidalap Leee
#####   2010/11/25 �[�J�s�W�� gender_eq, env_edu ���������.  Nidalap :D~
#####  ����e�нT�w���v�ɮ榡�L�~!
###########################################################################

$| = 1;
require "../../library/Reference.pm";

print("Content-type:text/html\n\n");

print("<BODY background=\"../../../Graph/manager.jpg\">");
print("<CENTER><H1>��s�ҵ{�����</H1><HR>");

$AllCourseFile = $DATA_PATH . "Transfer/allcourse.txt";
open(ALLCOURSE, $AllCourseFile) or
   die("Cannot open file $AllCourseFile!\n");
#$temp = <ALLCOURSE>;                          ###  �Ĥ@��O���W��, ���椣��
@line = <ALLCOURSE>;
close(ALLCOURSE);
print("�̾� allcourse.txt, ��s�}�Ҿ��v����� DATA/Course/* ... <P>\n");
print("���b�M���¦������v�����......<BR>\n");
Clear_Old_History_Course();
print("���b�g�J�s�����v�����......<P>\n");
foreach $line (@line) {
  chomp($line);
  ( $course{dept}, $course{id}, $course{grade}, $course{group}, 
    $course{credit}, $course{total_time}, $course{property}, 
    $course{suffix_cd}, $course{attr}, $course{cname}, @ename)
          = split(/\t/, $line);
  $course{ename} = join(" ",@ename);
  $course{grade} =~ /(.)./;   $course{grade} = $1;
  if( $course{id} =~ /^902....$/ ) {
    $course{dept} = "F000";
  }elsif($course{id} =~ /^903....$/ ) {
    $course{dept} = "V000";
  }
  print("$course{dept}, \n")
     if($course{dept} ne $last_dept);
  $course_path = $HISTORY_COURSE_PATH . $course{dept} . "/";  
  system("mkdir $course_path")  if( not -e $course_path );
  if($last_id ne $course{id}) {
    Append_Classindex();
    Write_Course_File();
  }
  $last_id = $course{id};
  $last_dept = $course{dept};
}

print ("���~�����<BR><A href=Update_allcourse03.cgi>��s��ƲĤT�B</A>");

#########################################################################
sub Clear_Old_History_Course()
{
  if($HISTORY_COURSE_PATH eq "") {
    die("HISTORY_COURSE_PATH is null, check for linkage of modules!\n");
  }
  system("rm -fr $HISTORY_COURSE_PATH*");
}
#########################################################################
sub Append_Classindex()
{
  $index_file = $course_path . "classindex";

  open(INDEX,">>$index_file") or die("Cannot append to file $index_file!\n");
#  print INDEX ("$course{id}\t$course{grade}\t$course{group}\n")
  print INDEX ("$course{id}\t$course{grade}\t01\n");
  close(INDEX);
}
#############################################################################
sub Write_Course_File()
{
#  $course_file = $course_path . $course{id} . "_" . $course{group};
  $course_file = $course_path . $course{id} . "_01";

  open(COURSE,">$course_file") or
     die("Cannot write to file $course_file!\n");
  print COURSE ("$course{cname}\n");
  print COURSE ("$course{ename}\n");
  print COURSE ("$course{total_time}\n");
  print COURSE ("$course{credit}\n");
  print COURSE ("$course{classroom}\n");
  print COURSE ("$course{property}\n");
  print COURSE ("$course{teacher}\n");
  print COURSE ("$course{time}\n");
  print COURSE ("$course{number_limit}\n");
  print COURSE ("$course{support_dept}\n");
  print COURSE ("$course{support_grade}\n");
  print COURSE ("$course{support_class}\n");
  print COURSE ("$course{ban_dept}\n");
  print COURSE ("$course{ban_grade}\n");
  print COURSE ("$course{ban_class}\n");
  print COURSE ("$course{reserved_number}\n");
  print COURSE ("$course{principle}\n");
  print COURSE ("$course{suffix_cd}\n");
  print COURSE ("$course{total_time}\n");   ### lab_time1
  print COURSE ("0\n");                     ### lab_time2
  print COURSE ("0\n");                     ### lab_time3
  print COURSE ("0\n");    ##  support_cge_type
  print COURSE ("0\n");    ##  support_cge_number
  print COURSE ("\n");     ##  prerequisite_course
  print COURSE ("AND\n");  ##  prerequisite_logic
  print COURSE ("\n");		## distant_learning
  print COURSE ("\n");		## english_teaching
  print COURSE ("\n");		## remedy
  print COURSE ("\n");		## s_match
  print COURSE ("\n");		## gender_eq
  print COURSE ("\n");		## env_edu
  print COURSE ("$course{attr}\n");  ## attr
  print COURSE ("\n");		## reserved 2~4
  print COURSE ("\n");
  print COURSE ("\n");
  print COURSE ("$course{note}");
}


