#!/usr/local/bin/perl

#######################################################################################################
#####  Print_Course.cgi
#####  本學年學期擬開科目表
#####  顯示本學期某年級所有科目列表
#####  Updates:
#####   ...
#####   2009/05/20 新增(暑修的)第一類/第二類課程於備註一欄.  Nidalap :D~
#####   2010/03/19 加入 教師專長與授課科目是否符合 s_match 欄位  Nidalap :D~
#####   2010/04/08 體育中心和軍訓開課，不顯示 s_match 欄位  Nidalap :D~
#####   2010/05/18 若為通識中心，備註欄加上檔修系所  Nidalap :D~
#####   2010/05/25 s_match 出現與否，改為交給 Need_s_match() 判斷  Nidalap :D~
#####	2010/06/03 暑修/專班暑修不會顯示 "加退選時開放外系學生選修" 字眼  Nidalap :D~
#####   2010/10/11 語言中心可開通識外語課程功能 Nidalap :D~
#####   2012/05/09 加入開課學制 attr 欄位  Nidalap :D~
#####   2015/04/13 因應文學院需求-委由各系實際執行開課，新增 $open_dept 變數  Nidalap :D~
#####   2015/04/23 若某科目上課時間為空值，則以紅色底色醒目提示，並加上警訊  Nidalap :D~
#####   2015/05/26 切換年級按鈕改由 Show_Switch_Grade_Buttons() 處理 Nidalap :D~
#####   2016/11/29 新增「本單位與其他單位併班上課課程」表格 Nidalap :D~

require "../library/Reference.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Open_Course.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Teacher.pm";

%Input= User_Input();
#%Dept = Read_Dept($Input{open_dept});
%Dept = Read_Dept($Input{dept_cd});
@Dept = Find_All_Dept();
@teacher = Read_Teacher_File();
Read_Teacher_File();
%cge = Read_Cge();
%all_classroom = Read_All_Classroom();

@property = ("", "必修", "選修", "通識");

print("Content-type: text/html","\n\n");
Check_Dept_Password($Input{open_dept}, $Input{password});

#foreach $k (keys %Input) {
# print("$k ---> $Input{$k}<br>");
#}

if( $Input{open_dept} eq $DEPT_LAN ) {					### 語言中心可開通識外語課
  if( $Input{dept_cd} eq $DEPT_CGE ) {
    $cge_lan_flag = 2;									###  語言中心，且選擇了通識外語課
  }else{
    $cge_lan_flag = 1;							  		###  語言中心，尚未選擇通識外語課
  }  
}elsif( $Input{open_dept} eq $DEPT_CGE ) {				### 通識中心不可選通識外語課
  $cge_lan_flag = 3;
}

Print_Title();

Print_Course_Table();
Print_Combine_Course_Table();

$sign = "單位主管簽章: ________________________________";
if( $Input{dept_cd} != $Input{open_dept} ) {
  $sign .= "<P>文學院院長簽章： ________________________________";
}  
print "<P>&nbsp;<P>&nbsp;<P>&nbsp;$sign<P>&nbsp;";

Links3($Input{dept_cd} ,$Input{grade}, $Input{password}, $Input{open_dept});

############################################################################
sub Print_Title()
{
  if( $TERM == 3 ) {
    $show_term = "";
  }else{
    $show_term = join("", "第", $TERM, "學期");
  }

  $title = "<H2><FONT face='標楷體'>
            國立中正大學 <FONT color=RED>$SUB_SYSTEM_NAME</FONT>開排課系統<BR>
			$YEAR 學年度 $show_term 擬開科目列表
			</H2>
		   ";
  $title = "國立中正大學 $SUB_SYSTEM_NAME 開排課系統 $YEAR 學年度 $show_term 擬開科目列表";
			
  print Print_Open_Course_Header(\%Input, \%Dept, $title);									###  顯示上方系所年級等資訊
  print Show_Switch_Grade_Buttons(\%Input, "Print_Course.cgi");								###  顯示切換年級按鈕
  
}

