#!/usr/local/bin/perl
###########################################################################
#####  View_Warning.cgi
#####  檢視篩選公告
#####  Coder: Nidalap :D~
#####  Updates:
#####    2005/02/17  本來和 Main.cgi 放在一起, 今年開始把它獨立出來.  Nidalap :D~
#####    2012/06/14  加入特殊情況通知訊息(如選課逾時未關閉，後續回溯等影響)  Nidalap :D~
#####    2013/08/23  英文版相關增修：將顯示文字拉到 Init_Text_Values() 中設定。 Nidalap :D~

print("Content-type:text/html\n\n");
require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Password.pm";
#require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Select_Course.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."System_Settings.pm";
require $LIBRARY_PATH."Session.pm";
require $LIBRARY_PATH."English.pm";

my(%Student,%Dept);
%time = gettime();

%Input = User_Input();

($Input{id}, $Input{password}, $login_time, $ip) = Read_Session($Input{session_id}, "", 1);
#print("session_id, id, pass = $Input{session_id}, $Input{id}, $Input{password}<BR>"); 

#%Input=User_Input();
###########################################################################

%Student=Read_Student($Input{id});
%Dept=Read_Dept($Student{dept});
%system_settings = Read_System_Settings();
%txt = Init_Text_Values();

Check_Student_Password($Input{id}, $Input{password});
#my($HEAD_DATA)=Head_of_Individual($Student{name},$Student{id},$Dept{cname},$Student{grade},$Student{class});
if( $IS_ENGLISH ) {
  $HEAD_DATA = Head_of_Individual($Student{ename},$Student{id},$Dept{ename},$Student{grade},$Student{class});
}else{
  $HEAD_DATA = Head_of_Individual($Student{name},$Student{id},$Dept{cname},$Student{grade},$Student{class});
}

if($SUPERUSER != 1){     ## 非 superuser 的使用者
  ##  warning message 不存在
#  print(" flag = $use_default_password_flag<BR>\n");
  ##  Check the System Status !!  Added by hanchu @ 1999/9/10
  if(Whats_Sys_State() == 0){
    Enter_Menu_Sys_State_Forbidden($HEAD_DATA);
  }else{
    VIEW_WARNING($Input{id}, $Input{password});
  }
}else{                   ## superuser 的使用者
  VIEW_WARNING($Input{id}, $Input{password});
}

