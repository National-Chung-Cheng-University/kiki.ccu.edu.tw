#!/usr/local/bin/perl

#############################################################################################
#####     Create_Course_View
#####  由目前開課資料產生課程資料HTML檔, 供學生查詢
#####  需要資料: 開課資料
#####  輸出資料: 選擇系所的HTML檔 * 1
#####            各個系所的開課資料HTML檔 * n
#####  Coder   : Nidalap
#####  Date    : May 31, 2000
#####  Update  : 
#####    May 15, 2001
#####    2007/06/22 加入自動 tgz 檔案, 並且放入 zipfiles/ 目錄
#####    2008/05/30 加入學程科目連結 -> class_new/Show_All_GRO.cgi
#####    2008/06/03 將學程視為一個學院, 加在最右側
#####	 2008/08/05 增加 Ecourse 課程大綱連結
#####	 2009/05/22 新增(暑修的)第一類/第二類課程於備註一欄.  Nidalap :D~
#####	 2009/06/04 為 Find_All_Dept 加上 "NO_COM_DEPT" 參數，只讀取可以開課的系所 Nidalap :D~
#####	 2009/12/25 若是暑修系統，將跨領域學程選項拿掉 Nidalap :D~
#####               另, 將原先跨領域學程動態網頁改為在此產生靜態網頁, 以免無法 tgz 歷史檔
#####    2010/05/20 若為通識科目，要顯示擋修系所  Nidalap :D~
#####    2010/08/10 全英語授課課程要顯示註解.  Nidalap :D~
#####    2012/04/17 新增開課學制 attr 欄位(只有非專班研究所).  Nidalap :D~
#####    2014/01/13 新增通識新制向度欄位. Nidalap :D~
#####    2015/07/28 新增中英對照  Nidalap :D~
#####    2015/08/18 發現中英對照畫面太雜亂，改把英文版獨立出來  Nidalap XDDD
#####    2015/10/27 解決下載歷年開課資料壓縮檔的學年學期列表排序錯亂問題 Nidalap :D~
#####	 2015/11/05 新增「全英語授課課程」頁面 $all_eng_page Nidalap :D~
##############################################################################################

$| = 1;
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Common_Utility.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Course.pm";
require $LIBRARY_PATH . "Teacher.pm";
require $LIBRARY_PATH . "Classroom.pm";
require $LIBRARY_PATH . "English.pm";
require $LIBRARY_PATH . "Password.pm";
require $LIBRARY_PATH . "Error_Message.pm";

#%Input=User_Input();
Read_GRO();
$HTML_PATH = $WWW_PATH . "Course/";        ### 產生的HTML要放在這個目錄
$fn1 = "<FONT size=3>";
$fn2 = "<FONT size=2>";
@dept = Find_All_Dept("NO_COM_DEPT");

HTML_Head("產生開課靜態網頁");
#print("passwd = $Input{password}<BR>\n");
$su_flag = Check_SU_Password($Input{password}, "su");
if( $su_flag ne "TRUE" ) {
  print("Password check error! system logged!!\n");
  exit();
}

print qq[
  </CENTER>
  <B>
    產生開課資料查詢網頁<BR>
    產生的網頁會放在: $HTML_PATH 下<BR>
     正在產生以下網頁:<BR>
  </B>
  <UL>index.html, 
];

$all_eng_page = $HTML_PATH . "all_english.html";
open(ALL_ENG, ">$all_eng_page") or die("Cannot open file > $all_eng_page!<BR>\n");

print ALL_ENG Create_Header_All_Eng();

foreach $dept (@dept) {
  $dept =~ /^(.)/;
  $changeline = $1;
  if( $old_changeline != $changeline ) {
    $old_changeline = $changeline;
    print("<BR>\n");
  }
  print(" $dept");
  $exists{$dept} = Create_Dept_Course_HTML($dept);
}
print("</UL>");
Create_Index_HTML(%exists);

#####   產生 zip 檔案
$zipfile_name = $YEAR . $TERM . ".tgz";
$exec_string = "sync; cd " . $WWW_PATH . "Course/;  tar cfz zipfiles/" . $zipfile_name . " *.html";
print("<B>正在執行 $exec_string...<BR>\n");
system($exec_string);
#####   對 zip 檔做索引 html 
Create_Zip_Index_HTML();

#####   用 lynx 對所有網頁做 reload
$exec_string = "lynx -reload -traversal -dump " . $HOME_URL . "Course/index.html";
print("<BR>\n正在執行 $exec_string...<BR></B>\n");
print("<UL>");
system($exec_string);

