#!/usr/local/bin/perl
############################################################################################
#####  Query_by_time2.cgi
#####  以系所, 開課節次時間, 科目名稱, 教師姓名等條件, 搜尋當學期開課資料.
#####  Last Update:
#####    2004/03/02
#####    2008/06/03  新增科目名稱與教師姓名查詢選項.  Nidalap :D~
#####    2009/03/27  允許 "非法字元" 查詢, 將該字元跳脫查詢而非直接禁止. 
#####                所以可以查詢如 "許漢" 等教師開的課. 但是對 "功" 之類的字仍查不到
#####    2013/08/27  英文版相關增修：將顯示文字拉到 Init_Text_Values() 中設定。 Nidalap :D~
#####				 但是只有做半套，因為此程式抓取的資料來源中，沒有英文的！！！
#####				 開學在即，沒時間理它了所以先擱著！！！  2013/08/28
#####    2015/??/??  英文版補全 by Nidalap :D~
#####	 2016/05/09  舊的安全檢查不夠嚴謹，被掃出好幾個漏洞！改為透過 Sanitize_Input() 檢查 Nidalap :D~
############################################################################################
print "Content-type: text/html","\n\n";

require "../library/Reference.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Open_Course.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."English.pm";

#Check_SU_Password($Input{password}, "dept", $Input{dept_cd});

###  在 English.pm 已呼叫過此函式，為避免抓不到 POST 資料，此處不再呼叫。 Nidalap :D~ 2013/08/28
#%Input = User_Input();

%txt	  = Init_Text_Values();

$file_path = $DATA_PATH . "Course_by_time/";
print "
  <HTML>
    <HEAD>
      <TITLE>" . $txt{'title'} . "</TITLE>
      $EXPIRE_META_TAG
      <LINK rel='stylesheet' type='text/css' href='$HOME_URL/font.css'>
    </HEAD>
  <body bgcolor=white background=$GRAPH_URL/ccu-sbg.jpg>
  <center>
    <SPAN class='title1'>" . $txt{'title'} . "</SPAN>
    <BR>
    <IMG src=$TITLE_LINE>
    <P class='illustration'>
";

%Input = Sanitize_Input(%Input);
$teacher_cname = $Input{'teacher_cname'};
#Print_Hash(%Input);

###  在此之後, $course_cname 和 $teacher_cname 用作比對用;
###  $Input{course_cname} 和 $Input{teacher} 用作顯示用.

#print "dept = " . $Input{dept} . "<BR>\n";

@dept = split(/\*:::\*/, $Input{dept_multi});

if( @dept == 0 ) {
  print $txt{'choose_dept'};
  exit();
}

foreach $dept (@dept) {
  $dept_selected{$dept} = 1;
}
Check_Dept(@dept);

$i = 0;
foreach $time (keys %Input) {
  next if( $time !~ /^\d_/);
  $file = $file_path . $time;
#  print("file = $file<BR>\n");
  next if( not -e $file );
  open(TIMEFILE, $file);
#  @{$course[$i]} = <TIMEFILE>;
  @line = <TIMEFILE>;
  foreach $line (@line) {
    ($dept, $dept_cname2, $grade, $id, $grp, $total_time, @junk) = split(/\t/, $line);
    $id = $id . "_" . $grp;
    $course{$time}{$id} = 1;
    $total_time{$id} = $total_time;
    $content{$id} = $line;
#    print("$time, $id, $course{$time}{$id}<BR>\n");
  }
  $i++;
}

$j = 0;
foreach $time (keys %course) {
  foreach $course (%{$course{$time}}) {
    if($time =~ /[A-J]$/) {
      $count{$course} += 1.5;
    }else{
      $count{$course}++;
    }
  }
  $j++;
}

$hits = 0;
$content = "";
foreach $course (sort keys %count) {
  if( $Input{query_type} == 1 ) {
    next if( $count{$course} != $total_time{$course} );
  }
  
  ($dept, $dept_cname2, $grade, $c_id, $c_grp, $total_time, $time_string, $number_limit, $classroom, $teacher, $note, $cname)
     = split(/\t/, $content{$course});
#  next if($dept ne $Input{dept});
  next if($dept_selected{$dept} != 1);						###  如果沒選此系, next
  if( $Input{'course_cname'} ne "" ) {						###  如果有輸入科目名稱, 篩選之
    $course_cname = $Input{'course_cname'};
    if( ($cname !~ /$course_cname/) or ($cname !~ /$course_ename/) ) {
      next;
    }else{
	  if( $IS_ENGLISH ) {
        $cname =~ s/$course_cname/<FONT color=RED>$Input{course_ename}<\/FONT>/g;
	  }else{
	    $cname =~ s/$course_cname/<FONT color=RED>$Input{course_cname}<\/FONT>/g;
	  }
    }
  }
  
  if( $teacher_cname ne "" ) {							###  如果有輸入教師姓名, 篩選之
    if( ($teacher !~ /$teacher_cname/) or ($teacher !~ /$teacher_cname/)) {
      next;
    }else{
      $teacher =~ s/$teacher_cname/<FONT color=RED>$teacher_cname<\/FONT>/g;            
    }
  }
  
  
  if( $last_dept ne $dept ) {
    if($high_light =~ /FFFFFF/) {
      $high_light = "bgcolor = FFFF77";
    }else{
      $high_light = "bgcolor = FFFFFF";
    }
  }
  if( $note == 0 ) {
    $note = $txt{'note0'};
  }else{
    $note = "<A href='$CLASS_URL" . "ShowNote.cgi?&dept=" . $dept . "&course=" . $c_id 
			. "&group=" . $c_grp . "' target=NEW>" . $txt{'note1'} . "</A>";
  }
  $content .= "<TR align=CENTER $high_light><TD>$dept_cname2</TD><TD>$grade</TD><TD>$c_id</TD><TD>$c_grp</TD><TD align=LEFT>$cname</TD><TD>$total_time{$course}</TD>";
  $content .= "<TD>$time_string</TD><TD>$teacher</TD><TD>$classroom</TD><TD>$number_limit</TD><TD>$note</TD></TR>";
#  $content .= "<TR><TD rowspan=2>$dept_cname2</TD><TD rowspan=2>$c_id</TD><TD rowspan=2>$c_grp</TD><TD colspan=5>$cname</TD></TR>";
#  $content .= "<TD>$total_time{$course}</TD><TD>$time_string</TD><TD>$classroom</TD><TD>$number_limit</TD></TR>";

  $hits ++;
  $last_dept = $dept;
#  print("$course, $count{$course}, $total_time{$course}<BR>\n");
}

