#!/usr/local/bin/perl

###################################################################################################
#####  Show_All_GRO.cgi
#####  顯示所有跨領域學程, 及特定學程的科目.
#####  若有傳入 session_id, 則顯示加選選項, 連往加選網頁.
#####  2008/05/28 Nidalap :D~

print("Content-type: text/html\n\n");

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Password.pm";
#require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Select_Course.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Teacher.pm";
require $LIBRARY_PATH."Classroom.pm";

########    讀取使用者輸入資料    ########
%Input=User_Input();
@dept = Find_All_Dept();
foreach $dept (@dept) {
  @course = Find_All_Course($dept);
  foreach $course (@course) {
#    print("$$course{id}  $$course{group}<BR>\n");
    $cou_dept{$$course{id}} = $dept;
#    print("$$course{id} belongs to  $dept<BR>\n");
  }
}

#$fs2 = "<FONT size=2>";

#%the_Course=Read_Course($Input{dept},$Input{course},$Input{group});
##########################################

if($Input{gro_no} eq "") {
  $html_title = "跨領域學程<BR>" . $YEAR . " 學年度第 " . $TERM . " 學期";
}else{
  $html_title = "跨領域學程<BR>" . $YEAR . " 學年度第 " . $TERM . " 學期";
}


Read_GRO();			###  讀入 %gro_name, @gro_dept, @gro_cour

print qq(
  <HTML>
    <HEAD>
      <meta http-equiv="Content-Type" content="text/html; charset=big5">
      <TITLE>$html_title</TITLE>
      <LINK rel="stylesheet" type="text/css" href="$HOME_URL/font.css">
    </HEAD>
    <BODY background=$GRAPH_URL/ccu-sbg.jpg>
    <CENTER>
      <SPAN class="title2">$html_title</SPAN>
      <HR>
    </CENTER>
    <SPAN class="font2">
    <P class="illustration">    
);

if($Input{gro_no} eq "") {
  List_All_GRO();
}else{
  Show_GRO($Input{gro_no});
}

##############################################################################################
sub Show_GRO()
{
  my($gro_no) = @_;
  my($TH, $TH2); 
  if( $Input{session_id} ne "" ) {
    $TH = "<TH>加選</TH>";
#    $TH2 = "<TD><A href=\"Add_Course01.cgi?session_id=$Input{session_id}?dept=$dept\">加選</A></TD>";
  }
  print qq(
    以下是 <FONT color=RED>$gro_name{$gro_no}{gro_name}</FONT> 的相關課程:<P>
    <CENTER>
    <TABLE border=1 class=font2>
      <TR bgcolor=YELLOW>$TH<TH>開課系所</TH><TH>科目代碼</TH><TH>科目名稱</TH><TH>學分數</TH></TR>
  );
  foreach $gro_cour (@gro_cour) {                             ###  相關課程
    if( $$gro_cour{gro_no} eq $gro_no )  {
      $dept = $cou_dept{$$gro_cour{cour_cd}};      
#      print("reading: $dept, $$gro_cour{cour_cd}...<BR>\n");
      %course = Read_Course($dept, $$gro_cour{cour_cd}, "01", "", "");
      %dept = Read_Dept($dept);      

      if( $Input{session_id} ne "" ) {
        $TH2 = "<TD><A href=\"Add_Course01.cgi?session_id=$Input{session_id}&dept=$dept&grade=$course{grade}\">加選</A></TD>";
      }

      if( $course{cname} ne "" ) {     
        if( $last_dept ne $dept ) {				###  改變系所則改變 TD 底色
          if($high_light =~ /FFFFFF/) {
            $high_light = "bgcolor = FFFF77";
          }else{
            $high_light = "bgcolor = FFFFFF";
          }
        }
  
        print qq(
          <TR $high_light>
            $TH2
            <TD>$dept{cname2}</TD>
            <TD>$$gro_cour{cour_cd}</TD>
            <TD>$course{cname}</TD>  
            <TD>$course{credit}</TD>
          </TR>
        );
        $last_dept = $dept;
      }
    }
  }
  print("</TD></TR>\n");
    


}

###############################################################################################
sub List_All_GRO()
{
  print qq(
    <CENTER>
    <TABLE border=1 class=font2>
      <TR bgcolor=YELLOW><TH>學程名稱</TH><TH>科目數</TH><TH>相關系所</TH></TR>
  );

  foreach $gro_no (keys %gro_name) {			###  所有 GRO
    $course_count = 0;
    foreach $gro_cour (@gro_cour) {				###  相關課程
      if( $$gro_cour{gro_no} eq $gro_no )  { 
        $dept = $cou_dept{$$gro_cour{cour_cd}};
        %course = Read_Course($dept, $$gro_cour{cour_cd}, "01", "", "");
        $course_count++  if( $course{cname} ne "" );      	###  本學期有開才++
      } 
    } 

    print qq(
      <TR>
        <TD><A href="Show_All_GRO.cgi?session_id=$Input{session_id}&gro_no=$gro_no">$gro_name{$gro_no}{gro_name}</A></TD>
        <TD>$course_count</TD>
        <TD>
    );
    foreach $gro_dept (@gro_dept) {				###  相關系所
      if( $$gro_dept{gro_no} eq $gro_no ) {
        %dept = Read_Dept($$gro_dept{dept});
        print(" $dept{cname2} ");
      }
    }
    print("</TD></TR>\n");
  }  
}













