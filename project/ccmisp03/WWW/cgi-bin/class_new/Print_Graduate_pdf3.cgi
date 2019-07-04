#!/usr/local/bin/perl

#########################################################################
#####  Print_Graduate_pdf3.cgi
#####  �C�L�ǥͲ��~���f�� pdf ��, ���ѱЮv�M�~�t�γs���L�Ӭ�.
#####  ���{���� Print_Course_pdf.cgi �ק�Ӧ�.
#####  
#####  �b���榹�{���P�ɰO���� ~/DATA/LOGS/Student_Graduate_PDF.log ��, �H�K����d��.
#####  Coder: Nidalap Leee
#####  Last Update: 2008/01/15
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
$id = $Input{id};
$password = "";

#$key2 = Generate_Key($id, "");
#$key = $key2;
#print("key = $key<BR>");
#print("key2 = $key2<BR>");
#Check_Key($key, $id, $password);

#($Input{id}, $Input{password}, $login_time, $ip) = Read_Session($Input{session_id});
#print("session_id, id, pass = $Input{session_id}, $Input{id}, $Input{password}<BR>"); 

%system_settings = Read_System_Settings();
%Student  = Read_Student($Input{id});
#%Dept     = Read_Dept($Student{dept});
%time     = gettime();

#Check_Student_Password($Input{id}, $Input{password});

$space = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";

if( Check_HTTP_REFERER() == 1 ) {
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
      <TITLE>���~���f�d��($Student{name})</TITLE>
    </head>
    <body background="$GRAPH_URL./ccu-sbg.jpg">
    <center>
      <FONT face="�з���">
        <H1>��ߤ����j�ǱаȨt��</H1>
      </FONT>
    <HR>
    ���~���f�d��ثe���}��C�L!<BR>
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
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    $redirect_tag
    <TITLE>���~���f�d��($Student{name})</TITLE>
  </head>
  <body background="$GRAPH_URL./ccu-sbg.jpg">
    <center>
      <FONT face="�з���">
        <H1>��ߤ����j�ǱаȨt��</H1>
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
      �еy��, ���Ū����...
      <P>
      �p�G�������S������, ���I��<A href="$pdf_file">���s��</A>
      &nbsp;<P>
      &nbsp;<P>
    );
  }else{
    print qq(
     <HR>
     <P>
      �d�L���P�Ǫ����~���f�d����.<BR>
      �Ь��аȳB�оǲ�!
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
    if( $time_diff > 600 ) {                ###  �ɮצs�b�W�L�Q����
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
  
