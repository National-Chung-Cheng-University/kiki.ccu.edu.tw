1;
##  顯示錯誤訊息                ##
##  input : 錯誤訊息(字串)      ##
##  output: none                ##
##  program by ionic ,1998/8/26 ##

#############################################################################
sub Error
{
  local ($Error_Message);
  print "Content-type: text/html","\n\n";
  print $EXPIRE_META_TAG
  print "<title>系統警告訊息</title>
         <body background=$GRAPH_URL"."ccu-sbg.jpg>
         <center><br>
         <h1><font color=red>系統發現錯誤如下</font></h1>
         <hr size=3 width=80%>
         <h2>";
  ($Error_Message)=@_;
  print "$Error_Message<br>";
  print "<hr size=3 width=80%><br>";
  print "<table border=0 width=50%><tr><th colspan=2>
         <form>
         <input type=button onclick=history.back() value=回上一畫面>
         </form></td></tr><tr>
         <th><a href=\"http://www.ccu.edu.tw\">回到中正大學首頁</a></th>
         <th><a href=$HOME_URL>回到開排課系統首頁</a></th>
         </tr></table>";
  print "</body></html>";
  exit(0);
}              

#############################################################################
#####    Fatal_Error()
#####    將程式不應該發生的錯誤記錄到記錄檔內
#####    Coder: Nidalap
#####    Date : Dec 31,1998
#############################################################################
sub Fatal_Error
{
  my($error_string, %time, $ip);
  my ($logfile);

#  require "./Reference.pm";
  ($error_string) = @_;
  %time = gettime();
  $logfile = $LOG_PATH . "Error.log";
  if($ENV{HTTP_X_FORWARDED_FOR} eq "")  { $ip = $ENV{REMOTE_ADDR};  }
  else			 	        { $ip = $ENV{HTTP_X_FORWARDED_FOR}; }
  $ip =~ s/, $LOG_IGNORE_IP//;
  
  umask(000);
  open(LOG,">>$logfile") or print("ERROR:Cannot open file $logfile!\n");
  print LOG ("$time{time_string} : $ip : $error_string : $ENV{SERVER_ADDR}\n");
  close(LOG);
}
#############################################################################
#####  2015/11/10  新增 $version 紀錄是否行動版，且將原有額外紀錄的 $su 變數也使用標準分隔字元做分隔(不相容於舊版)。 by Nidalap :D~
sub Student_Log
{
  my ($su, $ip, $log_file, $version);
  my ($action, $stu_id, $course_id, $course_group, $property, $by_whom) = @_;
  
#  if($action eq "DELETE") {  print("Lalalaa!!!"); }
  $log_file = $DATA_PATH . "Student.log";
  %time = gettime();
  $su = "SU"  if($SUPERUSER == 1);
  $version = "";
  $version = "MOBILE"  if( $IS_MOBILE == 1);
  if($ENV{HTTP_X_FORWARDED_FOR} eq "")  { $ip = $ENV{REMOTE_ADDR};  }
  else                                  { $ip = $ENV{HTTP_X_FORWARDED_FOR}; }  
  $ip =~ s/, $LOG_IGNORE_IP//;
  
  umask(000);
  open(LOG, ">>$log_file") or print("ERROR:Cannot open file $logfile!\n");
  print LOG ("$action : $time{time_string} : $ip  : $stu_id : $course_id : $course_group : $property : $by_whom : $su : $version\n");
#  print LOG ("$action : $time{time_string} : $ENV{HTTP_X_FORWARDED_FOR} : $stu_id : $course_id : $corse_group : $property $su\n");
  close(LOG);
}
#############################################################################
#####  系所開排課 log, 改自 Student_Log()
#####  Date: 
#####   2002/11/28 Created by Nidalap :D~
#####   2015/04/16 加入 $open_dept 實際開課單位代碼，以利追蹤 by Nidalap :D~
#############################################################################
sub Dept_Log
{
  my ($su, $ip, $log_file);
  my ($action, $dept_id, $course_id, $course_group, $open_dept) = @_;
  
  $log_file = $LOG_PATH . "Dept.log";
  %time = gettime();
  $su = "SU"  if($SUPERUSER == 1);
  if($ENV{HTTP_X_FORWARDED_FOR} eq "")  { $ip = $ENV{REMOTE_ADDR};  }
  else                                  { $ip = $ENV{HTTP_X_FORWARDED_FOR}; }
  $ip =~ s/, $LOG_IGNORE_IP//;  

  umask(000);
  open(LOG, ">>$log_file") or print("ERROR:Cannot open file $logfile!\n");
  print LOG ("$action : $time{time_string} : $ip  : $dept_id : $open_dept : $course_id : $course_group $su\n");
  close(LOG);
}
#############################################################################
sub gettime
{
  my($months, $weekdays, %time, $time_string, @cmonth);
  @cmonth = ("","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec");

  ($time{sec},$time{min},$time{hour},$time{day},$time{month}
   ,$time{year},$time{wday},$time{yday},$time{isdst}) = localtime(time);

#  if( $time{hour} > 12 )  {
#      $time{hour} -= 12;
#      $time{ampm} = "pm";
#  }else{
#      $time{ampm} = "am";
#  }
#  if( $time{hour} == 0 )  {
#    $time{hour} = 12;
#  }

  $time{hour2} = $time{hour};									###  hour:  1 2 3 4...
  $time{hour2} = "0".$time{hour2}  if($time{hour2} < 10);		###  hour2: 01 02 03 04...
  
  $time{month} ++;
  $time{month2} = $time{month};
  $time{month2} = "0".$time{month2}  if($time{month2} < 10);
#  print("month = $time{month}\n");
  $time{cmonth} = $cmonth[$time{month}];
#  print("cmonth = $time{cmonth}\n");
#   for($t=0; $t<=12; $t++) {
#    print("$cmonth[$t]\n");
#  }
  if($time{year}>97) { $time{year} += 1900; }
  else               { $time{year} += 2000; }				### 西元年
  $time{year2} = $time{year} - 1911;
  $time{year2} = "0" . $time{year2}  if( $time{year2} < 100 );          ### 民國年  

  if($time{day}<10)  { $time{day} = "0" . $time{day}; }
  $time{time_string} = sprintf("%s/%s/%s %02d:%02d%s",
                                $time{month},$time{day},$time{year},
                                $time{hour},$time{min},$time{ampm});
  $time{time_string3} = sprintf("%03s/%s/%s", , $time{year2}, $time{month}, $time{day});
  $time{time_string4} = sprintf("%04s/%s/%s", , $time{year}, $time{month}, $time{day});
  $time{time_string_e} = sprintf("%s %s, %04s", , $cmonth[$time{month}], $time{day}, $time{year});
  return(%time);
}

