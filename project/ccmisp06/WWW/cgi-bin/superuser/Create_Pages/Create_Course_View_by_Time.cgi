#!/usr/local/bin/perl

#############################################################################
#####  Create_Course_View_by_Time
#####  由目前開課資料產生以時間查詢開課資料檔,
#####  加快以時間查詢的功能.
#####  需要資料: 開課資料
#####  輸出資料: $dest_path/* 共 (15+10)*7 個檔案
#####  Coder   : Nidalap
#####  Date    : 2004/03/02
#############################################################################

$| = 1;
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH . "Common_Utility.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Course.pm";
require $LIBRARY_PATH . "Teacher.pm";
require $LIBRARY_PATH . "Classroom.pm";

$dest_path = $DATA_PATH . "Course_by_time/";

@dept = Find_All_Dept();
%classroom = Read_All_Classroom();
Read_Teacher_File();

print("Content-type:text/html\n\n");
print('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">');
print("產生開課資料(以時間查詢的檔案)<BR>\n");
if( not -e $dest_path ) {
  mkdir($dest_path, 0755);
}else{
  print("正在清除舊資料...<BR>\n");
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
  Create_Course_View_by_Time($dept);
}
print("<BR>\n<H1>資料產生完畢!<BR>\n");
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
sub Create_Course_View_by_Time()
{
  ($dept) = @_;
#  $html_file = $HTML_PATH . $dept . ".html";
#  open(HTML, ">$html_file") or die("Cannot create index file $html_file!\n");
  my($filename, $time_string, $teacher_string, $note);

  @course = Find_All_Course($dept, "", "");
  %dept = Read_Dept($dept);
  foreach $course (@course) {
#    print("$dept -> $$course{id}, $$course{group}\n");
    %course = Read_Course($dept, $$course{id}, $$course{group}, "", "");
    $time_string = Format_Time_String($course{time});
    $teacher_string = Format_Teacher_String(@{$course{teacher}});
    $note = Determine_Note(%course);
    foreach $ele ( @{$course{time}} ) {
      $filename = $$ele{week} . "_" . $$ele{time};
      $filename = $dest_path . $filename;
      open(FILE, ">>$filename");
      print FILE ("$dept\t$dept{cname2}\t$course{grade}\t$course{id}\t$course{group}\t$course{total_time}\t$time_string\t");
      print FILE ("$course{number_limit}\t$classroom{$course{classroom}}{cname}\t$teacher_string\t$note\t$course{cname}\n");
#      print("$course{id}_$course{group} -> $filename\n");
    }  
  }
}

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



