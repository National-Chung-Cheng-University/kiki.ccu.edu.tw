1;

##################################################################################################
#####  Student.pm 處理學生資料
#####  Updates:
#####    19??/??/?? program by Ionic
#####    2009/06/05 在學籍資料檔中，新增註冊次數欄位 enrollnum，相關函式修改  Nidalap :D~
#####    2009/06/15 新增系所合一導致的問題，修改學生所屬系所若干函式。  Nidalap :D~
#####    2010/03/25 修改 Find_All_Student 加入系所參數，用以尋找該系底下的學生(取代 Find_All_Student_In_Dept) Nidalap :D~
#####    2010/12/29 新增應用英外語課程/修課抵畢業門檻名單讀取函式 Read_Apply_Eng_List()  Nidalap :D~
##################################################################################################
##########################################################################
####  Find_All_Student_In_Dept() by Nidalap, Jun03,1999
##########################################################################
sub Find_All_Student_In_Dept
{
  my($student_file, @line, @student, $j, $student, $in_dept, $dept);
  ($in_dept) = @_;
  @student = ();
  $student_file = $REFERENCE_PATH."student.txt";
  open(STUDENT, $student_file) or
     die("Cannot open file $student_file!\n");
  @line = <STUDENT>;
  close(STUDENT);
  foreach $line (@line) {
     ( $dept,$j,$j,$j,$j, $student, $j, $j, $j, $j, $j, $j) = split(/\s+/,$line);
     $dept =~ s/8$/6/;
     $dept = Determine_Student_Dept($dept);     ###  2009/06/15 系所合一 Nidalap :D~
     push(@student, $student)  if($dept eq $in_dept);
#     print("pushing $student<BR>\n") if($dept eq $in_dept);
  }
  return(@student);
}
###########################################################################
sub Find_All_Student
{
  my($filter_dept) = @_;
  my($student_file) = $REFERENCE_PATH . "student.txt";
  my($line,$i,@student,$junk, $temp_file, $student, $dept);
  if( $filter_dept eq "" ) {						###  要傳回所有學生清單
    open(STUDENTFILE,$student_file) or die("Cannot open file $student_file\n"); 
    $i=0;
    while( $line=<STUDENTFILE> )  {
      ( $junk,$junk,$junk,$junk,$junk, $student[$i++] , $junk, $junk, $junk, $junk, $junk )  = 
          split(/\s+/,$line);
    }
    close(STUDENTFILE);
  }else{								###  傳回特定系所學生清單
    die("系所代碼 $filter_dept 錯誤!") if(!is_Valid_Dept($filter_dept));	## 檢查 $filter_dept 是否合法
    
    if( not(-e $TEMP_PATH) ) {							## 若暫存目錄不存在，建立之
      mkdir($temp_file);
    }    
    $temp_file = $TEMP_PATH . "grep.tmp.txt";
#    print("grep \"$filter_dept\" $student_file > $temp_file\n");
    system("grep \"$filter_dept\" $student_file > $temp_file");
    open(STUDENTFILE,$temp_file) or die("Cannot open file $temp_file!\n");
    $i=0;
    while( $line=<STUDENTFILE> )  {
      ( $dept,$junk,$junk,$junk,$junk, $student , $junk, $junk, $junk, $junk, $junk)  =
         split(/\s+/,$line);
#      $dept =~ s/8$/6/;
#      $dept = Determine_Student_Dept($dept);     ###  2009/06/15 系所合一 Nidalap :D~
      push(@student, $student)  if($dept eq $filter_dept);
    }
    close(STUDENTFILE);    
  }
  return(@student);
}
##########################################################################
#####  為了效率, 將此函式改為讀取單行的學生資料檔.
#####  該檔由 ~/BIN/Update/Update_Student.pl 產生,
#####  舊函式暫改名為 Read_Student_old()
#####  Updates:2005/09/20 Nidalap :D~
sub Read_Student
{
  my(%student,$input_id,$line,$temp,$junk,%stu_dept);
  my($line, $last_digit, $student_found);
  ($input_id)=@_;
  my($student_file) = $REFERENCE_PATH . "Student/" . $input_id;
  
  my %system_settings = Read_System_Settings();

  open(STUDENTFILE,$student_file) or return 0;
  $line = <STUDENTFILE>;
  close(STUDENTFILE);
  ($student{dept},$student{grade},$student{class},$junk,$student{status},$student{id},
   $student{personal_id}, $student{sex}, $student{enrollnum}, $student{name}, $student{ename} )  = split(/\t/,$line);

  $student{'enrollnum'}++  if( $system_settings{'grade_upgrade'} == 1 );	###  2015/01/08 從 Determine_Student_Grade 中提出
  
  $student{dept} =~ s/8$/6/;
  $student{dept}  = Determine_Student_Dept($student{dept});	###  2009/06/15 系所合一 Nidalap :D~
  $student{grade} = Determine_Student_Grade($input_id, $student{enrollnum});   ###  改由註冊次數判斷年級 2009/06/05
#  $student{name} = join("", @stu_cname);
  $student{name} =~ s/ +//;
  
#  $student{name} =~ s/　+//;
#  $student{name} =~ s/　+//;

  if($student{name} ne "") {
    return(%student);
  }else{
    return 0;
  }
}
##########################################################################
#####  自 2005/09/20 後，即停止使用此函式  Nidalap :D~
sub Read_Student_old
{
  my($student_file) = $REFERENCE_PATH . "student.txt";
  my(%student,$input_id,$line,$temp,$junk,%stu_dept);
  my(@students, $last_digit, $student_found);
  ($input_id)=@_;

  open(STUDENTFILE,$student_file) or die("Cannot open file$student_file\n");
  @students = <STUDENTFILE>;
  close(STUDENTFILE);
  foreach $line (@students)  {
    ## 4154    4    A     Y     0    482415021   M   李永祥
    ( $student{dept},$student{grade},$student{class},$junk,$student{status},$student{id}, 
      $student{personal_id}, $student{sex}, $student{enrollnum}, $student{name}, $student{ename} )  =  split(/\s+/,$line);
    if( $student{id} eq $input_id )  {
      $student{dept} =~ s/8$/6/;
      #$student{name} = join("", @stu_cname);
      $student{name} =~ s/ +//;
      $student{name} =~ s/　+//;
      $student{name} =~ s/　+//;
      
      $student_found = 1;
      last;
    } 
  }

  if($student_found == 1) {
    return(%student);
  }else{
    return 0;
  }
}
############################################################################
#####  Read_All_Student_Data()
#####  找出所有學生詳細資料 %student
#####  因為有時用 Find_All_Student 和 Read_Student 反而花時間,
#####  此函式花費記憶體但減少大量disk IO
#####  Nidalap, Jul01,1999
############################################################################
sub Read_All_Student_Data
{
  my($student_file) = $REFERENCE_PATH . "student.txt";
  my($i, $line, $dept,$grade,$class,$junk,$status,$id, $sex, $enrollnum, $name, $ename);
  my($last_digit);
#  my(%S);

  my %system_settings = Read_System_Settings();
  
  open(STUDENTFILE,$student_file)  or
     die("Cannot open file $student_file\n");
  while( $line=<STUDENTFILE> )  {
    ## 41544    A  Y0    482415021   M   李永祥
    ($dept,$grade,$class,$junk,$status,$id,$personal_id,$sex,$enrollnum, $name, $ename) = split(/\t+/,$line);
    #$name = join("", @name);
    $last_digit = chop($dept);
    $last_digit = '6' if($last_digit eq '8');
    $dept = $dept . $last_digit;
    $dept = Determine_Student_Dept($dept);     ###  2009/06/15 系所合一 Nidalap :D~
    #$name =~ s/ +//;
    $name =~ s/　+//;
    $name =~ s/　+//;
    $$S{$id}{id}		= $id;
    $$S{$id}{dept}		= $dept; 
#    $$S{$id}{grade}		= Determine_Student_Grade($id, $enrollnum);   ###  要等 enrollnum 修正後才能判斷此變數！
    $$S{$id}{class}		= $class;
    $$S{$id}{personal_id}	= $personal_id; 
    $$S{$id}{sex}		= $sex;
    $$S{$id}{name}		= $name;    
	$$S{$id}{ename}		= $ename;  

	$enrollnum++		if( $system_settings{'grade_upgrade'} == 1 );	###  2015/01/08 從 Determine_Student_Grade 中提出	
	$$S{$id}{enrollnum}	= $enrollnum;
    $$S{$id}{grade}		= Determine_Student_Grade($id, $enrollnum);   ###  改由註冊次數判斷年級 2009/06/06	

#    print $id . "\n";
  }
#  print("I am $$S{686415016}{name}");
  return(%S);
}

