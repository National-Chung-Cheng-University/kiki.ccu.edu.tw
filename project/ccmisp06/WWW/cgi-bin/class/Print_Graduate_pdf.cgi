#!/usr/local/bin/perl

#########################################################################
#####  Print_Graduate_pdf.cgi
#####  列印學生畢業資格審核 pdf 檔
#####  本程式由 Print_Course_pdf.cgi 修改而成.
#####  
#####  在執行此程式同時記錄到 ~/DATA/LOGS/Student_Graduate_PDF.log 中, 以便之後查詢.
#####  2005/09/07 新增下一頁確認功能, 限制學生必須確認後才能選課
#####  Coder: Nidalap Leee
#####  Updates: 
#####    2004/06/17 ???
#####    2013/08/23 英文版相關增修：將顯示文字拉到 Init_Text_Values() 中設定。 Nidalap :D~
#########################################################################

print("Content-type:text/html\n\n");

require "../library/Reference.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."GetInput.pm";
#require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."System_Settings.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Error_Message.pm";
#require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Session.pm";
require $LIBRARY_PATH."English.pm";

my(%Input,%Student,%Dept);


%Input    = User_Input();
($Input{id}, $Input{password}, $login_time, $ip) = Read_Session($Input{session_id}, "", 1);
#print("session_id, id, pass = $Input{session_id}, $Input{id}, $Input{password}<BR>"); 

%system_settings = Read_System_Settings();
%Student  = Read_Student($Input{id});
#%Dept     = Read_Dept($Student{dept});
%time     = gettime();
%txt	  = Init_Text_Values();

Check_Student_Password($Input{id}, $Input{password});

$space = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";

if( ($SUPERUSER==1) or ($system_settings{allow_print_graduate_pdf}==1) ) {
  Delete_Old_PDF_File();
  ($succeed_flag, $pdf_file) = Create_PDF_File($Input{id});
  Print_HTML($succeed_flag, $pdf_file);
}else{
  Print_BAN();
}

if( $IS_MOBILE )  {
  print Create_jQuery_Mobile_Footer_Tag($Student{name});
}

##############################################################################
sub Print_BAN()
{
  print "
    <html>
    <head>
      <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
      <TITLE>" . $txt{'html_title'} .  "</TITLE>
    </head>
    <body background='" . $GRAPH_URL . "/ccu-sbg.jpg'>
    <center>
      <FONT face='標楷體'>
        <H1>" . $txt{'html_title'} . "</H1>
      </FONT>
    <HR>
    " . $txt{'not_avail'} . "<BR>
  ";
}

##############################################################################

sub Print_HTML() 
{
  my($succeed_flag, $pdf_file) = @_;
  
  Graduate_Log($Input{id});
#  Student_Log("Print2", $Input{id}, "", "", "");
  if( $IS_MOBILE ) {  $mobile_temp = Create_jQuery_Mobile_Script();  }
  print "
    <html>
    <head>
      <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
	  $mobile_temp
      <TITLE>" . $txt{'html_title'} . "</TITLE>
    </head>
  ";
  
  if( $IS_MOBILE ) {
    print Create_jQuery_Mobile_Title_Tag();
  }else{
    print "
      <body background='$GRAPH_URL/ccu-sbg.jpg'>
      <center>
        <FONT face='標楷體'>
          <H1>" . $txt{'title'} . "</H1>
        </FONT>
		<HR>
    ";
  }
#  print("flag = $succeed_flag<BR>\n");
  if( $succeed_flag == 1 ) {
    print "
      <TABLE border=0>
        <TR><TD align=CENTER>
          &nbsp<P>
          &nbsp<P>
          " . $txt{'click'} . " <A href='$pdf_file' target=NEW>" . $txt{'title'} . "</A>
          <P>
    ";
    if( ($SUPERUSER==1) or ($system_settings{force_print_graduate_pdf}==1) ) {
      print "
          <FORM action='Print_Graduate_pdf2.cgi' method=POST>
            <INPUT type=hidden name=session_id value=" . $Input{session_id} . ">
			<INPUT type=checkbox name=check>            
            " . $txt{'reviewed'} . "
			<P>
            <INPUT type=SUBMIT value='" . $txt{'submit'} . "'>
          </FORM>
      ";
    }
	
	if( $IS_MOBILE ) {
	  print "
	     &nbsp<P>
        </TD></TR>
        <TR><TD>
		  <LI>" . $txt{'reference'} . $txt{'use_pc'} . "
		</TD></TR>
		</TABLE>
	  ";
	}else{
	
      print "
          &nbsp<P>
          &nbsp<P>
        </TD></TR>
        <TR><TD>
		  <LI>" . $txt{'note1'} . "
		  <LI>" . $txt{'note2'} . "
		  <LI>" . $txt{'note3'} . "
		  <LI>" . $txt{'note4'} . "
		  <LI>" . $txt{'note5'} . "
		  <LI>" . $txt{'note6'} . "
		  <LI>" . $txt{'note7'} . "
        </TD></TR>
        </TABLE>
      ";
	}
  }else{
    print "<P>" . $txt{'not_found'};
  }
}


