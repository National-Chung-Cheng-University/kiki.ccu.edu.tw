1;
############################################################
#####  Modify_Credit_Upper_Limit.pm
#####  個別學生學分上限修改(超修用)
#####  程式模組
#####  Coder: Nidalap :D~
#####  Date : 08/29/2001
############################################################
sub Read_Credit_Upper_Limit_Data
{
  my(%upper_limit, $temp_id, $temp_limit);
  my($upper_limit_file) = $REFERENCE_PATH . "credit_upper_limit.txt";
  open(LIMIT, $upper_limit_file);
  @line = <LIMIT>;
  $i = 0;
  foreach $line (@line) {
    $line =~ s/\n//;
    ($temp_id, $temp_limit) = split(/\s+/, $line);
    $upper_limit{$temp_id} = $temp_limit;
    $i++;
  }
  return(%upper_limit);
}
############################################################
sub Modify_Credit_Upper_Limit
{
  my(@line, @limit, $i, $found);
  my($upper_limit_file) = $REFERENCE_PATH . "credit_upper_limit.txt";
  my($id, $new_limit) = @_;

  if( ($id eq "") or ($new_limit == 0) ) {
    print("輸入資料不合法!<BR>\n");
    return();
  }
  
  open(LIMIT, $upper_limit_file);
  @line = <LIMIT>;
  $i = 0;
  foreach $line (@line) {
    $line =~ s/\n//;
    (${$limit[$i]}{id}, ${$limit[$i]}{limit}) = split(/\s+/, $line);
    $i++;
  }
  
  $found = 0;
  foreach $limit (@limit) {
    if($$limit{id} eq $id) {
      $found = 1;
      $$limit{limit} = $new_limit;
    }
  }
  if( $found == 0 ) {      ### 新增資料, 直接 append
    open(LIMIT, ">>$upper_limit_file");
    print LIMIT ("$id\t$new_limit\n");
    print("資料新增完成!");
  }else{                   ### 修改資料, 採用 write
    open(LIMIT, ">$upper_limit_file");
    foreach $limit (@limit) {
      print LIMIT ("$$limit{id}\t$$limit{limit}\n");
    }
    print("資料修改完成!");
  }
  close(LIMIT);

  return();
}
############################################################
sub Delete_Credit_Upper_Limit
{
  my(@limit);
  my($upper_limit_file) = $REFERENCE_PATH . "credit_upper_limit.txt";
  my($id) = @_;
  if( $id eq "" ) {
    print("請選擇要刪除的選項!<BR>\n");
    return();
  }

  open(LIMIT, $upper_limit_file);     ###  讀取資料
  @line = <LIMIT>;
  $i = 0;
  foreach $line (@line) {
    $line =~ s/\n//;
    (${$limit[$i]}{id}, ${$limit[$i]}{limit}) = split(/\s+/, $line);
    $i++;
  }
  open(LIMIT, ">$upper_limit_file");   ###  寫回資料
  foreach $limit (@limit) {
    next if( $$limit{id} eq $id );
    print LIMIT ("$$limit{id}\t$$limit{limit}\n");
  }

  print("資料順利刪除!<BR>\n");
  return();
}
############################################################
sub Form_Credit_Upper_Limit_Table
{
  my(%data) = @_;
  my($table_data);

  $table_data= "";
  foreach $id (keys %data) {
    %stu = Read_Student($id);
    %dept = Read_Dept($stu{dept});
    $table_data .= "<TR><TD><INPUT type=radio name=delete value=\"$id\"></TD>";
    $table_data .= "<TD>$id</TD><TD>$stu{name}</TD><TD>$dept{cname2}</TD><TD>$data{$id}</TD></TR>\n"; 
  }
  return($table_data);
}