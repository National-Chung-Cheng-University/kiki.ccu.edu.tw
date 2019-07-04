#!/usr/local/bin/perl

###################################################################################################
#####  Show_All_GRO.cgi
#####  ��ܩҦ�����ǵ{, �ίS�w�ǵ{�����.
#####  �Y���ǤJ session_id, �h��ܥ[��ﶵ, �s���[�����.
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

########    Ū���ϥΪ̿�J���    ########
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
  $html_title = "����ǵ{<BR>" . $YEAR . " �Ǧ~�ײ� " . $TERM . " �Ǵ�";
}else{
  $html_title = "����ǵ{<BR>" . $YEAR . " �Ǧ~�ײ� " . $TERM . " �Ǵ�";
}


Read_GRO();			###  Ū�J %gro_name, @gro_dept, @gro_cour

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
    $TH = "<TH>�[��</TH>";
#    $TH2 = "<TD><A href=\"Add_Course01.cgi?session_id=$Input{session_id}?dept=$dept\">�[��</A></TD>";
  }
  print qq(
    �H�U�O <FONT color=RED>$gro_name{$gro_no}{gro_name}</FONT> �������ҵ{:<P>
    <CENTER>
    <TABLE border=1 class=font2>
      <TR bgcolor=YELLOW>$TH<TH>�}�Ҩt��</TH><TH>��إN�X</TH><TH>��ئW��</TH><TH>�Ǥ���</TH></TR>
  );
  foreach $gro_cour (@gro_cour) {                             ###  �����ҵ{
    if( $$gro_cour{gro_no} eq $gro_no )  {
      $dept = $cou_dept{$$gro_cour{cour_cd}};      
#      print("reading: $dept, $$gro_cour{cour_cd}...<BR>\n");
      %course = Read_Course($dept, $$gro_cour{cour_cd}, "01", "", "");
      %dept = Read_Dept($dept);      

      if( $Input{session_id} ne "" ) {
        $TH2 = "<TD><A href=\"Add_Course01.cgi?session_id=$Input{session_id}&dept=$dept&grade=$course{grade}\">�[��</A></TD>";
      }

      if( $course{cname} ne "" ) {     
        if( $last_dept ne $dept ) {				###  ���ܨt�ҫh���� TD ����
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
      <TR bgcolor=YELLOW><TH>�ǵ{�W��</TH><TH>��ؼ�</TH><TH>�����t��</TH></TR>
  );

  foreach $gro_no (keys %gro_name) {			###  �Ҧ� GRO
    $course_count = 0;
    foreach $gro_cour (@gro_cour) {				###  �����ҵ{
      if( $$gro_cour{gro_no} eq $gro_no )  { 
        $dept = $cou_dept{$$gro_cour{cour_cd}};
        %course = Read_Course($dept, $$gro_cour{cour_cd}, "01", "", "");
        $course_count++  if( $course{cname} ne "" );      	###  ���Ǵ����}�~++
      } 
    } 

    print qq(
      <TR>
        <TD><A href="Show_All_GRO.cgi?session_id=$Input{session_id}&gro_no=$gro_no">$gro_name{$gro_no}{gro_name}</A></TD>
        <TD>$course_count</TD>
        <TD>
    );
    foreach $gro_dept (@gro_dept) {				###  �����t��
      if( $$gro_dept{gro_no} eq $gro_no ) {
        %dept = Read_Dept($$gro_dept{dept});
        print(" $dept{cname2} ");
      }
    }
    print("</TD></TR>\n");
  }  
}













