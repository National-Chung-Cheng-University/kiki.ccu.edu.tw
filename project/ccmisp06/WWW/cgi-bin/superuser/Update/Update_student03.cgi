#!/usr/local/bin/perl

################################################################################
#####  Update_Student.pl
#####  根據 student.txt 學籍大檔案，建立以學號為名稱的小檔案
#####  Updates:
#####    2005/09/20 為了增進選課系統效能，而增加此功能，事實證實的確大幅增進效能 :D~  Nidalap :D~
#####    2010/09/23 為了配合 Single Sign On 單一簽入，增加以身份證號為檔名的小檔案  Nidalap :D~

$| = 1;
require "../../library/Reference.pm";  

print("Content-type:text/html\n\n");

$source		= $REFERENCE_PATH . "student.txt";
$dest_path	= $REFERENCE_PATH . "Student/";
$dest_path2	= $REFERENCE_PATH . "Student_pid/";

print("$EXPIRE_META_TAG");
print("<BODY background=\"../../../Graph/manager.jpg\">");
print("<CENTER><H1>更新學生學籍資料檔</H1><HR>");

open(SOURCE, $source);
@lines = <SOURCE>;
close(SOURCE);
##  $test_line = "1104	3	A	Y	0	999999999	Q120578558	M	4	測試帳號";
push(@lines, $test_line);

print("正在清除舊的學籍資料...<BR>\n");
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
print("正在根據 student.txt 建立新的資料...<BR>\n");
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

print("更新完成!<HR><P>\n");
print("<INPUT type=button value=\"關閉視窗\" onClick=\"window.close()\">");
