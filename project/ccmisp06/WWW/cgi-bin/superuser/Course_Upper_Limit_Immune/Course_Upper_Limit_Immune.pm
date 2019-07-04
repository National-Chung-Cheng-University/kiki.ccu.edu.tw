1;

##############################################################################
sub Read_Immune_Record()
{
  my(@files, @line, @immune_list, $immune_path, $immune_file, $i);
  my($course_id, $course_group);
  my $immune_path = $DATA_PATH . "Course_Upper_Limit_Immune/" . $YEAR . "_" . $TERM . "/";
  opendir(IMMUNE_PATH, $immune_path);
  @files = readdir(IMMUNE_PATH);
  closedir(IMMUNE_PATH);
  $i=0;
  foreach $file (@files) {
    next if( ($file eq ".")or($file eq "..") );
    ($course_id, $course_group) = split(/_/, $file);
    $immune_file = $immune_path . $file;
    open(IMMUNE, $immune_file);
    @line = <IMMUNE>;
    close(IMMUNE);
    foreach $line (@line) {
      $line =~ s/\n//;
      ${$immune_list[$i]}{course_id}	= $course_id;
      ${$immune_list[$i]}{course_group}	= $course_group;
      ${$immune_list[$i]}{stu_id}	= $line;
      $i++;
    }
  }
  return(@immune_list);
}
##############################################################################
sub Add_Immune_Record()
{
  my($c_id, $c_group, $stu_id) = @_;
  my($immune_file) = $DATA_PATH . "Course_Upper_Limit_Immune/" . $YEAR . "_" . $TERM . "/" . 
                     $c_id . "_" . $c_group;
  my(@line);
  open(IMMUNE, $immune_file);
  @line = <IMMUNE>;
  close(IMMUNE);
  foreach $line (@line) {
    $line =~ s/\n//;
    return(FALSE)  if($line eq $stu_id);
  }
  open(IMMUNE, ">>$immune_file");
  print IMMUNE ("$stu_id\n");
  close(IMMUNE);
  return(TRUE);
}
##############################################################################
sub Delete_Immune_Record()
{
  my(@line, @list);
  my($c_id, $c_group, $stu_id) = @_;
  my($immune_file) = $DATA_PATH . "Course_Upper_Limit_Immune/" . $YEAR . "_" . $TERM . "/" . 
                     $c_id . "_" . $c_group;

  if( -e($immune_file) ) {
    open(IMMUNE, $immune_file);
    @line = <IMMUNE>;
    foreach $id (@line) {
      $id =~ s/\n//;
      push(@list, $id)  if( $id ne $stu_id );
    }
    close(IMMUNE);
    open(IMMUNE, ">$immune_file");    
    foreach $id (@list) {
      print IMMUNE ("$id\n");
    }
    close(IMMUNE);
    print("資料已刪除!<BR>");
  }else{
    print("該科目的加簽名單紀錄檔不存在!<BR>");
    exit(1);
  }
}
##############################################################################
sub Form_Course_Upper_Limit_Immune_Table()
{
  my($table_content, %stu);
  @list = Read_Immune_Record();
#  Read_All_Student_Data();

  foreach $list (@list) {
    $del_param = join("_", $$list{course_id}, $$list{course_group}, $$list{stu_id});
    %stu = Read_Student($$list{stu_id});
    $table_content .=
    qq(
      <TR>
        <TD><INPUT type=RADIO name=del_param value="$del_param"></TD>
        <TD>$$list{course_id}</TD>
        <TD>$$list{course_group}</TD>
        <TD>$$list{stu_id} $stu{name}</TD>
      </TR>
    );
  }
  return($table_content);
}
##############################################################################