############################################################################
sub Create_PDF_File()
{
  my($succeed_flag, $pdf_source, $pdf_temp_path, $pdf_dest, $pdf_url);
  
  my($id) = @_;
  $id =~ /^(...)/;
  
  $pdf_source = $DATA_PATH . "Graduate_PDF/" . $1 . "/" . $id . ".pdf";

  $pdf_dest = Scramble($id);
  $pdf_url  = $PDF_TEMP_URL . $pdf_dest;
  $pdf_dest = $PDF_TEMP_PATH . $pdf_dest;
  
#  print("source = $pdf_source<BR>\n");
  if( -e $pdf_source ) {
#    print("cp $pdf_source $pdf_dest ($pdf_url)<BR>\n");
    use File::Copy;
    copy($pdf_source, $pdf_dest);
    $succeed_flag = 1;
  }else{
    $succeed_flag = 0;
  }

#  print("flag = $succeed_flag<BR>\n");  
  return($succeed_flag, $pdf_url);
}
############################################################################
sub Scramble()
{
  my($id) = @_;
  
  my($filename, %time, $time_temp);
  $filename = $id;
  %time = gettime();

  $time_temp = join("", $time{year}, $time{month}, $time{day}, $time{hour}, $time{min});
  $time_temp = Crypt($time_temp);
  $filename = $time_temp . Crypt($filename);
#  print("filename = $filename<BR>\n");
  $filename =~ s/\W/A/g;
  $filename .= ".pdf";
#  $filename = md5($filename);
#  open(RESULT, "md5 -s 1111111");
#  $filename = <RESULT>;

#  print("filename = $filename<BR>\n");  
#  $filename = exec("md5 -s $filename");
  
  return($filename);
}
############################################################################
sub Delete_Old_PDF_File()
{
  my(@files, $j, $mtime, $now, $time_diff);
  opendir(TEMP, $PDF_TEMP_PATH);
  @files = readdir(TEMP);

#  print("TEMP_PATH = $PDF_TEMP_PATH<BR>\n");  
  foreach $file (@files) {
    next if( ($file eq ".") or ($file eq "..") );
    next if( $file eq "index.html" );

    $file = $PDF_TEMP_PATH . $file;
    ($j, $j, $j, $j, $j, $j, $j, $j, $j, $mtime) = stat $file;
    $now = time;
    $time_diff = $now - $mtime;
    if( $time_diff > 600 ) {                ###  檔案存在超過十分鐘
      unlink($file);
#      print("del: $file<BR>\n");
    }
#    print("$file -> $mtime, $time_diff<BR>\n");
  }  
}
##########################################################################
sub Graduate_Log()
{
  my($id) = @_;
  my($log_file, %time, $su, $ip);
  
  %time = gettime();
  $su = "SU"  if($SUPERUSER == 1);
  if($ENV{HTTP_X_FORWARDED_FOR} eq "")  { $ip = $ENV{REMOTE_ADDR};  }
  else                                  { $ip = $ENV{HTTP_X_FORWARDED_FOR}; }

  umask(000);
  $log_file = $LOG_PATH . "Student_Graduate_PDF.log";
  open(LOG_FILE, ">>$log_file") or print("ERROR:Cannot open file $logfile!\n");
  print LOG_FILE ("$time{time_string} : $ip  : $id : $course_id $su\n");
  close(LOG_FILE);
}
  
