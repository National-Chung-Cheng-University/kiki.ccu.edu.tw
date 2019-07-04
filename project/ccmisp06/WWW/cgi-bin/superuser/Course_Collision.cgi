#!/usr/local/bin/perl
###############################################################################
#####  Course_Collision.cgi
#####  教室與教師衝堂檢核（開課期間可使用，用以在開課結束前提早找到問題）
#####  Updates:
#####    2015/12/07 Created by Nidalap :D~
#####    2016/05/06 教室衝堂部分，排除教授研究室（代碼為 0） by Nidalap :D~
###############################################################################

require "../../../LIB/Reference.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Course.pm";
require $LIBRARY_PATH . "Teacher.pm";
require $LIBRARY_PATH . "Classroom.pm";
require $LIBRARY_PATH . "Common_Utility.pm";
require $LIBRARY_PATH . "System_Settings.pm";

HTML_Head("教室與教師衝堂檢核");

Read_Teacher_File();
%classroom = Read_All_Classroom();

@dept = Find_All_Dept();
@teacher_conflict = ();
foreach $dept (@dept) {
  @course = Find_All_Course($dept);
  foreach $course (@course) {
    #print "$$course{'id'} - $$course{'group'} <BR>\n";
	%cour = Read_Course($dept, $$course{'id'}, $$course{'group'});
	#@time = $cour{"time"};
	foreach $time (@{$cour{"time"}}) {
	  #print "time = $time";
	  foreach $teacher (@{$cour{"teacher"}}) {
	    next if $teacher eq "99999";
	    if( defined($teacher_time{$teacher}{$$time{'week'}}{$$time{'time'}}) ) {			###  若此教師此時段已經註冊
																							###  建立教師衝堂資料結構 %teacher_conflict
		  #$teacher_conflict{$teacher}{$$time{"week"}}{$$time{"time"}}[0]{"cid"} 
			#	= $teacher_time{$teacher}{$$time{'week'}}{$$time{'time'}}{"course"}{"cid"};
		  #$teacher_conflict{$teacher}{$$time{"week"}}{$$time{"time"}}[0]{"group"} 
			#	= $teacher_time{$teacher}{$$time{'week'}}{$$time{'time'}}{"course"}{"group"};
		  #$i = @teacher_conflict + 1;
		  #$teacher_conflict{$teacher}{$$time{'week'}}{$$time{'time'}}[$i]{"cid"} = $cour{"id"};
		  #$teacher_conflict{$teacher}{$$time{'week'}}{$$time{'time'}}[$i]{"group"} = $cour{"group"};		  
		  #$i++;
		  
		  $i = @teacher_conflict;
		  $teacher_conflict[$i]{"teacher"}	= $teacher;
		  $teacher_conflict[$i]{"dept1"}	= $teacher_time{$teacher}{$$time{'week'}}{$$time{'time'}}{"course"}{"dept"} ;
		  $teacher_conflict[$i]{"cid1"}		= $teacher_time{$teacher}{$$time{'week'}}{$$time{'time'}}{"course"}{"cid"} ;
		  $teacher_conflict[$i]{"group1"}	= $teacher_time{$teacher}{$$time{'week'}}{$$time{'time'}}{"course"}{"group"} ;
		  $teacher_conflict[$i]{"dept2"}	= $dept;
		  $teacher_conflict[$i]{"cid2"}		= $cour{"id"};
		  $teacher_conflict[$i]{"group2"}	= $cour{"group"};
	    }else{																				###  若此教師此時段尚未註冊，註冊之
	      #$teacher_time{$teacher}{$$time{'week'}}{$$time{'time'}}{"teacher"} = $teacher;
		  $teacher_time{$teacher}{$$time{'week'}}{$$time{'time'}}{"course"}{"dept"}	= $dept;
		  $teacher_time{$teacher}{$$time{'week'}}{$$time{'time'}}{"course"}{"cid"}		= $$course{"id"};
		  $teacher_time{$teacher}{$$time{'week'}}{$$time{'time'}}{"course"}{"group"}	= $$course{"group"};
		}
		#print "$teacher - $$time{'week'} - $$time{'time'} set to 1<BR>\n";
	  }
	  #####  以下執行教室衝堂相關的判斷及建立資料結構
	  $classroom = $cour{'classroom'};
	  next if( $classroom eq "0" );															###  排除教授研究室（代碼為0）
	  if( defined($classroom_time{$classroom}{$$time{'week'}}{$$time{'time'}}) ) {			###  若此教室此時段已經註冊
																							###  建立教室衝堂資料結構 %classroom_conflict
	    $i = @classroom_conflict;
		$classroom_conflict[$i]{'classroom'}	= $classroom;
		$classroom_conflict[$i]{'dept1'}			= $classroom_time{$classroom}{$$time{'week'}}{$$time{'time'}}{'dept'};
		$classroom_conflict[$i]{'cid1'}				= $classroom_time{$classroom}{$$time{'week'}}{$$time{'time'}}{'cid'};
		$classroom_conflict[$i]{'group1'}			= $classroom_time{$classroom}{$$time{'week'}}{$$time{'time'}}{'group'};
		$classroom_conflict[$i]{'dept2'}			= $dept;
		$classroom_conflict[$i]{'cid2'}				= $$course{"id"};
		$classroom_conflict[$i]{'group2'}			= $$course{"group"};
	  }else{
	    $classroom_time{$classroom}{$$time{'week'}}{$$time{'time'}}{'dept'}	= $dept;
		$classroom_time{$classroom}{$$time{'week'}}{$$time{'time'}}{'cid'}		= $$course{'id'};
		$classroom_time{$classroom}{$$time{'week'}}{$$time{'time'}}{'group'}	= $$course{'group'};
	  }
	  
	}
	#$time_str = Format_Time_String(@time);
	#print "$$course{'id'} - $$course{'group'} - $time_str <BR>\n";
  }
}