########################################################################
#####  VIEW_WARNING()
#####  顯示篩選, 異動, 及異動導致衝堂等訊息
########################################################################
sub VIEW_WARNING
{
  my($id,$password)=@_;
  my($ACTION)="Main.cgi";
  my($Table_Data)="";
  my($Table_Data2)="";
  my($Table_Data3)="";
  my(@Change,@Temp,$i,$count);
  if( $IS_ENGLISH ) {
    $State[0]="Fail";  $State[1]="Success";
  }else{
    $State[0]="未選上";  $State[1]="選上";
  }

  $Table_Data  = Form_System_Choose_Data_Table();
  $Table_Data2 = Form_Course_Change_Data_Table();
  $Table_Data3 = Form_Course_Change_Conflict_Data_Table();
  $Table_Data4 = Form_Prerequisite_Course_Data_Table();
  $Table_Data5 = Form_Duplicate_Course_Data_Table();
  $Table_Data6 = Form_Special_Notification_Table();

  print "
<html>
<head>
    <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
    <title>" . $txt{'title'} . "</title>
</head>
<body background='$GRAPH_URL/ccu-sbg.jpg'>
<center>
$HEAD_DATA<hr size=1>
<FONT color=GREEN>" . $txt{'now'} ." $time{time_string}</FONT><BR>

<FONT color=#dd2222 size=4>" . $txt{'change3'} . "</FONT><P>
$Table_Data4

<FONT color=#dd2222 size=4>" . $txt{'change4'} . "</FONT><P>
$Table_Data5

<hr size=1>
<font color=#dd2222 size=4>" . $txt{'change'} . "</font><p>
  $Table_Data2

<font color=#dd2222 size=4>" . $txt{'change2'} . "</font><p>
$Table_Data3

<font color=#dd2222 size=4>" . $txt{'title'} . "</font><p>
$Table_Data

<FONT color=#dd2222 size=4>" . $txt{'change5'} . "</FONT><P>
$Table_Data6

</center>
</body>
";
}
###########################################################################
#####  Form_System_Choose_Data_Table()
#####  產生並傳回篩選結果的 HTML Table 碼
###########################################################################
sub Form_System_Choose_Data_Table()
{
  my($FILENAME)=$DATA_PATH."Student_warning/".$Student{id}."_warning";
  my($Table_Data, @WARN);
  if(-e $FILENAME){
    open(FILE,"<$FILENAME");
    @WARN=<FILE>;
    close(FILE);
    $Table_Data .= "<TABLE border=0 width=70%><TR><TD>" . $txt{'change6'} . "<br>";
    $Table_Data .= "<FONT color=RED>" . $txt{'change7'} . "</FONT></TD></TR></TABLE><P>";
    $Table_Data .= "<table border=1 width=90%><tr>";
    $Table_Data .= " <th bgcolor=yellow>" . $txt{'cdept'} . "</th><th bgcolor=yellow>" . $txt{'cid'} . "</th>";
    $Table_Data .= " <th bgcolor=yellow>" . $txt{'cname'} . "</th>";
    $Table_Data .= " <th bgcolor=yellow>" . $txt{'cgroup'} . "</th><th bgcolor=yellow>" . $txt{'result'} . "</th></tr>";

    foreach $warn(reverse @WARN){
      $warn=~s/\n//;
      ($dept,$the_id,$group,$state)=split(/\s+/,$warn);
      %the_Dept=Read_Dept($dept);
      %the_Course=Read_Course($dept,$the_id,$group,"","",$id);
	  
	  if( $IS_ENGLISH ) {
	    $dept_name = $the_Dept{ename};
		$cour_name = $the_Course{ename};
	  }else{
	    $dept_name = $the_Dept{cname2};
		$cour_name = $the_Course{cname};
	  }
	  
      $Table_Data .= "<tr>";
      $Table_Data .= "<th>".$dept_name."</th>";
      $Table_Data .= "<th>".$the_id."</th>";
      $Table_Data .= "<th>".$cour_name."</th>";
      $Table_Data .= "<th>".$group."</th>";
      if($state == 0){
        $Table_Data .= "<th><font color=red>".$State[$state]."</font></th>";
      }else{
        $Table_Data .= "<th><font color=blue>".$State[$state]."</font></th>";
      }
      $Table_Data .= "</tr>";
    }
    $Table_Data .= "</table>";
  }else{
    $Table_Data = $txt{'no_affect'};
  }
  return($Table_Data);
}
#########################################################################
#####  Form_Course_Change_Data_Table()
#####  產生並傳回科目異動的 HTML Table 碼
#########################################################################
sub Form_Course_Change_Data_Table()
{
  my($FILENAME2)=$DATA_PATH."Student_warning/".$Student{id}."_change";
  my($Table_Data, @Change);
  if(-e $FILENAME2)  {
    $Table_Data .= 
      $txt['change8'] . "<br>
        <Table border=1 width=90%>
          <tr>
            <th colspan=9 bgcolor=yellow><font size=4>" . $txt{'before'} . "</th>
            <th colspan=4 bgcolor=orange><font size=4>" . $txt{'after'} . "</th>
          </tr>
          <tr>
            <th bgcolor=yellow>" . $txt{'change_type'} . "</th>
			<th bgcolor=yellow>" . $txt{'cdept'} . "</th>
            <th bgcolor=yellow>" . $txt{'cid'} . "</th>
            <th bgcolor=yellow>" . $txt{'cgroup'} . "</th>
			<th bgcolor=yellow>" . $txt{'cname'}. "</th>
            <th bgcolor=yellow>" . $txt{'teacher'} . "</th>
			<th bgcolor=yellow>" . $txt{'property'} . "</th>
            <th bgcolor=yellow>" . $txt{'weekday'} . "</th>
			<th bgcolor=yellow>" . $txt{'classroom'} . "</th>
            <th bgcolor=orange>" . $txt{'teacher'} . "</th>
            <th bgcolor=orange>" . $txt{'property'} . "</th>
            <th bgcolor=orange>" . $txt{'weekday'} . "</th>
			<th bgcolor=orange>" . $txt{'classroom'} . "</th>
          </tr>
      ";
    open(FILE,"<$FILENAME2");
    @Change=<FILE>;
    close(FILE);
    chop(@Change);
    foreach $change(@Change) {
      $Table_Data .="<tr>";
      @Temp = split("###",$change);
      $count=(@Temp);

      for($i=0;$i<$count;$i++)  {
        $Table_Data .="<th>$Temp[$i]</th>";
      }
      $Table_Data .="</tr>";
    }
    $Table_Data .= "</TABLE>" . $txt{'change9'} . $txt{'change10'} . "<br><hr size=1>";
  }else{
    $Table_Data = $txt{'no_affect2'} . "\n<P>";
  }
  $Table_Data .= "<HR size=1>";
  return($Table_Data);
}
########################################################################
#####  Form_Course_Change_Conflict_Data_Table()
#####  產生並傳回異動造成衝堂的 HTML Table 碼
########################################################################
sub Form_Course_Change_Conflict_Data_Table()
{
  my(@Courses,$course,$i,$j,$k,$l,%temp1,%temp2,$flag, $Table_Data3);
  @Courses = Course_of_Student($Student{id});
  $count = (@Courses);
  my $Table_exists_flag = 0;
  
  for($i=0;$i< $count-1;$i++)  {
    for($j=$i+1;$j< $count;$j++)  {
      %temp1=Read_Course($Courses[$i]{dept},$Courses[$i]{id},$Courses[$i]{group});
      %temp2=Read_Course($Courses[$j]{dept},$Courses[$j]{id},$Courses[$j]{group});
      $flag=0;
      
#      for($k=0;$k<$temp1{total_time} && $flag eq "0";$k++)  {
#        for($l=0;$l<$temp2{total_time} && $flag eq "0";$l++)  {
#          if($temp1{time}[$k]{week} eq $temp2{time}[$l]{week} && $temp1{time}[$k]{time} eq $temp2{time}[$l]{time}) {
#            $flag++;
#          }
#        }
#      }
      if($flag ne "0")  {
        if($Table_exists_flag == 0) {     ###  如果Table不存在, 先印出 Table
          $Table_Data3 .= 
               $txt['change11'] . "<br>
               <table border=1 width=90%>
                 <tr>
                   <th colspan=3 bgcolor=yellow><font size=4>" . $txt{'conflict'} . "</th>
                   <th colspan=3 bgcolor=orange><font size=4>" . $txt{'conflict'} . "</th>
                 </tr>
                 <tr>
                   <th bgcolor=yellow>" . $txt{'cid'} . "</th>
                   <th bgcolor=yellow>" . $txt{'cgroup'} . "</th>
				   <th bgcolor=yellow>" . $txt{'cname'} . "</th>
                   <th bgcolor=orange>" . $txt{'cid'} . "</th>
                   <th bgcolor=orange>" . $txt{'cgroup'} . "</th>
				   <th bgcolor=orange>" . $txt{'cname'} . "</th>
                 </tr>
           ";
           $Table_exists_flag = 1;
        }
		if( $IS_ENGLISH ) {
          $Table_Data3.="<TR><th>$temp1{id}</th><th>$temp1{group}</th><th>$temp1{ename}</th>";
          $Table_Data3.="<th>$temp2{id}</th><th>$temp2{group}</th><th>$temp2{ename}</th></TR>";
		}else{
          $Table_Data3.="<TR><th>$temp1{id}</th><th>$temp1{group}</th><th>$temp1{cname}</th>";
          $Table_Data3.="<th>$temp2{id}</th><th>$temp2{group}</th><th>$temp2{cname}</th></TR>";
		}
      }
    }
  }
  if( $Table_Data3 eq "" ) {
    $Table_Data3 .=  $txt['no_affect2'] . "<P>";
  }else{
    $Table_Data3 .= "</TABLE>";
  }
  return($Table_Data3);
}
########################################################################
#####  Form_Prerequisite_Course_Data_Table()
#####  產生並傳回因科目先修條件造成退選的 HTML Table 碼
########################################################################
sub Form_Prerequisite_Course_Data_Table()
{
  my($Table_Data4, @lines, $cou, $pre, %cou, %pre, $cou_name, $pre_name);

  %course_dept = Read_All_Course_Dept();		###  讀取所有科目的所屬系所
  Print_Hash(%course_dept);
  
  my $Table_exists_flag = 0;
  my $pre_file = $DATA_PATH . "Student_warning/" . $Student{id} . "_prerequisite";
  
  if(-e $pre_file) {
    $Table_Data4 = "
        <TABLE border=1 width=90%>
          <tr>
            <th bgcolor=yellow><font size=4>" . $txt{'del_course'} . "</th>
            <th bgcolor=orange><font size=4>" . $txt{'pre_fail'} . "</th>
          </tr>
    ";
    open(PREFILE, $pre_file);
    @lines = <PREFILE>;
    close(PREFILE);
    foreach $line (@lines) {
      $line =~ s/\n/<br>\n/;
      ($cou, $pre) = split(/\t/, $line);
	  $cou = substr($cou, -12, 7);			###  接軌舊版檔案作法，只抓取科目代碼
	  $pre = substr($pre, -13,7);
	  %cou	= Read_Course($$course_dept{$cou}{'dept'}, $cou, '01');
	  %pre	= Read_Course($$course_dept{$pre}{'dept'}, $pre, '01', "HISTORY");
	  
	  #Print_Hash(%pre);
	  	  
	  if( $IS_ENGLISH ) {
	    $cou_name = $cou{'ename'};
		$pre_name = $pre{'ename'};
	  }else{
	    $cou_name = $cou{'cname'};
		$pre_name = $pre{'cname'};
	  }
      $Table_Data4 .= "<TR><TD>$cou_name ($cou)</TD><TD>$pre_name ($pre)</TD></TR>";
    }
    $Table_Data4 .= "</TABLE>";
  }else{
    $Table_Data4 = $txt['no_affect2'] . "<P>"
  }
  return($Table_Data4);
}
########################################################################
#####  Form_Duplicate_Course_Data_Table()
#####  產生並傳回因重複修習造成退選的 HTML Table 碼
########################################################################
sub Form_Duplicate_Course_Data_Table()
{
  my($Table_Data5, @lines, $cou, $pre);

  my $Table_exists_flag = 0;
  my $dup_file = $DATA_PATH . "Student_warning/" . $Student{id} . "_duplicate";
  my($c_id, $c_group, $c_name);

  if(-e $dup_file) {
    $Table_Data5 = "
        <TABLE border=1 width=90%>
          <tr>
            <th bgcolor=yellow><font size=4>" . $txt{'del_course'} . "</th>
          </tr>
    ";
    open(DUPFILE, $dup_file);
    @lines = <DUPFILE>;
    close(DUPFILE);
    foreach $line (@lines) {
      $line =~ s/\n//;
      ($c_id, $c_group, $c_name) = split(/\t/, $line);
      $Table_Data5 .= "<TR><TD>$c_name($c_id, $c_group)</TD></TR>";
    }
    $Table_Data5 .= "</TABLE>";
  }else{
    $Table_Data5 = $txt{'no_affect2'} . "<P>"
  }
  return($Table_Data5);
}
########################################################################
#####  Form_Special_Notification_Table
#####  產生特殊情形通知的 Table(如系統因故回溯導致影響等)
sub Form_Special_Notification_Table
{
  my $table_data;
  
  my $file = $DATA_PATH . "Student_warning/" . $Student{id} . "_special";
  
  if( -e $file ) {
    $table_data = "
      <TABLE border=1 width=90%>
        <tr>
          <th bgcolor=yellow><font size=4>已過選課時間加退之科目篩選公告</th>
        </tr>
    ";
    open(SPEC_FILE, $file);
    @lines = <SPEC_FILE>;
    close(SPEC_FILE);
    foreach $line (@lines) {
      $line =~ s/\n//;
      $table_data .= "<TR><TD>$line</TD></TR>";
    }
    $table_data .= "</TABLE>";
  }else{
    $table_data = $txt['no_affect2'] . "<P>";
  }
  return($table_data);
}

