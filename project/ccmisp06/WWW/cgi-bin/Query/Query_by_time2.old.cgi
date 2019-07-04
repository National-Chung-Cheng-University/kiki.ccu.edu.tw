#!/usr/local/bin/perl
############################################################################################
#####  Query_by_time2.cgi
#####  以系所, 開課節次時間, 科目名稱, 教師姓名等條件, 搜尋當學期開課資料.
#####  Last Update:
#####   2004/03/02
#####   2008/06/03  新增科目名稱與教師姓名查詢選項.  Nidalap :D~
#####   2009/03/27  允許 "非法字元" 查詢, 將該字元跳脫查詢而非直接禁止. 
#####               所以可以查詢如 "許漢" 等教師開的課. 但是對 "功" 之類的字仍查不到
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

#Check_SU_Password($Input{password}, "dept", $Input{dept_cd});
%Input = User_Input();

print "input = ";
Print_Hash(%Input);

$file_path = $DATA_PATH . "Course_by_time/";
print qq(
  <HTML>
    <HEAD>
      <TITLE>進階開課資料查詢 -- 開課資料列表</TITLE>
      $EXPIRE_META_TAG
      <LINK rel="stylesheet" type="text/css" href="$HOME_URL/font.css">
    </HEAD>
  <body bgcolor=white background=$GRAPH_URL/ccu-sbg.jpg>
  <center>
    <SPAN class="title1">進階開課資料查詢</SPAN>
    <BR>
    <IMG src=$TITLE_LINE>
    <P class="illustration">
);


#Check_Input_Illigal($Input{course_cname});			###  檢查 course_cname 非法字元
#Check_Input_Illigal($Input{teacher});				###  檢查 teacher 非法字元

($illegal_flag, $course_cname)	= 
     Check_Input_Illigal($Input{course_cname});                      ###  檢查 course_cname 非法字元   
($illegal_flag, $teacher_cname)	=
     Check_Input_Illigal($Input{teacher});                           ###  檢查 teacher 非法字元
###  在此之後, $course_cname 和 $teacher_cname 用作比對用;
###  $Input{course_cname} 和 $Input{teacher} 用作顯示用.


@dept = split(/\*:::\*/, $Input{dept});

if( @dept == 0 ) {
  print("請至少選擇一個系所!");
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
  if( $Input{course_cname} ne "" ) {						###  如果有輸入科目名稱, 篩選之
    if( $cname !~ /$course_cname/ ) {
      next;
    }else{
      $cname =~ s/$course_cname/<FONT color=RED>$Input{course_cname}<\/FONT>/g;
    }
  }
  
  if( $Input{teacher} ne "" ) {							###  如果有輸入教師姓名, 篩選之
    if( $teacher !~ /$teacher_cname/ ) {
      next;
    }else{
      $teacher =~ s/$teacher_cname/<FONT color=RED>$Input{teacher}<\/FONT>/g;            
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
    $note = "無";
  }else{
    $note = "<A href=\"$CLASS_URL" . "ShowNote.cgi?&dept=" . $dept . "&course=" . $c_id . "&group=" . $c_grp . "\" target=NEW>有</A>";
  }
  $content .= "<TR align=CENTER $high_light><TD>$dept_cname2</TD><TD>$grade</TD><TD>$c_id</TD><TD>$c_grp</TD><TD align=LEFT>$cname</TD><TD>$total_time{$course}</TD>";
  $content .= "<TD>$time_string</TD><TD>$teacher</TD><TD>$classroom</TD><TD>$number_limit</TD><TD>$note</TD></TR>";
#  $content .= "<TR><TD rowspan=2>$dept_cname2</TD><TD rowspan=2>$c_id</TD><TD rowspan=2>$c_grp</TD><TD colspan=5>$cname</TD></TR>";
#  $content .= "<TD>$total_time{$course}</TD><TD>$time_string</TD><TD>$classroom</TD><TD>$number_limit</TD></TR>";

  $hits ++;
  $last_dept = $dept;
#  print("$course, $count{$course}, $total_time{$course}<BR>\n");
}


$Input{course_cname} = "(無限制)"	if($Input{course_cname} eq "");
$Input{teacher} = "(無限制)"		if($Input{teacher} eq "");

print qq(
    <SPAN class="font1">
      <CENTER>
      您的查詢條件是: 
      <TABLE border=1>
        <TR><TD>科目名稱: </TD><TD>$Input{course_cname}</TD></TR>
        <TR><TD>教師姓名: </TD><TD>$Input{teacher}</TD></TR>
      </TABLE>
      共有 $hits 筆開課資料符合條件
    <form name=form1 method=post action=Query_by_time2.cgi>
      <input type=hidden name=dept value=$Input{dept}>
      <input type=hidden name=password value=$Input{password}>
      <TABLE border=1 class=font1 width=800>
        <TR>
          <TH>開課系所</TH><TH>年級</TH><TH>科目代碼</TH><TH>班別</TH><TH>科目名稱</TH>
          <TH>時數</TH><TH>上課時間</TH>
          <TH>授課教師</TH><TH>上課教室</TH><TH>限修<BR>人數</TH><TH>其他<BR>限制</TH>
        </TR>
        $content
        </TR>
      </TABLE>
    <p>
  </body>
  </html>
);
 
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