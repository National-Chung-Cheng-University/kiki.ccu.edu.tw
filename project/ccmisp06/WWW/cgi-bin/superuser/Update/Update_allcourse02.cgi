#!/usr/local/bin/perl 
###########################################################################
#####  Update_Course.pl
#####  讀取資料庫傳上來的開課歷史檔(allcourse.txt), 製作相對應檔案及目錄
#####  Updates:
#####   1999/04/21 Created by Nidalap Leee
#####   2010/11/25 加入新增的 gender_eq, env_edu 等六個欄位.  Nidalap :D~
#####   2015/06/12 因加入 $open_dept 欄位，修改 Append_Classindex().  Nidalap :D~
#####  執行前請確定歷史檔格式無誤!
###########################################################################

$| = 1;
require "../../library/Reference.pm";

print("Content-type:text/html\n\n");

print $EXPIRE_META_TAG;
print("<BODY background=\"../../../Graph/manager.jpg\">");
print("<CENTER><H1>更新課程資料檔</H1><HR>");

$AllCourseFile = $DATA_PATH . "Transfer/allcourse.txt";
open(ALLCOURSE, $AllCourseFile) or
   die("Cannot open file $AllCourseFile!\n");
#$temp = <ALLCOURSE>;                          ###  第一行是欄位名稱, 此欄不用
@line = <ALLCOURSE>;
close(ALLCOURSE);
print("依據 allcourse.txt, 更新開課歷史資料檔 DATA/Course/* ... <P>\n");
print("正在清除舊有的歷史科目檔......<BR>\n");
Clear_Old_History_Course();
print("正在寫入新的歷史科目檔......<P>\n");
foreach $line (@line) {
  chomp($line);
  ( $course{dept}, $course{id}, $course{grade}, $course{group}, 
    $course{credit}, $course{total_time}, $course{property}, 
    $course{suffix_cd}, $course{attr}, $course{cname}, @ename)
          = split(/\t/, $line);
  $course{ename} = join(" ",@ename);
  $course{grade} =~ /(.)./;   $course{grade} = $1;
  
  if( $course{dept} =~ /8$/ ) {					###  將開在博班的課放到碩班 added 2014/12/03
    $course{dept} =~ s/8$/6/;
  }
  
  if( $course{id} =~ /^902....$/ ) {
    $course{dept} = "F000";
  }elsif($course{id} =~ /^903....$/ ) {
    $course{dept} = "V000";
  }
  print("$course{dept}, \n")
     if($course{dept} ne $last_dept);
  $course_path = $HISTORY_COURSE_PATH . $course{dept} . "/";  
  if( not -e $course_path ) {
    #print("making dir [$course_path]<BR>\n");
    system("mkdir $course_path");
  }
  if($last_id ne $course{id}) {
    Append_Classindex();
    Write_Course_File();
  }
  $last_id = $course{id};
  $last_dept = $course{dept};
}

print ("請繼續執行<BR><A href=Update_allcourse03.cgi>更新資料第三步</A>");

#########################################################################
sub Clear_Old_History_Course()
{
  if($HISTORY_COURSE_PATH eq "") {
    die("HISTORY_COURSE_PATH is null, check for linkage of modules!\n");
  }
  system("rm -fr $HISTORY_COURSE_PATH*");
}
#########################################################################
sub Append_Classindex()
{
  $index_file = $course_path . "classindex";

  open(INDEX,">>$index_file") or die("Cannot append to file $index_file!\n");
#  print INDEX ("$course{id}\t$course{grade}\t$course{group}\n")
  print INDEX ("$course{id}\t$course{grade}\t01\t$course{dept}\n");
  close(INDEX);
}
#############################################################################
sub Write_Course_File()
{
#  $course_file = $course_path . $course{id} . "_" . $course{group};
  $course_file = $course_path . $course{id} . "_01";

  open(COURSE,">$course_file") or
     die("Cannot write to file $course_file!\n");
  print COURSE ("$course{cname}\n");
  print COURSE ("$course{ename}\n");
  print COURSE ("$course{total_time}\n");
  print COURSE ("$course{credit}\n");
  print COURSE ("$course{classroom}\n");
  print COURSE ("$course{property}\n");
  print COURSE ("$course{teacher}\n");
  print COURSE ("$course{time}\n");
  print COURSE ("$course{number_limit}\n");
  print COURSE ("$course{support_dept}\n");
  print COURSE ("$course{support_grade}\n");
  print COURSE ("$course{support_class}\n");
  print COURSE ("$course{ban_dept}\n");
  print COURSE ("$course{ban_grade}\n");
  print COURSE ("$course{ban_class}\n");
  print COURSE ("$course{reserved_number}\n");
  print COURSE ("$course{principle}\n");
  print COURSE ("$course{suffix_cd}\n");
  print COURSE ("$course{total_time}\n");   ### lab_time1
  print COURSE ("0\n");                     ### lab_time2
  print COURSE ("0\n");                     ### lab_time3
  print COURSE ("0\n");    ##  support_cge_type
  print COURSE ("0\n");    ##  support_cge_number
  print COURSE ("\n");     ##  prerequisite_course
  print COURSE ("AND\n");  ##  prerequisite_logic
  print COURSE ("\n");		## distant_learning
  print COURSE ("\n");		## english_teaching
  print COURSE ("\n");		## remedy
  print COURSE ("\n");		## s_match
  print COURSE ("\n");		## gender_eq
  print COURSE ("\n");		## env_edu
  print COURSE ("$course{attr}\n");  ## attr
  print COURSE ("\n");		## reserved 2~4
  print COURSE ("\n");
  print COURSE ("\n");
  print COURSE ("$course{note}");
}


