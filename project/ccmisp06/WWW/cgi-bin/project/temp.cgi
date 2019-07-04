#!/usr/local/bin/perl
#############################################################################################
#####  Modify_Course2.cgi
#####  修改當學期已開科目
#####  page2: 
#####   修改模式：提供輸入科目相關資料的 FORM 
#####   刪除模式：要求確認
#####  Updates:
#####   2009/05/05 加入暑修課程類型 remedy 欄位 (1為一般，2為補救)  Nidalap :D~
#####   2010/03/19 加入 教師專長與授課科目是否符合 s_match 欄位  Nidalap :D~
#####   2010/04/08 體育中心和軍訓開課，不顯示 s_match 欄位  Nidalap :D~
#####   2010/04/20 篩選原則加入一些判定出現與否，以及預設值設定，防呆用 Nidalap :D~
#####   2010/05/17 修正上一條的防呆判定  Nidalap :D~
#####   2010/05/25 s_match 出現與否，改為交給 Need_s_match() 判斷  Nidalap :D~
#####   2010/10/25 語言中心可開通識外語課程功能 Nidalap :D~
#####   2010/11/24 加入 gender_eq, env_edu 兩個欄位  Nidalap :D~
#####   2010/12/16 若要刪除本學期新開課程，顯示特別警示訊息以提醒要同步刪除後端資料  Nidalap :D~
#####   2010/12/16 刪除課程前顯示該科目修習學生名單，並於下頁同步刪除選課資料  Nidalap :D~
#####   2011/04/25 新增學系服務學習課程相關判斷: 某些欄位不需顯示  Nidalap :D~
#####   2012/04/11 新增開課學制(碩/博班課程)欄位 attr，只有在研究所課程中需要選擇.  Nidalap :D~
#####   2012/11/07 學系服務學習課程「要」顯示支援班級欄位  Nidalap :D~
#####   2013/11/25 新增「擋修系所」下的「選擇所有大學部學系」點選功能; 擋修/支援系所size加到8  Nidalap :D~
#####   2015/04/15 因應文學院需求-委由各系實際執行開課，新增 $open_dept 變數  Nidalap :D~
#####	2015/11/09 若選擇電算中心的電腦教室，則透過 jquery 顯示電腦教室借用相關訊息 Nidalap :D~
#####	2016/05/16 判斷人數篩選選項處，改為透過 dept_cd 而非 open_dept 判斷 Nidalap :D~
#####	2016/06/27 學系服務學習課程只能選一小時的規定，改為暑修不在此限	Nidalap :D~
#####   2017/08/16 修正學系服務學習課程不應顯示篩選人數相關選項 Print_Number_Limit_Box() 的 BUG Nidalap :D~
#############################################################################################

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Open_Course.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Teacher.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."System_Settings.pm";

print("Content-type:text/html\n\n");
%Input = User_Input();
%Dept  = Read_Dept($Input{open_dept});
@teacher = Read_Teacher_File();
%cge = Read_Cge();

$cge_lan_flag = $Input{cge_lan_flag};
$grade_show = ($Input{grade} eq "cge_lan") ? "通識外語課" : $Input{grade};

#foreach $key (keys %Input) {
#  print("$key ---> $Input{$key}<br>");
#}

@all_course = Find_All_Course($Input{dept_cd}, "", "history");

($request, $course_id, $course_group) = split(/:::/, $Input{choice});
if( $cge_lan_flag == 2 ) {					###  若是語言中心開通識外語課，讀取語言中心密碼檔 salt
  Check_Dept_Password($DEPT_LAN, $Input{password});
}else{								###  其餘一般情形：讀取該系所密碼檔 salt
  Check_Dept_Password($Input{open_dept}, $Input{password});
}
%classroom = Read_Classroom($Input{classroom});
$is_dept_serv = 0;
$is_dept_serv = 1  if( $course_id == Get_Dept_Serv_Course_ID($Dept{id}));	### 系所服務學習課程



#print("superuser = $SUPERUSER<BR>");

Print_Header();

if( $request eq "" ) {
  print("請選擇刪除或修改某科目!");
  $Input{dept_cd} = $DEPT_LAN  if( $Input{cge_lan_flag} == 2 );  ### 若是語言中心開通識外語課，還原系所代碼為語言中心
  Links2();
  exit(1);
} 

%Course = Read_Course($Input{dept_cd}, $course_id, $course_group, "" );
$Input{grade} = 1 if( $Input{cge_lan_flag} == 2 );

#Print_Hash(%Course);

