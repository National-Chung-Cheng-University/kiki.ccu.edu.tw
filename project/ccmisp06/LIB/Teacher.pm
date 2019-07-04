1;

#####  Handle_Teacher_File.pm
#####  讀寫教師資料
#####       Read_Teacher_File()    讀取 teacher.txt
#####       輸出: @Teacher         儲存所有老師的教師代碼
#####             %Teacher_Dept    教師代碼相對應的系所
#####             %Teacher_Name    教師代碼相對應的姓名    
#####
#####       Write_Teacher_File()   寫入 teacher.txt
#####       輸入: $Teacher_Code,$Teacher_Dept,$Teacher_Name (需照順序)
#####
#####       Delete_Teacher()       將一位教師資料刪除
#####       輸入: $Teacher_Code    
#####
#####       Sort_Teacher_File()    將 teacher.txt 依照系所排序
#####      
##### program by ionic 1998/8/26


sub Read_Teacher_File
{
 my(@Teacher,$temp,$cname,$i,@Data,$data,@ename, $ename);
 open(FILE,"<$REFERENCE_PATH/teacher.txt");
 @Data=<FILE>;
 close(FILE);
 chop(@Data);
 $i=0;
 
 #$IS_ENGLISH = 1;
 
 foreach $data(@Data)
 {
   ($temp,$Teacher[$i],$cname,@ename )=split(/\s+/,$data);
   if($Teacher_Dept{$Teacher[$i]} eq "") {
     $Teacher_Dept{$Teacher[$i]}=$temp;
   }
   $ename = join(" ", @ename);
   $ename =~ s/^\s+//;
   $ename =~ s/\s+$//;
   #print $Teacher[$i] . ":$ename<BR>\n";
   if( $IS_ENGLISH and ($ename ne "") ) {
     $Teacher_Name{$Teacher[$i]}=$ename;
   }else{
     $Teacher_Name{$Teacher[$i]}=$cname;
   }
   $i++;
 }
 if( $IS_ENGLISH ) {
   $Teacher_Name{99999} = "Undetermined";
 }else{
   $Teacher_Name{99999} = "教師未定";
 }
 return @Teacher;
}

sub Write_Teacher_File
{
 my($Teacher_Code,$Teacher_Dept,$Teacher_Name);
 ($Teacher_Code,$Teacher_Dept,$Teacher_Name)=@_;
 if($Teacher_Code eq "" || $Teacher_Dept eq "" || $Teacher_Name eq "")
 {
  print "系統發現錯誤 in Handle_Teacher_File.pm!";
  print "<br>請聯絡系統管理者!<br>";
  exit(0);
 }
 open(FILE,">>$REFERENCE_PATH/teacher.txt");
  print FILE "$Teacher_Dept\t$Teacher_Code\t$Teacher_Name\n";
 close(FILE);
 Sort_Teacher_File();
}

sub Sort_Teacher_File
{
 my(@Data,$data);
 open(FILE,"<$REFERENCE_PATH/teacher.txt");
  @Data=<FILE>;
 close(FILE);
 @Data=sort(@Data);
 open(FILE,">$REFERENCE_PATH/teacher.txt");
  foreach $data(@Data)
  {
   print FILE $data;
  }
 close(FILE);
}

sub Delete_Teacher
{
 my(@Data,$data,$Teacher_Code,$temp,$useless);
 ($Teacher_Code)=@_;
 open(FILE,"<$REFERENCE_PATH/teacher.txt");
  @Data=<FILE>;
 close(FILE);
 open(FILE,">$REFERENCE_PATH/teacher.txt");
  foreach $data(@Data)
  {
   ($useless,$temp,$useless)=split(/\s+/,$data);
   if($temp ne $Teacher_Code)
   {
    print FILE $data;
   }
  }
 close(FILE);
}
####################################################################
###  由傳入 @T 教師代碼, 傳回教師姓名的字串
###  很不幸地, 須先執行 Read_Teacher_File() 
###  Update:
###    2004/03/05 從 Add_Course01.cgi copy 出來.
sub Format_Teacher_String
{
  my @T = @_;
  my($T, $teacher, $string);

  $T = @T;
#  print("T = $T<BR>\n");
  for($teacher=0; $teacher < $T; $teacher++){
    if($T[$teacher] != 99999){
      $string = $string . $Teacher_Name{$T[$teacher]};
    }else{
      $string = $string . "教師未定";
    }
    if($teacher != $T-1){
      $string = $string .", ";
    }
#    print("$T[$teacher]<BR>\n");
  }
#  print("$string<BR>\n");
  return($string);
}