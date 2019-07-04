#!/usr/local/bin/perl

#########################################################################
#####  Print_Graduate_pdf.cgi
#####  列印學生畢業資格審核 pdf 檔
#####  本程式由 Print_Course_pdf.cgi 修改而成.
#####  
#####  在執行此程式同時記錄到 ~/DATA/LOGS/Student_Graduate_PDF.log 中, 以便之後查詢.
#####  2005/09/07 新增下一頁確認功能, 限制學生必須確認後才能選課
#####  Coder: Nidalap Leee
#####  Last Update: 2004/06/17
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

my(%Input,%Student,%Dept);

%Input    = User_Input();
($Input{id}, $Input{password}, $login_time, $ip) = Read_Session($Input{session_id});
#print("session_id, id, pass = $Input{session_id}, $Input{id}, $Input{password}<BR>"); 

%system_settings = Read_System_Settings();
%Student  = Read_Student($Input{id});
#%Dept     = Read_Dept($Student{dept});
%time     = gettime();

Check_Student_Password($Input{id}, $Input{password});

$space = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";

if( ($SUPERUSER==1) or ($system_settings{allow_print_graduate_pdf}==1) ) {
  Delete_Old_PDF_File();
  ($succeed_flag, $pdf_file) = Create_PDF_File($Input{id});
  Print_HTML($succeed_flag, $pdf_file);
}else{
  Print_BAN();
}
##############################################################################
sub Print_BAN()
{
  print qq(
    <html>
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=big5">
      <TITLE>畢業資格審查表($Student{name})</TITLE>
    </head>
    <body background="$GRAPH_URL./ccu-sbg.jpg">
    <center>
      <FONT face="標楷體">
        <H1>國立中正大學教務系統</H1>
      </FONT>
    <HR>
    畢業資格審查表目前不開放列印!<BR>
  );
}

##############################################################################

sub Print_HTML() 
{
  my($succeed_flag, $pdf_file) = @_;
  
  Graduate_Log($Input{id});
#  Student_Log("Print2", $Input{id}, "", "", "");
  print qq(
  <html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <TITLE>畢業資格審查表($Student{name})</TITLE>
  </head>
  <body background="$GRAPH_URL./ccu-sbg.jpg">
    <center>
      <FONT face="標楷體">
        <H1>國立中正大學教務系統</H1>
      </FONT>
  );
#  print("flag = $succeed_flag<BR>\n");
  if( $succeed_flag == 1 ) {
    print qq(
      <HR>
      <TABLE border=0>
        <TR><TD align=CENTER>
          &nbsp<P>
          &nbsp<P>
          請點選檢視<A href="$pdf_file" target=NEW>畢業資格審查表</A>
          <P>
    );
    if( ($SUPERUSER==1) or ($system_settings{force_print_graduate_pdf}==1) ) {
      print qq(
          <FORM action="Print_Graduate_pdf2.cgi" method=POST>
            <INPUT type=checkbox name=check>
            <INPUT type=hidden name=session_id value=$Input{session_id}>
            我已經看過我的畢業資格審查表了
            <INPUT type=SUBMIT value="確認">
          </FORM>
      );
    }
    print qq(
          &nbsp<P>
          &nbsp<P>
        </TD></TR>
        <TR><TD>
<LI>畢業資格審查表為PDF檔無法即時更新，更新時間為第二階段加退選與期中考試前，
    每學期更新兩次。 

<LI>此畢業資格審查表僅供查詢參考，仍需以新生修業規定為準；
    應屆畢業生之畢業資格審查結果應以各學系公告為主。 

<LI>此畢業資格審查表需和新生修業規定配合使用，
    如果對查詢結果有任何疑問 請mail至 admytl@ccu.edu.tw 。

<LI>軍訓為分項選修課程，是否得計入畢業學分，依各學系之規定。
    若得計入畢業學分者，其屬性為自由選修學分，每一學期各以一學分為限。

<LI>三、四年級體育為分項選修課程，是否得計入畢業學分，依各學系之規定。
    若得計入畢業學分者，其屬性為自由選修學分，每一學期各以一學分為限。

<LI>畢業資格審查表採用 pdf 格式, 若無法檢視請下載並安裝 Adobe 
    <A href="http://download.adobe.com/pub/adobe/acrobatreader/win/5.x/5.1/AcroReader51_CHT_full.exe"
    target=NEW>Acrobat Reader</A>。

<LI>畢業資格審查表暫存檔可能在十分鐘後被系統刪除, 
    若無法檢視請重新整理(reload)本頁.
        </TD></TR>
      </TABLE>
    );
  }else{
    print qq(
     <HR>
     <P>
      查無您的畢業資格審查表資料.<BR>
      請洽教務處教學組!
    );
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
  
