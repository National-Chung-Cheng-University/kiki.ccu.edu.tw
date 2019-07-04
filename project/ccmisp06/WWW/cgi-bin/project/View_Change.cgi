#!/usr/local/bin/perl 
#########################################################################################
#####  View_Change.cgi
#####  課程異動一覽表
#####  2007/01/12 修改自 ~/WWW/cgi-bin/superuser/FindChange  Nidalap :D~
#####  2012/08/17 因應「語言中心可開設通識外語課程」功能，修改讀取科目/異動前科目列表功能  Nidalap :D~
#####  2015/01/23 「系所主管簽章」改為「單位主管簽章」  Nidalap :D~
#####  2015/08/11 引入 $open_dept 架構後，修正語言中心可開設通識外語課資料帶出問題 Nidalap :D~
#####  2016/02/02 修正語言中心開設通識課 old_course_dept_lan 的索引錯誤問題 Nidalap :D~
#####  2016/08/18 修正語言中心開設通識課 course_dept_lan 的索引錯誤問題 Nidalap :D~

require "../library/Reference.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Teacher.pm";
require $LIBRARY_PATH."Classroom.pm";

print("Content-type:text/html\n\n");
@Teachers= Read_Teacher_File();

my($count,$old_count,$i,$j,$flag);

%Input		= User_Input();
%dept		= Read_Dept($Input{dept_cd});			###  課開在哪個單位下
%open_dept	= Read_Dept($Input{open_dept});			###  實際執行開課的單位
%classrooms	= Read_All_Classroom();
$bg_alt = 0;
$fs	= "<FONT size=2>";

#foreach $k (keys %Input) {
#  print("$k -> $Input{$k}<BR>\n");
#} 

Write_HTML_File_Header();

 #####  讀取本系目前所有開課科目(@Course)，以及異動前所有開課科目(@Old_Course)
 #####  這裡有點複雜，主要是為了處理「語言中心可開設通識外語課程」功能。  2012/08/17 Nidalap :D~
 $i=0;
 if( $Input{'open_dept'} eq $DEPT_LAN ) {										#####  若是語言中心，額外抓取通識外語課程
   #print "dept_lan<BR>\n";
  
   @Course = Find_All_Course($DEPT_LAN ,"","");
   @Old_Course = Find_All_Course($DEPT_LAN ,"","change");
   @temp_course = Find_All_Course($DEPT_CGE,"","", "");
   @temp_old_course = Find_All_Course($DEPT_CGE,"","change", "");
   
   #####  語言中心的科目異動一覽表，包含了語中以及通識外語課，故需紀錄每一門課的開課單位。
   for($i=0; $i<@Course;$i++) {
     $course_dept_lan[$i] = $DEPT_LAN;
   }
   for($j=0; $j<=@Old_Course; $j++) {
     $old_course_dept_lan[$j] = $DEPT_LAN;
   }   
   
   #$i -= 1;
   $j -= 1;
   foreach $tc (@temp_course) {					###  檢查所有通識中心開的課程
     if( $$tc{id} =~ /^7102.../ ) {				###  如果科目代碼顯示是通識外語課
	   push(@Course, $tc);						###  就將該科目歸類進語言中心課程的一覽表內
	   $course_dept_lan[$i++] = $DEPT_CGE;		###  並紀錄開課單位為通識中心
	 }
   }
   foreach $tc (@temp_old_course) {
     if( $$tc{id} =~ /^7102.../ ) {
	   push(@Old_Course, $tc);
	   $old_course_dept_lan[$j++] = $DEPT_CGE;
	 }
   }
   
#   $i=0;
#   foreach $oc (@old_course_dept_lan) {
#     print("old: $i: $oc<BR>\n");
#	 $i++;
#   }
#   $i=0;
#   foreach $c (@course_dept_lan) {
#     print("new: $i: $c<BR>\n");
#	 $i++;
#   }

#   $i=0;
#   foreach $c (@Old_Course) {
#     print "old: " . $$c{id} . " " . $$c{group} . " " . $course_dept_lan[$i++] . "<BR>\n";
#   }  
#   $j=0;
#   foreach $c (@Course) {
#     print "cou: " . $$c{id} . " " . $$c{group} . " " . $course_dept_lan[$j++] . "<BR>\n";
#   }   
   
 }elsif( $Input{'open_dept'} eq $DEPT_CGE ) {									#####  若是通識中心，不要抓取通識外語課程
   #print "dept_cge<BR>\n";
 
   @temp_course = Find_All_Course($DEPT_CGE,"","");
   @temp_old_course = Find_All_Course($DEPT_CGE,"","change"); 
   foreach $tc (@temp_course) {
     push(@Course, $tc)  if( $$tc{id} !~ /^7102.../ );
   }
   foreach $tc (@temp_old_course) {
     push(@Old_Course, $tc)  if( $$tc{id} !~ /^7102.../ );
   }
 }else{																			#####  其他一般情況：直接讀取目前與異動前開課清單
   #print "dept other<BR>\n";   
   @Course = Find_All_Course($Input{'dept_cd'},"","", "", $Input{'open_dept'});
   @Old_Course = Find_All_Course($Input{'dept_cd'},"","change", "", $Input{'open_dept'});
 }
 #####  到此為止，已抓取 @Course 以及 @Old_Course
 $count=@Course;
 $old_count = @Old_Course;
 
