#!/usr/local/bin/perl

####################################################################################
#####  Create_Support_Course_View
#####  由目前開課資料, 產生 "支援本班課程" 網頁, 
#####  加快支援本班課程查詢的功能.
#####  需要資料: 開課資料
#####  輸出資料: $dest_path 下的檔案. 檔案數量 = 系所# * 年級# * 班級#
#####  Coder   : Nidalap
#####  Updates:
#####    2008/04/28 Created by Nidalap
#####    2010/02/24 比照另外幾個程式，從 BIN/ 搬到 WWW/ 下，給管理者操作  Nidalap :D~
#####################################################################################

$| = 1;
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH . "Common_Utility.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Course.pm";
require $LIBRARY_PATH . "Teacher.pm";
require $LIBRARY_PATH . "Classroom.pm";

$dest_path = $DATA_PATH . "Course_supported/";
@dept = Find_All_Dept();
%classroom = Read_All_Classroom();
Read_Teacher_File();

print("Content-type:text/html\n\n");
print('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">');
print("產生開課資料(支援本班課程的檔案)<HR>\n");
if( not -e $dest_path ) {
  mkdir($dest_path, 0755);
}else{
  print("正在清除舊資料...\n");
  Clean_Old_Data($dest_path);  
}
      
print("產生的網頁會放在: $dest_path 下<BR>\n");
print("  正在產生以下系所資料:");
foreach $dept (@dept) {
  $dept =~ /^(.)/;
  $changeline = $1;
  if( $old_changeline != $changeline ) {
    $old_changeline = $changeline;
    print("<BR>\n");
  }
  print(" $dept");
  Create_Course_Supported($dept);
}
print("\n資料產生完畢!\n");
############################################################################
sub Clean_Old_Data()
{
  my(@files, $readme_file);
  my($path) = @_;
  opendir(PATH, $path);
  
  @files = readdir(PATH);
  foreach $file (@files) {
    next if( ($file eq ".") or ($file eq "..") );
    $file = $path . $file;
    unlink $file;
#    print("unlink $file\n");
  }
  $readme_file = $path . "README.txt"; 
  open(README, ">$readme_file");
  print README ("本目錄所有檔案都是程式產生, 請勿直接修改.\n");
  print README ("產生檔案的程式是 $0\n");
  close(README);
}

############################################################################
#####  整理該系所支援她系的課程資料, 整理到該系所屬的檔案
sub Create_Course_Supported()
{
  ($dept) = @_;						# 開課系所
#  $html_file = $HTML_PATH . $dept . ".html";
#  open(HTML, ">$html_file") or die("Cannot create index file $html_file!\n");
  my($filename, $time_string, $teacher_string, $note, $temp);

  @course = Find_All_Course($dept, "", "");
  %dept = Read_Dept($dept);
  foreach $course (@course) {
#    print("$dept -> $$course{id}, $$course{group}\n");
    %course = Read_Course($dept, $$course{id}, $$course{group}, "", "");
    if( @{$course{support_dept}} > 0 )  {
#      print("Processing $dept	$course{id}	$course{group}: $course{support_dept}\n");
      @support_dept = $course{support_dept};
#      print("support_dept = @support_dept");

#      print("[ ${$course{support_dept}[0]}, $$course{support_dept}[0] ]\n");
#      foreach $support_dept ( @support_dept )  {
      foreach $support_dept ( @{$course{support_dept}} ) {
        @{$course{support_grade}} = ("1","2","3","4")    if( @{$course{support_grade}} == 0 );		##  如果沒有支援年級, 則設為所有年級
        foreach $support_grade ( @{$course{support_grade}} ) { 
          @{$course{support_class}} = ("A","B","C","D")   if( @{$course{support_class}} == 0 );		##  如果沒有支援班級, 則設為所有班級                  
          foreach $support_class ( @{$course{support_class}} ) { 
            Add_Course_Supported($dept, $support_dept, $support_grade, $support_class, $$course{id}, $$course{group});
          }
          
        }
      }
    }
  }
}

#####################################################################################
#####  將支援科目資料儲存到檔案中
sub Add_Course_Supported()
{
  my($dept, $support_dept, $support_grade, $support_class, $course_id, $course_group) = @_;
  my($supp_file);

  $supp_file = $dest_path . $support_dept . "_" . $support_grade . $support_class;
#  print("Adding: $dept, $support_dept, $support_grade, $support_class  -> $supp_file\n");
  open(SUPP_FILE, ">>$supp_file") or die("Cannot append to $supp_file!\n");
  print SUPP_FILE ("$dept\t$course_id\t$course_group\n");
  close(SUPP_FILE);
}



#    $time_string = Format_Time_String($course{time});
#    $teacher_string = Format_Teacher_String(@{$course{teacher}});
#    $note = Determine_Note(%course);
#    foreach $ele ( @{$course{time}} ) {
#      $filename = $$ele{week} . "_" . $$ele{time};
#      $filename = $dest_path . $filename;
#      open(FILE, ">>$filename");
#      print FILE ("$dept\t$dept{cname2}\t$course{grade}\t$course{id}\t$course{group}\t$course{total_time}\t$time_string\t");
#      print FILE ("$course{number_limit}\t$classroom{$course{classroom}}{cname}\t$teacher_string\t$note\t$course{cname}\n");
#      print("$course{id}_$course{group} -> $filename\n");
#    }  


###########################################################################
sub Determine_Note()
{
  my %course = @_;
  my $note = 0;
  
  $note++  if( $course{support_dept}[0] ne "" );
  $note++  if( $course{support_grade}[0] ne "" );
  $note++  if( $course{support_class}[0] ne "" );
  $note++  if( $course{ban_dept}[0] ne "" );
  $note++  if( $course{ban_grade}[0] ne "" );
  $note++  if( $course{ban_class}[0] ne "" );
  $note++  if( $course{prerequisite_course}[0] ne "" );
  $note++  if( $course{note} ne "" );
    
  return $note;      
}
###########################################################################



