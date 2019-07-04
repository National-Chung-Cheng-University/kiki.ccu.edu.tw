#!/usr/local/bin/perl
1;

###########################################################################
#####     Course.pm
#####     處理開課相關資料
#####     Coder: Nidalap
#####     Date : Dec 28,1998
#####     Updates:
#####       2009/12/31 將原先讀取舊學期資料所傳入的 $yearterm 改為 $year 和 $term, 以避免民國百年 bug.  Nidalap :D~
#####       ...
#####       2012/04/11 新增欄位 attr: [1,2,3,N] = [碩士班課程, 博士班課程, 碩博合開, 不適用]. Nidalap :D~
###########################################################################
###########################################################################
#####  Find_All_Course()
#####  找出某系所所有開課資料. 其中第二項輸入值$history_flag表示要
#####  讀取的是某學年學期的開課歷史資料.
#####  Updates:
#####    199x/xx/xx Created
#####    2015/04/14 新增 in_open_dept 輸入參數以及相關判斷 by Nidalap :D~
###########################################################################
sub Find_All_Course
{
  my($dept, $input_grade, $year, $term, $history_flag, $in_open_dept);
  my($course_path, $index_file); 
  my(@lines, $id, $grade, $group, @course, $i);

  ($dept, $input_grade, $year, $term, $in_open_dept) = @_;
  #print "[dept, input_grade, year, term, in_open_dept] = [$dept, $input_grade, $year, $term, $in_open_dept]<BR>\n";
  
  $year=$YEAR  if($year eq "");
  $term=$TERM  if($term eq "");
   if( ($year eq "history") or ($year eq "HISTORY") ) {			  ### 所有歷年開課檔
      $course_path = $HISTORY_PATH."Course/".$dept."/";   
   }elsif( $year eq "change" ) {                                          ### 開課異動前的開課檔
      $course_path = $CHANGE_COURSE_PATH . $dept . "/";
   }elsif( not(($year eq $YEAR)and($term eq $TERM))) {                    ### 特定某學期開課資料  
      $course_path = $HISTORY_PATH . "Course_last/" . $year . "_" . $term . "/" . $dept . "/";  
   }else{								  ### 目前開課檔
      $course_path = $COURSE_PATH.$dept."/";
   }

  #print("Find_All_Course: Trying to locate $course_path<BR>\n");
  
  $index_file = $course_path . "classindex";
  return()  if( not(-e $index_file) );
  open(INDEX,"$index_file") or 
     print("Cannot open file $index_file in Course::Find_All_Course");
#  print("INDEX = $index_file");
  @lines = <INDEX>;
  close(INDEX);
  $i = 0;

  foreach $line (@lines) {
#    print("$line <p>");
    $line =~ s/\n//;
    ($id, $grade, $group, $open_dept) = split(/\s+/,$line);
	
	#print "[id, grade, group, open_dept] = [" . join(", ", $id, $grade, $group, $open_dept) . "]<BR>\n";
	
    if( $grade eq $input_grade || $input_grade eq "" ) {					###  過濾年級
#	  print("[in_open_dept, open_dept] = [$in_open_dept, $open_dept]<BR>\n");
	  if( $in_open_dept eq $open_dept || $in_open_dept eq "" ) {			###  過濾實際開課系所
        $course[$i]{id}    = $id;
#       $course[$i]{grade} = $grade;      ## Add by hanchu @ 1999/3/20
        $course[$i]{group} = $group;
	    $course[$i]{open_dept} = $open_dept;		### 2015/04 加入，實際開課系所代碼(文學院委由各系所開課需求)。
        $i++;
	  }
    }
  }
  return(@course);
}
###########################################################################
#####  Read_All_Course_Dept
#####  讀取所有科目的所屬系所
#####  同 Read_Course_Dont_Know_Dept 用意, 但此函式讀取所有開課資料,
#####  並將開課系所紀錄在 hash 中, 如此便可知道某們課開在哪個系所
#####  Updates: 
#####    2003/09/30 Created by Nidalap XD~
#####    2015/05/04 新增 $history 輸入參數，用以判斷是否抓取歷年科目 by Nidalap :D~
###########################################################################
sub Read_All_Course_Dept()
{
  my(@dept, @course, %course_dept);
  my($history) = @_;
    
  @dept = Find_All_Dept();
  foreach $dept (@dept) {
    @course = Find_All_Course($dept, "", $history);	
    foreach $course (@course) {
      %course = Read_Course($dept, $$course{id}, $$course{group}, "", "");
      $$course_dept{$$course{id}}{dept}     = $dept;
      $$course_dept{$$course{id}}{property} = $course{property};
	  
	  #print $$course{id} . " : " . $dept . " : " . $$course_dept{$$course{id}}{dept} . "<BR>\n";
    }
  }
  
  #print "course dept = " . %course_dept;

  return(%course_dept);
}
###########################################################################
#####  Read_Course_Dont_Know_Dept
#####  由於一開始的設計有問題, 要讀取科目資料必須知道開課系所,
#####  此函式是補救用的, 但如果科目代碼與系所代碼沒有照規則的話,
#####  這個函式則找不到資料.
#####  Date: 04/16/2002 Nidalap XD~
###########################################################################
#sub Read_Course_Dont_Know_Dept()
#{
#  my($dept, %course);
#  my($id,$group,$history_flag, $stu_id) = @_;
#  $course{id} =~ /^(....)/;
#  $dept = $1;
#  $dept =~ s/[123]$/4/;
#  $dept =~ s/5$/6/;
#
#  %course = Read_Course($dept, $id, $group, $history_flag, $stu_id);
#  return(%course);
#}
###########################################################################
###########################################################################
#####     Read_Course()
#####     讀取單一科目資料
#####     ps.未完成!!!  <--- 早完成了啦!!!
###########################################################################
sub Read_Course
{
   require $LIBRARY_PATH."Error_Message.pm";   #### Add by hanchu @ 1999/3/19
   my(%course, $history_flag, $course_exists_flag);
   my($course_path, $course_file, @lines, $temp, $i, $j, $id, $grade, $group);
   my($dept_temp, $pre_course_temp, $grade_temp);
   
   ($course{dept},$course{id},$course{group},$year, $term, $stu_id) = @_;
   
   $history_file_test = $HISTORY_PATH."Course/".$course{dept}."/".$course{id}."_01";
   if( not (-e $history_file_test) ) {	$course{isNEW} = "TRUE";  }
   else {								$course{isNEW} = "FALSE";   }

  $year=$YEAR  if($year eq "");
  $term=$TERM  if($term eq "");   

#  print("$course{dept},$course{id},$course{group},$year, $term, $stu_id<BR>\n");

   if( ($year eq "history") or ($year eq "HISTORY") ) {				### 所有歷年開課檔
      if( -e $history_file_test )  {
	  	$course_path = $HISTORY_PATH."Course/".$course{dept}."/";		## 如果歷年開課檔存在，讀取之
	  }else{
	    $course_path = $COURSE_PATH . $course{dept} . "/";				## 如果不存在（新開課程），讀取目前開課檔
	  }
   }elsif( $year eq "change" ) {									### 開課異動前的開課檔
      $course_path = $CHANGE_COURSE_PATH . $course{dept} . "/";
   }elsif( not(($year eq $YEAR)and($term eq $TERM))) {				### 特定某學期開課資料
      $course_path = $HISTORY_PATH . "Course_last/" . $year . "_" . $term . "/" . $course{dept} . "/";
   }else{															### 目前開課檔
      $course_path = $COURSE_PATH.$course{dept}."/";
   }
   
   #print("Read_Course: Trying to locate $course_path<BR>\n")  if ( $course{id} eq '1101951' );
   
   $index_file = $course_path . "classindex";
   open(INDEX, $index_file) or 
     return();
#     print("Cannot open file $index_file in Course::Read_Course() from $stu_id!<BR>\n");
   @lines = <INDEX>;
   close(INDEX);
   foreach $line (@lines) {
     ($id, $grade, $group, $open_dept) = split(/\t/, $line);
	 
#	 print "($id , $grade , $group , $open_dept)<BR>\n";
#	 print "-> " . join(", ", $course{id}, $id, $course{group}, $group, "<BR>\n");
	 
     if( ($course{id} eq $id) and ($course{group} eq $group) ) {
       $course_exists_flag = 1;
       $course{grade}=$grade;
     }
   }
  
   if( $course_exists_flag !=1 )  {		### 如果在 classindex 中沒有讀到該課程
     $course{cname}	=	"<FONT color=RED>(此科目已取消)</FONT>";
	 #if ( $course{id} eq '1101951' ) {
	 #  $tmp = join(" : ", "id, group = ", $course{dept},$course{id},$course{group},$year, $term, $stu_id, $course_path, "<HR>\n");
	 #  print "NOT FOUND: $tmp<BR>\n";
	 #  die();
	 #}
	 return(%course);
   }
   $course_file = $course_path . $course{id} . "_" . $course{group};
   
#   print("Trying to read course file $course_file<BR>\n");
   
   open(COURSE,$course_file) or 
     return();
#     Fatal_Error("Cannot find file $course_file in Course::Read_Course()!\n");
   @lines = <COURSE>;
   close(COURSE);
   
#   print "course file lines = " . @lines . "<BR>\n";
   
   foreach $line (@lines) {
     $line =~ s/\n//;
   }
   $course{cname}	=	$lines[0];   
   $course{ename}	=	$lines[1];
   $course{total_time}  =       $lines[2];   ### 發現時數和學分顛倒!!!
   $course{credit}	=	$lines[3];   ### Nov22,1999發現並修正(Nidalap)
   $course{classroom}	=	$lines[4];
   $course{property}	=	$lines[5];
   $temp		=	$lines[6];
      if( $temp ne "\n") {
	    @{$course{teacher}} = split(/\s+/, $temp);
	  }else{
	    @{$course{teacher}} = ("99999");
	  }
	  #####  用來修正第一次批次開課程式BUG問題
	  @tmp = ();
	  foreach $tea(@{$course{teacher}}) {
	    if( $tea !~ /^HASH/ ) {
		  push(@tmp, $tea);
		}
	  }
	  @{$course{teacher}} = @tmp;
	  
#   $course{time}	=	$lines[7];
   $temp		=	$lines[7];
      @temp = split(/\s+/,$temp);
      for($i=0, $j=0; defined($temp[$j]); $i++, $j+=2) {
         $course{time}[$i]{week} = $temp[$j];
         $course{time}[$i]{time} = $temp[$j+1];
      }
      #####					2009/05/10 終於搞定，知道怎麼對這樣的資料結構做 sort  Nidalap :D~
      @{$course{time}}	=	sort { 
                                      if( $$a{week} eq $$b{week} )	{ return ( $$a{time} cmp $$b{time} );  }
                                      else				{ return ( $$a{week} cmp $$b{week} );  }
                                     }  @{$course{time}}; 
      
   $course{number_limit} =	$lines[8];
   $course{number_limit} = 0  if( $course{id} eq Get_Dept_Serv_Course_ID($course{dept}));	### 系所服務學習課程，將限修人數強制設定為0
   
   @{$course{support_dept}} = split(/\s+/,$lines[9]);
   @{$course{support_grade}} = split(/\s+/,$lines[10]);
   @{$course{support_class}} = split(/\s+/,$lines[11]);
#     if( (@{$course{support_dept}}!=0) and (@{$course{support_class}}==0) ) {
#       @{$course{support_class}} = @AVAILABLE_CLASSES;		### 若勾選支援系所卻沒有溝選支援班級，預設為全部
#     }
   @{$course{ban_dept}} = split(/\s+/,$lines[12]);
   @{$course{ban_grade}} = split(/\s+/,$lines[13]);
   @{$course{ban_class}} = split(/\s+/,$lines[14]);
   $course{reserved_number} =	$lines[15];
   $course{principle}	=	$lines[16];
   $course{suffix_cd}	=	$lines[17];	### Apr,2000加入此欄位
   $course{lab_time1}   =       $lines[18];     ### Apr,2000加入此欄位
   $course{lab_time2}   =       $lines[19];     ### Apr,2000加入此欄位
   $course{lab_time3}   =       $lines[20];     ### Apr,2000加入此欄位
   $course{support_cge_type} =	$lines[21];	### Nov,2000加入支援通識領域
   $course{support_cge_number}=	$lines[22];	### Nov,2000加入支援通識人數
   @temp  = split(/\s+/,$lines[23]);  ### Nov,2000加入先修科目,Apr2001修改
   for($i=0; defined($temp[$i]); $i++) {
     ($dept_temp, $pre_course_temp, $grade_temp) = split(/,/,$temp[$i]);
     $course{prerequisite_course}[$i]{dept} = $dept_temp;
     $course{prerequisite_course}[$i]{id}   = $pre_course_temp;
     $course{prerequisite_course}[$i]{grade}= $grade_temp;
#     if($grade_temp == pass) {
#       $course{prerequisite_course}[$i]{grade_show} = "及格";
#     }elsif( $grade_temp == 0 ){
#       $course{prerequisite_course}[$i]{grade_show} = "曾經修習";
#     }else{
#       $course{prerequisite_course}[$i]{grade_show} = "$grade_temp分以上";
#     }
   }
   $course{prerequisite_logic}	= $lines[24];
   $course{distant_learning}	= $lines[25];
   $course{english_teaching}	= $lines[26];
   $course{remedy}		= $lines[27];	###  2009/05 加入，暑修課程類型(1為一般，2為補救)
   $course{s_match}		= $lines[28];   ###  2010/03 加入，教師專長與授課科目是否符合
   $course{gender_eq}		= $lines[29];	###  2010/11 加入，性別平等教育課程(0,1)
   $course{env_edu}		= $lines[30];	###  2010/11 加入，環境教育相關課程(0,1)
   $course{attr}		= $lines[31];	###  2012/04 加入，開課學制(碩士/博士/碩博合開課程)(1,2,3,N)
   $course{reserved2}		= $lines[32];
   $course{reserved3}		= $lines[33];
   $course{reserved4}		= $lines[34];
   for( $i=35; defined($lines[$i]); $i++) {	### 備註
      $course{note}	=	$course{note} . $lines[$i];	
   }

   $course{ename} =~ s/\n//;    ### 2005/11/24 發現奇怪bug的修正

 #  print("[ename = $course{ename}]<BR>\n");
   return(%course);
}
#############################################################################################
sub  Sort_Course_Time
{
  my (@time) = @_;
  
  return(@time)

}
###########################################################################
sub Modify_Course
{
  my($operation, %course);
  my($course_file, $index_file);
  my(@dept, @line, $new_line);
  
  ($operation, %course) = @_;
  if( $operation eq "" ) {
    return("ERROR: No operation in Course::Modify_Course!");
  }
  if( ($course{id} eq "") ||($course{group} eq "") ) {
    return("ERROR:Null course id or group input in Course::Modify_Course!");
  }
  
  $course_file = $COURSE_PATH.$course{dept}."/".$course{id}."_".$course{group};

  if( ($operation eq "add") and (-e $course_file ) ) {
    return("ERROR: Course file $course_file already exists in Course::Modify_Course!");
  }
  if( ($operation eq "batch") and (-e $course_file ) ) {
    return("ERROR: Course file $course_file already exists in Course::Modify_Course!");
  }
  if( ($operation eq "modify") and not(-e $course_file) ) {
    return("ERROR: Course file $course_file not found in Course::Modify_Course!");
  }
  
  my $course_path_check = $COURSE_PATH.$course{dept};     ### 若系所目錄不存在 -> 建立目錄
  if( not( -e $course_path_check ) ) {
    mkdir($course_path_check, 0777);
  }
  $index_file = $COURSE_PATH.$course{dept}."/classindex";
  
  #print "index_file = $index_file<BR>\n";
  
  umask(000);  #  if(not( -e $index_file ));
  open(INDEX, $index_file)
    or Fatal_Error("ERROR: Cannot open file $index_file in Course::Modify_Course!");
  @line = <INDEX>;
  close(INDEX);
  $new_line = join("\t", $course{id},$course{grade},$course{group},$course{open_dept});
  push(@line,$new_line) if ( ($operation eq "add") or ($operation eq "batch") );
  foreach $line (@line) {
    $line =~ s/\n//;
    $line .= "\n";
  }
  ######  依照科目代碼排序，但系所服務學習課程優先  Added 20110426 by Nidalap :D~
  @line = sort { 
                 if   ($a =~ /$DEPT_SERV_CODE/) { return -1;} 
                 elsif($b =~ /$DEPT_SERV_CODE/) { return 1; }
                 else                           { return $a cmp $b;}
               } @line;

  open(INDEX, ">$index_file")
    or Fatal_Error("ERROR: Cannot write to file $index_file in Course::Modify_Course!\n");
  foreach $line (@line) {
    print INDEX $line;
  }
  close(INDEX);
  $course{time} =~ s/ /\t/g;

#  print "course_file = $course_file<BR>\n";
  
  open(COURSE,">$course_file") or 
     Fatal_Error("ERROR: Cannot write to file $course_file in Course::Modify_Course()!\n");
  print COURSE ("$course{cname}\n");
  print COURSE ("$course{ename}\n");
  print COURSE ("$course{total_time}\n");
  print COURSE ("$course{credit}\n");
  print COURSE ("$course{classroom}\n");
  print COURSE ("$course{property}\n");
  foreach $teacher ( @{$course{teacher}} ) {
    print COURSE ("$teacher\t");
  } 
  print COURSE ("\n");
  for($i=0; $course{time}[$i]{week} ne ""; $i++) {
    print COURSE ("$course{time}[$i]{week}\t$course{time}[$i]{time}");
    print COURSE ("\t") if ($course{time}[$i+1]{week} ne "");
  }
  print COURSE ("\n");

#  print COURSE ("$course{time}\n");
  print COURSE ("$course{number_limit}\n");
  foreach $temp ( @{$course{support_dept}} ) {
    print COURSE ("$temp\t");
  }
  print COURSE ("\n");
  foreach $temp ( @{$course{support_grade}} ) {
    print COURSE ("$temp\t");
  }
  print COURSE ("\n");
  foreach $temp ( @{$course{support_class}} ) {
    print COURSE ("$temp\t");
  }
  print COURSE ("\n");
  foreach $temp ( @{$course{ban_dept}} ) {
    print COURSE ("$temp\t");
  }
  print COURSE ("\n");
  foreach $temp ( @{$course{ban_grade}} ) {
    print COURSE ("$temp\t");
  }
  print COURSE ("\n");
  foreach $temp ( @{$course{ban_class}} ) {
    print COURSE ("$temp\t");
  }
  print COURSE ("\n");
  print COURSE ("$course{reserved_number}\n");
  print COURSE ("$course{principle}\n");
  print COURSE ("$course{suffix_cd}\n");	###  Apr.2000加入 Nidalap
  print COURSE ("$course{lab_time1}\n");  	###  Apr.2000加入 Nidalap
  print COURSE ("$course{lab_time2}\n");  	###  Apr.2000加入 Nidalap
  print COURSE ("$course{lab_time3}\n");  	###  Apr.2000加入 Nidalap
  print COURSE ("$course{support_cge_type}\n");	###  Nov,2000加入 Nidalap :D
  print COURSE ("$course{support_cge_number}\n"); ###  Nov,2000加入 Nidalap :D
  foreach $temp ( @{$course{prerequisite_course}} ) {  ###  Nov,2000加入,Apr2001修改 Nidalap :D~
    print COURSE ("$$temp{dept},$$temp{id},$$temp{grade}\t");
  }
  print COURSE ("\n");
  print COURSE ("$course{prerequisite_logic}\n");
  print COURSE ("$course{distant_learning}\n");
  print COURSE ("$course{english_teaching}\n");
  print COURSE ("$course{remedy}\n");		###  2009/05 加入，暑修課程類型(1為一般，2為補救)
  print COURSE ("$course{s_match}\n");		###  2010/03 加入，教師專長與授課科目是否符合
  print COURSE ("$course{gender_eq}\n");	###  2010/11 加入，性別平等教育課程(0,1)
  print COURSE ("$course{env_edu}\n");		###  2010/11 加入，環境教育相關課程(0,1)
  print COURSE ("$course{attr}\n");		###  2012/04 加入，開課學制(碩士/博士/碩博合開課程)(1,2,3,N)
  print COURSE ("$course{reserved2}\n");
  print COURSE ("$course{reserved3}\n");
  print COURSE ("$course{reserved4}\n");
  
  print COURSE ("$course{note}");
  close COURSE;
  if($operation eq "add") {
    Dept_Log("CREATE", $course{dept}, $course{id}, $course{group}, $course{open_dept});
  }elsif( $operation eq "batch") {
    Dept_Log("BATCH", $course{dept}, $course{id}, $course{group}, $course{open_dept});
  }else{
    Dept_Log("MODIFY", $course{dept}, $course{id}, $course{group}, $course{open_dept});
  }

  return("TRUE");
}
###########################################################################
sub Delete_Course
{
  my( $id, $group, $dept, $open_dept );
  my( $index_file, $course_file, @line, $course_line, $i, $j);
  my($cid_, $grade_, $grp_, $open_dept_);
  ($id, $group, $dept) = @_;

  $course_file = $COURSE_PATH.$dept."/".$id."_".$group;
  
  return("NOT_FOUND")  if( not(-e $course_file) );
  $index_file = $COURSE_PATH.$dept."/classindex";
  open(INDEX,$index_file) 
     or Fatal_Error("Cannot open file $index_file in Course::Delete_Course()");
  @line = <INDEX>;
  close(INDEX);

  while( defined($line[$i]) ) {
    $line[$i] =~ s/\n//;
	($cid_, $grade_, $grp_, $open_dept_) = split(/\t/, $line[$i]);
    if( ($cid_ eq $id) and ($grp_ eq $group) ) {
#      print("Hello! $line[$i]<br>");
#      @line = splice(@line, $i, "", @line);
      for( $j=$i; defined($line[$j+1]); $j++ ) {
        $line[$j] = $line[$j+1];
      }
    }
    $line .= "\n";
    $i++;
  }
  open(INDEX, ">$index_file") 
     or Fatal_Error("Cannot open file >$index_file in Course::Delete_Course()");
  $i=0; 
  foreach $line (@line) {
    $line .= "\n"  if($line !~ /\n/); 
    if(defined($line[$i+1])) {
      print INDEX $line;
    }
    $i++; 
  }
  close(INDEX);
  unlink($course_file)
     or Fatal_Error("Cannot unlink file $course_file in Course::Delete_Course()");
  Dept_Log("DELETE", $dept, $id, $group, $open_dept);
  
#  foreach $line (@line) {
#    print("<font color=RED>") if( $line =~ /$id/ );
#    print("$line<br>");
#  }
  
  
  return("TRUE");
}
###########################################################################
#####  Read_Cge()
#####  讀取通識代碼, 由內部代碼帶出次領域代碼及中文名稱
#####  Date : Nov04, 2000
#####  Coder: Nidalap
###########################################################################
sub Read_Cge
{
  my($cge_file, %cge, @temp, $internal_id, $cge_id, $sub_cge_id, $cge_name);
  $cge_file = $REFERENCE_PATH . "cge2.txt";
  open(CGE, $cge_file) or
      Fatal_Error("Cannot open file cge2.txt in Course::Read_Cge()!");
  @temp = <CGE>;
  close(CGE);
  foreach $temp (@temp) {
    ($sub_cge_id, $cge_name) = split(/\s/, $temp);

    $sub_cge_id =~ /.(.)../;
    $cge{$sub_cge_id}{cge_id}		  = $1;  ### 主領域代碼是次領域代碼的第二碼
    $cge{$sub_cge_id}{cge_name}           = $cge_name;
    if( $sub_cge_id eq "0") {                  ### 如果不支援, 則不show代碼
      $cge{$sub_cge_id}{sub_cge_id_show}  = "";
    }else{
      $cge{$sub_cge_id}{sub_cge_id_show}  = "(" . $sub_cge_id . ")";
    }
  }
  return(%cge);
}
###########################################################################
#####  Is_Current_Dept_Only()
#####  是否限本系
#####  由 @{$course{ban_dept}} 檢查該課目是否限本系生修,
#####  若是則傳回1, 否則傳回0
#####  Date : Dec 06,2000
#####  Coder: Nidalap :D~
###########################################################################
sub Is_Current_Dept_Only
{
  my(%course) = @_;
  my(@all_dept) = Find_All_Dept();
  my(%ban_dept, $same_dept);
  my $is_current_dept_only_flag = 1;            ### 預設為傳回1(限本系修)
  $course{dept} =~ /^(...)/;                    ### Match最前面三碼, 視為同系(所)
  $same_dept = $1;

  foreach $dept (@all_dept) {                   ### 預設所有系所不擋修
    $ban_dept{$dept} = 0;
  }
  foreach $ban_dept (@{$course{ban_dept}}) {   
    $ban_dept{$ban_dept} = 1;                   ### 設定所有擋修的系所
  }
  foreach $dept (keys %ban_dept) {
    if( $dept =~ /$same_dept/ ) {
      next;
    }
    if($ban_dept{$dept} == 0) {
      $is_current_dept_only_flag = 0;           ### 只要有一個外系沒擋就設為0
    }else{
#      print("$dept banned\n");
    }
  }
  return($is_current_dept_only_flag);
}
###########################################################################
#####  Read_History_Course()
#####  因為Read_Course內若要讀取歷年檔, 需要知道開課系所, 頗不方便
#####  而該函式所讀的資料又是從 DATA/Transfer/allcourse.txt 來的,
#####  所以不如直接讀這個檔.
#####  這是半實驗性質的函式, 所以還不敢取代Read_Course讀歷年檔的部份.
#####  Date: Jul 20,2000
#####  Coder:Nidalap
###########################################################################
sub Read_History_Course
{
  my($allcourse, @lines, $in_course_id, $in_group);
  my(%C, $tmp, @tmp);                           ###  以較短的%C代替%course
  
  ($in_course_id, $in_group) = @_;
  $allcourse = $DATA_PATH . "Transfer/allcourse.txt";
  open(ALLCOURSE, $allcourse) or Fatal_Error("Cannot open file $allcourse in Course::Read_History_Course()");
  @lines = <ALLCOURSE>;
  foreach $line (@lines) {
    ($tmp, $C{id}, $tmp, $C{group}, @tmp) = split(/\s+/, $line);
    if( ($C{id} eq $in_course_id) and ($C{group} eq $in_group) ) {
      ($C{dept}, $C{id}, $tmp, $C{group}, $C{credit}, $C{total_time}, 
       $C{property}, $tmp, $C{cname}, @tmp) = split(/\s+/, $line);
      $C{ename} = join("", $tmp);
      return(%C);
    }
  }
}
###########################################################################
#####  Read_All_History_Course()
#####  在少數需要一次讀進所有開課歷年資料的情形下, 這個函式可一次全部讀入,
#####  以大量記憶體換取處理時間. 資料直接來自 DATA/Transfer/allcourse.txt
#####  Date: Apr 18,2001
#####  Coder:Nidalap
###########################################################################
sub Read_All_History_Course
{
  my($allcourse, @lines);
  my(@C, $tmp, @tmp, $i, $linecount);                           ###  以較短的%C代替%course

  ($in_course_id, $in_group) = @_;
  $allcourse = $DATA_PATH . "Transfer/allcourse.txt";
  open(ALLCOURSE, $allcourse) or Fatal_Error("Cannot open file $allcourse in Course::Read_All_History_Course()");
  @lines = <ALLCOURSE>;

  $linecount = @lines;
  for($i=0, $j=0; $i<$linecount; $i++) {
    $lines[$i] =~ s/\n//;
    ($C[$j]{dept}, $C[$j]{id}, $tmp, $C[$j]{group}, $C[$j]{credit}, $C[$j]{total_time},
     $C[$j]{property}, $tmp, $tmp, $C[$j]{cname}, @tmp) = split(/\t/, $lines[$i]);
  
    next  if( ($C[$j]{id} eq $C[$j-1]{id}) and ($i!=0) );
    $C[$j]{ename} = join("", @tmp);
#    print("$C[$j]{dept}, $C[$j]{id}, $C[$i]{group}\n");
    $j++;
  }
  return(@C);
}
################################################################################################
#####  Course_of_Teacher()
#####  找出該教師當學期開的所有課程.
#####  由於系統架構之故，本函式必須掃過當學期所有開課資料，故執行無效率，謹慎使用之！
#####  Date: 2009/05/08  Nidalap :D~
sub Course_of_Teacher
{
  my($teacher, $limit_dept) = @_;
  my @course_of_teacher, $i=0;
  my @dept, %dept, @course, %course;
  
#  print("Trying to find course of teacher $teacher...<BR>\n");
  @dept = Find_All_Dept();
  foreach $dept (@dept) {
#    print("scanning $dept for $teacher...<BR>\n");
    @course = Find_All_Course($dept);
    foreach $course (@course) {
      %course = Read_Course($dept, $$course{id}, $$course{group});
      foreach $teacher_of_course (@{$course{teacher}}) {
        if($teacher_of_course eq $teacher) {
#          print("teacher $teacher has a course $course{id} _ $course{group}<BR>\n");
          $course_of_teacher[$i]{dept}	= $dept;
          $course_of_teacher[$i]{id}	= $course{id};
          $course_of_teacher[$i]{group}	= $course{group};
          $i++;
        }
      }
    }
  }
  return(@course_of_teacher);
}