#print "[count, old_count] = [$count, $old_count]<BR>\n";
 
######################################   檢查已取消的科目 ########################################
 for($i=0;$i < $old_count;$i++)
 {
   #####  若是語言中心登入且課程為通識外語，則使用 @old_course_dept_lan 紀錄的開課單位。其他情形 $dept2 = $Input{'dept_cd'}
   if( $Input{'open_dept'} eq $DEPT_LAN ) {
     $dept2 = $old_course_dept_lan[$i];
   }else{
     $dept2 = $Input{'dept_cd'};
   }
   
   #print "id = " . $Old_Course[$i]{id} . "<BR>\n";
   #if( $Old_Course[$i]{id} eq '1903981' ) {
   #  print "1903981 exists in old<BR>\n";
   #}
   
   for($j=0,$flag=0;$j < $count; $j++) {									###  $flag: [0,1] = [已取消, 仍存在]
     
	#if( $Course[$j]{id} eq '1903981' ) {
    # print "1903981 exists in new<BR>\n";
    #}
	 
	 if($Old_Course[$i]{id} eq $Course[$j]{id} && $Old_Course[$i]{group} eq $Course[$j]{group} )  { 
	   $flag=1;
	   break;
	 }
   }

#  print("searching $i $Old_Course[$i]{id} $Old_Course[$i]{group}<BR>\n");

  ######  科目已取消
  if( $flag == 0 )
  {
#   Log($dept,$Old_Course[$i]{id},$Old_Course[$i]{group},0);
#	print("read course($dept2, $Old_Course[$i]{id},$Old_Course[$i]{group}, 'change'<BR>\n");
    %log_course =Read_Course($dept2,$Old_Course[$i]{id},$Old_Course[$i]{group},"change");
#    Log2($dept,"C");
 
    my $teacher_string = Format_Teacher_String(@{$log_course{teacher}});
    my $time_string    = Format_Time_String($log_course{time});
    if( ($bg_alt++ % 2) == 0 ) {
      $bg_color = "#e0e0e0";
    }else{
      $bg_color = "#FFFFFF";
    }

   $content .=  qq(
     <TR bgcolor=$bg_color >
       <TD align=center>$fs$log_course{id}</TD>
       <TD align=center>$fs$log_course{group}</TD>
       <TD align=LEFT>$fs$log_course{cname}( $fs$log_course{ename} )</TD>
       <TD align=center>$fs$teacher_string</TD>
       <TD align=center>$fs$log_course{total_time}</TD>
       <TD align=center>$fs$log_course{credit}</TD>
       <TD align=center>$fs$PROPERTY_TABLE[$log_course{property}]</TD>
       <TD align=center>$fs$time_string</TD>
       <TD align=center>$fs$classrooms{$log_course{classroom}}{cname}</TD>
       <TD align=center>$fs取消</TD>
       <TD colspan=4></TD>
     </TR>
   );
  }
 }
 

 for($i=0;$i < $count;$i++)
 {
   ############################   註記 $flag 變數，[0,1] = [其他異動, 新增]   ###################################
   #####  若是語言中心登入且課程為通識外語，則使用 @course_dept_lan 紀錄的開課單位。其他情形 $dept2 = $Input{'dept_cd'}
   if( $Input{'open_dept'} eq $DEPT_LAN ) {
     $dept2 = $course_dept_lan[$i];
   }else{
     $dept2 = $Input{'dept_cd'};
   }
   
  for($j=0,$flag=0;$j < $old_count; $j++)  {
    if( $Course[$i]{id} eq $Old_Course[$j]{id} && $Course[$i]{group} eq $Old_Course[$j]{group} )  { 
       $flag=1; break;
    }
  }
  #print join(", ", $Course[$i]{id}, $Course[$i]{group}, $flag) . "<BR>\n";
  
  $j--;
  ######################################   檢查其他異動的科目 ########################################
  if($flag == 1)  ## 非新增之科目...檢查其他異動項目
  {
   %course= Read_Course( $dept2,$Course[$i]{id},$Course[$i]{group},"");
   %old_course = Read_Course($dept2,$Course[$i]{id},$Course[$i]{group},"change");
   %log_course = %old_course;
   $U_teacher="";
   $U_property="";
   $U_classtime="";
   $U_classroom="";
   my($check);
   $check=0;
   $check+=CheckPeriod();
   $check+=CheckClassroom();
   CheckTime();
   $check+=CheckProperty();
   $check+=CheckTeacher();

#   if( $course{id} eq "7102111" ) {
#     print("$course{id} _ $course{group} : check = $check<BR>\n");
#	 print("$course{cname} : $old_course{teacher}<BR>\n");
#   }
   
#   CheckSupport();
#   CheckBan();
#   CheckNote();
   #####  異動

#   print join(", ", $Course[$i]{id}, $Course[$i]{group}, $flag, $check) . "<BR>\n";
   if($check !=0)
   {
#    Log2($dept,"U",$U_teacher,$U_property,$U_classtime,$U_classroom);
   my $teacher_string = Format_Teacher_String(@{$course{teacher}});
   my $time_string    = Format_Time_String($course{time});
   my $old_teacher_string = Format_Teacher_String(@{$old_course{teacher}});
   my $old_time_string    = Format_Time_String($old_course{time});

   if( ($bg_alt++ % 2) == 0 ) {
     $bg_color = "#e0e0e0";
   }else{
     $bg_color = "#FFFFFF";
   }

     $content .=  qq(
       <TR bgcolor=$bg_color>
         <TD align=center>$fs$log_course{id}</TD>
         <TD align=center>$fs$log_course{group}</TD>
         <TD align=LEFT>$fs$log_course{cname}( $fs$log_course{ename} )</TD>
         <TD align=center>$fs$old_teacher_string</TD>
         <TD align=center>$fs$old_course{total_time}</TD>
         <TD align=center>$fs$course{credit}</TD>
         <TD align=center>$fs$PROPERTY_TABLE[$old_course{property}]</TD>
         <TD align=center>$fs$old_time_string</TD>
         <TD align=center>$fs$classrooms{$old_course{classroom}}{cname}</TD>
         <TD align=center>$fs</TD>
         <TD align=center>$fs$U_teacher</TD>
         <TD align=center>$fs$PROPERTY_TABLE[$U_property]</TD>
         <TD align=center>$fs$U_classtime</TD>
         <TD align=center>$fs$U_classroom</TD>
       </TR>
     );
   }
  }else{ 						 ######## 新增之科目
       ## 將新增科目記錄下來
#   Log($dept,$Course[$i]{id},$Course[$i]{group},1);
   
#   print join(" : ", $Course[$i]{id}, $Course[$i]{group}, "<BR>\n");   print "<HR>\n";

   %log_course=Read_Course($dept2,$Course[$i]{id},$Course[$i]{group});
#   Log2($dept,"A");
   my $teacher_string = Format_Teacher_String(@{$log_course{teacher}});
   my $time_string    = Format_Time_String($log_course{time});

   if( ($bg_alt++ % 2) == 0 ) {
     $bg_color = "#e0e0e0";
   }else{
     $bg_color = "#FFFFFF";
   }

     $content .=  qq(
       <TR bgcolor = $bg_color>
         <TD align=center>$fs$log_course{id}</TD>
         <TD align=center>$fs$log_course{group}</TD>
         <TD align=LEFT>$fs$log_course{cname}( $fs$log_course{ename} )</TD>
         <TD align=center>$fs$teacher_string</TD>
         <TD align=center>$fs$log_course{total_time}</TD>
         <TD align=center>$fs$log_course{credit}</TD>
         <TD align=center>$fs$PROPERTY_TABLE[$log_course{property}]</TD>
         <TD align=center>$fs$time_string</TD>
         <TD align=center>$fs$classrooms{$log_course{classroom}}{cname}</TD>
         <TD align=center>$fs新增</TD>
         <TD colspan=4></TD>
       </TR>
     );
  }
 }
