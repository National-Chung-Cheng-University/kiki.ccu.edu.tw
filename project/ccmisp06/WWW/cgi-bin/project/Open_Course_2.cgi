#!/usr/local/bin/perl
##########################################################################################
#####  Open_Course_2.cgi
#####  開課介面
#####  Last Update:
#####   2002/03/14 加入 75 分鐘課程, 修改功課表 (Nidalap :D~)
#####   2009/05/05 加入暑修課程類型 remedy 欄位 (1為一般，2為補救)
#####   2010/03/19 加入 教師專長與授課科目是否符合 s_match 欄位  Nidalap :D~
#####   2010/04/08 體育中心和軍訓開課，不顯示 s_match 欄位  Nidalap :D~
#####   2010/04/20 篩選原則加入一些判定出現與否，以及預設值設定，防呆用 Nidalap :D~
#####   2010/05/17 修正上一條的防呆判定  Nidalap :D~
#####   2010/05/25 s_match 出現與否，改為交給 Need_s_match() 判斷  Nidalap :D~
#####   2010/10/11 語言中心可開通識外語課程功能 Nidalap :D~
#####   2010/11/24 加入 gender_eq, env_edu 兩個欄位  Nidalap :D~
#####   2011/04/25 新增學系服務學習課程相關判斷: 某些欄位不需顯示  Nidalap :D~
#####   2012/04/11 新增開課學制(碩/博班課程)欄位 attr，只有在研究所課程中需要選擇.  Nidalap :D~
#####   2012/11/07 學系服務學習課程「要」顯示支援班級欄位  Nidalap :D~
#####   2013/11/25 新增「擋修系所」下的「選擇所有大學部學系」點選功能; 擋修/支援系所size加到8  Nidalap :D~
#####   2015/04/13 因應文學院需求-委由各系實際執行開課，新增切換身份按鈕以及 $open_dept 變數  Nidalap :D~
#####   2015/05/26 整合語言中心可開通識外語課，以及文學院委由各系開課功能 Nidalap :D~
#####              切換年級按鈕改由 Show_Switch_Grade_Buttons() 處理 Nidalap :D~
#####	2015/11/09 若選擇電算中心的電腦教室，則透過 jquery 顯示電腦教室借用相關訊息 Nidalap :D~
#####	2016/05/16 判斷人數篩選選項處，改為透過 dept_cd 而非 open_dept 判斷 Nidalap :D~
#####	2016/06/27 學系服務學習課程只能選一小時的規定，改為暑修不在此限	Nidalap :D~
#############################################################################################

$| = 1;
print "Content-type: text/html","\n\n";

require "../library/Reference.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Open_Course.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Error_Message.pm";

my(%Input);

%Input		= User_Input();
%cge		= Read_Cge();
@all_course	= Find_All_Course($Input{open_dept}, "", "history");
%Dept=Read_Dept($Input{open_dept});

#Check_SU_Password($Input{password}, "dept", $Input{open_dept});
$cge_lan_flag = $Input{"cge_lan_flag"};

if( $cge_lan_flag == 2 ) {                                      ###  若是語言中心開通識外語課，讀取語言中心密碼檔 salt
  Check_Dept_Password($DEPT_LAN, $Input{password});
  $Input{'dept_cd'} = $DEPT_CGE;
}else{                                                          ###  其餘一般情形：讀取該系所密碼檔 salt
  Check_Dept_Password($Input{open_dept}, $Input{password});
}


#foreach $k (keys %Input) {
#  print("$k -> $Input{$k}<BR>\n");
#}

if($Input{group} eq "") { $Input{group} = "01" };

if($Input{course_cd} eq "")  {
  $Input{course_cd} = "new";
}
if($Input{course_cd} ne "new") {
  if($Input{course_cd}=~/new/)  {
    ($Input{course_cd},$useless)=split(/\s/,$Input{course_cd});
    %Course = Read_Course( $Input{dept_cd}, $Input{course_cd}, $Input{group},"");
  }else{
    %Course = Read_Course( $Input{dept_cd}, $Input{course_cd}, $Input{group},"history");
  }
}else{
   $new_course_flag = 1;
}
#print "$Input{course_cd} == Get_Dept_Serv_Course_ID($Input{dept_cd})";
$is_dept_serv = 0;
$is_dept_serv = 1  if( $Input{course_cd} eq Get_Dept_Serv_Course_ID($Input{dept_cd}));	### 系所服務學習課程