##################################################################################################
#####  Read_a30tcourse()
#####  讀取 a30tcourse 資料(科目代碼檔).
#####  包含所有 "曾經開過的課", 甚至包括不曾開成功的課.
#####  因為不曾開成功的課, 在 allcourse 中找不到, 
#####  所以這裡的目的是為了開課時, 能夠避開已經使用過的科碼.
#####  Date: 2008/06/05
#####  Nidalap :D~
sub Read_a30tcourse_
{
  my($a30tcourse, @lines, $i, $temp, @a);
  
  $a30tcourse = $REFERENCE_PATH . "a30tcourse.txt";
  open(A30TCOURSE, $a30tcourse) or Fatal_Error("Cannot open file $a30tcourse in Course::Read_All_History_Course()");
  
  @lines = <A30TCOURSE>;
  foreach $line (@lines) {
    $line =~ s/\n//;
    ($a[$i]{id}, $temp, $a[$i]{cname}, $a[$i]{ename}, $a[$i]{credit}) = split(/\t/, $line);
    $i++;
  }
  return(@a);
}
############################################################################
sub Read_a30tcourse
{
  my($a30tcourse, @lines, $temp, %a);
  my($id, $cname, $ename, $credit);

  $a30tcourse = $REFERENCE_PATH . "a30tcourse.txt";
  open(A30TCOURSE, $a30tcourse) or Fatal_Error("Cannot open file $a30tcourse in Course::Read_All_History_Course()");

  @lines = <A30TCOURSE>;
  foreach $line (@lines) {
    $line =~ s/\n//;
    ($id, $temp, $cname, $ename, $credit) = split(/\t/, $line);
    $a{$id}{id}		= $id;
    $a{$id}{cname}	= $cname;
    $a{$id}{ename}	= $ename;
    $a{$id}{credit}	= $credit;
  }
  return(%a);
}

