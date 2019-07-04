#!/usr/local/bin/perl
print("Content-type:text/html\n\n");

require "../library/Reference.pm";
require $LIBRARY_PATH."Dept.pm";

my($FileName) = $REFERENCE_PATH."All_Changed_Data";
open(ALLDATA,"<$FileName") or
                              die("Cannot open file $FileName!\n");
  @LINES=<ALLDATA>;
close(ALLDATA);

$Content="";
$Table_Content="";

%State=("A"=>"新增","C"=>"取消","U"=>"異動");

foreach $line(@LINES){
# print $line."<br>\n";
  @DATA = split(/###/,$line);

  %the_Dept = Read_Dept($DATA[0]);

  $Table_Content .= "<tr>\n";

  $Table_Content .= "<th><font size=1>".$the_Dept{cname2};
  $Table_Content .= $DATA[1]."</font></th>";
  $Table_Content .= "<th><font size=1>".$DATA[2]."</font></th>";
  $Table_Content .= "<th><font size=1>".$DATA[3]."</font></th>";
  $Table_Content .= "<th><font size=1>".$DATA[4]."</font></th>";
  $Table_Content .= "<th>&nbsp<font size=1>".$DATA[5]."</font></th>";
  $Table_Content .= "<th><font size=1>".$DATA[6]."</font></th>";
  $Table_Content .= "<th><font size=1>".$DATA[7]."</font></th>";
  $Table_Content .= "<th><font size=1>".$DATA[8]."</font></th>";
  $Table_Content .= "<th><font size=1>".$DATA[9]."</font></th>";
  $Table_Content .= "<th><font size=1>".$DATA[0]."</font></th>";
  $Table_Content .= "<th><font size=1>".$State{$DATA[11]}."</font></th>";
  $Table_Content .= "<th>&nbsp<font size=1>".$DATA[12]."</font></th>";
  $Table_Content .= "<th>&nbsp<font size=1>".$DATA[13]."</font></th>";
  $Table_Content .= "<th>&nbsp<font size=1>".$DATA[14]."</font></th>";
  $Table_Content .= "<th>&nbsp<font size=1>".$DATA[15]."</font></th>";

  $Table_Content .= "</tr>\n";
}

print << "END_OF_HTML"
  <HTML><HEAD><TITLE>檢視所有異動科目</TITLE></HEAD></HTML>
  <BODY background="$GRAPH_URL/ccu-sbg.jpg">
    <Center>
      <H1>檢視所有異動科目<hr></H1>
      <table width=800 border=1>
      <tr>
        <th bgcolor=#ffff00><font size=1>系所別</font></th>
        <th bgcolor=#ffff00><font size=1>科目代碼</font></th>
        <th bgcolor=#ffff00><font size=1>班別</font></th>
        <th bgcolor=#ffff00><font size=1>科目名稱</font></th>
        <th bgcolor=#ffff00><font size=1>教師</font></th>
        <th bgcolor=#ffff00><font size=1>上課時數</font></th>
        <th bgcolor=#ffff00><font size=1>學分</font></th>
        <th bgcolor=#ffff00><font size=1>選必</font></th>
        <th bgcolor=#ffff00><font size=1>時間</font></th>
        <th bgcolor=#ffff00><font size=1>地點</font></th>
        <th bgcolor=orange><font size=1>增|異|取消</font></th>
        <th bgcolor=orange><font size=1>教師</font></th>
        <th bgcolor=orange><font size=1>選必</font></th>
        <th bgcolor=orange><font size=1>時間</font></th>
        <th bgcolor=orange><font size=1>地點</font></th>
      </tr>
      $Table_Content
      </table>
    </Center>
  </BODY>
END_OF_HTML