%temp=Read_Dept($Input{open_dept});

$|=0;
print qq(
  <html>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <head>
      $EXPIRE_META_TAG
      <title>新增學期開課- $temp{cname}</title>
    </head>
);
Add_JS();  ## function to add JavaScript Code

$grade_show = ($Input{grade} eq "cge_lan") ? "通識外語課" : $Input{grade};
if( $TERM == 3 ) {
  $show_term = "";
}else{
  $show_term = join("", "第", $TERM, "學期");
}

print Print_Open_Course_Header(\%Input, \%Dept, "新增當學期開課科目2/4 - 填寫科目資料");

print qq(
  <center>
   <form name=form1 method=post action=Open_Course_3.cgi>
     <INPUT type=hidden name=cge_lan_flag value=$Input{cge_lan_flag}>
     <input type=hidden name=dept_cd value=$Input{dept_cd}>
	 <input type=hidden name=open_dept value=$Input{open_dept}>
     <input type=hidden name=password value=$Input{password}>
     <input type=hidden name=new_course_flag value=$new_course_flag>
     <table border=1>
       <tr>
       <th bgcolor=yellow>科目名稱（中文）</th><th>
);
if($Input{course_cd} ne "new" && $SUPERUSER ne "1") {
  print "$Course{cname}<input type=hidden name=cname value=\"$Course{cname}\">";
}else{
  print "<input type=text length=70 name=cname value=\"$Course{cname}\">";
}
print qq(
    </th></tr>
  <tr>
    <th bgcolor=yellow>科目名稱（英文）</th><th>
);
#$Course{cname} =~ s/"/\"/g;
#$Course{ename} =~ s/"/\"/g;
if($Input{course_cd} ne "new" && $SUPERUSER ne "1") {
  print qq($Course{ename}<input type=hidden name=ename value="$Course{ename}">);
}else{
  print qq(<input type=text length=70 name=ename value="$Course{ename}">);
}
print qq(
    </th></tr></table><br>
    <table border=1>
      <tr>
        <th colspan=2 rowspan=12 valign=TOP>
);
Print_Timetable_Select();

######### end of 功課表 ################
print "</th>\n";
print "<th bgcolor=yellow>開課年級</th><th><select name=grade>";
@g_string = ("", "一", "二", "三", "四");

$grade_one_only = 1  if( ($Input{dept_cd} =~ /6$/) and ($Input{open_dept} != "7006") );	### 除了通識以外的研究所只能選一年級
$grade_one_only = 1  if( $is_dept_serv );						### 系所服務學習課程只能選一年級

if( $grade_one_only ) {
  print "<option value=1 selected>$g_string[1]年級\n";             ###  只能選一年級
}else{                                                             ###  其他系所可以選1~4年級
  for($i=1;$i<5;$i++) {
   if($i == $Input{grade}) {
     print "<option value=$i selected>$g_string[$i]年級\n";
   }else{
     print "<option value=$i>$g_string[$i]年級\n";
   }
  }
}
print "</select></th></tr><tr>
<th bgcolor=yellow>科目編號:</th><th>";
if($Input{course_cd} ne "new")
{
 print "$Course{id}<input type=hidden name=id value=$Course{id} maxlength=7>";
}
else
{
 print "<input type=text length=10 name=id>";
}
print "</th></tr><tr>
<th bgcolor=yellow>班別</th>
<th>";
print "<select name=group>";
for($i=1;$i<=60;$i++)
{
 if($i<10)
 {
   print "<option value=\"0$i\">0$i\n";
 }# end of if($i<10)
 else # $i>=10
 {
   print "<option value=\"$i\">$i\n";
 }
}
print "</select>";
print "</th>
</tr>
<tr>
<th bgcolor=yellow>授課老師</th>";

