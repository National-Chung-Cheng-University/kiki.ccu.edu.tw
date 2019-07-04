1;
############################################################################################
##### Dept.pm 處理系所資料
##### Program by Ionic
##### Changes:
#####   2009/06/01  因應系所合一導致的系所代碼更改，修改 Find_All_Dept 函式  Nidalap :D~
#####   2016/06/01 改為到 ccmisp06/07 的 $MAIN_HOME_PATH1/2 讀取資料檔 by Nidalap :D~
############################################################################################

############################################################################################
#####  Find_All_Dept
#####  讀取所有系所清單
#####  Changes:
#####    1999/05/27 系所資料加入學院別, 除了新增系所函式外都已修改 Nidalap
#####    2000/11/17 若系統是專班使用, 將大學部拿掉 Nidalap
#####    2009/06/01 因應系所合一導致的系所代碼更改，加入傳入參數以辨別是否不傳回系所合一的新系所 Nidalap
sub Find_All_Dept
{
  my($old_dept_only) = @_;
  $old_dept_only = ""  if( not defined($old_dept_only) );

  #my($DeptFile) = $REFERENCE_PATH . "Dept";
  my $DeptFile = ( $IS_GRA ? $MAIN_HOME_PATH2 : $MAIN_HOME_PATH1 ) . "DATA/Reference/Dept";
  
  my(@dept,$dept,@TempArray,$temp,$i);
  my($dept_com_file, @TempArray2, %dept_com, $deptcd, $com_deptcd);
  $i=0;

  open(DEPT,$DeptFile) or die("Cannot open file $DeptFile!\n");
  @TempArray = <DEPT>;
  close(DEPT);
  
  #####  如果不要系所合一的新系所，先讀取 $dept_com_file 新舊代碼對應檔
  #####  系所合一於 2009/06 左右開始，新系所代碼只用於學籍，不用於開課，故開課選擇處不提供選擇。
  if( $old_dept_only eq "NO_COM_DEPT" ) {
    $dept_com_file = $REFERENCE_PATH . "dept_com.txt";
    open(DEPT_COM, $dept_com_file) or die("Cannot open file $dept_com_file!\n");
    @TempArray2 = <DEPT_COM>;
    close(DEPT_COM);
    foreach $line (@TempArray2) {
      ($deptcd, $com_deptcd) = split(/\s+/, $line);
      $dept_com{$com_deptcd} = $deptcd;
    }
  }
  #####  準備傳回系所代碼 @dept
  foreach $dept(@TempArray)  {
    ($dept,$temp) = split(/\s+/,$dept); 
    if( $old_dept_only eq "NO_COM_DEPT" ) {
      if( $dept_com{$dept} ne "" ) {
        next;
      }
    }
    if( ($SUB_SYSTEM == 3)or($SUB_SYSTEM == 4) ) {
      next if($dept =~ /4$/);
    }
    $dept[$i++]=$dept;
  }
  return(@dept);
}
############################################################################
sub Find_Graduate_Dept    ##  Add by hanchu @ 1999/9/7
{
  #my($DeptFile) = $REFERENCE_PATH."/Dept";
  my $DeptFile = ( $IS_GRA ? $MAIN_HOME_PATH2 : $MAIN_HOME_PATH1 ) . "DATA/Reference/Dept";
  
  my(@dept,$dept,@TempArray,$temp,$i);
  $i=0;
  open(DEPT,$DeptFile) or die("Cannot open file $DeptFile!\n");
  @TempArray = <DEPT>;
  close(DEPT);
  foreach $dept(@TempArray)  {
    ($dept,$temp) = split(/\s+/,$dept);
    if($dept%10 > 4){
      $dept[$i++]=$dept;
    }
  }
  return(@dept);
}
############################################################################
sub Find_College_Dept    ##  Add by hanchu @ 1999/9/7
{
  #my($DeptFile) = $REFERENCE_PATH."/Dept";
  my $DeptFile = ( $IS_GRA ? $MAIN_HOME_PATH2 : $MAIN_HOME_PATH1 ) . "DATA/Reference/Dept";
  
  my(@dept,$dept,@TempArray,$temp,$i);
  $i=0;
  open(DEPT,$DeptFile) or die("Cannot open file $DeptFile!\n");
  @TempArray = <DEPT>;
  close(DEPT);
  foreach $dept(@TempArray)  {
    ($dept,$temp) = split(/\s+/,$dept);
    if($dept%10 == 4){
      $dept[$i++]=$dept;
    }
  }
  return(@dept);
}
############################################################################
sub Read_Dept
{
  #my($DeptFile) = $REFERENCE_PATH."/Dept";
  my $DeptFile = ( $IS_GRA ? $MAIN_HOME_PATH2 : $MAIN_HOME_PATH1 ) . "DATA/Reference/Dept";
  
  my($dept_line,%dept,$cname,$abbrev,$college, $junk,$Input_Dept);

  ($Input_Dept)=@_;

  open(DEPT,$DeptFile) or die("Cannot open file $DeptFile!\n");
   @TempArray = <DEPT>;
  close(DEPT);
  foreach $dept_line(@TempArray)  {
    ($dept_cd,$cname,$abbrev,$college,$ename) = split(/\t/,$dept_line); 
    if( $dept_cd eq $Input_Dept )  
    {
     $dept{id}=$dept_cd;
     #$dept{cname} = $IS_ENGLISH ? $ename : $cname;
	 $dept{cname} = $cname;
     $dept{cname2}=$abbrev;
     $dept{college}=$college;
	 $dept{ename}=$ename;
     $dept{password}="";
     open(PWD,$DEPT_PASSWORD_PATH."/".$dept_cd.".pwd") or goto EXIT;
      $dept{password}=<PWD>;
      $dept{password} =~ s//\n/;
     close(PWD);
     goto EXIT;
    }
  }
  EXIT:
  return(%dept);
}
############################################################################
#####  讀取學院資料
#####  要用的時候才發現沒有這個函式...
#####  2005/03/09, Nidalap :D~
############################################################################
sub Read_College
{
#  my($CollegeFile) = $REFERENCE_PATH."/college.txt";
  my $CollegeFile = ( $IS_GRA ? $MAIN_HOME_PATH2 : $MAIN_HOME_PATH1 ) . "DATA/Reference/college.txt";
  
  my(%college, @TempArray, $id, $name);
#  my($dept_cd,%dept,$temp,$temp2,$college, $junk,$Input_Dept);

  open(COLLEGE, $CollegeFile) or die("Cannot open file $CollegeFile!\n");
  @TempArray = <COLLEGE>;
  close(COLLEGE);
  foreach $line (@TempArray)  {
    ($id, $name) = split(/\s+/, $line);
    $college{$id} = $name;
  }
  return(%college);
}

