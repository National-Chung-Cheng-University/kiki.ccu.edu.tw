1;
############################################################################
##### Classroom.pm
##### 處理教室資料
#####   200?/??/?? Program by Ionic
#####   2002/11/19 Modified by Nidalap :D~
#####   2016/06/01 改為到 ccmisp06 的 $MAIN_HOME_PATH1 讀取資料檔 by Nidalap :D~
############################################################################

############################################################################
###  Read_All_Classroom
###  為了避免 Find_All_Classroom 加上 Read_Classroom 造成的額外負擔,
###  使用此函式代替之.
###  Nidalap :D~ 
###  2002/11/19
############################################################################
sub Read_All_Classroom
{
  #my($ClassFile) = $REFERENCE_PATH . "classroom.txt";
  my $ClassFile = $MAIN_HOME_PATH1 . "DATA/Reference/classroom.txt";
  my($class_id,%class,@temp, $line);

  open(CLASS,$ClassFile) or die("Cannot open file $ClassFile!\n");
  @TempArray = <CLASS>;
  close(CLASS);
  
  @txt_replace_e = Read_Classroom_English_Alias();			  #####  英文版所需的置換中英文字串
  foreach $line (@TempArray)  {
    last if($line eq "");
    ($class_id,@temp) = split(/\t/,$line);
    $class{$class_id}{cname}		= $temp[0]; 
	$class{$class_id}{ename}		= Translate_Classroom($class{$class_id}{cname}, @txt_replace_e);	###  翻譯教室英文
	$class{$class_id}{name}			= $IS_ENGLISH ? $class{$class_id}{ename} : $class{$class_id}{cname};
    $class{$class_id}{report_dept}	= $temp[1];
    $class{$class_id}{size_fit} 	= $temp[2];
    $class{$class_id}{allow_add} 	= $temp[3];
    $class{$class_id}{size_max}		= $temp[4];
    $class{$class_id}{note}		= $temp[5];

#    $class{$class_id}{cname} =~ s/ +//;
#    $class{$class_id}{cname} =~ s/　+//;
  }
  return(%class);
}
############################################################################
sub Find_All_Classroom
{
  #my($ClassFile) = $REFERENCE_PATH . "classroom.txt";
  my $ClassFile = $MAIN_HOME_PATH1 . "DATA/Reference/classroom.txt";
  my(@classroom,$classroom,@TempArray,$temp,$i);
  $i=0;
  open(CLASS,$ClassFile) or die("Cannot open file $ClassFile!\n");
  @TempArray = <CLASS>;
  close(CLASS);
  foreach $classroom (@TempArray)  {
    ($classroom,$temp) = split(/\t/,$classroom); 
    $classroom[$i++] = $classroom;
  }
  return(@classroom);
}
######################################################################
sub Read_Classroom
{
  #my($ClassFile) = $REFERENCE_PATH . "classroom.txt";
  my $ClassFile = $MAIN_HOME_PATH1 . "DATA/Reference/classroom.txt";
  my($class_id,%class,@temp, $input_id);
  my @txt_replace_e;
  
  @txt_replace_e = Read_Classroom_English_Alias();			#####  英文版所需的置換中英文字串
  
  ($input_id)=@_;

  if( $input_id eq "" ) {
    $class{id}		= "";
    $class{cname}	= "";
    return(%class);
  }
  open(CLASS,$ClassFile) or die("Cannot open file $ClassFile!\n");
  @TempArray = <CLASS>;
  close(CLASS);
  foreach $class_id (@TempArray)  {
    last if($class_id eq "");
    ($class_id,@temp) = split(/\t/,$class_id); 
    if( $class_id eq $input_id ) {
      $class{id}	= $class_id;
      $class{cname}	= $temp[0];
	  $class{ename}	= Translate_Classroom($class{cname}, @txt_replace_e);	###  翻譯教室英文
	  $class{name} = $IS_ENGLISH ? $class{ename} : $class{cname};	  
      $class{report_dept} = $temp[1];
      $class{size_fit}	= $temp[2];
      $class{allow_add}	= $temp[3];
      $class{size_max}	= $temp[4];
      $class{note}	= $temp[5];

#      $class{cname} =~ s/ +//;
#      $class{cname} =~ s/　+//;
      last;
    }
  }
  return(%class);
}
##########################################################################
#####  讀取教室特定字串翻譯英文之檔案
sub Read_Classroom_English_Alias
{
  my @txt_replace_e, $alias_file, @lines, $str_c, $str_e;
  my $i=0;
  
  #$alias_file = $REFERENCE_PATH . "classroom_e_alias.txt";
  $alias_file = $MAIN_HOME_PATH1 . "DATA/Reference/classroom_e_alias.txt";
  
  open(C_ALIAS, $alias_file) or return @txt_replace_e;				###  如果找不到對應檔，直接傳回空值
  @lines = <C_ALIAS>;
  close(C_ALIAS);
  
  foreach $line (@lines) {
    chop($line);
    ($str_c, $str_e) = split(/\t/, $line);
	#$txt_replace_e[$i++] = {'c' => $str_c, 'e' => $str_c . "<BR>" . $str_e };
	$txt_replace_e[$i++] = {'c' => $str_c, 'e' => $str_e };
  }
  
  return @txt_replace_e;
}
##########################################################################
#####  透過 Read_Classroom_English_Alias() 的教室中英文文字對照，翻譯教室名稱
sub Translate_Classroom
{
  my($room_name, @txt_replace_e) = @_;
  foreach $txt_r (@txt_replace_e) {
    $room_name =~ s/$$txt_r{'c'}/$$txt_r{'e'}/;
  }
  return $room_name;
}
##########################################################################
sub Add_Classroom
{
  #my($ClassFile) = $REFERENCE_PATH . "classroom.txt";
  my $ClassFile = $MAIN_HOME_PATH1 . "DATA/Reference/classroom.txt";
  
  my($class_id,%class,$temp,$temp2,%input_class, @classrooms);

  (%input_class)=@_;

  open(CLASS,$ClassFile) or return "FALSE";
   @classrooms = <CLASS>;
  close(CLASS);
  foreach $classroom(@classrooms)  {
    $classroom =~ s/\n//;
    ($class_id,$temp) = split(/\s+/,$classroom); 
    if( $class_id eq $input_class{id} )  
    {
     return "EXISTS";
     goto EXIT;
    }
  }

  my $allow_add = $input_class{size_max} - $input_class{size_fit};
  $class_string = join("\t", $input_class{id}, $input_class{cname}, $input_class{report_dept}, $input_class{size_fit}, $allow_add, $input_class{size_max});
#  $class_string = $input_class{id}."\t".$input_class{cname};
  push(@classrooms,$class_string);
  @classrooms = sort(@classrooms);
  open(CLASS,">$ClassFile");
  foreach $classroom (@classrooms) {
    print CLASS ("$classroom\n");
  }

#  open(CLASS,">> $ClassFile");
#  print CLASS $input_class{id}."\t".$input_class{cname}."\n";
#  close(CLASS);
 
  EXIT:
  return "TRUE";
}
###########################################################################
sub Delete_Classroom
{
  #my($ClassFile) = $REFERENCE_PATH . "classroom.txt";
  my $ClassFile = $MAIN_HOME_PATH1 . "DATA/Reference/classroom.txt";
  
  my($class_id,%class,$temp,$Found,$input_id);
  my(@TempArray);

  ($input_id)=@_;

  open(CLASS,$ClassFile) or return "FALSE";
  @TempArray = <CLASS>;
  close(CLASS);
  $Found=0;
  open(CLASS,">$ClassFile");
  foreach $line (@TempArray)  {
    ($class_id,$temp) = split(/\s+/,$line); 
    if( $class_id eq $input_id )  {
      $Found++;
    }else{
      print CLASS $line;
    }
  }
  close(CLASS);
  if( $Found ) {
    return "TRUE";
  }else{
    return "NOT_FOUND";
  }
}