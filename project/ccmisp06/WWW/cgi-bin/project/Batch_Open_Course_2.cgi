#!/usr/local/bin/perl 
#################################################################################################
#####  複製上學年同學期開課資料
#####  依上一頁傳來的批次開課清單，複製上學年同學期課程到當年度。
#####  Updates:
#####    2015/04/21 從 Batch_Open_Course_1.cgi 複製改來 by Nidalap :D~

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Open_Course.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."Password.pm";

my(%Input,%Dept);

%Input=User_Input();
%Dept=Read_Dept($Input{dept_cd});
if( $Dept{id} eq $DEPT_LAN ) {							### 語言中心可開通識外語課
  if( $Input{grade} eq "cge_lan" ) {
    $cge_lan_flag = 2;									###  語言中心，且選擇了通識外語課
  }else{
    $cge_lan_flag = 1;							  		###  語言中心，尚未選擇通識外語課
  }  
}elsif( $Dept{id} eq $DEPT_CGE ) {						### 通識中心不可選通識外語課
  $cge_lan_flag = 3;
}

print "Content-type: text/html","\n\n";

#foreach $key (keys %Input) {
#  print("$key ---> $Input{$key}<br>");
#}

if( $cge_lan_flag == 2 ) {                                      ###  若是語言中心開通識外語課，讀取語言中心密碼檔 salt
  Check_Dept_Password($DEPT_LAN, $Input{password});
}else{                                                          ###  其餘一般情形：讀取該系所密碼檔 salt
  Check_Dept_Password($Input{open_dept}, $Input{password});
}
$su_flag = "(SU)"  if($SUPERUSER == 1);

if( $TERM == 3 ) {
  $show_term = "";
}else{
  $show_term = join("", "第", $TERM, "學期");
}

$grade_show = ($Input{grade} eq "cge_lan") ? "通識外語課" : $Input{grade};
print Print_Open_Course_Header(\%Input, \%Dept, "複製上學年同學期開課資料");


if( $cge_lan_flag == 2 ) {  ### 語言中心可開通識外語課
  $Dept{id}	  = $DEPT_CGE;
  $Input{grade} = 1;
}

$year_last = $YEAR - 1;

foreach $key (sort keys %Input) {								###  找尋上一頁傳來的批次開課清單
  if( $key =~ /^chk/ ) {
    ($temp, $cid, $grp) = split(/_/, $key);

	%Course = Read_Course($Dept{id},$cid,$grp,$year_last, $TERM);
	$Course{'dept'}				= $Dept{id};
	$Course{'open_dept'}		= $Input{'dept_cd'};
	$Course{'classroom'}		= "";						###  清空以下欄位
	$Course{'teacher'}			= ("");
	$Course{'time'}				= "";
	$Course{'s_match'}			= "";
	$Course{'number_limit'}		= "";
	$Course{'reserved_number'}	= "";
	#Print_Hash(%Course);
	
	%Course_test = Read_Course($Dept{id}, $cid, $grp, $YEAR, $TERM);	###  檢查是否已經開設（重複執行此頁）
	if( $Course_test{'credit'} eq "" ) {
	  Modify_Course("batch", %Course);
	  print "成功開設科目 $Course{'cname'} (代碼：$cid，班別：$grp)<BR>";
	}else{
	  print "<FONT color='RED'>無法開設 $Course{'cname'} (代碼：$cid，班別：$grp)，科目已存在！<BR>";
	}
  }
}


$Dept{id} = $DEPT_LAN  if( $cge_lan_flag == 2 );  ### 若是語言中心開通識外語課，還原系所代碼為語言中心
#Links3($Dept{id},$Input{grade},$Input{password});
Links1($Input{dept_cd},$Input{grade},$Input{password}, "", $Input{open_dept});
print "
   </center>
   </body>
  </html>
";