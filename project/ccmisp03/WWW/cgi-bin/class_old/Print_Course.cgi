#!/usr/local/bin/perl

#########################################################################
#####  Print_Course.cgi
#####  �C�L�ǥͿ�ҳ�
#####  �b�W�w�ɶ����ǥͦC�L��ҳ�, ñ�W��ú��^�оǲ�.
#####  �b���榹�{���P�ɰO���� Student.log ��, �H�K����d��.
#####  Coder: Nidalap Leee
#####  Last Update: Feb 18,2000
#########################################################################

print("Content-type:text/html\n\n");

require "../library/Reference.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."System_Settings.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Select_Course.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Teacher.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Session.pm";

my(%Input,%Student,%Dept);

%Input    = User_Input();
($Input{id}, $Input{password}, $login_time, $ip) = Read_Session($Input{session_id});
#print("session_id, id, pass = $Input{session_id}, $Input{id}, $Input{password}<BR>"); 

%system_settings = Read_System_Settings();
%Student  = Read_Student($Input{id});
%Dept     = Read_Dept($Student{dept});
%time     = gettime();
my $BOARD_TEXT = Read_Board();

Check_Student_Password($Input{id}, $Input{password});

@MyCourse = Course_of_Student($Input{id}); 
my($Table_Data)=CREAT_COURSE_TABLE();
$space = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";

if( ($SUPERUSER==1) or ($system_settings{allow_print_student_course}==1) ) {
  Print_HTML();
}else{
  Print_BAN();
}

sub Print_BAN()
{
  print qq(
    <html>
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=big5">
      <TITLE>$SUB_SYSTEM_NAME�ǥͿ�ҳ�($Student{name})</TITLE>
    </head>
    <body background="$GRAPH_URL./ccu-sbg.jpg">
    <center>
      <FONT face="�з���">
        <H1>��ߤ����j��$SUB_SYSTEM_NAME�ǥͿ�Ҩt��<br>
        $YEAR�Ǧ~��$TERM_NAME  ��ҵ��G��</H1>
      </FONT>
    <HR>
    ��ҳ�ثe���}��C�L, ��Щ�[�h��I���C�L����, ����!<BR>
  );
}

##############################################################################

sub Print_HTML() 
{
  Student_Log("Print ", $Input{id}, "", "", "");
  print qq(
  <html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <TITLE>$SUB_SYSTEM_NAME�ǥͿ�ҳ�($Student{name})</TITLE>
  </head>
  <body background="$GRAPH_URL./ccu-sbg.jpg">
    <center>
      <FONT face="�з���">
        <H1>��ߤ����j��$SUB_SYSTEM_NAME�ǥͿ�Ҩt��<br>
        $YEAR�Ǧ~��$TERM_NAME  ��ҵ��G��</H1>
      </FONT>
    <H3>
   <TABLE border=0 width=100%>
     <TR><TH colspan=5 align=right>�L�s���:$time{time_string}</TH></TH>
     <TR><TH align=left>�t�ҧO:$Dept{cname}</TH>
         <TH>�~��:$Student{grade}</TH>
         <TH>�Z��:$Student{class}</TH>
         <TH>�Ǹ�:$Student{id}</TH>
         <TH align=right>�m�W:$Student{name}</TH></TR>
   </TABLE>
   $Table_Data<P>
   </CENTER>���Ǵ��@��<U> $MyCount </U>��<U> $CreditSum </U>�Ǥ�<P>
   <CENTER>
   <TABLE border=1 width=100%>
     <TR><TD>�t�ҥD��</TD><TD width=20%>$space</TD>
         <TD align=center nowrap>�ɮv<br>(���ɱб�)</TD><TD width=20%>$space</TD>
         <TD>�ǥ�</TD><TD width=20%>$space</TD>
     </TR>
   </TABLE>

   <P>
  );
##  if($TERM == 3) {      ###  �p�G�O����, �n�h�|��ñ�����
  if( ($SUB_SYSTEM == 2)or($SUB_SYSTEM == 4)) { ###  �p�G�O����, �n�h�|��ñ�����
    print qq(
      <TABLE border=1 width=100%>
       <TR>
    );
    if( $SUB_SYSTEM == 4 ) {    ### �@��ʹ��פ��n�X�ǲ�, ���O�M�Z�n(2005/06/24)
      print qq(
         <TD>�X�ǲ�</TD><TD width=20%>$space</TD>
      );
    }
    print qq(
         <TD align=center nowrap>�l��(�x��)����</TD><TD width=20%>$space</TD>
         <TD>�b��</TD><TD width=20%>$space</TD>
         <TD>�����Ҧr��</TD><TD width=20%>$space</TD>
       </TR>
      </TABLE>
    );
  }
  print qq(
   </CENTER>
    <FONT size=3 face="�з���">
     <UL>
     $BOARD_TEXT
    </FONT>
  );
}



