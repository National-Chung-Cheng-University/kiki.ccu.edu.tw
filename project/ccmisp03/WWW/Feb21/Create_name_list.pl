#!/usr/local/bin/perl

$IN = "name_list.txt";
$OUT = "name_list.html";

open(IN, $IN);
open(OUT, ">$OUT");
@lines = <IN>;

print OUT qq(
  <HTML><BODY background="http://kiki.ccu.edu.tw/bk.jpg">
    <CENTER><H1>�h��W��</H1><HR>
    �H�U��ҰO�����]�W�B�ӳQ�h��. 
    �H�U�W��̾Ǹ��Ƨ�, �Y�n�M��S�w�Ǹ��п�JCtrl-F�ÿ�J�Ǹ�
    <TABLE border=1>
     <TR><TD>�Ǹ�</TD><TD>��إN�X</TD><TD>�Z�O</TD><TD>��ؤ���W��</TD></TR>
);

foreach $line (@lines) {
  $line =~ s/\n//;
  ($id, $name, $j, $dept, $c_id, $group, $cname) = split(/\s+/, $line);
  print OUT ("  <TR><TD>$id</TD><TD>$c_id</TD><TD>$group</TD><TD>$cname</TD></TR>\n");
}




print OUT ("</TABLE>");