print("</UL><P><H1><B>網頁產生完畢!<P>\n");
############################################################################
sub Create_Zip_Index_HTML
{
  print("<BR>\n正在產生歷年 zip 檔案索引網頁...<BR>\n");
  my $zip_dir = $WWW_PATH . "Course/zipfiles/";
  print("$zip_dir");
  opendir(ZIP_DIR, $zip_dir) or die("Fatal error: cannot open dir $zip_dir!");
  my $content = "";
  my @files = readdir(ZIP_DIR);
  #@files = reverse sort(@files);
  @files = sort Sort_by_Year_Term @files;

  foreach $file (@files) {
#    print("<BR>-> $file<BR>\n");
    if( $file =~ /\.tgz$/ )  {
      $content .= "<LI><A href='$file'>$file</A>\n";
    }
  }

  my $index_file		= $zip_dir . "index.html";
  open(INDEX, ">$index_file") or die("Cannot create zip index file $index_file!\n");
  
  print INDEX qq(
    <HTML>
      <HEAD>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <META HTTP-EQUIV="Pragma" CONTENT="NO-CACHE">
        <META HTTP-EQUIV="expires" CONTENT="-1">
        <TITLE>
		  國立中正大學 $SUB_SYSTEM_NAME 開排選課系統歷年課程表
		  CCU Course Lists in Previous Semesters
		</TITLE>
      </HEAD>
      <BODY background="$GRAPH_URL/bk.jpg">
        <CENTER><H1><FONT face="標楷體">
          國立中正大學$SUB_SYSTEM_NAME開排選課系統<BR>
          歷年課程表 <BR>
		  CCU Course Lists in Previous Semesters
		  </FONT></H1>
        <HR>
        $content
  );  
  close(INDEX);

}
############################################################################
#####  從檔案名稱 YYYT.tgz 或者 YYT.tgz，擷取學年學期並排序之
sub Sort_by_Year_Term
{ 
#	$t1 = substr($a, -5, 1); $y1 = substr($a, -7, 3);
#	$t2 = substr($b, -5, 1); $y2 = substr($b, -7, 3);
	#$a =~ /^(\d[2-3])(\d)\.tgz$/;		$y1 = $1; $t1 = $2;		###  不可以直接修改 $a 和 $b！
	#$b =~ /^(\d[2-3])(\d)\.tgz$/;		$y2 = $1; $t2 = $2;
	$y1 = $a; $y1 =~ s/\.tgz//;		$t1 = chop($y1);
	$y2 = $b; $y2 =~ s/\.tgz//;		$t2 = chop($y2);

#	print("[y1,t1,y2,t2] = [$y1,$t1,$y2,$t2]<BR>\n");
	
	if( $y1 < $y2 )	{ return 1;  }
	else					{ return -1; }
	
}


############################################################################
sub Create_Index_HTML()
{
  my(%exists) = @_;		### 某系是否有開課的 flag

  mkdir($HTML_PATH, 0755)  if( not -e $HTML_PATH );
  $index_file		= $HTML_PATH . "index.html";
  $index_e_file	= $HTML_PATH . "index_e.html";
  open(INDEX, ">$index_file") or die("Cannot create index file $index_file!\n");
  open(INDEX_E, ">$index_e_file") or die("Cannot create index file $index_e_file!\n");
  
  $year_term_english = Year_Term_English();
  print INDEX		Create_Index_HTML_c();
  print INDEX_E		Create_Index_HTML_e();

  ($dept_table, $dept_table_e) = Dept_Table(%exists);
  print INDEX		$dept_table;
  print INDEX_E		$dept_table_e;
  %time = gettime();
  ($year_last, $term_last) = Last_Semester(1);
  $zipfile	= "zipfiles/" . $YEAR . $TERM . ".tgz";
  $zipfile_last	= "zipfiles/" . $year_last . $term_last . ".tgz";
  print INDEX		Create_Footer_HTML_c();
  print INDEX_E		Create_Footer_HTML_e();
  
  close(INDEX);
  close(INDEX_E);
}
############################################################################
sub Create_Index_HTML_c()
{
  my $html;
  $html = "
    <HTML>
      <HEAD>
        <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
        <TITLE>
		  國立中正大學$SUB_SYSTEM_NAME開排選課系統 $YEAR學年度第$TERM學期課程表
		  CCU Course Lists in $year_term_english
		</TITLE>
		<META HTTP-EQUIV='Pragma' CONTENT='NO-CACHE'>
        <META HTTP-EQUIV='expires' CONTENT='-1'>        
      </HEAD>
      <BODY background='$GRAPH_URL/bk.jpg'>
        <TABLE border=0 width=90%>
		  <TR>
		    <TD align='CENTER'>
			  <H1><FONT face='標楷體'>
              國立中正大學$SUB_SYSTEM_NAME開排選課系統<BR>
              $YEAR學年度$TERM_NAME課程表<BR>
		      CCU Course Lists in $year_term_english<BR></H1>
		    </TD>
		  </TR><TR>
		    <TD align='RIGHT'>
			  <H1>[ 中文版 | <A href='index_e.html'>English Version</A> ]</H1>
			</TD>
		  </TR>
		</TABLE>
        <HR>
  ";
  return $html;
}  
############################################################################
sub Create_Index_HTML_e()
{
  my $html;
  $html = "
    <HTML>
      <HEAD>
        <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
        <TITLE>
		  CCU Course Lists in $year_term_english
		</TITLE>
		<META HTTP-EQUIV='Pragma' CONTENT='NO-CACHE'>
        <META HTTP-EQUIV='expires' CONTENT='-1'>        
      </HEAD>
      <BODY background='$GRAPH_URL/bk.jpg'>
        <TABLE border=0 width=90%>
		  <TR>
		    <TD align='CENTER'>
			  <H1><FONT face='標楷體'>
              CCU Course Lists in $year_term_english<BR></H1>
		    </TD>
		  </TR><TR>
		    <TD align='RIGHT'>
			  <H1>[ <A href='index.html'>中文版</A> | English Version ]</H1>
			</TD>
		  </TR>
		</TABLE>
        <HR>
  ";
  return $html;
}  

