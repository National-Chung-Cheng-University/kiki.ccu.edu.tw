#!/usr/local/bin/perl
######################################################################################################
#####  Login.cgi
#####  �}�ҵn�J����
#####  Updates:
#####    ????/??/??
#####    2009/06/04  �� Find_All_Dept �[�W "NO_COM_DEPT" �ѼơA�uŪ���i�H�}�Ҫ��t�� Nidalap :D~
######################################################################################################
print "Content-type: text/html","\n\n";

require "../library/Reference.pm";
require $LIBRARY_PATH."Dept.pm";

print "
<html>
<head>
<title>��ߤ����j�� $SUB_SYSTEM_NAME�}�ƽҨt��</title>
</head>
<body background=".$GRAPH_URL."ccu-sbg.jpg>
<center>
<h1>";
print "
<img src=".$GRAPH_URL."open.jpg>
</h1>
<p><font size=4><blink>
";
print"</blink></font>";
print"<h4>�w��ϥ�<i>��ߤ����j��$SUB_SYSTEM_NAME�}�ƽҨt��</i></h4><p>
<h4>�ж�J�H�U�򥻸��</h4><p><br>

<form method=post action=Class_Menu.cgi>
<table border=0>
<tr>
<th><h3>�t�O:</h3></th><td><select name=dept_cd>";
my(@Dept,$dept,%Dept);

@Dept=Find_All_Dept("NO_COM_DEPT");

$last_college = "";
foreach $dept (@Dept)
{
  %Dept=Read_Dept($dept);
  if( is_GRA() == 1 ) {
    next if( $dept !~ /6$/ );
  }
#  next if( $Dept{cname2} =~ /�Ӥh�Z/ );
#  if( ($last_college ne $Dept{college}) and ($last_college ne "") ) {
#    print qq[<option value="dilimiter">------(���j�u�A�ſ�)------\n];
#  }
#  if( $Dept{cname2} =~ /�Ӥh�Z/ ) {
#    next;
#    print("<option value=$Dept{id}>* $Dept{cname2}\n"); 
#  }else{
#    $last_college = $Dept{college};
    print("<option value=$Dept{id}>$Dept{cname2}\n");
#  }
#  print "<option value=$Dept{id}>$Dept{cname}\n";
}

#print "<option value=\"sys\">Sys Manager";

print "
</select>
</td>
</tr>
<tr>
<th><h3>�K�X:</h3></th><td><input type=password name=password></td>
</tr>
</table>
<input type=\"submit\" value=\"��ƶ�g����\">
<input type=\"reset\" value=\"���s��g���\">

</form>
<p>

<img src=".$GRAPH_URL."net4.jpg>
<i>
�j�P��ĳ�ϥ�Netscape4.x�H�W�������s����
</i>
</center>
</body>
</html>
";
