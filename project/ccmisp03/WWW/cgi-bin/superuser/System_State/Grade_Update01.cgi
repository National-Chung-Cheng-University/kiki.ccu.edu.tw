#!/usr/local/bin/perl

####    require these .pm modual    ####
require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
########################################

######### Main Program Here #########
my(%Input);
%Input=User_Input();

  $StateMap[0]="�]�w<font color=black><b>����</b></font>";
  $StateMap[1]="�]�w<font color=red><b>�}��</b></font>";
  $DATA="";

Modify_Grade_State();
$state=Catch_Grade_State();
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

sub Modify_Grade_State
{
  my($FileName)=$REFERENCE_PATH."Basic/GradeState";

  open(STATE,">$FileName");
    print STATE $Input{State};
  close(STATE);
}

sub Catch_Grade_State
{
  my($FileName)=$REFERENCE_PATH."Basic/GradeState";
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

  if($S eq 0){

  $TD .= "<tr>\n";
  $TD .= "  <td align=left> $StateMap[$S] </td>\n";
  $TD .= "  <td>\n";
  $TD .= "    <ul>\n";
  $TD .= "      <li>�]�w�����A�Ҧ��ϥΪ̦~��<font color=#ff079f>�Ҥ��ɯ�</font>\n";
  $TD .= "      <li>�ݤJ�Ƿs�͡A�¥ͦ~�ŧ�s�����ᥲ���N���]�w�����C\n";
  $TD .= "    </ul>\n";
  $TD .= "  </td>\n";
  $TD .= "</tr>\n";
  }elsif($S eq 1){

  $TD .= "<tr>\n";
  $TD .= "  <td align=left> $StateMap[$S] </td>\n";
  $TD .= "  <td>\n";
  $TD .= "    <ul>\n";
  $TD .= "      <li>�]�w�}�ҡA�Ҧ��ϥΪ̦~��<font color=#ff079f>�۰ʤɯ�</font>\n";
  $TD .= "      <li>��s�Ǧ~�}�l�e�ϥΡA�ت��b���¥ͦ~�Ŧ۰ʤɯšC\n";
  $TD .= "    </ul>\n";
  $TD .= "  </td>\n";
  $TD .= "</tr>\n";
  }elsif($S eq 2){

  $TD .= "<tr>\n";
  $TD .= "  <th align=left> �}��[�h�� </th>\n";
  $TD .= "  <td>\n";
  $TD .= "    <ul>\n";
  $TD .= "      <li>�t�Υ��ƶ}��A<font color=#ff079f>�ϥΪ��v���̰�</font>\n";
  $TD .= "      <li>�ϥΪ̥i�H�[��B�h��ҵ{�A�d�߿�Ҹ��\n";
  $TD .= "      <li>�Y�ϥΪ̶i�J���ɬq���~�A�N�u��i���ҵ��G���d��\n";
  $TD .= "      <li>��Үɬq���]�w�A�ЧQ��<font color=#cc076f>��Үɵ{�]�w�t��</font>\n";
  $TD .= "    </ul>\n";
  $TD .= "  </td>\n";
  $TD .= "</tr>\n";
  }
  return($TD);
}




