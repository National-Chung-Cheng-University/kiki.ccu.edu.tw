#!/usr/local/bin/perl

########################################################################
#####  Update_teacher02.cgi
#####  讀取從人事資料庫得到的 teacher.txt, 做一些代碼轉換
#####  Updates:
#####    2009/02/05  本來是 perl script, 更新為線上執行(Nidalap :D~)
#####    2013/08/06  新增教師英文姓名欄位 Nidalap :D~

$| = 1;
require "../../library/Reference.pm";

print("Content-type:text/html\n\n");
print $EXPIRE_META_TAG;

$source = $REFERENCE_PATH . "teacher.txt";
$dest   = $REFERENCE_PATH . "teacher.txt";

open(SOURCE, $source) or die("Cannot open source file $source\n");

@lines = <SOURCE>;
close SOURCE;
open(DEST, ">$dest") or die("Cannot open dest file > $dest\n");

@lines = sort {				###  排序優先順序: 系所 -> 姓名
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
  ($dept, $id, $name, @ename) = split(/\s+/, $line);
  $ename = join(" ", @ename);
  $dept =~ s/3254/6054/;
  $dept =~ s/3256/6056/;
  $dept =~ s/3546/7156/;
  $dept =~ s/I001/I000/;
  $dept =~ s/M000/I000/;
  $dept =~ s/M110/V000/;
  $dept =~ s/7206/3546/;
  $dept =~ s/Z121/I000/;
  $dept =~ s/7408/7406/;           ###  課程研究所
  $dept =~ s/B000/Z121/;	   ###  語言中心
  $dept =~ s/8100/4456/;	   ###  前瞻中心, 2015/05/13
  $dept =~ s/1406/1416/;        ###  台文所，2016/10/06
    
#  print("checking $dept  $id  $name ... <BR>\n");
#  if( $dept eq "B000" ) {
#    next;
#  }
  if( !defined($teacher_exist{$dept}{$id}) ) {
    $teacher_exist{$dept}{$id} = 1;
    $newline = join("	",$dept, $id, $name, $ename);
    print DEST ("$newline\n");
  }else{
#    print("teacher $dept  $id  $name already exists!<BR>\n");
  }
}


print ("<BODY background=\"../../../Graph/manager.jpg\">");
print ("<CENTER><H1>更新教師資料檔</H1><HR>\n");   
print ("已經將教師資料檔中的系所代碼做過轉換...<BR>\n");
print ("請繼續執行<BR><A href=Update_teacher03.cgi>更新資料第三步</A>");
                  

close DEST;
