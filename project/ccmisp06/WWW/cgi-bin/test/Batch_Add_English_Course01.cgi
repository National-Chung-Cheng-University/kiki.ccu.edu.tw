#!/usr/local/bin/perl

print("Content-type:text/html\n\n");
print('<meta http-equiv="Content-Type" content="text/html; charset=big5">');
print("<CENTER><H1>新生通識英語課程批次載入</H1></CENTER><HR>\n");

#################################################################################
#####  已經解決的問題：
#####    * 支援系所的必修課	5/17(?)
#####  尚未解決的問題：
#####    * 必修時段只判斷到系，尚未到班  <- 看似沒必要了
#####    * 50/75分鐘課程衝堂判斷  <- done
#####    * 基礎/強化名單讀入功能尚未實做  <- done

require "../../../LIB/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Course.pm";
require $LIBRARY_PATH . "Student.pm";
require $LIBRARY_PATH . "Common_Utility.pm";
require $LIBRARY_PATH . "System_Settings.pm";
require $LIBRARY_PATH . "Error_Message.pm";

%Input=User_Input();

$script_name = $ENV{"SCRIPT_NAME"};
if( $Input{"debug"} == 1 ) {
  @show_debug_msg = (1, 1, 1, 1, 1);
  print("<A href='$script_name?debug=0'>隱藏所有偵錯訊息</A>\n");
}else{
  @show_debug_msg = (0, 0, 0, 0, 0);
  print("<A href='$script_name?debug=1'>顯示所有偵錯訊息</A>\n");
}

$number_limit	= 48;		###  每門課最多不超過此限修人數
#$number_limit	= 115;

@dept = Find_All_Dept();
Read_All_Student_Data();
#  @stu = Find_All_Student();
%eng_level_namelist = Read_English_Level();	###  讀取英檢分級檔

Find_All_Dept_Occupied_Time();			###  找出所有系所必修課時段
Read_All_Eng_Courses();				###  讀取所有英語課時段
%avail_class = Find_Dept_Available_Class();	###  所有系可以的課程班別
%ACS = Find_Student_Available_Class();		###  所有學生可以的課程班別

Dispatch_Class();				###  將學生一個一個塞入可以的時段的班別中
Display_Report();				###  顯示最後報表

#foreach $dept (sort {@{$avail_class{$a}} <=> @{$avail_class{$b}}} keys %avail_class) {
#  print $dept . "->";
#  foreach $class (@{$avail_class{$dept}}) {
#    print "$class ";
#  }
#  print "\n";
#}


