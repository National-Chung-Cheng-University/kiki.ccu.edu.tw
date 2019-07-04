#!/usr/local/bin/perl

print("Content-type:text/html\n\n");
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Student.pm";

%Input = User_Input();
#%student = Read_Student($Input{id});
print qq(
  <HEAD><TITLE>學生加退選log記錄資料</TITLE></HEAD>
  <BODY background="$GRAPH_URL//ccu-bg.jpg">
    <CENTER>
      <H1>學生加退選log記錄資料</H1><HR>
      查詢條件: $Input{value}<BR>\n
);

$log_file = $DATA_PATH . "Student.log";
my $tmpfile = "/tmp/Student.log.grep";
system("grep $Input{value} $log_file > $tmpfile");

open(TMP, $tmpfile);
@line = <TMP>;
close(TMP);
unlink $tmpfile;
print("<TABLE border=1>");
print("<TR><TD>學號</TD><TD>動作</TD><TD>日期</TD><TD>來源</TD><TD>科目代碼</TD><TD>班別</TD><TD>屬性</TD><TD>管理者</TD>\n");
foreach $line (@line) {
  $su = "";
  $hit = 0;
  if($line =~ /SU/) {
    $su = "是";
    $line =~ s/SU//;
  }
  ($action,$day,$ip,$id,$course,$group,$property) = split(/\s:\s/,$line);
  $ip =~ s/\s//;
  $action="加選"       if($action =~ /Add/);
  $action="退選"       if($action eq "Delete");
  $action="列印選課單" if($action =~ /Print/);
  
  print("<TR><TD>$id</TD><TD>$action</TD><TD>$day</TD><TD>$ip</TD><TD>$course</TD><TD>$group</TD><TD>$property</TD><TD>$su</TD></TR>");
}
print("</TABLE>");
