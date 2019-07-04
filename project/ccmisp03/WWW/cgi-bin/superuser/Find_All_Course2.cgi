#!/usr/local/bin/perl
#################################################################
#####  Find_All_Course2.cgi
#####  �d�ߩҦ���ؤ���W��
#####  �q Find_All_Course.cgi �ק�Ө�
#####  ���Ͷ}�ҩ��Ӹ��, �ѾǴ������Z�ֹ��(?)
#####  Coder: Nidalap 
#####  Date :2005/02/18
#################################################################

require "../../../LIB/Reference.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Student_Course.pm";
require $LIBRARY_PATH . "Course.pm";
require $LIBRARY_PATH . "Teacher.pm";

print("Content_type:text/plain\n\n");
Read_Teacher_File();

print("��Ǵ��}�ҩ��Ӫ�: $YEAR �Ǧ~�ײ� $TERM �Ǵ�\n");
print("-------------------------------------------\n");
print("�}�Ҩt��\t�}�ҽs�X\t�Z�O\t��ئW��\t�׽ҤH��\t���ұЮv\n");
@dept = Find_All_Dept();
foreach $dept (@dept) {
  %dept = Read_Dept($dept);
#  next if( $dept ne "1104");
  for($grade = 1 .. 4) {
    @course = Find_All_Course($dept, $grade);
    foreach $course (@course) {
      %course = Read_Course($dept, $$course{id}, $$course{group});
      $count = Student_in_Course($dept, $course{id}, $course{group});
      $teacher_string = Format_Teacher_String(@{$course{teacher}});
      print("$dept{cname}\t$course{id}\t$course{group}\t$course{cname}\t$count\t$teacher_string\n");
    }
  }
}

