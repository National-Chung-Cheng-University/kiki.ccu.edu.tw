1;

###################################################################################################################
#####   Student_Course.pm
#####   處理學生選課的資料
#####   Coding: hanchu   Date: 1999/3/14
#####  Updates:
#####   2009/12/31 將原先讀取舊學期資料所傳入的 $yearterm 改為 $year 和 $term, 以避免民國百年 bug.  Nidalap :D~
#####   2011/07/29 加入 Stu_Can_Apply_Concent() 以判斷學生是否可加簽某科目  Nidalap :D~
#####   2014/09/04 因應先搶先贏期間退選餘額延後釋出功能，新增 student_file 的 delayed_del_time 欄位，修改若干函式  Nidalap :D~
#####   2016/03/01 修正 Course_of_Student() 避免因 Check_Course.pl 多補科目上去導致判斷延遲退選錯誤 Nidalap :D~
###################################################################################################################

###########################################################################
####    Course_of_Student
####        輸入：$id,$year,$term,$include_delayed_del
####              若沒有傳入 $year $term，回傳目前學生選課資料
####              若 $year == "last"，回傳上次篩選後學生選課資料
####			  $include_delayed_del 若為 1，則傳回即將退選的課(在先搶先贏退選餘額延遲篩選機制下)
####        輸出：@Course_of_the_Student（型態為 List of Hash (Loh)）
####                 {id,dept,group,credit,property,delayed_del_time}
###########################################################################
sub Course_of_Student
{
    my($id, $year, $term, $include_delayed_del)=@_;
    
    my($FILENAME)=$id;
    my(@Course_of_the_Student, $student_path);
    my($i);
	
	my $debug = 0;
    if( ($year eq "") and ($term eq "") ) {				###  如果沒有傳入 $year, $term
      print("1") if($debug);
      $student_path = $STUDENT_PATH;				###  或是不是本學年學期
    }elsif( ($year eq $YEAR) and ($term eq $TERM) ) {		###    那就讀取本學年學期資料
      print("2") if($debug);
      $student_path = $STUDENT_PATH;				###  else讀取歷史資料
    }elsif( $year eq "last" ) {
	  $student_path = $DATA_PATH . "Student_last/"; ###  else讀取上次篩選後資料
	  print("last") if($debug);
    }else{
      print("3") if($debug);
      $student_path = $HISTORY_PATH . "Student/" . $year . "_" . $term;		###  else 特定學年學期
    }

    #print("Trying to access $student_path/$FILENAME<BR>\n") if($debug);
    if(-e "$student_path/$FILENAME"){
        open(FILE,"<$student_path/$FILENAME") or die("Cannot open file $FILENAME!\n");
    }else{
        umask(000);
        open(FILE,">$student_path/$FILENAME");
        close(FILE);
        open(FILE,"<$student_path/$FILENAME");
    }
	flock(FILE, 1);
    my @lines=<FILE>;
    my($index)=0;
	my @temp_fields;
	
	#print "count lines = " . @lines . "<BR>\n"  if($debug);
	
	my %to_del, $id_grp;
	
    foreach $line(@lines){
        $line =~ s/\n//;
		@temp_fields = split(/\s+/, $line);
		
		#####  $include_delayed_del 若不為 1，則不傳回即將退選的課
#		next if( ($include_delayed_del!=1) and ($temp_fields[5] ne "") );	

		#####  以下這一段用來取代上面這一行，為了避開 Check_Course.pl 可能將即將退選的課多補上一筆的 BUG。
		#####  此處將註記即將退選的課記下來，如果再次發現，則是同即將退選（不再檢查註記）。  2016/03/01 Nidalap :D~
		if( $include_delayed_del!=1) {
		  $id_grp = $temp_fields[0] . $temp_fields[2];
		  if($temp_fields[5] ne "") {
		    $to_del{$id_grp} = 1;
		    next;
		  }else{
		    if( $to_del{$id_grp} == 1 ) {
			  next;
			}
		  }
		}
		
		( $Course_of_the_Student[$index]{id},
		  $Course_of_the_Student[$index]{dept},
		  $Course_of_the_Student[$index]{group},
		  $Course_of_the_Student[$index]{credit},
		  $Course_of_the_Student[$index]{property},
		  $Course_of_the_Student[$index]{delayed_del_time}
		) = @temp_fields;

        $index++;
    }
    close(FILE);
    return(@Course_of_the_Student);
}

