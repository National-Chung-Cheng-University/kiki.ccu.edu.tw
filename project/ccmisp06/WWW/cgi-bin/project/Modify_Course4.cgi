#!/usr/local/bin/perl
###########################################################################
#####  Modify_Course4.cgi
#####  修改開課資料(最後寫入資料)
#####  Updates:
#####   2009/05/05 加入暑修課程類型 remedy 欄位 (1為一般，2為補救)  Nidalap :D~
#####   2010/03/19 加入 教師專長與授課科目是否符合 $s_match 欄位 Nidalap :D~
#####   2010/10/25 語言中心可開通識外語課程功能 Nidalap :D~
#####   2010/11/24 加入 gender_eq, env_edu 兩個欄位  Nidalap :D~
#####   2012/01/12 加入要求確認功能(目前只有教師/教室衝堂)  Nidalap :D~
#####   2015/04/16 因應文學院需求-委由各系實際執行開課，新增 $open_dept 變數  Nidalap :D~
###########################################################################
require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Open_Course.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Common_Utility.pm";

print("Content-type:text/html\n\n");
%Input = User_Input();
%dept  = Read_Dept($Input{dept_cd});
%Dept  = Read_Dept($Input{dept_cd});

$cge_lan_flag = $Input{cge_lan_flag};

#if( $cge_lan_flag != 2 ) {
#  Check_Dept_Password($Input{dept_cd}, $Input{password});
#}
if( $cge_lan_flag == 2 ) {                                      ###  若是語言中心開通識外語課，讀取語言中心密碼檔 salt
  Check_Dept_Password($DEPT_LAN, $Input{password});
}else{                                                          ###  其餘一般情形：讀取該系所密碼檔 salt
  Check_Dept_Password($Input{open_dept}, $Input{password});
}


#foreach $k (keys %Input) {
#  print("$k ---> $Input{$k}<br>");
#}

$grade_show = ($Input{grade} eq "cge_lan") ? "通識外語課" : $Input{grade};

Print_Title();
Delete_Course_Data()  if( $Input{action} eq "delete" );
Modify_Course_Data()  if( $Input{action} eq "modify" );


###########################################################################
sub Print_Title()
{
  $action = "修改"  if( $Input{action} eq "modify" );
  $action = "刪除"  if( $Input{action} eq "delete" );  
  $title = $SUB_SYSTEM_NAME . "開排課系統-- $action 當學期已開科目";
  print Print_Open_Course_Header(\%Input, \%Dept, $title);
}
###########################################################################
sub Delete_Course_Data()
{
  $result=Delete_Course($Input{course_id},$Input{course_group},$Input{dept_cd},$Input{dept_cd});
  if      ( $result eq "TRUE" ) {
    print("<font color=red>本科目已成功\刪除!</font>");
  }elsif  ( $result eq "NOT_FOUND" ) {
    print("<font color=red>系統發現錯誤: 科目資料不存在!</font>");
  }
  print("<p>");
  Links3($Input{dept_cd} ,$Input{grade}, $Input{password}, $Input{open_dept});
}
############################################################################
sub Modify_Course_Data()
{
  #####  若前一頁要求確認卻沒有確認，到此為止(請回上頁確認  Added 2012/01/12
  if( ($Input{"need_confirmation"} == 1) and ($Input{"yes_i_agree"} ne "on") ) {
    print qq'
          <FONT color=RED>
            請回上頁點選「好的，我知道了」！<P>
            <A href="javascript:history.back()">回上頁</A>
    ';
    exit();
  }

  $course{id}		=	$Input{course_id};
  $course{dept}		=	$Input{dept_cd};
  $course{open_dept}	=	$Input{open_dept};
  $course{cname}	=	$Input{cname};
  $course{ename}	=	$Input{ename};
  $course{total_time}	=	$Input{total_time};
  $course{lab_time1}	=	$Input{lab_time1};   ### Apr,2000  Nidalap
  $course{lab_time2}    =       $Input{lab_time2};   ### Apr,2000  Nidalap
  $course{lab_time3}    =       $Input{lab_time3};   ### Apr,2000  Nidalap
  $course{credit}	=	$Input{credit};
  $course{classroom}	=	$Input{classroom};
  $course{property}	=	$Input{property};
  $course{grade}	=	$Input{grade};
  $course{principle}	=	$Input{principle};
  $course{group}	=	$Input{group};
  $course{number_limit}	=	$Input{number_limit};
  $course{reserved_number} =	$Input{reserved_number};
#  $course{suffix_cd}	=	$Input{suffix_cd};      ### Apr,2000 Nidalap
  $course{support_cge_type} =	$Input{support_cge_type};  ### Nov07,2000
  $course{support_cge_number} =	$Input{support_cge_number}; ## Nov07,2000 Nidalap
  $course{distant_learning} =	$Input{distant_learning};	## 2006/11/14 Nidalap :D~
  $course{english_teaching} =	$Input{english_teaching};	## 2006/11/14 Nidalap :D~
  $course{remedy}	=	$Input{remedy};		## 2009/05/05 Nidalap :D~
  $course{attr}		=	$Input{attr};		## 2012/04/11 Nidalap :D~
  $course{note}		=	$Input{note};
  $temp	= $Input{teacher};
     @{$course{teacher}} = split(/\*:::\*/, $temp);
  $temp	= $Input{support_dept};
     @{$course{support_dept}} = split(/\*:::\*/, $temp);
  $temp = $Input{support_grade};
     @{$course{support_grade}} = split(/\*:::\*/, $temp);
  $temp = $Input{support_class};
     @{$course{support_class}} = split(/\*:::\*/, $temp);
  $temp = $Input{ban_dept};
     @{$course{ban_dept}} = split(/\*:::\*/, $temp);
  $temp = $Input{ban_grade};
     @{$course{ban_grade}} = split(/\*:::\*/, $temp);
  $temp = $Input{ban_class};
     @{$course{ban_class}} = split(/\*:::\*/, $temp);
#  $temp = $Input{prerequisite_course};
#     @{$course{prerequisite_course}} = split(/\*:::\*/, $temp);

  $i=0;
  my @day = split(/\*:::\*/, $Input{date});
  foreach $day (sort @day) {
    ($week, $time) = split(/_/, $day);
    $course{time}[$i]{week} = $week;
    $course{time}[$i]{time} = $time;
    $i++;
  } 
  @temp = split(/\*:::\*/, $Input{Precourse});
  for($i=0; $i<@temp; $i++) {
    ($predept, $precourse, $pregrade) = split(/:/,$temp[$i]);
    $course{prerequisite_course}[$i]{dept}        = $predept;
    $course{prerequisite_course}[$i]{id}          = $precourse;
    $course{prerequisite_course}[$i]{grade}       = $pregrade;
  }
  $course{prerequisite_logic}	= $Input{prerequisite_logic};
  $course{s_match}		= $Input{s_match};
  $course{gender_eq}		= $Input{gender_eq};
  $course{env_edu}		= $Input{env_edu};

  $result = Modify_Course("modify", %course);  
#  print("result = $result");
  if  ( $result eq "TRUE" ) {
    print("<font color=red>本科目已成功\修改!</font>");
  }elsif  ( $result eq "NOT_FOUND" ) {
    print("<font color=red>系統發現錯誤: 科目資料不存在!</font>");
  }
  print("<p>");
  
  $Input{dept_cd} = $DEPT_LAN  if( $Input{cge_lan_flag} == 2 );  ### 若是語言中心開通識外語課，還原系所代碼為語言中心
  Links3($Input{dept_cd} ,$Input{grade}, $Input{password}, $Input{open_dept});
}
