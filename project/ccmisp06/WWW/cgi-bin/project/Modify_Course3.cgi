#!/usr/local/bin/perl
#############################################################################################
#####  Modify_Course3.cgi
#####  修改當學期已開科目
#####  page3: 
#####   修改模式：檢查輸入是否合法，並顯示確認畫面
#####   刪除模式：執行刪除
#####  Updates:
#####   2009/05/05 加入暑修課程類型 remedy 欄位 (1為一般，2為補救)  Nidalap :D~
#####   2010/03/19 加入 教師專長與授課科目是否符合 $s_match 欄位 Nidalap :D~
#####   2010/04/08 體育中心和軍訓開課，不顯示 s_match 欄位  Nidalap :D~
#####   2010/05/25 s_match 出現與否，改為交給 Need_s_match() 判斷  Nidalap :D~
#####   2010/10/25 語言中心可開通識外語課程功能 Nidalap :D~
#####   2010/11/24 加入 gender_eq, env_edu 兩個欄位  Nidalap :D~
#####   2010/12/08 課程異動期間，不得選「教師待聘」  Nidalap :D~
#####   2010/12/16 刪除課程前顯示該科目修習學生名單，並於下頁同步刪除選課資料  Nidalap :D~
#####   2012/01/12 加入要求確認功能(目前只有教師/教室衝堂)  Nidalap :D~
#####   2012/04/11 新增開課學制(碩/博班課程)欄位 attr，只有在研究所課程中需要選擇.  Nidalap :D~
#####   2012/04/23 檢查修習此科目的學生，是否有人會因此而導致衝堂. Nidalap :D~
#####   2015/04/16 因應文學院需求-委由各系實際執行開課，新增 $open_dept 變數  Nidalap :D~
#############################################################################################

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."Open_Course.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Teacher.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."System_Settings.pm";

print("Content-type:text/html\n\n");
my(%Input,@Date,$i,@teacher);
%Input = User_Input();
$Input{dept_cd} = $Input{dept_cd};
%Input = %Input;
%system_settings = Read_System_Settings();
%dept  = Read_Dept($Input{dept_cd});
%Dept = %dept;
%cge = Read_Cge();

$cge_lan_flag = $Input{cge_lan_flag};
$grade_show = ($Input{grade} eq "cge_lan") ? "通識外語課" : $Input{grade};

if( $cge_lan_flag == 2 ) {  ### 語言中心可開通識外語課
  $dept{id}	  = $DEPT_CGE;
  $Input{grade} = 1;
}
$is_dept_serv = 1  if( $Input{id} == Get_Dept_Serv_Course_ID($dept{id}));	### 系所服務學習課程

%original_course = Read_Course($Input{dept_cd}, $Input{id}, $Input{group}, "", "");

#if( $cge_lan_flag != 2 ) {
#  Check_Dept_Password($Input{dept_cd}, $Input{password});
#}
if( $cge_lan_flag == 2 ) {                                      ###  若是語言中心開通識外語課，讀取語言中心密碼檔 salt
  Check_Dept_Password($DEPT_LAN, $Input{password});
}else{                                                          ###  其餘一般情形：讀取該系所密碼檔 salt
  Check_Dept_Password($Input{open_dept}, $Input{password});
}

%classroom = Read_Classroom($Input{classroom});

Print_Title();
 