############################################################################
####    Student_in_Course                                               ####
####        輸入：($course{dept}, $course{id}, $course{group}, $last_flag) #
####        輸出：@Students_of_the_course                               ####
####        說明：就原來的需求規劃中，需要輸入科目的系所，主要是因為    ####
####              各科目的學生名單將依系所存入，但目前我並未將這些學    ####
####              生名單依系所存入，而是放在同一目錄下，故系所代碼實    ####
####              際並未用到。                                          ####
####        2002/02/19 (Nidalap :D~)
####          $last_flag用於讀取上次篩選後的名單, 名單內容放在
####          $DATA_PATH . "Student_of_course_last" 中, 格式同一般.
####        2002/12/24 (Nidalap :D~)
####          加入 $last_flag == "last_semester" 判斷, 讀取上學期選課資料
####          用在 '同班學生批次加選' 功能
####                                   
####        Coder:hanchu      Date: 1999/3/14                           ####
############################################################################
sub Student_in_Course
{
    my($dept,$id,$group,$year,$term)=@_;
    my(@Students_of_the_course);
    my($STUDENT_OF_COURSE_PATH);    ###  =$DATA_PATH . "Student_of_course";
    my($FILENAME)=$id."_".$group;
    
    if( ($year eq "") and ($term eq "") ) {
      $year = $YEAR; $term = $TERM;
    }
    if( $year eq "last")  {                                     ### 要讀上次篩選後資料
      $STUDENT_OF_COURSE_PATH = $DATA_PATH . "Student_of_course_last/";
    }elsif( $year eq "last_semester")  {                        ### 要讀上學期選課資料
      $STUDENT_OF_COURSE_PATH = $DATA_PATH . "Student_of_course_last_semester/";
    }elsif( not( ($year==$YEAR)and($term==$TERM) ) ) {                                ### 要讀以前某學期資料
#      print("[$year <-> $YEAR; $term <-> $TERM] 讀舊學期資料... <BR>\n");
      $STUDENT_OF_COURSE_PATH = $HISTORY_PATH . "Student_of_course/" . $year . "_" . $term . "/";
    }else{                                                           ###  要讀目前選課名單
      $STUDENT_OF_COURSE_PATH = $DATA_PATH . "Student_of_course/";
    }
#    print("[year, term]=[$year, $term], <BR>Locating $STUDENT_OF_COURSE_PATH / $FILENAME ......<BR>\n");
    if(-e "$STUDENT_OF_COURSE_PATH/$FILENAME"){
        open(ALLSTUDENTS,"<$STUDENT_OF_COURSE_PATH/$FILENAME") or
               die("Cannot open file $FILENAME!!\n");
    }else{
        umask(000);
        open(ALLSTUDENTS,">$STUDENT_OF_COURSE_PATH/$FILENAME");
        close(ALLSTUDENTS);
        open(ALLSTUDENTS,"<$STUDENT_OF_COURSE_PATH/$FILENAME");
    }
	flock(ALLSTUDENTS, 1);
    @Students_of_the_course=<ALLSTUDENTS>;
    close(ALLSTUDENTS);

    foreach $Student(@Students_of_the_course){
        $Student =~ s/\n//;
    }

    return(@Students_of_the_course);
}

############################################################################
####    Student_of_Course_Number                                        ####
####        輸入：($course{dept}, $course{id}, $course{group})          ####
####        輸出：$number                                               ####
####        說明：同上一個 sub function (Student_in_Course)             ####
############################################################################
sub Student_of_Course_Number
{
    my($dept,$id,$group)=@_;
    my(@Students_of_the_course);
    my($STUDENT_OF_COURSE_PATH)=$DATA_PATH . "Student_of_course";

    my($FILENAME)=$id."_".$group;

    if( not -e $STUDENT_OF_COURSE_PATH/$FILENAME ) {
      return(0);
    }else{
      open(ALLSTUDENTS,"<$STUDENT_OF_COURSE_PATH/$FILENAME") or
 		die("Cannot open file $FILENAME!!\n");
      @Students_of_the_course=<ALLSTUDENTS>;
      close(ALLSTUDENTS);
      $number=@Students_of_the_course;
      return($number);
    }
}

