1;

############################################################################
#####  Common_Utility.pm
#####  一些一般性的函式
#####  Last Update:
#####   2002/03/14 建立此模組 (Nidalap :D~)
############################################################################
############################################################################
#####  Numeric_to_chars
#####  把數字轉化為數個字元傳回陣列
#####  可用在限修人數, 分為 "百 十 個" 供選擇
#####  傳回的陣列中 $char[0]為個位數, $char[1]為十位數, 以此類推
############################################################################
sub Numeric_to_chars
{
  my($num, @char, $i);
  ($num) = @_;
  $i = 0;
  do {
    $char[$i++] = chop($num);
  } while($num ne "");
  return(@char);  
}
############################################################################
#####  is_Time_Collision
#####  兩個時段是否有衝堂情形發生
#####  因為加入了 50/75 分鐘並行制, 衝堂不能單純以時間相同來判斷,
#####  此函式判斷兩個時段是否衝堂.
#####  需求 : 要 require Reference.pm
#####  Input: ($day1, $time1, $day2, $time2)
#####  Output [0,1,2] = [不衝堂, 完全衝堂, 部分衝堂]
#####  Last Update:
#####    2002/03/15 建立函式(Nidalap :D~)
############################################################################
sub is_Time_Collision
{
  my($d1,$t1,$d2,$t2) = @_;
  my($region1, $region2, $i, $place1, $place2);
  
  if($d1 == $d2) {                        #####  如果在同一天(衝堂必要條件)
    return(1)  if($t1 eq $t2);              ###  如果在同一截次(剛好衝)
    return(0)  if( ($t1>0) and ($t2>0) );   ###  兩個都是數字截次 -> 不衝堂
    return(0)  if( ($t1==0) and ($t2==0) ); ###  兩個都是英文截次 -> 不衝堂
    $region1 = $REGION_TIME_TABLE{$t1};
    $region2 = $REGION_TIME_TABLE{$t2};
    if($region1 == $region2) {              ###  同區段, 要再檢查...
      for($i=0; $i<5; $i++) {
        $place1=$i  if($TIME_REGION_TABLE[$region1][$i] eq $t1);
        $place2=$i  if($TIME_REGION_TABLE[$region1][$i] eq $t2);
      }
      if( abs($place1 - $place2) == 1 ) {   ###  在 @TIME_REGION_TABLE 中相鄰 
        return(2);                          ###  則是 50 和 75 分鐘的衝堂
      }else{
        return(0);
      }
    }else{                                  ###  不同區段, 不衝堂
      return(0);
    }
  }else{                                  #####  不同天 = 不衝堂
    return(0);
  }
}
#############################################################################
#####  Format_Time_String
#####  將選課節次時間資料, 轉為單一可閱讀字串(ex: 一6三5,6)
#####  20130808  新增英文版顯示 Nidalap :D~
sub Format_Time_String
{
  my($rtime) = @_;
  my $time_string = "", $last_day = "";
  my @weekday;
  
  if( $IS_ENGLISH ) {
    @weekday = @WEEKDAY_E;
  }else{
    @weekday = @WEEKDAY;
  }
  foreach $ele ( @{$rtime} ) {
    if( $$ele{week} ne $last_day ) {
      $time_string .= " " . $weekday[$$ele{week}];
    }else{
      $time_string .= ",";
    }
    $time_string .= $$ele{time};
    $last_day = $$ele{week};
  }
  return($time_string);
}
##############################################################################
#####  Last_Semester
#####  傳回上 n 個學期的學年學期值
#####  Updates:
#####    2007/06/05 Created by Nidalap :D~
#####    2009/12/29 可輸入參數 $n，用來傳回上 n 個學期的學年學期  Nidalap :D~
sub Last_Semester
{
  my($n) = @_;
  my($year, $term, $i);

  $year = $YEAR; $term = $TERM;
  for($i=0; $i<$n; $i++) {
    $term--;
    if( $term == 0 ) {
      $year--;
      $term = 2;
    }
  }

  return ($year, $term);
}