#foreach $k (keys %Input) {
#  print("$k ---> $Input{$k}<br>");
#}

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
  my(@stu, $result, %stu, %Course, $i);
  
  %Course = Read_Course($Input{dept_cd}, $Input{id}, $Input{course_group},"","","");
  @stu = Student_in_Course($Input{dept_cd}, $Course{id}, $Course{group}, "", "");
  
  ####  先將修習該科目的學生退選
  foreach $stu (@stu) {
    #print("del: $stu, $Input{dept_cd}, $Course{id}, $Course{group}<BR>\n");
    Delete_Student_Course($stu, $Input{dept_cd}, $Course{id}, $Course{group}, "DEL_COURSE");
  } 
    
  $result = Delete_Course($Input{id},$Input{course_group},$Input{dept_cd});
  if      ( $result eq "TRUE" ) {
    print("<font color=red>本科目已成功\刪除!</font>");
  }elsif  ( $result eq "NOT_FOUND" ) {
    print("<font color=red>系統發現錯誤: 科目資料不存在!</font>");
  }else{
    print("<font color=red>系統內部錯誤，無法刪除課程！</FONT>");
  }
  print("<p>");
  $Input{dept_cd} = $DEPT_LAN  if( $Input{cge_lan_flag} == 2 );  ### 若是語言中心開通識外語課，還原系所代碼為語言中心
  Links3($Input{dept_cd} ,$Input{grade}, $Input{password},$Input{open_dept} );
}
############################################################################
sub Modify_Course_Data()
{
  @selected_time = Find_Selected_Time(); 

  foreach $selected_time (@selected_time) {
    if($$selected_time{time} >= 1) {           ### 如果是數字截次 -> 1 hr
      $total_selected_time ++;
    }else{                                     ### 如果是英文截次 -> 1.5 hr
      $total_selected_time += 1.5;
    }
  }

  @teacher = Read_Teacher_File();
  $i=0;
  foreach $key(%Input)
  {
   if($Input{$key} eq "999")
   {
    $Date[$i++]=$key;
   }
  }

  if($Input{group} eq "") { $Input{group} = "01" };

  %temp=Read_Dept($Input{dept_cd});
  ########  非管理者, 若有限修, 則 限修人數 == 教室最適容量
  if( $SUPERUSER != 1 ) {                    ###  非管理者
    if( $Input{principle} == 0 ) {           ###   若不限修
      $Input{number_limit_0} = $Input{number_limit_1} = $Input{number_limit2} = 0;
    }else{                                   ###   若有限修
      %original_classroom = Read_Classroom($original_course{classroom});
      if( ($original_classroom{size_fit} != $original_course{number_limit}) and ($original_course{principle}!=0) ) {
					     ###   若原先有管理者改過限修人數 -> 限修人數不作修改
        ($Input{number_limit_0}, $Input{number_limit_1}, $Input{number_limit_2})
          = Numeric_to_chars($original_course{number_limit});
      }else{ 		                     ###     若原先科目並無特殊修改過限修人數 -> 限修人數跟著教室容量改
        ($Input{number_limit_0}, $Input{number_limit_1}, $Input{number_limit_2})
          = Numeric_to_chars($classroom{size_fit}); 
      }
    }
  }else{                                     ###  管理者
    ### (do nothing)
  }
  #########################################################################
  print qq(
    <html>
      <head><title>新增學期開課[開課確認]- $temp{cname}</title></head>
      <body bgcolor=white background=$GRAPH_URL/ccu-sbg.jpg>
        <center>
  );
  ###################################################################
  ($warning_count, $error_count, @error_message) =
                            Check_Open_Course_Restrictions("modify", %Input);

  if( $warning_count + $error_count > 0) {
    print("<FONT size=4 color=red>系統檢查開課資料結果如下</FONT><BR>\n");
    print("<TABLE border=0 size=85%>");
    print("  <TR><TD><OL>");
    foreach $error (@error_message) {
      print("<LI>$error");
      $temp++;
    }
    print("</TD></TR></TABLE>");
    if( $error_count > 0 ) {
      exit(1);
    }
  }
  $need_confirm_msg .= Check_Stu_Time_Collition();                   ### 檢查修習此科目的學生，是否有人會因此而導致衝堂  
  
  ###################################################################  
#  $temp=join("*:::*",@Date);
  $temp = "";
  foreach $time (@selected_time) {
    if( $temp ne "" ) {
      $temp .= "*:::*";
    }
    $temp = $temp . $$time{week} . "_" . $$time{time};
  }
#  print(" temp = $temp<BR>\n");

  print "<hr>
  <form method=post action=Modify_Course4.cgi>
  <Input type=hidden name=action value=\"modify\">
  <Input type=hidden name=password value=$Input{password}>
  <INPUT type=hidden name=cge_lan_flag value=$Input{cge_lan_flag}>
  <Input type=hidden name=grade value=$Input{grade}>
  <Input type=hidden name=dept_cd value=$Input{dept_cd}>
  <Input type=hidden name=open_dept value=$Input{open_dept}>
  <Input type=hidden name=date value=$temp>
  <table border=1>
  <tr>
  <th bgcolor=yellow>科目名稱(中文)</th><th>";
   print "$Input{cname}<Input type=hidden name=cname value=\"$Input{cname}\">";
  print "
  </th></tr>
  <tr>
  <th bgcolor=yellow>科目名稱(英文)</th><th>";
   print "$Input{ename}<Input type=hidden name=ename value=\"$Input{ename}\">";
  print "</th></tr>
  </table><br>
  <table border=1>
  <tr>
    <th colspan=2 rowspan=13>
  ";

  %time_table_cells = Format_Time(@selected_time);
  $time_table = Print_Timetable(%time_table_cells);
  print $time_table;

  print "
  </th>
  <th bgcolor=yellow>開課年級</th><th>";
  $g_string[1]="一";
  $g_string[2]="二";
  $g_string[3]="三";
  $g_string[4]="四";
  print "$g_string[$Input{grade}]年級</th></tr><tr>
  <th bgcolor=yellow>科目編號:</th><th>";
   print "$Input{id} <Input type=hidden name=course_id value=$Input{id}>";
  print "</th></tr><tr>
  <th bgcolor=yellow>班別</th>
  <th>$Input{group}</th><Input type=hidden name=group value=\"$Input{group}\">";
  print "</th>
  </tr>
  <tr>
  <th bgcolor=yellow>授課老師</th><th>";
   @temp = split(/\*:::\*/,$Input{Teacher});
   foreach $temp(@temp)
   {
    print $Teacher_Name{$temp},"<br>\n";
   }
   print ("<Input type=hidden name=teacher value=$Input{Teacher}>");
   $Input{Teacher} = join(/ /,@temp);
  print "</th></tr>";
  #####  教師專長與授課科目是否符合
  if(  Need_s_match($Input{dept_cd}) ) {
    print qq(
      <tr><th bgcolor=yellow>教師專長與授課科目是否符合</th><th>$S_MATCH{$Input{s_match}}</th></tr>
      <Input type=hidden name=s_match value=$Input{s_match}>
    );
  }
  ############################################################################
  print "
  <th bgcolor=yellow>時數:</th>
  <th>$Input{total_time}
  <Input type=hidden name=total_time value=$Input{total_time}></th></tr>";
############################################################################
print qq(
  <tr><th bgcolor=yellow>正課/實驗實習/書報討論時數:</th>
      <th>$Input{lab_time1}/$Input{lab_time2}/$Input{lab_time3}</th>
  <Input type=hidden name=lab_time1 value=$Input{lab_time1}>
  <Input type=hidden name=lab_time2 value=$Input{lab_time2}>
  <Input type=hidden name=lab_time3 value=$Input{lab_time3}>
);
############################################################################

  print "
  <tr>
  <th bgcolor=yellow>學分:</th>
 <th>$Input{credit}
  <Input type=hidden name=credit value=$Input{credit}>";
####################################################################
  print "
  </th>
  </tr>
  <tr>
  <th bgcolor=yellow>必修/選修/通識</th>
  <th>";
   if($Input{property}==1) { $name="必修"; }
   if($Input{property}==2) { $name="選修"; }
   if($Input{property}==3) { $name="通識"; }
  print $name;
  print "<Input type=hidden name=property value=$Input{property}>";
####################################################################
#  print qq(
#    </th></tr><tr>
#    <th bgcolor=yellow>一般/軍訓/體育</th>
#    <th>
#  );
#   if($Input{suffix_cd}==0) { $suffix_cd="一般"; }
#   if($Input{suffix_cd}==1) { $suffix_cd="軍訓"; }
#   if($Input{suffix_cd}==2) { $suffix_cd="體育"; }
#  print $suffix_cd;
#  print "<Input type=hidden name=suffix_cd value=$Input{suffix_cd}>";
####################################################################

  print "
    </th>
    </tr>
    <tr>
    <th bgcolor=yellow>上課教室:</th>
    <th>";
  print "[$classroom{id}]$classroom{cname}";
  print "<Input type=hidden name=classroom value=\"$classroom{id}\">\n";
  print "</th></tr>";
#####################################################################
#####  開課學制(碩/博班課程) attr
if( !$IS_GRA and !is_Undergraduate_Dept($Input{dept_cd}) and !is_Exceptional_Dept($Input{dept_cd}) ) {
  print qq(
    <TR>
      <TH bgcolor=yellow>開課學制</TH>
      <TH>
        $ATTR{$Input{attr}}
      </TH>    
    </TR>
  );
}
print "<INPUT type=hidden name=attr value=$Input{attr}>"; 

#####################################################################  
  print "<tr><th bgcolor=yellow>篩選原則</th><th>\n";
  my($p,@p_string);
  $p_string[0]="不需篩選";
  $p_string[1]="一次篩選";
  $p_string[2]="二次篩選";
  print "$p_string[$Input{principle}]";
  print "<Input type=hidden name=principle value=$Input{principle}>";
  print "</th></tr></table>\n";
  
  ## draw table for 備註 ##
  print "<table border=1>";
  print "</select></th></tr>\n";
  print "<tr><th bgcolor=yellow>限修人數</th><th>\n";

  if( $is_dept_serv ) {
    #print "dept_serv";
    $temp = 0;
  }else{
    $temp=$Input{number_limit_2}*100+$Input{number_limit_1}*10+$Input{number_limit_0};
  }  
  
  if($temp ne "0") {
    print "$temp 人";
  }else{
    print "無";
  }

  print "<Input type=hidden name=number_limit value=$temp>\n";
  print "</th>";
  ### 保留學生名額 ###
  print "<th bgcolor=yellow>保留新生名額</th><th>\n";
  $temp=$Input{reserved_number_2}*100+$Input{reserved_number_1}*10+$Input{reserved_number_0};
  if($temp ne "0")
  {
   print "$temp 人";
  }
  else
  {
   print "無";
  }
  print "<Input type=hidden name=reserved_number value=$temp>\n";
  print "</th></tr>\n";
  print "<tr><th bgcolor=yellow rowspan=2>支援系所</th><th rowspan=2>\n";
  my(@temp,$temp,%temp);
  if($Input{support_dept} ne "")
  {
   @temp=split(/\*:::\*/,$Input{support_dept});
   foreach $temp(@temp)
   {
    %dept=Read_Dept($temp);
    print $dept{cname},"<br>";
   }
  }
  else
  {
   print "無";
  }
  print "</th><th bgcolor=yellow>支援年級</th><th>\n";
  my(@g_string);
  $g_string[1]="一";
  $g_string[2]="二";
  $g_string[3]="三";
  $g_string[4]="四";
  if($Input{support_grade} ne "")
  {
   @temp=split(/\*:::\*/,$Input{support_grade});
   foreach $temp(@temp)
   {
    print $g_string[$temp],"年級<br>";
   }
  }
  else
  {
   print "無";
  }
  print "</th></tr><tr><th bgcolor=yellow>支援班級</th><th>\n";
  if($Input{support_class} ne "")
  {
   @temp=split(/\*:::\*/,$Input{support_class});
   foreach $temp(@temp)
   {
    print $temp,".";
   }
  }
  else
  {
   print "無";
  }
  print "</th>";
  print "<Input type=hidden name=support_dept value=$Input{support_dept}>\n";
  print "<Input type=hidden name=support_grade value=$Input{support_grade}>\n";
  print "<Input type=hidden name=support_class value=$Input{support_class}>\n";
  print "</th></tr>\n";
  ### 擋修系所 ###
  print "<tr><th bgcolor=YELLOW rowspan=2>擋修系所</th><th rowspan=2>\n";
  if($Input{ban_dept} ne "")
  {
   @temp=split(/\*:::\*/,$Input{ban_dept});
   foreach $temp(@temp)
   {
    %dept=Read_Dept($temp);
    print $dept{cname},"<br>";
   }
  }
  else
  {
   print "無";
  }
  print "</th><th bgcolor=YELLOW>擋修年級</th><th>\n";
  my(@g_string);
  $g_string[1]="一";
  $g_string[2]="二";
  $g_string[3]="三";
  $g_string[4]="四";
  if($Input{ban_grade} ne "")
  {
   @temp=split(/\*:::\*/,$Input{ban_grade});
   foreach $temp(@temp)
   {
    print $g_string[$temp],"年級<br>";
   }
  }
  else
  {
   print "無";
  }
  print "</th></tr><tr><th bgcolor=YELLOW>擋修班級</th><th>\n";
  if($Input{ban_class} ne "")
  {
   @temp=split(/\*:::\*/,$Input{ban_class});
   foreach $temp(@temp)
   {
    print $temp,".";
   }
  }
  else
  {
   print "無";
  }
  print "</th>";
  print "<Input type=hidden name=ban_dept value=$Input{ban_dept}>\n";
  print "<Input type=hidden name=ban_grade value=$Input{ban_grade}>\n";
  print "<Input type=hidden name=ban_class value=$Input{ban_class}>\n";
  print "</th></tr>\n";

####################  支援通識  ####################################
$Input{support_cge_number} = $Input{support_cge_number_1} * 10 + $Input{support_cge_number_0};
print("<INPUT type=hidden name=support_cge_type value=$Input{support_cge_type}>\n");
print("<INPUT type=hidden name=support_cge_number value=$Input{support_cge_number}>\n");
print qq(
  <TR><TH bgcolor=YELLOW>支援通識領域</TH>
     <TH colspan=3>$cge{$Input{support_cge_type}}{sub_cge_id_show} $cge{$Input{support_cge_type}}{cge_name}</TH>
  </TR>
  <TR><TH bgcolor=YELLOW>支援通識人數</TH>
      <TH colspan=3>$Input{support_cge_number}</TH>
  </TR>
);
######################################################################
print qq(
  <TR>
    <TH bgcolor=YELLOW>先修科目</TH>
    <TD colspan=3>
);
if($Input{Precourse} !~ "99999") {
  @temp=split(/\*:::\*/,$Input{Precourse});
  print("<FONT size=-1>\n");
  foreach $temp(@temp) {
    ($predept, $precourse, $pregrade) = split(/:/, $temp);
    %dept_temp = Read_Dept($predept);
    %prerequisite_course = Read_Course($predept, $precourse, "01", "history");
    print("($dept_temp{cname2})($precourse)$prerequisite_course{cname} - $GRADE{$pregrade}<BR> ");
    $pre_course_count++;
  }
} else {
  print "無<BR>";
}
print("<Input type=hidden name=Precourse value=$Input{Precourse}>\n");
print("($PREREQUISITE_LOGIC{$Input{prerequisite_logic}})\n")
  if($pre_course_count >= 2);                                   ###  超過兩門先修課程，才顯示此欄位
print("<INPUT type=hidden name=prerequisite_logic value=$Input{prerequisite_logic}>");
print("</TD></TR>");
######################################################################
#print qq(
#  <TR>
#    <TH bgcolor=PINK>先修科目邏輯關係</TH>
#    <TD colspan=3>$Input{prerequisite_logic}</TD>
#  </TR>
#  <INPUT type=hidden name=prerequisite_logic value=$Input{prerequisite_logic}>
#);

######################################################################

if ($Input{distant_learning} eq "on") {
  $flag_dis = "遠距教學課程";
  $Input{distant_learning} = 1;
}else{
  $flag_dis = "<FONT color=RED>非</FONT>遠距教學課程";
  $Input{distant_learning} = 0;
}

if ($Input{english_teaching} eq "on") {
  $flag_eng = "全英語授課";
  $Input{english_teaching} = 1;
}else{
  $flag_eng = "<FONT color=RED>非</FONT>全英語授課";
  $Input{english_teaching} = 0;
}
if ($Input{gender_eq} eq "on") {
  $flag_gen = "性別平等教育課程";
  $Input{gender_eq} = 1;
}else{
  $flag_gen = "<FONT color=RED>非</FONT>性別平等教育課程";
  $Input{gender_eq} = 0; 
}

if ($Input{env_edu} eq "on") { 
  $flag_env = "環境教育相關課程";
  $Input{env_edu} = 1;
}else{
  $flag_env = "<FONT color=RED>非</FONT>環境教育相關課程";
  $Input{env_edu} = 0;
}


print qq(
  <TR>
    <TH bgcolor=YELLOW>上課方式</TH>
    <TD colspan=3>
      $flag_dis<BR>
      $flag_eng<BR>
      $flag_gen<BR>
      $flag_env
    </TD>
  </TR>
  <INPUT type=hidden name=distant_learning value=$Input{distant_learning}>
  <INPUT type=hidden name=english_teaching value=$Input{english_teaching}>
  <INPUT type=hidden name=gender_eq        value=$Input{gender_eq}>
  <INPUT type=hidden name=env_edu          value=$Input{env_edu}>
);
########################################################################
#####  Added 2009/05/05  Nidalap :D~
#####  暑期授課辦法修訂，暑期所開授之課程分為以下兩類： 
#####  第一類課程：經系（所、中心）課程委員會議審議通過之選修課程。
#####  第二類課程：曾開授之課程，以補救教學為原則。 
#####  請於暑期開排課系統增加選項，排課人員得勾選課程類別，
#####  以利後端課務系統計算最低開課人數、課程收費標準等計算教師鐘點資料。

#if( is_Summer() ) {
if( is_Summer() and !is_GRA() ) {       ### 只作用於「一般生暑修」
  @flag_remedy = ("",
      "第一類課程：經系（所、中心）課程委員會議審議通過之選修課程",
      "第二類課程：曾開授之課程，以補救教學為原則");
  print qq( 
    <tr><th bgcolor=yellow>暑修課程類型</th>
      <td colspan=3>
        $flag_remedy[$Input{remedy}]
      </TD>
    </TR>
    <INPUT type=hidden name=remedy value=$Input{remedy}>
  );
}
##########################################################################

  print "<tr><th bgcolor=yellow>備註欄</th>";
  print "<th colspan=3>";
  print $Input{note};
  print "<Input type=hidden name=note value=\"$Input{note}\">";
  print "</th></tr>
  </table>
  ";
  #####  要求確認的訊息 Added 2012/01/12
  if( $need_confirm_msg ) {
	print "<DIV style='background-color:YELLOW; font-size:250%'>";
    print "<FONT color=RED>$need_confirm_msg<BR>"; 
    print "<INPUT type=checkbox name='yes_i_agree'><B>好的，我知道了。</B><P>";
    print "</DIV>";
    print "<INPUT type=hidden name='need_confirmation' value=1>";
  }  
 
  print "<p>
  <center>
  <Input type=\"submit\" value=\"確定修改科目資料\">
  </form>";
  END:
  print "
  <form>
  <Input type=button onclick=history.back() value=回到上一頁修改資料>
  </form>
  <hr>";
  $Input{dept_cd} = $DEPT_LAN  if( $Input{cge_lan_flag} == 2 );  ### 若是語言中心開通識外語課，還原系所代碼為語言中心
  Links1($Input{dept_cd},$Input{grade},$Input{password});
  print "
  </center>
  </body>
  </html>";
  ## end of html file ##
}
############################################################################
#####  Find Selected_Time
#####  讀取上一頁所選取的開課截次
############################################################################
sub Find_Selected_Time
{
  my(@time, $i, $week, $time);
  $i = 0;
  foreach $key (sort %Input) {
    if($Input{$key} eq "999") {
#      print("$key<BR>\n");
      ($week, $time) = split(/_/, $key);
      $time[$i]{week} = $week;
      $time[$i]{time} = $time;
      $i++;
    }
  }
  return(@time);
}
############################################################################
#####  檢查修習此科目的學生，是否有人會因此而導致衝堂
sub Check_Stu_Time_Collition()
{
  my(@stu, %stu, @cou_of_stu, %other_cou, $other_cou_time, $cou_time, $table_content);
  my(@stu_occupied_time, $i, @sel_time, %Course);

  
  %Course = Read_Course($Input{dept_cd}, $Input{id}, $Input{group},"","","");
  @stu = Student_in_Course($Input{dept_cd}, $Course{id}, $Course{group}, "", "");
  @sel_time = Find_Selected_Time();     ###  更改過的本科目節次

  $i = 0;
  $table_content = "";
  CHECK_STU_TIME_CONFLICT: foreach $stu (@stu) {
    @cou_of_stu = Course_of_Student($stu, "", "");
    ###  先建立 @stu_occupied_time : 學生除本科目以外有課的所有節次
    @stu_occupied_time = ();
    foreach $cou (@cou_of_stu) {
      next  if( ($$cou{id} eq $Course{id}) and ($$cou{group} eq $Course{group}) );
      %other_cou = Read_Course($$cou{dept}, $$cou{id}, $$cou{group}, "", "", "");
      foreach $time (@{$other_cou{time}}) {
        push(@stu_occupied_time, $time);
      }
    }

    ###  檢查 @stu_occupied_time 與本科目新的節次是否衝堂
    foreach $sot (@stu_occupied_time) {
      foreach $time (@sel_time) {
        if( is_Time_Collision($$sot{week}, $$sot{time}, $$time{week}, $$time{time}) ) {
          %stu = Read_Student($stu);
          $table_content .= "<TR>"  if( $i%4 == 0 );
          $table_content .= "<TD>$stu$stu{name}</TD>";
          $table_content .= "</TR>"  if( ($i%4 == 3) );
          $i++;
          next CHECK_STU_TIME_CONFLICT;
        }
      }
    }
  }
  if( $table_content ) {
    $table_content = "
      <P><B><FONT color=RED> 
        本科目目前選修學生中，以下學生會有衝堂問題：
      <FONT><B><BR>
      <TABLE border=1 size=50%>"
        . $table_content . 
      "</TABLE>";
    return $table_content;
  }  
  return "";
}