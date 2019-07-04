#!/usr/local/bin/perl

print("Content-type:text/html\n\n");
print('<meta http-equiv="Content-Type" content="text/html; charset=big5">');
print("<CENTER><H1>�s�ͳq�ѭ^�y�ҵ{�妸���J</H1></CENTER><HR>\n");

#################################################################################
#####  �w�g�ѨM�����D�G
#####    * �䴩�t�Ҫ����׽�	5/17(?)
#####  �|���ѨM�����D�G
#####    * ���׮ɬq�u�P�_��t�A�|����Z  <- �ݦ��S���n�F
#####    * 50/75�����ҵ{�İ�P�_  <- done
#####    * ��¦/�j�ƦW��Ū�J�\��|���갵  <- done

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
  print("<A href='$script_name?debug=0'>���éҦ������T��</A>\n");
}else{
  @show_debug_msg = (0, 0, 0, 0, 0);
  print("<A href='$script_name?debug=1'>��ܩҦ������T��</A>\n");
}

$number_limit	= 48;		###  �C���ҳ̦h���W�L�����פH��
#$number_limit	= 115;

@dept = Find_All_Dept();
Read_All_Student_Data();
#  @stu = Find_All_Student();
%eng_level_namelist = Read_English_Level();	###  Ū���^�ˤ�����

Find_All_Dept_Occupied_Time();			###  ��X�Ҧ��t�ҥ��׽Үɬq
Read_All_Eng_Courses();				###  Ū���Ҧ��^�y�Үɬq
%avail_class = Find_Dept_Available_Class();	###  �Ҧ��t�i�H���ҵ{�Z�O
%ACS = Find_Student_Available_Class();		###  �Ҧ��ǥͥi�H���ҵ{�Z�O

