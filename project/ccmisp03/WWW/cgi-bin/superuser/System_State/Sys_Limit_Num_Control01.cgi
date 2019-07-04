#!/usr/local/bin/perl

####    require these .pm modual    ####
require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
########################################

######### Main Program Here #########
my(%Input);
%Input=User_Input();



  $StateMap[0]="�t�Τ�����";
  $StateMap[1]="�Ҽ{�O�d�H��";
  $StateMap[2]="�ȦҼ{���פH��";
  $DATA="";

Modify_Sys_State();
$state=Catch_Sys_State();
$DATA=Creat_Table_DATA($state);
CREAT_HTML($DATA);

######################################
sub CREAT_HTML
{
my($DATA)=@_;
print << "End_of_HTML"
Content-type: text/html


<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <title> ��Ҩt�Ϊ��A�]�w�� </title>

<style>
        <!--
        A  {
           text-decoration: none;
           color:#0070A6
        }
        -->
</style>
</script>
</head>
<body bgcolor=white text=#666666>
<center>
<font size=5 color=#777777> �ǥͿ�Ҩt�Ϊ��A�]�w</font>
<hr size=1>

<table border=1 width=640>
<tr>
  <th bgcolor=#00ffff><font color=blue>�t�Ϊ��A</font></th>
  <th bgcolor=#00ffff><font color=blue>����</font></th>
</tr>
$DATA
</table>
<br>
<hr size=1>
<a href="javascript:history.back()">�^�W�@��</a>
</center>
</body>
</html>
End_of_HTML
}

################################################

sub Modify_Sys_State
{
  my($FileName)=$REFERENCE_PATH."Basic/LimitNumberState";

  open(STATE,">$FileName");
    print STATE $Input{State};
  close(STATE);
}

sub Catch_Sys_State
{
  my($FileName)=$REFERENCE_PATH."Basic/LimitNumberState";
  my(@data)="";
  my(@StateMap);


  if(-e $FileName){
    open(STATE,"<$FileName");
      @data=<STATE>;
    close(STATE);
  }else{
    die("Couldn't open the file $FileName!\n");
  }

  return($data[0]);
}

sub Creat_Table_DATA
{
  my($S)=@_;
  $TD="";

  if($S == 0){

  $TD .= "<tr>\n";
  $TD .= "  <th align=left>".$StateMap[$S]."</th>\n";
  $TD .= "  <td>\n";
  $TD .= "    <ul>\n";
  $TD .= "      <li><font color=blue>�i�[��H�ơG</font><font color=#dd2222>������H��</font>\n";
  $TD .= "      <li><font color=blue>�ϥήɾ��G</font><font color=#dd2222>�¥ͪ��I��e</font>\n";
  $TD .= "    </ul>\n";
  $TD .= "  </td>\n";
  $TD .= "</tr>\n";

  }elsif($S == 1){

  $TD .= "<tr>\n";
  $TD .= "  <th align=left>".$StateMap[$S]."</th>\n";
  $TD .= "  <td>\n";
  $TD .= "    <ul>\n";
  $TD .= "      <li><font color=blue>�i�[��H�ơG</font><font color=#dd2222>���פH��-�O�d�H��</font>\n";
  $TD .= "      <li><font color=blue>�ϥήɾ��G</font><font color=#dd2222>�¥ͪ��I��ܷs�ͪ��e</font>\n";
  $TD .= "    </ul>\n";
  $TD .= "  </td>\n";
  $TD .= "</tr>\n";


  }elsif($S == 2){

  $TD .= "<tr>\n";
  $TD .= "  <th align=left>".$StateMap[$S]."</th>\n";
  $TD .= "  <td>\n";
  $TD .= "    <ul>\n";
  $TD .= "      <li><font color=blue>�i�[��H�ơG</font><font color=#dd2222>���פH��</font>\n";
  $TD .= "      <li><font color=blue>�ϥήɾ��G</font><font color=#dd2222>�s�ͪ��I���</font>\n";
  $TD .= "    </ul>\n";
  $TD .= "  </td>\n";
  $TD .= "</tr>\n";
  }
  return($TD);
}
