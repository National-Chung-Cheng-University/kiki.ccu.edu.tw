#!/usr/local/bin/perl
#########################################################################################
#####  查詢修課學生名單
#####  判斷 Query_1.cgi 傳來的 print_notebook 參數，以決定要列出某系課科目人數統計表，
#####  或是進入列印上課記事簿登入畫面。
#####  Updates:
#####    199x/xx/xx Created
#####    2009/10/30 新增「列印上課記事簿」功能，由 print_notebook 值判定  Nidalap :D~
#####    2010/05/12 將學號末兩碼以及名字做馬賽克  Nidalap :D~
#####	 2010/06/08 馬賽克改為只針對未經系所登入者才會做。  Nidalap :D~

print "Content-type: text/html","\n\n";

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."System_Settings.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Teacher.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."Select_Course.pm";
require $LIBRARY_PATH."Error_Message.pm";

Print_Html_Header("國立中正大學開排選課系統 - 查詢修課學生名單","$GRAPH_URL/ccu-sbg.jpg");

$sys_state = Whats_Sys_State();

if( $sys_state == 0 ) {
  print qq(
    <html>
      <head><title>中正大學SUB_SYSTEM_NAME開排選課系統 - 查詢修課學生名單</title></head>
      <body background=$GRAPH_URL/ccu-sbg.jpg>
        <center>
         <img src=$GRAPH_URL/open.jpg><P>
         <h4>查詢修課學生名單功\能</h4><HR>
         目前系統暫不開放查詢!
  );
  exit(1);
}

#####  處理使用者輸入的資料
%now = gettime();
my($temp1,$temp2);
%Input = User_Input();
%Input = Sanitize_Input(%Input);
($temp1,$temp2)=split(/_/,$Input{course_cd});
($year, $term) = Last_Semester($Input{last_semester});
#print("Read_Course($Input{dept_cd},$temp1,$temp2, $year, $term) <BR>\n");
%Course = Read_Course($Input{dept_cd},$temp1,$temp2, $year, $term);

#foreach $k (keys %Input) { 
#  print("$k --> $Input{$k}<BR>\n"); 
#} 

#####  若是系所登入過，檢查密碼
if( $Input{login_dept_id} and $Input{password} ) {
  $password_pass = Check_Dept_Password($Input{login_dept_id}, $Input{password});
}  