#############################################################################
####    Add_Student_Course                                               ####
####        輸入：$student_id   學生學號   輸出：無                      ####
####              $course_dept  科目系所                                 ####
####              $course_id    科目代碼                                 ####
####              $course_group 科目班別                                 ####
####              $property     選課屬性                                 ####
####        Date : 1999/3/17                                             ####
####        說明：學生選課用，將學生所選的科目寫入相對的檔案。           ####
#############################################################################
sub Add_Student_Course
{
    my($student_id,$course_dept,$course_id,$course_group,$property)=@_;
    my($Course_File)=$course_id."_".$course_group;

#    print("Going to Add: $student_id, $course_id, $course_group, $property<BR>\n");

    ####   開啟並讀取該課的課程屬性   ####
    require $LIBRARY_PATH."Course.pm";
    require $LIBRARY_PATH."Error_Message.pm";
    my(%Course)=Read_Course($course_dept,$course_id,$course_group,"","",$student_id);
    $course_credit=$Course{credit};

    umask(000);
    ####   確定沒有重複選課   ####
    @MyCourses=Course_of_Student($student_id);
    $MyCount=@MyCourses;

    my($HAVE_SELECTED)=0;
    for($i=0; $i < $MyCount; $i++){
        if($MyCourses[$i]{id} eq $course_id){
            if($MyCourses[$i]{group} eq $course_group){
                $HAVE_SELECTED=1;
                break;
            }
        }
    }

    ####  $HAVE_SELECTED == 0         ####
    ####  表示該學生尚未選過該門科目  ####
    ####  故應正常加選                ####
    if($HAVE_SELECTED eq 0){
        ####      由於寫入 Student_of_course_file 疑似有一定小機率會出錯並中斷，
        ####      導致選課資料不一致，且該筆紀錄不會紀錄到 Student_Log，所以將寫入三個檔的順序更改為：
        ####      Student_Log ->  Student_of_course_file -> Student_file    [2010/01/18 Nidalap :D~]

        ####    紀錄該門課有哪些學生修    ####
        my($Student_of_course_file)=$Course_File;
        open(FILE,">>$STUDENT_OF_COURSE_PATH/$Student_of_course_file");
        print FILE $student_id."\n";
        close(FILE);
                        
        ####   記錄學生的選課資料檔    ####
        open(FILE,">>$STUDENT_PATH/$student_id");
        print FILE $course_id."\t";
        print FILE $course_dept."\t";
        print FILE $course_group."\t";
        print FILE $course_credit."\t";
        print FILE $property."\n";
        close(FILE);

        ####    記錄選課動作到LOG檔
        Student_Log("Add   ",$student_id, $course_id, $course_group, $property);

#        print("Added : $student_id, $course_id, $course_group, $property<BR>\n");

        return(1);
    }else{
        return(0);
    }

}