Dispatch_Class();				###  �N�ǥͤ@�Ӥ@�Ӷ�J�i�H���ɬq���Z�O��
Display_Report();				###  ��̫ܳ����

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
#    print "$dept : $all_dept{$dept} �H \n";
    @course = Find_All_Course($dept, 1, "", "");

    foreach $cour (@course) {
#      @extra_collide_time = ();                           ### �ΨӰ� 75<->50min �İ�P�_

      %cou = Read_Course($dept, $$cour{id}, $$cour{group}, "", "", "");
#        print "check again element " . $$$cou{support_dept}[0] . "\n";
      next if( $cou{property} != 1 );                     ###  �u�Ҽ{����

      foreach $time (@{$cou{time}}) {
#        print("$dept - $$cou{id} _ $$cou{group} : $$time{week} - $$time{time}\n");
        @extra_collide_time = ();                           ### �ΨӰ� 75<->50min �İ�P�_

        if( $time =~ /[A-Z]/ ) {			###  �p�G�O 75 min �I��
          for($i=1; $i<=15; $i++) {
            if( is_Time_Collision(1, $$time{time}, 1, $i) ) {
              push(@extra_collide_time, $i);
            }
          }
        }

        $support_dept_count = @{$cou{support_dept}};
        if( $support_dept_count > 0 ) {				### �P�_�䴩�t�ұ���
          foreach $support_dept ( @{$cou{support_dept}} ) {
            $dept_time{$support_dept}{$$time{week}}{$$time{time}} = 1;
            if( $time =~ /[A-Z]/ ) {
              foreach $t (@extra_collide_time) {
                $dept_time{$support_dept}{$$time{week}}{$t} = 1;
              }
            }
          }          
        }else{							### ���t�ҵ{
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
    print("<HR><H2>�U�t�ҥ��׽Үɬq���G</H2>");
    foreach $dept (sort keys %dept_time_count) {
      print("$dept($all_dept_cname{$dept}) : $dept_time_count{$dept} �ӥ��׮ɬq: ");
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

      if( $level eq "basic" ) {			### ��¦
        foreach $time (@{$c{time}}) {
          $time_eng{"basic"}{$id_grp}{$$time{week}}{$$time{time}} = 1;
        } 
#        $num_eng_basic{$id_grp}{time}    = $c{time};
      }else{					### �j��
	foreach $time (@{$c{time}}) {
	  $time_eng{"advanced"}{$id_grp}{$$time{week}}{$$time{time}} = 1;
	}
#        $num_eng_advanced{$id_grp}{time} = $c{time};
      }
#      print("number of $id_grp is $num_eng_basic{$id_grp}\n");      
    }
  }
  if( $show_debug_msg[1] ) {
    print("<HR><H2>�Ҧ��^�y�Үɬq:</H2>");
    foreach $level (keys %time_eng) {
      foreach $group (sort keys %{$time_eng{$level}}) {
        print("���� $level - $group : ");
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
    ###  �ˬd�C�@�� basic �M advanced �ҵ{
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
    print("<HR><H2>�Ҧ��t�Ҿǥͥi�諸�ҵ{:</H2>");
    foreach $level (keys %avail_class) {
      print("�{�� $level - $group :<BR>");
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
  my $i;					### $i �ΨӶ]�ҵ{����
  my $stu_count;
  
   foreach $stu (sort {rand(10) <=> rand(10)}  keys %ACS ) {
     $class_count = @{$avail_class{$dept}};
     $stu_count = @{$stu_in_dept{$dept}};
#     print "���b�z�� $temp_dept{cname2} $dept, $class_count ���ҥi��, $stu_count �H:\n";
    
     $i = Determine_Which_Class_to_Insert($stu);
    print("\t�� $stu ��� $ACS{$stu}[$i] �Z($i)<BR> ")  if($show_debug_msg[3]);
      
     $temp_count = @{$course{$ACS{$stu}[$i]}};
     push( @{$course{$ACS{$stu}[$i]}}, $stu);		###  @course �O�̫ᦨ�G
     
     if( $i >= $class_count)  {  $i = 0  }  
  }

  foreach $class (sort keys %course) {
    $class_count++;
    $count = @{$course{$class}};
#    print("$class �Z�G $count �H<BR>\n")  if( $show_debug_msg[3] );
  }

}
################################################################################
sub Display_Report
{
  my $last_dept, $bgcolor, $i, $level, $exceed;
  my @bgcolor = ("LIGHTYELLOW", "LIGHTBLUE", "LIGHTGREEN");
  
#  $class_count = %course;
  print("<HR><H2>�@ $stu_count{'basic'} �W��¦�B $stu_count{'advanced'} �W�i���ǥ͡A�妸��J $class_count ���^�y�ҵ{.</H2>\n");
  foreach $class (sort keys %course) {
    $exceed = "";
    $level = Determine_Basic_Advanced($class);
    $count = @{$course{$class}};
    if( $count > $number_limit ) {
      $exceed = "<FONT color=RED>�W�L�I</FONT>";
    }
    print("$class �Z($level)�G $count �H $exceed<BR>\n");
  }  
  
  print("<FORM action='Batch_Add_English_Course02.cgi' method=POST>");
  print("<HR><H2>�H�U�O�U�Z�������G: </H2>\n");
  foreach $class(sort keys %course) {
    $count = @{$course{$class}};
    $level = Determine_Basic_Advanced($class);
    
    print("$class �Z($level)�G $count �H");
    print("<FONT color=RED>�H�ƶW�L!!!</FONT>") if( $count > $number_limit );
    print("<BR>\n"); 
    print("<TABLE border=1>");
    foreach $stu (sort {$$S{$a}{dept} <=> $$S{$b}{dept}} @{$course{$class}}) {
      $i++ if( $last_dept ne $$S{$stu}{dept} );
      $bgcolor = $bgcolor[$i%3];
      $input_value = join("_", $class, $stu);
      print qq"
        <TR bgcolor=$bgcolor>
          <TD>$class</TD>
          <TD>$count �H</TD>
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
      <INPUT type=submit value="����妸���">
    </FORM>  
  );

}
################################################################################
###  �M�w�D����@�Z��J�s�ǥ� - �D�ثe�H�Ƴ̤֪�
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
    print "<HR><H2>�^�y�{�צW��</H2>\n";
    foreach $lvl (keys %eng_level_namelist) {
      $tmp_count = @{$eng_level_namelist{$lvl}};
      print("$lvl(�@ $tmp_count ��): ");
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

  if( $course_id =~ /^7102.11/ ) {             ### ��¦
    $level = "basic";
  }else{
    $level = "advanced";
  }
  return $level;

}