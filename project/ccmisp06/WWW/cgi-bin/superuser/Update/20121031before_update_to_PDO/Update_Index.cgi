#!/usr/local/bin/perl

#############################################################################
#####  Update_Index.cgi
#####  顯示系統參考資料檔案, 相關的更新時間
#####  Nidalap :D~
#####  2006/09/20
######### require .pm files #########
require "../../library/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Password.pm";
require $LIBRARY_PATH . "Error_Message.pm";

my(%Input);
%Input=User_Input();

 HTML_Head("系統參考資料管理子系統");
# print("pass = $Input{password}");
 $su_flag = Check_SU_Password($Input{password}, "su");
 if( $su_flag eq "TRUE" ) {
   HTML();
 }else{
   print("Password check error! system logged!!\n");
 }

##################################################################################
sub HTML_Head
{
  my($title);
  ($title)=@_;
  print("Content-type: text/html\n\n");
  print qq(
        <html>
    	  <SCRIPT language=JAVASCRIPT>
      		function Open_Update_Window(link)
   		{
        	  win=open(link,"openwin","width=600,height=800,resizable");
        	  win.creator=self;
      		}
	  </SCRIPT>
          <head>
            <meta http-equiv="Content-Type" content="text/html; charset=big5">
            <title>$title</title>
          </head>
          <BODY background="../../../Graph/manager.jpg">
            <CENTER>
              <H1>$title</H1>
              <HR size=2 width=50%>
  );
}         