#############################################################################
####    Delete_Student_Course                                            ####
####        輸入：$student_id    學生學號     輸出：個別學生選課檔       ####
####              $course_dept   科目系所           課程記錄選課學生檔   ####
####              $course_id     科目代碼                                ####
####              $course_group  科目班別                                ####
####        Updates:
####          1999/3/19  Created
####          2009/10/22 加入 $by_who 輸入欄位，作為紀錄檔查詢用
#############################################################################
sub Delete_Student_Course
{
    my($student_id,$course_dept,$course_id,$course_group,$by_whom)=@_;
    my($Course_File)=$course_id."_".$course_group;
    my($i);

    ####    刪除該科目的學生記錄檔     ####
    my(@Update_Students);
    my($Num)=0;

    my(@All_Students)=Student_in_Course($course_dept,$course_id,$course_group);

    foreach $item(@All_Students){
        if($item ne $student_id){
            $Update_Students[$Num]=$item;
            $Num++;
        }
    }

    ####    刪除該科目在學生資料檔的紀錄    ####
    my(@Course)=Course_of_Student($student_id, "", "", 1);
    
    my($num);
    $num=@Course;
    my(@Update_Course);
    my($count)=0;
    my($index);
    for($index=0; $index < $num; $index++){
        if(($Course[$index]{id} ne $course_id) or
           ($Course[$index]{group} ne $course_group)){
            $Update_Course[$count]{id}=$Course[$index]{id};
            $Update_Course[$count]{dept}=$Course[$index]{dept};
            $Update_Course[$count]{group}=$Course[$index]{group};
            $Update_Course[$count]{credit}=$Course[$index]{credit};
            $Update_Course[$count]{property}=$Course[$index]{property};
			$Update_Course[$count]{delayed_del_time}=$Course[$index]{delayed_del_time};
            $count++;
        }
    }

    ####    寫回記錄檔    ####
    #open(FILE,">$STUDENT_OF_COURSE_PATH/$Course_File") or die("Cannot open file $Course_File!!\n");
	open(FILE, "+< $STUDENT_OF_COURSE_PATH/$Course_File") or die("Cannot open file $Course_File!!\n");
	flock(FILE, 2);
	seek(FILE, 0, 0); truncate(FILE, 0);
	
    foreach $item(@Update_Students){
        print FILE $item."\n";
    }
    close(FILE);

    open(FILE,">$STUDENT_PATH/$student_id");
    for($index=0; $index < $count; $index++){
        print FILE $Update_Course[$index]{id}."\t";
        print FILE $Update_Course[$index]{dept}."\t";
        print FILE $Update_Course[$index]{group}."\t";
        print FILE $Update_Course[$index]{credit}."\t";
        print FILE $Update_Course[$index]{property}."\t";
		print FILE $Update_Course[$index]{delayed_del_time}."\n";
    }
    close(FILE);

    #####  檢查該學生是否有額滿權限, 若有則另外要取消紀錄
    Upper_Limit_Immune_Delete($course_id, $course_group, $student_id);
    
    #####  寫入LOG檔
    $by_whom = "UNDETERMINED"  if( !defined($by_whom) );
    Student_Log("Delete",$student_id, $course_id, $course_group, " ", $by_whom);
}
############################################################################
#####  Delayed_Delete_Student_Course 
#####  先搶先贏期間，退選餘額延後釋出用。此函式在 $delayed_del_dir 建立檔案，紀錄此退選紀錄將於何時被執行。
#####  待 crontab 排程於該時間實際執行之。
#####  輸入：$student_id,$course_dept,$course_id,$course_group,$by_whom
#####  輸出：(無)
#####  Updates:
#####    2014/09/02 Created by Nidalap :D~
#####    2015/10/06 先檢查此科目是否已經在等待延後釋出中。若是，則什麼都不做，直接離開 by Nidalap :D~
############################################################################
sub Delayed_Delete_Student_Course 
{
  my($student_id,$course_dept,$course_id,$course_group,$by_whom)=@_;
  my $delayed_del_dir = $DATA_PATH . "Del_Courses/";
  
  #####  先檢查此科目是否已經在等待延後釋出中。若是，則什麼都不做，直接離開
  my(@Course)=Course_of_Student($student_id, "", "", 1);  
  $count = @Course;
  for($i=0; $i<$count; $i++){
    if( ($Course[$i]{id}==$course_id) and ($Course[$i]{group}==$course_group) ) {
	  return if( $Course[$i]{delayed_del_time} != "" );
	}
  }
    
  my $min = 5*60;			### 批次退選開始時間(預設五分鐘)
  my $max = 10*60;			### 批次退選截止時間(預設十分鐘)
  
  $do_del_time = time() + int(rand($max-$min)) + $min;
   
  ##########  寫入(append)到 delayed_del_dir 的延遲退選檔案
  #$do_del_time = '1409627316';
  my $delayed_del_file = $delayed_del_dir . $do_del_time;
#  print("[min, max, now, do_del_time] = $min, $max, " . time() . ", $do_del_time<BR>\n")
  umask(000);
  if( !(-e $delayed_del_dir) ) {
    mkdir($delayed_del_dir);
  }
  open(FILE, ">>$delayed_del_file");
  print FILE ("$student_id\t$course_dept\t$course_id\t$course_group\n");
#  print("file = $delayed_del_file<BR>\n");
  my $course_file = $course_id."_".$course_group;  
  close(FILE);
  
  ##########  修改 Student/ 下該學生的選課檔
  open(FILE,">$STUDENT_PATH/$student_id");
  for($i=0; $i<$count; $i++){
    if( ($Course[$i]{id}==$course_id) and ($Course[$i]{group}==$course_group) ) {
	  $Course[$i]{delayed_del_time} = $do_del_time;
	}
    print FILE $Course[$i]{id}."\t";
    print FILE $Course[$i]{dept}."\t";
    print FILE $Course[$i]{group}."\t";
    print FILE $Course[$i]{credit}."\t";
    print FILE $Course[$i]{property}."\t";
	print FILE $Course[$i]{delayed_del_time}."\n";
  }
  close(FILE);
  
  #####  寫入LOG檔
  $by_whom = "UNDETERMINED"  if( !defined($by_whom) );
  Student_Log("DelWait",$student_id, $course_id, $course_group, " ", $by_whom);
  
}

