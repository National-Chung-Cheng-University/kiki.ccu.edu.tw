#!/usr/local/bin/perl
print "Content-type: text/html","\n\n";

#################################################################################################
#####   Query.cgi 
#####   提供學生查詢歷年及本學期的成績
#####   Date: Jun 22,2000
#####   Coder: Nidalap
#####   Updates:
#####     199?/??/??  第一版：花了幾天撰寫和測試完成  by ???
#####     199?/??/??  被笨蛋伯榆毀於一旦，臨危受命於三個小時內重新撰寫，用了至少三年  Nidalap :D~
#####     200?/??/??  讀取歷年成績部份執行嚴重缺乏效率，改為透過 grep 執行  Nidalap :D~
#####     2009/12/21  歷年成績檔改為依學年學期個別檔案，相關修正  Nidalap :D~
#################################################################################################
require "../../../LIB/Reference.pm";
require $LIBRARY_PATH . "System_Settings.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Course.pm";
require $LIBRARY_PATH . "Student.pm";
require $LIBRARY_PATH . "Password.pm";
require $LIBRARY_PATH . "Error_Message.pm";

%INPUT = User_Input();

#foreach $k (keys %INPUT) {
#  print("$k --> $INPUT{$k}<br>\n");
#}

$id = $INPUT{"id"};
$service = $INPUT{"service"};
$password = $INPUT{"password"};

%student = Read_Student($id);
%dept = Read_Dept($student{dept});

$crypt_salt = Read_Crypt_Salt($id, "student");
$password = Crypt($password, $crypt_salt);
Check_Student_Password($id, $password);

#&Check_For_Valid_Input($id,$dept);
#$correct_password = &Find_Password($dept,$id);
#&Check_For_Correct_Password($password,$id);

#require "Course_cname.pm";
#%Course_cname = &Find_Course_Cname();


@grades = &Get_Student_Grades($id);
%order = &Get_Student_Orders($id);

#foreach $grades (@grades) {
#  print("$$grades{cid}, $$grades{grp}, $$grades{grade}<br>\n");
#}

#foreach $year (sort keys %order) {
#  foreach $sem (sort keys %{$order{$year}}) {
#    print("$year $sem $order{$year}{$sem}<BR>\n");
#  }
#}

if   ($id =~ /^4/) {  $identity = "大學部";  }
elsif($id =~ /^6/) {  $identity = "碩士班";  }
elsif($id =~ /^8/) {  $identity = "博士班";  }
elsif($id =~ /^5/) {  $identity = "碩士專班";  }
else               {  $identity = "";  }

#$service == "當學期成績查詢";

if( ($service eq "歷年成績查詢") or ($service eq "暑修成績查詢") ) {
  &Show_Output("History");
}elsif($service eq "當學期成績查詢") {
  &Show_Output("Current");
}

