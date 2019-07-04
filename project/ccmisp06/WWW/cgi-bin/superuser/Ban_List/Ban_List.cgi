#!/usr/local/bin/perl
##########################################################################
#####   Ban_List.cgi
#####   停權名單
#####   由於加選次數太多而遭停權的名單
#####   Updates:
#####     2005/05/03 created by Nidalap :D~
#####     2009/02/25 增加三種排序功能 Nidalap :D~
##########################################################################
print("Content-type:text/html\n\n");
require "../../library/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Password.pm";
require $LIBRARY_PATH . "System_Settings.pm";
require $LIBRARY_PATH . "Student.pm";
require $LIBRARY_PATH . "Error_Message.pm";
require $LIBRARY_PATH . "Session.pm";

%Input = User_Input();
@dept = Find_All_Dept();

$pass_result = Check_SU_Password($Input{password}, "su", "su");
if($pass_result ne "TRUE") {
  print("密碼錯誤!");
  exit(1);
}
%sort_type = ("res_time"=>"剩餘時間", "bancount"=>"被停權次數", "id"=>"學號");
$Input{sort_type} = "id"  if($Input{sort_type} eq "");

$table_content = Form_Ban_List_Table();

print qq(
  <HTML>
    <HEAD>
      <TITLE>停權名單</TITLE>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    </HEAD>
    <BODY background="$GRAPH_URL./manager.jpg">
      <Center><H1>停權名單<hr></h1>
      目前停權名單(依照 <FONT color=RED>$sort_type{$Input{sort_type}}</FONT> 排序):
      <TABLE border=0>
        <TR><TD>
          <FORM action="Ban_List.cgi" method=POST>
            <INPUT type="hidden" name="password" value="$Input{password}">
            <INPUT type="hidden" name="sort_type" value="res_time">
            <INPUT type=submit value="以剩餘時間排序">
          </FORM>
        </TD><TD>
          <FORM action="Ban_List.cgi" method=POST>                   
            <INPUT type="hidden" name="password" value="$Input{password}">
            <INPUT type="hidden" name="sort_type" value="bancount">
            <INPUT type=submit value="以被停權次數排序">
          </FORM>
        </TD></TR>
      </TABLE>
      <TABLE border=1>
        <TR>
            <TH>學號</TH>
            <TH>姓名</TH>
            <TH>系所年級</TH>
            <TH>上次停權時間</TH>
            <TH>剩餘時間(分鐘)</TH>
            <TH>被停權次數(僅供參考)</TH>
        </TR>
        $table_content
      </TABLE>
    </BODY>
  </HTML>
);
################################################################################

sub Form_Ban_List_Table()
{
  my(@files, $ban_file, @lines, $content, $bancount);
  my($bantime1, $bantime, $id, $ip, $res_time, %student, %dept);
  my(@rec);
  
  opendir(BANPATH, $BAN_LIST_PATH);
  @files = readdir(BANPATH);
  my $i=0;
  foreach $file (sort @files) {
    next if( ($file eq ".") or ($file eq "..") );
    $ban_file = $BAN_LIST_PATH . $file;
    open(BANFILE, $ban_file);
    @lines = <BANFILE>;
    $bancount = 0;
    foreach $line (@lines) {
      $bancount++;
      ($bantime1, $bantime, $id, $ip) = split(/, /, $line);
    }
    close(BANFILE);
    %student = Read_Student($id);
    %dept = Read_Dept($student{dept});
    
#    $res_time = Read_Ban_Record($id, $BAN_COUNT_LIMIT);
    $res_time = Read_Ban_Record($id, 0);
    $res_time = int($res_time/60);

    $rec[$i]{'id'}		= $id;
    $rec[$i]{'ban_time'}	= $ban_time;
    $rec[$i]{'name'}		= $student{name};
    $rec[$i]{'dept_name'}	= $dept{cname2};
    $rec[$i]{'grade'}		= $student{grade};
    $rec[$i]{'ban_time'}	= $bantime; 
    $rec[$i]{'res_time'}	= $res_time;
    $rec[$i]{'bancount'}	= $bancount;

    $i++;
  }
  @rec = reverse sort {
    return ($$a{$Input{sort_type}} <=> $$b{$Input{sort_type}});
  } @rec;
  
  foreach $rec (@rec) {
    if($$rec{res_time} <= 0) {
      $$rec{res_time} = "(NONE)";
    }else{
      $$rec{res_time} = "<FONT color=RED>" . $$rec{res_time} . "</FONT>";
    }

    $content .= "<TR><TD>$$rec{id}</TD><TD>$$rec{name}</TD><TD>$$rec{dept_cname} $$rec{grade} 年級</TD>";
    $content .= "<TD>$$rec{ban_time}</TD><TD>$$rec{res_time}</TD><TD>$$rec{bancount}</TD></TR>";  
  }
  
  closedir(BANPATH);
  return($content);
}