###################################################################################
sub HTML
{
  print qq (
    <TABLE border=0>
      <TR><TD>
        <FORM action=View_crontab.cgi method=POST target=NEW>
          <INPUT type=hidden name=password value=$Input{password}>
          <INPUT type=submit value="檢視自動更新的 crontab">
        </FORM>
        
        </TD><TD>
        
        <FORM action=View_update_log.cgi method=POST target=NEW>
          <INPUT type=hidden name=password value=$Input{password}>
          <INPUT type=submit value="檢視更新檔案LOG">
        </FORM>
      </TR></TR>
    </TABLE>
  );
  print qq(
    <TABLE border=0 width=90%>
      <TR bgcolor=ORANGE><TH>檔名</TH><TH>更新時間</TH><TH>資料筆數</TH>
      <TH>說明</TH><TH>執行更新</TH></TR>      
  );
  
  List_file("grade_now");
  List_file("grade_summer");
  List_file("grade_all");
  List_file("deduct");
  List_file("std_orders");
#  List_file("qualify_english");
#  List_file("genedu_foreign_lang");
  List_file("a14teng_gen_class");
  
  print("<TR><TD colspan=6><HR></TD></TR>");
  List_file("dept");
  List_file("dept_com");

  print("<TR><TD colspan=6><HR></TD></TR>");    
  List_file("student");
  List_file("teacher");
  List_file("teacher_edu");
  List_file("change_school_student");
  List_file("dual");
  List_file("minor");
  List_file("early_warning_21_list");
    
  print("<TR><TD colspan=6><HR></TD></TR>");
  List_file("allcourse");
  List_file("a30tcourse");
  List_file("course_ncca");
  List_file("student_ncca");

  print("<TR><TD colspan=6><HR></TD></TR>");
  List_file("a14tapply_eng_class");
  List_file("a14tapply_eng_deduct_c");
  
  print("<TR><TD colspan=6><HR></TD></TR>");
  List_file("gro");

  print qq(
    </TABLE>
  );

}
###################################################################################
sub List_file
{
  my ($filename) = @_;
  
  my %X, $j, $size, $savetime, $timestring, @lines;

  @{$X{grade_now}}	= ( "當學期成績檔: 成績查詢, 先修科目篩選, 與重複修習篩選會用到.",
			    $DATA_PATH . "Grade/now.txt",
                    	    "Update_grade_now.php" );  
  @{$X{grade_summer}}	= ( "歷年暑修成績檔: 成績查詢, 先修科目篩選, 與重複修習篩選會用到.",
                    	    $DATA_PATH . "Grade/summer.txt",
                    	    "Update_grade_summer.php" );
  @{$X{grade_all}}	= ( "歷年成績檔: 成績查詢, 先修科目篩選, 與重複修習篩選會用到.",
                            $DATA_PATH . "Grade/score",
                            "Update_grade_all01.php" );
  @{$X{teacher}}	= ( "教師檔: 開課資料會用到.",
                    	    $REFERENCE_PATH . "teacher.txt",
                    	    "Update_teacher01.php"  );  
  @{$X{student}}	= ( "學籍資料檔: 學生選課/查詢等會用到.",                                                           
                    	    $REFERENCE_PATH . "student.txt",
                    	    "Update_student01.php"  );  
  @{$X{change_school_student}} = ( "轉學生資料檔: 上學期選課與篩選時會用到.",
                    	    $REFERENCE_PATH . "Change_School_Student.txt",
                    	    "Update_change_school_student.php" );
  @{$X{dept}}		= ( "系所資料檔: 開課與學生學籍相關.",
                            $REFERENCE_PATH . "Dept",
                            "Update_dept.php" );
  @{$X{dept_com}}	= ( "系所對應代碼檔: 因為系所合一, 導致系所更改代碼所用.",
                            $REFERENCE_PATH . "dept_com.txt",
                            "Update_dept_com.php" );
  @{$X{deduct}}		= ( "抵免成績檔: 先修科目篩選, 與重複修習篩選都會用到.",                                                           
                    	    $DATA_PATH . "Grade/deduct.txt",
                    	    "Update_deduct.php" );  
  @{$X{std_orders}}	= ( "學生排名檔: 查詢成績會用到.",
                    	    $DATA_PATH . "Grade/std_orders.txt",
                    	    "Update_std_orders01.php"  );
#  @{$X{qualify_english}}= ( "學生英文檢定成績, 先修篩選會用到.",
#                            $DATA_PATH . "Grade/qualify_english.txt",
#                            "Update_qualify_english.php"  );
#  @{$X{genedu_foreign_lang}} = ("新生英檢成績檔, 用於判別學生修習通識外語課程依據.",
#                            $DATA_PATH . "Grade/genedu_foreign_lang.txt",
#                            "Update_genedu_foreign_lang.php" );
  @{$X{a14teng_gen_class}} = ("通識英語成績檔, 用於作為批次載入新生通識英語課程依據, 以及選課時即時判斷程度用.",
                            $DATA_PATH . "Grade/a14teng_gen_class.txt",
                            "Update_a14teng_gen_class.php" );
  @{$X{teacher_edu}}	= ( "學程資格檔: 可加選學程中心開的課的名單.",
                    	    $REFERENCE_PATH . "teacher_edu.txt",
                    	    "Update_teacher_edu.php" );
  @{$X{dual}}		= ( "雙主修名單: 選課期間與系統篩選期間需要更新.",
                    	    $REFERENCE_PATH . "double.txt",
                    	    "Update_dual.php" );
  @{$X{minor}}		= ( "輔系名單: 選課期間與系統篩選期間需要更新.",
                    	    $REFERENCE_PATH . "fu.txt",
                    	    "Update_minor.php" );
  @{$X{early_warning_21_list}} = ("二一邊緣預警名單: (物理系)用於輔導學生選課的機制.",
                            $REFERENCE_PATH . "Early_Warning_21_List.txt",
                            "Update_early_warning_21_list.php" );
  @{$X{allcourse}}	= ( "歷年開課檔: 用來更新開課使用的歷年開課資料.",
                    	    $DATA_PATH . "Transfer/allcourse.txt",
                    	    "Update_allcourse01.php" );
  @{$X{course_ncca}}	= ( "<del>當學期開課/異動倒檔: 把當學期開課/異動資料倒到後端資料庫.",
                    	    $HOME_PATH . "BIN/NCCA/NCCA020",
                    	    "Update_course_ncca01.php" );
  @{$X{student_ncca}}	= ( "<del>當學期選課倒檔: 把當學期選課資料倒到後端資料庫.",
                    	    $HOME_PATH . "BIN/NCCA/NCCA090",
                    	    "Update_student_ncca01.php" );
  @{$X{a30tcourse}}	= ( "開課代碼檔: 為了避免開課使用到 \"曾經開過卻沒開成\" 的科目代碼, 須在開課前更新此檔.",
                            $REFERENCE_PATH . "a30tcourse.txt",
                            "Update_a30tcourse.php" );
  @{$X{gro}}		= ( "跨領域學程代碼檔: 此功\能會一併更新 gro_name, gro_dept, gro_cour, gro_std 四個學程相關檔案",
                            $REFERENCE_PATH . "gro_name.txt",
                            "Update_gro.php" );
  @{$X{a14tapply_eng_class}} = ( "應用英外語學程生名單, 用於加選應用應外語課程判斷.",
                            $REFERENCE_PATH . "a14tapply_eng_class.txt",
                            "Update_a14tapply_eng_class.php" );
  @{$X{a14tapply_eng_deduct_c}} = ( "可修課抵畢業門檻學生,  用於加選應用應外語課程判斷.",
                            $REFERENCE_PATH . "a14tapply_eng_deduct_c.txt",
                            "Update_a14tapply_eng_deduct_c.php" );
  

  ($j,$j,$j,$j,$j,$j,$j,$j,$j,$savetime,$j) = stat($X{$filename}[1]);
  my ($sec, $min, $hour, $mday, $mon, $year, $k) = localtime($savetime);
  $year += 1900;
  $mon  ++;
  $timestring = $year . "/" . $mon . "/" . $mday . " - " . $hour . ":" . $min . ":" . $sec;
  $timecolor  = Determine_Time_Color($year, $mon, $mday);
  
  open(REF_FILE, $X{$filename}[1]);
  @lines = <REF_FILE>;
  $size = @lines;
  close(REF_FILE);

  print qq(
    <TR>
      <TD align=RIGHT><B>$filename</TD>
      <TD><FONT size=-1 color=$timecolor>$timestring</TD>
      <TD align=RIGHT>$size</TD>
      <TD><FONT size=-1>$X{$filename}[0]</TD>
      <TD align=CENTER><INPUT type=button value=更新 onclick=Open_Update_Window("$X{$filename}[2]")></A></TD>
    </TR>
  );

}
###################################################################################
sub Determine_Time_Color
{
  my ($f_year, $f_mon, $f_mday) = @_;
  my $color;
  
  my ($sec, $min, $hour, $mday, $mon, $year, $k) = localtime();
  $year += 1900;
  $mon  ++;
  
  if( $year == $f_year ) {
    if( $mon == $f_mon )   {
      if( $mday == $f_mday )  {
        $color = "GREEN";			###  同年同月同日
      }else{
        $color = "BLUE";			###  不同日
      }
    }else{					###  不同月
      $color = "ORANGE";    
    }  
  }else{					###  不同年
    $color = "RED";
  }
    
  return($color);
}