############################################################################
#####  Print_Timetable()
#####
############################################################################

sub Print_Timetable
{
#  use encoding 'big5', STDIN => 'big5', STDOUT => 'big5';
  my(%cell) = @_;                ###  要先執行 Format_Time()
  my @txt;
  
  if( $IS_ENGLISH ) {
    @txt = ('Day','Period');
	@weekday = @WEEKDAY_E;
  }else{
    @txt = ('星期','區段');
	@weekday = @WEEKDAY;
  }
  my($day, $region, $bgc, $time_table);
  
  $bgc2 = "bgcolor=YELLOW"; 
  $bgc  = "bgcolor=ORANGE";

  $time_table = "
    <TABLE border=12>
      <TR>
        <TH $bgc>" . $txt[0] . "/<BR>" . $txt[1] . "</TH>
        <TH $bgc>" . $weekday[1] . "</TH>
        <TH $bgc>" . $weekday[2] . "</TH>
        <TH $bgc>" . $weekday[3] . "</TH>
        <TH $bgc>" . $weekday[4] . "</TH>
        <TH $bgc>" . $weekday[5] . "</TH>
        <TH $bgc>" . $weekday[6] . "</TH>
        <TH $bgc>" . $weekday[7] . "</TH>
      </TR>
  ";
  for($region=0; $region<5; $region++) {
    $table_of_region = Table_of_Region($region);
    $time_table = $time_table . "<TR valign=CENTER><TH $bgc2> " 
                . $table_of_region . "</TH>";
#    print qq(
#      <TR valign=CENTER>
#        <TH $bgc2>
#          &nbsp<BR>$REGION[$region]<BR>
#          <FONT size=1>($REGION_TIME[$region])</FONT>
#        </TH>
#    );
    for($day=1; $day<=7; $day++) {
      if($cell{$day}{$region} ne "") {
        $time_table = $time_table . "<TD align=LEFT>" . $cell{$day}{$region} . "</TD>";
      }else{
        $time_table = $time_table . "<TD>&nbsp</TD>";
      }
#      print("[$day, $region] = $cell{$day}{$region}<BR>\n");
    }
    $time_table = $time_table . "</TR>";
  }
  $time_table = $time_table . "</TABLE>";
  return($time_table);
}
############################################################################
sub Format_Time
{
  my(@selected_time) = @_;
  my(%cell, $region);
  
  foreach $time (@selected_time) {
    $region = $REGION_TIME_TABLE{$$time{time}};
     if( $cell{$$time{week}}{$region} ne "" ) {
       $cell{$$time{week}}{$region} .= "<BR>";
     }
    $cell{$$time{week}}{$region} = $cell{$$time{week}}{$region} . 
                                   "<FONT size=2>(" . $$time{time} . ")" . $$time{course};
#    $cell{$$time{week}}{$region} .= $$time{time};
#    print("[$$time{week}, $region] = $$time{time}<BR>\n");
  }
  return(%cell);  
}
###########################################################################
####  功課表左側區段與節次的部份
sub Table_of_Region
{
  my($region) = @_;
  my $table_data, @txt;
  my @cell, $fs = "<FONT size=1>";
  my $td2 = "<TD rowspan=2 bgcolor=ORANGE align=CENTER>";
  my $td3 = "<TD rowspan=3 bgcolor=ORANGE align=CENTER>";
  
  if( $IS_ENGLISH ) {
    @txt = ('', '');
  }else{
    @txt = ('第', '節');
  }
  
  $cell[0] = { "50" => {"name" => [1,2,3], 
                        "time" => ["07:10<BR>~<BR>08:00", "08:10<BR>~<BR>09:00", "09:10<BR>~<BR>10:00"]},
               "75" => {"name" => [A,B], 
                        "time" => ["07:15<BR>~<BR>08:30", "08:45<BR>~<BR>10:00"]} };
  $cell[1] = { "50" => {"name" => [4,5,6], 
                        "time" => ["10:10<BR>~<BR>11:00", "11:10<BR>~<BR>12:00", "12:10<BR>~<BR>13:00"]},
               "75" => {"name" => [C,D], 
                        "time" => ["10:15<BR>~<BR>11:30", "11:45<BR>~<BR>13:00"]} };
  $cell[2] = { "50" => {"name" => [7,8,9], 
                        "time" => ["13:10<BR>~<BR>14:00", "14:10<BR>~<BR>15:00", "15:10<BR>~<BR>16:00"]},
               "75" => {"name" => [E,F], 
                        "time" => ["13:15<BR>~<BR>14:30", "14:45<BR>~<BR>16:00"]} };
  $cell[3] = { "50" => {"name" => [10,11,12], 
                        "time" => ["16:10<BR>~<BR>17:00", "17:10<BR>~<BR>18:00", "18:10<BR>~<BR>19:00"]},
               "75" => {"name" => [G,H], 
                        "time" => ["16:15<BR>~<BR>17:30", "17:45<BR>~<BR>19:00"]} };
  $cell[4] = { "50" => {"name" => [13,14,15], 
                        "time" => ["19:10<BR>~<BR>20:00", "20:10<BR>~<BR>21:00", "21:10<BR>~<BR>22:00"]},
               "75" => {"name" => [I,J], 
                        "time" => ["19:15<BR>~<BR>20:30", "20:45<BR>~<BR>22:00"]} };

  foreach $ele (@{cell}) {
    foreach $time ( @{${$ele{50}}{time}} ) {
      $time =~ s/~/<BR>~<BR>/;
      print $time;
    }
  }

  $r = $region;
  $table_data = "<TABLE border=0 width=100%><TR><TD bgcolor=ORANGE rowspan=6>";
  $table_data = $table_data . $REGION[$region];
  $table_data = $table_data . "</TD>$td2$fs" . $txt[0] . "<BR>" . ${${${$cell[$r]}{50}}{name}}[0] . "<BR>" . $txt[1];
  $table_data = $table_data . "</TD>$td2$fs" . ${${${$cell[$r]}{50}}{time}}[0];
  $table_data = $table_data . "</TD>$td3$fs" . $txt[0] . "<BR>" . ${${${$cell[$r]}{75}}{name}}[0] . "<BR>" . $txt[1];
  $table_data = $table_data . "</TD><TD rowspan=3 bgcolor=ORANGE>$fs" . ${${${$cell[$r]}{75}}{time}}[0];
  $table_data = $table_data . "</TD></TR><TR></TR><TR>";
  $table_data = $table_data . "$td2$fs" . $txt[0] . "<BR>" . ${${${$cell[$r]}{50}}{name}}[1] . "<BR>" . $txt[1];
  $table_data = $table_data . "</TD>$td2$fs" . ${${${$cell[$r]}{50}}{time}}[1];
  $table_data = $table_data . "</TD></TR><TR>";
  $table_data = $table_data . "</TD>$td3$fs" . $txt[0] . "<BR>" . ${${${$cell[$r]}{75}}{name}}[1] . "<BR>" . $txt[1];
  $table_data = $table_data . "</TD>$td3$fs" . ${${${$cell[$r]}{75}}{time}}[1]; 
  $table_data = $table_data . "</TD></TR><TR>";         
  $table_data = $table_data . "$td2$fs" . $txt[0] . "<BR>" . ${${${$cell[$r]}{50}}{name}}[2] . "<BR>" . $txt[1]; 
  $table_data = $table_data . "</TD>$td2$fs" . ${${${$cell[$r]}{50}}{time}}[2];

  $table_data .= "</TR></TABLE>";

  return($table_data);
}
###########################################################################
#####  將開課資料的備註資料轉換為純文字型態
#####  2015/08/24 從 Create_Course_View.cgi 搬過來，並且加入英文版  by Nidalap :D~
sub Format_Note_String()
{
  my(%course) = @_;
  my $note_string = "";  my $note_string_e;
  my($temp_dept);

  if( (${${$course{prerequisite_course}}[0]}{dept} ne "99999") and (${${$course{prerequisite_course}}[0]}{dept} ne "") ) {
    $note_string		.= "<b>先修科目</b>";
	$note_string_e	.= "<b>Prerequisite Courses: </b>";
    foreach $pre_course (@{$course{prerequisite_course}}) {
      %pre_course = Read_Course( $$pre_course{dept}, $$pre_course{id}, "01" ,"history");
      $note_string		.= "(" . $$pre_course{id} . ")" . $pre_course{cname} . "(" . $GRADE{$$pre_course{grade}} . ")" . " ";
	  $note_string_e	.= "(" . $$pre_course{id} . ")" . $pre_course{ename} . "(" . $GRADE_E{$$pre_course{grade}} . ")" . " ";
    }
    if( $course{prerequisite_logic} and defined(${${$course{prerequisite_course}}[1]}{dept}) ) {
      $note_string		.= "($PREREQUISITE_LOGIC{$course{prerequisite_logic}})";
	  $note_string_e	.= "($PREREQUISITE_LOGIC_E{$course{prerequisite_logic}})";
    }
  }

  if ( $course{reserved_number} != 0 ) {
    $note_string		.= "保留新生$course{reserved_number}人; ";
	$note_string_e	.= "$course{reserved_number} preserved for 1st graders; ";
  }
  if( $dept eq $DEPT_CGE ) {				###  通識課要顯示擋修系所 2010/05/20 Nidalap :D~
    if( ${$course{ban_dept}}[0] ne "" ) {
      $note_string	.= "擋修";
	  $note_string_E.= " Forbidden:  ";
      foreach $dept (@{$course{ban_dept}}) {
        %temp_dept = Read_Dept($dept); 
        $note_string		.= $temp_dept{cname2};
		$note_string_E	.= $temp_dept{ename};
      }
      foreach $grade (@{$course{ban_grade}}) {
        $note_string		.= $GRADE[$grade];
		$note_string_e	.= $GRADE_E[$grade];
      }
      foreach $class (@{$course{ban_class}}) {
        $note_string		.= $class . "班";
		$note_string_e	.= $class . " class ";
      }
      $note_string 		.= "; ";
	  $note_string_e	.= "; ";
    }
    $note_string		=~ s/;\s$//;
    $note_string		.= ".";
	$note_string_e	=~ s/;\s$//;
    $note_string_e	.= ".";
  }

  if( ${$course{support_dept}}[0] ne "" ) {		###  支援系所年級班級
    $note_string		.= "支援";
	$note_string_e	.= " This course is for: ";
    foreach $dept (@{$course{support_dept}}) {
      %temp_dept = Read_Dept($dept);
      $note_string		.= $temp_dept{cname2};
	  $note_string_e	.= $temp_dept{ename};
    }
    foreach $grade (@{$course{support_grade}}) {
      $note_string		.= $GRADE[$grade];
	  $note_string_e	.= $GRADE_E[$grade];
    }
    foreach $class (@{$course{support_class}}) {
      $note_string		.= $class . "班";
	  $note_string_e	.= $class . " class ";
    }
    $note_string		.= "; ";
	$note_string_e	.= "; ";
  }
  $note_string		=~ s/;\s$//;
  $note_string_e	=~ s/;\s$//;
  $note_string		.= "."  if($note_string    =~ /支/);
  $note_string_e	.= "."  if($note_string_e =~ /Support/);
  $ban_num = @{$course{ban_dept}};
  if( ($ban_num > 30) and ( ($SUB_SYSTEM==1)or($SUB_SYSTEM==1)) ) {
     $note_string		.= "限本系生修.";         ### 權宜之計Nidalap,May11,1999
                                                  ### 2016/12/27 依淳純要求，從 50 人門檻改為 30 人 by Nidalap :D~
	 $note_string_e	.= "Not available for students from other departments.";         ### 權宜之計Nidalap,May11,1999
	 
#     if( $course{dept} !~ /[25].../) {      ### 理, 管院不顯示增加20%給外系文字
#     $note_string .= "於加退選期間開放供外系選修;";		###  2007/09/21 拿掉
#     }
#     $note_string .= $course{note};
  }
#  if( $course{distant_learning} == 1 ) {
#    $note_string .= "本科目為遠距教學課程;";
#  }
#  if( $course{english_teaching} == 1 ) {
#    $note_string .= "本科目為全英語授課;";
#  }

  #####  如果是學系服務學習課程，依照學期顯示不同訊息
  $dept_serv_course_id = Get_Dept_Serv_Course_ID($course{dept});
  if( $dept_serv_course_id eq $course{id} ) {
    if( $TERM == 1 ) {
      $temp = "單號";
	  $temp_e = " odd ";
    }else{
      $temp = "雙號";
	  $temp_e = " even ";
    }
    $note_string		.= "限本系一年級" . $temp . "學生修讀;";
	$note_string_e	.= "For 1st graders of " . $temp_e . "student ID of this department only;";
  }


  #####  (暑修的)第一類/第二類課程  Added 2009/05/22 Nidalap :D~
  if( is_Summer() and !is_GRA() ) {       ### 只作用於「一般生暑修」
    @flag_remedy = ("",
        "第一類課程：經系（所、中心）課程委員會議審議通過之選修課程",
        "第二類課程：曾開授之課程，以補救教學為原則");
    $note_string .= $flag_remedy[$course{remedy}];
  }
  
  foreach $gro_cour (@gro_cour) {
#  print("$course{id} eq $$gro_cour{cour_cd}?\n");
    next if($$gro_cour{gro_no} eq "80");		### 已經不使用的領域 added 20080822
    if( $course{id} eq $$gro_cour{cour_cd} ) {
      $note_string		.=  "<A href=\"" . "../cgi-bin/class/" . "Show_All_GRO.cgi\"> ,列入" .  $gro_name{$$gro_cour{gro_no}}{gro_name} . "科目</A>";
	  $note_string_e	.=  "<A href=\"" . "../cgi-bin/class/" . "Show_All_GRO.cgi\"> ,Included in " .  $gro_name{$$gro_cour{gro_no}}{gro_e_name} . "</A>";
    }
  }
  
  $note_string		.= $course{note};
  $note_string_e	.= $course{note};
  
  return($note_string, $note_string_e);
}