############################################################################
#####  Read_All_Student_Data2()
#####  找出所有學生詳細資料 %student
#####  從 student_all.txt 讀取所有欄位(警告: 這個檔案不一定會記得更新 :P)
#####  Nidalap, 10/04/2002
#####  2013/08/22 停止維護此函式 Nidalap :D~
############################################################################
sub Read_All_Student_Data2
{
  my($student_file) = $REFERENCE_PATH . "student_all.txt";
  my($i, $line, $dept,$grade, $id, $sex, $name, $military, $j, @j);
  my($last_digit);

  open(STUDENTFILE,$student_file)  or
     die("Cannot open file$student_file\n");
  while( $line=<STUDENTFILE> )  {
    ($id,$personal_id,$dept,$name,$j,$sex,$j,$j,$j,$j,$j,$j,$j,$j,$j,$military,@j) =
        split(/\t/,$line);
    $last_digit = chop($dept);
    $last_digit = '6' if($last_digit eq '8');
    $dept = $dept . $last_digit;
    $name =~ s/ +//;
    $name =~ s/　+//;
    $name =~ s/　+//;
    $$XS{$id}{id}                = $id;
    $$XS{$id}{dept}              = $dept;
    $$XS{$id}{grade}             = $grade;
    $$XS{$id}{class}             = $class;
    $$XS{$id}{personal_id}       = $personal_id;
    $$XS{$id}{sex}               = $sex;
    $$XS{$id}{name}              = $name;
    $$XS{$id}{military}		 = $military;
  }
  return(%XS);
}
##################################################################################
#####  2009/06/05 廢除  Nidalap :D~
#sub Add_Student
#{
#  my(%s) = @_;      ##  %student
#  my($file);
#
#  $file = $REFERENCE_PATH . "student.txt";
#  open(FILE, ">>$file");
#  print FILE ("$s{dept}\t$s{grade}\t$s{class}\tN\t0\t$s{stu_id}\t$s{personal_id}\t?\t$s{name}\n");
#  close(FILE);
#}
########################################
### Add by ionic 99/9/16
### 此函數供系統篩選使用,找出轉學生名單
### 並將轉學生的學號記錄下來 
### ps. 此函數也提供選課時使用, 轉學生視同新生
### 傳回一 hash

