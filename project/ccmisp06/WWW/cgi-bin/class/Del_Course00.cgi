#!/usr/local/bin/perl
print("Content-type:text/html\n\n");

######################################################################################################################
#####  Del_Course00.cgi
#####  退選
#####  Updates:
#####    199?/??/?? Created
#####    2009/10/02 加上退選 $by_whom 欄位，用以做 LOG 紀錄追查
#####    2011/04/27 若勾選退選「學系服務學習課程」，顯示 javascript 警告訊息.  Nidalap :D~
#####    2012/09/11 比照「學系服務學習課程」，若勾選退選「通識英語課程」，依目前系統設定跳出不同警訊。  
#####               因為採用 getElementById() 抓 checkbox，所以若學生同時選了兩門以上，退選第一門以外會不作用  Nidalap :D~
#####    2013/07/24 英文版相關增修：將顯示文字拉到 Init_Text_Values() 中設定。 Nidalap :D~
#####    2014/09/05 若設定先搶先贏期間退選餘額延後釋出，且目前為先搶先贏期間：則執行延遲退選而不直接退選。  Nidalap :D~
######################################################################################################################

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
require $LIBRARY_PATH."System_Settings.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Teacher.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."English.pm";
require $LIBRARY_PATH."Session.pm";

my(%Student,%Dept);

#%Input=User_Input();
($Input{id}, $Input{password}, $login_time, $ip) = Read_Session($Input{session_id}, "", 1);
#print("session_id, id, pass = $Input{session_id}, $Input{id}, $Input{password}<BR>"); 

%system_flags = Read_System_Settings();
%system_settings = %system_flags;

%Student=Read_Student($Input{id});
%Dept=Read_Dept($Student{dept});
%txt = Init_Text_Values();

Check_Student_Password($Input{id}, $Input{password});

#Print_Hash(%system_settings);

@MyCourse=Course_of_Student($Student{id});
if( $IS_ENGLISH ) {
  $HEAD_DATA = Head_of_Individual($Student{ename},$Student{id},$Dept{ename},$Student{grade},$Student{class});
}else{
  $HEAD_DATA = Head_of_Individual($Student{name},$Student{id},$Dept{cname},$Student{grade},$Student{class});
}

#############  非系統限定時間不可退選  #####################
if($SUPERUSER != 1){     ## 非 superuser 的使用者
  if( (Whats_Sys_State()==0)or(Whats_Sys_State()==1)or(Check_Time_Map(%Student)!=1) ){
    Enter_Menu_Sys_State_Forbidden($HEAD_DATA);
  }
}

PRINT_HTML_HEAD();