#########################################################################
#####  將最後的所有資料以 HTML 排版 Show 出
#####  但 Table 交由  &Print_Grade_Tables_Current() 及
#####                 &Print_Grade_Tables_History() 來秀
#########################################################################
sub Show_Output()
{
  my($service) = @_;
  my($i);
  $i = 0;

  print qq(
    <HTML>
      <HEAD>
        $EXPIRE_META_TAG
        <TITLE>國立中正大學  學生成績查詢系統</TITLE>
      </HEAD>
      <BODY background=$GRAPH_URL/bk.jpg>
        <Center>
          <H1>國立中正大學  學生成績查詢系統</H1><HR>
 
          <table border=1 width=75%>
            <TR><th bgcolor=YELLOW>姓名:$student{name}</th>
               <th bgcolor=YELLOW>學號:$id</th>
               <th bgcolor=YELLOW>系所名稱: $dept{cname} $identity</th>
          </table>
  );

  &Print_Grade_Tables_Current() if($service eq "Current");
  &Print_Grade_Tables_History() if( ($service eq "History") or
                                    ($service eq "Summer" )    );
}
#########################################################################
#####  Show 出所有的成績及科目 Table
#########################################################################
sub Print_Grade_Tables_History()
{
  my($last_year, $last_sem, $term);

  for($i=0; $grades[$i]{year} ne ""; $i++) {
#    %course = Read_History_Course($grades[$i]{cid}, $grades[$i]{grp});
    $new_table = "FALSE";
    if( ($last_year ne $grades[$i]{year}) or ($last_sem ne $grades[$i]{term}) ) {
       $new_table = "TRUE";
    }
    if( $new_table eq "TRUE" ) {
       if( $grades[$i]{term} == 3 ) {
         $term = "暑修";
       }else{
         $term = "第" . $grades[$i]{term} . "學期";
       }
       print("</table><P>");
       print("$grades[$i]{year}學年$term");
#       $year_ = $grades[$i]{year};
#       $term_ = $grades[$i]{term};
       
#foreach $year (sort keys %order) {
#  foreach $sem (sort keys %{$order{$year}}) {
#    print("$year $sem $order{$year}{$sem}<BR>\n");
#  }
#}

#       print("[$grades[$i]{year} : $grades[$i]{term}]<BR>\n");
#       if( ($grades[$i]{year} == 97) and ($grades[$i]{term} == 1 ) ) {
	 $temp_year = $grades[$i]{year};
	 $temp_term = $grades[$i]{term};
         #####  20091006實在解不出來的鬼 bug，暫時用鳥方法治標  Nidalap :D~
         #####  不知為何 97_1 的 order 值會是 null，但是直接這樣呼叫卻有值
#	 if( ($temp_year == 97) and ($temp_term == 2) ) {
#	   $temp_order = $order{'97'}{'2'};

         if( ($temp_year == 97)  ) {
           $temp_order = $order{'97'}{$temp_term};
	 }elsif( $temp_year == 98 ) {
	   $temp_order = $order{'98'}{$temp_term};
	 }elsif( $temp_year == 99 ) {
	   $temp_order = $order{'99'}{$temp_term};
	 }else{
           $temp_order = $order{"$temp_year"}{"$temp_term"}; 
         }

#	 $temp_order = $order{'97'}{'1'};
#         print("[$i : $grades[$i]{year} : $grades[$i]{term}]<BR>\n");
#         print("(第 $order{$grades[$i]{year}}{$grades[$i]{term}} 名)<BR>");
         print("(第 $temp_order 名)<BR>");                                 

#       }else{ 
#         print("(第 $order{$grades[$i]{year}}{$grades[$i]{term}} 名)<BR>");
#       }
#       print("(第 $order{$year_}{$term_} 名)<BR>");
       print("<table border=1 width=75%>");
       print("<tr><th>科目代碼</th><th>班別</th>
                  <th>科目名稱</th><TH>選課學分屬性</TH><th>學分</th><th>成績</th>");
    }
    $grades[$i]{grade} = "I" if($grades[$i]{grade} eq "");
    print("<tr>");
    print("<td>$grades[$i]{cid}</td>");
    print("<td>$grades[$i]{grp}</td>");
    print("<td>$grades[$i]{course_cname}</td>");
    print("<td align=CENTER>$PROPERTY_TABLE2{$grades[$i]{course_attr}}</TD>");
    print("<td>$grades[$i]{credit}</td>");
    print("<td>$grades[$i]{grade}</td>");
#    print("<td></td>");
    $last_year = $grades[$i]{year};
    $last_sem  = $grades[$i]{term};
  }
  print("</table>");
}

############################################################################
sub Print_Grade_Tables_Current()
{
  $y = $grades[$i]{year};
  $t = $grades[$i]{term};
  
  print("$y學年第$t學期");
  
  print("(第 $order{99}{1} 名)<BR>");
  print("<table border=1 width=75%>");
  print("<tr><th>科目代碼</th><th>班別</th>
             <th>科目名稱</th><TH>選課學分屬性</TH><th>學分</th><th>成績</th>");
  for($i=0; $grades[$i]{year} ne ""; $i++) {
#     %course = Read_History_Course($grades[$i]{cid}, $grades[$i]{grp});
     $grades[$i]{grade} = "I" if($grades[$i]{grade} eq "");
     print("<tr>");
     print("<td>$grades[$i]{cid}</td>");
     print("<td>$grades[$i]{grp}</td>");
     print("<td>$grades[$i]{course_cname}</td>");
     print("<td align=CENTER>$PROPERTY_TABLE2{$grades[$i]{course_attr}}</TD>");
     print("<td>$grades[$i]{credit}</td>");
     print("<td>$grades[$i]{grade}</td>");

#     print("<td></td>");
  }
  print("</table>");
}
############################################################################
#####  由Get_Student_Grades()讀出的出學生成績(一行一行的)
#####  取出學生的成績
############################################################################
#sub Read_Out_Grades()
#{
#  my(@lines, $i, $junk);
#  @lines = @_;
#
#  $i = 0;
#  foreach $line (@lines) {
#    $line =~ s/\n//;
#    ($junk,$year[$i],$sem[$i],$course_id[$i],$grp[$i],
#               $course_time[$i],$course_attr[$i],$grade[$i],$credit[$i]) = split(/\t/,$line);
##    print("$line ---> $junk<br>\n");
##    print("$course_id[$i] $grade[$i] <br>\n");
##    if($grade[$i] eq "
#    if( (($course_time[$i] eq '1')or($course_time[$i] eq '2'))  and
#        (($course_attr[$i] eq '1')or($course_attr[$i] eq 'A'))    )  {
#      if   ( $grade[$i] == "4" )  {  $grade[$i] = "甲";  }
#      elsif( $grade[$i] == "3" )  {  $grade[$i] = "乙";  }
#      elsif( $grade[$i] == "2" )  {  $grade[$i] = "丙";  }
#      elsif( $grade[$i] == "1" )  {  $grade[$i] = "丁";  }
#      elsif( $grade[$i] == "0" )  {  $grade[$i] = "戊";  }
#    }
#    $i++;
#  }
#
#}
#
############################################################################
sub Check_For_Correct_Password()
{ 
  my($password,$id) = @_;
  my($su_password_file, $su_password);

  $salt = Read_Crypt_Salt($id, "student");
  $password = Crypt($password, $salt);

  Check_Student_Password($id, $password);

#  return if($password eq $su_password);
#  return if($password eq $correct_password);    
  
#  &Error_Message("PASSWORD");
}

############################################################################
#####  由檔案讀出學生成績的資訊

sub Get_Student_Grades()
{
  my($id) = @_;
  my($grade_file,@grades,@id_grades, @line);
  my($tmp, $course_time, $course_attr, @GRA, $i);
  my $tmpfile = "/tmp/" . $id . ".grade";

  if($service eq "歷年成績查詢") {
     $grade_file = $DATA_PATH . "Grade/all.txt";
  }elsif($service eq "當學期成績查詢") {
     $grade_file = $DATA_PATH . "Grade/now.txt";
  }elsif($service eq "暑修成績查詢") {
     $grade_file = $DATA_PATH . "Grade/summer.txt";
  }  

  system("grep $id $grade_file > $tmpfile");

  open(TMP, $tmpfile);
  @line = <TMP>;
  close(TMP);
  unlink $tmpfile;

#  open(GRADE_FILE,$grade_file) or die("Cannot open file $grade_file!\n");
#  @grades = <GRADE_FILE>;
#  close(GRADE_FILE);
#  foreach $grade (@grades) {
#    if($grade =~ $id) {
#      push(@line,$grade);
#    }
#  }  
  for($i=0; defined($line[$i]); $i++) {
    ($tmp, $GRA[$i]{year}, $GRA[$i]{term}, $GRA[$i]{cid}, $GRA[$i]{grp},
     $GRA[$i]{course_time}, $GRA[$i]{course_attr}, $GRA[$i]{grade}, $GRA[$i]{credit}, $GRA[$i]{course_cname} )
    = split(/\t/,$line[$i]);

    if( $GRA[$i]{course_attr} == "9" )  {             ###  屬性欄==9, 是為棄選
      $GRA[$i]{grade} = "棄選";
    }
    ###  除了操性以外, 已經沒有等第制了. 好幾年前的事情, 現在發現.  2008/02/13 Nidalap :D~
#    if( (($GRA[$i]{course_time} eq '1')or($GRA[$i]{course_time} eq '2'))  and
#        (($GRA[$i]{course_attr} eq '1')or($GRA[$i]{course_attr} eq 'A'))    )  {
#      if   ( $GRA[$i]{grade} eq "4" )  {  $GRA[$i]{grade} = "甲";  }
#      elsif( $GRA[$i]{grade} eq "3" )  {  $GRA[$i]{grade} = "乙";  }
#      elsif( $GRA[$i]{grade} eq "2" )  {  $GRA[$i]{grade} = "丙";  }
#      elsif( $GRA[$i]{grade} eq "1" )  {  $GRA[$i]{grade} = "丁";  }
#      elsif( $GRA[$i]{grade} eq "0" )  {  $GRA[$i]{grade} = "戊";  }
#    }
  } 
  return(@GRA);
}
############################################################################
#####  Get_Student_Orders
#####  由檔案讀取學生的每學期排名
#####  Added Mar/16,2001
#####  Nidalap :D~
############################################################################
sub Get_Student_Orders()
{
  my($input_id) = @_;
  my(@lines, $year, $sem, $id, $order, %order );
  
  $order_file = $DATA_PATH . "Grade/std_orders.txt";
  open(ORDER_FILE, $order_file) or print("Error opening file $order_file!\n");
  
  @lines = <ORDER_FILE>;
  close(ORDER_FILE);
  foreach $line (@lines) {
    $line =~ s/\n//;
    ($year, $sem, $id, $order) = split(/\s+/, $line);
    if($id eq $input_id) {
      $order{$year}{$sem} = $order;
#      print("$year : $sem -> $order<BR>\n");
    }
  }
  return(%order);  
}
############################################################################

sub Check_For_Valid_Input()
{
  my($id,$dept,$message) = @_;
  if($dept eq "") {
     $message = "1";
     &Error_Message_($message);
  }
}
############################################################################
sub Error_Message_()
{
  my($message) = @_;
  if($message eq "1") {
    $message = "系統找不到您的學號, 請確認學號沒有打錯!"; 
  }elsif($message eq "2") {
    $message = "您並沒有輸入學號, 請重新輸入!";
  }elsif($message eq "PASSWORD") {
    $message = "您的密碼不正確, 請重新輸入!";
  }

  print("<HTML><BODY><CENTER><H1>登入錯誤</H1><hr>");
  print("$message");
  print qq (<p><A href="http://kiki.ccu.edu.tw/~ccmisp04/">回上頁</A>);    
  exit(1);
}

############################################################################

