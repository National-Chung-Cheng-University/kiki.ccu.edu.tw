#!/usr/local/bin/perl

$IN = "name_list.txt";
$OUT = "name_list.html";

open(IN, $IN);
open(OUT, ">$OUT");
@lines = <IN>;

print OUT qq(
  <HTML><BODY background="http://kiki.ccu.edu.tw/bk.jpg">
    <CENTER><H1>退選名單</H1><HR>
    以下選課記錄都因超額而被退選. 
    以下名單依學號排序, 若要尋找特定學號請輸入Ctrl-F並輸入學號
    <TABLE border=1>
     <TR><TD>學號</TD><TD>科目代碼</TD><TD>班別</TD><TD>科目中文名稱</TD></TR>
);

foreach $line (@lines) {
  $line =~ s/\n//;
  ($id, $name, $j, $dept, $c_id, $group, $cname) = split(/\s+/, $line);
  print OUT ("  <TR><TD>$id</TD><TD>$c_id</TD><TD>$group</TD><TD>$cname</TD></TR>\n");
}




print OUT ("</TABLE>");