############################################################################
#####  Upper_Limit_Immune_Delete()
#####  有額滿權限的學生退選
#####  若是學生有額滿加簽權限, 他退選時也要取消特別紀錄,
#####  作為其他學生選課時的人數計算參考(限修人數 + 此名單人數)
#####  若退選學生不做這個動作, 有可能造成可加選名額計算錯誤.
#####  傳回值: (null)
#####  Date : 2007/03/08
#####  Coder: Nidalap :D~
############################################################################
sub Upper_Limit_Immune_Delete
{
  my($course_id, $course_group, $stu_id) = @_;
  my($immune_file, @line, @line2, $found);

  $found = 0;
  $immune_file = $DATA_PATH . "Course_Upper_Limit_Immune/" . $YEAR . "_" . $TERM . "/" .
                 $course_id . "_" .  $course_group . "_add";

  if( -e $immune_file ) {
    open(IMMUNE, $immune_file);
    @line = <IMMUNE>;
    close(IMMUNE);
    foreach $line (@line) {
      $line =~ s/\n//;
      if($stu_id eq $line) {
        $found = 1;				### 把此人揪出來
      }else{
        push(@line2, $line);			### 把其他人丟進 @line2, 等一下寫回檔案
      }
    }
    if( $found == 1 ) {				### 如果此人的確曾以特殊權限加選
      open(IMMUNE, ">$immune_file");		### 寫回 _add 檔案
      foreach $line (@line2) {
        print IMMUNE ("$line\n");
      }
      close(IMMUNE);
    }
  }
}

############################################################################
#####  讀取某學生目前選修科目的節次
#####  Updates:
#####    2004/03/04 撰寫(Nidalap :D~)
#####    2008/06/03 debug  Nidalap :D~
sub Get_My_Table
{
  my($id, $free_flag) = @_;
  my(@course, %course, @my_time, $i, @alltime, %my_time_temp, $temp, @alltime);

  @course = Course_of_Student($id);
  $i = 0;
  foreach $course (@course) {
    %course = Read_Course($$course{dept}, $$course{id}, $$course{group}, "", "");
    foreach $time (@{$course{time}}) {
      $my_time[$i]{week} = $$time{week};
      $my_time[$i]{time} = $$time{time};
      $temp = $$time{week} . "_" . $$time{time};
      $my_time_temp{$temp} = 1;
      $i++;
      
#      print("I am occupied at $temp<BR>\n");
    }
#    print("$course{id}_$course{group}  $course{cname}<BR>\n");
  }
  #####  針對 @my_time, 找出 50/75 分鐘衝堂的節次, 再次更改 @my_time_temp 課程佔用時間陣列
  #####  added 20080917  Nidalap :D~
  foreach $my_time (@my_time) {
#    print("occupied at $$my_time{week} _ $$my_time{time}<BR>\n");
    @alltime = (@TIMEMAP50, @TIMEMAP75);
    foreach $alltime (@alltime) {
      if( ($alltime ne $$my_time{time}) and (is_Time_Collision(1,$alltime,1,$$my_time{time})) ) {
#        print("collides: $alltime vs $$my_time{time}...<BR>\n");        
        $temp = $$my_time{week} . "_" . $alltime;
        $my_time_temp{$temp} = 1;
      } 
    }
  }
  if( $free_flag eq "free" ) {                       ### 如果要傳回空堂時間
    my(@my_time2, $j);
    $j = 0;
    @alltime = (@TIMEMAP50, @TIMEMAP75);
    for($day=1; $day<=7; $day++) {
      foreach $time (@alltime) {                     ###  每個可能的時間
        $temp = $day . "_" . $time;
        if($my_time_temp{$temp} != 1) {
          $my_time2[$j]{week} = $day;
          $my_time2[$j]{time} = $time;
          $j++;
        }
      }
    }
                              
    @my_time = @my_time2;
  }
  return(@my_time); 
}

