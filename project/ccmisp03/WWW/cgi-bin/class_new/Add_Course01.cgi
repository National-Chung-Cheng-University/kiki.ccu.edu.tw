#!/usr/local/bin/perl
###########################################################################################
#####  Add_Course_01.cgi
#####  �B�z�ǥͥ[����
#####  ���� Add_Course_00.cgi �ǨӪ����, �P�_�ǥͿ�Ҹ�ƦX�k��
#####  (�K�X, �׭�, ���פH�� etc), �M�w�O�_�[�����ܶ}�Ҹ�ƺ���
#####  Coder   : Nidalap :D~
#####  Modified: Jan 10/2001
#####            2008/06/03  �W�[����ǵ{�\��, ��V�� Show_All_GRO.cgi	Nidalap :D~
#####		 2008/08/05  �W�[�s���e�� Ecourse �ҵ{�j��			Nidalap :D~
#####		 2008/09/01  ��|�ҵ{�����W��, �Ԩ� CHECK_VALID_SELECT_COURSE() Nidalap :D~
###########################################################################################
print("Content-type: text/html\n\n");

require "../library/Reference.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."System_Settings.pm";
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
%time = gettime();

###################    Ū���ϥΪ̿�J���    ######################
%system_flags = Read_System_Settings();
%Input=User_Input();
($Input{id}, $Input{password}, $login_time, $ip, $add_course_count) = Read_Session($Input{session_id}, 1);
#print("session_id, id, pass = $Input{session_id}, $Input{id}, $Input{password}<BR>"); 

#if( length($Input{dept}) == 2 ) {		###  ����ǵ{
#  print qq (Location: Show_All_GRO.cgi?gro_id=$Input{dept} );  
#}else{
#  print("Content-type: text/html\n\n");
#}

%Student=Read_Student($Input{id});
%Dept=Read_Dept($Student{dept});
%SelectDept=Read_Dept($Input{dept});

Check_Student_Password($Input{id}, $Input{password});
my($HEAD_DATA)=Head_of_Individual($Student{name},$Student{id},$Dept{cname},$Student{grade},$Student{class});

if($add_course_count >= $ADD_COURSE_LIMIT) {
  Session_Add_Course_Limit($system_flags{black_list}, $time{time_string}, $Input{id}, $ip);
}
$add_course_count ++  if($Input{SelectTag} == 1);
Write_Session($Input{session_id}, $Input{id}, $Input{password}, $add_course_count);

###################    �Y�D��Үɶ��h��ܤ��i�i�J  ################
if($SUPERUSER != 1){     ## �D superuser ���ϥΪ�
  if( (Whats_Sys_State()==0)or(Whats_Sys_State()==1)or(Check_Time_Map(%Student)!=1) ){
    Enter_Menu_Sys_State_Forbidden($HEAD_DATA);
  }
}
###################    ���w���i�ϥ�GET, �@�ߥ�POST  ###################
#if( $ENV{REQUEST_METHOD} ne "POST" ) {
#  Enter_Menu_Sys_State_Forbidden($HEAD_DATA);
#}
#######################################################################
########    �P�_�ϥΪ̬O�_����s�ҥH�W�ǥ�    ########
########    �p�G�O�A�h�~�Ť@�߬��@�~��        ########
########    ���ҰȲջݨD�N�����󭭨�h��      ########
#if($Input{dept}%10 > 4){
#    $Input{grade}=1;
#}
###########################################################################
####    �ŧi�����ܼ� (Golobal Variable)    ####
my($ERROR_DATA_1)="";                  ##�����İ��ˬd�ɵo�ͽİ󪺬�ذT��

my($Current_Page)=$Input{page};
my($TotalPages)=0;
Read_Student_State_Files();            ### Ū�����t���D�צW��->�����ܼ� %FU,%DOUBLE

if( ($Input{dept} eq "6104") or ($Input{dept} eq "6154") or
    ($Input{dept} eq "6204") ) {
                                                ### �p�G�}�Ҩt�ҬO�k�ߨt���@��
  if( ($FU{$Student{id}} eq "6054") or ($FU{$Student{id}} eq "3254") ) {
                                                ### �B�ǥͬO�k�ߨt���t��  
    $FU{$Student{id}} = $Input{dept};           ### �h���P�O�Ӳժ����t��
  }
}
if( $Input{dept} =~ /^5/ ) {          ###  �p�G�}�Ҩt�ҬO�ް|��     
  if( $FU{$Student{id}} =~ /^5/ ) {   ###  �p�G�ǥͬO�ް|���@�t�����t��
    $FU{$Student{id}} = $Input{dept}; ###  �h���P�O�Ӳժ����t��(�ް|�ҵ{��X)
  }
  if( $DOUBLE{$Student{id}} =~ /^5/ ) {   ###  �p�G�ǥͬO�ް|���@�t�����D�ץ�
    $DOUBLE{$Student{id}} = $Input{dept}; ###  �h���P�O�Ӳժ����D�ץ�(�ް|�ҵ{��X)
  }
}

############################################################################

####    �ǥͦ~�ŬO�_�ݭn�۰ʤɯŤ��P�_    ####
####    �ϥήɾ��G���@�Ǧ~�}�l�e�ϥ�      ####
if( is_Grade_Update() == 1){
  $Student{grade}++;
  $Student{grade}=4  if( $Student{grade} > 4 );  ### 2004/06/07�o�{BUG��s
}

####    �إ� HTML �ɮת����Y����    ####
####    �]�A�ϥΪ̪�������Ƶ�      ####

#############################################################################
####    ���{�����֤߽ХѦ��B�ۤ⩹�U�ݦU�Ӭ������禡                     ####
#############################################################################
########    �P�_�O�_�ݭn�B�z��Ҹ��    ########

