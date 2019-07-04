1;

############################################################################
#####  Open_Course.pm
#####  開課相關函式
#####  Last Update:
#####   2002/03/14  將原有開課程式中的功能搬到此模組中
#####   2008/01/23  教師教室衝堂檢核功能, 擴充到院層級
#####   2009/05/05  開課限制檢核，將不得連排三小時，改為三小時課程每日一次為限
#####   2009/11/26  教室衝堂排除教授研究室 (代碼 = '0')
#####   2012/04/23  若是以管理者登入，教師教室衝堂檢核擴充到全校。  Nidalap :D~
############################################################################

sub Print_Timetable_Select
{
  my(@my_time_table) = @_;
  my($i, $j, $count, $this_time_string, $this_time_string_temp,
     $time_check_flag);
  print qq(
        <table border=1>
          <tr>
             <th bgcolor=orange>區段/星期</th>
             <th bgcolor=orange>一</th>
             <th bgcolor=orange>二</th>
             <th bgcolor=orange>三</th>
             <th bgcolor=orange>四</th>
             <th bgcolor=orange>五</th>
             <th bgcolor=orange>六</th>
             <th bgcolor=orange>日</th>
             </tr>
  );
  for($i=0; $i<@REGION; $i++) {
    print("<TR>");
    for($j=0; $j<@WEEKDAY; $j++) {
      if($j==0) {                                   ###  顯示區段及時間
        print qq(
          <TD align=CENTER bgcolor=orange>
            $REGION[$i]<BR>
            <FONT size=1>($REGION_TIME[$i])</FONT>
          </TD>
        );
      }else{
        print("<TD>");
        $count = 0;
        foreach $time (@{$TIME_REGION_TABLE[$i]}) {
          $this_time_string = $j . "_" . $time;     ###  星期_截次
          $time_check_flag = "";                    ###  這一堂課是否是上課時間
#          foreach $ele (@{$Course{time}}) {
          foreach $ele (@my_time_table) {
            $this_time_string_temp = $$ele{week} . "_" . $$ele{time};
#            print(" $this_time_string_temp <BR>\n");
            
            if($this_time_string eq $this_time_string_temp ) {
              $time_check_flag = "CHECKED";         ### 這一堂課是上課時間
            }
          }
          print("<INPUT type=CHECKBOX name=\"$this_time_string\" value=999 $time_check_flag>");
          print("$time");
          $count++;
          if( ($count == 2) or ($count == 4) ) {
            print("<BR>");
          }
        }
        print("</TD>\n");
      }
    }
    print("</TR>\n");
  }
  print("</TABLE>\n");
}
#############################################################################
#####  Check_Open_Course_Restrictions
#####  檢查開課時的一些限制規定
#####  輸入: ($action, %Input)
#####  輸出: ($warning_count, $error_count, @message_string)
#####  Last Update: 2002/03/19 Nidalap :D~
#####   2009/05/05  開課限制檢核，將不得連排三小時，改為三小時課程每日一次為限
#####   2010/03/26  「教師專長與授課科目是否符合」s_match 欄位不得為 0  Nidalap :D~
#####	2010/04/08  只有教師為教師待聘，「教師專長與授課科目是否符合」s_match 欄位才可為 7  Nidalap :D~
#####   2010/04/16  4小時課程排課可排成 3+1  (做得零零落落)  Nidalap :D~
#####               偵測到併班上課課程（授課教師及上課時間相同）則可以略過「專任教師每日以一門三小時連排為限」  Nidalap :D~
#####   2010/04/20  若篩選原則與期待不同，給予警訊 Nidalap :D~
#####   2010/10/22  若語言中心開通識外語課，檢查科目代碼 Nidalap :D~
#####   2010/12/08  課程異動期間，不得選「教師待聘」  Nidalap :D~  <--- 已移除！ 2015/01/30
#####   2011/04/25  系所服務學習課程可不做若干檢查，如限修人數與篩選原則對應等  Nidalap :D~
#####   2012/04/11  新增開課學制(碩/博班課程)欄位 attr，只有在研究所課程中需要選擇.  Nidalap :D~
#####   2015/01/30  移除「課程異動期間不得選教師待聘」限制(淳純電話中要求)   Nidalap :D~ 
#####   2015/??/??  若勾選二次篩選，必須勾選保留新生名額，反之亦然。 Nidalap :D~
#####   2015/12/07  學系服務學習課程的體育課衝堂檢核層級降低為警告。 Nidalap :D~
#####	2016/03/28  教室必須要選擇，否則不可存檔。 Nidalap :D~
#####   2016/03/28  除了體育中心以外，學分數不可為 0。 Nidalap :D~
#####   2016/05/11  將學分數可為 0 的條件拉到 Allow_Zero_Credit() 判斷   Nidalap :D~
#############################################################################
sub Check_Open_Course_Restrictions
{
  my($wc, $ec, @ms, $i);    ### $warning_count, $error_count, @message_string
  my($action, %Input) = @_;
  $i = $wc = $ec = 0;
  my $is_dept_serv = 0;
  $is_dept_serv = 1     if( $Input{id} eq Get_Dept_Serv_Course_ID($Input{dept_cd}) );

#  foreach $key (sort keys %Input) {
#    print("$key -> $Input{$key}<BR>\n");
#  }

  #####  檢查某些必要欄位:
  #####		1. 沒有輸入科目中英文名稱及代碼
  #####		2. 沒有設上課時數或學分
  #####		3. 科目代碼固定為7碼
  #####		4. 教室必須要選擇(added 2016/03/28 Nidalap :D~)
  if($Input{id} eq "") {                             ###  檢查是否有科目代碼
    $ms[$i++] = "嚴重錯誤: 沒有輸入科目代碼";
    $ec++;
  }elsif(length($Input{id}) != 7 ) {                 ###  必須剛好七碼
    $ms[$i++] = "嚴重錯誤: 科目代碼必須是七碼";
    $ec++;
  }
  if($Input{cname} eq "" || $Input{ename} eq "") {   ###  中英文名稱
    $ms[$i++] = "嚴重錯誤: 沒有輸入科目名稱";
    $ec++;
  }
  if($Input{classroom} eq "") {						 ###  教室
    $ms[$i++] = "嚴重錯誤: 請選擇上課教室";
    $ec++;
  }
  
  
  #print "allow zero credit = " . Allow_Zero_Credit($Input{id}, $Input{dept_cd}) . "<BR>\n";
  
  #if(($Input{credit} eq "0") and (($Input{dept_cd} ne $DEPT_PHY) and !$is_dept_serv) ) {
  if(($Input{credit} eq "0") and !Allow_Zero_Credit($Input{id}, $Input{dept_cd}) ) {
    $ms[$i++] = "嚴重錯誤: 學分數不可為 0";			###  學分數不可為0(體育中心等特定條件除外)
    $ec++;
  }  
  
  ################ 若語言中心開通識外語課，檢查科目代碼
  if( $Input{cge_lan_flag} == 2 ) {
    if( ($Input{id} !~ /^7102/) or ($Input{grade} != 1) ) {
	  $ms[$i++] = "嚴重錯誤: 語言中心開設的通識課，必須為通識外語課(科目代碼為 7102xxx)，且年級必須為 1";
	  $ec++;
	}
  }
  ################  不可 "新增" 歷年科目
  if( $action eq "add" ) {                           ### 新增科目才檢查
    if( $Input{new_course_flag} == 1 )  {
      @all_course = Find_All_Course($Input{dept_cd}, "", "HISTORY");
      foreach $all_course (@all_course) {
        if($Input{id} eq $$all_course{id}) {
          %collision_course = Read_Course($Input{dept_cd}, $$all_course{id},
                                          "01", "HISTORY", "");
          $ec++;
          $ms[$i++]="嚴重錯誤: 科目代碼與歷年科目<FONT color=RED>$collision_course{cname}</FONT>衝突<br>\n";
          $temp_all_course_collision = 1;
          break;
        }
      }
      %a30tcourse = Read_a30tcourse();
      
      if( ( defined($a30tcourse{$Input{id}}{id}) ) and ($temp_all_course_collision != 1) ) {
        $ec++;
        $ms[$i]="嚴重錯誤: 科目代碼與歷年科目<FONT color=RED>$a30tcourse{$Input{id}}{cname}</FONT>衝突!";
        $ms[$i].="<FONT color=RED>此歷年科目不曾成功\開設, 請洽教學組移除歷年資料後方可用此代碼!</FONT><br>\n";
        $i++;
        break;
      }
    }
  }
  ################  檢查該科目是否在當學期已經開過(新增科目和修改科目要求不同)
  if( $action eq "add" ) {                                      ###  新增
    if(-e $COURSE_PATH.$Input{dept_cd}."/".$Input{id}."_".$Input{group}) {
      $ms[$i++] = "本科目已經開課完畢, 欲修改科目內容請由主選單使用修改當學期已開科目之功\能";
      $ec++;
    }
  }else{                                                        ###  修改
    if(!(-e $COURSE_PATH.$Input{dept_cd}."/".$Input{id}."_".$Input{group})) {
#      print("$COURSE_PATH, $Input{dept_cd}, $Input{id}, $Input{group}<BR>");
      $ms[$i++] = "科目資料不存在, 欲新增科目內容請由主選單使用新增當學期已開科目之功\能";
      $ec++;
    }
  }
  ########  教師專長與授課科目是否符合 s_match 不得為 0(未選擇)
  if( $Input{s_match} eq "0" ) {
    $ms[$i++] = "請選擇「教師專長與授課科目是否符合」欄位";
    $ec++;
  }
  ########  只有教師為教師待聘，「教師專長與授課科目是否符合」s_match 欄位才可為 7(教師待聘)
  if( ($Input{s_match} eq "7") and ($Input{Teacher} ne "99999") ) {
    $ms[$i++] = "「教師專長與授課科目是否符合」欄位不得為「教師待聘」";
    $ec++;
  }
  ########  課程異動期間，不得選「教師待聘」(依賴 %system_settings 全域變數)  <--- 2015/01/30 移除
#  print %system_settings;
#  if( ($system_settings{current_system_timeline} >=2) and ($system_settings{current_system_timeline} <=4) ) {
#    if( $Input{Teacher} eq "99999" ) {
#      $ms[$i++] = "課程異動期間，教師欄位不得為「教師待聘」";
#      $ec++;
#    }
#  }
  
  ########  上課時數與時間表上打勾時數要一致
  if($Input{total_time} != $total_selected_time) {
    $ms[$i++] = "嚴重錯誤: 上課時數與時間表上打勾時數不合";
    $ec++;
  }  
  ########  上課時數應等於正課+實驗實習+書報討論時數
  if($Input{total_time} != $Input{lab_time1} + $Input{lab_time2} + $Input{lab_time3} ) {
    $ms[$i++]="嚴重錯誤: 上課時數應等於正課+實驗實習+書報討論時數";
    $ec++;
  }
  ########  一般生開課系統不可開星期六日的課(管理者除外)
  if( ($SUB_SYSTEM == 1) and ($SUPERUSER != 1) ) {    ## 只適用於一般生開課
    foreach $selected_time (@selected_time) {
      if( ($$selected_time{week} =~ /^6/) or
          ($$selected_time{week} =~ /^7/) ) {      ## 不可開星期六日的課
        $ms[$i++]="嚴重錯誤: 欲開星期六日的課請洽教務處!";
        $ec++;
      }
    }
  }
  ########  教室和教師衝堂檢核
  my(@other_course, $j, %course, $conflict_flag);
  
  my %dept	= Read_Dept($Input{dept_cd});
  my $this_college = $dept{college};
  my @all_dept	= Find_All_Dept();
  my @same_college_depts;

  if( $SUPERUSER eq "1" ) {			###  如果目前使用者是管理者(2012/04/23)
    @same_college_depts = @all_dept;  		###    就將所有系所列入教師教室檢核
  }else{
    if( $Input{dept_cd} eq "I001" ) {		###  如果開課系所是通識中心
      foreach $all_dept (@all_dept)  {          ###    就將所有系所列入教師教室檢核
        push(@same_college_depts, $all_dept);
      }
    }else{
      foreach $all_dept (@all_dept)  {		###  如果開課系所是一般系所
        %dept = Read_Dept($all_dept);		###    就檢查屬於同一學院的所有系所, 以及通識中心
        if( $dept{college} == $this_college ) {
          push(@same_college_depts, $all_dept);
        } 
      }
      push(@same_college_depts, "I001");
    }
  }
#  print("same college depts = ", @same_college_depts);  
  foreach $same_college_dept (@same_college_depts) {
    %dept = Read_Dept($same_college_dept);
#    print("checking college $same_college_dept...<BR>\n");
    @other_course = Find_All_Course($same_college_dept);
    for($j=0; $j<@other_course; $j++) {                   ### 檢查同系所有科目
      if( not ( ($other_course[$j]{id}    eq $Input{id})    and 
                ($other_course[$j]{group} eq $Input{group})     )   )  {
        %course=Read_Course($same_college_dept, $other_course[$j]{id}, $other_course[$j]{group});
        $conflict_flag = 0;
        foreach $selected_time (@selected_time) {         ### 本科目的每一截次
          foreach $time (@{$course{time}}) {              ### 別科目的每一截次
            $collition_flag =
                 is_Time_Collision($$selected_time{week}, $$selected_time{time},
                                   $$time{week}, $$time{time});
            if( $collition_flag != 0 ) {                  ###時間相衝
              $conflict_flag = 1;
            }
          }
        }
        if( $conflict_flag == 1 ) {
          if( ($course{classroom} eq $Input{classroom}) and ($Input{classroom} ne '0') ) {
            $ms[$i++] = "系統警告: 同一時段有教室衝堂情形發生: ( $dept{cname} 的 $course{cname}, 
                         代碼 $course{id}, $course{group} 班) 系統仍接受開課資料.";
            $wc++;
            $need_confirm_msg = $ms[$i-1];			###  全域變數，要求勾選同意
          }
          @temp = split(/\*:::\*/,$Input{Teacher});
#          print("teacher = $Input{Teacher}<BR>\n");
#          print("Input = ", %Input, "<BR>\n");
          foreach $temp (@temp) {                           ### 本科目每一教師
            foreach $temp2 (@{$course{teacher}}) {          ### 別科目每一教師
              if( $temp eq $temp2 ) {
#                print("checking $temp <-> $temp2<BR>\n");
                next  if( $temp eq "99999" );               ### 排除 "教師未定"
                $ms[$i++] = "系統警告: 同一時段有授課教師衝堂情形發生
                           ($dept{cname} 的 $course{cname}, 代碼 $course{id}, $course{group} 班)
                           系統仍接受開課資料.";
                $wc++; 
                $need_confirm_msg = $ms[$i-1];			###  全域變數，要求勾選同意
              }
            }
          }
        }
      }
    }
  }
  ########  if 勾選支援系所 then 必須勾選支援年級 (added 2008/03/28 Nidalap :D~ ) 
  if( $Input{support_dept} )  {
    if( !$Input{support_grade} )  {
      $ms[$i++] = "嚴重錯誤: 若勾選支援系所, 則必須勾選支援年級.";
      $ec++;
    }
  }  
  
  ########  一二年級體育與必修不可衝堂 (added 2006/19/19 Nidalap :D~)
  $conflict_flag = 0;
  my($support_dept);
  if( $Input{grade} <= 2 ) {
    $physical_dept = "F000";
    if( $Input{dept_cd} eq $physical_dept ) {		### 體育中心開的課, 檢查支援系所的必修
      my(@all_dept) = Find_All_Dept();
      foreach $all_dept (@all_dept) {			### foreach 所有 "系"
        next if( $all_dept !~ /4$/);
        @all_course = Find_All_Course($all_dept, $Input{grade});
        for( $j=0; $j<@all_course; $j++) {		### foreach 所有課 of 所有系
		  $conflict_flag2 = 0;
		  $conflict_flag2 = 1  if( $all_course[$j]{id} eq Get_Dept_Serv_Course_ID($course{dept}) );		###  學系服務學習課程
          $conflict_flag = 0;
          %course = Read_Course($all_dept,$all_course[$j]{id},$all_course[$j]{group});
          if( @{$course{support_dept}} ) {  		### 如果此課有支援, 檢查支援系所
            @target_dept = @{$course{support_dept}};
            @target_class = @{$course{support_class}};
          }else{					### 如果沒有, 檢查開課的系
            @target_dept = ($all_dept);
            @target_class = @AVAILABLE_CLASSES;
          }
          
          
          if( ($course{grade} == 1 ) or ($course{grade} == 2 ) ) {  ### 所有支援系所一二年級的課
            if( $course{property} == 1 ) {                          ###   必修課
#              print("checking course $course{id} _ $course{group}<BR>\n");
              foreach $target_dept (@target_dept) {
                my @support_dept = split(/\*:::\*/, $Input{support_dept});	  ### 現在看這門體育課
                foreach $support_dept (@support_dept) {                       ### 所有支援系所同年級的課
                  if( $support_dept eq $target_dept ) {
                    my @support_class = split(/\*:::\*/, $Input{support_class});
                    foreach $support_class (@support_class) {			### 檢查所有支援「班別」
                      foreach $target_class (@target_class)  {
                        if( $support_class eq $target_class ) {
#                        print("checking course $course{id} _ $course{group}<BR>\n");
                          foreach $selected_time (@selected_time) {                ### 本科目的每一截次
                            foreach $time (@{$course{time}}) {                     ### 別科目的每一截次
                              $collition_flag =
                                     is_Time_Collision($$selected_time{week}, $$selected_time{time},
                                               $$time{week}, $$time{time});
                              if( $collition_flag != 0 ) {                         ###時間相衝
                                $conflict_flag = 1;
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
          if( $conflict_flag == 1 ) {
            if( $course{grade} == 1 ) {
			  if( $conflict_flag2 == 1 )  {			###  服務學習課程只做警告，不視為嚴重錯誤(2015/12/07)
			    $ms[$i++] = "系統警告: 同一時段有二年級必修課與體育課衝堂情形發生 
                             ($course{cname}, 代碼 $course{id}, $course{group} 班).";
                $wc++;
			  }else{
                $ms[$i++] = "嚴重錯誤: 同一時段有一年級必修課與體育課衝堂情形發生 
                             ($course{cname}, 代碼 $course{id}, $course{group} 班).";
                $ec++;
			  }
            }else{
              $ms[$i++] = "系統警告: 同一時段有二年級必修課與體育課衝堂情形發生 
                           ($course{cname}, 代碼 $course{id}, $course{group} 班).";
              $wc++;
            }
          }
        }
      }
    }else{						### 專業必修課, 檢查支援該系的體育課
	  $conflict_flag2 = 1  if( $is_dept_serv );		###  學系服務學習課程
      my @support_dept = split(/\*:::\*/, $Input{support_dept});
      if ($support_dept[0] eq "" ) {			### 如果本科目沒有支援, 檢查支援此系所的體育課
        @target_dept = ($Input{dept_cd});
      }else{						### 如果本科目有支援, 檢查支援 "那些支援系所" 的體育課
        @target_dept = @support_dept;
      }
      
      my @support_class = split(/\*:::\*/, $Input{support_class});
      if ($support_class[0] eq "" ) {                    ### 如果本科目沒有支援, 檢查支援此班級的體育課
        @target_class = ('A','B','C','D');
      }else{                           	                 ### 如果本科目有支援, 檢查支援 "那些支援年級" 的體育課
        @target_class = @support_class;
      }
      
#      print("support dept,class = $Input{support_dept}, $Input{support_class}<P>\n");
#      print("target dept,class = @target_dept, @target_class<P>\n");
      
      @other_course = Find_All_Course($physical_dept, $Input{grade});
      
      for( $j=0; $j<@other_course; $j++) {			### 所有體育課
        $conflict_flag = 0;
        %course=Read_Course($physical_dept,$other_course[$j]{id},$other_course[$j]{group});

#        print("正在檢查體育課 $course{id} _ $course{group}...<BR>\n");

        foreach $support_dept (@{$course{support_dept}}) {
          foreach $target_dept (@target_dept) {			### 對於所有本科目支援的系所
            if( $support_dept eq $target_dept ) {		### if(體育課支援系所 == 此科目支援系所)
			  if( (@{$course{support_dept}}!=0) and (@{$course{support_class}}==0) ) {
	            @{$course{support_class}} = @AVAILABLE_CLASSES;		### 若勾選支援系所卻沒有溝選支援班級，預設為全部
              }
              foreach $support_class (@{$course{support_class}}) {
#			    print("正在檢查支援年級 $support_class<BR>\n");
                foreach $target_class (@target_class) {		###   對於所有本科目支援的班級(added 2007/05/17)
                  if( $support_class eq $target_class )  {	###   if(體育課支援班級 == 此科目支援班級)

#                    print("$course{id} _ $course{group} supports dept $support_dept $support_class<br>\n");

                    foreach $selected_time (@selected_time) {         ### 本科目的每一截次
                      foreach $time (@{$course{time}}) {              ### 別科目的每一截次
                        $collition_flag =
                             is_Time_Collision($$selected_time{week}, $$selected_time{time},
                                               $$time{week}, $$time{time});
                        if( $collition_flag != 0 ) {                  ###時間相衝
                          $conflict_flag = 1;
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
        if( $conflict_flag == 1 ) {
          if( $course{grade} == 1) {
			if( $conflict_flag2 == 1 )  {			###  服務學習課程只做警告，不視為嚴重錯誤(2015/12/07)
			  $ms[$i++] = "系統警告: 同一時段有二年級必修課與體育課衝堂情形發生 
                           ($course{cname}, 代碼 $course{id}, $course{group} 班).";
              $wc++;
			}else{
              $ms[$i++] = "嚴重錯誤: 同一時段有一年級必修課與體育課衝堂情形發生 
                           ($course{cname}, 代碼 $course{id}, $course{group} 班).";
              $ec++;
			}
          }else{
            $ms[$i++] = "系統警告: 同一時段有二年級必修課與體育課衝堂情形發生 
                         ($course{cname}, 代碼 $course{id}, $course{group} 班).";
            $wc++;
          }
        }
      }
    }
  }
    

  ########  有勾選限修人數, 則必須勾選篩選原則, 反之亦然
  if( $is_dept_serv != 1 ) {			###  系所服務學習課程除外
    $temp_flag1 = $temp_flag2 = 0;
    if( $Input{principle} ne "0" ) {
      $temp_flag1 = 1;                         ### [0,1] = [不篩選, 篩選]
    }
    if( ($Input{number_limit_0} + $Input{number_limit_1}
         + $Input{number_limit_2}) != 0 ) {
      $temp_flag2 = 1;                         ### [0,1] = [沒限修, 限修]
    }
    if( $temp_flag1 != $temp_flag2 ) {
      if( $SUPERUSER == 1 ) {			###  管理者的話, 只給警告
        $ms[$i++]="系統警告(針對管理者): 有勾選限修人數, 則必須勾選篩選原則, 反之亦然!";
        $wc++;
                  
      }else{					###  一般使用者, 視為嚴重錯誤
        $ms[$i++]="嚴重錯誤: 有勾選限修人數, 則必須勾選篩選原則, 反之亦然!";
        $ec++;
      }
    }
    ########  若篩選原則與期待不同，給予警訊 (2010/04/20 Nidalap :D~)
    if( ($Input{dept_cd} =~ /6$/) and ($Input{dept_cd} ne $DEPT_CGE) and ($Input{principle} ne "0") ) {
      $ms[$i++]="系統警告: 碩博班課程原則上應為不需篩選, 但系統仍接受一次篩選!";
      $wc++;          
    }
#    print("$TERM, $Input{grade}, $Input{dept_cd}, $Input{principle}<BR>\n");
    if( ($TERM == 1) and ($Input{grade} eq "1") and ($Input{dept_cd} !~ /6$/) and ($Input{principle} ne "2") ) {
      $ms[$i++]="系統警告: 第一學期大一學士班課程原則上應為二次篩選, 但系統仍接受一次篩選!";
      $wc++;            
    }
  }
  
  ########  保留新生名額必須小於等於限修人數 (2003/06/18,Nidalap :D~)
  my $num_limit_temp = $Input{number_limit_2}*100 + $Input{number_limit_1}*10 + $Input{number_limit_0};
  my $res_number_temp = $Input{reserved_number_2}*100 + $Input{reserved_number_1}*10 + $Input{reserved_number_0};
  if( $num_limit_temp < $res_number_temp ) {
    $ms[$i++]="嚴重錯誤: 保留新生名額必須小於等於限修人數.";
    $ec++;
  }
  ########  若勾選二次篩選，必須勾選保留新生名額，反之亦然。(2014/??/??, Nidalap :D~)
  if( $Input{principle} eq "2" ) {
    if( $res_number_temp == 0 ) {
	  $ms[$i++]="嚴重錯誤: 若勾選二次篩選，必須勾選保留新生名額。";
      $ec++;
	}
  }
  if( $res_number_temp != 0 ) {
    if( $Input{principle} ne "2" ) {
	  $ms[$i++]="嚴重錯誤: 若勾選保留新生名額，必須勾選二次篩選。";
      $ec++;
	}
  } 
  
  ########  若勾選保留新生, 必須是開在大一的課.  (2003/06/18,Nidalap:D~)
  ########  2003/08/15 加入通識中心除外判斷 Nidalap :D~
  if( ($Input{reserved_number_0} + $Input{reserved_number_1} 
        + $Input{reserved_number_2}) != 0 ) {
     if( ($Input{grade} != 1) and ($Input{dept_cd} ne "I001") ) {
       $ms[$i++]="嚴重錯誤: 若勾選保留新生, 必須是開在大一的課.";
       $ec++;
     }
  }
  ########  若勾選支援通識領域則必須勾選支援通識人數, 反之亦然
  if( $is_dept_serv != 1 ) {			###  系所服務學習課程除外
    $temp_flag1 = $temp_flag2 = 0;
    if( $Input{support_cge_type} ne "0") {
      $temp_flag1 = 1;                         ### [0,1] = [不支援, 支援某領域]
    }
    if( ($Input{support_cge_number_0} + $Input{support_cge_number_1}) != 0 ) {
      $temp_flag2 = 1;                         ### [0,1] = [沒選人數, 有選人數]
    }
    if( $temp_flag1 != $temp_flag2 ) {
      $ms[$i++]="嚴重錯誤: 若勾選支援通識領域則必須勾選支援通識人數, 反之亦然!";
      $ec++;
    }
  }   
  ########  課程所選截次本身不可衝堂
  foreach $time (@selected_time) {
    foreach $time2 (@selected_time) {
      if( ($$time{week} eq $$time2{week}) and ($$time{time} eq $$time2{time})) {
        next;                                  ### 不檢查自己相衝
      }
      if( $$time{time} =~ /[A-Z]/ ) {          ### 自己相衝只有 50 <-> 75,
        next;                                  ### 所以不重複檢查
      }
      $collisiton_flag = is_Time_Collision($$time{week}, $$time{time},
                                           $$time2{week}, $$time2{time},);      
      if($collisiton_flag != 0) {
        $ms[$i++]="嚴重錯誤: [星期$$time{week}第$$time{time}堂課]和 [星期$$time2{week}第$$time2{time}堂課] 有衝堂情形發生!";
        $ec++;
      }
    }  
  }

  %immune_status = Read_Immune_Record($Input{id}, $Input{group});
#  foreach $k (keys %immune_status) {
#    print("$k -> $immune_status{$k}<BR>\n");
#  }
  
  ####################################################################################################################
  #####  大學部課程除實習、實驗課程之外，不可排連續3小時的課程(允許加簽)  <--- 2009/05 以前是這樣子的規則，以後取消了
  #####  學士班三學分之課程採連排者，專任教師每日以一門為限		  <--- 2009/05 以後採此規則
  my(@teacher, @teacher_course, %teacher_course, @teacher_course_time, @teacher_course_consequtive_weekday, $temp);
  my @consequtive_weekday;
  if( $SUB_SYSTEM != 1 ) {
    #####  非一般生系統, 不做檢查
  }elsif( $immune_status{r1} != 1 ) {

    foreach $temp (@selected_time) {
      $time_string_identifier .= $$temp{week} . $$temp{time} . "_";	###  課程時間的識別字串，用作判斷是否併班上課(同時段同教師)
    }
#    print $time_string_identifier;
    Read_Teacher_File();           
    if( is_Undergraduate_Dept($Input{dept_cd}) or is_Undergraduate_Dept($Input{dept_id}) ) {
      if( ($Input{lab_time2}+$Input{lab_time3}) == 0 ) {	 	###  如果沒實習實驗
#        foreach $temp (@selected_time) {
#          print("$$temp{week} $$temp{time}<BR>");
#        }
      
	@consequtive_weekday = Check_Consequtive_3_Hours(@selected_time);
	if( @consequtive_weekday ) {					###  如果有連續三小時課程
	  ##  找出該科目所有教師開的所有課目，檢查是否在同一天有連續三小時
	  foreach $weekday (@consequtive_weekday) {			###  foreach 有連續三小時發生的星期日子
#	    print("checking weekday $weekday...<BR>\n");
            @teacher = split(/\*:::\*/,$Input{Teacher});
	    foreach $teacher (@teacher) {				###    foreach 本科目每一個教師
              next  if( $teacher eq "99999" );				### 	 排除 "教師未定"
	      @teacher_course = Course_of_Teacher($teacher);
	      foreach $teacher_course (@teacher_course) {		###      foreach 該教師的每一門課
#	        print("checking teacher $teacher 's course $$teacher_course{id}_$$teacher_course{group} on weekday $weekday...<BR>\n");
	        if( $Input{NewOpen} != 1 )  {				###        如果本科目不是新開的, 除外自己    
	          if( ($Input{id} eq $$teacher_course{id}) and ($Input{group} eq $$teacher_course{group}) ) {
#	            print("除外自己: $Input{id} _ $Input{group}<BR>\n");
	            next;
	          }
	        }
	        next if(!is_Undergraduate_Dept($$teacher_course{dept}));###	   除外研究所課程
	        %teacher_course = Read_Course($$teacher_course{dept}, $$teacher_course{id}, $$teacher_course{group});
	        @teacher_course_time = @{$teacher_course{time}};
	        
	        $time_string_identifier_t = "";
	        foreach $temp (@teacher_course_time) {			###  課程時間的識別字串，用作判斷是否併班上課(同時段同教師)
	          $time_string_identifier_t .= $$temp{week} . $$temp{time} . "_";
                }
#                print("$time_string_identifier eq $time_string_identifier_t; $Input{classroom} eq $teacher_course{classroom}<BR>");
                if( ($time_string_identifier eq $time_string_identifier_t) and  	
                    ($Input{classroom} eq $teacher_course{classroom}) )  {	###  併班上課 : 同時間, 同教室
                  $ms[$i] = "系統警告: $Teacher_Name{$teacher} 老師於同時段另開了科目 $teacher_course{cname}";
                  $ms[$i] .= "(科目代碼 $teacher_course{id}, 班別 $teacher_course{group}) ";
                  $ms[$i] .= " 系統判斷應與本課為併班上課，不予阻擋. 若不是併班上課，請回上頁修改！";
                  $i++;
                  $wc++;
                  next;
                }

#	        print("checking teacher course $teacher_course{cname}<BR>\n");
                @teacher_course_consequtive_weekday = Check_Consequtive_3_Hours(@teacher_course_time);
                foreach $temp2 (@teacher_course_consequtive_weekday) {	###         foreach 教師每一門課連續三小時的那一天
#                  print("checking teacher course $$teacher_course{id}_$$teacher_course{group} $temp2 <-> $weekday ...<BR>\n");
                  if( $temp2 eq $weekday ) {
                    Read_Teacher_File();
                    $ms[$i] = "嚴重錯誤: $Teacher_Name{$teacher} 老師開設的科目 $teacher_course{cname}";
                    $ms[$i] .= "(科目代碼 $teacher_course{id}, 班別 $teacher_course{group}) ";
                    $ms[$i] .= " 已經在星期$WEEKDAY[$weekday]使用了連續三小時課程! 若欲開課, 請洽教學組!";
                    $i++;
                    $ec++;
                  }
                }
	      }
            }
	  }
	}
      }
    }
  }  
  ########  課程不可跨區段開排課(允許加簽)
  if( $SUB_SYSTEM != 1 ) {
    #####  非一般生系統, 不做檢查
  }elsif( not(is_Undergraduate_Dept($Input{dept_cd}) or is_Undergraduate_Dept($Input{dept_id})) ) {
    #####  碩士班, 也不做檢查 (Added 2006/03/21)
  }elsif( $immune_status{r2} != 1 ) {
    foreach $time (@selected_time) {
      if( $first_region eq "" ) {                      ###  第一堂課的 "區段"
        $first_region = $REGION_TIME_TABLE{$$time{time}};
      }else{
        $this_region = $REGION_TIME_TABLE{$$time{time}};
        if($this_region ne $first_region) {
          $same_region_check = -1;
        }
      }
    }
    if( $same_region_check == -1 ) {
      $ms[$i++]="嚴重錯誤: 課程不可跨區段開排課!";                            
      $ec++;
    }
  }
  ########  課程如果跨天，且必須在同一時段(一三五/二四)(允許加簽)
  if( $SUB_SYSTEM != 1 ) {
    #####  非一般生系統, 不做檢查
  }elsif( $immune_status{r3} != 1 ) {
    foreach $time (@selected_time) {
      if( $first_weekday_region eq "" ) {                ### 第一堂課的 "時段"
        $first_weekday_region = $WEEKDAY_REGION{$$time{week}};
      }else{
        $this_weekday_region = $WEEKDAY_REGION{$$time{week}};
        if($this_weekday_region ne $first_weekday_region) {
          $same_weekday_region_check = -1;
        }
      }
    }
    if( $same_weekday_region_check == -1 ) { 
      $ms[$i++]="嚴重錯誤: 課程如果跨天, 必須在同一時段(星期一三五或二四)!";
      $ec++;
    }          
  }
  ######## 課程如果跨天，必須在同截次(允許加簽)
  my $same_time_check = 0;
  if( $SUB_SYSTEM != 1 ) {
    #####  非一般生系統, 不做檢查
  }elsif( $immune_status{r4} != 1 ) {  ##### 以下有許多redundant code, 應設法精簡
    my(@st);
    @st = @selected_time;
    $time_count = @st;                 ##### 若有 (?) 堂課, 則該如何處理...
    if( $time_count == 2 ) {             ### case 兩堂課: 不同天則必須同截次
      if( ($st[0]{week} ne $st[1]{week}) and 
          ($st[0]{time} ne $st[1]{time}) )   {
        $same_time_check = -1;
      }
    }elsif( $time_count == 3 ) {         ### case 三堂課
                                         ###   case 三堂課都在不同天
      if( ($st[0]{week} ne $st[1]{week}) and
          ($st[0]{week} ne $st[2]{week}) and
          ($st[1]{week} ne $st[2]{week}) )   {
        if( not( ($st[0]{time} == $st[1]{time}) and
                 ($st[0]{time} == $st[2]{time})      ) ) {
          $same_time_check = -1;
        }
      }
                                         ###   case 其中兩堂同天
      if( ($st[0]{week} eq $st[1]{week}) or
          ($st[0]{week} eq $st[2]{week}) or
          ($st[1]{week} eq $st[2]{week}) )  { 
        if( ($st[0]{week} eq $st[1]{week}) and
            ($st[0]{week} eq $st[2]{week}) and
            ($st[1]{week} eq $st[2]{week}) )   {
                                                     ###    case 三堂同天
        }elsif( ($st[0]{time} ne $st[1]{time}) and   ###    case 只有兩堂同天
            ($st[0]{time} ne $st[2]{time}) and
            ($st[1]{time} ne $st[2]{time}) )   {
          $same_time_check = -1;
        }
      }
    }elsif( $time_count == 4 ) {         ### case 四堂課
      my(%timecount);
      foreach $time (@st) {
        if( not defined($timecount{$$time{time}}) ) {
          $timecount{$$time{time}} = 1;
        }
      }
      $timecount = keys(%timecount);
      my(%daycount);
      foreach $time (@st) {
        if( not defined($daycount{$$time{week}}) ) {
          $daycount{$$time{week}} = 1;
        }
      }
      $daycount = keys(%daycount);

      if( $timecount == 2 ) {            ###   case 共用了兩個不同截次
        
      }
      if( $timecount >= 3 ) {
        if($daycount > 2) {             ###     四堂課不得分佈在兩天以上
          $same_time_check = -1;
        }
      }
      
    }
  
    if( $same_time_check == -1 ) {
      $ms[$i++]="嚴重錯誤: 課程如果跨天，必須在同時間!";
      $ec++;
    }
  }
  ########  檢查是否沒有輸入某些非必要欄位:
  ########    沒有設定授課教師(warning only)
  if( ($Input{Teacher} eq "99999") or ($Input{Teacher} eq "99999") ) {
    $ms[$i++] = "系統警告: 沒有設定授課教師, 系統仍接受開課資料.";
    $wc++;
  }
  
  #####  檢查是否輸入開課學制
    
  if( $Input{attr} eq "0" ) {
    $ms[$i++] = "嚴重錯誤: 請選擇開課學制(碩士/博士/碩博合開課程)";
    $ec++;
  }
  
  ########    沒有設定上課教室(warning only)
  # No need...
  ########    沒有設定科目屬性, 將定為必修(warning only)
  # No need, too...
  ########    沒有設定篩選原則, 將定為不須篩選(warning only)
  # No need, three...

  return($wc, $ec, @ms);
}
##########################################################################
#####  傳入系所代碼與科目代碼，判別是否允許開 0 學分的課
#####  Updates:
#####    2016/05/11 原本只有體育中心開的課可以允許 0 學分，赫然發現另外還有服務學習課程，
#####				和台文所、語言中心開設的通識課等，所以拉出來到此判斷。  by Nidalap :D~
sub Allow_Zero_Credit
{
  my ($cid, $dept_cd) = @_;
  my $allow = 0;
  my @allow_dept = ($DEPT_PHY, $DEPT_CGE, "1416");		###  體育、通識、台文所
  
  if( $cid eq Get_Dept_Serv_Course_ID($dept_cd) ) {
    $allow = 1;											###  學系服務學習
  }
  foreach $a_dept(@allow_dept) {
    if( $dept_cd eq $a_dept ) {
	  $allow = 1;
	}
  }  
  return $allow;
}

##########################################################################
#####  檢查傳入開課時間，是否有連續三小時的存在
sub Check_Consequtive_3_Hours
{
  my @selected_time = @_;
  my $last_week, $last_time, $consequtive_hours, @consequtive_weekday=();

        foreach $time (@selected_time) {
#          print("checking time [$$time{week}, $$time{time}]<BR>");
          if( $last_week eq $$time{week} ) {       ##### 同一天的課程
            if( $$time{time} =~ /[A-Z]/ ) {          ### 75分鐘型的連續判斷
              if( (ord($$time{time})-ord($last_time)) == 1) {
                $consequtive_hours+=3;
              }
            }else{                                   ### 50分鐘型的連續判斷
              if( ($$time{time}-$last_time) == 1 ) {
                $consequtive_hours++;
              }
            }
#            print("conseq = $consequtive_hours<BR>");
            if( $consequtive_hours >= 3 ) {
#               print("consq 3 hours found at $$time{week}<BR>");
	       push(@consequtive_weekday, $$time{week});		###  發現連續三小時, 存入陣列
#              $ms[$i++]="嚴重錯誤: 大學部課程除實習、實驗課程之外，不可排連續3小時的課程!";
#              $ec++;
            }
          }else{
            $consequtive_hours = 1;
          }

          $last_week = $$time{week};
          $last_time = $$time{time};
        }          
#  print @consequtive_weekday;
  return(@consequtive_weekday);					###  將連續三小時的星期日子，傳回。
}
##############################################################################
sub Read_Immune_Record
{
  my(@line, $immune_file, %immune_status);
  my($course_id, $course_group, $r1, $r2, $r3, $r4);
  my $immune_file = $REFERENCE_PATH . "Open_Course_Restriction_Immune.txt";
  ($course_id, $course_group) = @_;
  
  open(IMMUNE, $immune_file);
  @line = <IMMUNE>;
  close(IMMUNE);
  $i = 0;
  foreach $line (@line) {
    ($c_id, $c_group, $r1, $r2, $r3, $r4) = split(/\t/, $line);
    if( ($course_id eq $c_id) and ($course_group eq $c_group) ) {
      $immune_status{r1} = $r1;
      $immune_status{r2} = $r2;
      $immune_status{r3} = $r3;
      $immune_status{r4} = $r4;
    }
  }
  return(%immune_status);
}
##########################################################################
sub Read_All_Immune_Record
{
  my(@files, @line, @immune_list, $immune_path, $immune_file, $i);
  my($course_id, $course_group, $r1, $r2, $r3, $r4);
  my $immune_file = $REFERENCE_PATH . "Open_Course_Restriction_Immune.txt";
  open(IMMUNE, $immune_file);
  @line = <IMMUNE>;
  close(IMMUNE);
  $i = 0;
  foreach $line (@line) {
    ($course_id, $course_group, $r1, $r2, $r3, $r4) = split(/\t/, $line);
    ${$immune_list[$i]}{course_id}      = $course_id;
    ${$immune_list[$i]}{course_group}   = $course_group;
    ${$immune_list[$i]}{r1}             = $r1;
    ${$immune_list[$i]}{r2}             = $r2;
    ${$immune_list[$i]}{r3}             = $r3;
    ${$immune_list[$i]}{r4}             = $r4;
    $i++;
  }
  return(@immune_list);
}
##############################################################################
sub Add_Immune_Record
{
  my($c_id, $c_group, $r1, $r2, $r3, $r4) = @_;
  my $immune_file = $REFERENCE_PATH . "Open_Course_Restriction_Immune.txt";
  my(@line);
  open(IMMUNE, $immune_file);
  @line = <IMMUNE>;
  close(IMMUNE);
  foreach $line (@line) {
    ($c_id_t, $c_group_t, @junk) = split(/\t/, $line);
    if( ($c_id eq $c_id_t) and ($c_group eq $c_group_t) ) {
      return(FALSE);
    }
  }
  open(IMMUNE, ">>$immune_file");
  print IMMUNE ("$c_id\t$c_group\t$r1\t$r2\t$r3\t$r4\n");
  close(IMMUNE);
  return(TRUE);
}
##############################################################################
sub Delete_Immune_Record
{
  my(@line, @list);
  my($c_id, $c_group) = @_;
  my $immune_file = $REFERENCE_PATH . "Open_Course_Restriction_Immune.txt";

  if( -e($immune_file) ) {
    open(IMMUNE, $immune_file);
    @line = <IMMUNE>;
    foreach $line (sort @line) {
      ($c_id_t, $c_group_t, @junk) = split(/\t/, $line);
      if( not( ($c_id eq $c_id_t) and ($c_group eq $c_group_t) ) ) {
        push(@list, $line);
      }
    }
    close(IMMUNE);
    open(IMMUNE, ">$immune_file");
    foreach $id (@list) {
      print IMMUNE ("$id");
    }
    close(IMMUNE);
    print("資料已刪除!<BR>");
  }
}
##############################################################################
sub Form_Open_Course_Restriction_Immune_Table
{
  my($table_content);
  @list = Read_All_Immune_Record();

  foreach $list (@list) {
#    $$list{course_id} =~ /^(....)/;
#    $dept = $1;
#    $dept =~ s/[123]$/4/;
#    $dept =~ s/5$/6/;
#    %course = Read_Course($dept, $$list{course_id},
#                          $$list{course_group}, "", "");
    $del_param = join("_", $$list{course_id}, $$list{course_group});
    $table_content .=
    qq(
      <TR>
        <TD><INPUT type=RADIO name=del_param value="$del_param"></TD>
        <TD>$$list{course_id}</TD>
        <TD>$$list{course_group}</TD>
        <TD>$$list{r1}</TD>
        <TD>$$list{r2}</TD>
        <TD>$$list{r3}</TD>
        <TD>$$list{r4}</TD>
      </TR>
    );
  }
  return($table_content);
}

############################################################################################
#####  刪除課程別名對應檔資料
#####  傳入：$new_id, $old_id, $dept
#####  傳回：$success_flag
#####  Updates: 2009/04/15  Nidalap :D~

sub Del_Course_Alias
{
  my($in_new_id, $in_old_id, $dept) = @_;
  my $alias_file, @line;
  my %dept_alias;

  %dept_alias = Read_Course_Alias();
#  print("deleting $in_new_id, $in_old_id<BR>\n");

  $alias_file = $REFERENCE_PATH . "course_alias.txt";
  open(ALIAS, ">$alias_file");
  foreach $old_id (keys %dept_alias) {
#    print("OLD: $in_old_id -> $old_id<BR>\n");
#    print("NEW: $in_new_id -> $dept_alias{$old_id}{'new_id'}<P>\n");
    if( ($in_old_id eq $old_id) and ($in_new_id eq $dept_alias{$old_id}{'new_id'}) )  {
#      print("MATCH! KILL!!<BR>\n");
    }else{
      print ALIAS ("$dept_alias{$old_id}{'dept'}\t$dept_alias{$old_id}{'new_id'}\t$old_id\n");      
    }
  }
  close(ALIAS);
  return(1, "已經刪除新課程 $in_new_id 和原課程 $in_old_id 的對應關係!");
}


############################################################################################
#####  新增課程別名對應檔資料
#####  傳入：$new_id, $old_id, $dept
#####  傳回：($success_flag, $reason)
#####  Updates: 2009/04/15  Nidalap :D~

sub Add_Course_Alias
{
  my($new_id, $old_id, $dept) = @_;
  my $alias_file, @line;
  my %dept_alias, %old_course;

  if( ( length($new_id) != 7 ) or ( length($old_id) != 7) )  {
    return(0, "請輸入正確的科目代碼!")
  }

  %dept_alias = Read_Course_Alias();
  %old_course = Read_Course($dept, $old_id, "01", "HISTORY");	###  如果原科目不存在，或是是別系所的課
  if( $old_course{cname} eq "" ) {
    return(0, "原課程 $old_id 不存在，或是非本系所所開設!");
  }

  if( exists($dept_alias{$old_id}{"new_id"}) )  {               ###  如果此筆資料早存在
    return(0, "此筆資料早已存在! 原課程 $old_id 已經存在對應新課程!");
  }
  
#  my $old_id_serial = $old_id;
#  $old_id_serial =~ s/^....//;					###  原課程代碼後三碼
#  my $new_id_serial = $new_id;
#  $new_id_serial =~ s/^....//;					###  新課程代碼後三碼  
#  if( $old_id_serial > $new_id_serial ) {
#    return(0, "原課程代碼流水號比新課程代碼流水號還要新！");
#  }
  $alias_file = $REFERENCE_PATH . "course_alias.txt";
  open(ALIAS, ">>$alias_file");
  print ALIAS ("$dept\t$new_id\t$old_id\n");
  close(ALIAS);
  return(1, "成功\建立新課程 $new_id 與原課程 $old_id 的對應關係!");
}

#############################################################################################
#####  讀取課程別名對應檔資料
#####  傳入：(無)
#####  傳回：%dept_alias
#####  Updates: 2009/04/15  Nidalap :D~
sub Read_Course_Alias
{
  my $alias_file, @line;
  my $dept, $old_id, $new_id;
  my %dept_alias;

  $alias_file = $REFERENCE_PATH . "course_alias.txt";
  open(ALIAS, $alias_file);
  @line = <ALIAS>;
  close(ALIAS);

  foreach $line (@line) {
    ($dept, $new_id, $old_id) = split(/\s+/, $line);
    $dept_alias{$old_id}{"dept"} = $dept;
    $dept_alias{$old_id}{"new_id"} = $new_id;
	
	#####  為了讓通識某課程可以雙向對應而加的違章建築  2014/12/22  Nidalap :D~
	#$dept_alias_inverse{$new_id}{"dept"} = $dept;			###  暫時不用，怕影響原有先修判斷！
    #$dept_alias_inverse{$new_id}{"old_id"} = $old_id;
    
#    print("\talias: $old_id -> $new_id of $dept\n");
  }
  return(%dept_alias)
}
#############################################################################################
#####  印出開課的 HTML header 以及上面的系所別/年級別等資訊
#####  輸入：\%Input, \%Dept
#####  輸出：相關的 html 碼
#####  Updates:
#####    199?/??/?? 原本散落在開課各網頁程式。
#####    2015/04/13 集中放置此處，且透過 $Input{'open_dept'} 判別是否為開設文學院課程需求醒目提示。
#####    2015/05/26 加入語言中心開設通識外文課提示功能。
sub Print_Open_Course_Header
{
  my(%Input) = %{$_[0]};
  my(%Dept) = %{$_[1]};
  my $title = $_[2];
  my $show_term;
  
  $dept_cname = $Dept{cname};
  $bgcolor = "#EEEEEE";
  
  #print "open_dept, dept_cd = " . $Input{'open_dept'} . ", " . $Input{'dept_cd'} . "<BR>\n";
  #print "lan, cge = $DEPT_LAN, $DEPT_CGE<BR>\n";
  #if($Input{'open_dept'} eq $DEPT_LAN) {  print "ccc"; }
  #if($Input{'dept_cd'} eq $DEPT_CGE) {  print "ddd"; }
  
  if( $Input{'open_dept'} ne $Input{'dept_cd'} ) {
    if( ($Input{'open_dept'} eq $DEPT_LAN) and ($Input{'dept_cd'} eq $DEPT_CGE) ) {
	  $dept_cname .= "<FONT color='YELLOW'>（開設通識外文課程）</FONT>";
#	  print "ccc";
	}elsif( substr($Input{dept_cd},3,1) == '4' ) {
	  $type = "學士班";
	  $dept_cname .= "<FONT color='YELLOW'>（開設文學院$type課程）</FONT>";
	}else{
	  #$type = "碩士班";
	  $type = "學士班";					#####  「語言所」切換身份仍是開設「文學院學士班」（非碩士班）課程  20150817
	  $dept_cname .= "<FONT color='YELLOW'>（開設文學院$type課程）</FONT>";
	}    
	$bgcolor = "RED";
  }
  
  if( $TERM <= 2 ) {
    $show_term = "第 " . $TERM . " 學期";
  }else{
    $show_term = "";						###  暑修
  }
  
  $html =  qq(
   <html>
     <head>
      $EXPIRE_META_TAG
      <title> $SUB_SYSTEM_NAME開排課系統 $title $su_flag</title>
     </head>
     <body background=$GRAPH_URL/ccu-sbg.jpg>
     <center>
      <br>
      <table border=0 width=40%>
       <tr>
        <td bgcolor=eeeeee>系別:</td><td bgcolor=$bgcolor> $dept_cname </td>
        <td bgcolor=eeeeee>年級:</td><td bgcolor=eeeeee> $Input{grade} </td></tr><tr>
        <th colspan=4>開排課系統 - $YEAR年度$show_term<FONT color=RED>$SUB_SYSTEM_NAME</FONT></th>
       </tr>
      </table>
     <br>
     <hr width=40%>
    <!--  <font size=3 color=brown>$title</font>  
     <br>
     <hr width=40%><br><br> -->
  );
  return $html;
}


#############################################################################################
#####  印出新增/修改開課頁面上的切換年級按鈕
#####  輸入：\%Input, \%Dept
#####  輸出：相關的 html 碼
#####  Updates:
#####    2015/05/26 從新增/修改/檢視/列印開課的程式中提取過來，並考慮語言中心開設通識外文課不可選擇年級。 by Nidalap :D~
sub Show_Switch_Grade_Buttons
{
  my $html, $grades;

  my(%Input)		= %{$_[0]};
  my $target_url	= $_[1];
  
  $html =  qq(
    <font size=4 color=brown>顯示此年級科目</font>
    <table border=0 width=30%> 
    <tr>
  );
  
#  print "[open, dept_cd] = [" . $Input{open_dept} . ", " . $Input{dept_cd} . "]<BR>\n";
#  print "is_under = " . is_Undergraduate_Dept($Input{open_dept}) . "<BR>\n";
#  Print_Hash(%Input);
  
  if( ($Input{open_dept} eq $DEPT_LAN) and ($Input{dept_cd} eq $DEPT_CGE) ) {
    @grades = (1);
  }elsif( is_Undergraduate_Dept($Input{open_dept}) > 0 ) {
    @grades = (1,2,3,4);
  }else{
    @grades = (1,2);
  }
  
  foreach $grade (@grades) {
    $grade_c = $GRADE[$grade];
	$html .= qq(
	  <th>
        <form action=$target_url method=post>
         <input type=hidden name=dept_cd value=$Input{dept_cd}>
         <input type=hidden name=grade value=$grade>
         <input type=hidden name=password value=$Input{password}>
		 <input type=hidden name=open_dept value=$Input{open_dept}>
         <input type=submit value=$grade_c>
        </form>
      </th>
	);
  }
  $html .= "</TABLE>";
  
  return $html;
}