####################################################################################################
#####  Read_GRO
#####  讀取學程資料(不是教育學程, 而是各系所特定領域學程)
#####  傳回: 寫入 global variable: %gro_name, @gro_dept, @gro_cour
#####  2008/05/28, Nidalap :D~
sub Read_GRO
{
  my($gro_name_file, $gro_dept_file, $gro_cour_file);
  my(@lines, $gro_no, $gro_name, $gro_e_name, $dept, $temp, $cour_cd, @temp);
#  my(%gro_name, %gro_dept, %gro_cour);
  
  $gro_name_file = $REFERENCE_PATH . "gro_name.txt";
  $gro_dept_file = $REFERENCE_PATH . "gro_dept.txt";
  $gro_cour_file = $REFERENCE_PATH . "gro_cour.txt";
  
  open(GRO_NAME, $gro_name_file);				###  %gro_name
  @lines = <GRO_NAME>;
  foreach $line (@lines) {
    $line =~ s/\n//;
    ($gro_no, $gro_name, @temp) = split(/\s+/, $line);
    next if ($gro_no =~ /^8/ );						###  舊的研究所學程, 略掉
    $gro_e_name = join(" ", @temp);
    $gro_name{$gro_no}{"gro_name"}	= $gro_name;
    $gro_name{$gro_no}{"gro_e_name"}	= $gro_e_name;
	if( $IS_ENGLISH )  {
	  $gro_name{$gro_no}{"gro_name"}	= $gro_e_name;
	}
  }
  
  open(GRO_DEPT, $gro_dept_file);				###  @gro_dept
  @lines = <GRO_DEPT>;
  $temp = 0;
  foreach $line (@lines) {
    $line =~ s/\n//;
    ($gro_no, $dept) = split(/\s+/, $line);
    $gro_dept[$temp]{"gro_no"}	= $gro_no;
    $gro_dept[$temp]{"dept"}	= $dept;
    $temp++;
  }

  open(GRO_COUR, $gro_cour_file);				###  @gro_cour
  @lines = <GRO_COUR>;
  $temp = 0;
  foreach $line (@lines) {
    $line =~ s/\n//;
    ($gro_no, $cour_cd) = split(/\s+/, $line);
    $gro_cour[$temp]{"gro_no"}	= $gro_no;
    $gro_cour[$temp]{"cour_cd"}	= $cour_cd;
    $temp++;
  }

  close(GRO_NAME);
  close(GRO_DEPT);
  close(GRO_COUR);
}