################################################################################
sub Find_All_Dept_Occupied_Time
{
  my @course, $i, @extra_collide_time;
  
  foreach $level (keys %eng_level_namelist) {
    foreach $id (@{$eng_level_namelist{$level}}) {
#      print "$level - $id - $$S{$id}{name} \n";
      if( ($$S{$id}{dept} =~ /4$/) and ($$S{$id}{grade}==1) ) {
        $all_dept{$$S{$id}{dept}}++;
        push( @{$stu_in_dept{$level}{$$S{$id}{dept}}}, $id);
        $stu_count{$level}++;
      }
    }
  }

  foreach $dept (sort keys %all_dept) {
    $dept_count++;
#    print "$dept : $all_dept{$dept} 人 \n";
    @course = Find_All_Course($dept, 1, "", "");

    foreach $cour (@course) {
#      @extra_collide_time = ();                           ### 用來做 75<->50min 衝堂判斷

      %cou = Read_Course($dept, $$cour{id}, $$cour{group}, "", "", "");
#        print "check again element " . $$$cou{support_dept}[0] . "\n";
      next if( $cou{property} != 1 );                     ###  只考慮必修

      foreach $time (@{$cou{time}}) {
#        print("$dept - $$cou{id} _ $$cou{group} : $$time{week} - $$time{time}\n");
        @extra_collide_time = ();                           ### 用來做 75<->50min 衝堂判斷

        if( $time =~ /[A-Z]/ ) {			###  如果是 75 min 截次
          for($i=1; $i<=15; $i++) {
            if( is_Time_Collision(1, $$time{time}, 1, $i) ) {
              push(@extra_collide_time, $i);
            }
          }
        }

        $support_dept_count = @{$cou{support_dept}};
        if( $support_dept_count > 0 ) {				### 判斷支援系所情形
          foreach $support_dept ( @{$cou{support_dept}} ) {
            $dept_time{$support_dept}{$$time{week}}{$$time{time}} = 1;
            if( $time =~ /[A-Z]/ ) {
              foreach $t (@extra_collide_time) {
                $dept_time{$support_dept}{$$time{week}}{$t} = 1;
              }
            }
          }          
        }else{							### 本系課程
          $dept_time{$dept}{$$time{week}}{$$time{time}} = 1;
          if( $time =~ /[A-Z]/ ) {
            foreach $t (@extra_collide_time) {
              $dept_time{$dept}{$$time{week}}{$t} = 1;
            }
          }
        }            
      }              
    }                
  }
  
  foreach $dept (sort keys %dept_time) {
    %temp_dept = Read_Dept($dept);
    $all_dept_cname{$dept} = $temp_dept{cname2};
    foreach $week (sort keys %{$dept_time{$dept}}) {
      foreach $time (sort keys %{$dept_time{$dept}{$week}}) {
        $dept_time_count{$dept}++;
      }
    }
  }

  if($show_debug_msg[0]) {
    print("<HR><H2>各系所必修課時段為：</H2>");
    foreach $dept (sort keys %dept_time_count) {
      print("$dept($all_dept_cname{$dept}) : $dept_time_count{$dept} 個必修時段: ");
      foreach $week (sort keys %{$dept_time{$dept}}) {
        print " | $week-";
        foreach $time (sort keys %{$dept_time{$dept}{$week}}) {
          print "$time ";
        }
      }
      print("<BR>\n");
    }
  }
}

