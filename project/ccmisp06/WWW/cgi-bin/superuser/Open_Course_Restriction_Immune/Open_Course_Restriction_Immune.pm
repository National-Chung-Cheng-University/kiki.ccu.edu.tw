1;

##############################################################################
sub Read_Immune_Record()
{
  my(@files, @line, @immune_list, $immune_path, $immune_file, $i);
  my($course_id, $course_group, $r1, $r2, $r3, $r4);
  my $immune_file = $REFERENCE_PATH . "Open_Course_Restriction_Immune.txt";
  open(IMMUNE, $immune_file);
  @line = <IMMUNE>;
  close(IMMUNE);
  $i = 0;
  foreach $line (@line) {
    ($course_id, $course_group, $r1, $r2, $r3, $r4) = split(/\t/, $line);
    ${$immune_list[$i]}{course_id}	= $course_id;
    ${$immune_list[$i]}{course_group}	= $course_group;
    ${$immune_list[$i]}{r1}		= $r1;
    ${$immune_list[$i]}{r2}             = $r2;
    ${$immune_list[$i]}{r3}             = $r3;
    ${$immune_list[$i]}{r4}             = $r4;
    $i++;
  }
  return(@immune_list);
}
##############################################################################
sub Add_Immune_Record()
{
  my($c_id, $c_group, $r1, $r2, $r3, $r4) = @_;
  my $immune_file = $REFERENCE_PATH . "Open_Course_Restriction_Immune.txt";
  my(@line);
  open(IMMUNE, $immune_file);
  @line = <IMMUNE>;
  close(IMMUNE);
  foreach $line (@line) {
    ($c_id_t, $c_group_t, @junk) = split(/\t/, $line);
    if( ($c_id eq $c_id_t) and ($c_group eq $c_group_t) ) {
      return(FALSE);
    }
  }
  open(IMMUNE, ">>$immune_file");
  print IMMUNE ("$c_id\t$c_group\t$r1\t$r2\t$r3\t$r4\n");
  close(IMMUNE);
  return(TRUE);
}
##############################################################################
sub Delete_Immune_Record()
{
  my(@line, @list);
  my($c_id, $c_group) = @_;
  my $immune_file = $REFERENCE_PATH . "Open_Course_Restriction_Immune.txt";
  
  if( -e($immune_file) ) {
    open(IMMUNE, $immune_file);
    @line = <IMMUNE>;
    foreach $line (sort @line) {
      ($c_id_t, $c_group_t, @junk) = split(/\t/, $line);
      if( not( ($c_id eq $c_id_t) and ($c_group eq $c_group_t) ) ) {
        push(@list, $line);
      }
    }
    close(IMMUNE);
    open(IMMUNE, ">$immune_file");
    foreach $id (@list) {
      print IMMUNE ("$id");
    }
    close(IMMUNE);
    print("資料已刪除!<BR>");
  }
}
##############################################################################
sub Form_Open_Course_Restriction_Immune_Table()
{
  my($table_content);
  @list = Read_Immune_Record();

  foreach $list (@list) {
#    $$list{course_id} =~ /^(....)/;
#    $dept = $1;
#    $dept =~ s/[123]$/4/;
#    $dept =~ s/5$/6/;
#    %course = Read_Course($dept, $$list{course_id},
#                          $$list{course_group}, "", "");
    $del_param = join("_", $$list{course_id}, $$list{course_group});
    $table_content .=
    qq(
      <TR>
        <TD><INPUT type=RADIO name=del_param value="$del_param"></TD>
        <TD>$$list{course_id}</TD>
        <TD>$$list{course_group}</TD>
        <TD>$$list{r1}</TD>
        <TD>$$list{r2}</TD>
        <TD>$$list{r3}</TD>
        <TD>$$list{r4}</TD>
      </TR>
    );
  }
  return($table_content);
}
##############################################################################
