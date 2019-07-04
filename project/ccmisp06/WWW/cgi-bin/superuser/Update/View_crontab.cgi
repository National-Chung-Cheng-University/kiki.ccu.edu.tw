#!/usr/local/bin/perl

require "../../library/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Password.pm";
require $LIBRARY_PATH . "Error_Message.pm";

print("Content-type:text/html\n\n");  

print $EXPIRE_META_TAG;
my(%Input);
%Input=User_Input();

 $su_flag = Check_SU_Password($Input{password}, "su");
 if( $su_flag ne "TRUE" ) {
   print("Password check error! system logged!!\n");
   exit(1);
 }

$file = $HOME_PATH . "BIN/Cron_jobs/cron_jobs";
open(FILE, $file);
@lines = <FILE>;

print qq(
  <BODY background="../../../Graph/manager.jpg">

  <CENTER>
  <H1>Crontab 自動執行參考檔</H1>
  <TABLE border=1 width=100%>
    <TR><TD><FONT size=2>
);
foreach $line (@lines) {
  if( $line =~ /^#/ ) {
    print("<FONT color=GREEN>$line</FONT><BR>\n");
  }else{ 
    print("$line<BR>\n");
  }
}
print qq(
    </TD></TR>
  </TABLE>
);

close(FILE);