#############################################################################################
#####  判斷開課時是否需要填寫「教師專長與授課科目是否符合 s_match 欄位」
#####  傳入：開課系所
#####  傳回：[0, 1] = [不必要，要]
#####  Updates: 
#####    2010/04/08 在開課、更改開課、列印等數支程式做判斷  Nidalap :D~
#####    2010/05/25 判斷條件變多了，全部拉到這裡來！ Nidalap :D~
sub Need_s_match  
{
  my($dept) = @_;
  
  return(0)  if( $dept eq $DEPT_PHY );          ###  體育，不必
  return(0)  if( $dept eq $DEPT_MIL );          ###  軍訓，不必
  return(0)  if( $SUB_SYSTEM == 2 );            ###  一般生暑修，不必  Added 20100525
  return(0)  if( $SUB_SYSTEM == 4 );            ###  專班暑修，不必  Added 20100525

  return(1);                                    ###  其餘皆要
} 

#############################################################################################
#####  判斷該系的「學系服務學習課程」代碼
#####  傳入：系所代碼
#####  傳回：科目代碼
#####  Updates:
#####    2011/04/20 Created by Nidalap :D~
sub Get_Dept_Serv_Course_ID
{
  my($dept) = @_;
  my($file, @line, $temp_dept, $temp_cour);
  
  my $file = $REFERENCE_PATH . "dept_serv_course_id.txt";
  open(SERV_CCD, $file) or die("內部錯誤：無法開啟學系服務學習科目對照檔！");
  my @line = <SERV_CCD>;
  close(SERV_CCD);
  
  foreach $line (@line) {
    ($temp_dept, $temp_cour) =  split(/\s+/, $line);
#    print("$temp_dept <-> $dept<BR>");
    return $temp_cour if($temp_dept eq $dept);		### 傳回該系的科目代碼
  }
  return "";						### 比對全部不成功
}