Modify_Course_Data() if( $Input{choice} =~ /MODIFY/ );
Delete_Course_Data() if( $Input{choice} =~ /DELETE/ );

#foreach $k (keys %Input) {
#  print  ("$k --> $Input{$k}<br>");
#}
#print("teacher = $Course{teacher}[0]<br>\n");
if( $Input{cge_lan_flag} == 2 ) { $Input{dept_cd} = $DEPT_LAN;  $Input{grade} = 1}  ### 若是語言中心開通識外語課，還原系所代碼為語言中心

#Print_Hash(%Input); 
#print "open_dept = " . $Input{open_dept};

Links3($Input{dept_cd} ,$Input{grade}, $Input{password},$Input{open_dept});
exit(1);

############################################################################
sub Print_Header()
{
  my($choice);
  $choice="修改"  if($Input{choice} =~ "MODIFY");
  $choice="刪除"  if($Input{choice} =~ "DELETE");
  print qq(
   <html>
     <head>
       $EXPIRE_META_TAG
       <title>開排課系統-- $choice當學期已開科目</title>
     </head>
  );

  Add_JS();

$title = $SUB_SYSTEM_NAME . "開排課系統--$choice當學期已開科目";
print Print_Open_Course_Header(\%Input, \%Dept, $title);

}
############################################################################
sub Add_JS()
{
  my($test, $classroom_msg) = Read_Special_Announce("classroom_msg");
  print qq(
    <SCRIPT language=javascript src=\"./Classify.js\"></SCRIPT>
	<SCRIPT language=javascript src=\"../../javascript/jquery.js\"></SCRIPT>
    <SCRIPT language=JAVASCRIPT>
	  \$(document).ready(function() {
	    //////////  點選「擋修系所」下的「選擇所有大學部學系」功能	added 2013/11/25 Nidalap :D~
	    \$('#ban_select_all_under_dept').click(function() {
		  var depts = new Array();
		  var i=0;
		
		  \$('#ban_dept option').each(function() {		///  選取所有代碼為 xxx4 的單位
		    if( \$(this).val().substring(3,4) == '4' ) 
		      depts[i++] = \$(this).val();
		  });
		  \$('#ban_dept').val(depts);
	    });
		/////  若選擇電算中心的電腦教室，則顯示電腦教室借用相關訊息
	    \$('#classroom').change(function(){
		  var classroom = \$(this).val();
		  var cc_test = /CC/;
		  if( cc_test.test(classroom) ) {
		    //alert("classroom = " + classroom);
		    \$('#classroom_msg').html("<FONT size=2 color='RED'>$classroom_msg</FONT>");
		  }else{
		    \$('#classroom_msg').html("");
		  }		
	    });
	  });
	
      function Add_Precourse_Win()
      {
        win2=open("./Add_Precourse_Window.html","openwin","width=400,height=350");
        win2.creator=self;
      }
      // 清除先修科目所選的所有資料
      function Clear_Precourse()
      {
        form1.Precourse.length=1;
        form1.Precourse.options[0].value="99999";
        form1.Precourse.options[0].text="無";
      }

    </SCRIPT>
  );
}
############################################################################
sub Delete_Course_Data()
{
  my(@stu, %stu, $table_content);
  print qq(
    <table border=1>
      <tr><th>科目編號</th><th>科目班別</th><th>科目中文名稱</th></tr>
      <tr><td>$course_id</td><td>$course_group</td><td>$Course{cname}</td></tr>
    </table>
  );
  #####  檢查此科目修課名單  Added 2010/12/16 Nidalap :D~
  @stu = Student_in_Course($Input{dept_cd}, $Course{id}, $Course{group}, "", "");
  $i = 0;
  foreach $stu (@stu) {
    %stu = Read_Student($stu);
    $table_content .= "<TR>"  if( $i%4 == 0 );
    $table_content .= "<TD>$stu$stu{name}</TD>";
    $table_content .= "</TR>"  if( ($i%4 == 3) );
    $i++;
  }
  
  if( @stu > 0 ) {
    print qq[
      <P><B><FONT color=RED>
        本科目目前尚有學生選修(名單如下)，若刪除此科目，系統會同步刪除學生選課資料！
      <FONT><B><BR>
      <TABLE border=1 size=50%">
        $table_content
      </TABLE>
    ];
  }
  
  print("<br><font color=red> 您確定要刪除此科目?</font>");
  if( $Course{isNEW} eq "TRUE" ) {
    print("<BR><B><FONT color=RED>本科目為當學期新開科目，請記得同時刪除後端資料！</FONT></B><BR>");
  }
  print qq(
    <FORM action="Modify_Course3.cgi" method=POST>
      <INPUT type=hidden name=dept_cd value=$Input{dept_cd}>
	  <INPUT type=hidden name=open_dept value=$Input{open_dept}>
      <INPUT type=hidden name=grade value=$Input{grade}>
      <INPUT type=hidden name=password value=$Input{password}>
	  <INPUT type=hidden name=cge_lan_flag value=$Input{cge_lan_flag}>
      <INPUT type=hidden name=id value=$course_id>
      <INPUT type=hidden name=course_group value=$course_group>
      <INPUT type=hidden name=action value="delete">
      <INPUT type=submit value="確定刪除">
      <INPUT type=button onclick=history.back() value="回上一畫面">
    </FORM>
  );

}
############################################################################
sub Modify_Course_Data()
{
  if( $SUPERUSER eq "1" ) {
    Print_Course_Title_For_SU();
  }else{
    Print_Course_Title();
  }

  Print_Timetable_Select(@{$Course{time}});                      ###  印出功課表

  Print_Course_Content();
  
  Print_Note_Table();

print "<p>
<center>
<Input type=\"submit\" value=\"送出資料\">
<Input type=\"reset\" value=\"重新填寫\">
</form><hr>";


 
}
############################################################################
sub Print_Course_Title()
{
  print qq(
    <FORM name=form1 method=post action=Modify_Course3.cgi>
    <Input type=hidden name=action value="modify">
    <Input type=hidden name=dept_cd value=$Input{dept_cd}>
	<INPUT type=hidden name=open_dept value=$Input{open_dept}>
	<INPUT type=hidden name=cge_lan_flag value=$Input{cge_lan_flag}>
    <Input type=hidden name=password value=$Input{password}>
    <table border=1>
    <tr>
    <th bgcolor=yellow>科目名稱(中文)</th>
      <th>$Course{cname}</th>
      <Input type=hidden name=cname value="$Course{cname}">
    </tr>
    <tr>
    <th bgcolor=yellow>科目名稱(英文)</th>
      <th>$Course{ename}</th>
      <Input type=hidden name=ename value="$Course{ename}">
    </tr>
    </table><br>
    <table border=1>
    <tr>
    <th colspan=2 rowspan=13>
  );
}
#################################################################################
sub Print_Course_Title_For_SU()
{
  print "
    <form name=form1 method=post action=Modify_Course3.cgi>
    <Input type=hidden name=action value=modify>
    <Input type=hidden name=dept_cd value=$Input{dept_cd}>
	<INPUT type=hidden name=open_dept value=$Input{open_dept}>
    <Input type=hidden name=password value=$Input{password}>
	<INPUT type=hidden name=cge_lan_flag value=$Input{cge_lan_flag}>
    <table border=1>
    <tr>
    <th bgcolor=yellow>科目名稱(中文)</th>
      <th><Input type=text length=70 name=cname value='$Course{cname}'></th>
    </tr>
    <tr>
    <th bgcolor=yellow>科目名稱(英文)</th>
      <th>
      <Input type=text length=70 name=ename value='$Course{ename}'>
      </th>
    </tr>
    </table><br>
    <table border=1>
    <tr>
    <th colspan=2 rowspan=13>";
}
############################################################################
sub Print_Time_Table()
{
  print qq(
        <table border=1>
           <tr>
             <th></th>
             <th bgcolor=orange>一</th>
             <th bgcolor=orange>二</th>
             <th bgcolor=orange>三</th>
             <th bgcolor=orange>四</th>
             <th bgcolor=orange>五</th>
             <th bgcolor=orange>六</th>
             <th bgcolor=orange>日</th>
           </tr>
  );
  for($j=0;$j<=13;$j++) {
    print "<tr><th bgcolor=orange>";
    if ($j==0)			{ print "A";}
    if ($j>=1 && $j<=4)		{ print "$j";}
    if ($j==5)			{ print "F";}
    if ($j==6)			{ print "B";}
    if ($j>=7 && $j<=10)	{ $jj=$j-2; print "$jj"; }
    if ($j==11)			{ print "C";}
    if ($j==12)			{ print "D";}
    if ($j==13)			{ print "E";}
    print "</th>";
    for($i=1;$i<=7;$i++) {
      $k="$i"."_$j";
      $CHECK=0;
      foreach $ele (@{$Course{time}}) {
        if($k eq "$$ele{week}_$$ele{time}" ) {
          $CHECK=1;
          goto OUT;
        }
      }
      OUT:
      if($CHECK == 0) {
        print "<td><Input type=checkbox name=$k value=999></td>";
      }else{
        print "<td><Input type=checkbox name=$k value=999 checked></td>";
      }
    }
    print "</tr>";
  }
  print "</table>";
}
###########################################################################
sub Print_Course_Content()
{
  print("<th bgcolor=yellow>開課年級</th><th><select name=grade>");
  
  @g_string = ("", "一", "二", "三", "四");

  if( ($Input{dept_cd} =~ /6$/) and ($Input{dept_cd} ne "7006") ) {
    print "<option value=1 selected>$g_string[1]年級\n";
  }else{
    for($i=1;$i<5;$i++) {
     if($i == $Input{grade}) {
       print "<option value=$i selected>$g_string[$i]年級\n";
     }else{
#       print "<option value=$i>$g_string[$i]年級\n";   ### 修改年級有BUG
     }
    }
  }

  print("</select></th></tr><tr><th bgcolor=yellow>科目編號:</th>");
  print qq(
    <td>$course_id</td></tr>
    <Input type=hidden name=id value=$course_id>
    <tr><th bgcolor=yellow>班別</th><th>
    $course_group</th></tr>
    <Input type=hidden name=group value=$course_group>
  );
  print("<tr><th bgcolor=yellow>授課老師</th>");
  ##### read teacher_code and name of this department####
  print qq[
    <th>
    <select name=Teacher size=3 multiple onblur=\"isDelete(document.form1.Teacher)\">
  ];
  if( $Course{teacher}[0] eq "" ) {
    print("<option value=99999 selected>教師未定");
  }else{
    $i=0;
    while( $Course{teacher}[$i] ne "" ) {
       print qq( <option value=$Course{teacher}[$i] selected>$Teacher_Name{$Course{teacher}[$i]} );
       $i++;
    }
  }
  print qq(
    </select>

    </th></tr>
    <tr><th bgcolor=yellow>選擇授課老師</th><th>);
  print qq[
    <Input type=button name=btn1 value=新增任課教師 onclick=\"AddWin()\">
    <Input type=button name=btn2 value=重置 onClick=\"ClearAll(document.form1.Teacher)\">
    </th></tr></tr>
  ];  
############################################################################
#####  教師專長與授課科目是否符合
if(  Need_s_match($Input{dept_cd}) ) {
  print qq(
    <tr>
      <th bgcolor=yellow>教師專長與授課科目是否符合</th>
      <td>
        <select name="s_match">
  );
  foreach $k (sort keys %S_MATCH) {
    if( $k eq $Course{s_match} ) {
      $temp = "SELECTED";
    }else{
      $temp = "";
    }
    print("        <option value='$k' $temp>$S_MATCH{$k}</option>\n");
  }
  print qq(
        </select>
      </td>
    </tr>
  );
}
############################################################################  
  print qq(
    <tr>
    <th bgcolor=yellow>時數:</th>
    <th><select name=total_time>
  );
  if( ($is_dept_serv == 1) and !$IS_SUMMER ) {              ###  學系服務學習課程只能選一小時（暑修不在此限20160627）
    print "<OPTION value=1>1";
  }else{
    for($i=1;$i<=12;$i++) {
      if($i ne $Course{total_time} ) {
        print "<option value=$i>$i";
      }else{
        print "<option value=$i selected>$i";
      }
    }
  }
  print("</SELECT>");
#############################################################################
  print qq(
    <tr><th bgcolor=yellow>正課/實驗實習/書報討論時數:</th>
    <th><select name=lab_time1>
  );
  if( ($is_dept_serv == 1) and !$IS_SUMMER ) {              ###  學系服務學習課程只能選一小時（暑修不在此限20160627）
    print "<OPTION value=1>1";
  }else{
    for($i=0;$i<=12;$i++) {
      if($i ne $Course{lab_time1} ) {
        print "<option value=$i>$i";
      }else{
        print "<option value=$i selected>$i";
      }
    }
  }
  print("</SELECT><SELECT name=lab_time2>");   ###
  for($i=0;$i<=12;$i++) {
    if($i ne $Course{lab_time2} ) {
      print "<option value=$i>$i";
    }else{
      print "<option value=$i selected>$i";
    }
  }
  print("</SELECT><SELECT name=lab_time3>");   ###
  for($i=0;$i<=12;$i++) {
    if($i ne $Course{lab_time3} ) {
      print "<option value=$i>$i";
    }else{
      print "<option value=$i selected>$i";
    }
  }
#############################################################################
  print qq(
    </select></th></tr><tr><th bgcolor=yellow>學分:</th>
    <th>$Course{credit}</th>
    <Input type=hidden name=credit value=$Course{credit}>
  );
  print qq(
    </select></th></tr><tr><th bgcolor=yellow>必修/選修/通識</th>
    <th><select name=property>
  );
  if( $is_dept_serv == 1 ) {              ###  系所服務學習課程只能選必修
    print "<OPTION value=1>必修";
  }else{
    for($i=1;$i<=3;$i++) {
      if($i==1) { $name="必修"; }
      if($i==2) { $name="選修"; }
      if($i==3) { $name="通識"; }
      if($i eq $Course{property} ) { 
        print "<option value=$i selected>$name";
      }else{
        print "<option value=$i>$name"; 
      }
    }
  }
######################################################################
#  print qq(
#    </select></th></tr><tr><th bgcolor=yellow>一般/軍訓/體育</th>
#    <th><select name=suffix_cd>
#  );
#  for($i=0;$i<=2;$i++) {
#    if($i==0) { $suffix_cd="一般"; }
#    if($i==1) { $suffix_cd="軍訓"; }
#    if($i==2) { $suffix_cd="體育"; }
#    if($i eq $Course{suffix_cd} ) {
#      print "<option value=$i selected>$suffix_cd";
#    }else{
#      print "<option value=$i>$suffix_cd";
#    }
#  }
######################################################################
  print qq(
    </select></th></tr><tr><th bgcolor=yellow>上課教室:</th>
    <th><select name=classroom id='classroom'>
  );
  %classroom = Read_All_Classroom();
  foreach $classroom_id (sort keys %classroom) {
    if( $classroom_id eq $Course{classroom} ) {
      print "<option value='$classroom_id' SELECTED>
            $classroom{$classroom_id}{cname}($classroom{$classroom_id}{size_fit})\n";
    }else{
      print "<option value=$classroom_id>
             $classroom{$classroom_id}{cname}($classroom{$classroom_id}{size_fit})\n";
    }
  }
  print qq(
    </select>
	<DIV id='classroom_msg'></DIV>
	</th>
  </tr>
  );

#######################################################################
#####  開課學制(碩/博班課程) attr
                                        ###  研究所： $attr = [0,1,2,3] 其中 0 會被打回來重填
#print ":::" . !$IS_GRA . ":::" . !is_Undergraduate_Dept($Input{open_dept}) . ":::" . !is_Exceptional_Dept($Input{open_dept}) . ":::";
#print "under:" . is_Undergraduate_Dept($Input{open_dept});
if( (!$IS_GRA) and (!is_Undergraduate_Dept($Input{dept_cd})) and (!is_Exceptional_Dept($Input{dept_cd})) ) {
  print qq(
    <TR>
      <TH bgcolor=yellow>開課學制:</TH>
        <th>
          <SELECT name="attr">
  );
  foreach $attr (sort keys %ATTR) {
    if( $attr eq $Course{attr} ) {
      print "<OPTION value='$attr' SELECTED>$ATTR{$attr}\n";
    }else{
      print "<OPTION value='$attr'>$ATTR{$attr}\n";
    }
  }
  print qq(
        </SELECT>
      </TH>
    </TR>
  )
}else{                                  ###  非研究所： $attr = 'N'   
  print "<INPUT type='hidden' name='attr' value='N'>\n";
}

}