############################################################################
sub Create_Header_All_Eng()
{
  my $html;
  
  $year_term_english = Year_Term_English();
  
  $html = "
    <HTML>
      <HEAD>
        <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
        <TITLE>
		  國立中正大學$SUB_SYSTEM_NAME開排選課系統 $YEAR學年度第$TERM學期課程表
		  CCU Course Lists in $year_term_english
		</TITLE>
		<META HTTP-EQUIV='Pragma' CONTENT='NO-CACHE'>
        <META HTTP-EQUIV='expires' CONTENT='-1'>        
      </HEAD>
      <BODY background='$GRAPH_URL/bk.jpg'>
        <TABLE border=0 width=90%>
		  <TR>
		    <TD align='CENTER'>
			  <H1><FONT face='標楷體'>
              國立中正大學$SUB_SYSTEM_NAME開排選課系統<BR>
              $YEAR學年度$TERM_NAME <FONT color='RED'>全英語授課</FONT>課程表<BR>
		      CCU Course Lists in $year_term_english <FONT color='RED'>(English taught courses)</FONT><BR></H1>
		    </TD>
		  </TR>
		</TABLE>
        <HR>
		<TABLE border=1 width='90%'>
		  <TR>
		    <TH>學系 / Department</TH>
			<TH>年級 / Year Standing</TH>
			<TH>科目代碼 / Course ID</TH>
			<TH>班別 / Class</TH>
			<TH>科目名稱 / Course Title</TH>
			<TH>任課教授 / Instructor</TH>
			<TH>時數 / Hours per Week</TH>
			<TH>學分數 / Credit</TH>
			<TH>選必 / Credit Type</TH>
			<TH>星期節次 / Day & Period</TH>
			<TH>教室 / Classroom</TH>
			<TH>限修人數 / Student Limit</TH>
			<TH>授課大綱 / Syllabus</TH>
			<TH>備註 / Remarks</TH>
		  </TR>
  ";
  return $html;
}  

