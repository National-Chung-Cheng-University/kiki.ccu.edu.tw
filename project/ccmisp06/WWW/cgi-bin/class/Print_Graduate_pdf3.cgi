#!/usr/local/bin/perl

#########################################################################
#####  Print_Graduate_pdf3.cgi
#####  列印學生畢業資格審核 pdf 檔, 提供教師專業系統連結過來看.
#####  本程式由 Print_Course_pdf.cgi 修改而成.
#####  
#####  在執行此程式同時記錄到 ~/DATA/LOGS/Student_Graduate_PDF.log 中, 以便之後查詢.
#####  Coder: Nidalap Leee
#####  Last Update: 
#####   2008/01/15 由 Print_Course_pdf.cgi 修改而成，提供教師專業系統連結過來看。
#####   2010/11/04 新增驗證碼 key 以避免使用者隨便看任何學生的資料(修改 Password.pm)。  Nidalap :D~
#####   2015/01/20 除了原本的教專系統外，亦開放課程地圖系統連結過來看。  Nidalap :D~
####################################################################################################

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

%Input			= User_Input();
$id				= $Input{id};
$in_key			= $Input{key};
$in_timestamp	= $Input{key1};
$call_system	= defined($Input{call_system}) ? $Input{call_system} : "teacher";
$password = "";

####  各個連過來的系統使用不同的 seed 產生 key
%key_seeds = ("teacher"		=> "bOsSlesSLESswORK", 
              "coursemap"	=> "thISisfORCoursEMaP");
$key_seed = $key_seeds{$call_system};
#$key_seed = $key_seeds{"coursemap"};

$key = Generate_Key2($id, $key_seed, $in_timestamp);

#print("[id, key, key_seed, key1, call_system] = [$id, $key, $key_seed, $in_timestamp, $call_system]...<BR>\n");
#Check_Key($key, $id, $password);

#($Input{id}, $Input{password}, $login_time, $ip) = Read_Session($Input{session_id}, "", 1);
#print("session_id, id, pass = $Input{session_id}, $Input{id}, $Input{password}<BR>"); 

%system_settings = Read_System_Settings();
%Student  = Read_Student($Input{id});
#%Dept     = Read_Dept($Student{dept});
%time     = gettime();

#Check_Student_Password($Input{id}, $Input{password});

$space = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";

if( Check_HTTP_REFERER() == 1 ) {
  if( $key eq $in_key ) {
    Delete_Old_PDF_File();
    ($succeed_flag, $pdf_file) = Create_PDF_File($Input{id});
    Print_HTML($succeed_flag, $pdf_file);
  }else{
    Print_BAN("key_error");
  }
}else{
  Print_BAN();
}

##############################################################################
sub Print_BAN()
{
  my($msg) = @_;
  if( $msg eq "key_error" ) {
    $msg_show = "驗證碼錯誤，<FONT color=RED>請回上一頁重新讀取</FONT>，以更新驗證碼！";
  }else{
    $msg_show = "畢業資格審查表目前不開放列印!";
  }
  
  print qq(
    <html>
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <TITLE>畢業資格審查表($Student{name})</TITLE>
    </head>
    <body background="$GRAPH_URL./ccu-sbg.jpg">
    <center>
      <FONT face="標楷體">
        <H1>國立中正大學教務系統</H1>
      </FONT>
    <HR>
    $msg_show<BR>
  );
}

##############################################################################

sub Print_HTML() 
{
  my($succeed_flag, $pdf_file) = @_;
  
  Graduate_Log($Input{id});
#  Student_Log("Print2", $Input{id}, "", "", "");

  $redirect_tag = "";
  if( $succeed_flag == 1 ){ 
    $redirect_tag = "<meta http-equiv=\"refresh\" content=\"0;url=$pdf_file\">";
  }
  print qq(
  <html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    $redirect_tag
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
#    foreach $key (keys %ENV) {
#      print("env{$key} = $ENV{$key}<BR>\n");
#    }
    print qq(
      <HR>
      &nbsp;<P>
      &nbsp;<P>
      請稍後, 資料讀取中...
      <P>
      如果此網頁沒有反應, 請點選<A href="$pdf_file">此連結</A>
      &nbsp;<P>
      &nbsp;<P>
    );
  }else{
    print qq(
     <HR>
     <P>
      查無此同學的畢業資格審查表資料.<BR>
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
  print LOG_FILE ("$time{time_string} : $ip  : $id : $call_system $su\n");
  close(LOG_FILE);
}
##########################################################################