#Write_HTML_File_Tail();
print $content;
Print_Footer();

#################################################################################

sub Write_HTML_File_Header()
{
#  $html_file_name = $WWW_PATH . "Update_Course.html";
#  open(HTML, ">$html_file_name") or die("Cannot open file >$html_file_name!\n");
  $content = qq(
    <HTML>
      <HEAD>
        $EXPIRE_META_TAG
        <TITLE>國立中正大學 $YEAR 學年度第  $TERM 學期 $SUB_SYSTEM_NAME  課程異動一覽表</TITLE>
      </HEAD>
      <BODY background="$GRAPH_URL/ccu-sbg.jpg">
        <CENTER><H1><FONT face="標楷體">國立中正大學 $YEAR 學年度第 $TERM 學期<FONT color=RED><U>$SUB_SYSTEM_NAME</U></FONT>課程異動一覽表</H1>
        <table width=95% border=0>
          <tr><th colspan=14 align=LEFT>系所別: $open_dept{cname}</th></tr>
          <TR><TD colspan=14><HR></TD></TR>
          <tr>
              <th bgcolor=#ffff00 colspan=9>$fs(原課程或新增課程資料)</font></th>
              <th bgcolor=orange colspan=7>$fs異  動  項  目</font></th>
          </tr>
          <tr>
              <th bgcolor=#ffff00>$fs編號</font></th>
              <th bgcolor=#ffff00>$fs班別</font></th>
              <th bgcolor=#ffff00>$fs科目名稱(英文譯名)</font></th>
              <th bgcolor=#ffff00 NOWRAP>$fs任課教師</font></th>
              <th bgcolor=#ffff00>$fs上課時數</font></th>
              <th bgcolor=#ffff00>$fs學分</font></th>
              <th bgcolor=#ffff00>$fs選必</font></th>
              <th bgcolor=#ffff00 NOWRAP>$fs上課時間</font></th>
              <th bgcolor=#ffff00>$fs上課地點</font></th>
              <th bgcolor=orange>$fs增|異|取消</font></th>
              <th bgcolor=orange NOWRAP>$fs任課教師</font></th>
              <th bgcolor=orange>$fs選/必</font></th>
              <th bgcolor=orange NOWRAP>$fs上課時間</font></th>
              <th bgcolor=orange>$fs上課地點</font></th>
          </tr>
  );
}
#################################################################################
sub Write_HTML_File_Tail() 
{
  $content = $content . "</TABLE>";
}

