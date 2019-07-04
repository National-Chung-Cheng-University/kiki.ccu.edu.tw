#!/usr/local/bin/perl

##############################################################################################
#####  ShowNote.cgi
#####  顯示該科目的詳細開課設定，備註等資訊
#####  Updates:
#####   ......
#####   2009/05/21 新增(暑修的)第一類/第二類課程於備註一欄.  Nidalap :D~

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
require $LIBRARY_PATH."System_Settings.pm";

########    讀取使用者輸入資料    ########
%Input=User_Input();
%the_Course=Read_Course($Input{dept},$Input{course},$Input{group});
##########################################

####    建立 HTML 檔案的表頭部分    ####
####    包括使用者的身份資料等      ####

if( $Input{user} eq "" ) {
  %Student=Read_Student($Input{user});
  %Dept=Read_Dept($Student{dept});
  my($HEAD_DATA)=Head_of_Individual($Student{name},$Student{id},$Dept{cname},$Student{grade},$Student{class});
}

####    將需要另外解碼的資料解碼    ####
if($the_Course{number_limit} == 0){
  $the_Course{number_limit} = "無";
}

  ####    支援解碼    ####
     $Support_Dept_Num = @{$the_Course{support_dept}};
     $Support_Grade_Num = @{$the_Course{support_grade}};
     $Support_Class_Num = @{$the_Course{support_class}};
     if(($Support_Dept_Num != 0) || ($Support_Grade_Num != 0) || ($Support_Class_Num != 0)){
       if($Support_Dept_Num == 0){
         $Support_Dept="所有系所";
       }else{
         for($i=0; $i < $Support_Dept_Num; $i++){
           %the_Dept=Read_Dept($the_Course{support_dept}[$i]);
           $Support_Dept = $Support_Dept."[".$the_Dept{cname2}."]";
         }
       }
       if($Support_Grade_Num == 0){
         $Support_Grade="所有年級";
       }else{
         for($i=0; $i < $Support_Grade_Num; $i++){
           $Support_Grade = $Support_Grade."[". $the_Course{support_grade}[$i] ."]";
         }
       }
       if($Support_Class_Num == 0){
         $Support_Class="所有班別";
       }else{
         for($i=0; $i < $Support_Class_Num; $i++){
           $Support_Class = $Support_Class."[". $the_Course{support_class}[$i] ."]";
         }
       }

     }else{
       $Support_Dept="無";
       $Support_Grade="無";
       $Support_Class="無";
     }
  ########################
  ####    擋修解碼    ####
     $Ban_Dept_Num = @{$the_Course{ban_dept}};
     $Ban_Grade_Num = @{$the_Course{ban_grade}};
     $Ban_Class_Num = @{$the_Course{ban_class}};
     if(($Ban_Dept_Num != 0) || ($Ban_Grade_Num != 0) || ($Ban_Class_Num != 0)){
       if($Ban_Dept_Num == 0){
         $Ban_Dept="所有系所";
       }else{
         for($i=0; $i < $Ban_Dept_Num; $i++){
           %the_Dept=Read_Dept($the_Course{ban_dept}[$i]);
           $Ban_Dept = $Ban_Dept."[".$the_Dept{cname2}."]";
         }
       }
       if($Ban_Grade_Num == 0){
         $Ban_Grade="所有年級";
       }else{
         for($i=0; $i < $Ban_Grade_Num; $i++){
           $Ban_Grade = $Ban_Grade."[".$the_Course{ban_grade}[$i]."]";
         }
       }
       if($Ban_Class_Num == 0){
         $Ban_Class="所有班級";
       }else{
          for($i=0; $i < $Ban_Class_Num; $i++){
           $Ban_Class = $Ban_Class."[".$the_Course{ban_class}[$i]."]";
         }
       }
     }else{
       $Ban_Dept="無";
       $Ban_Grade="無";
       $Ban_Class="無";
     }
  ########################
@Principle=("不需篩選","一次篩選","二次篩選");

#####  (暑修的)第一類/第二類課程  Added 2009/05/20 Nidalap :D~
if( is_Summer() and !is_GRA() ) {       ### 只作用於「一般生暑修」
  @flag_remedy = ("",
      "第一類課程：經系（所、中心）課程委員會議審議通過之選修課程",
      "第二類課程：曾開授之課程，以補救教學為原則");
  $the_Course{note} = $flag_remedy[$the_Course{remedy}] . $the_Course{note};
}

