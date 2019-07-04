#!/usr/local/bin/perl

#########################################################################
#####  Print_Graduate_pdf2.cgi
#####  列印學生畢業資格審核 pdf 檔2 -- 確認畢業資格審查表
#####  擁有畢業資格審查表的學生, 必須先確認過, 才能進行加退選.
#####  
#####  在執行此程式同時記錄到 ~/DATA/LOGS/Student_Graduate_PDF.log 中, 以便之後查詢.
#####  Coder: Nidalap Leee
#####  Last Update: 2005/09/07
#########################################################################

print("Content-type:text/html\n\n");

require "../library/Reference.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
#require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."System_Settings.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Error_Message.pm";
#require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Session.pm";

my(%Student,%Dept);

%Input    = User_Input();
($Input{id}, $Input{password}, $login_time, $ip) = Read_Session($Input{session_id});
#print("session_id, id, pass = $Input{session_id}, $Input{id}, $Input{password}<BR>"); 

%system_settings = Read_System_Settings();
%Student  = Read_Student($Input{id});
#%Dept     = Read_Dept($Student{dept});
%time     = gettime();

Check_Student_Password($Input{id}, $Input{password});

$space = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";

Print_Header();

if( ($SUPERUSER==1) or ($system_settings{force_print_graduate_pdf}==1) ) {
#  print("check = $Input{check}<BR>\n");
  if( $Input{check} eq "on" ) {
    Confirm_For_Graduate_pdf($Input{id});
    Print_HTML(); 
  }else{
    Print_Please_Check();
#    print("not ok");
  }
#  print("hello!");
#  Delete_Old_PDF_File();
#  ($succeed_flag, $pdf_file) = Create_PDF_File($Input{id});
}else{
  Print_BAN();
}

#print("session_id = $Input{session_id}<BR>\n");
my($LINK)=Select_Course_Link($Input{id},$Input{password});
print("$LINK");
##############################################################################
sub Print_Header()
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
  );
} 
##############################################################################
sub Print_Please_Check()
{
  print("請勾選上一頁的 \"我已經看過我的畢業資格審查表了\"");
}
##############################################################################
sub Print_BAN()
{
  print("  畢業資格審查表目前不開放列印!<BR>");
}

##############################################################################

sub Print_HTML() 
{
#  Graduate_Log($Input{id});
#  Student_Log("Print2", $Input{id}, "", "", "");
#  print("flag = $succeed_flag<BR>\n");
   print qq(
      <TABLE border=0>
        <TR><TD align=CENTER>
          &nbsp<P>
          &nbsp<P>
          您已經確認過畢業資格審查表, 現在可以進行加退選了
          <P>
          &nbsp<P>
          &nbsp<P>
        </TD></TR>
        <TR><TD>
          <FONT size=-1>
          <FONT color=RED>
          <LI>畢業學分歸屬有問題, 請與系上連絡;
              輔系,雙主修學分歸屬有問題,請與申請學系連絡.
          <LI>此系統目前僅供查詢參考，仍需以新生修業規定為準；
              應屆畢業生之畢業資格審查結果應以各學系公告為主。
          <LI>此畢業資格審查表需和新生修業規定配合使用，如果對查詢結果有任何疑問
              請mail至 <A href="mailto:admytl\@ccu.edu.tw">admytl\@ccu.edu.tw</A>
          </FONT>
        </TD></TR>
      </TABLE>
   );
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
  
