#!/usr/local/bin/perl

$IN = "name_list2.txt";
$OUT = "select_course2.html";

open(IN, $IN);
open(OUT, ">$OUT");
@lines = <IN>;

print OUT qq(
  <HTML><BODY background="http://kiki.ccu.edu.tw/bk.jpg">
    <CENTER><H1>��ܬd�ݶW�B���</H1><HR>
    <TABLE border=1>
     <TR><TD>���</TD><TD>��إN�X</TD><TD>�Z�O</TD><TD>��ئW��</TD></TR>
);

$i = 0;
foreach $line (@lines) {
  $line =~ s/\n//;
  ($id, $name, $j, $dept, $c_id, $group, $cname) = split(/\s+/, $line);
  if( ($last_cid ne $c_id) or ($last_grp ne $group) ) {
    Print_cell();
  }
  $last_cid = $c_id;
  $last_grp = $group;
}

print OUT ("</TABLE>");

############################################################################
sub Print_cell()
{
  print OUT qq(<TR><TD align=center>
       <A
href="http://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/Feb21/Show_Course.cgi?id=$c_id&group=$group">��</A></TD>
       <TD>$c_id</TD><TD>$group</TD><TD>$cname</TD></TR>\n);
}