#!/usr/local/bin/perl

require "../../library/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Password.pm";
require $LIBRARY_PATH . "Error_Message.pm";

print("Content-type:text/html\n\n");  

my(%Input);
%Input=User_Input();

 $su_flag = Check_SU_Password($Input{password}, "su");
 if( $su_flag ne "TRUE" ) {
   print("Password check error! system logged!!\n");
   exit(1);
 }

$file = $LOG_PATH . "Update.log";
open(FILE, $file);
@lines = <FILE>;

print qq(
  <BODY background="../../../Graph/manager.jpg">

  <CENTER>
  <H1>系統參考資料更新 LOG 紀錄檔</H1>
  <TABLE border=1 width=100%>
    <TR bgcolor=ORANGE><TH>時間</TH><TH>更新項目</TH><TH>資料筆數</TH><TH>耗用時間(秒)</TH></TR>
);
foreach $line (@lines) {
  ($date, $target, $count, $used_time) = split(/\t/, $line);
  print qq(
    <TR><TD>$date</TD><TD>$target</TD><TD>$count</TD><TD>$used_time</TD></TR>
  );
}
print qq(
  </TABLE>
);

close(FILE);