############################################################################
#####  Check_Multiple_Course_Collisions
#####  檢查學生所選的科目中有哪些衝堂情形
#####  Updates:
#####    2002/05/07
############################################################################
#sub Check_Multiple_Course_Collisions
#{
#  my(@selected_time) = @_;
#  foreach $time (@selected_time) {
#    print("$$time{week}_$$time{time}<BR>\n");
#  }
#
#}
############################################################################
#####  Check_course_number()
#####  確認選課學生的人數(防止0-byte bug)
#####  Coder: Nidalap
#####  Date : Jun 08/2000
#####  尚未啟用
############################################################################
sub Check_course_number
{
  my($course_id, $group, $actual_number) = @_;
  my $NUMBER_CHECK_FILE = $DATA_PATH . "Course_Number_Check/";
  my($number);
  
  $NUMBER_CHECK_FILE = $NUMBER_CHECK_FILE . $course_id . "_" . $group;
  if( not -e $NUMBER_CHECK_FILE ) {
    return();
  }else{
    open(CHECK_FILE, $NUMBER_CHECK_FILE);
    $number = <CHECK_FILE>;
    close(CHECK_FILE);
    $number =~ s/\n//;
  }
  if( abs($actual_number - $number) > 5 ) {
    #Do something!!!!!!!!
  }
}
############################################################################
#####  Update_course_number()
#####  更新選課學生的人數(防止0-byte bug)
#####  Coder: Nidalap
#####  Date : Jun 08/2000  <-- 未完成(suspended)
############################################################################
sub Update_course_number
{
  my($course_id, $group, $actual_number) = @_;
  my $NUMBER_CHECK_FILE = $DATA_PATH . "Course_Number_Check/";
  my($number);
  
  $NUMBER_CHECK_FILE = $NUMBER_CHECK_FILE . $course_id . "_" . $group;
  if( not -e $NUMBER_CHECK_FILE ) {
    umask(000);
    open(CHECK_FILE, ">$NUMBER_CHECK_FILE");
    print CHECK_FILE $actual_number;
    close(CHECK_FILE);
  }else{
    open(CHECK_FILE, $NUMBER_CHECK_FILE);
    $number = <CHECK_FILE>;
    
    $number =~ s/\n//;
  }
  if( abs($actual_number - $number) > 5 ) {
    #Do something!!!!!!!!
  }
      

}
############################################################################
#####  Lower_Credit_Limit()
#####  該學生當學期總學分數學分下限
#####  Coder: Nidalap :D~
#####  Date: 2008/11/14
############################################################################
sub Lower_Credit_Limit
{
  my(%student) = @_;
  my $limit = 0;			###  學分上限, 預設 0 (沒有限制)
  
  if( is_GRA() ) {				###  專班生
    $limit = 3  if( $student{grade} == 1 );		#  一年級
    $limit = 2  if( $student{grade} == 2 );		#  二年級
  }else{					###  一般生
    if( $student{id} =~ /^8/ ) {
                                                        #  博二以上不限
      $limit = 3  if( $student{grade} == 2 );		#  博二
      $limit = 6  if( $student{grade} == 1 );		#  博一
    }elsif( $student{id} =~ /^6/ ) {
      $limit = 6  if( $student{grade} == 1 );   	#  碩一
      #$limit = 2  if( ($student{grade} == 2)and($TERM==1) );  #  碩二上
	  $limit = 2  if( $student{enrollnum} == 3 );   	#  碩二上
    }else{
      $limit = 16;					#  大一到大三
      $limit = 8  if( $student{grade} == 4 );		#  大四
    }
  }
  
  return($limit);
}
############################################################################################
#####  Check_Ban_Limit
#####  檢查擋修系所年級班別
#####  檢查學生選修的科目, 是否有限定擋修系所年級班別. 如果有, 判斷該生身份,
#####  判斷是否可選修. (管理者不在此限)
#####  只要系所年級班別任一項有擋, 其他沒選的視同全部選. 三者以AND連結
#####  輸入      : %The_Course
#####  輸出      : $ban_flag                       $ban_flag:(0,1) = (不擋, 擋修)
#####  用到global: %Student
#####  Updates: 
#####    2011/07/30 從 Add_Course01.cgi 搬過來，「科目是否需要加簽」檢核也會用到 Nidalap :D~
#####    2016/12/20 改為透過 is_Same_Dept() 判斷相同系所 by Nidalap :D~
############################################################################################
sub Check_Ban_Limit
{
  my($Ban_Dept_Num, $Ban_Grade_Num, $Ban_Class_Num);
  my($L1, $L2, $L3);
  my(%The_Course) = @_;

  $Ban_Dept_Num = @{$The_Course{ban_dept}};
  $Ban_Grade_Num = @{$The_Course{ban_grade}};
  $Ban_Class_Num = @{$The_Course{ban_class}};

  if( ($Ban_Dept_Num==0) and ($Ban_Grade_Num==0) and ($Ban_Class_Num==0) ) {
    return(0);                       ##  不擋修, return
  }else{                             ##  擋修, 繼續檢查
    if($Ban_Dept_Num == 0){             ##  如果沒有擋系所，則預設為所有系所
      @Ban_Dept=Find_All_Dept();
    }else{
      @Ban_Dept=@{$The_Course{ban_dept}};
    }

    if($Ban_Grade_Num == 0){            ##  如果沒有擋年級，則預設為所有年級
      @Ban_Grade=(1,2,3,4,5,6,7,8,9,10);
    }else{
      @Ban_Grade=@{$The_Course{ban_grade}};
    }

    if($Ban_Class_Num == 0){            ##  如果沒有擋班級，則預設為所有班級
      @Ban_Class=(A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z);
    }else{
      @Ban_Class=@{$The_Course{ban_class}};
    }
    $L1=$L2=$L3=0;

    foreach $dept (@Ban_Dept){
      #if($dept eq $Student{dept}){
      if( is_Same_Dept($dept, $Student{dept}) ) {       ###  改為依 is_Same_Dept() 判斷相同系所 20161220
        $L1 = 1;
      }
    }
    
    
#    print("fu : $FU{$Student{id}}<BR>");
#    print("double : $DOUBLE{$Student{id}}<BR>");
#    print("this : $The_Course{dept}<BR>");
    if( ($The_Course{dept} eq "6104") or ($The_Course{dept} eq "6154") or
        ($The_Course{dept} eq "6204") ) {       ### 如果開課系所是法律系任一組
       if( $FU{$Student{id}} eq "6054" ) {      ### 且學生是法律系輔系生
         $FU{$Student{id}} = $The_Course{dept}; ### 則視同是該組的輔系生
       }
    }
    #if( $FU{$Student{id}} eq $The_Course{dept}) {
    if( is_Same_Dept($FU{$Student{id}}, $The_Course{dept}) ) {       ###  改為依 is_Same_Dept() 判斷相同系所 20161220
      $L1 = 0;                            ##  輔系不受擋修系所限制2002/02/26
    }
    #if( $DOUBLE{$Student{id}} eq $The_Course{dept}) {
    if( is_Same_Dept($DOUBLE{$Student{id}}, $The_Course{dept}) ) {   ###  改為依 is_Same_Dept() 判斷相同系所 20161220
      $L1 = 0;                            ##  雙主修不受擋修系所限制2002/02/26
    }

    foreach $item(@Ban_Grade){            ##  要在意，升級後與升級前不同...
      if($item eq $Student{grade} ){      ##  小心，不在意會發生重大危機...
        $L2 = 1;
      }
    }
    foreach $item(@Ban_Class){
      if($item eq $Student{class}){
        $L3 = 1;
      }
    }

    if(($L1 == 1) && ($L2 == 1) && ($L3 == 1)){   ###  學生符合擋修系所年級班級
      if( $SUPERUSER == 1 ) {                ##  管理者不擋修
        return(0);
      }elsif($system_flags{no_ban} == 1) {   ##  若設定第二階段設定擋修無效:
        if( $Ban_Dept_Num < 10 ) {           ##    -> 擋修系所少於 10 個(視同於限本系), 要檔修
          return(1);
        }elsif( ($The_Course{dept} eq $DEPT_MIL) or ($The_Course{dept} eq $DEPT_CGE ) ) {
          return(1);                         ##    -> 軍訓與通識仍要擋修
        }else{
          return(0);                         ##    -> 其他課程依設定不擋修
        }
      }else{
        return(1);                           ##  符合限制, 要擋修
      }
    }
  }
}