###############  系所資料加入學院別, 此函式尚未更新! Nidalap May27,1999
###############  加入學院別已經更新 6/3 ionic
sub Add_Dept
{
  my($DeptFile) = $REFERENCE_PATH."/Dept";
  my(%dept,$dept_string,$no);

  ($dept{id},$dept{cname},$dept{cname2},$dept{college},$dept{password})=@_;
  $dept_string=join("\t",$dept{id},$dept{cname},$dept{cname2},$dept{college});
  open(DEPT,$DeptFile) or die("Cannot open file $DeptFile!\n");
   @TempArray = <DEPT>;
   chop(@TempArray);
  close(DEPT);
  $no = @TempArray;
  $TempArray[$no] = $dept_string;
  @TempArray=sort(@TempArray);
  open(DEPT,">$DeptFile");
  foreach $item(@TempArray)
  {
   print DEPT $item,"\n";
  }
  close(DEPT);
  if($dept{password} ne "")
  {
   Change_Dept_Password($dept{id}, $dept{password});
  }
}
#########################################################################
## ionic 6/3 ##

sub Delete_Dept
{
  my($dept_cd);
  my($DeptFile) = $REFERENCE_PATH."/Dept";
  my(@dept,$dept,@TempArray,$temp,$i);
  $i=0;
  ($dept_cd)=@_;

  open(DEPT,$DeptFile) or die("Cannot open file $DeptFile!\n");
  @TempArray = <DEPT>;
  close(DEPT);
  open(DEPT,">$DeptFile");
  foreach $Dept(@TempArray)  {
    ($dept,$temp) = split(/\s+/,$Dept); 
    if( $dept ne $dept_cd )
    {
     print DEPT $Dept;
    }
  }
  close(DEPT);
}
###########################################################################
#####  is_Math_Dept()
#####  回傳該系所是否是數學系相關係所.
#####  因為在第一階段選課期間, 數學系所開設的課程是先選先贏額滿為止,
#####  系統採用不同天給學生選課的方式, 故需判斷.
#####  傳回值: [0,1] = [不是, 是]
#####  Added: 2003/01/09, Nidalap :D~
sub is_Math_Dept
{
  my($dept) = @_;
  if( ( ($dept eq "2104") or 
        ($dept eq "2106") or
        ($dept eq "2306") or
        ($dept eq "2316") or
        ($dept eq "2406")
      ))
  {
    return(1);
  }else{
    return(0);
  }
}
###########################################################################
#####  is_Exceptional_Dept()
#####  回傳該系所代碼，是否為例外單位(非一般系所)
#####  傳入值：[$dept, $exclude_dept_phy]
#####  傳回值: [0,1] = [不是, 是]
#####  Added: 2010/05/17, Nidalap :D~
sub is_Exceptional_Dept
{
  my($dept, $exclude_dept_phy) = @_;		 ###  第二個參數若為 1，則體育中心也算做一般單位。
  
  return(1)  if( $dept eq $DEPT_CGE );		###  通識中心
  return(1)  if( $dept eq $DEPT_EDU );		###  師培中心
  return(1)  if( $dept eq $DEPT_LAN );		###  語言中心
  return(1)  if( $dept eq $DEPT_MIL );		###  軍訓
  return(1)  if( ($dept eq $DEPT_PHY) and ($exclude_dept_phy ne "1") );		###  體育中心
  
  return(0);									###  一般單位
}