###########################################################################
#####  功課表下的資料欄
sub Print_Note_Table()
{
#  print "is_dept_serv = $is_dept_serv<BR>\n";
  
  print "<table border=1>";
  print "</select></th></tr>\n";

  if( $is_dept_serv != 1 ) {			###  系所服務學習課程: 不顯示人數篩選相關選項
    Print_Number_Limit_Box();
  }
  Print_Support_Dept_Box();			###  一律顯示支援系所年級班級相關選項框框
  if( $is_dept_serv != 1 ) {			###  系所服務學習課程: 除了備註以外其餘欄位皆不顯示
    Print_Ban_Dept_Box();				###  顯示擋修系所年級班級相關選項框框
    Print_Support_CGE_Box();			###  顯示支援通識領域人數相關選項框框
    Print_Precourse_Box();				###  顯示先修科目相關選項框框
    Print_Misc_Box();						###  顯示上課方式相關選項框框
    Print_Remedy_Box();					###  顯示暑期授課辦法相關選項框框  
  } 
  Print_Note_Box();						###  顯示備註欄選項框框
  print "  </table>";
}
###########################################################################
sub Print_Number_Limit_Box
{
  print "<tr><th bgcolor=yellow>限修人數</th><th>";

  if( $SUPERUSER == 1 ) {                    #####  管理者, 可以修改限修人數   
    print "<table border=0>\n<tr><td>百</td><td>十</td><td>個</td></tr>\n";
    print "<tr><td><select name=number_limit_2>";
    my($i,$j);
    $j = int($Course{number_limit}/100);
    #$j= ($Course{number_limit}-$Course{number_limit}%100)/100;
    for($i=0;$i<10;$i++) {
      if($i ne $j) { 
        print "<option value=$i>$i\n"; 
      }else{
        print "<option value=$i selected>$i\n"; 
      }
    }
    print "</select></td><td><select name=number_limit_1>";
    $j= int(( $Course{number_limit} % 100 ) /10);
    for($i=0;$i<10;$i++) {
      if($i ne $j) {
        print "<option value=$i>$i\n"; 
      }else{ 
        print "<option value=$i selected>$i\n"; 
      }
    }
    print "</select></td><td><select name=number_limit_0>";

    $j= $Course{number_limit} % 10;
    for($i=0;$i<10;$i++) {
      if($i ne $j) { 
        print "<option value=$i>$i\n"; 
      }else{ 
        print "<option value=$i selected>$i\n"; 
      }
    }
    print "</select></td></tr></table>";
  }elsif( $Course{number_limit} == 0 ) {         #####  不限修
    print("無");
  }else{                                         #####  有限修
    print("$Course{number_limit}(由教室容量決定)<BR>");
  }

  print "</th>";
  ### 保留學生名額 ###
  print "<th bgcolor=yellow>保留新生名額</th><th><table border=0>\n";
  print "<tr><td>百</td><td>十</td><td>個</td></tr>\n";
  print "<tr><td><select name=reserved_number_2>";
  my($i,$j);
  $j= ($Course{reserved_number}-$Course{reserved_number}%100)/100;
  for($i=0;$i<10;$i++) {
    if($i ne $j)
       { print "<option value=$i>$i\n"; }
    else
       { print "<option value=$i selected>$i\n"; }
  }
  print "</select></td><td><select name=reserved_number_1>";
  $j= int (( $Course{reserved_number} % 100 ) /10);
  for($i=0;$i<10;$i++)  {
    if($i ne $j)
      { print "<option value=$i>$i\n"; }
    else
      { print "<option value=$i selected>$i\n"; }
  }
  print "</select></td><td><select name=reserved_number_0>";

  $j= $Course{reserved_number} % 10;
  for($i=0;$i<10;$i++)  {
    if($i ne $j)
      { print "<option value=$i>$i\n"; }
    else
      { print "<option value=$i selected>$i\n"; }
  }
  print "</select></td></tr></table></th></tr>\n";
}
#######################################################################################
#####  顯示支援系所年級班級相關選項框框
sub Print_Support_Dept_Box
{

  my(@Dept,$dept,%Dept,$flag,$disabled_html);

  $disabled_html = "";
  if( $is_dept_serv == 1 ) {
    $disabled_html = "DISABLED = DISABLED";
  }
  @Dept=Find_All_Dept();
  print "<tr><th bgcolor=yellow rowspan=2>支援系所</th><th rowspan=2>\n";
  print "<select name=support_dept size=8 multiple $disabled_html>\n";
  foreach $dept(@Dept)  {
    %Dept=Read_Dept($dept);
    $flag=0;
    foreach $ele(@{$Course{support_dept}})  {
      if( $ele eq $dept)
        { $flag = 1; break; }
    }
    if( $flag == 1 )  {
       print "<option value=$Dept{id} selected>$Dept{cname}\n";
    }else{
       print "<option value=$Dept{id}>$Dept{cname}\n";
    }
  }
  print "</select></th><th bgcolor=yellow >支援年級</th><th>\n";
  print "<select name=support_grade size=2 multiple $disabled_html>";
  my(@g_string) = ("", "一", "二", "三", "四");
  for($i=1;$i<=4;$i++)  {
    $flag=0;
    foreach $ele(@{$Course{support_grade}})  {
      if($ele eq $i)
        { $flag=1; break; }
      }
      if($flag == 1)
         { print "<option value=$i selected>$g_string[$i]年級\n"; }
      else
         { print "<option value=$i>$g_string[$i]年級\n"; }
    }
   print "</select></th></tr><tr><th bgcolor=yellow>支援班級</th>\n";
   print "<th><select name=support_class size=2 multiple>\n";
   @g_string= ("A", "B", "C", "D", "E", "F");
   for($i=0;$i <=5;$i++)  {
     $flag=0;
     foreach $ele( @{$Course{support_class}} )  {
       if($ele eq $g_string[$i])
          { $flag=1; break; }
     }
	 if($flag == 1)   {
        print "<option value=$g_string[$i] selected>$g_string[$i]\n";
     }else{
        print "<option value=$g_string[$i]>$g_string[$i]\n";
     }
   }
   print "</select></th></tr>\n";
}
###################################################################################
sub Print_Ban_Dept_Box
{

  print "<tr>
           <th bgcolor=YELLOW rowspan=2>
			 擋修系所
		   </th>
		   <th rowspan=2>
		     <INPUT type=checkbox id='ban_select_all_under_dept'>選擇所有大學部學系<BR>
  ";
  print "<select name=ban_dept id='ban_dept' size=8 multiple>\n";
  
  my(@Dept,$dept,%Dept,$flag);
  @Dept=Find_All_Dept();

  foreach $dept(@Dept)  {
    %Dept=Read_Dept($dept);
    $flag=0;
    foreach $ele(@{$Course{ban_dept}})  {
      if( $ele eq $dept)
         { $flag = 1; break; }
      }
	  if( $flag == 1 )  {
  	     print "<option value=$Dept{id} selected>$Dept{cname}\n";
     }else{
         print "<option value=$Dept{id}>$Dept{cname}\n";
     }
   }
   print "</select></th><th bgcolor=YELLOW>擋修年級</th><th>\n";
   print "<select name=ban_grade size=2 multiple>";
   my(@g_string) = ("", "一", "二", "三", "四");
   for($i=1;$i<=4;$i++)  {
     $flag=0;
     foreach $ele(@{$Course{ban_grade}})  {
       if($ele eq $i)
           { $flag=1; break; }
	 }
	 if($flag == 1)
        { print "<option value=$i selected>$g_string[$i]年級\n"; }
     else
   	    { print "<option value=$i>$g_string[$i]年級\n"; }
     }
     print "</select></th></tr><tr><th bgcolor=YELLOW>擋修班級</th>\n";
     print "<th><select name=ban_class size=2 multiple>\n";
    @g_string= ("A", "B", "C", "D", "E", "F");
    for($i=0;$i <=5;$i++)  {
	  $flag=0;
	  foreach $ele( @{$Course{ban_class}} )  {
  	     if($ele eq $g_string[$i])
           { $flag=1; break; }
	  }
	  if($flag == 1)  {
  	       print "<option value=$g_string[$i] selected>$g_string[$i]\n";
      }else{
           print "<option value=$g_string[$i]>$g_string[$i]\n";
      }
    }
    print "</select></th></tr>\n";
}
########################################################################################
#####  顯示支援通識領域人數相關選項框框
sub Print_Support_CGE_Box
{
  print qq(
    <TR><TH bgcolor=PINK>支援通識領域</TH>
        <TH colspan=3 align=left><SELECT name="support_cge_type">
  );
  foreach $cge (sort keys %cge) {
    if($cge eq $Course{support_cge_type}) {
      print("<OPTION value=$cge SELECTED>$cge{$cge}{sub_cge_id_show} $cge{$cge}{cge_name}");
    }else{
      print("<OPTION value=$cge>$cge{$cge}{sub_cge_id_show} $cge{$cge}{cge_name}");
    }
  }
  ###########################   支援通識人數
  $support_cge_number_0 = $Course{support_cge_number} % 10;  ## 個位數
  $support_cge_number_1 = ($Course{support_cge_number} - $support_cge_number_0) / 10;  ## 十位數
 
  print qq(
    </SELECT></TH></TR>
    <TR><TH bgcolor=PINK>支援通識人數</TH>
        <TH colspan=3 align=left>
          <TABLE>
            <tr><td>十</td><td>個</td></tr>
            <tr><td><select name=support_cge_number_1>
  );
  my($i);
  for($i=0;$i<10;$i++) {
     if($i ne $support_cge_number_1)
       { print "<option value=$i>$i\n"; }
     else
       { print "<option value=$i selected>$i\n"; } 
  }
  print("</select></td><td><select name=support_cge_number_0>");

  for($i=0;$i<10;$i++) {
     if($i ne $support_cge_number_0)
       { print "<option value=$i>$i\n"; }
     else
       { print "<option value=$i selected>$i\n"; }
  }
  print("</SELECT></TD></TR></TABLE></TD></TR>");
}
########################################################################################
######  顯示先修科目相關選項框框
sub Print_Precourse_Box
{
  print qq(
    <TR>
      <TH bgcolor=PINK>先修科目</TH>
      <TD colspan=3 align=left>
        <SELECT name=Precourse size=3 multiple>
  );

  if( !defined($Course{prerequisite_course}) )  {
    print qq(<OPTION value="99999">無);
  }else{
    foreach $precourse (@{$Course{prerequisite_course}}) {
      if( ($$precourse{dept} eq "99999") or ($$precourse{dept} eq "")) {
        print qq(<OPTION value="99999">無);
        next;
      }
      %predept = Read_Dept($$precourse{dept});
      %precourse = Read_Course($$precourse{dept}, $$precourse{id}, "01", "history");
      $course_string_to_select = $predept{cname2} . ":[" . $$precourse{id} . "]" . $precourse{cname} . "-" . $GRADE{$$precourse{grade}};

      $course_string_hidden = join(":", $$precourse{dept}, $$precourse{id}, $$precourse{grade});
      print qq(<OPTION value=$course_string_hidden SELECTED>$course_string_to_select\n);
    }

    $default_pre_and = "SELECTED";
    $default_pre_or  = "";
    if( $Course{prerequisite_logic} eq "OR" ) {
      $default_pre_and = "";
      $default_pre_or  = "SELECTED";
    }
  }
  print qq(
        </SELECT>
        <BR>
        <!CENTER>
        <INPUT type=button name=select_precourse value=選擇先修科目 onclick="Add_Precourse_Win()">
        <INPUT type=button name=select_precourse2 value=重置 onclick="Clear_Precourse()"><BR>
        <SELECT name=prerequisite_logic>
          <OPTION value="AND" $default_pre_and>$PREREQUISITE_LOGIC{AND}
          <OPTION value="OR"  $default_pre_or>$PREREQUISITE_LOGIC{OR}
        </SELECT>
      </TD>
    </TR>
  );
}
########################################################################################
#####  顯示上課方式相關選項框框
sub Print_Misc_Box
{
  print "<tr><th bgcolor=yellow>上課方式</th>";

  $checked{dis} = "CHECKED"  if( $Course{distant_learning} == 1 );
  $checked{eng} = "CHECKED"  if( $Course{english_teaching} == 1 );
  $checked{gen} = "CHECKED"  if( $Course{gender_eq} == 1 );
  $checked{env} = "CHECKED"  if( $Course{env_edu} == 1);

  print qq(
    <TD colspan=3>
      <INPUT type=checkbox name=distant_learning $checked{dis}> 遠距教學課程<BR>
      <INPUT type=checkbox name=english_teaching $checked{eng}> 全英語授課<BR>
      <INPUT type=checkbox name=gender_eq        $checked{gen}> 性別平等教育課程<BR>
      <INPUT type=checkbox name=env_edu          $checked{env}> 環境教育相關課程
    </TD>   
  );
}
########################################################################################
#####  顯示暑期授課辦法相關選項框框  
#####  Added 2009/05/05  Nidalap :D~
#####  暑期授課辦法修訂，暑期所開授之課程分為以下兩類： 
#####  第一類課程：經系（所、中心）課程委員會議審議通過之選修課程。
#####  第二類課程：曾開授之課程，以補救教學為原則。 
#####  請於暑期開排課系統增加選項，排課人員得勾選課程類別，
#####  以利後端課務系統計算最低開課人數、課程收費標準等計算教師鐘點資料。
sub Print_Remedy_Box
{
  if( is_Summer() and !is_GRA() ) {       ### 只作用於「一般生暑修」
    $temp{$Course{remedy}} = "SELECTED";
    print qq( 
      <tr><th bgcolor=yellow>暑修課程類型</th>
        <td colspan=3>
          <SELECT name="remedy">
            <OPTION value="1" $temp{1}>第一類課程：經系（所、中心）課程委員會議審議通過之選修課程
            <OPTION value="2" $temp{2}>第二類課程：曾開授之課程，以補救教學為原則
          </SELECT>
        </TD>
      </TR>
    );
  }
}
##########################################################################################
###  顯示備註欄選項框框
sub Print_Note_Box
{
  print "<tr><th bgcolor=yellow>備註欄</th>";
  print "<th colspan=3><textarea name=note rows=3 cols=40>";
  print $Course{note};
  print "</textarea></th></tr>";
}