if($system_flags{black_list} == 1) {
  $ban_time = Read_Ban_Record($Student{id}, $BAN_COUNT_LIMIT);	### ���v�|���h�[��_(�j��0�N�O���v��)
  if( $ban_time > 0 ) {
    Show_Ban_Message($ban_time, 1);
  }
}
if($Input{SelectTag} == 0 or not defined $Input{SelectTag}){
    $Current_Page++;      ####    Ū���U�@��    ####
    VIEW_COURSE();
}else{                    ####    ���B�z��ҵ{�ǡA�AŪ����ҫ���    ####
    SELECT_COURSE($HEAD_DATA,$Input{dept},$Input{course});
    VIEW_COURSE();
}
#############################################################################
#############################################################################
#####  SELECT_COURSE()
#####  �Y�ǥͦ����(Input{SelectTag}���]�w), ���B�z��Ҹ��
#####  ���P�_��Ҹ�ƪ��X�k��, �A�i���ҩΦ^�����~�T��.
#####  ��s: �N�P�_�X�k�ʪ��{����b�P�@�j�餺, �H��֦h���I�sRead_Course()
#####        �y�����h�lIO��C�t�� (Nidalap, Jan10/2001)
#############################################################################
sub SELECT_COURSE
{
  my($HEAD_DATA, $course_stream);
  ($HEAD_DATA,$course_dept,$course_stream)=@_;
  @Courses=split(/\*:::\*/,$course_stream);
  my(@Courses_Data, $valid_flag, $valid_string);
  my($count)=0;

  ($valid_flag, $valid_string) = CHECK_VALID_SELECT_COURSE(@Courses);
  if($valid_flag == 0) {                                        ### �Y��Ҹ�Ƥ��X�k
    REPORT_ERROR($valid_string);
  }else{                        		                ### �Y��Ҹ�ƦX�k                                
    foreach $course(@Courses){
      my($id,$group)=split(/_/,$course);
      %the_Course=Read_Course($course_dept,$id,$group,"",$Input{id});
                                          ## �ǥͿ諸�Ҧ��Y�@�������ױ���, �N������W���ĵ�T
      if( $pre_course_count == 0 ) {
         $pre_course_count = @{$the_Course{prerequisite_course}};
         if($the_Course{prerequisite_course}[0]{dept} eq "99999") {
           $pre_course_count = 0;
         }
      }
      Add_Student_Course($Input{id},$course_dept,$id,$group,$Input{$course});
#      $add_course_count ++;
#      Write_Session($Input{session_id}, $Input{id}, $Input{password}, $add_course_count);
    }
  }
}
###########################################################################################
#####  CHECK_VALID_SELECT_COURSE
#####  �P�_��Ҹ�ƦX�k��
#####  ������ƭ��ˬd�禡, ���C�ӳ��|�AŪ�Ʀ�Read_Course()�y���{���C, 
#####  �ҥH�N�ƭ��ˬd�ﰵ�b�@�_, ���IO�W�i�t�׮į�
#####  �ˬd�����ئ�:
#####     a. ��ؽİ�	: ���i��
#####     b. �ݩʦ��~	: ���i��
#####     c. �׭�	: ���޲z�̥~���i��
#####     d. �W�L25�Ǥ�	: ���޲z�̥~���i��
#####     e. ���פH��	: ���t�έ��ױ���(�޲z�̤��b����)
#####     f. �M�Z���o��~�� : �]�A�M�Z�αM�Z����(�޲z�̤��b����)
#####     g. �q�Ѥ��ߤ��}��j�|(���޲z���]�w�өw)
#####     h. �̷Ӻ޲z�̳]�w�}��Τ��}��ƾǨt���ҩM�D�ƾǨt����
#####     i. �C�Ǵ��ȭ��פ@��������|(2008/09/01)
#####     j. ��|�ҥi�U�פ��i�W��(��~��)
#####  ��J: (@Courses)                     ## �ǥ��I��n�ת����
#####  ��X: ($valid_flag, $valid_string)   ## $valid_flag:(0,1) = (���X�k, �X�k)
#####  Jan10/2001��g(Nidalap:D~)
###########################################################################################
sub CHECK_VALID_SELECT_COURSE
{
  my($id, $group, %The_Course);
  my($conflict_flag, $property_flag, $ban_flag, $credit_25_limit_flag, $number_limit_flag);
  local($conflict_string, $valid_string);
  local $total_credit = 0;
  local $valid_flag = 1;                                               ###  �w�]��Ҹ�Ƭ��X�k
  local(@time_map);            ###  �ΰ��ˬd�İ󪺰}�C, Check_Course_Conflict()�|��ʤ�
  local(@Course_of_Student);   ###  �ΰ��ˬd�İ��25�Ǥ��W��, �ǥͦ��w��ת����
  my(@Courses) = @_;
  
  ####################  �ˬd�ǥͦ��w�ײߪ���, �إ�@time_map�ΰO��Ǥ�  ####################
  @Course_of_Student = Course_of_Student($Student{id});
  foreach $stu_course (@Course_of_Student) {
    %The_Course = Read_Course($$stu_course{dept}, $$stu_course{id}, $$stu_course{group}, "", $Student{id});
    $total_credit += $The_Course{credit};
    my $course_identifier = join("_", $$stu_course{dept}, $$stu_course{id}, $$stu_course{group});
    ($conflict_flag, $conflict_string) = Check_Course_Conflict(%The_Course);
    if( $conflict_flag == 1 ) {
      return("0", $conflict_string);
    };
  }
  #######################  �B�z�ǥͥثe�ҿ諸��, �ˬd�X�k��  #######################
  foreach $course (@Courses) {
    ($id, $group) = split(/_/, $course);
    %The_Course = Read_Course($course_dept, $id, $group, "", $Student{id});
    ################  �ˬd�ǥͥثe�ҿ諸��, �إ�@time_map�ΰO��Ǥ� ################
    ($conflict_flag, $conflict_string) = Check_Course_Conflict(%The_Course);
    if( $conflict_flag == 1 ) {
      return("0", $conflict_string);
    };
    ################  �ˬd�Ǥ��k�ݬO�_����  ################################################
    ################  ps. �i�諸���bShow_Property_Select�w�]�n�F, �b�������|���������  ############
    $property_flag = Check_Property($The_Course{property}, $Input{$course});
    if($property_flag != 99) {
      return("0", "�z�諸��إ����T����Ǥ��k��");
    }
    ####################################################################################
    $ban_flag = Check_Ban_Limit(%The_Course);
    if( $ban_flag == 1 ) {
      return("0", "�z�ҿ諸���<FONT color=RED>���׭�</FONT>, �H�P��z�L�k�[��");
    }
    ####################################################################################
    $credit_25_limit_flag = Check_Credit_Upper_Limit($Student{id}, $total_credit, $The_Course{credit});
    if( $credit_25_limit_flag == 0 ) {
      return("0", "�z�ҿ諸���<FONT color=RED>�Ǥ��Ƥw�g�L�h</FONT>");
    }else{
      if( ($total_credit + $The_Course{credit} > 25) and ($SUPERUSER == 1) ) {
        print("<FONT color=RED>NOTE: �z�諸�Ǥ��Ƥw�g�W�L25�Ǥ�!</FONT><BR>");
      }
      $total_credit += $The_Course{credit};     ####  �Y�ǥͤ@����h���ҾǤ��n���Ʋ֥[
    }
    ####################################################################################
    $number_limit_flag = Check_Number_Limit($Student{id}, %The_Course);
    if( $number_limit_flag == 0 ) {
      return("0", "�z�諸���<FONT color=RED>�ثe��ҤH�Ƥw��,</FONT>");
    }
    ####################################################################################
    ####  2003/09/09 �Ȯɭק�!
#    if( ($The_Course{id} eq "7102001") and ($The_Course{group} eq "02") ) {
#      return("0", "����اY�N����, �Фſ�ץ����");
#    }
    
  }
  #################################################################################
  if( $SUPERUSER != 1 ) {
    if( ($SUB_SYSTEM==3) or ($SUB_SYSTEM==4) ) {      ### �M�Z�αM�Z����, ���o��~��
      if($Student{dept} ne $Input{dept}) {
        return("0", "�M�Z�P�ǽФŭײߥ~�ҽҵ{!");
      }
    }
  }
  ######################################################################################
  if( $SUPERUSER != 1 ) {
    if( $Input{dept} eq "7006" ) {
      if( $system_flags{cge_ban_grade} == 1 ) {
        if( $Student{grade} == 4 ) {
          return("0", "�Ĥ@���q�q�ѽҵ{���}��j�|�ͭײ�!");
        }
      }elsif( $system_flags{cge_ban_grade} == 2 ) {
        if( ($Student{grade} == 3) or ($Student{grade} == 4) ) {
          return("0", "�Ĥ@���q�q�ѽҵ{���}��j�|�ͭײ�!");
        }
      }
    }
  }
  ######################################################################################
  if( $SUPERUSER != 1 ) {
    if( ($system_flags{allow_select_math} == 1) and (is_Math_Dept($Input{dept})) ) {
      return("0", "�ثe�t�Τ��}���׼ƾǨt�Ҷ}�]�����, �Щ�}��������!");
    }elsif( ($system_flags{allow_select_math} == 2) and (not is_Math_Dept($Input{dept})) ) {
      return("0", "�ثe�t�Τ��}���׫D�ƾǨt�Ҷ}�]�����, �Щ�}��������!");
    }
  }
  ######################################################################################
  ###  �Ш|�ǵ{�}�]���, �u���֦��Ш|�ǵ{���̥i�H�ײ�(Added 2003/09/09, Nidalap :D~)
  if($SUPERUSER != 1) {
    if( ($Input{dept} eq "7306") or ($Input{dept} eq "3546") ) {
      my($is_teacher_edu);
      $is_teacher_edu = is_Teacher_Edu($Student{id});
      ###  ���t�X�³W�w, �Ш|�t�Ұ��~�ťH�W���]�i�ױШ|�ǵ{�Ҷ}�]�ҵ{
      ###  2004/06 �������W�w, �ȱШ|�ǵ{�ǥͥi��פ� :D~
#      if( $Student{dept} =~ /^7/ )  {
#        if( ($YEAR - $Student{grade}) <= 90 )  {    ###  92_1 ��, �G�~�ťH�W���Ш|�ǰ|�ǥ�
#          $is_teacher_edu = 1;
#        }
#      }
      
      if($is_teacher_edu != 1) {
        return("0", "�Ш|�ǵ{�}�]���, ���֦��Ш|�ǵ{���̭ײ�!");
      }
    }
  }
  ######################################################################################
  ###  ��|�Ҭ�������  (Added 2008/09/01, Nidalap :D~)
  ###  1. �C�Ǵ��ȭ��פ@��������|
  if($SUPERUSER != 1) {
    if( $The_Course{id} =~ /^902(1|2)/ ) {		### 9021, 9022 ���O�O���@�~��, �G�~�Ū�
      foreach $stu_course (@Course_of_Student) {
        if( $$stu_course{id} =~ /^902(1|2)/ ) { 
          return("0", "�C�@�Ǵ��ȭ��פ@��������|�ҵ{!");
        }
      }
    }
    ###  2. ��|�ҥi�U�פ��i�W��(��~��) 
    if( $The_Course{id} =~ /^902(.)/ ) {		### ��إN�X�ĥ|�X, ���ӻP�~�Ŭۤ��
      if( ($Student{grade} < $1) and ($Student{id} =~ /^4/) ) {
        return("0", "��|�ҵ{�i�U��, �����i�W��!");
      }
    }
    
  }    

  ######################################################################################
  ### �}���j�@���x�V�Ҥ����s�Ϳﭭ��(Added 2004/06/07, Nidalap :D~)
  ### ���W�w�w����(2006/04/18, Nidalap :D~)
  #if( $id =~ /^9031/ ) {
  #  if( $Student{id} !~ /^4/ ) {
  #    return("0", "��s�ҦP�ǽФſ�׶}�]���j�@���x�V�ҵ{!");
  #  }
  #  elsif( $Student{grade} == 2 ) {    
  #    return("0", "�j�G�P�ǽФſ�׶}�]���j�@���x�V�ҵ{");        
  #  }   
  #}
  #if( $id =~ /^9032/ ) {
  #  if( ($Student{id} =~ /^4/) and ($Student{grade} == 1) ) {
  #    return("0", "�j�@�P�ǽФſ�׶}�]���j�G���x�V�ҵ{");
  #  }
  #}
  
  return($valid_flag, $valid_string);      ###  �ˬd�X�k�Ǧ^��
}

