#!/usr/local/bin/perl
############################################################################
#####  View_Student_Course_pdf.cgi
#####  檢視學生選課資料 - 單一學生畢業資格審查表
#####  Coder: Nidalap :D~
#####  Updates: 
#####    2010/03/25 由 View_Student_Course3.cgi 更改而來  Nidalap :D~
#####    2012/02/17 加入檢查學生是否屬於此系所  Nidalap :D~
############################################################################

require "../library/Reference.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."System_Settings.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Select_Course.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Teacher.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Session.pm";

%Input = User_Input();
if( $Input{dept_id} eq "cashier" )  {
#  print("cashier login, password check required...<BR>");
}else{
  %dept  = Read_Dept($Input{dept_id});
}
#Check_Dept_Password($input{dept_id}, $input{password});

#Print_Hash(%Input);

#($year, $term) = ($Input{year}, $Input{term});
($year, $term) = ($YEAR, $TERM);

############################################################################

my(%Student,%Dept);

%Student=Read_Student($Input{id});
%Dept=Read_Dept($Input{dept});

############################################################################
#####  檢查此學生是否屬於此系所  2012/02/17  Nidalap :D~
$stu_dept = Determine_Student_Dept($Student{dept});
if( $stu_dept ne $Dept{id} ) {
  print "Content-type:text/html\n\n";
  print "<FONT color=RED>您無權觀看此學生資料！<BR></FONT>\n";
  print "$stu_dept <-> " . $Dept{id} . "<BR>\n";
  exit();
}

#print("[$Student{id}, $Input{year}, $Input{term}]<BR>\n");
#@MyCourse=Course_of_Student($Student{id}, $Input{year}, $Input{term});
        
if( $Input{dept_id} eq "cashier" )  {
#  print("cashier login, password check required...<BR>");
}else{
  Check_Dept_Password($Input{dept}, $Input{password});
}

#my($HEAD_DATA)=Head_of_Individual($Student{name},$Student{id},$Dept{cname},$Student{grade},$Student{class});

###################    若非選課時間則顯示不可進入  ################
if($SUPERUSER != 1){     ## 非 superuser 的使用者
#  if( (Whats_Sys_State()==0)or(Check_Time_Map(%Student)!=1) ){
  if( Whats_Sys_State()==0 ) {
    print("Content-type:text/html\n\n");
    Enter_Menu_Sys_State_Forbidden($HEAD_DATA);
  }
}
###################################################################

Print_PDF_Content($Input{id});
#my($COURSE_TIME_TABLE) = Create_Course_Time_Table();
#my($BOARD_TEXT) = Read_Board();

#Student_Log("View  ", $Input{id}, "", "", "");

#MAIN_VIEW_HTML($HEAD_DATA,$Table_Data);

###################################################################################
sub Print_PDF_Content
{
  my($id) = @_;
  $id =~ /^(...)/;
  my $pdf_file = $DATA_PATH . "Graduate_PDF/" . $1 . "/" . $id . ".pdf";
  my $buffer;
  if( -e $pdf_file ) {
     print("Content-type:application/pdf\n");
     print("Content-Disposition: attachment;Filename=$id.pdf\n\n");
     open(PDF, $pdf_file) or die("Cannot open file $pdf_file!\n");
     while( read(PDF, $buffer, 1024) ) {
       print $buffer;
     }
  }else{
    print("Content-type:text/html\n\n");
	print $EXPIRE_META_TAG;
    print("錯誤！ 此學生無畢業資格審查表資料($pdf_file)！<P>\n");
  }
}
######################################################################
