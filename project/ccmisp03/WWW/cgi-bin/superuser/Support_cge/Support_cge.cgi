#!/usr/local/bin/perl

#################################################################
#####  Support_cge.cgi
#####  ���@�q�Ѧ����N�X���
#####  Coder: Nidalap
#####  Date : Nov04, 2000
#################################################################
print("Content-type: text/html\n\n");
require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Error_Message.pm";

my(%Input,%Student,%Dept);
%Input=User_Input();
$id = $Input{sub_cge_id};
$name = $Input{cge_name};
%cge = Read_Cge();
$CGE_FILE = $REFERENCE_PATH . "cge2.txt";

#foreach $k (keys %Input) {
#  print("$k -> $Input{$k}<br>\n");
#}

$f1 = "<FONT>";
#################################################################
if    ($Input{add} ne "") {
  Add_cge();
}elsif($Input{delete} ne "") {
  Delete_cge();
}elsif($Input{modify} ne "") {
  Modify_cge();
}
%cge = Read_Cge();
Show_HTML();
#################################################################
sub Show_HTML()
{
  print qq(
    <HTML>
      <HEAD><TITLE>�q�ѻ���ƺ��@</TITLE></HEAD>
      <BODY background="$GRAPH_URL/bk.jpg">
        <CENTER>
        <H1>�q�ѻ���ƺ��@</H1><HR>
        <TABLE border=1>
          <TR><TH>�q�Ѧ����N�X</TH><TH>���ݥD���</TH><TH>�W��</TH></TR>
  );
  foreach $cge (sort keys %cge) {
    print("<TR><TD>$f1$cge</TD><TD>$f1$cge{$cge}{cge_id}</TD><TD>$f1$cge{$cge}{cge_name}</TD></TR>\n");
  }
  print qq(
        </TABLE>
      <FORM method="POST" action="Support_cge.cgi">
        �q�Ѧ����N�X: <INPUT name="sub_cge_id">  �W��:<INPUT name="cge_name"><P>
        <INPUT name="reload" type=SUBMIT value="���sŪ��">
        <INPUT name="add" type=SUBMIT value="�s�W">
        <INPUT name="delete" type=SUBMIT value="�R��">
        <INPUT name="modify" type=SUBMIT value="�ק�">
      </FORM>
  );
}
#################################################################
sub Add_cge()
{
  if( defined($cge{$id}) ) {
    print("�N�X�w�g�s�b!");
  }elsif( ($id eq "")or($name eq "") ) {
    print("�п�J�N�X�ΦW��!!<br>\n");
  }else{
    open(CGE, ">$CGE_FILE") or print("Fatal: Cannot open file > $CGE_FILE!<br>\n");
    $cge{$id}{cge_name} = $name;
    foreach $cge_id (sort keys %cge) {
      print CGE ("$cge_id\t$cge{$cge_id}{cge_name}\n");
    }
  }
}
#################################################################
sub Delete_cge()
{
  if( not defined($cge{$id}) ) {
    print("�N�X���s�b, �L�k�R��!");
  }elsif( ($id eq "") ) {
    print("�п�J�N�X�ΦW��!!<br>\n");
  }elsif( $id eq "0" ) {
    print("�N�X0���w�����䴩, �L�k�ק�!<BR>\n");
  }else{
    open(CGE, ">$CGE_FILE") or print("Fatal: Cannot open file > $CGE_FILE!<br>\n");
    foreach $cge_id (sort keys %cge) {
      next if($id eq $cge_id);
      print CGE ("$cge_id\t$cge{$cge_id}{cge_name}\n");
    }
  }
}
#################################################################
sub Modify_cge()
{
  if( not defined($cge{$id}) ) {
    print("�N�X���s�b, �L�k�ק�!");
  }elsif( ($id eq "")or($name eq "") ) {
    print("�п�J�N�X�ΦW��!!<br>\n");
  }elsif( $id eq "0" ) {
    print("�N�X0���w�����䴩, �L�k�ק�!<BR>\n");
  }else{
    open(CGE, ">$CGE_FILE") or print("Fatal: Cannot open file > $CGE_FILE!<br>\n");
    $cge{$id}{cge_name} = $name;
    foreach $cge_id (sort keys %cge) {
      print CGE ("$cge_id\t$cge{$cge_id}{cge_name}\n");
    }
  }

}
#################################################################