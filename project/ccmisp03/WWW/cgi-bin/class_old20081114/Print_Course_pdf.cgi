#!/usr/local/bin/perl

#########################################################################
#####  Print_Course_pdf.cgi
#####  �C�L�ǥͿ�ҵ��G��
#####  ���{�����P�� Print_Course.cgi, �b�󥻵{����ܪ��O�ǥͿ�ҳ� pdf ��,
#####  �� 92_2 �_, �ǥͥi�H�����C�L��ҳ�ñ�Wú�^, �ǥͦb�u�W�i�ݨ� pdf ��.
#####  
#####  �b���榹�{���P�ɰO���� Student.log ��, �H�K����d��.
#####  Coder: Nidalap Leee
#####  Last Update: Feb 18,2000
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

if( ($SUPERUSER==1) or ($system_settings{allow_print_pdf}==1) ) {
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
      <TITLE>$SUB_SYSTEM_NAME ��ҵ��G��($Student{name})</TITLE>
    </head>
    <body background="$GRAPH_URL./ccu-sbg.jpg">
    <center>
      <FONT face="�з���">
        <H1>��ߤ����j��$SUB_SYSTEM_NAME�ǥͿ�Ҩt��<br>
        $YEAR�Ǧ~��$TERM_NAME  ��ҵ��G��</H1>
      </FONT>
    <HR>
    ��ҵ��G��ثe���}��C�L!<BR>
  );
}

##############################################################################

sub Print_HTML() 
{
  my($succeed_flag, $pdf_file) = @_;
  
  Student_Log("Print2", $Input{id}, "", "", "");
  print qq(
  <html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <TITLE>$SUB_SYSTEM_NAME ��ҵ��G��($Student{name})</TITLE>
  </head>
  <body background="$GRAPH_URL./ccu-sbg.jpg">
    <center>
      <FONT face="�з���">
        <H1>��ߤ����j��$SUB_SYSTEM_NAME�ǥͿ�Ҩt��<br>
        $YEAR�Ǧ~��$TERM_NAME  ��ҵ��G��</H1>
      </FONT>
  );
#  print("flag = $succeed_flag<BR>\n");
  if( $succeed_flag == 1 ) {
    print qq(
      <HR>
      <P>
      &nbsp<P>
      ���I���˵�<A href="$pdf_file" target=NEW>��ҵ��G��</A>
      <P>
      &nbsp<P>
      <FONT size=-1>
      <LI>��ҵ��G��ĥ� pdf �榡, �Y�L�k�˵��ФU���æw��
        <A href="http://download.adobe.com/pub/adobe/acrobatreader/win/5.x/5.1/AcroReader51_CHT_full.exe"> 
        Adobe Acrobat Reader</A>
      <LI>��ҵ��G��Ȧs�ɥi��b�Q������Q�t�ΧR��, �Y�L�k�˵��Э��s��z(reload)����.
    );
  }else{
    print qq(
     <HR>
     <P>
      �]���z���Ǵ������, �d�L�z����ҵ��G��.<BR>
      �Y�z���Ǵ����T�����,  �Ь��q�⤤��(����14203)!
    );
  }
}


############################################################################
sub Create_PDF_File()
{
  my($succeed_flag, $pdf_source, $pdf_temp_path, $pdf_dest, $pdf_url);
  
  my($id) = @_;
  $id =~ /^(......)/;
  
  $pdf_source = $DATA_PATH . "PDF_files/" . $1 . "/" . $id . "_" . $YEAR . $TERM . ".pdf";

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

