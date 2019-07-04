#!/usr/local/bin/perl

################################################################################
#####  Update_Student.pl
#####  2005/09/20

$| = 1;
require "../../library/Reference.pm";  

print("Content-type:text/html\n\n");

$source = $REFERENCE_PATH . "student.txt";
$dest_path = $REFERENCE_PATH . "Student/";

print("<BODY background=\"../../../Graph/manager.jpg\">");
print("<CENTER><H1>更新學生學籍資料檔</H1><HR>");

open(SOURCE, $source);
@lines = <SOURCE>;
close(SOURCE);
$test_line = "1104	3	A	Y	0	999999999	111111111	M	測試帳號";
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

print("正在根據 student.txt 建立新的資料...<BR>\n");
foreach $line (@lines) {
  ($j, $j, $j, $j, $j, $id, @junk) = split(/\s+/, $line);
  $dest = $dest_path . $id;
  open(DEST, ">$dest");
  print DEST $line;
  close(DEST);
#  print("$dest\n"); 
}

print("更新完成!<HR><P>\n");
print("<INPUT type=button value=\"關閉視窗\" onClick=\"window.close()\">");