sub Find_Change_School_Student
{
  my($limit_id) = @_;				###  限制學號前三碼
  my($student_file) = $REFERENCE_PATH . "Change_School_Student.txt";
  my($line,$i,%student,$junk,$grade,$temp);
  open(STUDENTFILE,$student_file)  or
            die("Cannot open file $student_file\n");
  $i=0;
  while( $line=<STUDENTFILE> )  {
    ## 4154    4    A     Y     0    482415021   M   李永祥
    ( $junk,$grade,$junk,$junk,$junk, $temp ,   $junk, $junk )  = 
        split(/\s+/,$line);
    if( $limit_id ne "" ) {			###  如果有限制學號前三碼
      $student{$temp}=1  if( $temp =~ /^$limit_id/ );
    }else{					###  如果要看所有轉學生
      $student{$temp}=1;
    }
  }
  close(STUDENTFILE);
  return(%student);
}
#############################################################################
#####

#############################################################################
#####  Read_Student_State_Files()
#####    讀入輔系及雙學位等名單檔
#####    輸入:(None)
#####    輸出:(None)
#####    需求: 輔系名單FU.txt, DOUBLE.txt
#####    影響:(Global variables:) %FU, %DOUBLE
#####    本函式是從系統篩選程式copy來的, 原來功能完全一樣
#####    Last update: 2002/02/26 Nidalap :D~
############################################################################
sub Read_Student_State_Files
{
  my(@line, $line);
  my($FUfile,$DOUBLEfile);

  $FUfile     = $REFERENCE_PATH . "fu.txt";
  $DOUBLEfile = $REFERENCE_PATH . "double.txt";
  open(FU,$FUfile)         or die("Cannot open file <$FUfile\n");
  @line = <FU>;
  close(FU);
  foreach $line (@line) {
    $line =~ s/\n//;
    $line =~ /(.*)\s+(\d+).*/;
    $FU{$2} = $1;
  }
  open(DOUBLE,$DOUBLEfile) or die("Cannot open file <$DOUBLEfile\n");
  @line = <DOUBLE>;
  close(DOUBLE);
  foreach $line (@line) {
    $line =~ s/\n//;
    $line=~/(.*)\s+(\d+).*/;
    $DOUBLE{$2} = $1;
  }
}
##############################################################################
#####  is_Teacher_Edu()
#####  讀取教育學程名單資料 $REFERENCE_PATH/teacher_edu.txt
#####  教育學程所開設課程, 只有通過教育學程審核者可以修習.
#####  本名單資料透過 cron 抓取 sybase 資料庫定期更新
#####  更新程式放在 ~/BIN/......
#####   Date: 2003/09/09
#####  Coder: Nidalap :D~
##############################################################################
sub is_Teacher_Edu
{
  my(@line, $line, $teacher_edu_file, %teacher_edu);
  my($junk, $id, $abandon_date, $type);
  my($stu_id) = @_;
  
  $teacher_edu_file = $REFERENCE_PATH . "teacher_edu.txt";
  open(TEACHER_EDU, $teacher_edu_file) or    ### die("Cannot open file $teacher_edu_file!");
                                       return(0);
  @line = <TEACHER_EDU>;
  close(TEACHER_EDU);
  foreach $line (@line) {
    $line =~ s/\n//;
    ($junk, $junk, $id, $junk, $junk, $abandon_date, $junk, $type) = split(/\t/, $line);
#    print("comparing $id ($abandon_date)...<BR>\n");
    if( $abandon_date eq "" or $abandon_date eq " " )  {          ###  放棄日期不可有資料
      return(1)  if($stu_id eq $id);
    }
  }
  return(0);
}
##############################################################################
#####  Read_Black_List()
#####  讀取選課黑名單.
#####  加選太多次的學生, 會被列入黑名單內, 用來警告使用者, 以提醒管理者用.
#####  此名單透過 ~/BIN/Cron_Jobs/cron_jobs 定期更新
#####   Date: 2005/03/21
#####  Coder: Nidalap :D~
sub Read_Black_List
{
  my($black_file, @list, @line);
  $black_file = $REFERENCE_PATH . "black_list.txt";
  open(BLACKLIST, $black_file);
  @line = <BLACKLIST>;
  close(BLACKLIST);
  foreach $line (@line) {
    ($line) = split(/ /, $line);
    push(@list, $line);
  }
  return(@list);
}
##############################################################################
#####  Verify_For_Graduate_pdf
#####  確認學生是否需要看畢業資格審查表
#####  三年級以上的大學生就要看
#####   Date: 2005/08/23
#####  Coder: Nidalap :D~
sub Verify_For_Graduate_pdf
{
  my($id, $grade) = @_;
#  print("$system_settings{allow_print_graduate_pdf}, $SUPERUSER<BR>\n");
  if( ($grade >= 3) and ($id =~ /^4/) ) {   ## 只影響大三以上的大學生
    my %change_school_stu = Find_Change_School_Student();
    return(0)  if( $change_school_stu{$id} == 1 );	##  轉學生不必看 2012/09/12
    if( ($system_settings{force_print_graduate_pdf} == 1) ) {
      return(2);  ### 強制要看才能加退選
    }elsif( ($system_settings{allow_print_graduate_pdf} == 1) or ($SUPERUSER == 1) ) {
      return(1);  ### 可以看
    }else{
      return(0);  ### 不必看
    }
  }
  return(0);      ### 不受影響
}
##############################################################################
#####  if_Confirmed_For_Graduate_pdf
#####  確認學生是否確認過畢業資格審查表
#####  Date: 2005/09/08
#####  Coder: Nidalap :D~
sub if_Confirmed_For_Graduate_pdf
{
  my($id) = @_;
  my($confirm_file, %time);

  $confirm_file = $DATA_PATH . "Graduate_PDF_Confirmation/" . $id;
#  print("confirm_file = $confirm_file<BR>\n");
  if( -e $confirm_file ) {
    return(1);
  }else{
    return(0);
  }
}

