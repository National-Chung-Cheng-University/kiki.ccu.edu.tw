#!/usr/local/bin/perl

#############################################################################################
#####  Print_Course.cgi
#####  列印學生選課單
#####  在規定時間給學生列印選課單, 簽名後繳交回教學組.
#####  在執行此程式同時記錄到 Student.log 中, 以便之後查詢.
#####  Coder: Nidalap Leee
#####  Last Updates: 
#####    2000/02/18  ???
#####    2010/01/04  將 $yearterm 改為 $year, $term 以避免民國百年 bug  Nidalap :D~
#####    2013/08/23  英文版相關增修：將顯示文字拉到 Init_Text_Values() 中設定。 Nidalap :D~
##############################################################################################

print("Content-type:text/html\n\n");

require "../library/Reference.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."System_Settings.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Select_Course.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Teacher.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Session.pm";
require $LIBRARY_PATH."English.pm";


my(%Input,%Student,%Dept);

%Input    = User_Input();
($Input{id}, $Input{password}, $login_time, $ip) = Read_Session($Input{session_id}, "", 1);
#print("session_id, id, pass = $Input{session_id}, $Input{id}, $Input{password}<BR>"); 

%system_settings = Read_System_Settings();
%Student  = Read_Student($Input{id});
%Dept     = Read_Dept($Student{dept});
%time     = gettime();

my $BOARD_TEXT = Read_Board();
Check_Student_Password($Input{id}, $Input{password});

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
%txt	  = Init_Text_Values();

#if( ($year==$YEAR) and ($term==$TERM) ) {
#  $yearterm = "";
#}else{
#  $yearterm = $year . $term;
#}
############################################################################

@MyCourse = Course_of_Student($Input{id}, $Input{year}, $Input{term}); 
my($Table_Data)=CREAT_COURSE_TABLE();
$space = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";

if( ($SUPERUSER==1) or ($system_settings{allow_print_student_course}==1) ) {
  Print_HTML();
}else{
  Print_BAN();
}
Print_TAIL();

#################################################################################
sub Print_TAIL()
{
  print qq(
    </BODY>
      $EXPIRE_META_TAG2
    </HTML>
  );
}
#################################################################################

sub Print_BAN()
{
  print "
    <html>
    <head>
      <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
      $EXPIRE_META_TAG
      <TITLE>" . $txt{'html_title'} .  "</TITLE>
    </head>
    <body background='$GRAPH_URL./ccu-sbg.jpg'>
    <center>
      <FONT face='標楷體'>
        <H1>" . $txt{'title'} . "</H1>
      </FONT>
    <HR>
    " . $txt{'not_avail'} . "<BR>
  ";
}

##############################################################################

