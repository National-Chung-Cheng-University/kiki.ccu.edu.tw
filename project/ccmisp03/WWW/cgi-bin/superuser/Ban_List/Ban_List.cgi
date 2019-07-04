#!/usr/local/bin/perl
##########################################################################
#####   Ban_List.cgi
#####   停權名單
#####   由於加選次數太多而遭停權的名單
#####   Coder: Nidalap :D~
#####   Date : 2005/05/03
##########################################################################
print("Content-type:text/html\n\n");
require "../../library/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Password.pm";
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
$table_content = Form_Ban_List_Table();

print qq(
  <HTML>
    <HEAD><TITLE>停權名單</TITLE></HEAD>
    <BODY background="$GRAPH_URL./manager.jpg">
      <Center><H1>停權名單<hr></h1>
      目前停權名單:
      <FORM action="Course_Upper_Limit_Immune02.cgi" method=POST>
        <INPUT type="hidden" name="password" value="$Input{password}">
        <INPUT type="hidden" name="action" value="delete">
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
        <!INPUT type="submit" value="刪除該筆資料">
      </FORM>
    </BODY>
  </HTML>
);
################################################################################

sub Form_Ban_List_Table()
{
  my(@files, $ban_file, @lines, $content, $bancount);
  my($bantime1, $bantime, $id, $ip, $res_time, %student, %dept);
  
  opendir(BANPATH, $BAN_LIST_PATH);
  @files = readdir(BANPATH);
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
    if($res_time <= 0) {
      $res_time = "(NONE)";
    }else{
      $res_time = "<FONT color=RED>" . $res_time . "</FONT>";
    }
      
    $content .= "<TR><TD>$id</TD><TD>$student{name}</TD><TD>$dept{cname2} $student{grade} 年級</TD><TD>$bantime</TD><TD>$res_time</TD><TD>$bancount</TD></TR>";
#    print("$file<BR>\n");
  }

  closedir(BANPATH);
  return($content);
}