#################################################################################
sub Log
{
 my($dept,$id,$group,$flag);
 ($dept,$id,$group,$flag)=@_;
 open(LOG,">>Change.Log");
  print LOG "$dept $id $group $flag\n";
 close(LOG);
}
#################################################################################
sub CheckPeriod
{
 my($i,$j,$flag,$found);
 $flag =0;

 ## 如果時數改變則上課時間肯定改變
 if( $course{total_time} ne $old_course{total_time} )
 { $flag = 1; }

 
 for($i=0;$i<$course{total_time} && $flag!=1;$i++)
 {
  $found=0;
  for($j=0;$j<$course{total_time};$j++)
  {
   if( ($course{time}[$i]{week} eq $old_course{time}[$j]{week}) 
    && ($course{time}[$i]{time} eq $old_course{time}[$j]{time}) )
   { $found =1; }
  }
  
  ## $found==0 代表 $course{time}[$i]找不到相同的$old_course{time}[$j]
  if($found != 1)
  {
   $flag=1;
  # Log($dept,$course{id},$course{group},2);
  # return; 
  }
 }
 if( $flag == 1 )
 {
  Log($dept,$course{id},$course{group},2);
  for($i=0;$i<$course{total_time};$i++)
  {
   $U_classtime=$U_classtime.$WEEKDAY[$course{time}[$i]{week}];
   $U_classtime=$U_classtime.$course{time}[$i]{time};  
  }
  return 1;
 }
 return 0;
}
################################################################################
sub CheckClassroom
{
  my(%classroom);
  
#     if( $course{id} eq "4305017" ) {
#          print("$course{id} : $course{classroom} <-> $old_course{classroom}\n");
#     }
             
  if($course{classroom} ne $old_course{classroom})  { 
    Log($dept,$course{id},$course{group},3);
    %classroom = Read_Classroom($course{classroom});
    $U_classroom = $classroom{cname}; 
    return 1;
  }
  return 0;
}
################################################################################
sub CheckTime
{
  if( $course{total_time} ne $old_course{total_time}) {
    Log($dept,$course{id},$course{group},4); 
  }
}
################################################################################
sub CheckProperty
{
  if( $course{property} ne $old_course{property} )  {
    Log($dept,$course{id},$course{group},5);
    $U_property = $course{property};
    return 1;
  }
  return 0;
}
################################################################################
sub CheckTeacher
{
  my($i,$j,$count1,$count2,$flag,$found);
  $count1 = @{$course{teacher}};
  $count2 = @{$old_course{teacher}};
  if($count1 ne $count2) { 
    $flag =1;
  }
  for($i=0;$i<$count1 && $flag!=1;$i++)  {
    $found=0;
    for($j=0;$j<$count1;$j++)  {
      if($course{teacher}[$i] eq $old_course{teacher}[$j])  { 
        $found=1; break;
      }
    }
	
	
#	if( $course{id} eq "7102111" ) {
#      print $course{id} . "_" . $course{group} . "found = $found <BR>\n";
#    }
	
	
    if($found==0)  {
      $flag=1;
    }
  }
  if($flag==1)  {
    Log($dept,$course{id},$course{group},6);
    for($i=0;$i<$count1;$i++)  {
      $U_teacher=$U_teacher.$Teacher_Name{$course{teacher}[$i]}." ";
    }
    return 1;
  }
  return 0;
}
################################################################################
sub CheckSupport
{
  my($i,$j,$count1,$count2,$flag,$found);
  $count1 = $course{support_dept};
  $count2 = $old_course{support_dept};
  if($count1 ne $count2) {
    $flag =1;
  }
  for($i=0;$i<$count1 && $flag!=1;$i++)  {
    $found=0;
    for($j=0;$j<$count1;$j++)  {
      if($course{support_dept}[$i] eq $old_course{support_dept}[$j])  {
        $found=1; break;
      }
    }
    if($found==0)  {
      $flag=1;
    }
  }
  if($flag==1)  {
    Log($dept,$course{id},$course{group},7);
  }
}
################################################################################
sub CheckBan
{
  my($i,$j,$count1,$count2,$flag,$found);
  $count1 = $course{ban_dept};
  $count2 = $old_course{ban_dept};
  if($count1 ne $count2)  {
    $flag =1; 
  }
  for($i=0;$i<$count1 && $flag!=1;$i++) {
    $found=0;
    for($j=0;$j<$count1;$j++)  {
      if($course{ban_dept}[$i] eq $old_course{ban_dept}[$j]) {
        $found=1;
        break;
      }
    }
    if($found==0)  {
      $flag=1;
    }
  }
  if($flag==1)  {
    Log($dept,$course{id},$course{group},8);
  }
}
################################################################################
sub Log2
{
 my($dept,$flag,$teachers,$property,$classtime,$classroom,%classroom,$teacher_string);
 my($teacher_count,$i,@property_string,$output_string,@temp,$classtime_string);
 $property_string[0]="";
 $property_string[1]="必修";
 $property_string[2]="選修";
 $property_string[3]="通識";
 
 ($dept,$flag,$teachers,$property,$classtime,$classroom)=@_;
 %classroom = Read_Classroom( $log_course{classroom} );
# $teacher_string = Make_Teacher_String( @{$log_course{teacher}} );
 $teacher_count = @{$log_course{teacher}};
 for($i=0;$i<$teacher_count;$i++)
 {
#  print "log_course{teacher}[$i]=$log_course{teacher}[$i]\n";
  $teacher_string=$teacher_string.$Teacher_Name{$log_course{teacher}[$i]}." ";
 }
 
 for($i=0;$i<$log_course{total_time};$i++) {
   $classtime_string=$classtime_string.$WEEKDAY[$log_course{time}[$i]{week}];
   $classtime_string=$classtime_string.$log_course{time}[$i]{time};  
#   if( length($log_course{time}[$i]{time}) == 1) {
#     $classtime_string=$classtime_string." ";
#   }
 }
 open(LOG,">>Output");

 if( $IS_GRA ) {			###  專班的教師長度改為 200 bytes (2006/08/22)
   $output_string=sprintf("%2s%1s%4s%1sA%7s%2s%-60s%-200s%1s%1s%4s%-30s%-30s%1s%-200s%4s%-30s%-30s\n",
     $YEAR, $TERM, $dept,$log_course{grade},$log_course{id},$log_course{group},
     $log_course{cname},$teacher_string,$log_course{total_time},
     $log_course{credit},$property_string[$log_course{property}],
     $classtime_string,$classroom{cname},$flag,$teachers,
     $property_string[$property],$classtime,$classroom);
 }else{
   $output_string=sprintf("%2s%1s%4s%1sA%7s%2s%-60s%-100s%1s%1s%4s%-30s%-30s%1s%-100s%4s%-30s%-30s\n",
     $YEAR, $TERM, $dept,$log_course{grade},$log_course{id},$log_course{group},
     $log_course{cname},$teacher_string,$log_course{total_time},
     $log_course{credit},$property_string[$log_course{property}],
     $classtime_string,$classroom{cname},$flag,$teachers,
     $property_string[$property],$classtime,$classroom);
 }

 print LOG $output_string;
 close(LOG);

 open(LOG2,">>Output2");
 $output_string=sprintf("%s###%sA###%s###%s###%s###%s###%s###%s###%s###%s###%s###%s###%s###%s###%s###%s\n",
  $dept,$log_course{grade},$log_course{id},$log_course{group},
  $log_course{cname},$teacher_string,$log_course{total_time},
  $log_course{credit},$property_string[$log_course{property}],
  $classtime_string,$classroom{cname},$flag,$teachers,
  $property_string[$property],$classtime,$classroom);
  print LOG2 $output_string; 
 close(LOG2);

# if( $flag eq "C" ) {
#   %course = Read_Course($dept, $log_course{id}, $log_course{group}, "change","");
# }else{
   %course = Read_Course($dept, $log_course{id}, $log_course{group}, "", "");
# }

  %temp_old_course = Read_Course($dept, $log_course{id}, $log_course{group}, "change","");

 %dept = Read_Dept($dept);
 if($course{cname} eq "") {
   $course{cname} = $temp_old_course{cname};
 }
 %flag_meaning = ("C", "取消", "U", "異動", "A", "新開");
 print HTML qq(
   <TR><TD>$fs$dept{cname2}$log_course{grade}</TD>
       <TD>$fs$log_course{id}</TD>
       <TD>$fs$log_course{group}</TD>
       <TD>$fs$course{cname}</TD>
       <TD>$fs$teacher_string</TD>
       <TD>$fs$log_course{total_time}</TD>
       <TD>$fs$log_course{credit}</TD>
       <TD>$fs$property_string[$log_course{property}]</TD>
       <TD>$fs$classtime_string</TD>
       <TD>$fs$classroom{cname}</TD>
       <TD>$fs$flag_meaning{$flag}</TD>
       <TD>$fs$teachers&nbsp;</TD>
       <TD>$fs$property_string[$property]&nbsp;</TD>
       <TD>$fs$classtime&nbsp;</TD>
       <TD>$fs$classroom&nbsp;</TD>
    </TR>
 );
}
################################################################################
sub Make_Teacher_String
{
 my($string,$no,@teachers,$i);
 @teachers = @_;
 $no = @_;
 for($i=0;$i < $no; $i++)
 {
  print "teacher[$i]=$teacher[$i]\n";
  $string+=$Teacher_Name{$teachers[$i]};
  $string+=" ";
 }
 return $string;
}
################################################################################
sub Print_Footer
{
  $footer = qq(
      <TR>
        <TD colspan=14><HR></TD>
      </TR>
      <TR>
        <TD colspan=14>
          <FONT size=1>
          註:
          <BR>
            &nbsp&nbsp 1. 本異動表僅供「教師, 學分, 選必修, 上課時間」變更及「新增課程」用.
            <BR>
            &nbsp&nbsp 2. 學生係依本處上網公告 $YEAR$TERM 課程時間表選課, 請系所勿擅動上課時間, 以防衝堂.
            <BR>
            &nbsp&nbsp 3. 於<B>不妨礙選課同學衝堂下</B>, 上課時間得變更.
            <BR>
            &nbsp&nbsp 4. 依本校第 44 次教務會議決議: 「...課程異動截至日起至加退選截至日止, 不再受理任何課程異動, ...」,
               請各系所於規定期間內妥善安排課程.
            <BR>
          </OL>
        </TD>
      </TR>
      <TR>
        <TD colspan=14 align=RIGHT>
          &nbsp<P>
          單位主管簽章:______________________ &nbsp&nbsp&nbsp&nbsp 日期:______________________
        </TD>
      </TR>
    </TABLE>
  );
  print $footer;
}