##########################################################################
sub Print_Course_Table()
{
#  @course = Find_All_Course($Input{dept_cd}, $Input{grade}, "");

  #print "cge_lan_flag = $cge_lan_flag<BR>\n";
  
  if( $cge_lan_flag == 2 ) {  ### 語言中心可開通識外語課
        $Dept{id}         = $DEPT_CGE;
        $Input{grade} = 1;
        @temp_course = Find_All_Course($DEPT_CGE,1);
        foreach $tc (@temp_course) {
          push(@course, $tc)  if( $$tc{id} =~ /^7102.../ );
        }
  }elsif( $cge_lan_flag == 3 ) {        ###  通識中心不可開通識外語課
    @temp_course = Find_All_Course($Dept{id},$Input{grade},"");
    foreach $tc (@temp_course) {
      push(@course, $tc)  if( $$tc{id} !~ /^7102.../ );
    }
  }else{
    @course = Find_All_Course($Dept{id},$Input{grade}, "", "", $Input{open_dept});
  }

  local $course_count=0;
  $number_of_course = @course;

  #####  顯示「教師專長與授課科目是否符合」欄位
  if(  Need_s_match($Input{dept_cd}) ) {
    $s_match_head = "<th><font size=1>教師專長與授課科目是否符合</font></th>";
  }else{
    $s_match_head = "";
  }

  #####  顯示「開課學制」欄位(非專班的研究所)  2012/04/17  Nidalap :D~
  if( !$IS_GRA and !is_Undergraduate_Dept($Dept{id}) and !is_Exceptional_Dept($Dept{id}) ) {
    $show_attr = 1;
    $attr_head = "<th><font size=1>開課學制</font></th>";
  }else{ 
    $show_attr = 0;
    $attr_head = "";
  }

  print qq(
  本年級共有 $number_of_course 筆開課資料
  <table border=1>
    <tr bgcolor=YELLOW>
      <th><font size=1>編號</font></th>
      <th><font size=1>班別</font></th>
      <th><font size=1>年級</font></th>
      <th><font size=1>科目名稱</font></th>
      <th><font size=1>教師</font></th>
      <th><font size=1>時數<br>正課/實習實驗/書報討論</font></th>
      <th><font size=1>學分</font></th>
      <th><font size=1>選必</font></th>
      <th><font size=1>上課時間</font></th>
      <th><font size=1>教室</font></th>
      <th><font size=1>篩選原則</font></th>
      <th><font size=1>限修/保留</font></th>
      <th><font size=1>支援通識領域/支援通識人數</font></th>
      $s_match_head
      $attr_head
      <th><font size=1>備註</font></th>
    </tr>
  );

  $need_modify = 0;			###  （因批次開課）尚須修正之科目數
  foreach $course (@course) {
    %course = Read_Course($Dept{id}, $$course{id}, $$course{group}, "");
    %classroom = Read_Classroom($course{classroom});
    $time_string = Format_Time_String($course{time});
    $note_string = Format_Note();
    $is_dept_serv = 0;
    $is_dept_serv = 1  if( $$course{id} eq Get_Dept_Serv_Course_ID($Input{dept_cd}));

    if(  Need_s_match($Input{dept_cd}) ) {
      $s_match_table = "<td align=center><font size=1>" . $S_MATCH{$course{s_match}} . "</font></td>";
    }else{
      $s_match_table = "";
    }

    if($course_count % 5 == 4) {
       $bgcolor = "#f0f0f0";
    }elsif( $is_dept_serv ) {
       $bgcolor = "LIGHTGREEN";
    }else{
       $bgcolor = "";
    }
	if( $time_string eq "" ) {
	  $bgcolor = "RED";
	  $need_modify++;
	}
	
	print "<TR bgcolor='$bgcolor'>";
    print qq(
        <td align=center><font size=1> $$course{id} </font></td>
        <td align=center><font size=1> $$course{group} </font></td>
        <td align=center><font size=1> $course{grade} </font></td>
    );
    $note_dis = $note_eng = "";
    $note_dis = "<BR><FONT color=RED>(此科目為遠距教學課程)" if( $course{distant_learning} == 1 );
    $note_eng = "<BR><FONT color=RED>(此科目為全英語授課)"   if( $course{english_teaching} == 1 );
    print qq(
        <td align=left><font size=1> $course{cname}<br>
        $course{ename} $note_dis $note_eng</font></td>
        <td align=center>
    );
    $i=0;
    while( $course{teacher}[$i] ne "" ) {
       print qq(<font size=1>$Teacher_Name{$course{teacher}[$i]}</font>);
       print (", ")  if($course{teacher}[$i+1] ne "");
       $i++;
    }
#    if($course{teacher}[0] eq "99999") {
#       print qq(<font size=1>教師未定</font>);
#    }

  #####  顯示「開課學制」欄位(非專班的研究所)  2012/04/17  Nidalap :D~    
  if( $show_attr == 1 ) {
    $attr_table = "<td align=center><font size=1>" . $ATTR{$course{attr}} . "</font></td>";
  }else{
    $attr_table = "";
  }

    
    print qq(
        </td>
        <td align=center><font size=1> $course{total_time}<br>$course{lab_time1}/$course{lab_time2}/$course{lab_time3} </font></td>
        <td align=center><font size=1> $course{credit} </font></td>
        <td align=center><font size=1> $property[$course{property}] </font></td>
        <td align=center><font size=1> $time_string</font></td>
        <td align=center><font size=1> $classroom{cname} </font></td>
        <td align=center><font size=1> $PRINCIPLE[$course{principle}] </font></td>
        <td align=center><font size=1> $course{number_limit} / $course{reserved_number} </font></td>
        <td align=center><font size=1> $cge{$course{support_cge_type}}{sub_cge_id_show} $cge{$course{support_cge_type}}{cge_name} / $course{support_cge_number} </font></td>
        $s_match_table
        $attr_table
        <td align=left><font size=1> $note_string </font></td>
      </tr>
    );
    $course_count++;
  }

  if( $need_modify > 0 ) {
    $need_modify_text = "本學期部份開課資料尚未齊全，請補齊以上紅色底色之課程資料！";
  }
  
  print qq(
     </table>
     <P>&nbsp<P>
     <CENTER>
	   <B><FONT color="RED">$need_modify_text</FONT></B>
	   <P>
     <P>
  );

  
  
  #####  如果尚未開設學系服務學習課程，顯示警示訊息
  $dept_serv_course_id = Get_Dept_Serv_Course_ID($Dept{id});
  %serv_course = Read_Course($Dept{id}, $dept_serv_course_id, "01"); 
#  if( (not is_Exceptional_Dept($Dept{id})) and $serv_course{ename} eq "" ) {
  if(      not is_Summer() 
       and (is_Undergraduate_Dept($Dept{id})==1) 
       and (not is_Exceptional_Dept($dept{id})) and ($serv_course{ename} eq "") ) { 
    print "<FONT color=RED>本學期尚未開設學系服務學習課程！</FONT> ";
  }


}
#########################################################################
sub Format_Note()
{
  my $note_string = "";
  my($temp_dept);
  my(@grade) = ("", "一年級", "二年級", "三年級", "四年級");   

#  if( $course{number_limit} != 0 ) {
#    $note_string .= "限修$course{number_limit}人; ";
#  }
#  if ( $course{reserved_number} != 0 ) {
#    $note_string .= "保留$course{reserved_number}人; ";
#  }
  if( ${$course{support_dept}}[0] ne "" ) {
    $note_string .= "<b>支援</b>";
    foreach $dept (@{$course{support_dept}}) {
      %temp_dept = Read_Dept($dept);
      $note_string .= $temp_dept{cname2};
    }   
    foreach $grade (@{$course{support_grade}}) {
      $note_string .= $grade[$grade];
    }
    foreach $class (@{$course{support_class}}) {
      $note_string .= $class;
      $note_string .= "班";
    }
    $note_string .= "; ";
  }
 
  if( $course{dept} eq $DEPT_CGE ) {					###  若通識，顯示擋修系所  Added 2010/05/18 Nidalap :D~
    if( ${$course{ban_dept}}[0] ne "" ) {
      $note_string .= "<b>擋修</b>";
      foreach $dept (@{$course{ban_dept}}) {
        %temp_dept = Read_Dept($dept);
        $note_string .= $temp_dept{cname2};
      }
      foreach $grade (@{$course{ban_grade}}) {
        $note_string .= $grade[$grade];
      }
      foreach $class (@{$course{ban_class}}) {
        $note_string .= $class;
        $note_string .= "班";
      }
      $note_string .= "; ";
    }
  }  

  #####  如果是學系服務學習課程，依照學期顯示不同訊息
  $dept_serv_course_id = Get_Dept_Serv_Course_ID($Dept{id});
  if( $dept_serv_course_id eq $course{id} ) {
    if( $TERM == 1 ) {
      $temp = "單號";
    }else{
      $temp = "雙號";
    }
    $note_string .= "限本系一年級" . $temp . "學生修讀;";
  }
        
  if( ${$course{ban_dept}}[10] ne "" ) {
    $note_string .= "限本系生修;"  if($course{dept} ne $DEPT_CGE);		###  2009/12/08 排除通識
    if( not is_Summer() ) {							###  暑修不顯示以下字眼 2010/06/03 Nidalap :D~
      if( ($course{number_limit} > 0)and($course{dept} ne $DEPT_CGE) ) {  
        ### 非通識開課若限本系且限人數, 顯示+20%訊息
        ### 字眼改成 "加退選時開放外系學生選修" (2002/12/02)
        $note_string .= "於加退選期間開放外系學生選修;";
      }
    }
  }
######  先修科目
#$note_string .= "${${$course{prerequisite_course}}[0]}{dept} - ${${$course{prerequisite_course}}[0]}{id} - ${${$course{prerequisite_course}}[0]}{grade}<BR>\n";
#if( (${${$course{prerequisite_course}}[0]}{dept} ne "")and( ${${$course{prerequisite_course}}[0]}{dept} ne "99999") ) {
  if( (${${$course{prerequisite_course}}[0]}{dept} ne "99999") and (${${$course{prerequisite_course}}[0]}{dept} ne "") ) {
      $note_string .= "<b>先修科目</b>";
      foreach $pre_course (@{$course{prerequisite_course}}) {
        %pre_course = Read_Course( $$pre_course{dept}, $$pre_course{id}, "01" ,"history");
        $note_string = $note_string . "(" . $$pre_course{id} . ")" . $pre_course{cname} . "(" . $GRADE{$$pre_course{grade}} . ")" . " ";
      }
	  $course{prerequisite_logic} = "AND"  if( $course{prerequisite_logic} eq "" );
      $note_string .= "($PREREQUISITE_LOGIC{$course{prerequisite_logic}})"  if($course{prerequisite_logic});
  }

#####  (暑修的)第一類/第二類課程  Added 2009/05/20 Nidalap :D~
  if( is_Summer() and !is_GRA() ) {       ### 只作用於「一般生暑修」
    @flag_remedy = ("", 
        "第一類課程：經系（所、中心）課程委員會議審議通過之選修課程",
        "第二類課程：曾開授之課程，以補救教學為原則");
    $note_string .= $flag_remedy[$course{remedy}];
  }

#  if( ${$course{ban_dept}}[0] ne "" ) {
#    $note_string .= "<b>擋修</b>";
#    foreach $dept (@{$course{ban_dept}}) {
#      %temp_dept = Read_Dept($dept);
#      $note_string = $note_string . $temp_dept{cname2} . " ";
#    }
#    foreach $grade (@{$course{ban_grade}}) {
#      $note_string .= $grade[$grade];
#    }
#    foreach $class (@{$course{ban_class}}) {
#      $note_string .= $class;
#      $note_string .= "班";
#    }
#    $note_string .= "; ";
#  }
  $note_string .= $course{note};
  $note_string = "無"  if( $note_string eq "" );
  return $note_string;
}
##########################################################################################################
sub Print_Combine_Course_Table
{
  print qq(
    <P>
    本單位與其他單位併班上課課程（教師上課時間相同）如下：
    <table border=1>
      <tr bgcolor=YELLOW>
        <th><font size=1>  </font></th>
        <th><font size=1>系所名稱</font></th>
        <th><font size=1>科目編碼</font></th>
        <th><font size=1>班別</font></th>
        <th><font size=1>科目名稱</font></th>
        <th><font size=1>授課教師</font></th>
        <th><font size=1>上課時間</font></th>
        <th><font size=1>教室</font></th>
        <th><font size=1>學分</font></th>
    </tr>
  );
  $i=0;
  foreach $course (@course) {
    %course = Read_Course($Dept{id}, $$course{id}, $$course{group}, "");
    %classroom = Read_Classroom($course{classroom});
    $time_string = Format_Time_String($course{time});
    $teacher_string = Format_Teacher_String(@{$course{teacher}});
#    $note_string = Format_Note();  
    next if($teacher_string eq "");

    if( $i++%2 == 0 ) {
      $bgcolor = "#f0f0f0";
    }else{
      $bgcolor = "#FFFFFF";
    }
    $i++;
    
    foreach $teacher (@{$course{teacher}}) {
      #print $$course{id} . "-" . $$course{group} . "-" . $teacher . "<BR>";
      next if( $teacher eq "99999" );
      next if( $teacher eq "" );
      foreach $other_dept (@Dept) {
        next if($other_dept eq $Dept{id});
        %other_Dept = Read_Dept($other_dept);
        @other_course = Find_All_Course($other_dept);
        foreach $other_course (@other_course) {
          %other_course = Read_Course($other_dept, $$other_course{id}, $$other_course{group}, "");
          $other_time_string = Format_Time_String($other_course{time});
          $other_teacher_string = Format_Teacher_String(@{$other_course{teacher}});
          
          if( $time_string eq $other_time_string ) {
            foreach $other_teacher (@{$other_course{teacher}}) {
            
              if( $teacher eq $other_teacher ) {
                print qq(
                  <TR bgcolor='$bgcolor'>
                    <TD>本單位課程</TD>
                    <TD>$Dept{cname2}</TD>
                    <TD>$course{id}</TD>
                    <TD>$course{group}</TD>
                    <TD>$course{cname}</TD>
                    <TD>$teacher_string</TD>
                    <TD>$time_string</TD>
                    <TD>$all_classroom{$course{classroom}}{'name'}</TD>
                    <TD>$course{credit}</TD>
                  </TR>
                
                  <TR bgcolor='$bgcolor'>
                    <TD>其他單位課程</TD>
                    <TD>$other_Dept{cname2}</TD>
                    <TD>$other_course{id}</TD>
                    <TD>$other_course{group}</TD>
                    <TD>$other_course{cname}</TD>
                    <TD>$other_teacher_string</TD>
                    <TD>$other_time_string</TD>
                    <TD>$all_classroom{$other_course{classroom}}{'name'}</TD>
                    <TD>$other_course{credit}</TD>
                  </TR>
                );
              }
            }
          }
        }
      }
      
    }
  }
  print "</TABLE>";
}
