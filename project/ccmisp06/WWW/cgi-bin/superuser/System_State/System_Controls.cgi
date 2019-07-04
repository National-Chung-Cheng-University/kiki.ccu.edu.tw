#!/usr/local/bin/perl
print("Content-type:text/html\n\n");

#############################################################################
#####  System_Controls.cgi 
#####  選課系統相關設定
#####  整合選課系統的一些限制開關設定
#####  Coder: Nidalap :D~
#####   Date: 2002/06/06
#####         2011/07/28  新增 Show_Date_Selection() by Nidalap :D~
#####         2014/06/23  隱藏部份只有一般生正式非暑修、測試系統會需要看到的選項 by Nidalap :D~
#############################################################################
require "../../library/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Common_Utility.pm";
require $LIBRARY_PATH . "Password.pm";
require $LIBRARY_PATH . "System_Settings.pm";
require $LIBRARY_PATH . "Error_Message.pm";

print $EXPIRE_META_TAG;

my(%Input);
%Input=User_Input();

$crypt_salt = "aa";
#print("password = $Input{password}<BR>\n");
#$password = Crypt($Input{password},$crypt_salt);
$password = $Input{password};
$pass_result = Check_SU_Password($password, "su", "su");

#print("password = $password<BR>\n");
#print("result = $pass_result");

ERR_HTML()  if( $pass_result ne "TRUE" );

@{$option{cge_ban_grade}}		= ("不限制", "不開放大四", "不開放大三大四");
@{$option{allow_print_student_course}}	= ("不開放列印", "開放列印");
@{$option{show_last_total}}		= ("不顯示篩選後餘額欄位", "顯示篩選後餘額欄位");
@{$option{show_immune_count}}		= ("不顯示可加選名額欄位", "顯示可加選名額欄位");
@{$option{allow_query_last_select_namelist}} = ("不可查詢上次篩選後名單", "可查詢上次篩選後名單");
@{$option{no_ban}}			= ("允許\限本系擋修", "限本系擋修設定無效");
@{$option{allow_select_math}}		= ("開放加選數學系所及其他系課程","只開放加選非數學系所課程","只開放加選數學系所課程");
@{$option{allow_print_pdf}}		= ("不開放列印", "開放列印");
@{$option{allow_print_graduate_pdf}}	= ("不開放列印", "開放列印");
@{$option{force_print_graduate_pdf}}	= ("不要求確認", "要求確認");
@{$option{redirect_to_query}}		= ("本系統上線中", "請使用者連線至查詢系統");
@{$option{black_list}}			= ("關閉黑名單功\能", "開啟黑名單功\能");
@{$option{grade_upgrade}}		= ("註冊次數不升級", "註冊次數升級");
@{$option{current_system_timeline}}	= ("第一階段選課前", "第一階段選課期間", "科目異動前", "科目異動期間", 
                                       "第二階段選課前", "第二階段選課期間", "第二階段選課結束");
@{$option{allow_english}} = ("否", "是");
@{$option{allow_mobile}} = ("否", "是");
@{$option{questionnaire2013}} = ("否", "是", "強迫必填");
@{$option{delayed_del}} = ("否", "是(請務必手動開啟crontab排程執行批次退選！)");

if( $Input{modify_flag} == 1 ) {
  Write_System_Settings(%Input);
}