################################################################################
#####  顯示給學生看的訊息
#####  Added on 2005/08/22 Nidalap :D~
sub Show_Message
{
  my($id, $key) = @_;
  
  my @messages;
#  $message[0]{link} = "infotest_msg.html";
#  $message[0]{text} = "資訊能力線上測驗公告";
#  $message[1]{link} = "ic_card_msg.html";
#  $message[1]{text} = "IC 卡學生證最新消息";
  $message[0]{link} = "http://mis.cc.ccu.edu.tw/academic/";
  $message[0]{text} = "學籍登錄系統";
#  $message[3]{link} = "physical_info.html";
#  $message[3]{text} = "選修體育課須知";
#  $message[4]{link} = "http://140.123.10.202/CCU_Center/Infotest/ShowRecState2.php?id=$id&key=$key";
#  $message[4]{text} = "資訊能力繳費查詢";
  $message[1]{link} = "military_info.html";
  $message[1]{text} = "選修軍訓課程須知";
  
#  if( $SUB_SYSTEM == 2 ) {
#    print("<B><FONT COLOR=RED>繳費期限至95年6月29日截止，請同學務必於期限內繳費</FONT><B><BR>\n");
#  }
  print("<TABLE border=1 width=40% bgcolor=YELLOW><TR><TD><FONT size=-1>重要訊息公告:");
  for ($i=0; defined($message[$i]{link}); $i++) {
    print("<LI><A href=\"$message[$i]{link}\" target=NEW>$message[$i]{text}</A>\n");
  }

#  print("<LI><A href=\"javascript:Open_Infotest_Page($message[4]{link})\">aaa</A>"); 
#  print ("<INPUT type=button value=\"資訊能力繳費查詢\" onClick=Open_Infotest_Page(\"$message[4]{link}\")>"); 
#  print("<LI><A href=\"$message[4]{link}\" target=NEW onfocus=\"javascript:Open_Infotest_Page($message[4]{link})\">aaa</A>");


#  print("<LI><A name=infotest href=\"javascript:window.open($message[4]{link},\"width=350,height=300, top=250,left=300\")\" target=NEW>$message[4]{text}");

  print("</TD></TR></TABLE>");

}

