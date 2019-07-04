#!/usr/local/bin/perl
print("Content-type:text/html\n\n");

require "../library/Reference.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."GetInput.pm";
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
require $LIBRARY_PATH."Session.pm";

my(%Student,%Dept);

%Input=User_Input();
($Input{id}, $Input{password}, $login_time, $ip) = Read_Session($Input{session_id});
#print("session_id, id, pass = $Input{session_id}, $Input{id}, $Input{password}<BR>"); 

%Student=Read_Student($Input{id});
%Dept=Read_Dept($Student{dept});

Check_Student_Password($Input{id}, $Input{password});

@MyCourse=Course_of_Student($Student{id});
my($HEAD_DATA)=Head_of_Individual($Student{name},$Student{id},$Dept{cname},$Student{grade},$Student{class});

#############  �D�t�έ��w�ɶ����i�h��  #####################
if($SUPERUSER != 1){     ## �D superuser ���ϥΪ�
  if( (Whats_Sys_State()==0)or(Whats_Sys_State()==1)or(Check_Time_Map(%Student)!=1) ){
    Enter_Menu_Sys_State_Forbidden($HEAD_DATA);
  }
}
###########################################################

if(not defined $Input{DelCourse}){
    my($Table_Data)=CREAT_COURSE_TABLE();
    MAIN_DEL_HTML($HEAD_DATA,$Table_Data);
}else{
    DELETE_COURSE();
    @MyCourse=Course_of_Student($Student{id});
    my($Table_Data)=CREAT_COURSE_TABLE();
    MAIN_DEL_HTML($HEAD_DATA,$Table_Data);
}




sub MAIN_DEL_HTML
{
my($HEAD_DATA,$DATA)=@_;
my($NEXT_URL)="Del_Course00.cgi";
my($LINK)=Select_Course_Link($Input{id},$Input{password});

print << "End_of_HTML"
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <TITLE>�h����</TITLE>
</head>
<body background="$GRAPH_URL./ccu-sbg.jpg">
<center>
    $HEAD_DATA 
    <hr>
    <form action="$NEXT_URL" method="post" name="WorkForm">
    $DATA
    <input type="hidden" name="session_id" value="$Input{session_id}">
    <input type="submit" value="�T�w�R���аO�����">
    </form>
</center>
$LINK
</body>
</html>
End_of_HTML
}
################################################################
##################    ���ͥD�n��ҳ檺���    ##################
################################################################
sub CREAT_COURSE_TABLE
{
my($DATA)="";
my(@Teachers)=Read_Teacher_File();
my(@WeekDay)=@WEEKDAY;
my(@TimeMap)=@TIMEMAP;
$MyCount=@MyCourse;
@Credit=CREDIT_TABLE();

  $DATA = $DATA."<table width=640 border=1>\n";
  $DATA = $DATA."<tr>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>�аO</font></th>";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>��ئW�٤ΥN�X</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>�½ұЮv</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>�Z�O</font></th>";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>�Ǥ�</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>�Ǥ��k��</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>�P���`��</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>�Ы�</font></th>\n";
  $DATA = $DATA."</tr>\n";

  ####  �C�L�����ҵ{���  ####
  for($i=0; $i < $MyCount; $i++){
      my(%theCourse)=Read_Course($MyCourse[$i]{dept},$MyCourse[$i]{id},$MyCourse[$i]{group},"");
      my($value)=$theCourse{dept}."_".$theCourse{id}."_".$theCourse{group};
      $DATA = $DATA."<tr>\n";
      $DATA = $DATA."<th><input type=checkbox name=DelCourse value=\"";
      $DATA = $DATA.$value;
      $DATA = $DATA."\"></th>\n";

      $DATA = $DATA."<th><font size=2>";
      $DATA = $DATA.$theCourse{id}."<br>";
      $DATA = $DATA.$theCourse{cname}."</font></th>\n";

      $DATA=$DATA."<th><font size=2>";           ##  �½ұЮv
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
      $DATA=$DATA."</font></th>\n";


      $DATA = $DATA."<th><font size=2>";
      $DATA = $DATA.$theCourse{group}."</font></th>\n";
      $DATA = $DATA."<th><font size=2>";
      $DATA = $DATA.$theCourse{credit}."</font></th>\n";
      $DATA = $DATA."<th><font size=2>";
      $DATA = $DATA.$Credit[$MyCourse[$i]{property}];
      $DATA = $DATA."</font></th>\n";

      $DATA=$DATA."<th><font size=2>";           ## �P���`��
      $time_string = Format_Time_String($theCourse{time});
      $DATA .= $time_string;
      $DATA=$DATA."</font></th>\n";

      $DATA=$DATA."<th><font size=2>";           ##  �Ы�
      %Room=Read_Classroom($theCourse{classroom});
      $DATA=$DATA.$Room{cname};
      $DATA=$DATA."</font></th>\n";

      $DATA = $DATA."</tr>\n";
  }

  $DATA = $DATA."</table>\n";

return($DATA);
}
################################################################
##################       �R����ܪ����       ##################
################################################################
sub DELETE_COURSE
{
#  print("<font color=RED>�ثe�ëD�[�h��ɬq, ����!<br></font>\n");
    @Courses=split(/\*:::\*/,$Input{DelCourse});
    foreach $course(@Courses){
        my($dept,$id,$group)=split(/_/,$course);
        Delete_Student_Course($Input{id},$dept,$id,$group);
    }
}

