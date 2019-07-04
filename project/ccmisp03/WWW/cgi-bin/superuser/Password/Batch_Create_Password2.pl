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

###   跳過第一行, 從第二行開始, 請小心!!
for($i=2; $line[$i] ne ""; $i++) {
  ($dept, $number) = split(/\s+/,$line[$i]);
  @id_range = Create_Range($dept, $number);
  Write_Outfile($dept, @id_range);
}
###########################################################################
###  Create_Range 編學號起迄
###  學號共有9碼: 
###      第1碼是身份(大, 碩, 博, 專班) = (4,6,8,5).
###         除專班外皆以系所代碼第四碼為準
###      第2~3碼是入學學年度, 由Reference.pm取得
###      第4~6碼是系所代碼前三碼
###      第7~9碼為流水號, 由1開始算
###########################################################################
sub Create_Range()
{
  my($dept, $number) = @_;
  my($start, $end, @range);
  return("")  if( $number eq "" );

  $dept =~ /(...)(.)/;
  if($SUB_SYSTEM eq "3") {	### 若是專班, 學號第一碼為5
    $start = "5";
  }else{			### 一般生則以系所代碼(4,6,8)=(大,碩,博)
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
  print("正在處理[$dept $dept{cname2}]的學生密碼資料....\n");
  foreach $id (@range) {
    ($pass, $crypt) = Create_Random_Password();
    $student{id} = $id;
    $student{dept} = $dept;
    
    if( $id ne "") {
       print("$dept --> $id\n");
#      Change_Student_Password($id, $dept, $crypt, $crypt);
      ## 此處有檔案權限問題, 仍須手動chmod 666
##      Add_Student(%student);
#      print OUTFILE ("$id $pass $dept\n");
##      print OUTFILE ("$dept\t$id\t$pass\n");
##      print OUTFILE ("$dept\t$id\t$pass\t$crypt\n");
    }
  }
}




