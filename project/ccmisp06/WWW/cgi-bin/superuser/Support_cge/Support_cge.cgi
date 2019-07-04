#!/usr/local/bin/perl

#################################################################
#####  Support_cge.cgi
#####  維護通識次領域代碼資料
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
      <HEAD><TITLE>通識領域資料維護</TITLE></HEAD>
      <BODY background="$GRAPH_URL/bk.jpg">
        <CENTER>
        <H1>通識領域資料維護</H1><HR>
        <TABLE border=1>
          <TR><TH>通識次領域代碼</TH><TH>所屬主領域</TH><TH>名稱</TH></TR>
  );
  foreach $cge (sort keys %cge) {
    print("<TR><TD>$f1$cge</TD><TD>$f1$cge{$cge}{cge_id}</TD><TD>$f1$cge{$cge}{cge_name}</TD></TR>\n");
  }
  print qq(
        </TABLE>
      <FORM method="POST" action="Support_cge.cgi">
        通識次領域代碼: <INPUT name="sub_cge_id">  名稱:<INPUT name="cge_name"><P>
        <INPUT name="reload" type=SUBMIT value="重新讀取">
        <INPUT name="add" type=SUBMIT value="新增">
        <INPUT name="delete" type=SUBMIT value="刪除">
        <INPUT name="modify" type=SUBMIT value="修改">
      </FORM>
  );
}
#################################################################
sub Add_cge()
{
  if( defined($cge{$id}) ) {
    print("代碼已經存在!");
  }elsif( ($id eq "")or($name eq "") ) {
    print("請輸入代碼及名稱!!<br>\n");
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
    print("代碼不存在, 無法刪除!");
  }elsif( ($id eq "") ) {
    print("請輸入代碼及名稱!!<br>\n");
  }elsif( $id eq "0" ) {
    print("代碼0內定為不支援, 無法修改!<BR>\n");
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
    print("代碼不存在, 無法修改!");
  }elsif( ($id eq "")or($name eq "") ) {
    print("請輸入代碼及名稱!!<br>\n");
  }elsif( $id eq "0" ) {
    print("代碼0內定為不支援, 無法修改!<BR>\n");
  }else{
    open(CGE, ">$CGE_FILE") or print("Fatal: Cannot open file > $CGE_FILE!<br>\n");
    $cge{$id}{cge_name} = $name;
    foreach $cge_id (sort keys %cge) {
      print CGE ("$cge_id\t$cge{$cge_id}{cge_name}\n");
    }
  }

}
#################################################################