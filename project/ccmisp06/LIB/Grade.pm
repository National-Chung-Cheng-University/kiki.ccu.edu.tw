1;

###########################################################################################################
#####  Grade.pm
#####  存取學生成績資料檔
#####  Updates:
#####    2009/06/15 開始使用  Nidalap :D~
###########################################################################################################

###########################################################################################################
#####  Read_Grade
#####  從成績檔案中讀取(特定學生的)成績
#####  輸入：(當學期/歷年, 學號) <--- 可不輸入學號，則讀出所有學生成績
#####  輸出：%grade 成績資料
#####  Issues: 
#####    1. 應可改用 system grep 增進效能！
#####  Updates:
#####    2011/05/02 歷年成績資料改為從 $DARA_PATH/Grade/score/ 下讀取，不再用舊有的 all.txt
sub Read_Grade
{
  my($all_now, $in_stu_id) = @_;
  
  my($grade_file, @lines, $id, $year, $term, $c_id, $grp, $j, $grade, $credit);
  my(%grade);
    
  if( $all_now eq "NOW" ) {				### 當學期成績
    $grade_file = $DATA_PATH . "Grade/now.txt";
    open(GRADE, $grade_file) or die("Cannot open file $grade_file!\n");
    @lines = <GRADE>;
  }else{						### 歷年成績
    my $all_grade_path = $DATA_PATH . "Grade/score/";
    opendir(DIR, $all_grade_path) or die("Error opening dir $all_grade_path!\n");
    my @grade_files = readdir(DIR);
    foreach $grade_file (@grade_files) {
      if( $grade_file =~ /\d\d\d_\d/ ) {
        $grade_file = $all_grade_path . $grade_file;
#        print("reading $grade_file...\n");
        open(GRADE, $grade_file) or die("Error opening file $grade_file!\n");
        my @temp_grade_lines = <GRADE>;
        @lines = (@lines, @temp_grade_lines);
      }
    }
    closedir(DIR);
  }
  close(GRADE);
  
  foreach $line (@lines) {
    ($id, $year, $term, $c_id, $grp, $j, $j, $grade, $j, $j) = split(/\t/, $line);
    if( $in_stu_id ne "" ) {				###  如果要讀取特定學生成績
      if( $in_stu_id ne $id ) {
        next;						###    如果學號不一樣，next
      }
    }
#    $grade{$id}{$year}{$term}{$c_id} = $grade;
    $grade{$id}{$c_id} = $grade;   
#    print("$id -> $c_id -> $grade!\n");
  }
  return(%grade);
}
################################################################################
#####  Read_All_Grade()
#####  找出所有學生歷年/當學期/暑修/抵免成績, 並放入 %grade 中。
#####  若同一科目學生有修過數次, 以成績高者為準。
#####  此函式主用用作先修/重複篩選用。
#####  %grade 是一個 hash of hash, 存取方法是
#####     $grade{學生學號}{科目代碼} = 分數
#####  Updates:
#####    2011/05/02 從先修/重複篩選程式中，獨立出來此函式
################################################################################
sub Read_All_Grade
{
  my($grade_file, @grade_lines, %grade, $now_grade_lines, $summer_grade_lines);
  my($stu_id, $j, $course_id, $attr, $grade, @deduct, $temp);
  my(@grade_files, $all_grade_path);

  #####  讀取歷年成績
  $all_grade_path = $DATA_PATH . "Grade/score/";
  opendir(DIR, $all_grade_path) or die("Error opening dir $all_grade_path!\n");
  @grade_files = readdir(DIR);
  foreach $grade_file (@grade_files) {
    if( $grade_file =~ /\d\d\d_\d/ ) {
      $grade_file = $all_grade_path . $grade_file;
#      print("reading $grade_file...\n");
      open(GRADE, $grade_file) or die("Error opening file $grade_file!\n");
      @all_grade_lines = <GRADE>;
      @grade_lines = (@grade_lines, @all_grade_lines);
    }
  }
#  $grade_file = $DATA_PATH . "Grade/all.txt";
#  open(GRADE, $grade_file) or print("Error opening file!\n");
#  @grade_lines = <GRADE>;

  #####  讀取當學期成績
  $grade_file = $DATA_PATH . "Grade/now.txt";
  open(GRADE, $grade_file) or die("Error opening file $grade_file!\n");
  @now_grade_lines = <GRADE>;
  @grade_lines = (@grade_lines, @now_grade_lines);

  #####  讀取暑修成績
  $grade_file = $DATA_PATH . "Grade/summer.txt";
  open(GRADE, $grade_file) or die("Error opening file $grade_file!\n");
  @summer_grade_lines = <GRADE>;
  @grade_lines = (@grade_lines, @summer_grade_lines);

  #####  讀取抵免檔
  $grade_file = $DATA_PATH . "Grade/deduct.txt";
  open(GRADE, $grade_file) or die("Error opening file $grade_file!\n");
  @deduct = <GRADE>;
  close(GRADE);
  $default_grade = 70;                        ###  轉學抵免無成績, 預設為及格
  foreach $line (@deduct) {
    ($stu_id, $j, $j, $j, $course_id, $j) = split(/\t/, $line);
    $temp = join("\t", $stu_id, "test", "test", $course_id, "test", "test",
                 "test", $default_grade, "test");
    push(@grade_lines, $temp);
#    print("$temp\n") if($stu_id eq "488225062");
  }

  foreach $grade_line (@grade_lines) {
    ($stu_id, $j, $j, $course_id, $j, $j, $attr, $grade, $j) = split(/\s+/, $grade_line);
    next if( $attr == 9 );                            ### 棄選不算選過

    if( $course_id =~ /^9022/ ) {                   ### 如果是大二體育課: 不得重複修習大二體育課
      if( $course_id =~ /[24680]$/ ) {              ###   尾碼雙號是上學期
        $course_id = "90220";
      }else{                                        ###   尾碼單號是下學期
        $course_id = "90221";
      }
    }

    if( defined($grade{$stu_id}{$course_id}) ) {      ### 如果該成績早已讀入
      if( $grade{$stu_id}{$course_id} < $grade ) {    ### 如果第二次修課成績較高
        $grade{$stu_id}{$course_id} = $grade;         ###   取代較低分數
      }
    }else{                                            ### 如果該成績尚未讀入
      $grade{$stu_id}{$course_id} = $grade;
    }
  }
  return(%grade);
}
################################################################################
#####  將課程別名代碼的成績取較大值
#####  讀取所有課程別名檔中的科目代碼，將學生得到的最高分帶出
#####  傳入：無，但需要全域變數 %course_alias 和 %grade
#####  傳回：無，但是會竄改全域變數 %grade
#####  Updates:
#####    2011/05/02 從先修/重複篩選程式中，獨立出來此函式
sub Substitute_Alias_Grade
{
  foreach $old_cid (keys %course_alias) {
    foreach $sid (keys %grades) {
      foreach $cid (keys %{$grades{$sid}}) {
        if( $cid eq $old_cid) {
          if( $grades{$sid}{$cid} >= $grades{$sid}{$course_alias{$old_cid}{'new_id'}} ) {	### if 學生曾在舊科碼得過較高成績
            $grades{$sid}{$course_alias{$old_cid}{'new_id'}} = $grades{$sid}{$cid};		###   set 新成績 = 舊成績
          }else{
            $grades{$sid}{$cid} = $grades{$sid}{$course_alias{$old_cid}{'new_id'}};		### else 對調
          }
#          print("$sid      got $grades{$sid}{$cid} in $cid \n");
#          print("$sid also got $grades{$sid}{$course_alias{$old_cid}{'new_id'}} in $course_alias{$old_cid}{'new_id'}\n");
        }
      }
    }
  }
}