############################################################################
#####  Stu_Can_Apply_Concent_Form
#####  判斷學生是否可加簽某科目
#####  此處先做粗略檢查，PHP 版本會進一步檢查學生成績，以判斷先修條件是否符合。
#####  符合以下條件任一，即可加簽：
#####    1. 科目目前選修人數 >= 限修人數
#####    2. 科目要求先修科目
#####    3. 科目擋修學生所屬系所年級班級
#####    4. 科目為軍訓，且學生當學期已選修其他軍訓
#####    5. 科目為語言中心課程(190開頭)
#####    6. 科目為學系服務學習課程
#####  輸入：(\%Student, \%the_Course, \@Course_of_Student, $student_count)
#####  Updates:
#####    2011/07/30 Coded by Nidalap :D~
#####    2016/12/20 改為透過 is_Same_Dept() 判斷相同系所 by Nidalap :D~
sub Stu_Can_Apply_Concent_Form
{
  my(%Student)		 = %{$_[0]};
  my(%the_Course)	 = %{$_[1]};
  my(@Course_of_Student) = @{$_[2]};
  my $student_count = $_[3];

  my $can_apply = 0;
  
#  Print_Hash(%Student);
#  Print_Hash(%the_Course);
#  print"<HR>";
#  print $student_count . "<BR>";
#  print @Course_of_Student;

  if( ($the_Course{number_limit} > 0) and ($student_count >= $the_Course{number_limit}) ) {
    $can_apply = 1;				###  1. 科目目前選修人數 >= 限修人數
  } 
  if( @{$the_Course{prerequisite_course}} > 0 ) {
    foreach $pre_cou (@{$the_Course{prerequisite_course}}) {
      if($$pre_cou{dept} ne "99999") {		###       先修課目所屬系所為「無」
        $can_apply = 1;				###  2. 科目要求先修科目
      }
    }
  }
  if( Check_Ban_Limit(%the_Course)==1 ) {
    $can_apply = 1;				###  3. 科目擋修學生所屬系所年級班級
  }
  if( $the_Course{id} =~ /^903/ ) {
    foreach $cou (@Course_of_Student) {
      if( $$cou{id} =~ /^903/ ) {
        $can_apply = 1;				###  4. 科目為軍訓，且學生當學期已選修其他軍訓
      }
    }
  } 
  if( $the_Course{id} =~ /^190/) {
    $can_apply = 1;				###  5. 科目為語言中心所開設
  }
#  print Get_Dept_Serv_Course_ID($the_Course{dept});
  if( $the_Course{id} eq Get_Dept_Serv_Course_ID($the_Course{dept}) ) {
    #if( $Student{dept} eq $the_Course{dept} ) {
    if( is_Same_Dept($Student{dept}, $the_Course{dept}) ) {   ###  改為依 is_Same_Dept() 判斷相同系所 20161220
      $can_apply = 1;				###  6. 科目為學系服務學習課程, 且學生為該系學生
    }
  }

  return $can_apply;
}


