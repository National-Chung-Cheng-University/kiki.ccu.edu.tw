#!/usr/local/bin/perl

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
%the_Course=Read_Course($Input{dept},$Input{course},$Input{group});
##########################################

####    �إ� HTML �ɮת����Y����    ####
####    �]�A�ϥΪ̪�������Ƶ�      ####

if( $Input{user} eq "" ) {
  %Student=Read_Student($Input{user});
  %Dept=Read_Dept($Student{dept});
  my($HEAD_DATA)=Head_of_Individual($Student{name},$Student{id},$Dept{cname},$Student{grade},$Student{class});
}

####    �N�ݭn�t�~�ѽX����ƸѽX    ####
if($the_Course{number_limit} == 0){
  $the_Course{number_limit} = "�L";
}

  ####    �䴩�ѽX    ####
     $Support_Dept_Num = @{$the_Course{support_dept}};
     $Support_Grade_Num = @{$the_Course{support_grade}};
     $Support_Class_Num = @{$the_Course{support_class}};
     if(($Support_Dept_Num != 0) || ($Support_Grade_Num != 0) || ($Support_Class_Num != 0)){
       if($Support_Dept_Num == 0){
         $Support_Dept="�Ҧ��t��";
       }else{
         for($i=0; $i < $Support_Dept_Num; $i++){
           %the_Dept=Read_Dept($the_Course{support_dept}[$i]);
           $Support_Dept = $Support_Dept."[".$the_Dept{cname2}."]";
         }
       }
       if($Support_Grade_Num == 0){
         $Support_Grade="�Ҧ��~��";
       }else{
         for($i=0; $i < $Support_Grade_Num; $i++){
           $Support_Grade = $Support_Grade."[". $the_Course{support_grade}[$i] ."]";
         }
       }
       if($Support_Class_Num == 0){
         $Support_Class="�Ҧ��Z�O";
       }else{
         for($i=0; $i < $Support_Class_Num; $i++){
           $Support_Class = $Support_Class."[". $the_Course{support_class}[$i] ."]";
         }
       }

     }else{
       $Support_Dept="�L";
       $Support_Grade="�L";
       $Support_Class="�L";
     }
  ########################
  ####    �׭׸ѽX    ####
     $Ban_Dept_Num = @{$the_Course{ban_dept}};
     $Ban_Grade_Num = @{$the_Course{ban_grade}};
     $Ban_Class_Num = @{$the_Course{ban_class}};
     if(($Ban_Dept_Num != 0) || ($Ban_Grade_Num != 0) || ($Ban_Class_Num != 0)){
       if($Ban_Dept_Num == 0){
         $Ban_Dept="�Ҧ��t��";
       }else{
         for($i=0; $i < $Ban_Dept_Num; $i++){
           %the_Dept=Read_Dept($the_Course{ban_dept}[$i]);
           $Ban_Dept = $Ban_Dept."[".$the_Dept{cname2}."]";
         }
       }
       if($Ban_Grade_Num == 0){
         $Ban_Grade="�Ҧ��~��";
       }else{
         for($i=0; $i < $Ban_Grade_Num; $i++){
           $Ban_Grade = $Ban_Grade."[".$the_Course{ban_grade}[$i]."]";
         }
       }
       if($Ban_Class_Num == 0){
         $Ban_Class="�Ҧ��Z��";
       }else{
          for($i=0; $i < $Ban_Class_Num; $i++){
           $Ban_Class = $Ban_Class."[".$the_Course{ban_class}[$i]."]";
         }
       }
     }else{
       $Ban_Dept="�L";
       $Ban_Grade="�L";
       $Ban_Class="�L";
     }
  ########################
@Principle=("���ݿz��","�@���z��","�G���z��");
if($the_Course{note} eq ""){
  $the_Course{note} = "�L";
}
########################################
%cge = Read_Cge();
###########################################################
#####  ���� $Prerequisite_Course
if( (${${$the_Course{prerequisite_course}}[0]}{dept} ne "99999") and (${${$the_Course{prerequisite_course}}[0]}{dept} ne "") ) {
  $note_string .= "";
  foreach $pre_course (@{$the_Course{prerequisite_course}}) {
    %pre_course = Read_Course( $$pre_course{dept}, $$pre_course{id}, "01" ,"history");
    $Prerequisite_Course = $Prerequisite_Course . "(" . $$pre_course{id} . ")" .
                           $pre_course{cname} . "(" . $GRADE{$$pre_course{grade}} . ")<BR>";
  }
  if($the_Course{prerequisite_logic} eq "OR") {
    $Prerequisite_Course .= "($PREREQUISITE_LOGIC{OR})";
  }else{
    $Prerequisite_Course .= "($PREREQUISITE_LOGIC{AND})";
  }
}else{
  $Prerequisite_Course = "�L";
}
###########################################################
$online_help = Online_Help();
$show_help{'support_dept'}	= Show_Online_Help('SUPPORT_DEPT');
$show_help{'ban_dept'}		= Show_Online_Help('BAN_DEPT');
$show_help{'reserved_number'}	= Show_Online_Help('RESERVED_NUMBER');
$show_help{'principle'}		= Show_Online_Help('PRINCIPLE');
$show_help{'prerequisite_course'} = Show_Online_Help('PREREQUISITE_COURSE');
$show_help{'note'}		= Show_Online_Help('NOTE');


print << "End_of_HTML"
<html>
$online_help
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
</head>
<body background="$GRAPH_URL/ccu-sbg.jpg">
<center>
    $HEAD_DATA
    <hr><br>
    <font size=4>��L�����Ƶ����</font><br><p>
    <table width=640 border=0>
    <tr>
    <th>���</th><td align=left>$the_Course{cname}</td>
    <th>�N�X</th><td align=left>$the_Course{id}</td>
    <th>�Z�O</th><td align=left>$the_Course{group}�Z</td>
    </tr>
    </table>
    <table border=1 width=640>
      <tr> <th width=30%>���פH��</th><td>$the_Course{number_limit}</td> </tr>
      <tr> <th>�䴩�t�� $show_help{'support_dept'}</th><td>$Support_Dept</td></tr>
      <tr> <th>�䴩�~��</th><td>$Support_Grade</td></tr>
      <tr> <th>�䴩�Z�O</th><td>$Support_Class</td></tr>
      <tr> <th>�׭רt�� $show_help{'ban_dept'}</th><td>$Ban_Dept</td></tr>
      <tr> <th>�׭צ~��</th><td>$Ban_Grade</td></tr>
      <tr> <th>�׭ׯZ�O</th><td>$Ban_Class</td></tr>
      <tr> <th>�O�d���t�W�B $show_help{'reserved_number'} </th><td>$the_Course{reserved_number}</td> </tr>
      <tr> <th>�z���h $show_help{'principle'} </th><td>$Principle[$the_Course{principle}]</td></tr>
      <tr> <th>�䴩�q�Ѭ��</th><td>$cge{$the_Course{support_cge_type}}{cge_name}</td></tr>
      <TR> <TH>�䴩�q�ѤH��</TH><TD>$the_Course{support_cge_number}</TD></TR>
      <TR> <TH>���׬�� $show_help{'prerequisite_course'} </TH><TD>$Prerequisite_Course</TD></TR>
      <tr> <th>��L�Ƶ� $show_help{'note'} </th><td>$the_Course{note}&nbsp</td></tr>
    </table>
    <table width=640 border=0>
    <tr><th>
    <a href="javascript:history.back()">�^�W��</a>
    </th></tr>
    </table>
</center>

</body>
</html>
End_of_HTML

