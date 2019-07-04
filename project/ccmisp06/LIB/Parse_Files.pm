1;

#####  Parse_Files.pm
#####  讀取一些常用的檔案, 建立資料陣列
#####  函式:
#####       Parse_Dept_File()       讀取 Dept
#####       Parse_Student_File()    讀取 student.txt
#####  Version 1.0
#####  Coder: Nidalap (Super BUG Maker!)

############################################################################
#####  Parse_Dept_File()
#####    用途: 讀取系所代碼
#####    輸入: (None)
#####    輸出: @DEPT  (各系所的代碼)
#####    需求: 檔案 Dept
#####    影響: %DEPT  (系所及其中文簡稱對應)
############################################################################
sub Parse_Dept_File
{
  my($DeptFile) = $REFERENCE_PATH."Dept";
  my(@dept,$dept,$temp);
  open(DEPT,$DeptFile) or die("Cannot open file $DeptFile!\n");
  @dept = <DEPT>;
  close(DEPT);
  foreach $dept(@dept)  {
    ($dept,$temp) = split(/\s+/,$dept); 
    $DEPT{$dept} = $temp;
  }
  return(@dept);
}
############################################################################
#####  Parse_Student_File()
#####    用途: 讀取學生學號及相關資料
#####    輸入: (None)
#####    輸出: %stu_dept  學號對應的系所代碼
#####    需求: student.txt
#####    影響: (Global Var) %stu_grad 學號對應的學生年級
###########################################################################
sub Parse_Student_File
{
  my($student_file) = $REFERENCE_PATH."student.txt";
  my($line,$id,$temp,$temp2,$junk,$stu_cname,%stu_dept);
  my($last_digit);
  open(STUDENTFILE,$student_file)  or
            die("Cannot open file$student_file\n");
  while( $line=<STUDENTFILE> )  {
    ## 4154    4    A     Y     0    482415021   M   李永祥
    ( $temp,$temp2,$junk,$junk,$junk,    $id,   $junk, $stu_cname )  = 
        split(/\s+/,$line);

    $last_digit = chop($temp);
    $last_digit='6' if($last_digit eq '8');
    $temp = $temp . $last_digit;

    $stu_dept{$id} = $temp;
#    print("$id ---> $stu_dept{$id}\n");
    $stu_grad{$id} = $temp2;
    $stu_cname =~ s/ +//;
    $stu_cname{$id}= $stu_cname;
  }
  close(STUDENTFILE);
  return(%stu_dept);
}
##########################################################################




sub Parse_Students_CNAME
{
  my($student_file) = $REFERENCE_PATH."student.txt";
  my($line,$id,$temp,$temp2,$junk,$stu_cname,%stu_dept);
  my($last_digit);
  open(STUDENTFILE,$student_file)  or
            die("Cannot open file$student_file\n");
  while( $line=<STUDENTFILE> )  {
    ## 4154    4    A     Y     0    482415021   M   李永祥
    ( $temp,$temp2,$junk,$junk,$junk,    $id,   $junk, $stu_cname )  =
        split(/\s+/,$line);

    $last_digit = chop($temp);
    $last_digit='6' if($last_digit eq '8');
    $temp = $temp . $last_digit;

    $stu_dept{$id} = $temp;
#   print("$id ---> $stu_dept{$id}\n");
    $stu_grad{$id} = $temp2;
    $stu_cname =~ s/ +//;
    $stu_cname{$id}= $stu_cname;
  }
  close(STUDENTFILE);
  return(%stu_cname);
}
##########################################################################

