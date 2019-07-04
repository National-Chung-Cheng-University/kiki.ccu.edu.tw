#!/usr/local/bin/perl

require "../library/Reference.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Teacher.pm";

%input= User_Input();
%dept = Read_Dept($input{dept_id});
@dept = Find_All_Dept();
@teacher = Read_Teacher_File();
%cge = Read_Cge();
@property = ("", "必修", "選修", "通識");

print("Content-type: text/html","\n\n");
Check_Dept_Password($input{dept_id}, $input{password});

#foreach $k (keys %input) {
#  print("$k ---> $input{$k}<br>");
#}


Print_Title();
Print_Grade_Selection();
Print_Course_Table();
Links3($input{dept_id} ,$input{grade}, $input{password});

############################################################################
sub Print_Title()
{
  if( $TERM == 3 ) {
    $show_term = "";
  }else{
    $show_term = join("", "第", $TERM, "學期");
  }

  print qq(
   <html>
     <meta http-equiv="Content-Type" content="text/html; charset=big5">
     <head><title>$SUB_SYSTEM_NAME開排課系統--列印當學期已開科目</title></head>
   <body background=../../Graph/ccu-sbg.jpg>
     <center>
      <br>
      <table border=0 width=80%>
       <tr>
        <td>系別:</td><td><b> $dept{cname} </b></td>
        <td>年級:</td><td><b> $input{grade} </b></td></tr><tr>
        <th colspan=4><H1><FONT face="標楷體">
            國立中正大學 <FONT color=RED>$SUB_SYSTEM_NAME</FONT>開排課系統<BR>
            $YEAR學年度$show_term擬開科目列表</FONT></th>
       </tr>
      </table>
      <hr width=80%>
      </H1>
  );
}
############################################################################
sub Print_Grade_Selection()
{
  print qq(
      顯示此年級科目
    <TABLE border=0>
     <tr><td>
      <FORM action="Print_Course.cgi" method=POST>
        <input type=hidden name="dept_id" value=$input{dept_id}>
        <input type=hidden name="grade" value="1">
        <input type=hidden name="password" value=$input{password}>
        <input type=submit value=" 一 ">
      </FORM>
     </td><td>
      <FORM action="Print_Course.cgi" method=POST>
        <input type=hidden name="dept_id" value=$input{dept_id}>
        <input type=hidden name="grade" value="2">
        <input type=hidden name="password" value=$input{password}>
        <input type=submit value=" 二 ">
      </FORM>
     </td><td>
      <FORM action="Print_Course.cgi" method=POST>
        <input type=hidden name="dept_id" value=$input{dept_id}>
        <input type=hidden name="grade" value="3">
        <input type=hidden name="password" value=$input{password}>
        <input type=submit value=" 三 ">
      </FORM>
     </td><td>
        <FORM action="Print_Course.cgi" method=POST>
        <input type=hidden name="dept_id" value=$input{dept_id}>
        <input type=hidden name="grade" value="4">
        <input type=hidden name="password" value=$input{password}>
        <input type=submit value=" 四 ">
      </FORM>
     </td></tr>
    </TABLE>
  );
}
##########################################################################
sub Print_Course_Table()
{
  @course = Find_All_Course($input{dept_id}, $input{grade}, "");
  local $course_count=0;
  $number_of_course = @course;
  print qq(
  本年級共有 $number_of_course 筆開課資料
  <table border=1>
    <tr bgcolor=YELLOW>
      <th><font size=1>編號</font></th>
      <th><font size=1>班別</font></th>
      <th><font size=1>年級</font></th>
      <th><font size=1>科目名稱</font></th>
      <th><font size=1>教師</font></th>
      <th><font size=1>時數<br>正課/實習實驗/書報討論</font></th>
      <th><font size=1>學分</font></th>
      <th><font size=1>選必</font></th>
      <th><font size=1>上課時間</font></th>
      <th><font size=1>教室</font></th>
      <th><font size=1>篩選原則</font></th>
      <th><font size=1>限修/保留</font></th>
      <th><font size=1>支援通識領域/支援通識人數</font></th>
      <th><font size=1>備註</font></th>
    </tr>
  );

  foreach $course (@course) {
    %course = Read_Course($input{dept_id}, $$course{id}, $$course{group}, "");
    %classroom = Read_Classroom($course{classroom});
    $time_string = Format_Time_String($course{time});
    $note_string = Format_Note();

    if($course_count % 5 == 4) {
       print("<tr bgcolor=#f0f0f0>");
    }else{
       print("<tr>");
    }
    print qq(
        <td align=center><font size=1> $$course{id} </font></td>
        <td align=center><font size=1> $$course{group} </font></td>
        <td align=center><font size=1> $course{grade} </font></td>
    );
    $note_dis = $note_eng = "";
    $note_dis = "<BR><FONT color=RED>(此科目為遠距教學課程)" if( $course{distant_learning} == 1 );
    $note_eng = "<BR><FONT color=RED>(此科目為全英語授課)"   if( $course{english_teaching} == 1 );
    print qq(
        <td align=left><font size=1> $course{cname}<br>
        $course{ename} $note_dis $note_eng</font></td>
        <td align=center>
    );
    $i=0;
    while( $course{teacher}[$i] ne "" ) {
       print qq(<font size=1>$Teacher_Name{$course{teacher}[$i]}</font>);
       print (", ")  if($course{teacher}[$i+1] ne "");
       $i++;
    }
#    if($course{teacher}[0] eq "99999") {
#       print qq(<font size=1>教師未定</font>);
#    }
    print qq(
        </td>
        <td align=center><font size=1> $course{total_time}<br>$course{lab_time1}/$course{lab_time2}/$course{lab_time3} </font></td>
        <td align=center><font size=1> $course{credit} </font></td>
        <td align=center><font size=1> $property[$course{property}] </font></td>
        <td align=center><font size=1> $time_string</font></td>
        <td align=center><font size=1> $classroom{cname} </font></td>
        <td align=center><font size=1> $PRINCIPLE[$course{principle}] </font></td>
        <td align=center><font size=1> $course{number_limit} / $course{reserved_number} </font></td>
        <td align=center><font size=1> $cge{$course{support_cge_type}}{sub_cge_id_show} $cge{$course{support_cge_type}}{cge_name} / $course{support_cge_number} </font></td>
        <td align=left><font size=1> $note_string </font></td>
      </tr>
    );
    $course_count++;
  }

  print qq(
     </table>
     <P>&nbsp<P>
     <CENTER>系所主管簽章: ________________________________
  );

}
#########################################################################
sub Format_Note()
{
  my $note_string = "";
  my($temp_dept);
  my(@grade) = ("", "一年級", "二年級", "三年級", "四年級");   

#  if( $course{number_limit} != 0 ) {
#    $note_string .= "限修$course{number_limit}人; ";
#  }
#  if ( $course{reserved_number} != 0 ) {
#    $note_string .= "保留$course{reserved_number}人; ";
#  }
  if( ${$course{support_dept}}[0] ne "" ) {
    $note_string .= "<b>支援</b>";
    foreach $dept (@{$course{support_dept}}) {
      %temp_dept = Read_Dept($dept);
      $note_string .= $temp_dept{cname2};
    }   
    foreach $grade (@{$course{support_grade}}) {
      $note_string .= $grade[$grade];
    }
    foreach $class (@{$course{support_class}}) {
      $note_string .= $class;
      $note_string .= "班";
    }
    $note_string .= "; ";
  }
if( ${$course{ban_dept}}[10] ne "" ) {
  $note_string .= "限本系生修;";
  if( ($course{number_limit} > 0)and($course{dept} ne "7006") ) {  
    ### 非通識開課若限本系且限人數, 顯示+20%訊息
    ### 字眼改成 "加退選時開放外系學生選修" (2002/12/02)
    $note_string .= "於加退選期間開放外系學生選修;";
  }
}
######  先修科目
#$note_string .= "${${$course{prerequisite_course}}[0]}{dept} - ${${$course{prerequisite_course}}[0]}{id} - ${${$course{prerequisite_course}}[0]}{grade}<BR>\n";
#if( (${${$course{prerequisite_course}}[0]}{dept} ne "")and( ${${$course{prerequisite_course}}[0]}{dept} ne "99999") ) {
if( (${${$course{prerequisite_course}}[0]}{dept} ne "99999") and (${${$course{prerequisite_course}}[0]}{dept} ne "") ) {
    $note_string .= "<b>先修科目</b>";
    foreach $pre_course (@{$course{prerequisite_course}}) {
      %pre_course = Read_Course( $$pre_course{dept}, $$pre_course{id}, "01" ,"history");
      $note_string = $note_string . "(" . $$pre_course{id} . ")" . $pre_course{cname} . "(" . $GRADE{$$pre_course{grade}} . ")" . " ";
    }
    $note_string .= "($PREREQUISITE_LOGIC{$course{prerequisite_logic}})"  if($course{prerequisite_logic});
}
#  if( ${$course{ban_dept}}[0] ne "" ) {
#    $note_string .= "<b>擋修</b>";
#    foreach $dept (@{$course{ban_dept}}) {
#      %temp_dept = Read_Dept($dept);
#      $note_string = $note_string . $temp_dept{cname2} . " ";
#    }
#    foreach $grade (@{$course{ban_grade}}) {
#      $note_string .= $grade[$grade];
#    }
#    foreach $class (@{$course{ban_class}}) {
#      $note_string .= $class;
#      $note_string .= "班";
#    }
#    $note_string .= "; ";
#  }
  $note_string .= $course{note};
  $note_string = "無"  if( $note_string eq "" );
  return $note_string;
}
