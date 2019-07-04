#!/usr/local/bin/perl

########################################################################
#####  Update_teacher02.cgi
#####  Ū���q�H�Ƹ�Ʈw�o�쪺 teacher.txt, ���@�ǥN�X�ഫ
#####  Updates:
#####    2009/02/05  ���ӬO perl script, ��s���u�W����(Nidalap :D~)

$| = 1;
require "../../library/Reference.pm";

print("Content-type:text/html\n\n");

$source = $REFERENCE_PATH . "teacher.txt";
$dest   = $REFERENCE_PATH . "teacher.txt";

open(SOURCE, $source) or die("Cannot open source file $source\n");

@lines = <SOURCE>;
close SOURCE;
open(DEST, ">$dest") or die("Cannot open dest file > $dest\n");

@lines = sort {				###  �Ƨ��u������: �t�� -> �m�W
  ($dept_a, $id_a, $name_a) = split(/\s+/, $a);
  ($dept_b, $id_b, $name_b) = split(/\s+/, $b);
  if( $dept_a ne $dept_b ) {
    return $a cmp $b;
  }else{
    return $name_a cmp $name_b;
  }
} @lines;

foreach $line (sort @lines) {
  $line =~ s/\n//;
  ($dept, $id, $name) = split(/\s+/, $line);
  $dept =~ s/3254/6054/;
  $dept =~ s/3256/6056/;
  $dept =~ s/3546/7156/;
  $dept =~ s/I001/I000/;
  $dept =~ s/M000/I000/;
  $dept =~ s/M110/V000/;
  $dept =~ s/7206/3546/;
  $dept =~ s/Z121/I000/;
  $dept =~ s/7408/7406/;           ###  �ҵ{��s��
  $dept =~ s/B000/Z121/;	   ###  �y������
    
#  print("checking $dept  $id  $name ... <BR>\n");
#  if( $dept eq "B000" ) {
#    next;
#  }
  if( !defined($teacher_exist{$dept}{$id}) ) {
    $teacher_exist{$dept}{$id} = 1;
    $newline = join("     ",$dept, $id, $name);
    print DEST ("$newline\n");
  }else{
#    print("teacher $dept  $id  $name already exists!<BR>\n");
  }
}


print ("<BODY background=\"../../../Graph/manager.jpg\">");
print ("<CENTER><H1>��s�Юv�����</H1><HR>\n");   
print ("�w�g�N�Юv����ɤ����t�ҥN�X���L�ഫ...<BR>\n");
print ("���~�����<BR><A href=Update_teacher03.cgi>��s��ƲĤT�B</A>");
                  

close DEST;