###########################################################################
sub Create_Footer_HTML_c
{
  my $html;
  $html =  "
    <P>
    <center>
      <FONT color=GREEN size=-1>
        <LI>本課程表僅供查詢當學期開課資料用, 若要選課請使用<A href='http://kiki.ccu.edu.tw/'>選課系統</A>.
        <LI>這裡的資料是 [$time{time_string}] 產生的, 科目異動或新舊學期交替期間, 可能會出現舊資料, 可按 Ctrl + F5 重新讀取以更新資訊.
      </FONT>
      <BR>
      <FONT size=+1>
        [
          <A href='$CGI_URL/Query/Query_by_time1.cgi'>進階開課資料查詢</A> |
          <A href='../cgi-bin/class/Show_All_GRO.cgi'>所有跨領域學程</A> |
          <A href='$HOME_URL/Update_Course.html'>檢視所有異動科目</A> |
		  <A href='$HOME_URL/Course/all_english.html'>檢視所有全英語授課科目</A>
        ]
        <BR>

        </FONT><FONT size=-1>
        [
          開課資料壓縮檔下載: 
          <A href='$zipfile'>本學期</A> | 
          <A href='$zipfile_last'>上學期</A> |
          <A href='zipfiles/'>其他學期(檔案名稱是學年學期)</A>
        ]
	</center>
	</BODY>
    <HEAD>
      <META HTTP-EQUIV='Pragma' CONTENT='no-cache'>
      <META HTTP-EQUIV='Expires' CONTENT='-1'>
    </HEAD>
  ";
  
  return $html;
}
###########################################################################
sub Create_Footer_HTML_e
{
  my $html;
  $html =  "
    <P>
    <center>
      <FONT color=GREEN size=-1>
		<LI>The information here is for reference only, for updated info, please refer to <A href='http://kiki.ccu.edu.tw/'>Course Selection System</A>.
		<LI>The data here is generated at [$time{time_string}]. For latest updates, Please use Ctrl-F5 to refresh your browser.
      </FONT>
      <BR>
      <FONT size=+1>
        [
          <A href='$CGI_URL/Query/Query_by_time1.cgi'>Advanced Course Query</A> |
          <A href='../cgi-bin/class/Show_All_GRO.cgi'>Interdisciplinary Courses</A> |
          <A href='$HOME_URL/Update_Course.html'>Updated Courses</A> |
		  <A href='$HOME_URL/Course/all_english.html'>English-taught Courses</A>
        ]
        <BR>

        </FONT><FONT size=-1>
        [
          Download Course Data Zipped Files: 
          <A href='$zipfile'>Current Semester</A> | 
          <A href='$zipfile_last'>Last Semester</A> |
          <A href='zipfiles/'>Previous Semesters</A>
        ]
	</center>
	</BODY>
    <HEAD>
      <META HTTP-EQUIV='Pragma' CONTENT='no-cache'>
      <META HTTP-EQUIV='Expires' CONTENT='-1'>
    </HEAD>
  ";
  
  return $html;
}
###########################################################################
sub Create_Dept_Course_HTML()
{
  ($dept) = @_;
  my $exists;				## 回傳本系是否有開課資料的 flag
  my $html, $html_e;
  
  $html_file			= $HTML_PATH . $dept . ".html";
  open(HTML, ">$html_file") or die("Cannot create index file $html_file!\n");
  $html_file_e			= $HTML_PATH . $dept . "_e.html";
  open(HTML_E, ">$html_file_e") or die("Cannot create index file $html_file_e!\n");

  @course = Find_All_Course($dept, "", "");
  $exists = @course;
  %dept = Read_Dept($dept);
  %time = gettime();
  if( !$IS_GRA and !is_Undergraduate_Dept($dept) and !is_Exceptional_Dept($dept) ) {
    $show_attr = 1;			###  非暑修的研究所要顯示欄位「開課學制」
    $attr_th		= "<TH>$fn1開課學制</TH>";
	$attr_th_e	= "<TH>$fn1Credit Type</TH>";
  }else{
    $show_attr = 0;
    $attr_th		= "";
	$attr_th_e	= "";
  }
  #####  如果是在產生通識的科目清單，年級欄位要改為顯示領域與向度
  if( $dept eq $DEPT_CGE ) {
    %cge_course_list = Find_All_History_Course_by_CGE_Category();
	#Print_Hash(%cge_course_list);
	#die();
	my ($cate_ref, $subcate_ref) = Get_CGE_Categories();
	%category = %{$cate_ref};
	%subcategory = %{$subcate_ref};
	
	Print_Hash(%category);
	Print_Hash(%subcategory);
	
	#die();
	
    #my %cge_course_list = Find_All_History_Course_by_CGE_Category();
    $grade_title		= "領域</TH><TH>向度";
	$grade_title_e	= "Category(old)</TH><TH>Category(new)";
  }else{
    $grade_title		= $fn1 . "年級";
	$grade_title_e	= $fn1 . "Year Standing";
  }
  
  ($html, $html_e) = Create_Dept_Course_HTML1();
  print HTML		$html;
  print HTML_E  $html_e;  

  foreach $course (@course) {
#    print("$dept -> $$course{id}, $$course{group}\n");
    %course = Read_Course($dept, $$course{id}, $$course{group}, "", "", "產生開課資料HTML");
    @bgcolor = ("", "#F4B780", "#D39F71", "#C09067", "#AE8662");
    %classroom = Read_Classroom($course{classroom});
    $teacher_string = "";  $teacher_string_e = "";
    foreach $t (@{$course{teacher}}) {
      Read_Teacher_File();
      $teacher_string .= $Teacher_Name{$t};
      $teacher_string .= " ";
	  $IS_ENGLISH = 1;
	  Read_Teacher_File();
	  $IS_ENGLISH = 0;
      $teacher_string_e .= $Teacher_Name{$t};
      $teacher_string_e .= " ";
    }
    #my $time_string = "", $time_string_e = "";
    $time_string = Format_Time_String($course{time});
    $IS_ENGLISH = 1;
	$time_string_e = Format_Time_String($course{time});
	$IS_ENGLISH = 0;
    
    $link_to_ecourse = "<A href=\"" . $ECOURSE_QUERY_COURSE_URL
                          . "&courseno=" . $$course{id} . "_" . $$course{group}
                          . "&year=" . $YEAR . "&term=" . $TERM . "\" target=NEW>";
    $link_to_ecourse_e = $link_to_ecourse . "link</A>";
    $link_to_ecourse .=  "link</A>";
    
    ($note_string, $note_string_e) = Format_Note_String(%course);

    $note_dis = $note_eng = $note_dis_e = $note_eng_e = "";
    if( $course{distant_learning} == 1 ) {
      $note_dis = "<FONT color=RED>(遠距教學課程)";
	  $note_dis = "<FONT color=RED>(Distant learning)";
    }
    if( $course{english_teaching} == 1 ) {
      $note_eng		= "<FONT color=RED>(全英語授課/English-Taught Course)";
	  $note_eng_e	= "<FONT color=RED>(English-Taught Course)";
    }
    
    if( $show_attr ) {
      $attr_td		= "<TD>" . $fn1 . $ATTR{$course{attr}} . "</TD>";
	  $attr_td_e	= "<TD>" . $fn1 . $ATTR_E{$course{attr}} . "</TD>";
    }else{
      $attr_td = "";
    }
	
    #####  如果是在產生通識的科目清單，年級欄位要改為顯示領域與向度
	if( $dept eq $DEPT_CGE ) {
	  my $cate = $cge_course_list{$course{id}}{'category'};
	  my $subcate = $cge_course_list{$course{id}}{'subcategory'};
	  my $cate_subcate = $subcategory{$cate}{$subcate}{'cname'};
	  $grade_show = $course{grade} . "</TD><TD>" . $cate_subcate;
	}else{
	  $grade_show = $course{grade};
	}
	
	($html, $html_e) = Create_Dept_Course_HTML2();
    print HTML		$html;
	print HTML_E	$html_e;	
	
	if( $course{'english_teaching'} == 1 ) {
	  Add_Eng_Record();			###  新增一筆紀錄到全英語授課頁面
	}	
  }
  print HTML ("</TABLE>");
  
  print HTML qq(<P><CENTER><A href="index.html">回上頁</A>);
  print HTML qq(
    </BODY>
      <HEAD>
        <META HTTP-EQUIV="Pragma" CONTENT="no-cache">
        <META HTTP-EQUIV="Expires" CONTENT="-1">
      </HEAD>
    </HTML>  
  );
  return($exists);
}
###########################################################################
sub Create_Dept_Course_HTML1
{
  my $html, $html_e;
  $html = "
    <HTML>
      <HEAD>
        <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>    
        <META HTTP-EQUIV='Pragma' CONTENT='NO-CACHE'>                
        <META HTTP-EQUIV='expires' CONTENT='-1'>
        <TITLE>國立中正大學$SUB_SYSTEM_NAME開排選課系統 $YEAR學年度第$TERM學期課程表--$dept{cname}</TITLE>
      </HEAD>
      <BODY background='$GRAPH_URL/bk3.jpg'>
      <CENTER><H1><FONT face='標楷體'>
         國立中正大學$SUB_SYSTEM_NAME開排選課系統<BR>
         $YEAR學年度$TERM_NAME  課程表<BR>
         系所別: $dept{cname}</FONT></H1>
      <HR>
      <FONT size=-1><A href='http://kiki.ccu.edu.tw/ccu_timetable.doc' target=NEW>上課時間表</A><BR>
      這裡的資料是 [$time{time_string}] 產生的, 科目異動或新舊學期交替期間, 可能會出現舊資料, 可按 Ctrl + F5 重新讀取以更新資訊. </FONT>
      <TABLE border=1>
        <TR bgcolor=YELLOW>
            <TH>$grade_title</TH><TH>$fn1編號</TH>
            <TH>$fn1班別</TH><TH>$fn1科目名稱</TH>
            <TH>$fn1任課教授</TH><TH>$fn1上課時數<BR>正課/實驗實習/書報討論</TH>
            <TH>$fn1學分</TH><TH>$fn1選必</TH>
            <TH>$fn1上課時間</TH><TH>$fn1上課地點</TH>
            <TH>$fn1限修人數</TH>
            $attr_th
            <TH>$fn1課程大綱</TH>
            <TH>$fn1備註</TH>
        </TR>
  ";

  $html_e = "
    <HTML>
      <HEAD>
        <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>    
        <META HTTP-EQUIV='Pragma' CONTENT='NO-CACHE'>                
        <META HTTP-EQUIV='expires' CONTENT='-1'>
        <TITLE>CCU Course Lists in $year_term_english -- $dept{ename}</TITLE>
      </HEAD>
      <BODY background='$GRAPH_URL/bk3.jpg'>
      <CENTER><H1><FONT face='標楷體'>
         CCU Course Lists in $year_term_english<BR>
         $dept{ename}</FONT></H1>
      <HR>
      <FONT size=-1><A href='http://kiki.ccu.edu.tw/ccu_timetable.doc' target=NEW>Course time table</A><BR>
	  The data here is generated at [$time{time_string}]. For latest updates, Please use Ctrl-F5 to refresh your browser.
      <TABLE border=1>
        <TR bgcolor=YELLOW>
            <TH>$grade_title_e</TH><TH>$fn1 Course ID</TH>
            <TH>$fn1 Class</TH><TH>$fn1 Course Title</TH>
            <TH>$fn1 Instructor</TH><TH>$fn1 Hours per week<BR>Regular/Experiments/Discussions</TH>
            <TH>$fn1 Credit</TH><TH>$fn1 Credit type</TH>
            <TH>$fn1 Day/Period</TH><TH>$fn1 Classroom</TH>
            <TH>$fn1 Student Limit</TH>
            $attr_th_e
            <TH>$fn1 Syllabus</TH>
            <TH>$fn1 Remarks(Might contain Chinese due to course remarks which cannot be translated afterwards)</TH>
        </TR>
  ";  
  
  return($html, $html_e);
}
###########################################################################
sub Create_Dept_Course_HTML2()
{
  my $html, $html_e;
  $html = "
        <TR>
        <TD bgcolor=$bgcolor[$course{grade}]>$fn1$grade_show</TD>
        <TD>$fn1$$course{id}</TD>
        <TD>$fn1$$course{group}</TD>
        <TD>$fn1$course{cname}<br>$course{ename}<BR>$note_dis $note_eng</TD>
        <TD>$fn1$teacher_string</TD>
        <TD align=center>$fn1$course{total_time}<BR>
            $course{lab_time1}/$course{lab_time2}/$course{lab_time3}</TD>
        <TD>$fn1$course{credit}</TD>
        <TD>$fn1$PROPERTY_TABLE[$course{property}]</TD>
        <TD>$fn1$time_string</TD>
        <TD>$fn1$classroom{cname}</TD>
        <TD>$fn1$course{number_limit}</TD>
        $attr_td
        <TD align=CENTER>$fn1$link_to_ecourse</TD>
        <TD>$fn1$note_string</TD>        
      </TR>
    ";
	
	$html_e = "
        <TR>
        <TD bgcolor=$bgcolor[$course{grade}]>$fn1$grade_show</TD>
        <TD>$fn1$$course{id}</TD>
        <TD>$fn1$$course{group}</TD>
        <TD>$fn1$course{ename}<BR>$note_dis_e $note_eng_e</TD>
        <TD>$fn1$teacher_string_e</TD>
        <TD align=center>$fn1$course{total_time}<BR>
            $course{lab_time1}/$course{lab_time2}/$course{lab_time3}</TD>
        <TD>$fn1$course{credit}</TD>
        <TD>$fn1$PROPERTY_TABLE_E[$course{property}]</TD>
        <TD>$fn1$time_string_e</TD>
        <TD>$fn1$classroom{ename}</TD>
        <TD>$fn1$course{number_limit}</TD>
        $attr_td_e
        <TD align=CENTER>$fn1$link_to_ecourse_e</TD>
        <TD>$fn1$note_string_e</TD>        
      </TR>
    ";
	return($html, $html_e);
}
###########################################################################
sub Dept_Table()
{
    my(%exists) = @_;
	
    my(@Dept)=Find_All_Dept("NO_COM_DEPT");
    foreach $gro_name (keys %gro_name) {				###  將跨領域學程視為系所
      if( $gro_name{$gro_name}{gro_name} ne "" ) {
#        print("pushing $gro_name ( $gro_name{$gro_name}{gro_name} ) into dept...\n");
        push(@Dept, $gro_name);
      }
    }
    my $DATA="", $DATA_E = "";
    my($Dept1,$Dept2,$Dept3,$Dept4,$Dept5,$Dept6,$Dept7,$Dept0)="";
	my($Dept1e,$Dept2e,$Dept3e,$Dept4e,$Dept5e,$Dept6e,$Dept7e,$Dept0e)="";

    $DATA		.= "<table width=90% border=0><tr>";
	$DATA_E 	.= "<table width=90% border=0><tr>";
	
	%COLLEGE = Find_All_College();
	foreach $col (sort  keys %COLLEGE) {
	  #print join(" : ", "col ", $col, $$col{"c"}, $COLLEGE{$col}{"e"}, "<BR>\n");
	  $DATA		.= "	 <th bgcolor=#99ffff>$fn2" . $COLLEGE{$col}{"c"} . "</th>";
	  $DATA_E	.= "	 <th bgcolor=#99ffff>$fn2" . $COLLEGE{$col}{"e"} . "</th>";
	}
		
    if( not (is_Summer() or is_GRA()) ) {
      $DATA		.= "	    <th bgcolor=#99ffff>$fn2跨領域學程</th>\n";
	  $DATA_E	.= "	    <th bgcolor=#99ffff>$fn2Interdisciplinary</th>\n";
    }
    $DATA		.= "   </tr>\n";
	$DATA_E	.= "   </tr>\n";

#    $Dept0 .= "<A href=I000.html>";
#    $Dept0 .= "共同科</A><br>\n";

    foreach $dept (@Dept){
#      print("now processing dept $dept...\n");
        if( length($dept) == 2 ) {		###  跨領域學程代碼是兩碼
          %Dept=("id"=>"$dept", "cname2"=>"$gro_name{$dept}{gro_name}", "ename"=>"$gro_name{$dept}{gro_e_name}");
        }else{					###  一般系所代碼是四碼
          %Dept=Read_Dept($dept);
        }
        $link = 1;
        $link = 0  if( $exists{$dept} == 0 );
        
        if( length($dept) == 2 ) {				###  if 跨領域學程
#          print("adding $dept into Dept8\n");
          $gro_link = "../cgi-bin/class/Show_All_GRO.cgi?gro_no=" . $dept;
          $Dept8	.= "<A href=$gro_link>$gro_name{$dept}{gro_name}</A><br>\n";
		  $Dept8e	.= "<A href=$gro_link>$gro_name{$dept}{gro_e_name}</A><br>\n";
        }else{							###  else 一般系所
#          print("adding $dept into dept0~7\n");
          if( ($Dept{id} == 0) or ($Dept{id} eq "7006") ){
              $Dept0	.= "<A href=$Dept{id}.html>" if $link;
              $Dept0	.= $fn2.$Dept{cname2}."</A><br>\n";
			  $Dept0e	.= "<A href=$Dept{id}_e.html>" if $link;
              $Dept0e	.= $fn2.$Dept{ename}."</A><br>\n";
          }else{
            if( $Dept{id}/1000 >= 7 ){
              $Dept7	.= "<A href=$Dept{id}.html>" if $link;
              $Dept7	.= $fn2.$Dept{cname2}."</A><br>\n";
              $Dept7e	.= "<A href=$Dept{id}_e.html>" if $link;
              $Dept7e	.= $fn2.$Dept{ename}."</A><br>\n";
            }elsif($Dept{id}/1000 >= 6){
              $Dept6 .= "<A href=$Dept{id}.html>" if $link;
              $Dept6 .= $fn2.$Dept{cname2}."</A><br>\n";
			  $Dept6e	.= "<A href=$Dept{id}_e.html>" if $link;
              $Dept6e	.= $fn2.$Dept{ename}."</A><br>\n";
            }elsif($Dept{id}/1000 >= 5){
              $Dept5 .= "<A href=$Dept{id}.html>" if $link;
              $Dept5 .= $fn2.$Dept{cname2}."</A><br>\n";
			  $Dept5e	.= "<A href=$Dept{id}_e.html>" if $link;
              $Dept5e	.= $fn2.$Dept{ename}."</A><br>\n";
            }elsif($Dept{id}/1000 >= 4){
              $Dept4 .= "<A href=$Dept{id}.html>" if $link;
              $Dept4 .= $fn2.$Dept{cname2}."</A><br>\n";
			  $Dept4e	.= "<A href=$Dept{id}_e.html>" if $link;
              $Dept4e	.= $fn2.$Dept{ename}."</A><br>\n";
            }elsif($Dept{id}/1000 >= 3){
              $Dept3 .= "<A href=$Dept{id}.html>" if $link;
              $Dept3 .= $fn2.$Dept{cname2}."</A><br>\n";
			  $Dept3e	.= "<A href=$Dept{id}_e.html>" if $link;
              $Dept3e	.= $fn2.$Dept{ename}."</A><br>\n";
            }elsif($Dept{id}/1000 >= 2){
              $Dept2 .= "<A href=$Dept{id}.html>" if $link;
              $Dept2 .= $fn2.$Dept{cname2}."</A><br>\n";
			  $Dept2e	.= "<A href=$Dept{id}_e.html>" if $link;
              $Dept2e	.= $fn2.$Dept{ename}."</A><br>\n";
            }elsif($Dept{id}/1000 >= 1){
              $Dept1 .= "<A href=$Dept{id}.html>" if $link;
              $Dept1 .= $fn2.$Dept{cname2}."</A><br>\n";
			  $Dept1e	.= "<A href=$Dept{id}_e.html>" if $link;
              $Dept1e	.= $fn2.$Dept{ename}."</A><br>\n";
            }
          }
        }
    }

#    $DATA = $DATA ."<tr>\n";
#    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept1."</td>\n";         # 文
#    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept2."</td>\n";         # 理
#    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept3."</td>\n";         # 社
#    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept4."</td>\n";         # 工
#    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept5."</td>\n";         # 管
#    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept6."</td>\n";         # 法
#    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept7."</td>\n";         # 教
#    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept0."</td>\n";         # 其他

    $DATA  .= 
	  "<tr>
        <td valign=top><FONT size=2>$Dept1</td>
        <td valign=top><FONT size=2>$Dept2</td>
        <td valign=top><FONT size=2>$Dept3</td>
        <td valign=top><FONT size=2>$Dept4</td>
        <td valign=top><FONT size=2>$Dept5</td>
        <td valign=top><FONT size=2>$Dept6</td>
        <td valign=top><FONT size=2>$Dept7</td>
        <td valign=top><FONT size=2>$Dept0</td>
	  ";
    $DATA_E  .= 
	  "<tr>
        <td valign=top><FONT size=2>$Dept1e</td>
        <td valign=top><FONT size=2>$Dept2e</td>
        <td valign=top><FONT size=2>$Dept3e</td>
        <td valign=top><FONT size=2>$Dept4e</td>
        <td valign=top><FONT size=2>$Dept5e</td>
        <td valign=top><FONT size=2>$Dept6e</td>
        <td valign=top><FONT size=2>$Dept7e</td>
        <td valign=top><FONT size=2>$Dept0e</td>
	  ";
	
    if( not (is_Summer() or is_GRA()) ) {
      $DATA		.= "    <td valign=top><FONT size=2>".$Dept8."</td>\n";         # 跨領域學程
	  $DATA_E	.= "    <td valign=top><FONT size=2>".$Dept8e."</td>\n";         # 跨領域學程
    }
    $DATA  .= "</tr></table>\n";
	$DATA_E  .= "</tr></table>\n";

    return($DATA, $DATA_E);
}


