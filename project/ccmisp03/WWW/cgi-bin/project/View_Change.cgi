#!/usr/local/bin/perl 
#########################################################################################
#####  View_Change.cgi
#####  �ҵ{���ʤ@����
#####  ���{���ק�� ~/WWW/cgi-bin/superuser/FindChange 
#####  Nidalap :D~  [2007/01/12]

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

%input= User_Input();
$dept = $input{dept_cd};
%dept = Read_Dept($dept);
%classrooms = Read_All_Classroom();
$bg_alt = 0;
$fs	= "<FONT size=2>";

#foreach $k (keys %input) {
#  print("$k -> $input{$k}<BR>\n");
#} 

Write_HTML_File_Header();

 @Course = Find_All_Course($dept,"","");
 @Old_Course = Find_All_Course($dept,"","old");
 $count=@Course;
 $old_count = @Old_Course;
 ## �ˬd canceled courses ##
 for($i=0;$i < $old_count;$i++)
 {
  for($j=0,$flag=0;$j < $count; $j++)
  {
   if($Old_Course[$i]{id} eq $Course[$j]{id}
   && $Old_Course[$i]{group} eq $Course[$j]{group} )
   { $flag=1; break; }
  }

#  print("searching $i $Old_Course[$i]{id} $Old_Course[$i]{group}<BR>\n");

  ######  ��ؤw����
  if( $flag == 0 )
  {
#   Log($dept,$Old_Course[$i]{id},$Old_Course[$i]{group},0);
   %log_course =Read_Course($dept,$Old_Course[$i]{id},$Old_Course[$i]{group},"old");
#   Log2($dept,"C");

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
       <TD align=center>$fs����</TD>
       <TD colspan=4></TD>
     </TR>
   );
  }
 }
 
 
 for($i=0;$i < $count;$i++)
 {
  ## �ˬd�O�_���s�W���
  for($j=0,$flag=0;$j < $old_count; $j++)
  {
   if( $Course[$i]{id} eq $Old_Course[$j]{id} 
    && $Course[$i]{group} eq $Old_Course[$j]{group} )
   { 
    $flag=1; break;
   }
  }
  $j--;
  if($flag == 1)  ## �D�s�W�����...�ˬd��L���ʶ���
  {
   %course= Read_Course( $dept,$Course[$i]{id},$Course[$i]{group},"");
   %old_course = Read_Course($dept,$Course[$i]{id},$Course[$i]{group},"old");
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

#   if( $course{id} eq "4305017" ) {
#     print("$course{id} : check = $check\n");
#   }
   
#   CheckSupport();
#   CheckBan();
#   CheckNote();
   #####  ����

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
  }
  else  ## �N���s�W�����
  {     ## �N�s�W��ذO���U��
#   Log($dept,$Course[$i]{id},$Course[$i]{group},1);
   %log_course=Read_Course($dept,$Course[$i]{id},$Course[$i]{group});
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
         <TD align=center>$fs�s�W</TD>
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
    <HTML><HEAD><TITLE>��ߤ����j�� $YEAR �Ǧ~�ײ�  $TERM �Ǵ� $SUB_SYSTEM_NAME  �ҵ{���ʤ@����</TITLE></HEAD>
      <BODY background="$GRAPH_URL/ccu-sbg.jpg">
        <CENTER><H1><FONT face="�з���">��ߤ����j�� $YEAR �Ǧ~�ײ� $TERM �Ǵ�<FONT color=RED><U>$SUB_SYSTEM_NAME</U></FONT>�ҵ{���ʤ@����</H1>
        <table width=95% border=0>
          <tr><th colspan=14 align=LEFT>�t�ҧO: $dept{cname}</th></tr>
          <TR><TD colspan=14><HR></TD></TR>
          <tr>
              <th bgcolor=#ffff00 colspan=9>$fs(��ҵ{�ηs�W�ҵ{���)</font></th>
              <th bgcolor=orange colspan=7>$fs��  ��  ��  ��</font></th>
          </tr>
          <tr>
              <th bgcolor=#ffff00>$fs�s��</font></th>
              <th bgcolor=#ffff00>$fs�Z�O</font></th>
              <th bgcolor=#ffff00>$fs��ئW��(�^��Ķ�W)</font></th>
              <th bgcolor=#ffff00 NOWRAP>$fs���ұЮv</font></th>
              <th bgcolor=#ffff00>$fs�W�Үɼ�</font></th>
              <th bgcolor=#ffff00>$fs�Ǥ�</font></th>
              <th bgcolor=#ffff00>$fs�沈</font></th>
              <th bgcolor=#ffff00 NOWRAP>$fs�W�Үɶ�</font></th>
              <th bgcolor=#ffff00>$fs�W�Ҧa�I</font></th>
              <th bgcolor=orange>$fs�W|��|����</font></th>
              <th bgcolor=orange NOWRAP>$fs���ұЮv</font></th>
              <th bgcolor=orange>$fs��/��</font></th>
              <th bgcolor=orange NOWRAP>$fs�W�Үɶ�</font></th>
              <th bgcolor=orange>$fs�W�Ҧa�I</font></th>
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

 ## �p�G�ɼƧ��ܫh�W�Үɶ��֩w����
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
  
  ## $found==0 �N�� $course{time}[$i]�䤣��ۦP��$old_course{time}[$j]
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
 $property_string[1]="����";
 $property_string[2]="���";
 $property_string[3]="�q��";
 
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

 if( $IS_GRA ) {			###  �M�Z���Юv���קאּ 200 bytes (2006/08/22)
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
#   %course = Read_Course($dept, $log_course{id}, $log_course{group}, "old","");
# }else{
   %course = Read_Course($dept, $log_course{id}, $log_course{group}, "", "");
# }

  %temp_old_course = Read_Course($dept, $log_course{id}, $log_course{group}, "old","");

 %dept = Read_Dept($dept);
 if($course{cname} eq "") {
   $course{cname} = $temp_old_course{cname};
 }
 %flag_meaning = ("C", "����", "U", "����", "A", "�s�}");
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
          ��:
          <BR>
            &nbsp&nbsp 1. �����ʪ�Ȩѡu�Юv, �Ǥ�, �沈��, �W�Үɶ��v�ܧ�Ρu�s�W�ҵ{�v��.
            <BR>
            &nbsp&nbsp 2. �ǥͫY�̥��B�W�����i $YEAR$TERM �ҵ{�ɶ�����, �Шt�ҤžհʤW�Үɶ�, �H���İ�.
            <BR>
            &nbsp&nbsp 3. ��<B>����ê��ҦP�ǽİ�U</B>, �W�Үɶ��o�ܧ�.
            <BR>
            &nbsp&nbsp 4. �̥��ղ� 44 ���аȷ|ĳ�Mĳ: �u...�ҵ{���ʺI�ܤ�_�ܥ[�h��I�ܤ��, ���A���z����ҵ{����, ...�v,
               �ЦU�t�ҩ�W�w�����������w�ƽҵ{.
            <BR>
          </OL>
        </TD>
      </TR>
      <TR>
        <TD colspan=14 align=RIGHT>
          &nbsp<P>
          �t�ҥD��ñ��:______________________ &nbsp&nbsp&nbsp&nbsp ���:______________________
        </TD>
      </TR>
    </TABLE>
  );
  print $footer;
}