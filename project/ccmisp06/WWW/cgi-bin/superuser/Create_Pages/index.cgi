#!/usr/local/bin/perl

#############################################################################
#####  index.cgi
#####  提供連結, 用來產生開課資料靜態網頁ㄝ, 以及以時間查詢開課資料的資料
#####  Nidalap :D~
#####  2008/11/13
######### require .pm files #########
require "../../library/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Password.pm";
require $LIBRARY_PATH . "Error_Message.pm";

my(%Input);
%Input=User_Input();

 HTML_Head("產生開課靜態網頁");
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
        	  win=open(link,"openwin","width=350,height=350,resizable");
        	  win.creator=self;
      		}
	  </SCRIPT>
          <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
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
        <FORM action=Create_Course_View.cgi method=POST target=NEW>
          <INPUT type=hidden name=password value=$Input{password}>
          <INPUT type=submit value="產生靜態開課HTML網頁">
        </FORM>
        
        </TD><TD>
        
        <FORM action=Create_Course_View_by_Time.cgi method=POST target=NEW>
          <INPUT type=hidden name=password value=$Input{password}>
          <INPUT type=submit value="產生以開課時間查詢的資料">
        </FORM>
        
        </TD><TD>
        
        <FORM action=Create_Support_Course_View.cgi method=POST target=NEW>
          <INPUT type=hidden name=password value=$Input{password}>
          <INPUT type=submit value="產生支援本班課程的資料">
        </FORM>
		
		</TD><TD>
		<FORM action=Create_Precourse_Selection.cgi method=POST target=NEW>
          <INPUT type=hidden name=password value=$Input{password}>
          <INPUT type=submit value="產生選擇先修科目檔">
        </FORM>
		

      </TD></TR>
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
  @{$X{teacher}}	= ( "<del>教師檔: 開課資料會用到.",
                    	    $REFERENCE_PATH . "teacher.txt",
                    	    "Update_teacher01.php"  );  
  @{$X{student}}	= ( "學籍資料檔: 學生選課/查詢等會用到.",                                                           
                    	    $REFERENCE_PATH . "student.txt",
                    	    "Update_student01.php"  );  
  @{$X{change_school_student}} = ( "<del>轉學生資料檔: 上學期選課與篩選時會用到.",
                    	    $REFERENCE_PATH . "Change_School_Student.txt",
                    	    "Update_change_school_student.php" );
  @{$X{deduct}}		= ( "抵免成績檔: 先修科目篩選, 與重複修習篩選都會用到.",                                                           
                    	    $DATA_PATH . "Grade/deduct.txt",
                    	    "Update_deduct.php" );  
  @{$X{std_orders}}	= ( "學生歷年排名: 查詢成績會用到.",
                    	    $DATA_PATH . "Grade/std_orders.txt",
                    	    "Update_std_orders.php"  );
  @{$X{qualify_english}}= ( "學生英文檢定成績, 先修篩選會用到.",
                            $DATA_PATH . "Grade/qualify_english.txt",
                            "Update_qualify_english.php"  );
  @{$X{teacher_edu}}	= ( "學程資格檔: 可加選學程中心開的課的名單.",
                    	    $REFERENCE_PATH . "teacher_edu.txt",
                    	    "Update_teacher_edu.php" );
  @{$X{dual}}		= ( "雙主修名單: 選課期間與系統篩選期間需要更新.",
                    	    $REFERENCE_PATH . "double.txt",
                    	    "Update_dual.php" );
  @{$X{minor}}		= ( "輔系名單: 選課期間與系統篩選期間需要更新.",
                    	    $REFERENCE_PATH . "fu.txt",
                    	    "Update_minor.php" );
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