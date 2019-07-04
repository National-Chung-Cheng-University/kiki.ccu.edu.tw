1;
######################################################
####    本模組主要包含確認開排課、及選課的狀態    ####
######################################################

sub Check_Dept_State
{
  my($Dept)=@_;
  my($FileName)=$REFERENCE_PATH."Dept_Control.map";
  open(FILE,"<$FileName")
                   or die("Cannot open file $FileName!\n");
  my(@MAP)=<FILE>;
  close(FILE);

  foreach $map(@MAP){
    $map=~s/\n//;
    ($dept,$state)=split(/\s+/,$map);
    if($dept eq $Dept){
      $State=$state;
    }
  }

  return($State);
}