###########################################################################
#####  is_Undergraduate_Dept()
#####  回傳該系所代碼是否是大學部所使用.
#####  一般情況可直接以代碼尾碼判斷, 但如通識等代碼則有例外
#####  傳回值: [0,1,2] = [不是, 是大學部的系, 是大學部所用]
#####  Added: 2003/04/24, Nidalap :D~
sub is_Undergraduate_Dept
{
  my($dept) = @_;
  return(3)  if( $dept =~ /014$/ );			### 尾碼 014 是某學院學士班
  return(1)  if( $dept =~ /4$/ );          ### 尾碼為4
  return(2)  if( ($dept eq $DEPT_CGE) or	### 通識教育中心	# 2008/05/08 7006->I001
                 ($dept eq $DEPT_PHY) or	### 體育中心
                 ($dept eq "I000") or		### 共同科
                 ($dept eq $DEPT_MIL) or	### 軍訓室
				 ($dept eq $DEPT_LAN)		### 語言中心  # 2015/05/26 added
               );
  return(0);                               ### else
}
##################################################################################
#####  回傳該代碼是否為一個合法的系所代碼
#####  此函式不檢查該代碼是否存在，只是檢查是否隱藏了不安全的字元
#####  傳回值: [0,1] = [不是, 是]
#####  Added: 2010/03/25, Nidalap :D~
sub is_Valid_Dept
{
  my($id) = @_;
  my $pass, @c;
  $pass = 1;					###  預設為通過
  
  $pass = 0  if( length($id) != 4 );		###  檢查字元長度
  $pass = 0  if( $id =~ /\W/ );			###  檢查不可有 [0-9a-zA-Z] 以外的字元
  
  return($pass);
}