%flags = Read_System_Settings();
Show_Page();
#############################################################################
sub Show_Page()
{
  print qq (
    <HTML>
      <HEAD>
        <TITLE>選課系統相關設定</TITLE>
        <link rel="stylesheet" href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.14/themes/base/jquery-ui.css" type="text/css" media="all" />
	<link rel="stylesheet" href="http://static.jquery.com/ui/css/demo-docs-theme/ui.theme.css" type="text/css" media="all" />
      </HEAD>
      <BODY background="$GRAPH_URL/ccu-sbg.jpg">
      <CENTER>
      <H1>選課系統相關設定</H1>
      <HR>
      <FORM action="System_Controls.cgi" method=POST>
        <INPUT type=hidden name="password" value="$password">
	  <TABLE border=1>
        <TR>
          <TH>設定名稱</TH>
          <TH>設定說明</TH>
          <TH>設定</TH>
        </TR>
  );
#  Show_Selection("cge_ban_grade", "通識中心課程不開放大四選修",
#                 "通識中心課程不開放大三大四學生修課.
#                  由於通識中心政策, 第一階段不開放大三大四生修課.");
  
  Show_Selection("allow_print_student_course", "開放列印選課單",
                 "只有在第二階段選課後才列印選課單的功\能,
                  本設定決定該功\能是否開放.");
  Show_Selection("allow_print_pdf", "開放列印選課確認pdf檔",
                 "加退選結束後由教學組產生選課結果確認單(pdf檔), 
                  交由電算中心執行檔案分配程式後方可開放.");

  Show_Selection("allow_print_graduate_pdf", "開放列印畢業資格審查pdf檔",
                 "教學組不定期更新畢業資格審核pdf檔, 
                  交由電算中心執行檔案分配程式後方可開放.")
  if( ($IS_MAIN_SYSTEM!=0) and !$IS_GRA );		###  只有一般生正式非暑修非專班、測試系統會顯示

  Show_Selection("force_print_graduate_pdf", "要求確認畢業資格審查pdf檔",
                 "對於有畢業資格審查檔的同學, 強制要先確認該資料後才能選課.
                  若開啟此選項, 上一個選項也必須開啟.")
  if( ($IS_MAIN_SYSTEM!=0) and !$IS_GRA );		###  只有一般生正式非暑修非專班、測試系統會顯示

  Show_Selection("show_last_total", "是否顯示上次篩選後餘額",
                 "在第二階段的多次篩選過程中,
                  顯示此資料可避免學生選一些不太可能選上的課.
                  此欄位將顯示在加選時的科目選單中")
  if( ($IS_MAIN_SYSTEM!=0) and !$IS_GRA );		###  只有一般生正式非暑修非專班、測試系統會顯示
  
  Show_Selection("show_immune_count", "是否顯示可加選名額人數",
                 "在先選先贏的時段中, 顯示此欄位,
                 可加選名額 = (限修人數) + (已加選的加簽人數) - (目前所有選修人數)
                 此欄位將顯示在加選時的科目選單中")
  if( ($IS_MAIN_SYSTEM!=0) and !$IS_GRA );		###  只有一般生正式非暑修非專班、測試系統會顯示

  Show_Selection("allow_query_last_select_namelist", "是否可以查詢上次篩選後名單",
                 "(教師)查詢選課名單功\能中, 
                 是否出現可查詢 \"上次篩選後名單\" 選項")
  if( ($IS_MAIN_SYSTEM!=0) and !$IS_GRA );		###  只有一般生正式非暑修非專班、測試系統會顯示
  
  Show_Selection("no_ban", "是否允許\限本系擋修",
                 "(第二階段選課時)若設定為限本系擋修無效,
                 所有超過十個科目的擋修設定(視同為限本系)將不作用(通識與軍訓課程不在此限)")
  if( ($IS_MAIN_SYSTEM!=0) and !$IS_GRA );		###  只有一般生正式非暑修非專班、測試系統會顯示

#  Show_Selection("allow_select_math", "是否開放加選數學系所開設之課程",
#                 "第一階段選課時, 數學系所的課程採先選先贏額滿為止, 
#                 系統獨立某一天專門選修數學系所開設的課程, 故有此選項");

  Show_Selection("redirect_to_query", "是否請使用者連線至查詢系統",
                 "系統準備下學期開課期間, 會把本學期資料清空放歷史區,
                 此時系統會顯示「上學期功課表」等選項供查詢。");
  Show_Selection("black_list", "是否開啟黑名單功\能",
                 "加選次數太過分的黑名單. 若是開啟此功\能, 
                 黑名單中的學生會在主選單看到警告訊息. 若關閉此功\能,
                 系統仍會紀錄 log, 只是不會顯示警訊.");
  Show_Selection("grade_upgrade", "是否開啟學生註冊次數升級",
		 "只有在第一階段選課開啟，目的在使學生註冊次數加一，以便判斷下學期的年級。
		 (學生年級是依據註冊次數以及此處設定兩者一起判別)");
  Show_Selection("current_system_timeline", "目前系統時間點",
                 "設定目前系統的時間點，作為某些頁面參考(比如說科目異動了沒)");
  Show_Date_Selection("concent_form_start", "開放申請加簽單日期", 
                 "此日期以後，到截止日期前，方可線上申請加簽單");
  Show_Date_Selection("concent_form_accept", "開放受理加簽單日期",
                   "此日期以後，到截止日期前，教學組才會受理加簽單");
  Show_Date_Selection("concent_form_end", "截止申請加簽單日期",
                 "開放申請加簽單日起，到此日期前，方可申請加簽單");

  Show_Separation_Line();
  Show_Date_Selection("withdrawal_form_start", "開放申請棄選單日期", 
                 "此日期以後，到截止日期前，方可線上申請棄選單");
  Show_Date_Selection("withdrawal_form_accept", "開放受理棄選單日期",
                   "此日期以後，到截止日期前，教學組才會受理棄選單");
  Show_Date_Selection("withdrawal_form_end", "截止申請棄選單日期",
                 "開放申請棄選單日起，到此日期前，方可申請棄選單");
				 
  Show_Input("restrict_stdno", "限制可選課學號", 
             "在此輸入學號第二～三碼數字，以限制只有此學號學生可選課。
              (ex:輸入 00 則只有 400, 600, 800, 500 可選課, 測試帳號不在此限).
              可在上學期新生第一階段選課時開啟，將此欄位填空以取消此功\能.
              轉學生不在此限，仍可選課。"
              );
  Show_Input("restrict_stdno2", "限制「不可」選課學號", 
             "在此輸入學號第二～三碼數字，以限制此學號學生「不可」選課。
			  學生需同時滿足註冊次數為 0 之條件（註冊次數加一以後為1）。
			 <BR>
              (ex:輸入 00 則只有 400, 600, 800, 500 可選課, 測試帳號不在此限).
              可在上學期舊生第一階段選課時開啟，以避免尚未入學的新生進來選課，
			  之後將此欄位填空以取消此功\能。"
              );
  Show_Selection("allow_english", "是否開啟選課英文版本選項",
		 "若開啟「是」，選課登入畫面會出現英文選項。若否則不會出現");
  Show_Selection("allow_mobile", "是否自動開啟行動版本選項",
		 "若開啟「是」，選課登入畫面會出現行動版本選項，
		 且使用行動裝置時畫面會預設使用行動版本。若否則不會主動出現。");
  Show_Selection("delayed_del", "先搶先贏期間是否開啟退選餘額延後釋出",
		 "若開啟「是」，且系統目前時程設定為第二階段選課期間，則退選餘額會延後釋出。
		 請務必手動設定並確認排程 crontab，以確保系統定時執行批次退選！"); 
#  Show_Selection("questionnaire2013", "是否開放填寫(2013)中正大學選課系統暨通識篩選原則意見調查表",
#		 "只有舊生會看到此選項，若開啟「強迫必填」，系統會要求舊生先填寫此問卷，然後才能選課。");
  
  $check = Check_Date_Constrictions();
  
  print qq(
      </TABLE>
      <P>
        <FONT color="RED">$check</FONT><P>
        <INPUT type=hidden name=modify_flag value=1>
        <INPUT type=submit>
      </FORM>
    </BODY>
  );
  Check_Date_Constrictions();
  Print_Javascript();
}

#####################################################################
sub Check_Date_Constrictions
{
  my @date_types = ("concent_form", "withdrawal_form");
  my $cmp1, $cmp2;
  
  foreach $date_type ( @date_types ) {
    $date_start = $date_type . "_start";
	$date_accept = $date_type . "_accept";
	$date_end = $date_type . "_end";
	#print "compare : " . $date_start . ", " . $date_accept . ", " . $date_end . "...<BR>\n";
	#print "compare : " . $flags{$date_start} . ", " . $flags{$date_accept} . ", " . $flags{$date_end} . "...<BR>\n";
	$cmp1 = Compare_Dates($flags{$date_start}, $flags{$date_accept});
	$cmp2 = Compare_Dates($flags{$date_accept}, $flags{$date_end});
	if( $cmp1 != -1 ) {
	  return("錯誤！開放申請日期必須早於受理申請日期");
	}elsif( $cmp2 != -1 ) {
	  return("錯誤！受理申請日期必須早於結束申請日期");
	}	
  }
  return("");
}
#####################################################################
sub Show_Input
{
  my($input, $name, $descriptions) = @_;
  
  print qq(
    <TR>
      <TD>$name</TD>
      <TD><FONT color=GREEN size=2>$descriptions</TD>
      <TD><INPUT name=$input value='$flags{$input}'></TD>
    </TR>
  );  
}
#####################################################################
sub Show_Selection
{
  my($selection, $name, $descriptions) = @_;
  my(@option, $i, $option_count);
  
  @option = @{$option{$selection}};
  
  print qq(
    <TR>
      <TD>$name</TD>
      <TD><FONT color=GREEN size=2>$descriptions</TD>
      <TD>
        <SELECT name="$selection">
  );
  $option_count = @option;
  for( $i=0; $i<$option_count; $i++ ) {
    if( $i eq $flags{$selection} ) {
      print("<OPTION value=$i SELECTED>$option[$i]\n");
    }else{
      print("<OPTION value=$i        >$option[$i]\n");
    }
  }
  print qq(
        </SELECT>
      </TD>
    </TR>
  );
}
######################################################################
sub Show_Date_Selection()
{
  my($selection, $name, $descriptions) = @_;
  
  print qq(
    <TR>
      <TD>$name</TD>
      <TD><FONT color=GREEN size=2>$descriptions</FONT></TD>
      <TD>
        <INPUT name="$selection" value="$flags{$selection}" class="SelectDate">
      </TD>
    </TR>
    
  );
}
######################################################################
sub Show_Separation_Line()
{
  print qq(
    <TR><TD colspan=3><HR></TD></TR>
  );
}
######################################################################
sub Print_Javascript
{
  print qq(
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js"></script>
    <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.9/jquery-ui.min.js"></script>
    <script type="text/javascript">
       \$(function() {
	  \$.datepicker.regional['zh-TW'] = {
		clearText: '清除', clearStatus: '清除已選日期',
		closeText: '關閉', closeStatus: '不改變目前的選擇',
		prevText: '&lt;上月', prevStatus: '顯示上月',
		nextText: '下月&gt;', nextStatus: '顯示下月',
		currentText: '今天', currentStatus: '顯示本月',
		monthNames:['一\月','二月','三月','四月','五月','六月',
			'七月','八月','九月','十月','十一月','十二月'],
		monthNamesShort: ['一\','二','三','四','五','六',
			'七','八','九','十','十一\','十二'],
		monthStatus: '選擇月份', yearStatus: '選擇年份',
		weekHeader: '周', weekStatus: '年內周次',
		dayNames:['星期日','星期一\','星期二','星期三','星期四','星期五','星期六'],
		dayNamesShort:['週日','週一\','週二','週三','週四','週五','週六'],
		dayNamesMin: ['日','一\','二','三','四','五','六'],
		dayStatus: '設定 DD 為一周起始', dateStatus: '選擇 m月 d日, DD',
		dateFormat: 'yy/mm/dd', firstDay: 1, 
		initStatus: '請選擇日期', isRTL: false
		};
	  \$.datepicker.setDefaults(\$.datepicker.regional['zh-TW']);
	  \$(".SelectDate").datepicker();
        });
    </script>

  );

}

##########################################################################
sub ERR_HTML()
{
  print qq(
   <body background=$GRAPH_URL"."ccu-sbg.jpg>
    <center>
    <H1>開排選課管理系統<hr></H1>
    您輸入的密碼有誤, 請重新輸入!<br>
    <FORM>
    <input type=button onclick=history.back() value="回上一頁">
    </FORM>
       
 
  );
  exit(1);
}