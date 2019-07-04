#!/usr/local/bin/perl
#########################################################################################
#####  查詢修課學生名單
#####  判斷 Query_2.cgi 傳來的教師人事代碼以及科目代碼，列印該科目上課記事簿。
#####  Updates:
#####    2009/12/23 Created by Nidalap :D~
#####    2010/01/04 將原先讀取舊學期資料所傳入的 $yearterm 改為 $year 和 $term, 以避免民國百年 bug.  Nidalap
#####	 2010/09/17 將教師人事代碼轉換為大寫  Nidalap :D~
#####    2010/09/23 改為：若是系所登入則檢查系所密碼，若是尚未登入則檢查上一頁傳來的教師身份證號  Nidalap :D~

print "Content-type: text/html","\n\n";

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."System_Settings.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Teacher.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."Select_Course.pm";
require $LIBRARY_PATH."Error_Message.pm";

$sys_state = Whats_Sys_State();

#####  處理使用者輸入的資料
my($temp1,$temp2);
%Input = User_Input();
%Input = Sanitize_Input(%Input);

#foreach $k (keys %Input) {
#  print("$k --> $Input{$k}<BR>\n");
#}  

($temp1,$temp2)=split(/_/,$Input{course_cd});
($year, $term) = Last_Semester($Input{last_semester});
%Course = Read_Course($Input{dept_cd},$temp1,$temp2, $year, $term);

%now = gettime();
$title = "國立中正大學 $SUB_SYSTEM_NAME <U>$year</U> 學年度";
$title .= "第 <U>$term</U> 學期  教師上課記事簿";
Print_Html_Header($title,"$GRAPH_URL/ccu-sbg.jpg");

if( $sys_state == 0 ) {
  print qq(
        <center>
         <img src=$GRAPH_URL/open.jpg><P>
         <h4>查詢修課學生名單功\能</h4><HR>
         目前系統暫不開放查詢!
  );
  Print_Html_Tail();
  exit(1);
}


#####  做一下安全檢查
#$id = Quotes($Input{id});
$teacher_id = uc($Input{teacher_id});

#####  判別輸入的教師人事代碼，是否是此科目的開課教師之一
$valid_teacher = 0;
if( $Input{login_dept_id} and $Input{password} ) {		###  如果是系所登入
  $password_pass = Check_Dept_Password($Input{open_dept}, $Input{password});  
}else{
  foreach $teacher (@{$Course{teacher}}) {
    $valid_teacher = 1  if( $teacher_id eq $teacher );
#    print("teacher = $teacher<BR>\n");
  }
  if( $valid_teacher == 0 ) {
    print qq(<H1>錯誤：您並非本科目授課教師！</H1>); 
    Print_Html_Tail();
    exit(1);
  }
}

#foreach $k (keys %Input) {
#  print("$k --> $Input{$k}<BR>\n");
#}

$notebook = Format_Notebook();