###################################################################################
#####  回傳某系所對應的學院
#####  因應文學院需求-委由各系實際執行開課需求
#####  轉換身份，若一般學系則轉換至「該學院學士班」(X014)
#####  若輸入學系代碼為語言中心，則轉換為通識中心，反之亦然（語言中心開設通識外語需求）
#####  傳入值: 系所代碼
#####  傳回值: 所屬學院代碼
sub Find_Dept_College
{
  my($dept) = @_;
  my $college;
  
  print "[dept, LAN, CGE] = [$dept, $DEPT_LAN, $DEPT_CGE]<BR>\n";
  
  if( $dept eq $DEPT_LAN ) {						###  如果是語言中心
    $college = $DEPT_CGE;
  }elsif( $dept eq $DEPT_CGE ) {					###  如果是語言中心
    $college = $DEPT_LAN;
  }else{											###  否則傳回該學系所屬學院(目前只有文學院會用)
    #$college = substr($dept, 0, 1) . "01" . substr($dept, 3, 1);
	$college = substr($dept, 0, 1) . "014";				###  「語言所」切換身份仍是開設「文學院學士班」（非碩士班）課程  20150817
  }
#  $college = "1234";

  return $college;  
}

###################################################################################
#####  判斷輸入系所代碼是否擁有可以切換身份的權限
#####  回傳值：[0,1,2] = [ 不可(一般系所)，可(文學院)，可(語言中心) ]
#####  Updates:
#####    2015/05/26 整合文學院下各系可開設文學院課程，以及更早的語言中心可開設通識外語課功能。 by Nidalap :D~
sub Dept_Can_Switch
{
  my($dept) = @_;
  
  return 1	if( $dept =~ /^1...$/ );
  return 2	if( $dept eq $DEPT_LAN);
    
  return 0;  
}
####################################################################################
sub Find_All_College
{
  my %college = 
    (
	  "1" => {"c"=>"文學院", "e"=>"College of Humanities"},
	  "2" => {"c"=>"理學院", "e"=>"College of Sciences"} ,
	  "3" => {"c"=>"社會科學學院", "e"=>"College of Social Sciences"},
	  "4" => {"c"=>"工學院", "e"=>"College of Engineering"},
	  "5" => {"c"=>"管理學院", "e"=>"College of Management"},
	  "6" => {"c"=>"法學院", "e"=>"College of Law"} ,
	  "7" => {"c"=>"教育學院", "e"=>"College of Education"},
	  "8" => {"c"=>"其他", "e"=>"Others"} 	
	);

  return %college;
}
#####################################################################################
#####  判斷兩個系所代碼是否對應到同一個系所
#####  因應系所改代碼，若選課學生系所代碼與開課（或支援）系所代碼不符合，此函式可判斷兩者相同。
#####  回傳值：[0,1] = [不相同, 相同]
#####  Updates: 
#####    2016/12/19 撰寫此函式，並且在篩選程式 SystemChoose.pl 中採用 by Nidalap :D~
sub is_Same_Dept
{
  my ($dept1, $dept2) = @_;
  my @TempArray, $deptcd, $com_deptcd;
  
  if( !defined(%dept_com) ) {       ###  如果還沒有抓取過新舊系所代碼對照表，先從檔案中抓取，並存在全域變數 %dept_com 中
    my $dept_com_file = $REFERENCE_PATH . "dept_com.txt";
    open(DEPT_COM, $dept_com_file) or die("Cannot open file $dept_com_file!\n");
    @TempArray = <DEPT_COM>;
    close(DEPT_COM);
    foreach $line (@TempArray) {
      ($deptcd, $com_deptcd) = split(/\s+/, $line);
      $dept_com{$com_deptcd} = $deptcd;
    }
  }
  
  return 1  if($dept1 eq $dept2);
  return 1  if( defined($dept_com{$dept1}) and $dept_com{$dept1} eq $dept2 );
  return 1  if( defined($dept_com{$dept2}) and $dept_com{$dept2} eq $dept1 );
  return 0;  
}