############################################################################
sub CREAT_COURSE_TABLE
{
  my($DATA)="";
  my(@Teachers)=Read_Teacher_File();
  my(@WeekDay)=@WEEKDAY;
  my(@TimeMap)=@TIMEMAP;
  $fs = 2;        ##### ��椺���r��j�p (font size)
  $CreditSum=0;
  $MyCount=@MyCourse;
  @Credit=CREDIT_TABLE();

  $DATA = $DATA."<table width=100% border=1>\n";
  $DATA = $DATA."<tr>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=$fs>��ؽs��</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=$fs>�Z�O</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=$fs>��ئW��</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=$fs>���ұЮv</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=$fs>�Ǥ�</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=$fs>�Ǥ��k��</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=$fs>�W�Үɶ�</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=$fs>�W�ұЫ�</font></th>\n";
  $DATA = $DATA."</tr>\n";

  ####  �C�L�����ҵ{���  ####
  for($i=0; $i < $MyCount; $i++){
    my(%theCourse)=Read_Course($MyCourse[$i]{dept},$MyCourse[$i]{id},$MyCourse[$i]{group},"","");
      $CreditSum += $theCourse{credit};
      $DATA = $DATA."<tr>\n";
      $DATA = $DATA."<td align=center><font size=$fs>";
      $DATA = $DATA.$theCourse{id};                         ##  ��إN�X
      $DATA = $DATA."</font></td>\n";
      $DATA = $DATA."<td align=center><font size=$fs>";
      $DATA = $DATA.$theCourse{group}."</font></td>\n";     ##  �Z�O

      $theCourse{cname} =~ s/�B/�B /;
      $theCourse{cnema} =~ s/��/�� /;
      $DATA = $DATA."<td align=left><font size=$fs>";
      $DATA = $DATA.$theCourse{cname}."</font></td>\n";     ##  ��ئW��

      $DATA=$DATA."<td><font size=$fs>";           ##  �½ұЮv
      $T=@{$theCourse{teacher}};
      for($teacher=0; $teacher < $T; $teacher++){
        if($theCourse{teacher}[$teacher] != 99999){
          $DATA=$DATA.$Teacher_Name{$theCourse{teacher}[$teacher]};
        }else{
          $DATA=$DATA."�Юv���w";
        }
        if($teacher != $T-1){
          $DATA=$DATA.", ";
        }
      }
      $DATA=$DATA."</font></td>\n";

      $DATA = $DATA."<td align=center><font size=$fs>";
      $DATA = $DATA.$theCourse{credit}."</font></td>\n";    ##  �Ǥ�

      $DATA = $DATA."<td align=center><font size=$fs>";
      $DATA = $DATA.$Credit[$MyCourse[$i]{property}];       ##  �Ǥ��k��
      $DATA = $DATA."</font></td>\n";

      $DATA=$DATA."<td align=center><font size=$fs>";           ## �P���`��
      $time_string = Format_Time_String($theCourse{time});
      $DATA .= $time_string;
      $DATA=$DATA."</font></th>\n";

      $DATA=$DATA."<td align=left><font size=$fs>";           ##  �Ы�
      %Room=Read_Classroom($theCourse{classroom});
      $DATA=$DATA.$Room{cname};
      $DATA=$DATA."</font></td>\n";

      $DATA = $DATA."</tr>\n";
  }
  $DATA = $DATA."</table>\n";
  return($DATA);
}
#-----------------------------------------------------------------------
sub Check_Time_Map
{
  ###################################################
  ##  Step 1: ���o�ǥͪ��~��##
  ##  Step 2: Ū���������ɶ��]�w��##
  ###################################################
  my($user)=@_;
  my($MapClass)=Check_Map_Class($user);
  my($FileName)=$REFERENCE_PATH."SelectTimeMap/".$MapClass.".map";

  %User=Read_Student($user);
  open(FILE,"<$FileName");
      @Orignal=<FILE>;
      foreach $item(@Orignal){
        my($dept, $state)=split(/\s+/,$item);
        $My_Time{$dept}=$state;
      }
  $FileName=$REFERENCE_PATH."TimeMap/T".$My_Time{$User{dept}}.".map";
  open(FILE,"<$FileName");
  my($count)=0;
  @Duration=<FILE>;
  foreach $item(@Duration){
    $item=~s/\n//;
    ($TD[$count]{S},$TD[$count]{E})=split(/\s+/,$item);
    $count++;
  }

  ($sec,$min,$hour,$day,$nmonth,$year,$wday,$yday,$isdst) = localtime(time);

  $Value=$min+$hour*100;

  for($i=0; $i < $count; $i++){
    if( ($Value > int($TD[$i]{S})) && ($Value < int($TD[$i]{E})) ){
      $Flag = 1;
    }
  }

  return($Flag);
}
#-----------------------------------------------------------------------
sub Check_Map_Class
{
  my($user)=@_;
  %User=Read_Student($user);

  if($User{dept}%10 <= 4){    ##  �j�@�ܤj�|
    return($User{grade});
  }else{
    if($User{grade} == 1){    ##  ��@�γդ@
      return(5);
    }else{                    ##  ��G�H�W�t�դh�Z�ǥ�
      return(6);
    }
  }
}

###########################################################################
###  Ū����ҳ椽�G��
sub Read_Board()
{
  my($text, $board_file, @temp);
  $board_file = $REFERENCE_PATH."select_course_board.txt";
  open(BOARD, $board_file) or 
      Fatal_Error("Cannot read file $board_file in Selected_View00.cgi!");
  @temp = <BOARD>;
  close(BOARD);
  $text = join("", @temp);
  $text =~ s/\n/<br>\n/g;
  return $text;
}
