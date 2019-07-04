#!/usr/local/bin/perl
######################################################################
#####  View_Student_Course1.cgi
#####  檢視學生選課資料 - 選擇學年學期
#####  Coder: Nidalap :D~
#####  Updates:
#####    2009/05/13 Created
#####    2009/12/29 可查詢最近六個學期的修課名單  Nidalap :D~
######################################################################

printf("Content-type:text/html\n\n");

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH . "Select_Course.pm";
require $LIBRARY_PATH . "Common_Utility.pm";
require $LIBRARY_PATH . "System_Settings.pm";

print("<HTML><HEAD> $EXPIRE_META_TAG");
%Input = User_Input();
#foreach $key (keys %Input) {
#  print("$key -> $Input{$key}<BR>\n");
#}

Check_Dept_Password($Input{dept_cd}, $Input{password});

$sys_state = Whats_Sys_State();
#if( $sys_state == 0 ) {
#  print qq(
#    <html>
#      <head><title>開排課系統</title></head>
#      <body background=$GRAPH_URL/ccu-sbg.jpg>
#        <center>
#         <img src=$GRAPH_URL/open.jpg><P>
#         <h4>檢視學生選課資料</h4><HR>
#         目前系統暫不開放查詢!
#  );
#}else{
#  ($year, $term) = Last_Semester(1);
  %system_settings = Read_System_Settings();

#  foreach $key (keys %system_settings) {   
#    print("$key => $system_settings{$key}<BR>\n");
#  }

  if( $system_settings{redirect_to_query} == 1 ) {			###  如果系統目前正在開新學期的課
    $selected1 = "";							###    那就預設選擇上學期資料
    $selected2 = "selected=\"selected\"";
  }else{
    $selected1 = "selected=\"selected\"";
    $selected2 = "";
  }

  print qq(
    <html>
	  $EXPIRE_META_TAG
      <head><title>開排課系統</title></head>
      <body background=$GRAPH_URL/ccu-sbg.jpg>
        <center>
         <img src=$GRAPH_URL/open.jpg><P>
         <h4>檢視學生選課資料與畢業資格審查表 - 請選擇學年學期</h4><p>
         <form method=post action=View_Student_Course2.cgi>
           <SELECT name=semester>
  );
  for( $i=0; $i<6; $i++ ) {
    ($year, $term) = Last_Semester($i);
    print("<OPTION value=$i ");
    print("SELECTED ")  if( $i==0 );
    print(">$year 學年度第 $term 學期資料</OPTION>\n");

#    print("<OPTION value=$i $selected1>$year 學年度第 $term 學期資料</OPTION>\n");
  }
  print qq(
           </SELECT>
           <P>
           <INPUT type=hidden name=password value=$Input{password}>
     	   <INPUT type=hidden name=id value=$Input{id}>
           <INPUT type=hidden name=dept_id value=$Input{dept_id}>
           <INPUT type=hidden name=dept_cd value=$Input{dept_cd}>
           <INPUT type=hidden name=grade value=$Input{grade}>
           <INPUT type=submit value="列出學生名單">
         </form>
       </center>
     </body>
   </html>
  );
#}