#### read teacher_code and name of this department####
print "
<th><select name=Teacher size=3 multiple onblur=\"isDelete(document.form1.Teacher)\">
<option value=99999 selected>教師未定
</select></th>
</tr>
<tr><th bgcolor=yellow>選擇授課教師</th>
<th>";
print "
<input type=button name=btn1 value=選擇任課教師 onclick=\"AddWin()\"> 
<input type=button name=btn2 value=重置 onClick=\"ClearAll(document.form1.Teacher)\">
</th></tr>
</tr>
";
############################################################################
#####  教師專長與授課科目是否符合
if( Need_s_match($Input{open_dept}) ) {
  print qq(
    <tr>
      <th bgcolor=yellow>教師專長與授課科目是否符合</th>
        <td>
          <select name="s_match">
  );
  foreach $k (sort keys %S_MATCH) {
    print("        <option value='$k'>$S_MATCH{$k}</option>\n");
  }
  print qq(
        </select>
      </td>
    </tr>
  );
}
############################################################################
print "
  <tr>
  <th bgcolor=yellow>時數:</th>
  <th><select name=total_time>
";
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
print("</select>");
###########################################################################
print qq(
  <tr>
    <th bgcolor=yellow>正課/<BR>實驗實習/<BR>書報討論時數:</th>
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
print qq(</select><SELECT name="lab_time2">);      ###
for($i=0;$i<=12;$i++) {
 if($i ne $Course{lab_time2} ) {
   print "<option value=$i>$i";
 }else{
   print "<option value=$i selected>$i";
 }
}
print qq(</select><SELECT name="lab_time3">);      ###
for($i=0;$i<=12;$i++) {
 if($i ne $Course{lab_time3} ) {
   print "<option value=$i>$i";
 }else{
   print "<option value=$i selected>$i";
 }
}
print("</SELECT></TH></TR>");


###########################################################################
print "
<tr>
<th bgcolor=yellow>學分:</th>
<TH>";
#if($Course{credit} == "" )  {
if($Input{course_cd} eq "new") {      ### 新增科目才能改學分
  print("<SELECT name=credit>\n");
  for($temp=0; $temp<7; $temp++) {
    print("<OPTION>$temp\n");
  }
  print("</SELECT>");
}else{                                ### 歷年科目一律不可改
  print("$Course{credit}");
  print("<INPUT type=hidden name=credit value=$Course{credit}>");
}
#<th><select name=credit>";
#for($i=0;$i<=8;$i++)
# {
#  if($i ne $Course{credit} )
#  { print "<option value=$i>$i"; }
#  else
#  { print "<option value=$i selected>$i"; }
# }
#print "</select>";
print "
</th>
</tr>

<tr>
<th bgcolor=yellow>必修/選修/通識</th>
<th><select name=property>";

if( $is_dept_serv == 1 ) {              ###  系所服務學習課程只能選必修
  print "<OPTION value=1>必修";
}else{
  for($i=1;$i<=3;$i++) {
    if($i==1) { $name="必修"; }
    if($i==2) { $name="選修"; }
    if($i==3) { $name="通識"; }
    if($i eq $Course{property} )
      { print "<option value=$i selected>$name"; }
    else
      { print "<option value=$i>$name"; } 
  }
}

#print "
#</select>
#<tr>
#<th bgcolor=yellow>一般/軍訓/體育</th>
#<th><select name=suffix_cd>";
#for($i=0;$i<=2;$i++)
#{
# if($i==0) { $suffix_cd="一般"; }
# if($i==1) { $suffix_cd="軍訓"; }
# if($i==2) { $suffix_cd="體育"; }
# if($i eq $Course{suffix_cd} )
# { print "<option value=$i selected>$suffix_cd"; }
# else
# { print "<option value=$i>$suffix_cd"; }
#}

print qq(
  </select>
  </th>
  </tr>
  <tr>
  <th bgcolor=yellow>上課教室:</th>
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

#####  開課學制(碩/博班課程) attr
					###  研究所： $attr = [0,1,2,3] 其中 0 會被打回來重填
if( !$IS_GRA and !is_Undergraduate_Dept($Input{dept_cd}) and !is_Exceptional_Dept($Input{dept_cd}) ) {
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
}else{					###  非研究所： $attr = 'N'
  print "<INPUT type='hidden' name='attr' value='N'>\n";
}


#####  結束含功課表的上半部 TABLE
print qq(
  </TABLE>
);

########################  以下是功課表下的資料欄 #######################
print  "    <TABLE border=1><TR>";

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
###################################################################

$Input{dept_cd} = $DEPT_LAN  if( $Input{cge_lan_flag} == 2 );  ### 若是語言中心開通識外語課，還原系所代碼為語言中心

print "<p>
<center>
<input type=\"submit\" value=\"送出資料\">
<input type=\"reset\" value=\"重新填寫\">
</form><hr>";
Links1($Input{dept_cd},$Input{grade},$Input{password}, "", $Input{open_dept});
print "
</center>
</body>
</html>";
 

## end of html file ##

sub Add_JS()
{
  $dept = $Input{open_dept};
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
      win2=open("./Add_Precourse_Window.html?dept=$dept","openwin","width=400,height=450");
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
######################################################################################
#####  顯示篩選原則、限修人數、保留人數等欄位
sub Print_Number_Limit_Box
{
  print qq(
        <TH bgcolor=yellow>人數篩選</TH>
        <TH colspan=3 align=RIGHT>篩選原則: <select name=principle>\n
  );
  my($p,@p_string, $p_default);
  $p_string[0]="不需篩選（碩博士班）";
  $p_string[1]="一次篩選（學士班）";
  $p_string[2]="二次篩選（第一學期學士班大一必修）";

  ###  設定篩選原則的預設值 : 第一學期的大一，預設為二次篩選
  $p_default = 2  if( ($TERM == 1) and ($Course{grade} eq "1") and ($Input{open_dept} !~ /6$/) );
  ###  設定篩選原則的預設值 : 預設為本科目原先的篩選原則
  $p_default = $Course{principle}  if( $Course{principle} ne "" );

  for($p=0;$p<3;$p++) {
    if( $SUPERUSER != 1 ) {			###  判斷特定情況，不顯示某選項
      if($p == 0) {					###  不需篩選: 只有碩博士班會顯示
                                                          ###  通識、師培等單位，不算碩博士
        next if( ($Input{dept_cd} !~ /6$/) or ($Input{dept_cd} eq $DEPT_CGE) or ($Input{dept_cd} eq $DEPT_EDU) and !$is_dept_serv );
      }
	  if($p == 1 ) {				###  一次篩選: 除了學系服務課程外，都要顯示
	    next if $is_dept_serv;
	  }
      if($p == 2) {					###  二次篩選: 只有第一學期的大一(含體育)，或例外單位會顯示
		next if( $TERM != 1 );
        next if( not (  ( (is_Undergraduate_Dept($Input{dept_cd})or($Input{dept_cd} eq $DEPT_PHY)) and ($Input{grade} eq "1") ) 
                       or is_Exceptional_Dept($Input{dept_cd}, 1) ) );
      }
    }
  
    if($p ne $p_default) { 			###  顯示篩選原則選項
      print "<option value=$p>$p_string[$p]\n";
    }else{
      print "<option value=$p selected>$p_string[$p]\n"; 
    }
  }
  print qq(
        </SELECT><BR>
        限修人數: 
  );
  if($SUPERUSER != 1) {           #####  非管理者, 不能修改限修人數
    print("(見上課教室選項後括弧)<BR>");
  }else{                          #####  管理者, 可以修改限修人數
    print qq( <select name=number_limit_2> );
    my($i, @limit_chars);
    @limit_chars = Numeric_to_chars($Course{number_limit});
    for($i=0;$i<10;$i++) {
     if($i ne $limit_chars[2]) { 
       print "<option value=$i>$i\n"; 
     }else{ 
       print "<option value=$i selected>$i\n"; 
     }
    }
    print "</SELECT><SELECT name=number_limit_1>";
    for($i=0;$i<10;$i++) {
     if($i ne $limit_chars[1]) { 
       print "<option value=$i>$i\n"; 
     }else{
       print "<option value=$i selected>$i\n"; 
     }
    }
    print "</select><select name=number_limit_0>";
    for($i=0;$i<10;$i++) {
      if($i ne $limit_chars[0]) { 
        print "<option value=$i>$i\n"; 
      }else{ 
        print "<option value=$i selected>$i\n"; 
      }
    }
    print "</SELECT><BR>";
  }
  ### 保留學生名額 ###
  print "保留新生名額: <SELECT name=reserved_number_2>";
  my($i, @limit_chars);
  @reserved_chars = Numeric_to_chars($Course{reserved_number});

  for($i=0;$i<10;$i++) {
   if($i ne $reserved_chars[2]) { 
     print "<option value=$i>$i\n"; 
   }else{ 
     print "<option value=$i selected>$i\n"; 
   }
  }
  print "</select><select name=reserved_number_1>";
  for($i=0;$i<10;$i++) {
   if($i ne $reserved_chars[1]) { 
     print "<option value=$i>$i\n"; 
   }else{ 
     print "<option value=$i selected>$i\n"; 
   }
  }
  print "</select><select name=reserved_number_0>";
  for($i=0;$i<10;$i++) {
   if($i ne $reserved_chars[0]) { 
     print "<option value=$i>$i\n"; 
   }else{ 
     print "<option value=$i selected>$i\n"; 
   }
  }
  print "</select></th></tr>\n";
}
######################################################################################
#####  顯示支援系所年級班級相關選項框框
sub Print_Support_Dept_Box
{

  my(@Dept,$dept,%Dept,$flag, $disabled_html);

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
    if( $flag == 1 )
      {  print "<option value=$Dept{id} selected>$Dept{cname}\n";  } 
    else 
      {  print "<option value=$Dept{id}>$Dept{cname}\n";  }
  }          
  print "</select></th><th bgcolor=yellow>支援年級</th><th>\n";
  print "<select name=support_grade size=2 multiple $disabled_html>";
  my(@g_string) = ("", "一", "二", "三", "四");
  for($i=1;$i<=4;$i++)  {
   $flag=0;
   foreach $ele(@{$Course{support_grade}}) {
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
    foreach $ele( @{$Course{support_class}} ) {
      if($ele eq $g_string[$i])
      { $flag=1; break; }
    }
     if($flag == 1)
       {   print "<option value=$g_string[$i] selected>$g_string[$i]\n";  }
     else
       { print "<option value=$g_string[$i]>$g_string[$i]\n";  }
   }
  print "</select></th></tr>\n";

}
######################################################################################
#####  顯示擋修系所年級班級相關選項框框
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
  foreach $dept(@Dept) {
   %Dept=Read_Dept($dept);
   $flag=0;
   foreach $ele(@{$Course{ban_dept}}) {
    if( $ele eq $dept)
      { $flag = 1; break; }
   } 
   if( $flag == 1 )
     {  print "<option value=$Dept{id} selected>$Dept{cname}\n"; } 
   else 
     {  print "<option value=$Dept{id}>$Dept{cname}\n";  }
  }          
  print "</select></th><th bgcolor=YELLOW>擋修年級</th><th>\n";
  print "<select name=ban_grade size=2 multiple>";
  my(@g_string) = ("", "一", "二", "三", "四");
  for($i=1;$i<=4;$i++)  {
   $flag=0;
   foreach $ele(@{$Course{ban_grade}}) {
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
    if($flag == 1)
      {  print "<option value=$g_string[$i] selected>$g_string[$i]\n"; }
    else
      {  print "<option value=$g_string[$i]>$g_string[$i]\n";  }
   }
   print "</select></th></tr>\n";
}
######################################################################################
#####  顯示支援通識領域人數相關選項框框
sub Print_Support_CGE_Box
{
  print qq(
    <TR><TH bgcolor=PINK>支援通識領域</TH>
        <TH colspan=3 align=left><SELECT name="support_cge_type">
  );
  foreach $cge (sort keys %cge) {
    if($cge eq "0") {
      print("<OPTION value=$cge SELECTED>$cge{$cge}{sub_cge_id_show} $cge{$cge}{cge_name}");
    }else{
      print("<OPTION value=$cge>$cge{$cge}{sub_cge_id_show} $cge{$cge}{cge_name}");
    }
  }
  print qq(
    </SELECT></TH></TR>
    <TR><TH bgcolor=PINK>支援通識人數</TH>
        <TH colspan=3 align=left>
          <TABLE>
            <tr><td>十</td><td>個</td></tr>
            <tr><td><select name=support_cge_number_1>
  );
  my($i,$j);
  $j = $Course{support_cge_number} / 10;
    for($i=0;$i<10;$i++) {
     if($i ne $j)
       { print "<option value=$i>$i\n"; }
     else
       { print "<option value=$i selected>$i\n"; }
    }
    print("</select></td><td><select name=support_cge_number_0>");
    $j= $Course{support_cge_number} % 10;
    for($i=0;$i<10;$i++) { 
     if($i ne $j)
       { print "<option value=$i>$i\n"; }
     else
       { print "<option value=$i selected>$i\n"; }
    }
  print("</SELECT></TD></TR></TABLE></TD></TR>");
}
######################################################################################
#####  顯示先修科目相關選項框框
sub Print_Precourse_Box
{
  print qq(
    <TR>
      <TH bgcolor=PINK>先修科目</TH>
      <TD colspan=3 align=left>
        <SELECT name=Precourse size=3 multiple>
          <OPTION value=99999 selected>無　　　　　　　　　　　　　　　　　　
        </SELECT>
        <BR>
        <!CENTER>
        <INPUT type=button name=select_precourse value="選擇先修科目" onclick="Add_Precourse_Win()"> 
        <INPUT type=button name=select_precourse2 value="重置" onclick="Clear_Precourse()"><BR>
        <SELECT name=prerequisite_logic>
          <OPTION value="AND" SELECTED>$PREREQUISITE_LOGIC{AND}
          <OPTION value="OR">$PREREQUISITE_LOGIC{OR}
        </SELECT>
      </TD>
    </TR>                              
  );

}
######################################################################################
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
      <INPUT type=checkbox name=gender_eq       $checked{gen}> 性別平等教育課程<BR>
      <INPUT type=checkbox name=env_edu          $checked{env}> 環境教育相關課程<BR>
    </TD>   
  );
}
######################################################################################
#####  Added 2009/05/05  Nidalap :D~
#####  暑期授課辦法修訂，暑期所開授之課程分為以下兩類： 
#####  第一類課程：經系（所、中心）課程委員會議審議通過之選修課程。
#####  第二類課程：曾開授之課程，以補救教學為原則。 
#####  請於暑期開排課系統增加選項，排課人員得勾選課程類別，
#####  以利後端課務系統計算最低開課人數、課程收費標準等計算教師鐘點資料。
sub Print_Remedy_Box
{
  #if( is_Summer() ) {
  if( is_Summer() and !is_GRA() ) { 	### 只作用於「一般生暑修」
    print qq( 
      <tr><th bgcolor=yellow>暑修課程類型</th>
        <td colspan=3>
          <SELECT name="remedy">
            <OPTION value="1" SELECTED>第一類課程：經系（所、中心）課程委員會議審議通過之選修課程
            <OPTION value="2">第二類課程：曾開授之課程，以補救教學為原則
          </SELECT>
        </TD>
      </TR>
    );
  }
}
######################################################################################
#####  顯示備註欄選項框框
sub Print_Note_Box
{
  print "<tr><th bgcolor=yellow>備註欄</th>";
  print "<th colspan=3><textarea name=note rows=3 cols=40>";
  if( $is_dept_serv == 1 )  {  print "限本系學生修讀.";  }
  print $Course{note};
  print "</textarea></th></tr>";
}
######################################################################################