if($the_Course{note} eq ""){
  $the_Course{note} = "無";
}
########################################
%cge = Read_Cge();
###########################################################
#####  產生 $Prerequisite_Course
if( (${${$the_Course{prerequisite_course}}[0]}{dept} ne "99999") and (${${$the_Course{prerequisite_course}}[0]}{dept} ne "") ) {
  $note_string .= "";
  foreach $pre_course (@{$the_Course{prerequisite_course}}) {
    %pre_course = Read_Course( $$pre_course{dept}, $$pre_course{id}, "01" ,"history", "", "");   ##  可能有問題！？ 2010/01/05
    $Prerequisite_Course = $Prerequisite_Course . "(" . $$pre_course{id} . ")" .
                           $pre_course{cname} . "(" . $GRADE{$$pre_course{grade}} . ")<BR>";
  }
  if($the_Course{prerequisite_logic} eq "OR") {
    $Prerequisite_Course .= "($PREREQUISITE_LOGIC{OR})";
  }else{
    $Prerequisite_Course .= "($PREREQUISITE_LOGIC{AND})";
  }
}else{
  $Prerequisite_Course = "無";
}

#####  如果是學系服務學習課程，依照學期顯示不同訊息
$note_string = $the_Course{note};
$dept_serv_course_id = Get_Dept_Serv_Course_ID($Input{dept});
if( $dept_serv_course_id eq $the_Course{id} ) {
  if( $TERM == 1 ) {
    $temp = "單號";
  }else{
    $temp = "雙號";
  }
  $note_string = "限本系一年級" . $temp . "學生修讀; " . $note_string;
}


###########################################################
$online_help = Online_Help();
$show_help{'support_dept'}	= Show_Online_Help('SUPPORT_DEPT');
$show_help{'ban_dept'}		= Show_Online_Help('BAN_DEPT');
$show_help{'reserved_number'}	= Show_Online_Help('RESERVED_NUMBER');
$show_help{'principle'}		= Show_Online_Help('PRINCIPLE');
$show_help{'prerequisite_course'} = Show_Online_Help('PREREQUISITE_COURSE');
$show_help{'note'}		= Show_Online_Help('NOTE');

if( is_Undergraduate_Dept($Input{dept})==0 ) {
  $attr_html = "<tr> <th>開課學制 </th><td>$ATTR{$the_Course{attr}}</td></tr>";
}else{
  $attr_html = "";
}

print << "End_of_HTML"
<html>
$online_help
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>
<body background="$GRAPH_URL/ccu-sbg.jpg">
<center>
    $HEAD_DATA
    <hr><br>
    <font size=4>其他相關備註資料</font><br><p>
    <table width=640 border=0>
    <tr>
    <th>科目</th><td align=left>$the_Course{cname}</td>
    <th>代碼</th><td align=left>$the_Course{id}</td>
    <th>班別</th><td align=left>$the_Course{group}班</td>
    </tr>
    </table>
    <table border=1 width=640>
      <tr> <th width=30%>限修人數</th><td>$the_Course{number_limit}</td> </tr>
      <tr> <th>支援系所 $show_help{'support_dept'}</th><td>$Support_Dept</td></tr>
      <tr> <th>支援年級</th><td>$Support_Grade</td></tr>
      <tr> <th>支援班別</th><td>$Support_Class</td></tr>
      <tr> <th>擋修系所 $show_help{'ban_dept'}</th><td>$Ban_Dept</td></tr>
      <tr> <th>擋修年級</th><td>$Ban_Grade</td></tr>
      <tr> <th>擋修班別</th><td>$Ban_Class</td></tr>
      <tr> <th>保留本系名額 $show_help{'reserved_number'} </th><td>$the_Course{reserved_number}</td> </tr>
      <tr> <th>篩選原則 $show_help{'principle'} </th><td>$Principle[$the_Course{principle}]</td></tr>
      $attr_html
      <tr> <th>支援通識科目</th><td>$cge{$the_Course{support_cge_type}}{cge_name}</td></tr>
      <TR> <TH>支援通識人數</TH><TD>$the_Course{support_cge_number}</TD></TR>
      <TR> <TH>先修科目 $show_help{'prerequisite_course'} </TH><TD>$Prerequisite_Course</TD></TR>
      <tr> <th>其他備註 $show_help{'note'} </th><td>$note_string &nbsp</td></tr>
    </table>
    <table width=640 border=0>
    <tr><th>
    <a href="javascript:history.back()">回上頁</a>
    </th></tr>
    </table>
</center>

</body>
</html>
End_of_HTML