##############################################################################
#####  Confirm_For_Graduate_pdf
#####  讓學生確認畢業資格審查表
#####  Date: 2005/09/08
#####  Coder: Nidalap :D~
sub Confirm_For_Graduate_pdf
{
  my($id) = @_;
  my($confirm_file, %time, $log_file);

  $confirm_file = $DATA_PATH . "Graduate_PDF_Confirmation/" . $id;
#  print("confirm_file = $confirm_file<BR>\n");
  open(CONFIRMATION, ">$confirm_file");
  %time = gettime();
  print CONFIRMATION ("$time{time_string}\n");
  close(CONFIRMATION);

  ###  要寫 log
  $action = "Confirm";
  Student_Log($action, $id, "", "", "");
  return(1);
}

############################################################################################################
#####  Determine_Student_Grade
#####  由學生的學號、註冊次數、以及系統是否升級的設定，來判斷學生年級
#####  Updates:
#####    2009/06/05 開始使用  Nidalap :D~
#####    2013/01/11 升級設定由原本「升級年級」改為「升級註冊次數」，以符合實際需求 by Nidalap :D~  
#####    2015/01/08 把註冊次數是否加一的判斷做在 Read_Student() 和 Read_All_Student() 中 by Nidalap :D~
sub Determine_Student_Grade
{
  my($id, $enrollnum) = @_;
  my($grade, @grade_table);

  use POSIX;    
#  %system_settings = Read_System_Settings();		###  此處需要 require Common_Utility.pm
  
#  if( $system_settings{grade_upgrade} == 1 ) {		###  如果系統設定升級
#    $grade = ceil( ($enrollnum+1) / 2 );
#  }else{											###  如果系統設定不升級
    $grade = ceil( $enrollnum / 2 );
#  }
  
#  $grade = 2   if( ($grade == 1) and ($enrollnum == 2) );	###  20090909 違章建築!!!!!!!!!!!!!!!!!!
  
  if( $id =~ /^4/ ) {					###  大學生最高四年級
    $grade=4  if( $grade > 4 );
  }else{						###  碩博士生最高三年級
    $grade=3  if( $grade > 3 );
  }

  $grade=1  if( $grade == 0 );  			###  註冊次數為零的新生，為一年級
  return($grade);
}
  