#############################################################################################
#####  以通識向度抓取科目清單
#####  傳入：[$category, $subcategory] = [向度代碼, 次向度代碼]
#####  傳回：科目清單 array(含 cid, group)
#####  若沒有傳入向度/次向度代碼，則傳回所有通識科目代碼清單（含向度等欄位）
#####  注意：1. perl 版本不從資料庫抓，而是抓資料檔案
#####        2. 此函式傳回「所有符合條件的歷年科目清單」，若要抓取當學期或特定學期資料，請用 Find_All_Course_by_CGE_Category
#####  Updates：
#####    2013/12/11 Created by Nidalap :D~
sub Find_All_History_Course_by_CGE_Category
{
  my ($cate_in, $subcate_in) = @_;
  my $cate, $subcate, $cid, %temp_cour, @course_list;
  
  ###  (主)向度資料表
  my $CGE_category_cour_map_file = $REFERENCE_PATH . "cge_category_cour_map.txt";
  open(CATE, $CGE_category_cour_map_file) or die("內部錯誤：無法開啟通識向度資料檔！");
  my @lines = <CATE>;
  foreach $line (@lines) {
	$line =~ s/\n//;
    ($cid, $cate, $subcate) = split(/\t/, $line);
	
	if( ($cate_in ne "") and ($subcate_in ne "") ) {			###  抓取特定向度：直接回傳科目清單(Hash，值一律為1)
	  #print("-> $cate, $subcate, $cid, $cate_in, $subcate_in<BR>\n");  
	  if( ($cate_in == $cate) and ($subcate_in == $subcate) ) {
		
		#push(@course_list, $cid);
		$course_list{$cid} = 1;
	  }
	}else{														###  抓取全部向度：回傳二維陣列(Hash of Hashes)科目清單
	  #print "all ";
	  #$temp_cour{'id'}			= $cid;
	  #$temp_cour{'category'}	= $cate;
	  #$temp_cour{'subcategory'}	= $subcate;
	  #push(@course_list, %temp_cour);
	  $course_list{$cid}{'category'}	= $cate;
	  $course_list{$cid}{'subcategory'}	= $subcate;
	}
  }
  close(CATE);
  
  return(%course_list);
}
#############################################################################################
#####  以通識向度抓取「當學期開課」或「特定學期開課」科目清單
#####  傳入：[$category, $subcategory] = [向度代碼, 次向度代碼]
#####  傳回：科目清單 array(含 cid, group，資料型別同 Find_All_Course() )
#####  若沒有傳入向度/次向度代碼，則傳回所有通識科目代碼清單
#####  Updates：
#####    2013/12/12 Created by Nidalap :D~
sub Find_All_Course_by_CGE_Category
{
  my ($cate_in, $subcate_in, $year, $term) = @_;
  my $cate, $subcate, $cid, %CGE_course_list, @temp, @course_list;    
  
#  print("[$cate_in, $subcate_in, $year, $term]<BR>\n");
  
  return ()  if( ($cate_in eq "") or ($subcate_in eq "") );
  %CGE_course_list = Find_All_History_Course_by_CGE_Category($cate_in, $subcate_in);
  @temp = Find_All_Course($DEPT_CGE, "", $year, $term);
  
  #print "cge course list = ";
  #Print_Hash(%CGE_course_list);
  
  #use Data::Dumper;
  
  #print "<P>cge list = ";
  #print Dumper(\%CGE_course_list);
  
  #print "<P>temp = ";
  #print Dumper(\@temp);
  
  
#  @print @temp;
#  foreach $t (@temp) {
#    print $t['id'] . $t['grp'] . "<BR>\n";
#  }
  
  
  foreach $temp (@temp) {
    #print "checking " . $$temp{'id'} . "<BR>\n";
    if( exists($CGE_course_list{$$temp{'id'}}) ) {
	  #print "<FONT color=RED>!!!" . $$temp{'id'} . "exists in CGE course list!</FONT>";
	  push(@course_list, $temp);
	}
  }
  #use Data::Dumper;
  #print Dumper(\@course_list);
  
  
  return @course_list;
}
#############################################################################################
#####  抓取通識向度/次向度
#####  傳入：(無)
#####  傳回：向度/次向度二維陣列
#####  注意：perl 版本不從資料庫抓，而是抓資料檔案
#####  使用方法：
#####		($cate_ref, $subcate_ref) = Get_CGE_Categories();
#####		%category = %{$cate_ref};
#####		%subcategory = %{$subcate_ref};
sub Get_CGE_Categories
{
  my $category, $subcategory, $cate, $subcate, $cname, $ename;
  
  ###  (主)向度資料表
  my $CGE_category_file = $REFERENCE_PATH . "cge_category.txt";
  open(CATE, $CGE_category_file) or die("內部錯誤：無法開啟通識向度資料檔！");
  my @lines = <CATE>;
  foreach $line (@lines) {
	$line =~ s/\n//;
    ($cate, $cname, $ename) = split(/\t/, $line);
    $category{$cate}{'cname'}= $cname;
	$category{$cate}{'ename'}= $ename;
  }
  
  ###  次向度資料表
  my $CGE_subcategory_file = $REFERENCE_PATH . "cge_subcategory.txt";
  open(CATE, $CGE_subcategory_file);
  my @lines = <CATE>;
  foreach $line (@lines) {
	$line =~ s/\n//;
    ($cate, $subcate, $cname, $ename) = split(/\t/, $line);
    $subcategory{$cate}{$subcate}{'cname'}= $cname;
	$subcategory{$cate}{$subcate}{'ename'}= $ename;
	#print "$cate : $subcate : $cname<BR>\n";
  }
  close(CATE);
  
  return(\%category, \%subcategory);
  #return(\%category);
}


