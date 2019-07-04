#!/usr/local/bin/perl
########################################################################################
#####  Get_Total_Credit.cgi
#####  顯示學生總學分數（給教專系統使用）
#####  輸入：多個學號
#####  輸出：每個學號及其總學分數
#####  Updates: 
#####    2016/01/08  本來教專系統連到 Selected_View00.cgi，但因為回傳太多不需要的東西，
#####				 所以用 Selected_View_Multiple.cgi 改了這支程式 Nidalap :D~
########################################################################################

#print("Content-type:text/html\n\n");

require "../library/Reference.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Password.pm";
#require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Select_Course.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Teacher.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Session.pm";
require $LIBRARY_PATH."System_Settings.pm";

###########################################################################

$online_help = Online_Help();

$bypass = 0;

print("Content-type:text/plain\n\n");
%Input			= User_Input();
$in_key			= $Input{key};
$in_timestamp	= $Input{key1};
@id				= split(/\*:::\*/, $Input{id});

$id_sum = 0;
foreach my $id (@id) {
  $id_sum += $id;
}

$key = Generate_Key2($id_sum, "bOsSlesSLESswORK", $in_timestamp);		### 基本安全檢查
if( $key ne $in_key ) {
  if( !$bypass ) {
    Print_BAN("key_error");
  }
}


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


my(%Student,%Dept);

foreach $id (@id) {
  #print("processing $id...<BR>\n");
  %Student=Read_Student($id);
  if( $Student{name} eq "" ) {
    #print("$id: 無此學生資料!\n");
    next;
  }
  @MyCourse=Course_of_Student($Student{id}, $year, $term);

  $CreditSum = 0;
  foreach $cour (@MyCourse) {
    %cou=Read_Course($$cour{dept},$$cour{id},$$cour{group},$year, $term);
    $CreditSum += $cou{'credit'};
  }
  
  print $Student{id} . ":" . $CreditSum . "\n";
  
}
