#!/usr/local/bin/perl
#################################################################################################
#####  修改/刪除當學期已開科目 1/4
#####  顯示該年級開設科目等供點選到下頁，以帶出開課資料。
#####  Updates:
#####   199x/xx/xx 程式撰寫 by 不知道誰
#####   2010/10/25 語言中心可開通識外語課程功能 Nidalap :D~
#####   2015/04/15 因應文學院需求-委由各系實際執行開課，新增 $open_dept 變數  Nidalap :D~
#####   2015/05/26 切換年級按鈕改由 Show_Switch_Grade_Buttons() 處理 Nidalap :D~
#####	2016/05/31 「尚未開設學系服務學習課程」排除暑修系統  Nidalap :D~

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Open_Course.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Teacher.pm";
require $LIBRARY_PATH."Common_Utility.pm";

print("Content-type:text/html\n\n");
%Input = User_Input();
%Dept  = Read_Dept($Input{open_dept});
@teacher = Read_Teacher_File();

$Input{page} = 1  if( not defined $Input{page} );

#foreach $k (keys %Input) {
#  print("$k ---> $Input{$k}<br>");
#}

Check_Dept_Password($Input{open_dept}, $Input{password});

if( $Input{open_dept} eq $DEPT_LAN ) {					### 語言中心可開通識外語課
  if( $Input{dept_cd} eq $DEPT_CGE ) {
    $cge_lan_flag = 2;									###  語言中心，且選擇了通識外語課
  }else{
    $cge_lan_flag = 1;							  		###  語言中心，尚未選擇通識外語課
  }  
}elsif( $Input{open_dept} eq $DEPT_CGE ) {				### 通識中心不可選通識外語課
  $cge_lan_flag = 3;
}

#print "cge_lan_flag = $cge_lan_flag<BR>\n";

#print("superuser = $SUPERUSER<BR>");


$title = $SUB_SYSTEM_NAME . "開排課系統--修改當學期已開科目";
print Print_Open_Course_Header(\%Input, \%Dept, $title);									###  顯示上方系所年級等資訊
print Show_Switch_Grade_Buttons(\%Input, "Modify_Course.cgi");								###  顯示切換年級按鈕

print qq(
     </td></tr>
    </TABLE>

);

#foreach $k (keys %Input) {
#  print("$k --> $Input{$k}<br>");
#}

if( $TERM == 3 ) {
  $show_term = "";
}else{
  $show_term = join("", "第", $TERM, "學期");
}

if( $cge_lan_flag == 2 ) {  ### 語言中心可開通識外語課
  $Dept{id}	  = $DEPT_CGE;
  $Input{grade} = 1;
  @temp_course = Find_All_Course($DEPT_CGE,1,"");
  foreach $tc (@temp_course) {
	push(@course, $tc)  if( $$tc{id} =~ /^7102.../ );
#	print("push $$tc{id} _ $$tc{group} into course...<BR>\n");
  }
  $Input{grade} = "cge_lan";
}elsif( $cge_lan_flag == 3 ) {        ###  通識中心不可開通識外語課
    @temp_course = Find_All_Course($Input{dept_cd},$Input{grade},"");
    foreach $tc (@temp_course) {
      push(@course, $tc)  if( $$tc{id} !~ /^7102.../ );
    }
}else{
  @course = Find_All_Course($Input{dept_cd},$Input{grade},"","",$Input{open_dept});
}  
 
print qq(
  $YEAR年度$show_term擬開科目列表
  <FORM action="Modify_Course2.cgi" method="POST">
    <Input type=hidden name="dept_cd" value=$Input{dept_cd}>
	<Input type=hidden name="open_dept" value=$Input{open_dept}>
	<INPUT type=hidden name=cge_lan_flag value=$cge_lan_flag>
    <Input type=hidden name="grade" value=$Input{grade}>
    <Input type=hidden name="password" value=$Input{password}>
  <table border=1>
    <tr bgcolor=yellow>
      <th>刪除</th><th>修改</th><th>科目編號</th><th>班別</th>
      <th>科目屬性</th><th>開課教師</th><th>科目中文名稱</th>
    </tr>
);