############################################################################################
#####  Check_Course_Conflict
#####  �ˬd��ؽİ�
#####  �ˬd�C�Ӭ�ت��ɬq, �N�ɬq�[�J@time_map�}�C, �p�G�}�C���w���ȫh�P�_�İ�.
#####  ���ˬd�w�ײߪ����, �O�_�w�g���İ󱡧�(�i��]����ز���),
#####  �A�ˬd�ǥͩҿ諸���.
#####  ��J	    : %The_Course
#####  ��X	    : ($conflict_flag, $conflict_string)   $conflict_flag:(0,1)=(����, �İ�)
#####  �ϥ�local�ܼ�: @time_map, @Student_Course
############################################################################################
sub Check_Course_Conflict
{
  my(%The_Course) = @_;
  my($conflict_flag, $conflict_string);
#  print("Checking $The_Course{id} _ $The_Course{group}<br>\n");

  my $course_identifier = join("_", $The_Course{dept}, $The_Course{id}, $The_Course{group});
  foreach $course_time (@{$The_Course{time}}) {
#    print("Checking time [$$course_time{week}][$$course_time{time}]<br>\n");
    ($conflict_flag, $conflict_string) = 
         Check_and_Modify_Time_Map($$course_time{week}, $$course_time{time}, $course_identifier);
    if($conflict_flag == 1) {
      return(1, $conflict_string);
    }
  }
}
############################################################################################
#####  Check_and_Modify_Time_Map
#####  �ˬd�ɶ��Ĭ�
#####  �ѶǤJ���P���X�ĴX��ɶ�, ���C�@��@time_map�������, �öǦ^�O�_�İ󪺰T��
#####  ��J         : ($week, $time, $course_identifier)
#####  ��X	    : ($conflict_flag, $conflict_string)          $flag:(0,1) = (����, �İ�)
#####  �Ψ�local�ܼ�: @time_map
############################################################################################
sub Check_and_Modify_Time_Map
{
  my($week, $time, $course_identifier) = @_;
  my($conflict_string, $flag, $size);

  foreach $ut (@time_map) {           ### �ˬd�C�@�Ӥw�g�α����ɶ�, $ut = used_time
    $flag = is_Time_Collision($$ut{week}, $$ut{time}, $week, $time);
    if( $flag != 0 ) {                ###   �Y���İ󱡧�...
      $conflict_string = "�z�ҿ諸���(�έ���w����)���İ󱡧�:<BR>";
      $conflict_string .="<FONT color=RED>(�P��$WEEKDAY[$$ut{week}]���� $$ut{time} ��)";
      $conflict_string .=" �P (�P��$WEEKDAY[$week]���� $time ��)"; 
      last;
    }
  }
  if( $flag == 0 ) {                  ###  �Y�ˬd�L�~, �N���ɬq�Ь��w��
    $size = @time_map;
    $time_map[$size]{week} = $week;
    $time_map[$size]{time} = $time;
    return(0, "");
  }else{                              ###  �Y�ˬd���~, �^�п��~�T��
    return(1, $conflict_string);
  }

#  if( $time_map{$week}{$time} eq "" ) {                              ### �p�G�Ӯɬq�O�Ū�
#    $time_map{$week}{$time} = $course_identifier;
#    return(0, "");
#  }else{                                                             ### �p�G�Ӯɬq�w�Q��
#    $conflict_string = "�z�ҿ諸��ةέ���w���ئb<BR><FONT color=RED>�P�� $week ���� $TIMEMAP[$time] ��</FONT>���İ󱡧�.";
#    return(1, $conflict_string);
#  }
}
############################################################################################
#####  Check_Ban_Limit
#####  �ˬd�׭רt�Ҧ~�ůZ�O
#####  �ˬd�ǥͿ�ת����, �O�_�����w�׭רt�Ҧ~�ůZ�O. �p�G��, �P�_�ӥͨ���,
#####  �P�_�O�_�i���. (�޲z�̤��b����)
#####  �u�n�t�Ҧ~�ůZ�O���@������, ��L�S�諸���P������. �T�̥HAND�s��
#####  ��J	 : %The_Course
#####  ��X	 : $ban_flag                       $ban_flag:(0,1) = (����, �׭�)
#####  �Ψ�global: %Student
############################################################################################
sub Check_Ban_Limit()
{
  my($Ban_Dept_Num, $Ban_Grade_Num, $Ban_Class_Num);
  my($L1, $L2, $L3);
  my(%The_Course) = @_;
  
  $Ban_Dept_Num = @{$The_Course{ban_dept}};
  $Ban_Grade_Num = @{$The_Course{ban_grade}};
  $Ban_Class_Num = @{$The_Course{ban_class}};
  
  if( ($Ban_Dept_Num==0) and ($Ban_Grade_Num==0) and ($Ban_Class_Num==0) ) {
    return(0);                       ##  ���׭�, return
  }else{                             ##  �׭�, �~���ˬd
    if($Ban_Dept_Num == 0){             ##  �p�G�S���ɨt�ҡA�h�w�]���Ҧ��t��
      @Ban_Dept=Find_All_Dept();
    }else{
      @Ban_Dept=@{$The_Course{ban_dept}};
    }

    if($Ban_Grade_Num == 0){            ##  �p�G�S���צ~�šA�h�w�]���Ҧ��~��
      @Ban_Grade=(1,2,3,4,5,6,7,8,9,10);
    }else{
      @Ban_Grade=@{$The_Course{ban_grade}};
    }

    if($Ban_Class_Num == 0){            ##  �p�G�S���ׯZ�šA�h�w�]���Ҧ��Z��
      @Ban_Class=(A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z);
    }else{
      @Ban_Class=@{$The_Course{ban_class}};
    }
    $L1=$L2=$L3=0;

    foreach $item (@Ban_Dept){
      if($item eq $Student{dept}){
        $L1 = 1;
      }
    }

#    print("fu : $FU{$Student{id}}<BR>");
#    print("double : $DOUBLE{$Student{id}}<BR>");
#    print("this : $The_Course{dept}<BR>");
    if( ($The_Course{dept} eq "6104") or ($The_Course{dept} eq "6154") or
        ($The_Course{dept} eq "6204") ) {       ### �p�G�}�Ҩt�ҬO�k�ߨt���@��
       if( $FU{$Student{id}} eq "6054" ) {      ### �B�ǥͬO�k�ߨt���t��  
         $FU{$Student{id}} = $The_Course{dept}; ### �h���P�O�Ӳժ����t��
       }   
    }  
    if( $FU{$Student{id}} eq $The_Course{dept}) {
      $L1 = 0;                            ##  ���t�����׭רt�ҭ���2002/02/26
    }
    if( $DOUBLE{$Student{id}} eq $The_Course{dept}) {
      $L1 = 0;                            ##  ���D�פ����׭רt�ҭ���2002/02/26
    }

    foreach $item(@Ban_Grade){            ##  �n�b�N�A�ɯū�P�ɯūe���P...
      if($item eq $Student{grade} ){      ##  �p�ߡA���b�N�|�o�ͭ��j�M��...
        $L2 = 1;
      }
    }
    foreach $item(@Ban_Class){
      if($item eq $Student{class}){
        $L3 = 1;
      }
    }

    if(($L1 == 1) && ($L2 == 1) && ($L3 == 1)){   ###  �ǥͲŦX�׭רt�Ҧ~�ůZ��
      if( $SUPERUSER == 1 ) {                ##  �޲z�̤��׭�
        return(0);
      }elsif($system_flags{no_ban} == 1) {   ##  �Y�]�w�ĤG���q�]�w�׭׵L��:
        if( $Ban_Dept_Num < 10 ) {           ##    -> �׭רt�Ҥ֩� 10 ��(���P�󭭥��t), �n�ɭ�
          return(1);
        }elsif( ($The_Course{dept} eq "V000") or ($The_Course{dept} eq "7006") ) {
          return(1);                         ##    -> �x�V�P�q�Ѥ��n�׭�
        }else{
          return(0);                         ##    -> ��L�ҵ{�̳]�w���׭�
        }
      }else{
        if( $TEMP_REMEDY_20040224 == 1 ) {      ### �ɱ� 20040224 �ƥ�
          ### �ˬd�ӦP�ǬO�_�b�ɱϦW�椺, ���\�����׭׭���(added 2004/06/08)
          my($temp_file, @temp_lines, $j, $temp_cid);
          $temp_file = $DATA_PATH . "20040224/" . $Student{id};
          if( -e $temp_file ) {
            open(TEMP_FILE, $temp_file);
            @temp_lines = <TEMP_FILE>;
            close(TEMP_FILE);
            foreach $temp_line (@temp_lines) {
              ($j, $temp_cid) = split(/\[/, $temp_line);
              ($temp_cid, $j) = split(/ /, $temp_cid);
#              print("allowed no-ban: $temp_cid <-> $The_Course{id}<BR>\n");
              if( $The_Course{id} eq $temp_cid ) {
                return(0);			## �b�ɱϦW�椺, ���׭�
              }
            }
          }
        }
        return(1);                           ##  �ŦX����, �n�׭�
      }
    }
  }
}
############################################################################################
#####  Check_Credit_Upper_Limit()
#####  �ˬd�Ǥ��W��(�{�b�W�w�O25�Ǥ�)
#####  ���޲z�̥~���o��׶W�L�Ǥ��W��
#####  ��s: �Ҽ{�ӧO�ǥ;Ǥ��W������(�b�޲z��椤�]�w) 2001/09/04 Nidalap
#####  ��J: ($total_credit, $The_Course{credit})
#####  ��X: $limit_flag                   $limit_flag:(0,1) = (�W�L, ���W�L)
############################################################################################
sub Check_Credit_Upper_Limit()
{
  my($upper_limit_file) = $REFERENCE_PATH . "credit_upper_limit.txt";
  my($temp_id, $temp_limit, $upper_limit);
  my( $student_id, $total_credit, $credit ) = @_;
  $upper_limit = 25;
  $total_credit += $credit;

  open(LIMIT, $upper_limit_file);      ###  �ˬd�ӧO�ǥ;Ǥ��W����
  @line = <LIMIT>;
  close(LIMIT);
  foreach $line (@line) {
    $line =~ s/\n//;
    ($temp_id, $temp_limit) = split(/\s+/, $line);
    if($temp_id eq $student_id) {
      $upper_limit = $temp_limit;
    }
  }

  if( $total_credit > $upper_limit ) {  
    if( $SUPERUSER == 1 ) {
      return(1);
    }else{
      return(0);
    }
  }else{
    return(1);
  }
}
############################################################################################
#####  Check_Number_Limit()
#####  �ˬd�׽ҤH�ƭ���
#####  �P�_�Ӭ�ت��׽ҤH��, ���ױ���, �H�Υثe�t�Ϊ����ױ���, �M�w�ӾǥͬO�_�i���
#####  
#####  ��J: ($student_id, %The_Course)
#####  ��X: $number_limit_flag         (0,1) = (�w��, ����)
############################################################################################
sub Check_Number_Limit()
{
  my ($stu_id, %The_Course) = @_;
  my($number, $limit_state, $flag, $upper_limit_immune_flag);
  $number = Student_in_Course($The_Course{dept}, $The_Course{id}, $The_Course{group}, "");
  $limit_state = Limit_State();
  
  $The_Course{number_limit} = 0		if( $The_Course{number_limit} eq "" );
  $The_Course{reserved_number} = 0	if( $The_Course{reserved_number} eq "" );

  $flag = 0;				####  �w�]�w�������
    
  if( $SUPERUSER == 1 ) {
    $flag = 1;
  }elsif( $The_Course{number_limit} == 0 ) {      ###  ���� 0 �H����������
    $flag = 1;
  }else{
    if( $limit_state == 0 ) {                     ###  �t�γ]�w������
      $flag = 1;      
    }elsif( $limit_state == 1 ) {                 ###  �t�γ]�w�Ҽ{�O�d�H��
      $upper_limit_immune_flag = Check_Course_Upper_Limit_Immune( $The_Course{id},
                                     $The_Course{group}, $stu_id);
      if( $upper_limit_immune_flag == 1 ) {
        $flag = 1;
      }
      if( $number < $The_Course{number_limit} - $The_Course{reserved_number} ) {
        $flag = 1;
      }
    }elsif( $limit_state == 2 ) {                 ### �t�γ]�w�ȦҼ{���פH��
      my($immune_count);                          ### �B���[ñ�����b��ҤH�Ƥ�
      $immune_count = Check_Course_Upper_Limit_Immune_Count($The_Course{id}, $The_Course{group}, "add");
      $immune_count=0  if($immune_count < 0);
      if( $number < ($The_Course{number_limit} + $immune_count) ) {
        $flag = 1;
      }
      $upper_limit_immune_flag = Check_Course_Upper_Limit_Immune( $The_Course{id},
                                     $The_Course{group}, $stu_id);  
      if( $upper_limit_immune_flag == 1 ) {
        Upper_Limit_Immune_Add($The_Course{id}, $The_Course{group}, $stu_id);
                                                  ###  ���[ñ���[��, �n�t�~����
        $flag = 1;
      }
    }
  }
#  print("upper_limit_immune_flag = $upper_limit_immune_flag<BR>\n");
  return($flag);
}
############################################################################################
#####  REPORT_ERROR()
#####  �^�����~�T��
#####  ��X���~�T��HTML���ǥ�, �i�������ҵL�k����.
#####  ��J: $error_string
#####  ��X: (none)
############################################################################################
sub REPORT_ERROR()
{
  my($error_string) = @_;
  
  print qq(
    <html>
      <head><meta http-equiv="Content-Type" content="text/html; charset=big5"></head>
      <body background="$GRAPH_URL./ccu-sbg.jpg">
        <center>
        $HEAD_DATA
        <hr><br>
        <font size=5>���~: $error_string</FONT><BR>
        <font size=5>��<a href="javascript:history.back()">���s���</a></font>
        </center>
      </body>
    </html>
  );
  exit();
}
############################################################################
############################################################################
#####   �ˬd����ݩʤξǤ��k��                                      
#####   ����ت��}���ݩ�, �ξǥͩҿ諸�Ǥ��k��, �öǦ^��ﵲ�G
#####   ��J: ($Property, $MyProperty)
#####   ��X: $result: (���T���ܶǦ^99)
############################################################################
sub Check_Property
{
  my($Property,$MyProperty)=@_;
  if($MyProperty == 0){                        ###  ������Ǥ��k��
    return 0;
  }
  if($MyProperty == 1 and $Property != 1){     ###  ����
    return 1;
  }
#  if( $MyProperty != 3 and $Property == 3){    ###  �q�Ѭ��
#    return 2;
#  }
  return 99;
}
#############################################################################
#############################################################################
sub VIEW_COURSE
{
@MyCourse=Course_of_Student($Student{id});
$MyCount=@MyCourse;
@Teachers=Read_Teacher_File();
my(@WeekDay)=("�@","�G","�T","�|","��","��","��");
my(@TimeMap)=(A,1,2,3,4,B,5,6,7,8,C,D,E);

if($Input{dept} eq "" or $Input{grade} eq ""){   ####  �å�����t�Ҧ~��  ####
    RESELECT($HEAD_DATA);                        ####  �Э��s���        ####
}else{
    @Course=Find_All_Course($Input{dept},$Input{grade},"");
    $Count=@Course;
    if(($Count % 10) == 0 && ($Count != 0)){
      $TotalPages=int($Count/10);
    }else{
      $TotalPages=int($Count/10)+1;
    }
  if($Count != 0){                               ####  ���`���p          ####
    ####  �קK���ƶW�L  ####                     ####  �i���`���        ####
    while($Current_Page*10 >= $Count+10){
        $Current_Page--;
    }

    my($DATA)="";

    $DATA = $DATA."<table width=800 border=1>\n";
    $DATA = $DATA."<tr>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>�аO</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>�ثe��פH��</font></th>";
    if( $system_flags{show_immune_count} == 1 ) {
      $DATA = $DATA."<TH bgcolor=YELLOW><FONT size=2>�i�[��W�B</FONT></TH>";
    } 
    if( $system_flags{show_last_total} == 1 ) {
      $DATA = $DATA."<th bgcolor=yellow><font size=2>�W���z���l�B</font></th>";
    }
    $DATA = $DATA."<th bgcolor=yellow><font size=2>��ئW��</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>�½ұЮv</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>�Z�O</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>�Ǥ�</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>����ݩ�</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>�P���`��</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>�Ы�</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>�Ǥ��k��</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>�ҵ{�j��</font></th>";
    $DATA = $DATA."<th bgcolor=yellow><font size=2>��L</font></th>";
    $DATA = $DATA."</tr>";

    ####  ����������ƪ����  ####
    for($i=($Current_Page-1)*10; $i < $Count and $i < $Current_Page*10; $i++){
      ####  �}�lŪ��������ت�������ơA��ַj�M�d��A�`�ٮɶ�  ####
      %the_Course=Read_Course($Input{dept},$Course[$i]{id},$Course[$i]{group});
      $DATA=$DATA."<tr>";                        ##  �аO
      $DATA=$DATA."<th>";
      my($Flag)=0;
      my($Property)="";
      for($j=0; $j < $MyCount; $j++){
          if( ($the_Course{id} eq $MyCourse[$j]{id})){
              if( ($the_Course{group} eq $MyCourse[$j]{group}) ){
                  $Flag=1;
                  $Property=$MyCourse[$j]{property};
                  break;
              }
          }
      }
                     
      if($Flag == 1){   ###  �Ӫ��Ҥw�g��L�F  ###
          $DATA=$DATA."<img src=\"".$GRAPH_URL."flag.gif\">\n";
      }else{            ###  �Ӫ��ҩ|����L    ###
          $DATA=$DATA."<input type=checkbox name=";
          $DATA=$DATA."\"course\" value=\"";
          $DATA=$DATA.$the_Course{id}."_".$the_Course{group}."\">";
      }
      $DATA=$DATA."</th>\n";

      ###########  �O�_�B�����O Added Feb 21,2000 Nidalap
#      $course_full_flag = Student_of_Course_Number($Input{dept}, $Course[$i]{id}, $Course[$i]{group});
      $student_count = Student_in_Course($Input{dept}, $Course[$i]{id}, $Course[$i]{group});
      $student_count_show = $student_count;
      
#      $course_full_flag = "�_";
#      print("$course_full_flag $the_Course{number_limit} $the_Course{reserved_number}");

      $limit_state = Limit_State();
      if( $limit_state == 1 ) {                                 ###  �Ҽ{�O�d�H��
        if( ($student_count >= $the_Course{number_limit} - $the_Course{reserved_number}) and ($the_Course{number_limit} != 0)) {
          $student_count_show = "<font color=RED>" . $student_count . "</font>";
        }
      }elsif( $limit_state == 2 ) {                             ###  �u�Ҽ{���פH��
        if( ($student_count >= $the_Course{number_limit}) and ($the_Course{number_limit} != 0)) {
          $student_count_show = "<font color=RED>" . $student_count . "</font>";
        }
      }            
      $DATA = $DATA . "<TH>";
      $DATA = $DATA . $student_count_show . "</TH>";
      
      #####################################################################   
      if( $system_flags{show_immune_count} == 1 ) {  ### �n��ܥi�[��W�B
        my($limit_state);
        $limit_state = Limit_State();
        if( $limit_state == 2 ) {                    ### �j��u���b�����Ĺ�ɤ~���
          my($immune_count, $available_count);
          $DATA = $DATA . "<TH>";
          $immune_count = Check_Course_Upper_Limit_Immune_Count($Course[$i]{id}, $Course[$i]{group}, "add");
          if( ($the_Course{number_limit} == 0) or ($the_Course{number_limit} == 999) ) {
            $DATA .= "<FONT size=2>�L����</FONT>";
          }else{
            $immune_count = 0  if($immune_count <= 0);
            $available_count = $the_Course{number_limit} + $immune_count - $student_count;
            $available_count = 0  if( $available_count <= 0 );    ###  ���Ӥ��|�o�� :P
            if( $available_count == 0) {
              $available_count_show = "<FONT color=RED size=2>" . $available_count . "</FONT>";
            }else{
              $available_count_show = $available_count;
            }
            $DATA .= $available_count_show;
          }
          $DATA .= "</TH>";
        }
      }
      #####################################################################
      if( ($system_flags{show_last_total} == 1) ) {  ### �n��ܤW���z���l�B    
        $DATA = $DATA . "<TH>";
        $rest_count = Student_in_Course($Input{dept}, $Course[$i]{id}, $Course[$i]{group}, "last");
        $rest_count = $the_Course{number_limit} - $rest_count;
        $rest_count = 0  if($rest_count < 0);
        if( $rest_count == 0 ) {
          $DATA = $DATA . "<FONT color=RED>";
        }
        $rest_count = "<FONT size=2 color=BLACK>�L����" if( $the_Course{number_limit} == 0 );
        $DATA = $DATA . $rest_count . "</TH>";
      }
      #####################################################################
      $DATA=$DATA."<th><font size=2>";
      $DATA=$DATA.$the_Course{id};               ##  ��إN�X
      $DATA=$DATA."<br>".$the_Course{cname};     ##  ��ئW��
      $DATA=$DATA."</font></th>\n";

      $DATA=$DATA."<th><font size=2>";           ##  �½ұЮv
      $T=@{$the_Course{teacher}};

      for($teacher=0; $teacher < $T; $teacher++){
        if($the_Course{teacher}[$teacher] != 99999){
          $DATA=$DATA.$Teacher_Name{$the_Course{teacher}[$teacher]};
        }else{
          $DATA=$DATA."�Юv���w";
        }
        if($teacher != $T-1){
          $DATA=$DATA.", ";
        }
      }
      $DATA=$DATA."</font></th>\n";

      $DATA=$DATA."<th><font size=2>";
      $DATA=$DATA.$the_Course{group};            ##  �Z�O
      $DATA=$DATA."</font></th>\n";
      $DATA=$DATA."<th><font size=2>";
      $DATA=$DATA.$the_Course{credit};           ##  �Ǥ���
      $DATA=$DATA."</font></th>\n";
      $DATA=$DATA."<th><font size=2>";

      if($the_Course{property} == 1){            ##  ����ݩ�
          $DATA=$DATA."����";
      }elsif($the_Course{property} ==2){
          $DATA=$DATA."���";
      }else{
          $DATA=$DATA."�q��";
      }

      $DATA=$DATA."</font></th>\n";

      $DATA=$DATA."<th><font size=2>";           ## �P���`��
      $time_string = Format_Time_String($the_Course{time});
      $DATA .= $time_string;
      $DATA=$DATA."</font></th>\n";

      $DATA=$DATA."<th><font size=2>";           ##  �Ы�
      %Room=Read_Classroom($the_Course{classroom});
      $DATA=$DATA.$Room{cname};
      $DATA=$DATA."</font></th>\n";

      $DATA=$DATA."<th><font size=2>";##  �Ǥ��k��
      if($Flag == 0){
        $DATA .= Show_Property_Select();
      }else{
          if($Property == 1){$DATA=$DATA."����";}
          if($Property == 2){$DATA=$DATA."���";}
          if($Property == 3){$DATA=$DATA."�q��";}
          if($Property == 4){$DATA=$DATA."���t";}
          if($Property == 5){$DATA=$DATA."���D��";}
          if($Property == 6){$DATA=$DATA."�j�ǳ��ҵ{";}
          if($Property == 7){$DATA=$DATA."�Ш|�ǵ{";}
#          if($Property == 8){$DATA=$DATA."���C�J���~�`�Ǥ�";}
      }

      $DATA=$DATA."</font></th>\n";
      ###  �ҵ{�j�� Added 20080805 Nidalap :D~
      $DATA=$DATA."<th><font size=2>";
      $DATA=$DATA."<A href=\"".$ECOURSE_QUERY_COURSE_URL."&courseno=".$the_Course{id}
        ."_".$the_Course{group}."&year=".$YEAR."&term=".$TERM."\" target=NEW>"
        ."�s��</A>";
      $DATA=$DATA."</font></th>\n";

#      my($FILENAME)=$CLASS_URL."ShowNote.cgi";
      my($FILENAME)="ShowNote.cgi";
      $DATA=$DATA."<th><font size=2>";
      $DATA=$DATA."<a href=\"".$FILENAME."?";
      $DATA=$DATA."user=";
      $DATA=$DATA.$Input{id};
      $DATA=$DATA."&dept=";
      $DATA=$DATA.$Input{dept};
      $DATA=$DATA."&course=";
      $DATA=$DATA.$the_Course{id};
      $DATA=$DATA."&group=";
      $DATA=$DATA.$the_Course{group};
      $DATA=$DATA."\">�Ƶ�</a>";
      $DATA=$DATA."</font></th>\n";

      $DATA=$DATA."</tr>";
    }

    $DATA = $DATA."</table>\n";

    DEPTS_COURSE($HEAD_DATA,$Student{id},$Student{password},$DATA);
  }else{
      RESELECT2($HEAD_DATA);                     ##  �L��Ҹ�� ���s���  ##
  }
}
}
########################################################################
#####  Show_Property_Select()
#####  ���ͬ���ݩʿﶵ�ѾǥͿ��
#####  �̾ڶ}���ݩ�, �䴩�q��, �ǥͨ������Ӳ��ͤ��P�ﶵ
#####  Update: Nov30,2000 Nidalap
########################################################################
sub Show_Property_Select()
{
  my($property_select, $graduate_select_under);
  $graduate_select_under = 0;

  if( ($Student{dept} =~ /6$/) and
      ( ($the_Course{dept} =~ /4$/)or($the_Course{dept} eq "7006")
        or($the_Course{dept} eq "I000")or($the_Course{dept} eq "V000")
        or($the_Course{dept} eq "Z121")or($the_Course{dept} eq "F000")  ) ) {
     $graduate_select_under = 1;                               ###  ��s�ͭפj�ǳ��ҵ{
  }

  $property_select .= "<select name=\"$the_Course{id}_$the_Course{group}\">\n";
#  $property_select .= "<option value=0>�Ǥ��k��\n";
  
  if( (($the_Course{property} == 1) or ($SUPERUSER == 1)) and ($the_Course{dept} ne "7306") ) {
    if( $graduate_select_under != 1 ) {
      $property_select .= "<option value=1>����\n";             ###  �}������, �B���O�ǵ{����
    }
  }
  if( (($the_Course{property} == 2) or ($SUPERUSER == 1)) and ($the_Course{dept} ne "7306") ) {
    if( $graduate_select_under != 1 ) {
      $property_select .= "<option value=2>���\n";             ###  �}�����, �B���O�ǵ{����
    }
  }
  if( ($the_Course{property} == 3) or ($SUPERUSER == 1) or ($the_Course{support_cge_type} ne "0") ) {
    if( $graduate_select_under != 1 ) {
      $property_select .= "<option value=3>�q��\n";              ### �p�G�Ӭ�}���q�ѩΤ䴩�q��
    }
  }
  if( ($the_Course{dept} ne "7306") and ($the_Course{dept} ne "I000") and ($the_Course{dept} ne "7006") ) {
                                                                ### �ǵ{����, �@�P��, �q�Ѥ��߶}���Ҥ��o�אּ���t
    if( ($FU{$Student{id}} eq $the_Course{dept}) or ($SUPERUSER == 1) ) {
      $property_select .= "<option value=4>���t\n";
    }
    if( ($DOUBLE{$Student{id}} eq $the_Course{dept}) or ($SUPERUSER == 1) ) {
      $property_select .= "<option value=5>���D��\n";
    }
  }
  if( $graduate_select_under == 1 ) {
    $property_select .= "<option value=6>�j�ǳ��ҵ{\n";
  }

  if( $the_Course{dept} eq "7306" ) {                                ### �ǵ{���߶}���Ҥ~��אּ�ǵ{
    $property_select .= "<option value=7>�Ш|�ǵ{\n";
  }
###  "���C�J���~�Ǥ�" �ﶵ�w�g���_�s�b (2003/01/06 Nidalap :D~)
#  if( (($Student{dept} =~ /4$/) and ($the_Course{dept} =~ /6$/)) and ($the_Course{dept} ne "7006") ) {
#                                                                     ### �p�G�O�j�ǥͭ׬�s�ҽҵ{, �θӬ�جO�q�ѩҶ}
#    $property_select .= "<option value=8>���C�J���~�Ǥ�";
#  }
  $property_select .= "</select>\n";
}
################################################################################
########################################################################
####  �[��t�α���椸�l�{��                                        ####
####    Limit_State() : ��X�ثe��ҤH�ƭ�����A (0/1/2)          ####
####    is_Grade_Update() : �]���ǥ͸���ɧ�s�t�׸��C�����D�A��  ####
####                    �@�Ǧ~�}�l�e�ȮɱN�U�~�žǥͦ~�Ŧ۰ʥ[ 1�C  ####
########################################################################
sub Limit_State()
{
  my($FileName)=$REFERENCE_PATH."Basic/LimitNumberState";
  open(FILE,"<$FileName")
                   or die("Cannot open file $FileName!\n");
  $State=<FILE>;
  close(FILE);

  return($State);
}

sub is_Grade_Update()
{
  my($FileName)=$REFERENCE_PATH."Basic/GradeState";
  open(FILE,"<$FileName")
                   or die("Cannot open file $FileName!\n");
  $State=<FILE>;
  close(FILE);

  return($State);
}

########################################################################
####    ���͸ӿ�ܪ������t�Ҷ}�Ҹ�ƪ� HTML �ɮ�                    ####
####    ���� table ���禡�b�W��                                     ####
########################################################################
sub DEPTS_COURSE
{
my($HEAD_DATA,$id,$password,$DATA)=@_;
my($NEXT_URL)="Add_Course01.cgi";
my($LINK)=Select_Course_Link($Input{id},$Input{password});
my($PRE_COURSE_WARNING, $EDU_COURSE_WARNING, $MIL_COURSE_WARNING);

if($pre_course_count > 0) {        ###### �����׬�ت���, ���ĵ�Thtml��
  $PRE_COURSE_WARNING = qq(
    <SCRIPT language="javascript">
      messageWindow = open('Show_Special_Announce.php?type=prerequisite_msg', 'messageWindow', 'resizable=yes, width=250, height=250');
    </SCRIPT>
  );
}
if( $Input{dept} eq "7306" ) {     ######  �ױШ|�ǵ{����, �����O�Ш|�ǵ{���ǥ�html warning
  my($announce_title, $announce_content) =  Read_Special_Announce("edu_msg");
  $COURSE_WARNING2 = Special_Announce_Table($announce_title, $announce_content);    
#  $EDU_COURSE_WARNING = qq(
#    <SCRIPT language="javascript">
#      messageWindow = open('Show_Special_Announce.php?type=edu_msg','messageWindow', 'resizable=yes, width=250, height=250');
#    </SCRIPT>
#  );
}

if( $Input{dept} eq "V000" ) {     ######  �x�V�ҵ{���� (added 2006/11/14)
  my($announce_title, $announce_content) =  Read_Special_Announce("military_msg");
  $COURSE_WARNING2 = Special_Announce_Table($announce_title, $announce_content);
      
#  $MIL_COURSE_WARNING = qq(
#    <SCRIPT language="javascript">
#      messageWindow = open('Show_Special_Announce.php?type=military_msg','messageWindow', 'resizable=yes, width=350, height=350');
#    </SCRIPT>
#  );
}

if( $Input{dept} eq "F000" ) {     ######  ��|�ҵ{���� (added 2006/11/24)  
  my($announce_title, $announce_content) =  Read_Special_Announce("physical_msg");
  $COURSE_WARNING2 = Special_Announce_Table($announce_title, $announce_content);
    
#  $MIL_COURSE_WARNING = qq(
#    <SCRIPT language="javascript">
#      messageWindow = open('Show_Special_Announce.php?type=physical_msg','messageWindow', 'resizable=yes, width=450, height=450');
#    </SCRIPT>
#  );
}

if( $Input{dept} eq "Z121" ) {     ######  �y�����߽ҵ{���� (added 2006/12/26)
  $MIL_COURSE_WARNING = qq(
    <SCRIPT language="javascript">
      messageWindow = open('Show_Special_Announce.php?type=lang_msg','messageWindow', 'resizable=yes, width=800, height=600');
    </SCRIPT>
  );
  
  my($announce_title, $announce_content) =  Read_Special_Announce("lang_msg");
  $COURSE_WARNING2 = Special_Announce_Table($announce_title, $announce_content);
#  $COURSE_WARNING2 = qq(
#    <TABLE border=0 width=70%>
#      <TR><TH bgcolor=YELLOW>$announce_title</TH></TR>
#      <TR><TD bgcolor=YELLOW>
#    )
#    . $announce_content
#    . qq(        
#      </TD></TR>
#    </TABLE>
#    <P>
#  );
}


#print("dept = $Input{dept}<BR>\n");

#if( length($Input{dept}) == 2 ) {               ###  ����ǵ{
#  print qq(
#    <html>                                   
#      <head>
#        <meta http-equiv="Content-Type" content="text/html; charset=big5">
#        <meta http-equiv="refresh" content="1; URL=Show_All_GRO.cgi">
#        <Title>$SelectDept{cname}$Input{grade}�~�Ŭ�ئC��</Title>  
#      </head>  
#  );
#
#}else{
  print << "End_of_HTML"
    <html>
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=big5">
        <Title>$SelectDept{cname}$Input{grade}�~�Ŭ�ئC��</Title>
      </head>
      <script language="javascript">
        function FreeSelect(OBJ)
        {
            OBJ.page.value=3;
            OBJ.submit();
        }
      </script>
      $PRE_COURSE_WARNING
      $EDU_COURSE_WARNING
      $MIL_COURSE_WARNING
      
      <body background="$GRAPH_URL/ccu-sbg.jpg">
        <center>
            $HEAD_DATA
        <hr>
        <br>
        <b>
        $COURSE_WARNING2
        <font size=5>$SelectDept{cname}$Input{grade}�~�Ŭ�ئC��</font>
        </b>
        <br>
        <form action="$NEXT_URL" method="post" name="SelectForm">
          <input type=hidden name="session_id" value="$Input{session_id}">
          <input type="hidden" name="dept" value="$Input{dept}">
          <input type="hidden" name="grade" value="$Input{grade}">
          <input type="hidden" name="page" value="$Current_Page">
          <input type="hidden" name="SelectTag" value=1>
          <table border=0 width=90%>
            <tr>
              <th colspan=2>
                $DATA
              </th>
            </tr>
            <tr>
              <th colspan=2> 
                 <input type=submit value="�[��H�W�аO���">
              </th>
              </tr>
          </form>
              <tr>
                <th align=left>
                  <form action="$NEXT_URL" method="post" name="NextForm">
                    <input type=hidden name="session_id" value="$Input{session_id}">
                    <input type="hidden" name="dept" value="$Input{dept}">
                    <input type="hidden" name="grade" value="$Input{grade}">
                    <input type="hidden" name="SelectTag" value=0>
                    <input type="hidden" name="page" value="$Current_Page">
                    <input type=button value="�W�@��" onClick="javascript:history.back()">
                    <input type=submit value="�U�@��">
                </th>	
                  </form>
                <th align=right>
                  ��$Current_Page/$TotalPages��
                </th>
              </tr>
        </table>
      </center>
      </body>
    </html>
End_of_HTML
#}

}
#################################################################################
sub RESELECT
{
my($HEAD_DATA)=@_;
print << "End_of_HTML"
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
</head>
<body background="$GRAPH_URL./ccu-sbg.jpg">
<center>
    $HEAD_DATA
    <hr><br>
    <br>
    <br>
    <font size=5>�z�|�����T����t�ҩΦ~��</font><br>
    <font size=5>��<a href="javascript:history.back()">���s���</a></font>
</center>
</body>
</html>
End_of_HTML
}

#####################################################################################
sub RESELECT2()
{
my($HEAD_DATA)=@_;

if( length($Input{dept}) == 2 ) {               ###  ����ǵ{
  print qq(
    <html>                                   
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=big5">
        <meta http-equiv="refresh" content="1; URL=Show_All_GRO.cgi?session_id=$Input{session_id}&gro_no=$Input{dept}">
        <Title>$SelectDept{cname}$Input{grade}�~�Ŭ�ئC��</Title>  
      </head>  
      <BODY background="$GRAPH_URL./ccu-sbg.jpg">
        <CENTER>
        �����N��V�Ҧ�����ǵ{����, �еy��.<BR>
        �p�G�����S����V, 
        ��<A href="Show_All_GRO.cgi?session_id=$Input{session_id}&gro_no=$Input{dept}"">�I�惡�B</A>.
      </BODY>
    </HTML>
  );
}else{
  print << "End_of_HTML"
    <html>
	<head>
	    <meta http-equiv="Content-Type" content="text/html; charset=big5">
	</head>
	<body background="$GRAPH_URL./ccu-sbg.jpg">
	<center>
	    $HEAD_DATA
	    <hr><br><br>
	    <font size=5>$SelectDept{cname}$Input{grade}�~�źI�ܥثe����</font><br>
	    <font size=5>�õL����}�Ҹ�ƥi��Ū��</font><br>
	    <font size=5>��<a href="javascript:history.back()">���s���</a></font>
	</center>
	</body>
    </html>
End_of_HTML
}
}
######################################################################################
sub Special_Announce_Table()
{
  my ($announce_title, $announce_content) = @_;
  my $COURSE_WARNING2 = qq(
    <TABLE border=0 width=70% cellspacing=0>
      <TR><TH bgcolor=YELLOW>$announce_title</TH></TR>
      <TR><TD bgcolor=YELLOW>
    )
    . $announce_content
    . qq(        
      </TD></TR>
    </TABLE>
    <P>
  );
  return($COURSE_WARNING2);
}