sub Format_Notebook
{
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
#  %Room=Read_Classroom($Course{classroom});
  ### 讀入學生名單 ###
  if( $Input{last_select} == 1 ) {
    $list_title = "上次篩選後名單";
    @Students = Student_in_Course($Input{dept_cd},$Course{id},$Course{group}, "last");  
  }else{
    $list_title = "目前選課名單";
    @Students = Student_in_Course($Input{dept_cd},$Course{id},$Course{group}, $year, $term);
#  print("$Input{dept_cd},$Course{id},$Course{group}, $year, $term<BR>\n");
  
  }
  $total = @Students;
#  $total_page = int($total/90);
#  
#  my($temp);
#  $temp =$page +1;
#  Print_Html_Header("$Course{cname} 修課學生名單第 $temp 頁","$GRAPH_URL/ccu-sbg.jpg");
#  print("$Course{cname} 修課學生名單第 $temp 頁<BR>\n");
  @Students=sort(@Students);
#  $temp= $total_page+1;

  ## 顯示科目基本資料 ##
 
  $th  = "科目編號: $Course{id} &nbsp;&nbsp; 科目班別: $Course{group} &nbsp;&nbsp; ";
  $th .= "學分數: $Course{credit} &nbsp;&nbsp; 修課人數: $total &nbsp;&nbsp; ";
  $th .= "授課教師: $teacher_string<BR>";
  $th .= "科目名稱: $Course{cname}<br>";
  
  print qq[
    <P ALIGN=RIGHT>
      (本表供教師平時記事考核用)  &nbsp;&nbsp;&nbsp;&nbsp;  列印日期: $now{time_string3}
    </P>
    <TABLE border=1 width=100%>
      <TR align=JUSTIFY>
        <TH colspan=8>$th</TH>
      </TR>
      <TR>
        <TH width=10%>系所別</TH><TH width=10%>學號</TH><TH width=10%>姓名</TH>
        <TH>備註</TH><TH colspan=4>重要記事</TH>
      </TR>
  ];
#  print "$Input{print_notebook}";
#  print "</center>";
#  print "科目名稱: $Course{cname}<br>";
#  print "科目代碼: $Course{id} , 科目班別: $Course{group}<br>";
#  print "授課教師: $teacher_string<BR>";
#  print "上課時間: $time_string<BR>";
#  print "上課教室: $Room{cname}<BR>";
#  print "修課人數: $total , 共分 $temp 頁<br>";
#  print("本名單是 <FONT color=RED>$list_title</FONT>");

#  if( ($page+1)*90 > $total )
#  { $Limit= $total; }
#  else { $Limit=($page+1)*90 ; }
#
#  print "<table border=0 width=100%>";
#  print "<tr>";
  my(%student);

  #print("page = $page; total = $total, Limit = $Limit<BR>\n");
#  for($i=($page*90); $i<$Limit ; $i++ )
  for($i=0; $i<$total; $i++) {
  # print("$i<BR>\n");
#    if($i %30 ==0 )
#    { print "<td valign=top><table border=1>\n"; }
 
    %student = Read_Student($Students[$i]);  
    %dept = Read_Dept($student{dept});
    print qq[
      <TR>
        <TD>$dept{cname2}</TD><TD>$student{id}</TD><TD>$student{name}</TD>
        <TD>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</TD>
        <TD width=7%>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</TD>
        <TD width=7%>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</TD>
        <TD width=7%>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</TD>
        <TD width=7%>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</TD>
    ];
#    if( ($i+1) % 30 ==0 || $i ==($Limit-1) )
#    { print "</table></td>"; }
  }
  print "</tr></table>\n";

#  if( $page ne "" && $page ne "0" )
#  {
#   $Temp=$Input{'page'}-1;
#   print qq(
#     <form method="post" action="Query_2.cgi">
#       <input type="hidden" name="dept_cd" value="$Input{'dept_cd'}">
#       <input type="hidden" name="course_cd" value="$Input{'course_cd'}">
#       <input type="hidden" name="page" value="$Temp">
#       <input type="hidden" name="last_select" value="$Input{last_select}">
#       <input type="hidden" name="yearterm" value="$Input{yearterm}">
#       <input type="submit" value="翻前一頁">
#     </form>
#   );
#  }
#  print "<br>";
#  if( $total_page > $page )
#  {
#   $Temp=$Input{'page'}+1;
#   print qq(
#     <form method="post" action="Query_2.cgi">       
#       <input type="hidden" name="dept_cd" value="$Input{'dept_cd'}">             
#       <input type="hidden" name="course_cd" value="$Input{'course_cd'}">             
#       <input type="hidden" name="page" value="$Temp">             
#       <input type="hidden" name="last_select" value="$Input{last_select}">
#       <input type="hidden" name="yearterm" value="$Input{yearterm}">
#       <input type="submit" value="翻下一頁">
#     </form>       
#   );
#  }

  print "<p><a href=\"Login.cgi\">回到查詢修課學生主選單</a><br>\n";
#  print "<a href=\"http://www.ccu.edu.tw\">回中正大學首頁</a>\n";
}
#####################################################################################
sub Print_Html_Header
{
  my($title,$BG)=@_;
  $BG = $GRAPH_URL . "/ccu-sbg.jpg"  if($BG eq "");
  print qq(
   <HTML>
     <HEAD>
       $EXPIRE_META_TAG
       <TITLE>$title</TITLE>
     </HEAD>
     <BODY background="$BG">
       <CENTER>
         <H2>
           $title
         </H2>
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
