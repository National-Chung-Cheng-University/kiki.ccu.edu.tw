1;
#############################################################################
#####  System_Settings.pm
#####  系統相關設定
#####  一些系統相關設定資料的讀取, 另有部分存於 Reference.pm 中
#####  Coder: Nidalap :D~
#####   Date: 2002/06/06
#############################################################################

sub Read_System_Settings
{
  my(%flags, @lines, $key, $value, $temp);
  my($state_file);
  
  ###  讀取 System_Settings.txt
  $state_file = $REFERENCE_PATH . "System_Settings.txt";
  open(SYS_SETTINGS, $state_file) or die("Cannot open system state file! abort!!<BR>\n");
  @lines = <SYS_SETTINGS>;
  close(SYS_SETTINGS);
  foreach $line (@lines) {
    $line =~ s/\n//;
    ($key, $value) = split("\t", $line);
    $flags{$key} = $value;
  }
  ###  讀取 SysState
  $state_file = $REFERENCE_PATH . "Basic/SysState";
  open(SYSSTATE, $state_file) or die("Internal error: Cannot read state_file!\n");
  $temp = <SYSSTATE>;
  close(SYSSTATE);
  $flags{sysstate} = chomp($temp);
  ###  讀取 LimitNumberState (限修人數控管機制： [0,1,2] = [不限修, 考慮保留人數, 僅考慮限修人數])
  $state_file = $REFERENCE_PATH . "Basic/LimitNumberState";
  open(LIMITNUMBERSTATE, $state_file) or die("Internal error: Cannot read state_file!\n");
  $temp = <LIMITNUMBERSTATE>;
  close(LIMITNUMBERSTATE);
  $flags{limit_number_state} = $temp;

#  foreach $k (keys %flags) {
#    print "$k : $flags{$k}<BR>\n";
#  }

  return(%flags);
}
##############################################################################
sub Write_System_Settings
{
  my %flags = @_;
  my($setting_file);

  $setting_file = $REFERENCE_PATH . "System_Settings.txt";
  open(SYS_SETTINGS, ">$setting_file")
    or print("Cannot open system setting file! abort!!<BR>\n");
  foreach $key (sort keys %flags) {
    next if($key eq "modify_flag");
    print SYS_SETTINGS ("$key\t$flags{$key}\n");
  }
  close(SYS_SETTINGS);
  return(%flags);
}
##############################################################################
#####  是否升級
#####  舊的設定檔，還沒時間整合。
#####  此函式是從 Add_Course01.cgi 搬過來的  2009/06/04  Nidalap :D~
sub is_Grade_Update
{
  my($FileName)=$REFERENCE_PATH."Basic/GradeState";
  open(FILE,"<$FileName")
                   or die("Cannot open file $FileName!\n");
  $State=<FILE>;
  close(FILE);

  return($State);
}