#print @teacher_conflict;

#####  顯示教師衝堂資訊 TABLE
print qq "
  <TABLE border=1> 
    <TR bgcolor='YELLOW'><TH colspan=3>教師衝堂</TH></TR>
    <TR><TH>科目1</TH><TH>科目2</TH><TH>教師</TH></TR>
";
foreach $tea (@teacher_conflict) {
  #print "$$tea{'dept1'}, $$tea{'cid1'}, $$tea{'group1'}<BR>\n";
  %cou1 = Read_Course($$tea{'dept1'}, $$tea{'cid1'}, $$tea{'group1'});
  %cou2 = Read_Course($$tea{'dept2'}, $$tea{'cid2'}, $$tea{'group2'});
  print "
    <TR>
	  <TD>($$tea{'cid1'} _ $$tea{'group1'}) $cou1{'cname'}</TD>
	  <TD>($$tea{'cid2'} _ $$tea{'group2'}) $cou2{'cname'}</TD>
	  <TD>$Teacher_Name{$$tea{'teacher'}}</TD>
	</TR>
  ";
}
print "</TABLE>";

#####  顯示教室衝堂資訊 TABLE
print qq "
  <TABLE border=1> 
    <TR bgcolor='YELLOW'><TH colspan=3>教室衝堂</TH></TR>
    <TR><TH>科目1</TH><TH>科目2</TH><TH>教室</TH></TR>
";
foreach $room (@classroom_conflict) {
  %cou1 = Read_Course($$room{'dept1'}, $$room{'cid1'}, $$room{'group1'});
  %cou2 = Read_Course($$room{'dept2'}, $$room{'cid2'}, $$room{'group2'});
  print "
    <TR>
	  <TD>($$room{'cid1'} _ $$room{'group1'}) $cou1{'cname'}</TD>
	  <TD>($$room{'cid2'} _ $$room{'group2'}) $cou2{'cname'}</TD>
	  <TD>$classroom{$$room{'classroom'}}{'cname'}</TD>
	</TR>
  ";
}
print "</TABLE>";

################################################################################
sub HTML_Head
{
  my($title);
  ($title)=@_;
  print("Content-type: text/html\n\n");
  print qq(
        <html>
		  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
          <SCRIPT language=JAVASCRIPT>
                function Open_Update_Window(link)
                {
                  win=open(link,"openwin","width=350,height=350,resizable");
                  win.creator=self;
                }
          </SCRIPT>
          <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <title>$title</title>
          </head>
          <BODY background="../../Graph/manager.jpg">
            <CENTER>
              <H1>$title</H1>
              <HR size=2 width=50%>
  );
}