$Input{course_cname} = $txt{'any'}	if($Input{course_cname} eq "");
$teacher_cname = $txt{'any'}		if($teacher_cname eq "");

print "
    <SPAN class='font1'>
      <CENTER>
      " . $txt{'result1'} . "
      <TABLE border=1>
        <TR><TD>" . $txt{'cname'} . ": </TD><TD>$Input{course_cname}</TD></TR>
        <TR><TD>" . $txt{'teacher'} . ": </TD><TD>$teacher_cname</TD></TR>
      </TABLE>
      " . $txt{'result2'} . $hits  . $txt{'result3'} . "
      <TABLE border=1 class=font1 width=800>
        <TR>
          <TH>" . $txt{'dept'} . "</TH>
		  <TH>" . $txt{'grade'} . "</TH>
		  <TH>" . $txt{'cid'} . "</TH>
		  <TH>" . $txt{'group'} . "</TH>
		  <TH>" . $txt{'cname'} . "</TH>
          <TH>" . $txt{'total_time'} . "</TH>
		  <TH>" . $txt{'weekday'} . "</TH>
          <TH>" . $txt{'teacher'} . "</TH>
		  <TH>" . $txt{'classroom'} . "</TH>
		  <TH>" . $txt{'number_limit'} . "</TH>
		  <TH>" . $txt{'note'} . "</TH>
        </TR>
        $content
        </TR>
      </TABLE>
    <p>
  </body>
  </html>
";
 
######################################################################################
sub Check_Dept()
{
  my(@dept) = @_;
  my($message);
  
#  if( @dept > 7 ) {
#    print("為避免系統負載過大, 請勿一次查詢超過七個系所, 謝謝!<BR>\n");
#    exit();
#  }
}
######################################################################################
#####  因應英文版本，將所有要顯示的文字在此整理，依照 $IS_ENGLISH 自動判別  2013/07/25
sub Init_Text_Values
{
  my %txtall;
    
  %txtall = (
    'title'		=> {'c'=>'進階開課資料查詢 -- 開課資料列表', 'e'=>'Advanced Course Search'},
	'choose_dept'=> {'c'=>'請至少選擇一個系所!', 'e'=>'Select at least one department!'},
	'any'		=> {'c'=>'(無限制) ', 'e'=>'(any)'},

	'result1'	=> {'c'=>'您的查詢條件是: ', 'e'=>'Here are your query conditions: '},
	'cname'		=> {'c'=>'科目名稱', 'e'=>'Course title'},
	'teacher'	=> {'c'=>'教師姓名', 'e'=>'Instructor name'},
	'result2'	=> {'c'=>'共有 ', 'e'=>'There are '},
	'result3'	=> {'c'=>'筆開課資料符合條件 ', 'e'=>' courses that match your query conditions.'},
	
	'sel_time2'	=> {'c'=>'取消所有節次', 'e'=>'Cancel all periods'},
	'sel_time3'	=> {'c'=>'選擇所有我的空堂', 'e'=>'Select all periods without schedule conflict'},
	'sel_time4'	=> {'c'=>'查詢所有"只"使用到這些時段的科目', 'e'=>'Search courses involving with the selected period'},
	'sel_time5'	=> {'c'=>'查詢所有使用到這些時段的科目', 'e'=>'Search courses offered at the selected period'},
	'sel_time6'	=> {'c'=>'請選擇時段(必填)', 'e'=>'Please choose period (required)'},

	'dept'		=> {'c'=>'開課系所', 'e'=>'Department'},
	'grade'		=> {'c'=>'年級', 'e'=>'Year Standing'},
	'cid'		=> {'c'=>'科目代碼', 'e'=>'Course ID'},
	'cgroup'	=> {'c'=>'班別', 'e'=>'Class'},
	'total_time'=> {'c'=>'時數', 'e'=>'Total time'},
	'weekday'	=> {'c'=>'上課時間', 'e'=>'Day/Period'},
	'classroom'	=> {'c'=>'教室', 'e'=>'Class Location'},
	'num_limit'	=> {'c'=>'限修<BR>人數', 'e'=>'Enrollment Limit'},
    'note'		=> {'c'=>'其他<BR>備註', 'e'=>'Other Remarks'},
	
	'note0'		=> {'c'=>'無', 'e'=>'None'},
	'note1'		=> {'c'=>'有', 'e'=>'Click me'},

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