sub Print_HTML() 
{
  Student_Log("Print ", $Input{id}, "", "", "");
  print "
  <html>
  <head>
    <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
    $EXPIRE_META_TAG
    <TITLE>" . $txt{'html_title'} . "</TITLE>
  </head>
  <body background='$GRAPH_URL./ccu-sbg.jpg'>
    <center>
      <FONT face='標楷體'>
        <H1>" . $txt{'title'} . "</H1>
      </FONT>
    <H3>
   <TABLE border=0 width=100%>
     <TR><TH colspan=5 align=right>" . $txt{'time_print'} . "</TH></TH>
     <TR><TH align=left>" . $txt{'dept'} . "</TH>
         <TH>" . $txt{'grade'} . "</TH>
         <TH>" . $txt{'class'} . "</TH>
         <TH>" . $txt{'sid'} . "</TH>
         <TH align=right>" . $txt{'sname'} . "</TH></TR>
   </TABLE>
   $Table_Data<P>
   </CENTER>"
    	 . $txt{'total1'} . '<u> <SPAN id="total_course">' . $MyCount . '</SPAN> </u>' . $txt{'total2'} 
		 . '<u> <SPAN id="total_credit">' . $CreditSum . '</SPAN> </u>' . $txt{'total3'} . "
     <P>
   <CENTER>
   <TABLE border=1 width=100%>
     <TR><TD>" . $txt{'dept_chair'} ."</TD><TD width=20%>$space</TD>
         <TD align=center nowrap>" . $txt{'adviser'} ."</TD><TD width=20%>$space</TD>
         <TD>" . $txt{'student'} ."</TD><TD width=20%>$space</TD>
         <TD>" . $txt{'mobile'} ."</TD><TD width=20%>$space</TD>
     </TR>
   </TABLE>

   <P>
  ";
##  if($TERM == 3) {      ###  如果是暑修, 要多四個簽章欄位
  if( ($SUB_SYSTEM == 2)or($SUB_SYSTEM == 4)) { ###  如果是暑修, 要多四個簽章欄位
    print qq(
      <TABLE border=1 width=100%>
       <TR>
    );
#    if( $SUB_SYSTEM == 4 ) {    ### 一般生暑修不要出納組, 但是專班要(2005/06/24)
      print qq(
         <TD> $txt{'cashier'} </TD><TD width=20%>$space</TD>
      );
#    }
    print qq(
         <TD align=center nowrap> $txt{'bank_account1'} </TD><TD width=20%>$space</TD>
         <TD> $txt{'bank_account2'} </TD><TD width=20%>$space</TD>
         <TD> $txt{'personal_id'} </TD><TD width=20%>$space</TD>
       </TR>
      </TABLE>
    );
  }
  print "
   </CENTER>
    <FONT size=3 face='標楷體'>
     <UL>
     $BOARD_TEXT
    </FONT>
  <CENTER>
    <a href='javascript:window.print()'>" . $txt{'print_page'} ."</a>
  ";
}