###############################################################################################################
#####  Determine_Student_Dept
#####  將系所合一的系所代碼，轉換為相對應舊系所代碼。用於將學生所屬系所改為開課系所。
#####  Updates:
#####    2009/06/15 開始使用  Nidalap :D~
#####    2012/02/17 若沒有輸入 $dept_id，則傳回整個 %dept_com  Nidalap :D~
sub Determine_Student_Dept
{
  my($dept_id) = @_;

  my($dept_com_file, @temp, $deptcd, $com_deptcd, %dept_com); 

  $dept_com_file = $REFERENCE_PATH . "dept_com.txt";
  open(DEPT_COM, $dept_com_file) or die("Cannot open file $dept_com_file!\n");
  @temp = <DEPT_COM>;
  close(DEPT_COM);
  foreach $line (@temp) {
    ($deptcd, $com_deptcd) = split(/\s+/, $line);
    $dept_com{$com_deptcd} = $deptcd;
    if( $dept_id ne "" ) {
      if( $dept_id eq $com_deptcd ) {
        $dept_id = $deptcd;
        last;
      }
    }
  }
  if( $dept_id ne "" )	{  return($dept_id); }
  else			{  return %dept_com; }  
}

###############################################################################################################
#####  Determine_Dept_Student_Dept
#####  因系所合一，部份學生所屬系所與開課系所代碼不同(如英語教學所學生所屬 1376，開課代碼 1366)。
#####  此函式輸入開課系所代碼，傳回該系所擁有學生的代碼。 (其實就是 Determine_Student_Dept() 的相反 )
#####  Updates:
#####    2012/02/17 開始使用  Nidalap :D~
#####	 2015/06/08 因為專班的政治所用新代碼 3316 開課，搭了違章建築，讓這個特例不做轉換！  Nidalap XD~
sub Determine_Dept_Student_Dept
{
  my($stu_dept) = @_;
  my %dept_com, $dept;

  return $stu_dept  if( $IS_GRA and ($stu_dept eq "3316") );	###  20150608 違章建築，因為專班的政治所用新代碼 3316 開課！

  %dept_com = Determine_Student_Dept();

  foreach $dept (keys %dept_com) {
    if( $dept_com{$dept} eq $stu_dept) {
      return $dept;
    }
  }
  return $stu_dept;
}

