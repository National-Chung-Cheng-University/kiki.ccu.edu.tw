#!/usr/local/bin/perl 
#################################################################################################
#####  複製上學年同學期開課資料
#####  列出上學年同學期的開課資料供選擇。
#####  Updates:
#####   2015/04/21 從 Open_Course_1.cgi 複製改來 by Nidalap :D~
#####   2015/05/26 切換年級按鈕改由 Show_Switch_Grade_Buttons() 處理 Nidalap :D~

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Open_Course.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Password.pm";

my(%Input,%Dept);

%Input=User_Input();
%Dept=Read_Dept($Input{open_dept});
if( $Input{open_dept} eq $DEPT_LAN ) {					### 語言中心可開通識外語課
  if( $Input{dept_cd} eq $DEPT_CGE ) {
    $cge_lan_flag = 2;									###  語言中心，且選擇了通識外語課
  }else{
    $cge_lan_flag = 1;							  		###  語言中心，尚未選擇通識外語課
  }  
}elsif( $Input{open_dept} eq $DEPT_CGE ) {				### 通識中心不可選通識外語課
  $cge_lan_flag = 3;
}

print "Content-type: text/html","\n\n";

#foreach $key (keys %Input) {
#  print("$key ---> $Input{$key}<br>");
#}


Check_Dept_Password($Input{open_dept}, $Input{password});

$su_flag = "(SU)"  if($SUPERUSER == 1);

if( $TERM == 3 ) {
  $show_term = "暑修";
}else{
  $show_term = join("", "第", $TERM, "學期");
}

$grade_show = ($Input{grade} eq "cge_lan") ? "通識外語課" : $Input{grade};

print Print_Open_Course_Header(\%Input, \%Dept, "複製上學年同學期開課資料");				###  顯示上方系所年級等資訊
print Show_Switch_Grade_Buttons(\%Input, "Batch_Open_Course_1.cgi");						###  顯示切換年級按鈕

if( $cge_lan_flag == 2 ) {  ### 語言中心可開通識外語課
  $Dept{id}	  = $DEPT_CGE;
  #$Input{grade} = 1;
}

$year_last = $YEAR - 1;

  my(@course,%Course,@course_last, %Course_last);

  if( $cge_lan_flag == 2 ) {													######  語言中心可開通識外語課
 	$Dept{id}	  = $DEPT_CGE;
	#$Input{grade} = 1;
	@temp_course = Find_All_Course($DEPT_CGE,1,$year_last, $TERM);
	foreach $tc (@temp_course) {
	  push(@course_last, $tc)  if( $$tc{id} =~ /^7102.../ );					###  過濾只抓出通識外語課
	}
	@temp_course = Find_All_Course($DEPT_CGE,1);
	foreach $tc (@temp_course) {
	  push(@course, $tc)  if( $$tc{id} =~ /^7102.../ );
	}
  }elsif( $cge_lan_flag == 3 ) {												######  通識中心不可開通識外語課
    @temp_course = Find_All_Course($Input{dept_cd},$Input{grade},$year_last, $TERM);
    foreach $tc (@temp_course) {
      push(@course_last, $tc)  if( $$tc{id} !~ /^7102.../ );					###  過濾不可抓出通識外語課
    }
	@temp_course = Find_All_Course($Input{dept_cd},$Input{grade});
    foreach $tc (@temp_course) {
      push(@course, $tc)  if( $$tc{id} !~ /^7102.../ );
    }
  }else{																		######  一般情況：直接抓取開課資料
	@course_last = Find_All_Course($Input{'dept_cd'},$Input{grade},$year_last, $TERM);
    @course = Find_All_Course($Input{'dept_cd'},$Input{'grade'});
  }  

  foreach $cou (@course)  {		###  將本學期開課資料變成 %course，方便找尋
    $course{$$cou{'id'}}{$$cou{'group'}} = 1;
  }
  
  #####  顯示歷年開課資料的 TABLE HTML
  $table_html = "";
  foreach $cou_last (@course_last) {
    %Course_last = Read_Course($Input{dept_cd},$$cou_last{id},$$cou_last{group},$year_last, $TERM);
	
#	print "read course [$Input{dept_cd},$$cou_last{id},$$cou_last{group},$year_last, $TERM]<BR>\n";
	
	
	$input_name = "chk_" . $$cou_last{id} . "_" . $$cou_last{group};
	if( $course{$Course_last{"id"}}{$Course_last{"group"}} == 1 ) {
	  $status	= "已開";
	  $checked	= "DISABLED";
	  $bgcolor	= "LIGHTGRAY";
	}else{
	  $status = "未開";
	  $checked	= "CHECKED";
	  $bgcolor = "";
	}
	
    $table_html .= "
	  <TR bgcolor='$bgcolor'>
	    <TD><INPUT type='checkbox' name='$input_name' id='$input_name' $checked></TD>
		<TD>" . $Course_last{"id"} . "</TD>
		<TD>" . $Course_last{"group"} . "</TD>
		<TD>" . $Course_last{"cname"} . "</TD>
		<TD>" . $status . "</TD>
	  </TR>
	";
  }

print qq(
  <P>
  以下列出 $year_last 學年度 $show_term 開課資料：
  <FORM ACTION="Batch_Open_Course_2.cgi" method="POST">
    <input type=hidden name=dept_cd value=$Input{dept_cd}>
    <input type=hidden name=grade value=$Input{grade}>
    <input type=hidden name=password value=$Input{password}>
	<input type=hidden name=open_dept value=$Input{open_dept}>
  <table border=1>
    <tr>
      <th>選擇</th>
      <th>科目代碼</th>
	  <th>班別</th>
      <th>科目名稱</th>
	  <th>狀態</th>
    </tr>
    $table_html
  </TABLE>
  <INPUT type="SUBMIT" value="批次開設以上勾選之科目">
  </FORM>
);  


$Dept{id} = $DEPT_LAN  if( $cge_lan_flag == 2 );  ### 若是語言中心開通識外語課，還原系所代碼為語言中心
#Links3($Dept{id},$Input{grade},$Input{password});
Links1($Input{dept_cd},$Input{grade},$Input{password}, "", $Input{open_dept});
print "
   </center>
   </body>
  </html>
";