#!/usr/local/bin/perl

print("Content-type:text/html\n\n");
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Student.pm";

%Input = User_Input();
#%student = Read_Student($Input{id});
print qq(
  <HEAD><TITLE>�ǥͥ[�h��log�O�����</TITLE></HEAD>
  <BODY background="$GRAPH_URL//ccu-bg.jpg">
    <CENTER>
      <H1>�ǥͥ[�h��log�O�����</H1><HR>
      �d�߱���: $Input{value}<BR>\n
);

$log_file = $DATA_PATH . "Student.log";
my $tmpfile = "/tmp/Student.log.grep";
system("grep $Input{value} $log_file > $tmpfile");

open(TMP, $tmpfile);
@line = <TMP>;
close(TMP);
unlink $tmpfile;
print("<TABLE border=1>");
print("<TR><TD>�Ǹ�</TD><TD>�ʧ@</TD><TD>���</TD><TD>�ӷ�</TD><TD>��إN�X</TD><TD>�Z�O</TD><TD>�ݩ�</TD><TD>�޲z��</TD>\n");
foreach $line (@line) {
  $su = "";
  $hit = 0;
  if($line =~ /SU/) {
    $su = "�O";
    $line =~ s/SU//;
  }
  ($action,$day,$ip,$id,$course,$group,$property) = split(/\s:\s/,$line);
  $ip =~ s/\s//;
  $action="�[��"       if($action =~ /Add/);
  $action="�h��"       if($action eq "Delete");
  $action="�C�L��ҳ�" if($action =~ /Print/);
  
  print("<TR><TD>$id</TD><TD>$action</TD><TD>$day</TD><TD>$ip</TD><TD>$course</TD><TD>$group</TD><TD>$property</TD><TD>$su</TD></TR>");
}
print("</TABLE>");
