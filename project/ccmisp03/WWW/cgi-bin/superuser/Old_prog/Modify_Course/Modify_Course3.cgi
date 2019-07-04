#!/usr/local/bin/perl

require "../../../LIB/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Teacher.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Error_Message.pm";

print("Content-type:text/html\n\n");
my(%Input,@Date,$i,@Teacher);
%Input = User_Input();
%input = %Input;
%dept  = Read_Dept($input{dept_id});

Check_Dept_Password($Input{dept_id}, $Input{password});
Print_Title();

#foreach $k (keys %Input) {
#  print("$k ---> $Input{$k}<br>");
#}

Delete_Course_Data()  if( $Input{action} eq "delete" );
Modify_Course_Data()  if( $Input{action} eq "modify" );


###########################################################################
sub Print_Title()
{
  $action = "修改"  if( $input{action} eq "modify" );
  $action = "刪除"  if( $input{action} eq "delete" );
  print qq(
   <html><head><title>開排課系統--$action當學期已開科目</title></head>
   <body background=$GRAPH_URL/ccu-sbg.jpg>
     <center>
      <br>
      <table border=0 width=40%>
       <tr>
        <td>系別:</td><td> $dept{cname} </td>
        <td>年級:</td><td> $input{grade} </td></tr><tr>
        <th colspan=4><H1>$action當學期已開科目</H1></th>
       </tr>
      </table>
      <hr width=80%>
  );
}
###########################################################################
sub Delete_Course_Data()
{

  $result=Delete_Course($input{course_id},$input{course_group},$input{dept_id});
  if      ( $result eq "TRUE" ) {
    print("<font color=red>本科目已成功\刪除!</font>");
  }elsif  ( $result eq "NOT_FOUND" ) {
    print("<font color=red>系統發現錯誤: 科目資料不存在!</font>");
  }
  print("<p>");
  Links3($input{dept_id} ,$input{grade}, $input{password} );
}
############################################################################
sub Modify_Course_Data()
{

  @Teacher = Read_Teacher_File();
  $i=0;
  foreach $key(%Input)
  {
   if($Input{$key} eq "999")
   {
    $Date[$i++]=$key;
   }
  }

  if($Input{group} eq "") { $Input{group} = "01" };

  %temp=Read_Dept($Input{dept_id});

  print "
  <html>
  <head>
  <title>新增學期開課[開課確認]- $temp{cname} </title>
  </head>
  
  <body bgcolor=white background=$GRAPH_URL"."ccu-sbg.jpg>
  <center>";
  ## check area ##
  $error=0;
  $fatal_error=0;
   
$time_string="A/1/2/3/4/B/5/6/7/8/C/D/E";
$week_string="日/一/二/三/四/五/六";  

#  print "<hr><font size=4 color=red>系統檢查開課資料結果如下</font><br>\n";
#  print "<font size=4 brown>
#  [如有嚴重錯誤出現,系統將不接受此開課資料]</font><br><br>\n";
#  if(-e $COURSE_PATH.$Input{dept_id}."/".$Input{dept_id}."_".$Input{group})
#  {
#   print "本學期本科目已經開課完畢<br>\n";
#   print "欲修改科目內容請由主選單使用修改當學期已開科目之功\能<br>";
#   goto END;
#  }
  if($Input{course_id} eq "")
  {
   $fatal_error++;
   print "嚴重錯誤: 沒有輸入科目代碼<br>\n";
  }
  if($Input{cname} eq "" || $Input{ename} eq "")
  {
   $fatal_error++;
   print "嚴重錯誤: 沒有輸入科目名稱<br>\n";
  }
  if($Input{Teacher} eq "")
  {
   $error++;
   print "錯誤: 沒有設定授課教師, 將設為教師未定, 系統仍接受此開課資料<br>\n";
   $Input{Teacher}="99999";
  }
  if($Input{total_time} eq "" || $Input{credit} eq "")
  {
   $fatal_error++;
   print "嚴重錯誤: 沒有設上課時數或學分<br>\n";
  }
  if($Input{classroom} eq "")
  {
   $error++;
   print "錯誤: 沒有設定上課教室, 將設為教室未定, 系統仍接受此開課資料<br>\n";
   $Input{classroom}="E0000";
  }
  if($Input{property} eq "")
  {
   $error++;
   print "錯誤: 沒有設定科目屬性, 將定為必修, 系統仍接受此開課資料<br>\n";
   $Input{property}="0";
  }
  if($Input{principle} eq "")
  {
   $error++;
   print "錯誤: 沒有設定篩選原則, 將定為不須篩選, 系統仍接受此開課資料<br>\n";
  }
  if($Input{total_time} ne $i)
  {
   $fatal_error++;
   print "嚴重錯誤: 上課時數與時間表上打勾時數不合<br>\n";
  }
  my(@Course,$Course_Number,$j,%course);
@Course = Find_All_Course($Input{dept_id});
$Course_Number = @Course;
for($j=0;$j<$Course_Number;$j++)
{
 if($Course[$j]{id} ne $Input{course_id} || $Course[$j]{group} ne $Input{group}) 
 {
 %course=Read_Course($Input{dept_id},$Course[$j]{id},$Course[$j]{group});
 
  my($k,$classroom_error,$teacher_error);
  for($k=0;$k < $course{total_time};$k++)
  {
   for($l=0;$l < $i;$l++)
   {
    ### 新增科目時間與舊有科目時間相同時 ###
    if( join("_",$course{time}[$k]{week},$course{time}[$k]{time})
        eq $Date[$l] )
    {
     @temp = split(/\*:::\*/,$Input{Teacher});
     foreach $temp(@temp)
     {   
foreach $temp2( @{$course{teacher}} )
      {
       if($temp eq $temp2 && $temp ne "99999")
       {
        ($temp3,$temp4)=split(/_/,$Date[$l]);
        $error++;
        my($temp5);
        $temp5= (split("/",$week_string))[$temp3];
        $temp5=$temp5.(split("/",$time_string))[$temp4];
print "錯誤:授課教師<font color=brown>
$Teacher_Name{$temp}</font>
授課時間<font color=red>[$temp5]</font>
與$course{cname}班別$course{group}衝堂，系統仍接受此開課資料<br>\n";
       }
      }
     }
      ### end of 教師衝堂檢查 ###
      ### begin 教室衝堂檢查 ###
     if( $course{classroom} eq $Input{classroom} )
     {
       ($temp3,$temp4)=split(/_/,$Date[$l]);
        $error++;
        my($temp5);
        $temp5= (split("/",$week_string))[$temp3]; 
        $temp5=$temp5.(split("/",$time_string))[$temp4];
        my(%temp6);
        %temp6=Read_Classroom($Input{classroom});
print "錯誤:教室<font color=brown>$temp6{cname}</font> 
與$course{cname}班別$course{group}於
<font color=red>[$temp5]</font>教室衝堂<br>";
     }
    }
   }
  }
 }
}         

  if($fatal_error>0)
  {
   goto END;
  }
#  if($error==0)
#  {
#   print "沒有發現錯誤";
#  }
  
  ## end of check area ##
  $temp=join("*:::*",@Date);
  print "<hr>
  <form method=post action=Modify_Course4.cgi>
  <input type=hidden name=action value=\"modify\">
  <input type=hidden name=password value=$Input{password}>
  <input type=hidden name=grade value=$Input{grade}>
  <input type=hidden name=dept_id value=$Input{dept_id}>
  <input type=hidden name=date value=$temp>
  <table border=1>
  <tr>
  <th bgcolor=yellow>科目名稱(中文)</th><th>";
   print "$Input{cname}<input type=hidden name=cname value=\"$Input{cname}\">";
  print "
  </th></tr>
  <tr>
  <th bgcolor=yellow>科目名稱(英文)</th><th>";
   print "$Input{ename}<input type=hidden name=ename value=\"$Input{ename}\">";
  print "</th></tr>
  </table><br>
  <table border=1>
  <tr>
    <th colspan=2 rowspan=12>
    <table border=12>
    <tr>
    <th></th><th bgcolor=orange>一</th>
             <th bgcolor=orange>二</th>
             <th bgcolor=orange>三</th>
             <th bgcolor=orange>四</th>
             <th bgcolor=orange>五</th>
             <th bgcolor=orange>六</th>
             <th bgcolor=orange>日</th>
             </tr>
    ";
  for($j=0;$j<=12;$j++)
  {
   print "<tr><th bgcolor=orange>";
   if ($j==0)
     { print "A";}
   if ($j>=1 && $j<=4)
     { print "$j";}
   if ($j==5)
     { print "B";}
   if ($j>=6 && $j<=9)
     { $jj=$j-1; print "$jj"; }
   if ($j==10)
     { print "C";}
   if ($j==11)
     { print "D";}
   if ($j==12)
     { print "E";}
   print "</th>";
   for($i=1;$i<=7;$i++)
   {
    $k="$i"."_$j";
    $CHECK=0;
    foreach $ele (@Date) {
      if($k eq $ele)
      {
       $CHECK=1;
       goto OUT;
      } 
    }
    OUT:
    if($CHECK==1)
    {
     print "<th><img src=$GRAPH_URL"."Scheck.gif></th>\n";
    }
    else
    {
     print "<th>&nbsp</th>\n";
    }
   }
   print "</tr>";
  }
  print "
  </table>";
  ######### end of 功課表 ################
  print "
  </th>
  <th bgcolor=yellow>開課年級</th><th>";
  $g_string[1]="一";
  $g_string[2]="二";
  $g_string[3]="三";
  $g_string[4]="四";
  print "$g_string[$Input{grade}]年級</th></tr><tr>
  <th bgcolor=yellow>科目編號:</th><th>";
   print "$Input{course_id} <input type=hidden name=course_id value=$Input{course_id}>";
  print "</th></tr><tr>
  <th bgcolor=yellow>班別</th>
  <th>$Input{group}</th><input type=hidden name=group value=\"$Input{group}\">";
  print "</th>
  </tr>
  <tr>
  <th bgcolor=yellow>授課老師</th><th>";
   @temp = split(/\*:::\*/,$Input{Teacher});
   foreach $temp(@temp)
   {
    print $Teacher_Name{$temp},"<br>\n";
   }
   print ("<input type=hidden name=Teacher value=$Input{Teacher}>");
   $Input{Teacher} = join(/ /,@temp);
  print "</th>
  </tr>
  <tr>
  <th bgcolor=yellow>時數:</th>
  <th>$Input{total_time}
  <input type=hidden name=total_time value=$Input{total_time}>";
  print "
  </th>
  </tr>
  <tr>
  <th bgcolor=yellow>學分:</th>
 <th>$Input{credit}
  <input type=hidden name=credit value=$Input{credit}>";
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
  print "<input type=hidden name=property value=$Input{property}>";
  print "
  </th>
  </tr>
  <tr>
  <th bgcolor=yellow>上課教室:</th>
  <th>";
    %classroom=Read_Classroom($Input{classroom});
  print "[$classroom{id}]$classroom{cname}";
  print "<input type=hidden name=classroom value=\"$classroom{id}\">\n";
  print "</th>
  </tr>
  <tr><th bgcolor=yellow>篩選原則</th><th>\n";
  my($p,@p_string);
  $p_string[0]="不需篩選";
  $p_string[1]="一次篩選";
  $p_string[2]="二次篩選";
  print "$p_string[$Input{principle}]";
  print "<input type=hidden name=principle value=$Input{principle}>";
  print "</th></tr></table>\n";
  
  ## draw table for 備註 ##
  print "<table border=1>";
  print "</select></th></tr>\n";
  print "<tr><th bgcolor=yellow>限修人數</th><th>\n";
  $temp=$Input{number_limit_2}*100+$Input{number_limit_1}*10+$Input{number_limit_0};
  if($temp ne "0")
  {
  print "$temp 人";
  }
  else
  {
   print "無";
  }
  print "<input type=hidden name=number_limit value=$temp>\n";
  print "</th>";
  ### 保留學生名額 ###
  print "<th bgcolor=yellow>保留名額</th><th>\n";
  $temp=$Input{reserved_number_2}*100+$Input{reserved_number_1}*10+$Input{reserved_number_0};
  if($temp ne "0")
  {
   print "$temp 人";
  }
  else
  {
   print "無";
  }
  print "<input type=hidden name=reserved_number value=$temp>\n";
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
  print "<input type=hidden name=support_dept value=$Input{support_dept}>\n";
  print "<input type=hidden name=support_grade value=$Input{support_grade}>\n";
  print "<input type=hidden name=support_class value=$Input{support_class}>\n";
  print "</th></tr>\n";
  ### 擋修系所 ###
  print "<tr><th bgcolor=pink rowspan=2>擋修系所</th><th rowspan=2>\n";
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
  print "</th><th bgcolor=pink>擋修年級</th><th>\n";
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
  print "</th></tr><tr><th bgcolor=pink>擋修班級</th><th>\n";
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
  print "<input type=hidden name=ban_dept value=$Input{ban_dept}>\n";
  print "<input type=hidden name=ban_grade value=$Input{ban_grade}>\n";
  print "<input type=hidden name=ban_class value=$Input{ban_class}>\n";
  print "</th></tr>\n";
  print "<tr><th bgcolor=yellow>備註欄</th>";
  print "<th colspan=3>";
  print $Input{note};
  print "<input type=hidden name=note value=\"$Input{note}\">";
  print "</th></tr>
  </table>
  ";
  print "<p>
  <center>
  <input type=\"submit\" value=\"確定修改科目資料\">
  </form>";
  END:
  print "
  <form>
  <input type=button onclick=history.back() value=回到上一頁修改資料>
  </form>
  <hr>";
  Links1($Input{dept_id},$Input{grade},$Input{password});
  print "
  </center>
  </body>
  </html>";
  ## end of html file ##
}