##############################################################################
#####  Check_HTTP_REFERER
#####  從外部系統連過來的, 檢查哪些來源是安全的
#####  目前可能連過來的系統:
#####    學籍, 英檢, 教專
#####  Nidalap 2008/01/18  :D~
sub Check_HTTP_REFERER
{
  my $referer = $ENV{HTTP_REFERER};
  my $check_succeed_flag = 0;

  my $script_name = 'tea_tutor_std.php';
  my @allowed_referers = (
    'http://mis.cc.ccu.edu.tw/~paccount01/lsg/',
    'http://mis.cc.ccu.edu.tw/profession/',
    'http://mis.cc.ccu.edu.tw/~paccount01/profession/'
  );

  foreach $ip (@allowed_referers) {
    $check_succeed_flag = 1  if($referer =~ /$ip/);
#    print("$referer <-> $ip: $check_succeed_flag<BR>\n");
  }

#  return($check_succeed_flag);
  return(1);
  
}
##############################################################################
#####  Online_Help()
#####  產生線上說明的 javascript code
#####  2008/05/23, Nidalap :D~
sub Online_Help
{
  my $help = qq(
    <SCRIPT language="javascript">
      function OnlineHelp(anchor)
      {
         var link= "../../online_help.html#" + anchor;
         window.open(link, 'ExplainWindow', 'resizable=yes, width=450,height=400, scrollbars=yes, resizable=yes');
      }
    </SCRIPT>
  );
  return($help);
}
##############################################################################
#####  Show_Online_Help
#####  產生前往線上說明 javascript 的連結
#####  2008/05/23, Nidalap :D~
sub Show_Online_Help
{
  my($anchor) = @_;
  my($show);
    
  $show = "<A href=\"javascript:OnlineHelp('$anchor')\"><FONT color=BLUE>[?]</FONT></A>";
  return($show);
}
##############################################################################
#####  Read_Special_Announce
#####  讀取特定公告內容
#####  2008/05/26, Nidalap :D~
sub Read_Special_Announce
{
  my($type) = @_;
  
  my(@announce, $announce, $announce_file, $title);
  my %announce_map =  (
    "lang_msg"		=> "lang_msg.txt",
    "physical_msg"	=> "physical_msg.txt",
    "military_msg"	=> "military_msg.txt",
    "edu_msg"		=> "edu_msg.txt",
    "prerequisite_msg"	=> "prerequisite_msg.txt",
    "cge_msg"		=> "cge_msg.txt",
	"not_supported"	=> "not_supported.txt",
	"classroom_msg"	=> "classroom_msg.txt"
  );
  
  $announce_file = $REFERENCE_PATH . $announce_map{$type};
  open(SPECIAL_ANNOUNCE, $announce_file);
  $title = <SPECIAL_ANNOUNCE>;
  @announce = <SPECIAL_ANNOUNCE>;
  close(SPECIAL_ANNOUNCE);
    
  foreach $line (@announce) {
    $line =~ s/\n/<BR>\n/;
    $announce .= $line;
  }
  return($title, $announce);
}
##############################################################################
#####  Print_Hash
#####  在螢幕上印出一個 hash 的值 (debug 用) 
sub Print_Hash
{
  my %hash = @_;
  use Data::Dumper;

  print Dumper(%hash);
}
#############################################################################
#####  Compare_Dates()
#####  將 "yyyy/mm/dd" 字串型態的兩個日期做比較
#####  輸入：[$date1, $date2] = [日期1, 日期二]
#####  輸出：[1,0,-1] = [前者大，兩者相等，後者大]
sub Compare_Dates
{
  my ($date1, $date2) = @_;
  my ($y1, $m1, $d1, $y2, $m2, $d2);
  
  ($y1, $m1, $d1) = split(/\//,$date1);
  ($y2, $m2, $d2) = split(/\//,$date2);
  
  if( $y1 > $y2 ) {		return 1;
  }elsif( $y1 < $y2 ){		return -1;
  }else{
    if( $m1 > $m2 ){		return 1;
    }elsif( $m1 < $m2 ){	return -1;
    }else{
      if( $d1 > $d2 ){		return 1;
      }elsif( $d1 < $d2){	return -1;
      }else{		return 0;  }
    }
  }
}
#############################################################################
#####  Apply_Form_Allowed
#####  目前時間是否可申請加簽/棄選單
#####  依照系統設定的加簽/棄選開始、截止日期，以及目前時間判斷
#####  傳入值：($form_type) = 加簽/棄選單
#####  傳回值：($allow, $msg) = (可否申請, 錯誤訊息)
#####  2011/07/29 Nidalap :D~
#####  2013/04/15 將原先的 Concent_Form_Allowed() 改為 Apply_Form_Allowed，可接受「加簽」、「棄選」兩種判斷。 Nidalap :D~
sub Apply_Form_Allowed
{    
  my($form_type) = @_;            
  my $start_hour   = 12;           ###  開放日幾點開始才算開放
  my $end_hour     = 17;           ###  截止日幾點開始才算截止
                         
  %time = gettime();
  my %ss = %system_flags;

  ###  依據傳入參數判斷要抓取加簽還是棄選的開始/結束日期設定
  $start_date	= $ss{$form_type . "_form_start"};
  $end_date		= $ss{$form_type . "_form_end"};

#  print "ss = ";  
#  Print_Hash(%ss);
#  print "now = $time{time_string4} <-> $ss{concent_form_start}<BR>\n";
#  print "start = " . $start_date . "; end = " . $end_date . "<BR>\n";

  if( Compare_Dates($time{time_string4}, $start_date) == -1 ) {
    return(0,"尚未開放申請");             ###  現在 < 開放時間
  }elsif( Compare_Dates($time{time_string4}, $start_date) == 0 ){
    if( $time{hour} < $start_hour ) {
      return(0,"尚未開放申請");
    }else{
      return(1,"");
    }
  }elsif( Compare_Dates($time{time_string4}, $end_date) == -1 ){
    return(1,"");                         ###  開放時間 < 現在 < 關閉時間：  開放
  }elsif( Compare_Dates($time{time_string4}, $end_date) == 1 ){
    return(0,"申請已截止");               ###  關閉時間 < 現在： 已截止
  }else{                         	  ###  現在 = 關閉日期：             判斷時間
    if( $time{hour} < $end_hour ) {
      return(1,"");
    }else{
      return(0,"申請已截止"); 
    }
  }
}


######################################################################
#####  檢核特殊字元, 在前面加上 back-slash, 以避免 SQL injection 攻擊
#####  目前只有作到 addslashes，且不能接受陣列輸入。
#####  2013/12/12 從 PHP 版本改過來 Nidalap :D~ 
#####  2016/05/13 多加幾道防護上去，並且加入 advanced_mode  Nidalap :D~
sub quotes
{
  my ($content, $advanced_mode) = @_;
  #my $advanced_mode = 0; 

  use CGI;
  if( $advanced_mode == 1 ) {
    #$content = strip_tags(CGI::escapeHTML(addslashes($content)));
	$content =~ s/\\//g;								###  相當於 stripslashes()
	$content = CGI::escapeHTML($content);
	$content =~ s/<\S[^<>]*(?:>|$)//gs;					###  相當於 PHP 的 strip_tags()
  }else{
     $content = addslashes($content);
  }
  return $content;
}
######################################################################

######################################################################
sub addslashes {
    $text = shift;
    ## Make sure to do the backslash first!
    $text =~ s/\\/\\\\/g;
    $text =~ s/'/\\'/g;
    $text =~ s/"/\\"/g;
    $text =~ s/\\0/\\\\0/g;
    return $text;
}


##############################################################################
#####  檢查特定資料是否合法，以補 quotes() 之不足。本身即包含 quotes()。
#####  輸入：[要驗證的資料，它應該是哪種類型，檢查失敗時顯示的欄位名稱，額外參數1(依類型定義), 額外參數2(依類型定義)]
#####  2016/03/02 從 Common_Utility.php 中複製改來（尚未完成！） by Nidalap :D~
sub Verify_Specific_Data
{
    #my($data, $type="text", $data_name, $param1=NULL, $param2=NULL) = @_;
	my($data, $type, $data_name, $param1, $param2) = @_;
	my $data = quotes($data, 1);
	my $pass = 0;
	my $data_len;
	
	if( !$type )  { $type = "text";	 }

	SWITCH: { 
	  if( $type eq "int" ) {										###  一般數字：$param1 是長度(位數)，$param2 若為 1 則可允許負號
	    if( $data =~ /^[-\d]\d*$/ ) {
		  $data_len = length($data);
		  if( $param2 ) {
		    if( substr($data, 0, 1) == "-" ) {
			  $data_len = $data_len - 1;
			}else{
			  $pass = 0;
			  last SWITCH;
			}
		  }
		  if( $param1 ) {
			if( $data_len == $param1 )  { $pass = 1; }
		  }else{
		    $pass = 1;
		  }		  
#		}else{
#		  print "$data does not pass INT check!<BR>\n";
		}
		
	  }elsif( $type eq "year ") {										###  學年度
	    if( is_numeric($data) and ((length($data)==2) or (length($data)==3)) )  { $pass = 1; }
	  }elsif( $type eq "term ") {										###  學期
	    if( is_numeric($data) and ($data>=1) and ($data<=3) ) 					{ $pass = 1; }
	  }elsif( $type eq "deptcd") {										###  系所代碼
		if( length($data) == 4 )			{ $pass = 1; }
	  }elsif( $type eq "college") {										###  學院代碼。$param1 若為 1，代表允許 0 代表全校
	    if( ($data>=1) and ($data<=7) )     { $pass = 1; }
		if( ($param1==1) and ($data==0) )	{ $pass = 1; }
	  }elsif( $type eq "student_id") {									###  學號
	    if( length($data) == 9 ) {
		  if( $data =~ /^[45689]\n[8]$/ )	{ $pass = 1; }
		}
	  }elsif( $type eq "person_id") {									###  身份證號(檢查正確後，順手將英文部分轉大寫)
	    if( length($data) == 10 ) {
		  if( $data =~ /^[0-9a-zA-Z]{10}$/ )  {
			$pass = 1;
			$data = uc($data);
		  }
		}
	  }elsif( $type eq "course_id") {									###  科目代碼
	    if( length($data) == 7 ) {
		  if( $data =~ /^[1-9][0-9A]{6}$/ )	{ $pass = 1; }
		}
#	  }elsif( $type eq "password_crypt") {								###  密碼(經過 crypt 函式編碼後)
#	    if( length($data) == 13 ) {
#		  if( $data =~ /^[0-9a-zA-Z\.\/]{13}$/ )  {
#			$pass = 1;
#		  }
#		}
	  }else{															###  若無指定（一般文字），$param1 為最大 byte 數
		if( ($param1 eq "") or (length($data) <= $param1) )	{  $pass = 1;  }
	  }
	}
    if( $pass == 0 ) {
	  Error("$data_name 欄位不可為： " .  $data);
	  print $SYS{"HTML_META_TAG"};
	  print "錯誤：欄位 $type 不可為 $data";
	  die();
	}else{
	  return $data;
    }
}
#############################################################################################
#####  針對 %Input 做資料消毒（透過 Verify_Specific_Data() 函式）
#####  Added 2016/05/10 by Nidalap :D~
sub Sanitize_Input
{
  my %i = @_;			###  %Input
 
#  print "last_semester = " . $i{'last_semester'} . "<BR>\n";
  
  $i{'dept_cd'}			= Verify_Specific_Data($i{'dept_cd'}, "deptcd")			if exists($i{'dept_cd'});
  $i{'open_dept'}		= Verify_Specific_Data($i{'open_dept'}, "deptcd")		if exists($i{'open_dept'}) and $i{'open_dept'}!="";
  $i{'login_dept_id'}	= Verify_Specific_Data($i{'login_dept_id'}, "deptcd")	if exists($i{'login_dept_id'});
  $i{'last_semester'}	= Verify_Specific_Data($i{'last_semester'}, "int", 2)	if exists($i{'last_semester'});
  $i{'year'}			= Verify_Specific_Data($i{'year'}, "int", 2)			if exists($i{'year'});
  $i{'term'}			= Verify_Specific_Data($i{'term'}, "int", 1)			if exists($i{'term'});
  $i{'dept_name'}		= Verify_Specific_Data($i{'dept_name'}, "text", 20)		if exists($i{'dept_name'});
  $i{'password'}		= Verify_Specific_Data($i{'password'}, "password")		if exists($i{'password'});
  $i{'password_crypt'}	= Verify_Specific_Data($i{'password_crypt'}, "text", 13)if exists($i{'password_crypt'});
  $i{'teacher_id'}		= Verify_Specific_Data($i{'teacher_id'}, "person_id")	if exists($i{'teacher_id'});
  $i{'teacher_cname'}	= Verify_Specific_Data($i{'teacher_cname'}, "text", 10)	if exists($i{'teacher_cname'});
  $i{'course_cname'}	= Verify_Specific_Data($i{'course_cname'},"text",20)	if exists($i{'course_cname'});
  $i{'dept_multi'}		= Verify_Specific_Data($i{'dept_multi'},"text",300)		if exists($i{'dept_multi'});
  $i{'session_id'}		= Verify_Specific_Data($i{'session_id'},"text",40)		if exists($i{'session_id'});
#  $i{''}	= Verify_Specific_Data($i{''})	if exists($i{''});
#  $i{''}	= Verify_Specific_Data($i{''})	if exists($i{''});
#  $i{''}	= Verify_Specific_Data($i{''})	if exists($i{''});
#  $i{''}	= Verify_Specific_Data($i{''})	if exists($i{''});
#  $i{''}	= Verify_Specific_Data($i{''})	if exists($i{''});
 
  return %i;
}