#####  判別要帶出選課學生名單，或是列印上課記事簿
if( $Input{"print_notebook"} == 1 ) {
  Print_Notebook_Login();  
}else{
  print qq[
    <H4>您查詢的是第 $year 學年度第 $term 學期 $Dept{cname} 的課程</H4>
  ];
  Print_Namelist();
}
######################################################################################
sub Print_Notebook_Login
{
  print qq[
    <CENTER>
    <FORM action=Print_Notebook.php method=POST>
      請輸入您的身份證號(教師專用): <INPUT type=text name="teacher_id"><P>
      <INPUT type=hidden name=dept_cd value="$Input{dept_cd}">
      <INPUT type=hidden name=course_cd value="$Input{course_cd}">
      <INPUT type=hidden name=last_semester value="$Input{last_semester}">
      <INPUT type="hidden" name="last_select" value="$Input{last_select}">
      <INPUT type=submit value="檢視上課記事簿">
    </FORM>
  ];
}
######################################################################################
sub Print_Namelist
{
  $page = $Input{page};
  if($page eq "") { $page = 0; }

#foreach $k (keys %Input) {
#  print("$k --> $Input{$k}<BR>\n");
#}

###  處理授課教師顯示字串
  my $teacher_string = "";
  @Teachers=Read_Teacher_File();
  $T=@{$Course{teacher}};
  for($teacher=0; $teacher < $T; $teacher++){
    if($Course{teacher}[$teacher] != 99999){
      $teacher_string .= $Teacher_Name{$Course{teacher}[$teacher]};
    }else{
      $teacher_string = "教師未定";
    }
    if($teacher != $T-1){
      $teacher_string .= ", ";
    }
  }
  ###  處理上課時間顯示字串
  $time_string = Format_Time_String($Course{time});

  ### 讀取教室資料
  %Room=Read_Classroom($Course{classroom});
  ### 讀入學生名單 ###
  if( $Input{last_select} == 1 ) {
    $list_title = "上次篩選後名單";
    @Students = Student_in_Course($Input{dept_cd},$Course{id},$Course{group}, "last");  
  }else{
    $list_title = "目前選課名單";
    @Students = Student_in_Course($Input{dept_cd},$Course{id},$Course{group}, $year, $term);
  }
  $total = @Students;
  $total_page = int($total/90);
  
  my($temp);
  $temp =$page +1;
#  Print_Html_Header("$Course{cname} 修課學生名單第 $temp 頁","$GRAPH_URL/ccu-sbg.jpg");
#  if( ($year==$YEAR) and ($term==$TERM) ) {
    print qq[
      <FORM action=Query_2.cgi method=POST>
        <INPUT type=hidden name=dept_cd value=$Input{dept_cd}>
        <INPUT type=hidden name=dept_name value=$Dept{cname}> 
        <INPUT type=hidden name=course_cd value=$Input{course_cd}>
        <INPUT type=hidden name=last_semester value="$Input{last_semester}">
        <INPUT type=hidden name=print_notebook value=1>
        <INPUT type=submit value="列印上課記事簿">        
      </FORM>
    ];
#  }
                        
  print("$Course{cname} 修課學生名單第 $temp 頁<BR>\n");
  @Students=sort(@Students);

  $temp= $total_page+1;

  ## 顯示科目基本資料 ##
#  print "$Input{print_notebook}";
  print "</center>";
  print "科目名稱: $Course{cname}<br>";
  print "科目代碼: $Course{id} , 科目班別: $Course{group}<br>";
  print "授課教師: $teacher_string<BR>";
  print "上課時間: $time_string<BR>";
  print "上課教室: $Room{cname}<BR>";
  print "修課人數: $total , 共分 $temp 頁<br>";
  print "本名單是 <FONT color=RED>$list_title</FONT><BR>";
  print "資料處理時間: $now{time_string}<BR>";

  if( ($page+1)*90 > $total )
  { $Limit= $total; }
  else { $Limit=($page+1)*90 ; }

  print "<table border=0 width=100%>";
  print "<tr>";
  my(%student);

  #print("page = $page; total = $total, Limit = $Limit<BR>\n");
  for($i=($page*90); $i<$Limit ; $i++ )
  {
  # print("$i<BR>\n");
    if($i %30 ==0 )
    { print "<td valign=top><table border=1>\n"; }
 
    %student = Read_Student($Students[$i]);  
    %dept = Read_Dept($student{dept});
    if( $password_pass ne "TRUE" ) {			###  若沒有透過系所登入過，名字都改為 XX。 20100608 Nidalap :D~
      $student{id}	=~ s/..$/XX/;
      $student{name}	=~ s/(^..).+/$1XX/;
    }
    print "<tr><th align=left>$dept{cname2}</th>";
    print "<td>$student{id}</td><th align=left>$student{name}</th></tr>\n";
  
    if( ($i+1) % 30 ==0 || $i ==($Limit-1) )
    { print "</table></td>"; }
  }
  print "</tr></table>\n";

  if( $page ne "" && $page ne "0" )
  {
   $Temp=$Input{'page'}-1;
   print qq(
     <form method="post" action="Query_2.cgi">
       <input type="hidden" name="dept_cd" value="$Input{'dept_cd'}">
       <input type="hidden" name="course_cd" value="$Input{'course_cd'}">
       <input type="hidden" name="page" value="$Temp">
       <input type="hidden" name="last_select" value="$Input{last_select}">
       <input type="hidden" name="last_semester" value="$Input{last_semester}">
   );
   if( $password_pass eq "TRUE" ) {		###  只有系所登入要傳此值
     print qq(
       <INPUT type="hidden" name="login_dept_id" value="$Input{login_dept_id}">
       <INPUT type="hidden" name="password"      value="$Input{password}">
     );
   }
   print qq(
       <input type="submit" value="翻前一頁">
     </form>
   );
   
  }
  print "<br>";
  if( $total_page > $page )
  {
   $Temp=$Input{'page'}+1;
   print qq(
     <form method="post" action="Query_2.cgi">       
       <input type="hidden" name="dept_cd" value="$Input{'dept_cd'}">             
       <input type="hidden" name="course_cd" value="$Input{'course_cd'}">             
       <input type="hidden" name="page" value="$Temp">             
       <input type="hidden" name="last_select" value="$Input{last_select}">
       <input type="hidden" name="last_semester" value="$Input{last_semester}">
   );
   if( $password_pass eq "TRUE" ) {             ###  只有系所登入要傳此值
     print qq(
       <INPUT type="hidden" name="login_dept_id" value="$Input{login_dept_id}">
       <INPUT type="hidden" name="password"      value="$Input{password}">
     );
   }                                                                          
   print qq(  
       <input type="submit" value="翻下一頁">
     </form>       
   );
  }

  print "<p><a href=\"Login.cgi\">回到查詢修課學生主選單</a><br>\n";
  print "<a href=\"http://www.ccu.edu.tw\">回中正大學首頁</a>\n";
}
#####################################################################################
sub Print_Html_Header
{
 my($title,$BG)=@_;
 print qq(
  <HTML>
    <HEAD>
      $EXPIRE_META_TAG
      <TITLE>$title</TITLE>
    </HEAD>
    <BODY background="$BG">
      <CENTER>
        <H1>
          $title
        </H1>
      </CENTER>
      <HR>
 );
}
####################################################################################
sub Print_Html_Tail
{
 print "</center>\n";
 print "</Body>\n";
 print "</Html>\n";
}
