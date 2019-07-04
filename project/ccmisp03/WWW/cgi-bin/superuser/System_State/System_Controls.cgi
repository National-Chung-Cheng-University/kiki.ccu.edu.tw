#!/usr/local/bin/perl
print("Content-type:text/html\n\n");
#############################################################################
#####  System_Controls.cgi 
#####  選課系統相關設定
#####  整合選課系統的一些限制開關設定
#####  Coder: Nidalap :D~
#####   Date: 2002/06/06
#############################################################################
require "../../library/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "System_Settings.pm";

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

%Input = User_Input();

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
      <HEAD><TITLE>選課系統相關設定</TITLE></HEAD>
      <BODY background="$GRAPH_URL/ccu-sbg.jpg">
      <CENTER>
      <H1>選課系統相關設定</H1>
      <HR>
      <FORM action="System_Controls.cgi" method=POST>
      <TABLE border=1>
        <TR>
          <TH>設定名稱</TH>
          <TH>設定說明</TH>
          <TH>設定</TH>
        </TR>
  );
  Show_Selection("cge_ban_grade", "通識中心課程不開放大四選修",
                 "通識中心課程不開放大三大四學生修課.
                  由於通識中心政策, 第一階段不開放大三大四生修課.");
  
  Show_Selection("allow_print_student_course", "開放列印選課單",
                 "只有在第二階段選課後才列印選課單的功\能,
                  本設定決定該功\能是否開放.");
  Show_Selection("allow_print_pdf", "開放列印選課確認pdf檔",
                 "加退選結束後由教學組產生選課結果確認單(pdf檔), 
                  交由電算中心執行檔案分配程式後方可開放.");

  Show_Selection("allow_print_graduate_pdf", "開放列印畢業資格審查pdf檔",
                 "教學組不定期更新畢業資格審核pdf檔, 
                  交由電算中心執行檔案分配程式後方可開放.");

  Show_Selection("force_print_graduate_pdf", "要求確認畢業資格審查pdf檔",
                 "對於有畢業資格審查檔的同學, 強制要先確認該資料後才能選課.
                  若開啟此選項, 上一個選項也必須開啟."); 

  Show_Selection("show_last_total", "是否顯示上次篩選後餘額",
                 "在第二階段的多次篩選過程中,
                  顯示此資料可避免學生選一些不太可能選上的課.
                  此欄位將顯示在加選時的科目選單中");
  Show_Selection("show_immune_count", "是否顯示可加選名額人數",
                 "在先選先贏的時段中, 顯示此欄位,
                 可加選名額 = (限修人數) + (已加選的加簽人數) - (目前所有選修人數)
                 此欄位將顯示在加選時的科目選單中");
  Show_Selection("allow_query_last_select_namelist", "是否可以查詢上次篩選後名單",
                 "(教師)查詢選課名單功\能中, 
                 是否出現可查詢 \"上次篩選後名單\" 選項");
  Show_Selection("no_ban", "是否允許\限本系擋修",
                 "(第二階段選課時)若設定為限本系擋修無效,
                 所有超過十個科目的擋修設定(視同為限本系)將不作用(通識與軍訓課程不在此限)");
  Show_Selection("allow_select_math", "是否開放加選數學系所開設之課程",
                 "第一階段選課時, 數學系所的課程採先選先贏額滿為止, 
                 系統獨立某一天專門選修數學系所開設的課程, 故有此選項");
  Show_Selection("redirect_to_query", "是否請使用者連線至查詢系統",
                 "系統準備下學期開課期間, 會把本學期資料清空,
                 此時要設定請使用者連線至資料查詢網頁(ccmisp03/04)");
  Show_Selection("black_list", "是否開啟黑名單功\能",
                 "加選次數太過分的黑名單. 若是開啟此功\能, 
                 黑名單中的學生會在主選單看到警告訊息. 若關閉此功\能,
                 系統仍會紀錄 log, 只是不會顯示警訊.");

  print qq(
      </TABLE>
      <P>
        <INPUT type=hidden name=modify_flag value=1>
        <INPUT type=submit>
      </FORM>
  );
}

#####################################################################
sub Show_Selection()
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


