#!/usr/local/bin/perl

################################################################################
#####  Update_Student.pl
#####  �ھ� student.txt ���y�j�ɮסA�إߥH�Ǹ����W�٪��p�ɮ�
#####  Updates:
#####    2005/09/20 ���F�W�i��Ҩt�ήį�A�ӼW�[���\��A�ƹ��ҹꪺ�T�j�T�W�i�į� :D~  Nidalap :D~
#####    2010/09/23 ���F�t�X Single Sign On ��@ñ�J�A�W�[�H�����Ҹ����ɦW���p�ɮ�  Nidalap :D~

$| = 1;
require "../../library/Reference.pm";  

print("Content-type:text/html\n\n");

$source		= $REFERENCE_PATH . "student.txt";
$dest_path	= $REFERENCE_PATH . "Student/";
$dest_path2	= $REFERENCE_PATH . "Student_pid/";

print("<BODY background=\"../../../Graph/manager.jpg\">");
print("<CENTER><H1>��s�ǥ;��y�����</H1><HR>");

open(SOURCE, $source);
@lines = <SOURCE>;
close(SOURCE);
$test_line = "1104	3	A	Y	0	999999999	Q120578558	M	4	���ձb��";
push(@lines, $test_line);

print("���b�M���ª����y���...<BR>\n");
opendir(DESTPATH, $dest_path);
@old_files = readdir(DESTPATH);
foreach $file (@old_files) {
  next if( ($file eq ".") or ($file eq "..") );
  $file = $dest_path . $file;
  unlink($file);
#  print("deletomg $file...\n");
}
opendir(DESTPATH, $dest_path2);
@old_files = readdir(DESTPATH);
foreach $file (@old_files) {
  next if( ($file eq ".") or ($file eq "..") );
  $file = $dest_path2 . $file;
  unlink($file);
#  print("deletomg $file...\n");
}
####################################################################################
print("���b�ھ� student.txt �إ߷s�����...<BR>\n");
foreach $line (@lines) {
  ($j, $j, $j, $j, $j, $id, $pid, @junk) = split(/\s+/, $line);
  $dest = $dest_path . $id;
  open(DEST, ">$dest");
  print DEST $line;
  close(DEST);
  
  $dest2 = $dest_path2 . $pid;
  open(DEST2);
  open(DEST2, ">>$dest2");
  print DEST2 $line;
  close(DEST2);
  
#  print("$dest\n"); 
}

print("��s����!<HR><P>\n");
print("<INPUT type=button value=\"��������\" onClick=\"window.close()\">");