my %cname = ( "1" => "必修",
              "2" => "選修",
              "3" => "通識",
              "4" => "學程"  );
$record_count = 0;
foreach $course (@course) {
  if( ($record_count>=($Input{page}*10-10)) and ($record_count<=($Input{page}*10-1)) ) {
    $course_id_and_group = $$course{id} . ":::" . $$course{group};
    %course = Read_Course($Input{dept_cd}, $$course{id}, $$course{group}, "");
    $is_dept_serv = 0;
    $is_dept_serv = 1  if( $$course{id} eq Get_Dept_Serv_Course_ID($Input{dept_cd}) );

    if( $is_dept_serv ) {
      print("<tr bgcolor=LIGHTGREEN>");
    }else{
      print("<tr>");
    }

    print qq(
        <td align=center>
          <INPUT name="choice" type="radio" value="DELETE:::$course_id_and_group">
        </td>
        <td align=center>
          <INPUT name="choice" type="radio" value="MODIFY:::$course_id_and_group">
        </td>
        <td align=center> $$course{id} </td>
        <td align=center> $$course{group} </td>
        <td align=center> $cname{$course{property}} </td>
        <td align=center> 
    );
    foreach $teacher( @{ $course{teacher} } ) {
       print $Teacher_Name{ $teacher },"<br>\n";
    }
    print qq(
        </td>
        <td align=left> $course{cname} </td>
       
      </tr>
    );
  }
#  print("<tr><td>$$course{id}</td></tr>");
  $record_count++;
}

$num_of_course = @course;
$next_page = $Input{page}+1;
$prev_page = $Input{page}-1;
print qq(
   </table>
   <Input type=submit value="確認">
  </FORM>  
);

#print("[page, num_of_course, record_count] = [$Input{page}, $num_of_course, $record_count]<BR>\n");
#foreach $c (@course) {
#  print("$c<BR>\n");
#  foreach $k (%{$c}) {
#    print("$k -> $$c{$k}<BR>\n");
#  }
#}
print("<table border=0><tr>");
if( $Input{page} > 1 ) {
  print qq(
    <td> 
    <FORM action=Modify_Course.cgi method=post>
      <Input type=hidden name=dept_cd value=$Input{dept_cd}>
	  <Input type=hidden name="open_dept" value=$Input{open_dept}>
      <Input type=hidden name=grade   value=$Input{grade}>
      <Input type=hidden name=password value=$Input{password}>
      <Input type=hidden name=page value=$prev_page>
      <Input type=submit value="顯示上十筆科目資料">
    </FORM>
    </td>
  );
}

if( $num_of_course>$Input{page}*10 ) {
  print qq( 
    <td>
    <FORM action=Modify_Course.cgi method=post>
      <Input type=hidden name=dept_cd value=$Input{dept_cd}>
	  <Input type=hidden name="open_dept" value=$Input{open_dept}>
      <Input type=hidden name=grade   value=$Input{grade}>
      <Input type=hidden name=password value=$Input{password}>
      <Input type=hidden name=page value=$next_page>
      <Input type=submit value="顯示下十筆科目資料">
    </FORM>
    </td>
  );
}
print("</tr></table>");

#####  如果尚未開設學系服務學習課程，顯示警示訊息 
$dept_serv_course_id = Get_Dept_Serv_Course_ID($Input{open_dept});
%serv_course = Read_Course($Input{dept_cd}, $dept_serv_course_id, "01");
if( !$IS_SUMMER and (is_Undergraduate_Dept($Input{dept_cd})) and (not is_Exceptional_Dept($Input{dept_cd})) and ($serv_course{ename} eq "") ) {
  print "<FONT color=RED>本學期尚未開設學系服務學習課程！</FONT>";
}

Links3($Input{dept_cd} ,$Input{grade}, $Input{password}, $Input{open_dept});
