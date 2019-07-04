#!/usr/local/bin/perl 
###########################################################################
#####  Update_a30tcourse02.cgi
#####  Ū��dept_serv_course_id.txt, �s�@�۹����ɮפΥؿ�
#####  ���F�����ɤ����u�Ǩt�A�Ⱦǲߡv�ҵ{�i�ΡA�G�Ӧ����ק�C
#####  ���ӥu�� 100_1 �|�Ψ�...
#####  Updates:
#####    2011/04/21 �q Update_allcourse02.cgi copy �ӥ�  Nidalap :D~
###########################################################################

$| = 1;
require "../../library/Reference.pm";

print("Content-type:text/html\n\n");

print("<BODY background=\"../../../Graph/manager.jpg\">");
print("<CENTER><H1>��s���~�}�Ҹ����</H1><HR>");

$AllCourseFile = $REFERENCE_PATH . "dept_serv_course_id.txt";
open(ALLCOURSE, $AllCourseFile) or
   die("Cannot open file $AllCourseFile!\n");
@line = <ALLCOURSE>;
close(ALLCOURSE);
print("�̾� dept_serv_course_id.txt, ��s�}�Ҿ��v����� DATA/Course/* ... <P>\n");
print("���b�g�J�s�����v�����......<P>\n");

$course{cname} = "�Ǩt�A�Ⱦǲ�";
$course{ename} = "Service Learning�GCampus Service";
$course{grade} = 1;
$course{total_time} = 2;
$course{credit} = 0;
$course{property} = 1;

foreach $line (@line) {
  chomp($line);
  ( $course{dept}, $course{id} )  = split(/\t/, $line);

  $course_path = $HISTORY_COURSE_PATH . $course{dept} . "/";  
#  system("mkdir $course_path")  if( not -e $course_path );
  if($last_id ne $course{id}) {
    Append_Classindex();
    Write_Course_File();
  }
}
print ("<BR>�����I<P>");
print ("<INPUT type=button value='��������' onClick='window.close()'>");

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
  print COURSE ("\n");		## reserved 1~4
  print COURSE ("\n");
  print COURSE ("\n");
  print COURSE ("\n");
  print COURSE ("$course{note}");
}


