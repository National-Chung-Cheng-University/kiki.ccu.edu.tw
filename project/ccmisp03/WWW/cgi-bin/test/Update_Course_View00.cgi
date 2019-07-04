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

%State=("A"=>"�s�W","C"=>"����","U"=>"����");

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
  <HTML><HEAD><TITLE>�˵��Ҧ����ʬ��</TITLE></HEAD></HTML>
  <BODY background="$GRAPH_URL/ccu-sbg.jpg">
    <Center>
      <H1>�˵��Ҧ����ʬ��<hr></H1>
      <table width=800 border=1>
      <tr>
        <th bgcolor=#ffff00><font size=1>�t�ҧO</font></th>
        <th bgcolor=#ffff00><font size=1>��إN�X</font></th>
        <th bgcolor=#ffff00><font size=1>�Z�O</font></th>
        <th bgcolor=#ffff00><font size=1>��ئW��</font></th>
        <th bgcolor=#ffff00><font size=1>�Юv</font></th>
        <th bgcolor=#ffff00><font size=1>�W�Үɼ�</font></th>
        <th bgcolor=#ffff00><font size=1>�Ǥ�</font></th>
        <th bgcolor=#ffff00><font size=1>�沈</font></th>
        <th bgcolor=#ffff00><font size=1>�ɶ�</font></th>
        <th bgcolor=#ffff00><font size=1>�a�I</font></th>
        <th bgcolor=orange><font size=1>�W|��|����</font></th>
        <th bgcolor=orange><font size=1>�Юv</font></th>
        <th bgcolor=orange><font size=1>�沈</font></th>
        <th bgcolor=orange><font size=1>�ɶ�</font></th>
        <th bgcolor=orange><font size=1>�a�I</font></th>
      </tr>
      $Table_Content
      </table>
    </Center>
  </BODY>
END_OF_HTML