##################################################################################
sub HTML_Head
{
  my($title);
  ($title)=@_;
  print("Content-type: text/html\n\n");
  print qq(
        <html>
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
##################################################################################
sub Add_Eng_Record
{
  my 	$bgcolor, @bgcolor = ("#F4B780", "#D39F71", "#C09067", "#AE8662");

  $i++  if( $last_dept_ ne $course{'dept'} );
  $last_dept_ = $course{'dept'};
  
  my $bgcolor = $bgcolor[$i%4];
  
  print ALL_ENG qq"
    <TR>
	  <TD bgcolor='$bgcolor'>$dept{'cname'} / $dept{'ename'}</TD>
	  <TD>$course{'grade'}</TD>
	  <TD>$course{'id'}</TD>
	  <TD>$course{'group'}</TD>
	  <TD>$course{'cname'} / $course{'ename'}</TD>
	  <TD>$teacher_string / $teacher_string_e</TD>
	  <TD>$course{'total_time'}</TD>
	  <TD>$course{'credit'}</TD>
	  <TD>$PROPERTY_TABLE[$course{'property'}] / $PROPERTY_TABLE_E[$course{'property'}]</TD>
	  <TD>$time_string / $time_string_e</TD>
	  <TD>$classroom{'cname'} / $classroom{'ename'}</TD>
	  <TD>$course{'number_limit'}</TD>
	  <TD>$link_to_ecourse</TD>
	  <TD>$note_string / $note_string_e</TD>
    </TR>
  "

}