###############################################################################################################
#####  Read_Apply_Eng_List
#####  應用英外語課程/修課抵畢業門檻名單讀取函式。
#####  Updates:
#####    2010/12/29 開始使用  Nidalap :D~
sub Read_Apply_Eng_List
{
  my(@class, @decuct, %class, %deduct, $y, $t, $id, $level);
  my $a14tapply_eng_class_file		= $REFERENCE_PATH . "a14tapply_eng_class.txt";
  my $a14tapply_eng_deduct_c_file	= $REFERENCE_PATH . "a14tapply_eng_deduct_c.txt";
  
  open(CLASS_FILE, $a14tapply_eng_class_file) or Fatal_Error("Cannot open file $a14tapply_eng_class_file!");
  open(DEDUCT_FILE, $a14tapply_eng_deduct_c_file) or Fatal_Error("Cannot open file $a14tapply_eng_deduct_c_file!");
  
  @class  = <CLASS_FILE>;
  @deduct = <DEDUCT_FILE>;
  close(CLASS_FILE);
  close(DEDUCT_FILE);
  
  foreach $class (@class) {
    ($y, $t, $id, $level) = split(/\s+/, $class);
	${$_[0]}{$id} = $level;
	$class{$id} = $level;
  }
  foreach $deduct (@deduct) {
    ($y, $t, $id, $level) = split(/\s+/, $deduct);
	${$_[1]}{$id} = $level;
	$deduct{$id} = $level;
  }
}
###############################################################################################################
#####  Early_Warning_21_Status
#####  傳回某學生的 21 預警輔導狀態
#####  傳回值： [0,1,-1] = ["尚未與導師洽談，不得選課", "已與導師洽談，可以選課", 不在名單內]
#####  Updates:
#####    2011/02/10 Created by Nidalap :D~
sub Early_Warning_21_Status
{
  my($in_id) = @_;
  my $ew_file = $REFERENCE_PATH . "Early_Warning_21_List.txt";
  my $y, $t;
  $status = -1;					### 預設：紀錄中查無此學號
  
  if( -e $ew_file ) {
    open(EW_FILE, $ew_file);
    @line = <EW_FILE>;
    close(EW_FILE);
    foreach $line (@line) {
      chomp($line);
      ($y, $t, $id, $temp_status) = split(/\t/, $line);
      if( $id eq $in_id ) {			### 找到該筆紀錄
        $status = $temp_status;
        last;
      }
    }
  }else{					### 紀錄檔案不存在！
    Fatal_Error("Cannot open file $ew_file!");
  }
  return $status;
}

#################################################################################################################
#####  Student_Suit_CGE_New_Category
#####  從學號判別學生是否適用2014通識新制（向度）
#####  此函式會有學號百年 BUG，當學號回到 x88xxxxxx 會判斷錯誤！
#####  不過那時候這個制度大概早死了（我也早退休了哇哈哈哈）！ 								2013/12/06 Nidalap :D~
sub Student_Suit_CGE_New_Category
{
  my($sid) = @_;
  
  $year_min = 03;							###  x03xxxxxx 以上（含）的學號才會 return 1
  $year_max = 88;							###  x88xxxxxx 以下（含）的學號才會 return 1
  
  $sid_year = substr($sid, 1, 2);
#  print "sid_year = $sid_year<BR>\n";
  return 1  if( $sid == '999999999' );

  if( ($sid_year >= $year_min) and ($sid_year<=$year_max) )  {
    return 1;
  }else{
    return 0;
  }
}