############################################################################
sub CREAT_COURSE_TABLE
{
  my($DATA)="";
  my(@Teachers)=Read_Teacher_File();
  my(@WeekDay)=@WEEKDAY;
  my(@TimeMap)=@TIMEMAP;
  $fs = 2;        ##### 表格內的字體大小 (font size)
  $CreditSum=0;
  $MyCount=@MyCourse;
  @Credit=CREDIT_TABLE();

  $DATA = $DATA."<table width=100% border=1>\n";
  $DATA = $DATA."<tr>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=$fs>" . $txt{'cid'} . "</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=$fs>" . $txt{'cgroup'} . "</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=$fs>" . $txt{'cname'} . "</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=$fs>" . $txt{'teacher'} . "</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=$fs>" . $txt{'credit'} . "</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=$fs>" . $txt{'property'} . "</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=$fs>" . $txt{'weekday'} . "</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=$fs>" . $txt{'classroom'} . "</font></th>\n";
  $DATA = $DATA."</tr>\n";

  ####  列印相關課程資料  ####
  for($i=0; $i < $MyCount; $i++){
    my(%theCourse)=Read_Course($MyCourse[$i]{dept},$MyCourse[$i]{id},$MyCourse[$i]{group},$year, $term,"");
      $CreditSum += $theCourse{credit};
      $DATA = $DATA."<tr>\n";
      $DATA = $DATA."<td align=center><font size=$fs>";
      $DATA = $DATA.$theCourse{id};                         ##  科目代碼
      $DATA = $DATA."</font></td>\n";
      $DATA = $DATA."<td align=center><font size=$fs>";
      $DATA = $DATA.$theCourse{group}."</font></td>\n";     ##  班別

      $theCourse{cname} =~ s/、/、 /;
      $theCourse{cname} =~ s/＆/＆ /;
      $DATA = $DATA."<td align=left><font size=$fs>";
      if( $IS_ENGLISH ) {
	    $course_name = $theCourse{ename};
	  }else{
	    $course_name = $theCourse{cname};
	  }
	  
	  $DATA = $DATA.$course_name."</font></td>\n";     ##  科目名稱

      $DATA=$DATA."<td><font size=$fs>";           ##  授課教師
      $T=@{$theCourse{teacher}};
      for($teacher=0; $teacher < $T; $teacher++){
        #if($theCourse{teacher}[$teacher] != 99999){
        $DATA=$DATA.$Teacher_Name{$theCourse{teacher}[$teacher]};
        #}else{
        #  $DATA=$DATA."教師未定";
        #}
        if($teacher != $T-1){
          $DATA=$DATA.", ";
        }
      }
      $DATA=$DATA."</font></td>\n";

      $DATA = $DATA."<td align=center><font size=$fs>";
      $DATA = $DATA.$theCourse{credit}."</font></td>\n";    ##  學分

      $DATA = $DATA."<td align=center><font size=$fs>";
      $DATA = $DATA.$Credit[$MyCourse[$i]{property}];       ##  學分歸屬
      $DATA = $DATA."</font></td>\n";

      $DATA=$DATA."<td align=center><font size=$fs>";           ## 星期節次
      $time_string = Format_Time_String($theCourse{time});
      $DATA .= $time_string;
      $DATA=$DATA."</font></th>\n";

      $DATA=$DATA."<td align=left><font size=$fs>";           ##  教室
      %Room=Read_Classroom($theCourse{classroom});
      $DATA=$DATA.$Room{name};
      $DATA=$DATA."</font></td>\n";

      $DATA = $DATA."</tr>\n";
  }
  $DATA = $DATA."</table>\n";
  return($DATA);
}
#-----------------------------------------------------------------------
sub Check_Time_Map
{
  ###################################################
  ##  Step 1: 取得學生的年級##
  ##  Step 2: 讀取相關的時間設定檔##
  ###################################################
  my($user)=@_;
  my($MapClass)=Check_Map_Class($user);
  my($FileName)=$REFERENCE_PATH."SelectTimeMap/".$MapClass.".map";

  %User=Read_Student($user);
  open(FILE,"<$FileName");
      @Orignal=<FILE>;
      foreach $item(@Orignal){
        my($dept, $state)=split(/\s+/,$item);
        $My_Time{$dept}=$state;
      }
  $FileName=$REFERENCE_PATH."TimeMap/T".$My_Time{$User{dept}}.".map";
  open(FILE,"<$FileName");
  my($count)=0;
  @Duration=<FILE>;
  foreach $item(@Duration){
    $item=~s/\n//;
    ($TD[$count]{S},$TD[$count]{E})=split(/\s+/,$item);
    $count++;
  }

  ($sec,$min,$hour,$day,$nmonth,$year,$wday,$yday,$isdst) = localtime(time);

  $Value=$min+$hour*100;

  for($i=0; $i < $count; $i++){
    if( ($Value > int($TD[$i]{S})) && ($Value < int($TD[$i]{E})) ){
      $Flag = 1;
    }
  }

  return($Flag);
}
#-----------------------------------------------------------------------
sub Check_Map_Class
{
  my($user)=@_;
  %User=Read_Student($user);

  if($User{dept}%10 <= 4){    ##  大一至大四
    return($User{grade});
  }else{
    if($User{grade} == 1){    ##  研一或博一
      return(5);
    }else{                    ##  研二以上含博士班學生
      return(6);
    }
  }
}

###########################################################################
###  讀取選課單公佈欄
sub Read_Board()
{
  my($text, $board_file, @temp);
  if( $IS_ENGLISH ) {
    $board_file = $REFERENCE_PATH."select_course_board_e.txt";
  }else{
    $board_file = $REFERENCE_PATH."select_course_board.txt";
  }
  
  open(BOARD, $board_file) or 
      Fatal_Error("Cannot read file $board_file in Selected_View00.cgi!");
  @temp = <BOARD>;
  close(BOARD);
  $text = join("", @temp);
  $text =~ s/\n/<br>\n/g;
  return $text;
}

