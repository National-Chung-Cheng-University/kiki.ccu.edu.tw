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
require "../../LIB/Reference.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Error_Message.pm";

$infile  = $REFERENCE_PATH."pre_student2.txt";
$outfile = $REFERENCE_PATH."pre_password2.txt";

open(INFILE, $infile) or die("Fatal: Cannot read file $infile!\n");
@line = <INFILE>;
close(INFILE);
open(OUTFILE,">$outfile") or die("Fatal: Cannot write file $outfile!\n");
print OUTFILE ("\n");

###   ���L�Ĥ@��, �q�ĤG��}�l, �Фp��!!
for($i=2; $line[$i] ne ""; $i++) {
  ($dept, $number) = split(/\s+/,$line[$i]);
  @id_range = Create_Range($dept, $number);
  Write_Outfile($dept, @id_range);
}
###########################################################################
###  Create_Range �s�Ǹ��_��
###  �Ǹ��@��9�X: 
###      ��1�X�O����(�j, ��, ��, �M�Z) = (4,6,8,5).
###         ���M�Z�~�ҥH�t�ҥN�X�ĥ|�X����
###      ��2~3�X�O�J�ǾǦ~��, ��Reference.pm���o
###      ��4~6�X�O�t�ҥN�X�e�T�X
###      ��7~9�X���y����, ��1�}�l��
###########################################################################
sub Create_Range()
{
  my($dept, $number) = @_;
  my($start, $end, @range);
  return("")  if( $number eq "" );

  $dept =~ /(...)(.)/;
  if($SUB_SYSTEM eq "3") {	### �Y�O�M�Z, �Ǹ��Ĥ@�X��5
    $start = "5";
  }else{			### �@��ͫh�H�t�ҥN�X(4,6,8)=(�j,��,��)
    $start = $2;
  }
  $start .= $YEAR;
  $start .= $1;
  $start .= "001";
  
  $end = $start + $number;

  print("start = $start;  end = $end; number=$number\n");

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
  %dept = Read_Dept($dept);
  print("���b�B�z[$dept $dept{cname2}]���ǥͱK�X���....\n");
  foreach $id (@range) {
    ($pass, $crypt) = Create_Random_Password();
    $student{id} = $id;
    $student{dept} = $dept;
    
    if( $id ne "") {
       print("$dept --> $id\n");
#      Change_Student_Password($id, $dept, $crypt, $crypt);
      ## ���B���ɮ��v�����D, �������chmod 666
##      Add_Student(%student);
#      print OUTFILE ("$id $pass $dept\n");
##      print OUTFILE ("$dept\t$id\t$pass\n");
##      print OUTFILE ("$dept\t$id\t$pass\t$crypt\n");
    }
  }
}