################################################################################
sub Read_All_Eng_Courses()
{
  my @eng_cou = ("7102111", "7102211", "7102121", "7102221");
  my $c, $i, $j, $level;
  foreach $eng_id (@eng_cou) {
    for($i=1; $i<15; $i++) {
      if( $i < 10 ) {	$j = "0" . $i;	}
      else	    {	$j = $i;	}
#      print("reading course $eng_id _ $j...\n");
      %c = Read_Course("I001", $eng_id, $j, "", "", "");
      next if( $c{ename} eq "" );
      $id_grp = $eng_id . "_" . $j;
      $level = Determine_Basic_Advanced($id_grp);

      if( $level eq "basic" ) {			### 基礎
        foreach $time (@{$c{time}}) {
          $time_eng{"basic"}{$id_grp}{$$time{week}}{$$time{time}} = 1;
        } 
#        $num_eng_basic{$id_grp}{time}    = $c{time};
      }else{					### 強化
	foreach $time (@{$c{time}}) {
	  $time_eng{"advanced"}{$id_grp}{$$time{week}}{$$time{time}} = 1;
	}
#        $num_eng_advanced{$id_grp}{time} = $c{time};
      }
#      print("number of $id_grp is $num_eng_basic{$id_grp}\n");      
    }
  }
  if( $show_debug_msg[1] ) {
    print("<HR><H2>所有英語課時段:</H2>");
    foreach $level (keys %time_eng) {
      foreach $group (sort keys %{$time_eng{$level}}) {
        print("等級 $level - $group : ");
        foreach $week (sort keys %{$time_eng{$level}{$group}} ) {
          print "$week-";
          foreach $time (sort keys %{$time_eng{$level}{$group}{$week}} ) {
            print "$time";
#            print "($time_eng{$level}{$group}{$week})";
            print ",";
          }
        }
        print "<BR>\n";
      }
    }
  }
}
################################################################################
sub Find_Dept_Available_Class
{
  my $free_flag, $i;
  my %avail_class;

  foreach $dept (sort { $dept_time_count{$b} <=> $dept_time_count{$a} } keys %dept_time) {
    %temp_dept = Read_Dept($dept);
#    print("$dept($temp_dept{cname2}) : ");
    ###  檢查每一個 basic 和 advanced 課程
    foreach $level (keys %time_eng) {
      $i = 0;
      foreach $group (sort keys %{$time_eng{$level}}) {
        $free_flag = 1;
        foreach $week (sort keys %{$dept_time{$dept}}) {
#          print "$week-";
          foreach $time (sort keys %{$dept_time{$dept}{$week}}) {
#            print "$time ";        
#            print(" checking $group $time_eng{$level}{$group}{$week}{$time}...\n");
            $free_flag = 0 if( $time_eng{$level}{$group}{$week}{$time} );
          }
        }
        if( $free_flag ) {
#          print("group $group is ok for dept $dept\n");
#          push(@{$avail_class{$dept}}, $group);
          $avail_class{$level}{$dept}[$i++] = $group;
          push(@temp, $group);
        }
      }
#      print("\n");
    }
  }
  if( $show_debug_msg[2] ) {
    print("<HR><H2>所有系所學生可選的課程:</H2>");
    foreach $level (keys %avail_class) {
      print("程度 $level - $group :<BR>");
      foreach $dept (sort 
                       {@{$avail_class{$level}{$a}} <=> @{$avail_class{$level}{$b}}} 
                     keys %{$avail_class{$level}}) {
        print "$dept($all_dept_cname{$dept}) ->";
        foreach $class (@{$avail_class{$level}{$dept}}) {
          print "[$class]";
        }
        print "<BR>\n";
      }
    }
  }

#  print "avail =  %avail_class\n";
#  print "temp = @temp\n";
  return %avail_class;
}
################################################################################
sub Find_Student_Available_Class
{
  my %ACS;			###  available class for student
  foreach $level ( keys %avail_class ) {
    foreach $dept ( keys %{$avail_class{$level}} ) {
      foreach $level (keys %stu_in_dept ) {
        foreach $stu (@{$stu_in_dept{$level}{$dept}}) {
          $ACS{$stu} = $avail_class{$level}{$dept};
#          print "ACS for $stu is: ";
          foreach $ac ( @{$avail_class{$level}{$dept}} ) {
#            print "$ac ";
          }
#          print "<BR>\n";
        }
      }
    }
  }
  return %ACS;
}
################################################################################
sub Dispatch_Class
{
  my $i;					### $i 用來跑課程輪替
  my $stu_count;
  
   foreach $stu (sort {rand(10) <=> rand(10)}  keys %ACS ) {
     $class_count = @{$avail_class{$dept}};
     $stu_count = @{$stu_in_dept{$dept}};
#     print "正在篩選 $temp_dept{cname2} $dept, $class_count 門課可選, $stu_count 人:\n";
    
     $i = Determine_Which_Class_to_Insert($stu);
    print("\t把 $stu 塞到 $ACS{$stu}[$i] 班($i)<BR> ")  if($show_debug_msg[3]);
      
     $temp_count = @{$course{$ACS{$stu}[$i]}};
     push( @{$course{$ACS{$stu}[$i]}}, $stu);		###  @course 是最後成果
     
     if( $i >= $class_count)  {  $i = 0  }  
  }

  foreach $class (sort keys %course) {
    $class_count++;
    $count = @{$course{$class}};
#    print("$class 班： $count 人<BR>\n")  if( $show_debug_msg[3] );
  }

}
################################################################################
sub Display_Report
{
  my $last_dept, $bgcolor, $i, $level, $exceed;
  my @bgcolor = ("LIGHTYELLOW", "LIGHTBLUE", "LIGHTGREEN");
  
#  $class_count = %course;
  print("<HR><H2>共 $stu_count{'basic'} 名基礎、 $stu_count{'advanced'} 名進階學生，批次選入 $class_count 門英語課程.</H2>\n");
  foreach $class (sort keys %course) {
    $exceed = "";
    $level = Determine_Basic_Advanced($class);
    $count = @{$course{$class}};
    if( $count > $number_limit ) {
      $exceed = "<FONT color=RED>超過！</FONT>";
    }
    print("$class 班($level)： $count 人 $exceed<BR>\n");
  }  
  
  print("<FORM action='Batch_Add_English_Course02.cgi' method=POST>");
  print("<HR><H2>以下是各班分派結果: </H2>\n");
  foreach $class(sort keys %course) {
    $count = @{$course{$class}};
    $level = Determine_Basic_Advanced($class);
    
    print("$class 班($level)： $count 人");
    print("<FONT color=RED>人數超過!!!</FONT>") if( $count > $number_limit );
    print("<BR>\n"); 
    print("<TABLE border=1>");
    foreach $stu (sort {$$S{$a}{dept} <=> $$S{$b}{dept}} @{$course{$class}}) {
      $i++ if( $last_dept ne $$S{$stu}{dept} );
      $bgcolor = $bgcolor[$i%3];
      $input_value = join("_", $class, $stu);
      print qq"
        <TR bgcolor=$bgcolor>
          <TD>$class</TD>
          <TD>$count 人</TD>
          <TD>$stu</TD>
          <TD>$all_dept_cname{$$S{$stu}{dept}}</TD>
        </TR>
        <INPUT type=hidden name=$input_value value=1>
      ";
      $last_dept = $$S{$stu}{dept};
    }
    print "</TABLE><HR>\n";
  }
  print qq(
      <INPUT type=submit value="執行批次選課">
    </FORM>  
  );

}
################################################################################
###  決定挑選哪一班塞入新學生 - 挑目前人數最少者
sub Determine_Which_Class_to_Insert
{
  my($stu) = @_;
  my $class_count = @{$ACS{$stu}};
  my $j=0, $k, $i;
  my $temp_count;
  my $this_count, $min_count = 999;
  
  for( $j=0; $j < $class_count; $j++ ) {
    $this_count = @{$course{$ACS{$stu}[$j]}};
    if( $this_count < $min_count ) {
      $i = $j;
      $min_count = $this_count;
    }
  }
  if( $min_count >= $number_limit ) {
#    print("Class exceeded number_limit for $dept!\n");
  }

#  print("Class exceeded number_limit for $dept!\n");
  
  return($i);
}
################################################################################
sub Read_English_Level
{
  my $file = $DATA_PATH . "Grade/english_level.txt";
  my @lines, $id, $cname, $level, %eng_level_namelist, $tmp_count;
  
  open(ENG, $file) or die("Cannot open file $file! bye!");
  @lines = <ENG>;
  close(ENG);
  foreach $line (@lines) {
    chomp($line);
    ($id, $cname, $level) = split(/\t/, $line);
    $stu_level{$id} = $level;
    if( $level == 1 ) {
      push( @{$eng_level_namelist{"basic"}}, $id);
    }elsif( $level == 2 ) {
      push( @{$eng_level_namelist{"advanced"}}, $id);
    }
  }
  
  if( $show_debug_msg[4] ) {
    print "<HR><H2>英語程度名單</H2>\n";
    foreach $lvl (keys %eng_level_namelist) {
      $tmp_count = @{$eng_level_namelist{$lvl}};
      print("$lvl(共 $tmp_count 個): ");
      foreach $id ( @{$eng_level_namelist{$lvl}} ) {
        print("$id, ");
      }
      print("<P>");
    }
  }
  return %eng_level_namelist;
}
##################################################################################
sub Determine_Basic_Advanced
{
  my($course_id) = @_;
  my $level;

  if( $course_id =~ /^7102.11/ ) {             ### 基礎
    $level = "basic";
  }else{
    $level = "advanced";
  }
  return $level;

}