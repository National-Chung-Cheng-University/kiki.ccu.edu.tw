#!/usr/local/bin/perl
###########################################################################
#####   Batch_Create_Password.pl
#####   �妸���;ǥͱK�X
#####   �ɮ׻ݨD: �@�Өt�һP�w���Ǹ�������
#####   �����ɮ�: ����[�t�Ҥ���W��, �Ǹ�, �K�X] ������;
#####             �g�J�ǥͱK�X��; �����s�W�ǥ͸�ƨ�student.txt,
#####             �ҥH���ݦA�s�W��student.txt�s�ͤ~�i�i�J�t��
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

###   ���L�e���, �q�ĤT��}�l, �Фp��!!
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
  print("���b�B�z[$dept]���ǥͱK�X���....\n");
  foreach $id (@range) {
    ($pass, $crypt) = Create_Random_Password();
    $student{id} = $id;
    $student{dept} = $dept;
    
    if( $id ne "") {
      Change_Student_Password($id, $dept, $crypt, $crypt);
      ## ���B���ɮ��v�����D, �������chmod 666
#      Add_Student(%student);
      print OUTFILE ("$id $pass $dept\n");
#      print OUTFILE ("$dept\t$id\t$pass\n");
#      print OUTFILE ("$dept\t$id\t$pass\t$crypt\n");
    }
  }
}