##################################################################################
#####  因應英文版本，將所有要顯示的文字在此整理，依照 $IS_ENGLISH 自動判別  2013/07/25
sub Init_Text_Values
{
  my %txtall;
  #global $SUB_SYSTEM_NAME, $YEAR, $TERM_NAME, $Student, $Dept;
  
  %txtall = (
    'html_title'=> {'c'=>$SUB_SYSTEM_NAME . '學生選課單(' . $Student{name}. ')',
					'e'=>'Course Selection Result for ' . Year_Term_English() },
	'title'		=> {'c'=>'國立中正大學' . $SUB_SYSTEM_NAME . '選課系統<br>' . $year . '學年度第' . $term . '學期選課結果單',
					'e'=>'Course Selection Result for ' . Year_Term_English() . 
						 '<BR>National Chung Cheng University'},
	'not_avail'	=> {'c'=>'選課單目前不開放列印, 於請於加退選截止後列印本單, 謝謝!', 
					'e'=>'The course selection is not available for printing. 
						  Please print it out after the the deadline for ADD/Drop.'},
	'date_print'=> {'c'=>'印製日期:' . $time{'time_string'}, 'e'=>'Date Printed:' . $time{'time_string_e'}},
	'dept'		=> {'c'=>'系所別:' . $Dept{cname}, 'e'=>'Department:' . $Dept{ename}},
	'grade'		=> {'c'=>'年級:' . $Student{grade}, 'e'=>'Year Standing: ' . $Student{grade}},
	'class'		=> {'c'=>'班級:' . $Student{class}, 'e'=>'Class: ' . $Student{class}},
	'sid'		=> {'c'=>'學號:' . $Student{id}, 'e'=>'Student ID: ' . $Student{id}},
	'sname'		=> {'c'=>'姓名:' . $Student{name}, 'e'=>'Student Name: ' . $Student{ename}},
	'total1'	=> {'c'=>'共修習', 'e'=>'You have selected'},
	'total2'	=> {'c'=>'科', 'e'=>'courses and'},
	'total3'	=> {'c'=>'學分', 'e'=>'credits in total.'},
	'dept_chair'=> {'c'=>'系所主管', 'e'=>'Department Chair'},
	'adviser'	=> {'c'=>'導師<br>(指導教授)', 'e'=>'Adviser'},
	'student'	=> {'c'=>'學生', 'e'=>'Student'},
	'mobile'	=> {'c'=>'學生<br>行動電話', 'e'=>'Mobile Phone'},
	'cashier'	=> {'c'=>'出納組', 'e'=>'The Cashier Section<br>(出納組)'},
	'bank_account1'	=> {'c'=>'郵局（台銀）局號', 'e'=>'郵局（台銀）局號'},
	'bank_account2'	=> {'c'=>'郵局（台銀）帳號', 'e'=>'郵局（台銀）局號'},
	'personal_id'=> {'c'=>'身分證字號', 'e'=>'身分證字號'},
    'print_page'=> {'c'=>'【列印本頁】', 'e'=>'[Print this page]'},

	'cid'		=> {'c'=>'科目代碼', 'e'=>'Course ID'},
	'cgroup'	=> {'c'=>'班別', 'e'=>'Class'},
	'cname'		=> {'c'=>'科目名稱', 'e'=>'Course Title'},
	'teacher'	=> {'c'=>'授課教師', 'e'=>'Instructor'},
	'no_teacher'=> {'c'=>'教師未定', 'e'=>'Undetermined'},
	'credit'	=> {'c'=>'學分數', 'e'=>'Credit'},
    'property'	=> {'c'=>'學分歸屬', 'e'=>'Credit Type'},
    'weekday'	=> {'c'=>'星期節次', 'e'=>'Day/Period'},
    'classroom'	=> {'c'=>'教室', 'e'=>'Class Location'},

	'a'		=> {'c'=>'a', 'e'=>'a'}	
  );

  foreach $k (keys %txtall) {
	if( $IS_ENGLISH ) {
	  $txt{$k} = $txtall{$k}{'e'};
	}else{
	  $txt{$k} = $txtall{$k}{'c'};
	}
  }
 
  return %txt;  
}

