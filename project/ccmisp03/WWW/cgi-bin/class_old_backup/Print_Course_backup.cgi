#!/usr/local/bin/perl

#########################################################################
#####  Print_Course.cgi
#####  列印學生選課單
#####  在規定時間給學生列印選課單, 簽名後繳交回教學組.
#####  在執行此程式同時記錄到 Student.log 中, 以便之後查詢.
#####  Coder: Nidalap Leee
#####  Last Update: Feb 18,2000
#########################################################################

print("Content-type:text/html\n\n");

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Select_Course.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Teacher.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Error_Message.pm";

my(%Input,%Student,%Dept);

%Input    = User_Input();
%Student  = Read_Student($Input{id});
%Dept     = Read_Dept($Student{dept});
%time     = gettime();
my $BOARD_TEXT = Read_Board();

Check_Student_Password($Input{id}, $Input{password});

@MyCourse = Course_of_Student($Input{id}); 
my($Table_Data)=CREAT_COURSE_TABLE();
Student_Log("Print ", $Input{id}, "", "", "");
$space = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";

#Print_BAN();
Print_HTML();

sub Print_BAN()
{
  print qq(
    <html>
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=big5">
      <TITLE>國立中正大學$SUB_SYSTEM_NAME選課系統--學生選課單</TITLE>
    </head>
    <body background="$GRAPH_URL./ccu-sbg.jpg">
    <center>
      <FONT face="標楷體">
        <H1>國立中正大學$SUB_SYSTEM_NAME學生選課系統<br>
        $YEAR學年度$TERM_NAME  選課結果單</H1>
      </FONT>
    <HR>
    選課單目前不開放列印, 於請於加退選截止後列印本單, 謝謝!
  );
}

##############################################################################

sub Print_HTML() 
{
  print qq(
  <html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <TITLE>國立中正大學$SUB_SYSTEM_NAME選課系統--學生選課單</TITLE>
  </head>
  <body background="$GRAPH_URL./ccu-sbg.jpg">
    <center>
      <FONT face="標楷體">
        <H1>國立中正大學$SUB_SYSTEM_NAME學生選課系統<br>
        $YEAR學年度$TERM_NAME  選課結果單</H1>
      </FONT>
    <H3>
   <TABLE border=0 width=100%>
     <TR><TH colspan=4 align=right>印製日期:$time{time_string}</TH></TH>
     <TR><TH align=left>系所別:$Dept{cname}</TH><TH>班級:$Student{class}</TH>
         <TH>學號:$Student{id}</TH><TH align=right>姓名:$Student{name}</TH></TR>
   </TABLE>
   $Table_Data<P>
   </CENTER>本學期共修<U> $MyCount </U>科<U> $CreditSum </U>學分<P>
   <CENTER>
   <TABLE border=1 width=100%>
     <TR><TD>系所主管</TD><TD width=20%>$space</TD>
         <TD align=center nowrap>導師<br>(指導教授)</TD><TD width=20%>$space</TD>
         <TD>學生</TD><TD width=20%>$space</TD>
     </TR>
   </TABLE>
   <P>
  );
  if($TERM == 3) {      ###  如果是暑修, 要多四個簽章欄位
    print qq(
      <TABLE border=1 width=100%>
       <TR>
         <TD>出納組</TD><TD width=20%>$space</TD>
         <TD align=center nowrap>郵局(台銀)局號</TD><TD width=20%>$space</TD>
         <TD>帳號</TD><TD width=20%>$space</TD>
         <TD>身份證字號</TD><TD width=20%>$space</TD>
       </TR>
      </TABLE>
    );
  }
  print qq(
   </CENTER>
    <FONT size=3 face="標楷體">
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
  my(@WeekDay)=("一","二","三","四","五","六","日");
  my(@TimeMap)=(A,1,2,3,4,B,5,6,7,8,C,D,E);
  $fs = 2;        ##### 表格內的字體大小 (font size)
  $CreditSum=0;
  $MyCount=@MyCourse;
  @Credit=CREDIT_TABLE();

  $DATA = $DATA."<table width=100% border=1>\n";
  $DATA = $DATA."<tr>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=$fs>科目編號</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=$fs>班別</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=$fs>科目名稱</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=$fs>任課教師</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=$fs>學分</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=$fs>學分歸屬</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=$fs>上課時間</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=$fs>上課教室</font></th>\n";
  $DATA = $DATA."</tr>\n";

  ####  列印相關課程資料  ####
  for($i=0; $i < $MyCount; $i++){
    my(%theCourse)=Read_Course($MyCourse[$i]{dept},$MyCourse[$i]{id},$MyCourse[$i]{group},"","");
      $CreditSum += $theCourse{credit};
      $DATA = $DATA."<tr>\n";
      $DATA = $DATA."<td align=center><font size=$fs>";
      $DATA = $DATA.$theCourse{id};                         ##  科目代碼
      $DATA = $DATA."</font></td>\n";
      $DATA = $DATA."<td align=center><font size=$fs>";
      $DATA = $DATA.$theCourse{group}."</font></td>\n";     ##  班別

      $theCourse{cname} =~ s/、/、 /;
      $theCourse{cnema} =~ s/＆/＆ /;
      $DATA = $DATA."<td align=left><font size=$fs>";
      $DATA = $DATA.$theCourse{cname}."</font></td>\n";     ##  科目名稱

      $DATA=$DATA."<td><font size=$fs>";           ##  授課教師
      $T=@{$theCourse{teacher}};
      for($teacher=0; $teacher < $T; $teacher++){
        if($theCourse{teacher}[$teacher] != 99999){
          $DATA=$DATA.$Teacher_Name{$theCourse{teacher}[$teacher]};
        }else{
          $DATA=$DATA."教師未定";
        }
        if($teacher != $T-1){
          $DATA=$DATA.", ";
        }
      }
      $DATA=$DATA."</font></td>\n";

      $DATA = $DATA."<td align=center><font size=$fs>";
      $DATA = $DATA.$theCourse{credit}."</font></td>\n";    ##  學分

      $DATA = $DATA."<td align=center><font size=$fs>";
      $DATA = $DATA.$Credit[$MyCourse[$i]{property}];       ##  學分歸屬
      $DATA = $DATA."</font></td>\n";

      $DATA=$DATA."<td align=center><font size=$fs>";           ## 星期節次
      $T=@{$theCourse{time}};
      my($last_day);
      for($t1=0; $t1 < $T; $t1++){
        if($last_day ne $theCourse{time}[$t1]{week}) {
          $DATA .= $WeekDay[$theCourse{time}[$t1]{week}-1];
        }
        $DATA .= $TimeMap[$theCourse{time}[$t1]{time}];
#        $DATA=$DATA.$WeekDay[$theCourse{time}[$t1]{week}-1];
#        $DATA=$DATA.$TimeMap[$theCourse{time}[$t1]{time}] . " ";
        $last_day = $theCourse{time}[$t1]{week};
      }
      $DATA=$DATA."</font></td>\n";

      $DATA=$DATA."<td align=left><font size=$fs>";           ##  教室
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
  ##  Step 1: 取得學生的年級##
  ##  Step 2: 讀取相關的時間設定檔##
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

  if($User{dept}%10 <= 4){    ##  大一至大四
    return($User{grade});
  }else{
    if($User{grade} == 1){    ##  研一或博一
      return(5);
    }else{                    ##  研二以上含博士班學生
      return(6);
    }
  }
}

###########################################################################
###  讀取選課單公佈欄
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
