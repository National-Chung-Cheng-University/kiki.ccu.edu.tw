#!/usr/local/bin/perl
###########################################################################
#####   Batch_Create_Password.pl
#####   批次產生學生密碼
#####   檔案需求: 一個系所與預估學號對應表
#####   產生檔案: 產生[系所中文名稱, 學號, 密碼] 對應檔;
#####             寫入學生密碼檔; 但不新增學生資料到student.txt,
#####             所以仍需再新增到student.txt新生才可進入系統
#####   Coder: Nidalap
#####   Date : Jun 02,1999
###########################################################################
require "/ultra2/project/ccmisp06/LIB/Reference.pm";
#require $LIBRARY_PATH."Student.txt";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Error_Message.pm";


$infile  = $REFERENCE_PATH."pre_student.txt";
$outfile = $REFERENCE_PATH."pre_password.txt";
#$infile   = $REFERENCE_PATH."pre_law.txt";
#$outfile = $REFERENCE_PATH."pre_law_password.txt";

open(INFILE, $infile) or die("Fatal: Cannot read file $infile!\n");
@line = <INFILE>;
close(INFILE);
open(OUTFILE,">$outfile") or die("Fatal: Cannot write file $outfile!\n");
print OUTFILE ("\n");

###   跳過前兩行, 從第三行開始, 請小心!!
for($i=2; $line[$i] ne ""; $i++) {
  ($dept, $id_range1, $id_range2) = split(/\s+/,$line[$i]);
  @id_range1 = Create_Range($id_range1);
  @id_range2 = Create_Range($id_range2);
  Write_Outfile($dept, @id_range1, @id_range2);
}
###########################################################################
sub Create_Range()
{
  my($range) = @_;
  my($start, $end, @range);
  $range =~ s/\s//;
  return("")  if( $range eq "" );
  
  ($start, $end) = split(/~/, $range);
  while( $start <= $end ) {
    push(@range, $start);
    $start++;
  }
  return(@range);
}
###########################################################################
sub Write_Outfile()
{  
  my($dept, @range) = @_;
  my($pass, $crypt,%student);
  print("正在處理[$dept]的學生密碼資料....\n");
  foreach $id (@range) {
    ($pass, $crypt) = Create_Random_Password();
    $student{id} = $id;
    $student{dept} = $dept;
    
    if( $id ne "") {
      Change_Student_Password($id, $dept, $crypt, $crypt);
      ## 此處有檔案權限問題, 仍須手動chmod 666
#      Add_Student(%student);
      print OUTFILE ("$id $pass $dept\n");
#      print OUTFILE ("$dept\t$id\t$pass\n");
#      print OUTFILE ("$dept\t$id\t$pass\t$crypt\n");
    }
  }
}