#####  依系統設定, 檢查該生是否在停權黑名單中, 以及是否在停權期間 2009/02/25 Nidalap :D~
#####  即使關閉此功能, 系統仍會紀錄 log, 差別在於是否顯示警訊和是否給加退選.
if( $system_settings{black_list} == 1 ) {                      ### 如果開啟黑名單功能
  $ban_time = Read_Ban_Record($Student{id}, $BAN_COUNT_LIMIT); ### 停權尚須多久恢復(大於0就是停權中)
  if($ban_time > 0) {
    Show_Ban_Message($ban_time, 1);
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

#####################################################################################################
sub PRINT_HTML_HEAD
{
  my $javascripts = Create_Javascripts();
  print qq(
	<html>
	<head>
	    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	    $EXPIRE_META_TAG
	    <TITLE>退選科目</TITLE>
	</head>
        $javascripts
	<body background="$GRAPH_URL./ccu-sbg.jpg">
	<center>
	    $HEAD_DATA 
	    <hr>
  );
}
#####################################################################################################
sub MAIN_DEL_HTML
{
my($HEAD_DATA,$DATA)=@_;
my($NEXT_URL)="Del_Course00.cgi";
my($LINK)=Select_Course_Link($Input{id},$Input{password});

$submit = $txt{'del_button'};

$eng_input = '';
$mobile_input = '';
$eng_input		= '<input type=hidden name="e" value=1>'		if( $IS_ENGLISH );
$mobile_input	= '<input type=hidden name="m" value=1>'		if( $IS_MOBILE );
print qq|
    <form action="$NEXT_URL" method="post" name="WorkForm">
    $DATA
    <input type="hidden" name="session_id" value="$Input{session_id}">
    <input type="submit" value="$submit">
	$eng_input
	$mobile_input
    </form>
</center>
</body>
$EXPIRE_META_TAG2
</html>
|;
}
################################################################
##################    產生主要選課單的表格    ##################
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
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>" . $txt{'mark'} . "</font></th>";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>" . $txt{'cname'} . "</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>" . $txt{'teacher'} . "</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>" . $txt{'class'} . "</font></th>";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>" . $txt{'credit'} . "</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>" . $txt{'property'} . "</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>" . $txt{'weekday'} . "</font></th>\n";
  $DATA = $DATA."  <th bgcolor=yellow><font size=2>" . $txt{'classroom'} . "</font></th>\n";
  $DATA = $DATA."</tr>\n";

  ####  列印相關課程資料  ####
  for($i=0; $i < $MyCount; $i++){
      my(%theCourse)=Read_Course($MyCourse[$i]{dept},$MyCourse[$i]{id},$MyCourse[$i]{group},"");
      my($value)=$theCourse{dept}."_".$theCourse{id}."_".$theCourse{group};
      my $is_dept_serv = 0;	###  判斷是否為學系服務學習課程
      my $is_genedu_eng = 0;	###  判斷是否為通識英語課程
      $is_dept_serv = 1  if( $theCourse{id} eq Get_Dept_Serv_Course_ID($theCourse{dept}) );
      $is_genedu_eng = 1 if( $theCourse{id} =~ /^7102...$/ );
      
#      print("is genedu eng = $is_genedu_eng");
      
      $DATA = $DATA."<tr>\n<th>";
      if( $is_dept_serv ) {
        $DATA = $DATA . "<FONT COLOR=RED><A title='" . $txt{'nodel'} . "'>
                   <IMG SRC=$GRAPH_URL/icon_ps.gif></A></FONT>";
      }elsif( $is_genedu_eng ) {
        my $del_genedu_eng_msg = Determine_Del_Genedu_Eng_Warning_Msg();
        $DATA = $DATA . "<FONT COLOR=RED><A title='" . $del_genedu_eng_msg . "'>
                   <IMG SRC=$GRAPH_URL/icon_ps.gif></A></FONT>";
      }
      $DATA = $DATA."<input type=checkbox name=DelCourse value=\"";
      $DATA = $DATA.$value;
      $DATA = $DATA."\"";
      if( $is_dept_serv ) {
        $DATA = $DATA . " id=del_dept_serv_checkbox onclick=javascript:del_dept_serv_confirm()";
      }elsif( $is_genedu_eng ) {
        $DATA = $DATA . " id=del_genedu_eng_checkbox onclick=javascript:del_genedu_eng_confirm()";
      }
      $DATA = $DATA . "></th>\n";

      $DATA = $DATA."<th><font size=2>";
      $DATA = $DATA.$theCourse{id}."<br>";
      if( $IS_ENGLISH ) { 
	    $DATA = $DATA.$theCourse{ename}."</font></th>\n";
	  }else{
	    $DATA = $DATA.$theCourse{cname}."</font></th>\n";
	  }

      $DATA=$DATA."<th><font size=2>";           ##  授課教師
      $T=@{$theCourse{teacher}};
      for($teacher=0; $teacher < $T; $teacher++){
        if($theCourse{teacher}[$teacher] != 99999){
          $DATA=$DATA.$Teacher_Name{$theCourse{teacher}[$teacher]};
        }else{
          $DATA=$DATA. $txt{'tea_undefined'};
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

      $DATA=$DATA."<th><font size=2>";           ## 星期節次
      $time_string = Format_Time_String($theCourse{time});
      $DATA .= $time_string;
      $DATA=$DATA."</font></th>\n";

      $DATA=$DATA."<th><font size=2>";           ##  教室
      %Room=Read_Classroom($theCourse{classroom});
      $DATA=$DATA.$Room{name};
      $DATA=$DATA."</font></th>\n";

      $DATA = $DATA."</tr>\n";
  }

  $DATA = $DATA."</table>\n";

return($DATA);
}
################################################################
##################       刪除選擇的科目       ##################
################################################################
sub DELETE_COURSE
{
#  print("<font color=RED>目前並非加退選時段, 謝謝!<br></font>\n");
    my $by_whom = "SELF";
    @Courses=split(/\*:::\*/,$Input{DelCourse});
    foreach $course(@Courses){
      my($dept,$id,$group)=split(/_/,$course);
	  ###  若設定先搶先贏期間退選餘額延後釋出，且目前為先搶先贏期間：則執行延遲退選而不直接退選。 added 20140905
	  if( ($system_settings{'delayed_del'} == 1) and ($system_settings{'limit_number_state'} == 2)) {
	    Delayed_Delete_Student_Course($Input{id},$dept,$id,$group,$by_whom);
	  }else{
        Delete_Student_Course($Input{id},$dept,$id,$group,$by_whom);
	  }
    }
}
################################################################
####  產生「退選學系服務學習課程」應顯示的警訊
sub Create_Javascripts
{
  my $del_genedu_eng_msg = Determine_Del_Genedu_Eng_Warning_Msg();
  
  my $js = qq|
    <script type="text/javascript">
      function del_dept_serv_confirm() {
	var obj = document.getElementById("del_dept_serv_checkbox");
	if( obj.checked == true ) {
  	  var answer =
            confirm("請勿退選本科目！若退選後，將無法加選，需填寫加簽單，並完成加簽程序後方可選課。"
                     + "\\n\\n" + "點擊「確定」以繼續退選，「取消」以取消退選。")
	  if (answer){
            obj.checked = true;
	  }else{
	    obj.checked = false;
	  }
        }
      }
      
      function del_genedu_eng_confirm() {
        var obj = document.getElementById("del_genedu_eng_checkbox");
        if( obj.checked == true ) {
          var answer =
            confirm("| . $del_genedu_eng_msg . qq|"
                     + "\\n\\n" + "點擊「確定」以繼續退選，「取消」以取消退選。");
          if (answer){
            obj.checked = true;
          }else{
            obj.checked = false;
          }
        }
      }
      
    </script>
  |;
  return $js;
}
##############################################################################
####  產生「退選通識英語課程課程」應顯示的警訊  Added 2012/09/11 Nidalap :D~
sub Determine_Del_Genedu_Eng_Warning_Msg()
{
  my $msg, $cst;
  my @MSG = (
    "您即將退選的課程為大一新生第一學期優先保障之「大一必修」通識英語課程，退選後即失去優先保障名額。" 
      . "退選後自行加選其他班別但未篩選上者，需於開學第一週欲選之上課時段至語言中心遞補有餘額班級。"  
      . "然各班餘額有限，退選此一保障名額前務必先審慎評估。", 
    "您即將退選的課程為大一新生第一學期優先保障之「大一必修」通識英語課程，退選後即失去優先保障名額。"  
      . "退選後若欲重新加選其他班別，需於開學第一週欲選之上課時段至語言中心遞補有餘額班級，再以加簽方式辦理選課。" 
      . "然各班餘額有限，退選前務必先審慎評估。", 
    "您即將退選的是大一必修的通識英語課程，若本階段選修之通識英語課程為篩選上者，" 
      . "需於開學第一週欲選之上課時段至語言中心遞補有餘額班級。", 
    "您即將退選通識英語課程。" 
      . "退選後若欲重新加選通識英語，需於開學第一週欲選之上課時段至語言中心遞補有餘額班級，再以加簽方式辦理選課。" 
      . "然各班餘額有限，退選前務必先審慎評估。" 
  );
  $cst = $system_settings["current_system_timeline"];
  
  if( ($TERM==1) and ($cst<=1) ) {
    $msg = $MSG[0];
  }elsif( ($TERM==1) and ($cst>=4) ) {
    $msg = $MSG[1];
  }elsif( ($TERM==2) and ($cst<=1) ) {
    $msg = $MSG[2];
  }else{
    $msg = $MSG[3];
  }
  return $msg;  
}
##################################################################################
#####  因應英文版本，將所有要顯示的文字在此整理，依照 $IS_ENGLISH 自動判別  2013/07/24
sub Init_Text_Values
{
  my %txtall;
  
  %txtall = (
    'mark'		=> {'c'=>'標記', 'e'=>'Mark'},
	'cname'		=> {'c'=>'科目名稱與代碼', 'e'=>'Course Title & ID'},
	'teacher'	=> {'c'=>'授課教師', 'e'=>'Instructor'},
	'class'		=> {'c'=>'班別', 'e'=>'Class'},
	'credit'	=> {'c'=>'學分', 'e'=>'Credit'},
    'property'	=> {'c'=>'學分歸屬', 'e'=>'Credit Type'},
    'weekday'	=> {'c'=>'星期節次', 'e'=>'Day/Period'},
    'classroom'	=> {'c'=>'教室', 'e'=>'Class Location'},
	
	'nodel'		=> {'c'=>'請勿退選本科目！若退選後，將無法加選，需填寫加簽單，並完成加簽程序後方可選課。', 
	                'e'=>'請勿退選本科目！若退選後，將無法加選，需填寫加簽單，並完成加簽程序後方可選課。'},
	'del_button'=> {'c'=>'確定刪除標記中科目', 'e'=>'Delete all courses with selection marks'},
	'tea_undefined'	=> {'c'=>'教師未定', 'e'=>'教師未定'},
	'mark'		=> {'c'=>'標記', 'e'=>'Mark'},
	'mark'		=> {'c'=>'標記', 'e'=>'Mark'},
	'mark'		=> {'c'=>'標記', 'e'=>'Mark'},
	
	
	
  );

  foreach $k (keys %txtall) {
	if( $IS_ENGLISH ) {
	  $txt{$k} = $txtall{$k}{'e'};
	}else{
	  $txt{$k} = $txtall{$k}{'c'};
	}
  }
 
  return %txt;  
}
