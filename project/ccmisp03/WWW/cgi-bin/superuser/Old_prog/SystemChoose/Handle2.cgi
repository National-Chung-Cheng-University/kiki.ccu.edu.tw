#!/usr/local/bin/perl 

require "../../library/Reference.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."GetInput.pm";


%Change_School = Find_Change_School_Student();  ## 讀入轉學生名單

my($dept,$count,$i,$flag);

%Input = User_Input();
($course{dept},$course{id},$course{group},$course{cname})=split(/\s+/,$Input{course});

HTML_Head("查詢系統篩選結果--$course{cname}班別:$course{group}");

##HTML_Head();
HTML();


sub HTML
{
 print "<body background=$GRAPH_URL"."ccu-sbg.jpg>\n"; 
 print "<font size=4>";
 print "<hr>\n";
 print "<table border=0><tr><th>科目代碼:</th><th>$course{id}</th>\n";
 print "<th>科目班別:</th><th>$course{group}</th><th>科目名稱</th>\n";
 print "<th>$course{cname}</th></tr></table><hr>\n";
 Handle();
 Show_Page();
}

sub Handle
{
 my(@Lines,$i,$temp,$id,$grade,$flag,%s,$page);
 $LOG_PATH =$BIN_PATH."SystemChoose/Test";
 $page = $Input{page};
 if( $page eq "") { $page = 0; }
 $flag[0]="<font color=red>未選上</font>";
 $flag[1]="<font color=blue>選上</font>";

 if(-e $LOG_PATH."/$course{id}"."_$course{group}")
 {
  open(LOG,$LOG_PATH."/$course{id}"."_$course{group}");
   @Lines = <LOG>;
   chop(@Lines);
  close(LOG);
  $count = @Lines;
  $Lines[0]=~ /限修人數:(\d+)保留人數:(\d+) 通過篩選:(\d+) 最低選上權重:\d+ 選修人數:(\d+)/;
  print "限修人數:$1,保留人數:$2,通過篩選人數:$3,選修人數:$4<br>";
  print "<table width=100% border=0><tr>";
  for($i=1+$page*90;($i<$count && $i<=($page+1)*90);$i++)
  {
   ($id,$dept,$grade,$temp,$flag,$temp)=split(/\s+/,$Lines[$i]);
   if($i % 30 == 1)
   {
    print "<td valign=top><table border=1>\n";
    print "<tr><th>系所</th><th>學號</th><th>姓名</th><th>篩選</th></tr>\n";
   }
    %dept = Read_Dept($dept);
    %s = Read_Student($id);
    if($Change_School{$id} ne "1")
    {
     print "<tr><td>$dept{cname2}</td><td>$id</td><td>$s{name}</td><td>$flag[$flag]</td></tr>\n";
    }
    else
    {
     print "<tr><td>$dept{cname2}</td><td>$id</td><td bgcolor=yellow>$s{name}</td><td>$flag[$flag]</td></tr>";
    }
   if($i %30 == 0 || $i== $count-1)
   {
    print "</table></td>";
   }
  }

  print "</tr></table>";
 }
 else
 {
  print "Error opening file:$LOG_PATH"."/$course{id}"."_$course{group}\n";
 }
}

sub HTML_Head
{
 my($title);
 ($title)=@_;
 print "Content-type: text/html\n\n";
print "
<html>
<head>
 <meta http-equiv=\"Content-Type\" content=\"text/html; charset=big5\">
 <title>$title</title>
</head>";
}

sub Show_Page
{
 my($current_page);
 $current_page = $Input{page} + 1;
 for($total_pages=1;$total_pages*90 < ($count-1);$total_pages++)
 {}
 print "<br><hr>";
 print "目前為第<font size=4 color=brown>$current_page</font>頁,共<font color=blue size=4>$total_pages</font>頁<br>";

 if($total_pages > $current_page)
 {
   print "<form method=post action=Handle2.cgi>\n";
   print "<input type=hidden name=course value=\"$Input{course}\">";
   print "<input type=hidden name=page value=$current_page>";
   print "<input type=submit name=submit value=下一頁>\n";
   print "</form>\n";
 }
 if($current_page != 1)
 {
   $temp = $Input{page}-1;
   print "<form method=post action=Handle2.cgi>\n";
   print "<input type=hidden name=course value=\"$Input{course}\">";
   print "<input type=hidden name=page value=$temp>";
   print "<input type=submit name=submit value=上一頁>\n";
   print "</form>\n";
 }
 print "<br><a href=Handle.cgi>回到查詢系統篩選結果首頁</a><br>";
}