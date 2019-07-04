#!/usr/local/bin/perl
############################################################################
#####  Teacher_Course02.cgi
#####  教師查詢當學期一般生與碩士在職專班授課明細
#####  此功能不從教師專業系統連結過來，因為該系統不給兼任教師使用。
#####  Updates: 
#####	2016/01/12 Created by Nidalap :D~
############################################################################
#print("Content-type:text/html\n\n");

require "../library/Reference.pm";
require $LIBRARY_PATH."Common_Utility.pm";
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
require $LIBRARY_PATH."System_Settings.pm";

###########################################################################

$online_help = Online_Help();

print("Content-type:text/html\n\n");
%Input			= User_Input();
$in_key			= $Input{key};
$in_timestamp	= $Input{key1};

$in_teacher_id = $Input{'teacher_id'};
$in_teacher_id = 'R122389443';

#$key = Generate_Key2($id_sum, "bOsSlesSLESswORK", $in_timestamp);		### 基本安全檢查
#if( $key ne $in_key ) {
#  Print_BAN("key_error");
#}


print $EXPIRE_META_TAG;
#foreach $key (keys %Input) {
#  print("$key -> $Input{$key}<BR>\n");
#}

if( Check_HTTP_REFERER() != 1 ) {			###  檢查來源
#  print("error!!!");
  Show_Password_Error_Message();
}

############################################################################
###  由輸入的 year, term 判斷是否要讀取本學期資料, 或是以前的資料
if( $Input{year} != "" ) {
  $year = $Input{year};
}else{
  $year = $YEAR;
}

if( $Input{term} != "" ) {
  $term = $Input{term};
}else{
  $term = $TERM;
}

#if( ($year==$YEAR) and ($term==$TERM) ) {
#  $yearterm = "";
#}else{
#  $yearterm = $year . $term;
#}
#print("session_id, id, pass = $Input{session_id}, $id, $Input{password}<BR>"); 

############################################################################



Get_Teacher_Courses();

Switch_To_GRA(1);
print("reference path = $REFERENCE_PATH<BR>\n");
print("course path = $COURSE_PATH<BR>\n");

Get_Teacher_Courses();
 
Switch_To_GRA(0);
print("reference path = $REFERENCE_PATH<BR>\n");
print("course path = $COURSE_PATH<BR>\n");

foreach $cou (@teacher_course) {
  print "$$cou{'id'} - $$cou{'group'}<BR>\n";
}

##############################################################################
sub Print_BAN()
{
  my($msg) = @_;
  if( $msg eq "key_error" ) {
    $msg_show = "驗證碼錯誤，<FONT color=RED>請回上一頁重新讀取</FONT>，以更新驗證碼！";
  }else{
    $msg_show = "";
  }
  
  print qq(
    <html>
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <TITLE>國立中正大學$SUB_SYSTEM_NAME選課系統--檢視目前已選修科目</TITLE>
    </head>
    <body background="$GRAPH_URL./ccu-sbg.jpg">
    <center>
      <FONT face="標楷體">
        <H1>國立中正大學$SUB_SYSTEM_NAME選課系統--檢視目前已選修科目</H1>
      </FONT>
    <HR>
    $msg_show<BR>
  );
  die();
}
#############################################################################################
sub Get_Teacher_Courses
{
  my %Dept, @courses, %course;
  my @dept = Find_All_Dept();
  foreach $dept (@dept) {
    %Dept=Read_Dept($Student{dept});
    @courses = Find_All_Course($dept, "", $year, $term);
    foreach $course (@courses) {
	  %course = Read_Course($dept, $$course{'id'}, $$course{'group'}, $year, $term);
	  #print "looking teachers for course... <BR>\n";
	  #print %course;
	  foreach $teacher (@{$course{'teacher'}}) {
	    if( $teacher eq $in_teacher_id) {
	      #%temp = ('id' => $$course{'id'}, 'group' => $$course{'group'});
		  #%temp = ('id' => "123456", 'group' => "02");
		  #Print_Hash(%temp);
	      %{$teacher_course[$i++]} = (
			'id' => $$course{'id'}, 
			'group' => $$course{'group'}, 
			'credit' => $$course{'credit'}, 
			'cname' => $$course{'cname'}, 
			'time' => $$course{'time'}, 
			'classroom' => $$course{'classroom'}
		  );
#		  push(@teacher_course, %temp);
	      #print "teacher teaches in course $$course{'id'} _ $$course{'group'}<BR>\n";
	    }
	  }
    }
  }
}
#############################################################################################
sub Switch_To_GRA
{
  my($switch) = @_;
  if( $switch == 1 ) {
    $LIBRARY_PATH =~ s/ccmisp06/ccmisp07/g;
  }else{
    $LIBRARY_PATH =~ s/ccmisp07/ccmisp06/g;
  }
  require $LIBRARY_PATH . "Reference.pm";
  require $LIBRARY_PATH."Dept.pm";
  require $LIBRARY_PATH."Course.pm";
  require $LIBRARY_PATH."Error_Message.pm";
}