##################################################################################
#####  因應英文版本，將所有要顯示的文字在此整理，依照 $IS_ENGLISH 自動判別  2013/07/25
sub Init_Text_Values
{
  my %txtall;
  
  %txtall = (
    'title'		=> {'c'=>'檢視篩選公告', 'e'=>'Course Screening Result'},
	'now'		=> {'c'=>'目前時間是:', 'e'=>'Current Time:'},
	'change'	=> {'c'=>'科目異動公告', 'e'=>'Course update announcement'},
	'change2'	=> {'c'=>'以下科目因科目異動影響導致衝堂', 'e'=>'Course update resulting in schedule conflict'},
	'change3'	=> {'c'=>'以下科目因不符先修條件導致退選', 'e'=>'Course dropped by the system: prerequisite requirement'},
	'change4'	=> {'c'=>'以下科目因重複修習導致退選', 'e'=>'Course dropped by the system: courses already taken'},
	'change5'	=> {'c'=>'特殊情形通知', 'e'=>'Other notice'},
	'change6'	=> {'c'=>'<LI>您選修的科目經過系統人數限修篩選結果如下表<FONT color=RED>(最上面為最近的紀錄)</FONT>。
						<LI>若篩選結果為未選上，則此科目已經由系統幫您退選。', 
					'e'=>'The result of priority screening for your selected courses is as followed (the system will automatically drop those courses that do not pass priority screen): '},
	'change7'	=> {'c'=>'<LI>選課資料以選課清單為主，請至主選單中「檢視已選修科目」確認選課結果。', 
					'e'=>'Please go to the main menu and click "Review Courses You Selected" to confirm courses selected.'},
	'change8'	=> {'c'=>'您選修的科目經過科目異動影響如下', 
					'e'=>'The effect of the course update on your course  selection is as follows:'},
	'change9'	=> {'c'=>'若科目異動屬性為取消,則此科目已經由系統幫您退選', 
					'e'=>'If the course has been cancelled, the system will automatically drop the course for you.'},
	'change10'	=> {'c'=>'若異動後欄位空白代表該欄位並未異動，與異動前內容相同', 
					'e'=>'If the update column is empty, there is no change made to the course.'},
	'change11'	=> {'c'=>'以下每列之左右兩欄科目彼此時間衝堂:', 
					'e'=>'Schedule conflicts: '},
	
	'cdept'		=> {'c'=>'開課系所', 'e'=>'Department'},
	'cid'		=> {'c'=>'科目代碼', 'e'=>'Course ID'},
	'cname'		=> {'c'=>'科目名稱', 'e'=>'Course Title'},
	'cgroup'	=> {'c'=>'班別', 'e'=>'Class'},	
	'result'	=> {'c'=>'篩選結果', 'e'=>'Priority Screening Result'},	
	'no_affect'	=> {'c'=>'系統篩選對您並無影響', 'e'=>'None'},
	'before'	=> {'c'=>'異動前', 'e'=>'Before Course Update'},
	'after'		=> {'c'=>'異動後', 'e'=>'After Course Update'},
	'no_affect2'=> {'c'=>'無影響', 'e'=>'No impact'},
	'conflict'	=> {'c'=>'衝堂科目', 'e'=>'Conflicting Courses'},

	'change_type'=> {'c'=>'異動屬性', 'e'=>'Course Change Type'},
	'teacher'	=> {'c'=>'授課教師', 'e'=>'Instructor'},
	'no_teacher'=> {'c'=>'教師未定', 'e'=>'Undetermined'},
	'credit'	=> {'c'=>'學分數', 'e'=>'Credit'},
    'property'	=> {'c'=>'學分歸屬', 'e'=>'Credit Type'},
    'weekday'	=> {'c'=>'星期節次', 'e'=>'Day/Period'},
    'classroom'	=> {'c'=>'教室', 'e'=>'Class Location'},

	'del_course'=> {'c'=>'被退選科目(代碼,班別)', 'e'=>'Course dropped by system'},
	'pre_fail'	=> {'c'=>'不合先修條件科目(未修習或不及格)', 'e'=>'Prerequisite courses that you have not selected or passed'},

	'a'		=> {'c'=>'a', 'e'=>'a'}	
  );

  foreach $k (keys %txtall) {
	if( $IS_ENGLISH ) {
	  $txt{$k} = $txtall{$k}{'e'};
	}else{
	  $txt{$k} = $txtall{$k}{'c'};
	}
  }
  
  #Print_Hash(%txt);
  
  return %txt;  
}
