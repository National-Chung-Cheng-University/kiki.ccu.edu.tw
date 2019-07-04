#!/usr/local/bin/perl

#########################################################################
#####  Print_Course_pdf.cgi
#####  列印學生選課結果單
#####  本程式不同於 Print_Course.cgi, 在於本程式顯示的是學生選課單 pdf 檔,
#####  自 92_2 起, 學生可以不必列印選課單簽名繳回, 學生在線上可看到 pdf 檔.
#####  
#####  在執行此程式同時記錄到 Student.log 中, 以便之後查詢.
#####  Coder: Nidalap Leee
#####  Updates: 
#####    2000/02/18 Created by Nidalap :D~
#####    2015/05/05 因應英文版做修改  by Nidalap :D~
#########################################################################

print("Content-type:text/html\n\n");

require "../library/Reference.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Select_Course.pm";
require $LIBRARY_PATH."System_Settings.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."English.pm";
require $LIBRARY_PATH."Session.pm";
require $LIBRARY_PATH."Display_Links.pm";

my(%Input,%Student,%Dept);

%Input    = User_Input();
($Input{id}, $Input{password}, $login_time, $ip) = Read_Session($Input{session_id}, "", 1);
#print("session_id, id, pass = $Input{session_id}, $Input{id}, $Input{password}<BR>"); 

%system_settings = Read_System_Settings();
%Student  = Read_Student($Input{id});
%Dept     = Read_Dept($Student{dept});
%time     = gettime();

%txt = Init_Text_Values();
Check_Student_Password($Input{id}, $Input{password});

if( $IS_ENGLISH ) {
  $HEAD_DATA = Head_of_Individual($Student{ename},$Student{id},$Dept{ename},$Student{grade},$Student{class});
}else{
  $HEAD_DATA = Head_of_Individual($Student{name},$Student{id},$Dept{cname},$Student{grade},$Student{class});
}

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
  print "
    <html>
    <head>
      <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
      <TITLE>" . $txt{'html_title'} . "</TITLE>
    </head>
    <body background='$GRAPH_URL./ccu-sbg.jpg'>
    <center>
      <FONT face='標楷體'>
        $HEAD_DATA<HR>
		<H1>" . $txt{'title'} . "</H1>
      </FONT>
    <HR>
    " . $txt{'not_allowed'} . "<BR>
  ";
}

##############################################################################

sub Print_HTML() 
{
  my($succeed_flag, $pdf_file) = @_;
  
  Student_Log("Print2", $Input{id}, "", "", "");
  print "
  <html>
  <head>
    <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
    <TITLE>" . $txt{'html_title'} . "</TITLE>
  </head>
  <body background='$GRAPH_URL/ccu-sbg.jpg'>
    <center>
      <FONT face='標楷體'>
        $HEAD_DATA<HR>
		<H1>" . $txt{'title'} . "</H1>
      </FONT>
  ";
#  print("flag = $succeed_flag<BR>\n");
  if( $succeed_flag == 1 ) {
    print "
      <HR>
      <P>
      &nbsp<P>
      " . $txt{'plz_click'} . "<A href='$pdf_file' target=NEW>" . $txt{'pdf'} . "</A>
      <P>
      &nbsp<P>
      <FONT size=-1>
      <LI>" . $txt{'note1'} . "
      <LI>" . $txt{'note2'} . "
    ";
  }else{
    print "
     <HR>
     <P>
       " . $txt{'not_avail'} . "<BR>
    ";
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
    if( $time_diff > 600 ) {                ###  檔案存在超過十分鐘
      unlink($file);
#      print("del: $file<BR>\n");
    }
#    print("$file -> $mtime, $time_diff<BR>\n");
  }  
}

##################################################################################
#####  因應英文版本，將所有要顯示的文字在此整理，依照 $IS_ENGLISH 自動判別  2015/05/05
sub Init_Text_Values
{
  my %txtall;
  
  %txtall = (
    'html_title'=> {'c'=>'選課結果單', 'e'=>'Course Selection Results Sheet'},
	'title'		=> {'c'=>'選課結果單', 'e'=>'Course Selection Results Sheet'},
	'not_avail'	=> {'c'=>'因為您本學期未選課, 或是選課單尚未產生, 目前查無您的選課結果單。', 
					'e'=>'You have not selected any course for this semester or the course selection results sheet is not generated yet, so the course selection result sheet is not available.'},
	'plz_click'	=> {'c'=>'請點選檢視', 'e'=>'Click here to view '},
	'pdf'		=> {'c'=>'選課結果單', 'e'=>'the course selection results sheet.'},
	'note1'		=> {'c'=>'選課結果單採用 PDF 格式, 若無法檢視請下載並安裝
					  <A href="http://download.adobe.com/pub/adobe/acrobatreader/win/5.x/5.1/AcroReader51_CHT_full.exe"> 
					  Adobe Acrobat Reader</A>', 
					'e'=>'The course selection result sheet is in PDF format, if you have trouble viewing it, please
					  install the 
					  <A href="http://download.adobe.com/pub/adobe/acrobatreader/win/5.x/5.1/AcroReader51_CHT_full.exe"> 
					  Adobe Acrobat Reader</A>'},
	'note2'		=> {'c'=>'選課結果單暫存檔可能在十分鐘後被系統刪除, 若無法檢視請重新整理(reload)本頁。', 
					'e'=>'The PDF file might be deleted by system in 10 minutes. If you cannot view it anymore, 
					  please reload this page.'},	
	
	'mark'		=> {'c'=>'標記', 'e'=>'Mark'}
  );

   
  foreach $k (keys %txtall) {
	if( $IS_ENGLISH ) {
	  $txt{$k} = $txtall{$k}{'e'};
	}else{
	  $txt{$k} = $txtall{$k}{'c'};
	  #print "$k -> " . $txt{$k} . "<BR>\n";
	}
  }
  
  return %txt;  
}