##################################################################################
#####  因應英文版本，將所有要顯示的文字在此整理，依照 $IS_ENGLISH 自動判別  2015/04/30
sub Init_Text_Values
{
  my %txtall;
  #global $SUB_SYSTEM_NAME, $YEAR, $TERM_NAME, $Student, $Dept;
  
  %txtall = (
    'html_title'=> {'c'=>$SUB_SYSTEM_NAME . '畢業資格審查表(' . $Student{name}. ')',
					'e'=>'Qualification Form for Graduation' },
    'title'=> {'c'=>$SUB_SYSTEM_NAME . '畢業資格審查表(' . $Student{name}. ')',
					'e'=>'Qualification Form for Graduation' },
	'not_avail'	=> {'c'=>'畢業資格審查表目前不開放列印!', 
					'e'=>'The qualification form for graduation is not available for printing. '},
	'not_found'	=> {'c'=>'查無您的畢業資格審查表資料, <BR>請洽教務處教學組!', 
					'e'=>'Your qualification form for graduation is not found,<BR>
					      please contact Division of Instruction and Curriculum.'},
	'reviewed'	=> {'c'=>'我已經看過我的畢業資格審查表了', 'e'=>'I have reviewed my qualification form for graduation'},
	'click'		=> {'c'=>'請點選檢視', 'e'=>'Click  to view'},
	'submit'	=> {'c'=>'確認', 'e'=>'Submit'},
	'reference'	=> {'c'=>'此畢業資格審查表僅供查詢參考，仍需以新生修業規定為準，
						  應屆畢業生之畢業資格審查結果應以各學系公告為主。', 
					'e'=>'The qualification form for graduation is for reference only; please follow based the provisions of
						study for new students. The results of qualification shall be based on the announcements of each department.'},
	'use_pc'		=> {'c'=>'詳細說明請使用電腦板檢視。', 
						'e'=>'For detailed information, please refer to PC version.'},
	
	'note1'			=> {'c'=>'畢業資格審查表為PDF檔無法即時更新，更新時間為第二階段加退選與期中考試前，每學期更新兩次。', 
						'e'=>'Qualification form for graduation is in PDF format and will only be updated twice each semester: 
							before the second phase of course add/drop and before the midterm exams. '},
	'note2'			=> {'c'=>'此畢業資格審查表僅供查詢參考，仍需以新生修業規定為準；
							應屆畢業生之畢業資格審查結果應以各學系公告為主。 ', 
						'e'=>'The qualification form for graduation is for reference only; please follow based the provisions
							of study for new students. The results of qualification shall be based on the announcements of each department.'},
	'note3'			=> {'c'=>'此畢業資格審查表需和新生修業規定配合使用，如果對查詢結果有任何疑問請mail至 admytl\@ccu.edu.tw 。', 
						'e'=>'The qualification form for graduation shall be applied together with the provisions of study for
							new students. Please mail your questions to admytl@ccu.edu.tw, if any.'},
	'note4'			=> {'c'=>'軍訓為分項選修課程，是否得計入畢業學分，依各學系之規定。
							若得計入畢業學分者，其屬性為自由選修學分，每一學期各以一學分為限。', 
						'e'=>'Military training course is an elective course. Please consult the regulations of your department
							whether its credits can be included into the credits for graduation. If the credits are to be taking into account, then it is recognized as a free elective course. The maximum credit of free elective course for each semester is 1 credit.'},
	'note5'			=> {'c'=>'三、四年級體育為分項選修課程，是否得計入畢業學分，依各學系之規定。
							若得計入畢業學分者，其屬性為自由選修學分，每一學期各以一學分為限。', 
						'e'=>'Physical education course is an elective course for junior and senior students. Please consult the
							regulations of your department whether its credits can be included into the credits for graduation. If the credits are to be taking into account, then it is recognized as a free elective course. The maximum credit of free elective course for each semester is 1 credit.'},
	'note6'			=> {'c'=>'畢業資格審查表採用 PDF 格式, 若無法檢視請下載並安裝 Adobe Acrobat Reader。', 
						'e'=>'Qualification form for graduation is in PDF format. Please download and install Adobe Acrobat
							Reader if you are unable to open the file.'},
	'note7'			=> {'c'=>'畢業資格審查表暫存檔可能在十分鐘後被系統刪除, 
							若無法檢視請重新整理(reload)本頁.', 
						'e'=>'Qualification form for graduation would be deleted in 10 minutes. 
							Please reload the page if you could not see '},

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

