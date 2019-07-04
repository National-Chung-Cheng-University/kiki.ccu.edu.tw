#!/usr/local/bin/perl 
#########################################################################################
#####  查詢當學期已開科目 1/2
#####  顯示年級供點選，以及該系所該年級下當學期已開設課程供下拉
#####  Updates:
#####   199x/xx/xx 程式撰寫 by 不知道誰
#####   2010/10/11 語言中心可開通識外語課程功能 Nidalap :D~
#####   2015/04/16 因應文學院需求-委由各系實際執行開課，新增 $open_dept 變數  Nidalap :D~
#####   2015/05/26 切換年級按鈕改由 Show_Switch_Grade_Buttons() 處理 Nidalap :D~
#####	2016/05/31 「尚未開設學系服務學習課程」排除暑修系統  Nidalap :D~

print "Content-type: text/html","\n\n";

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Open_Course.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Common_Utility.pm";

my(%Input,%Dept);

%Input=User_Input();
%Dept=Read_Dept($Input{open_dept});

if( $Input{open_dept} eq $DEPT_LAN ) {					### 語言中心可開通識外語課
  if( $Input{dept_cd} eq $DEPT_CGE ) {
    $cge_lan_flag = 2;									###  語言中心，且選擇了通識外語課
  }else{
    $cge_lan_flag = 1;							  		###  語言中心，尚未選擇通識外語課
  }  
}elsif( $Input{open_dept} eq $DEPT_CGE ) {				### 通識中心不可選通識外語課
  $cge_lan_flag = 3;
}

#foreach $k (keys %Input) {
#  print("$k ---> $Input{$k}<br>");
#}
 
$grade_show = ($Input{grade} eq "cge_lan") ? "通識外語課" : $Input{grade};

if( $TERM == 3 ) {
  $show_term = "";
}else{
  $show_term = join("", "第", $TERM, "學期");
}

## Begin of HTML ##

$title = $SUB_SYSTEM_NAME . "開排課系統-- 查詢當學期已開科目";
print Print_Open_Course_Header(\%Input, \%Dept, $title);									###  顯示上方系所年級等資訊
print Show_Switch_Grade_Buttons(\%Input, "Show_Course_1.cgi");								###  顯示切換年級按鈕

if( $cge_lan_flag == 2 ) {  ### 語言中心可開通識外語課
  $Dept{id}       = $DEPT_CGE;
  $Input{grade} = 1;
}

print qq(
    </tr>
   </table>
   <hr width=40%><br>
    <Form action=Show_Course_2.cgi method=post>
    <input type=hidden name=password value=$Input{password}>\n
);
  
 my(@course,%Course);

#  @course = Find_All_Course($Dept{id},$Input{grade},"");
  if( $cge_lan_flag == 2 ) {  ### 語言中心可開通識外語課
        $Dept{id}         = $DEPT_CGE;
        $Input{grade} = 1;
        @temp_course = Find_All_Course($DEPT_CGE,1);
        foreach $tc (@temp_course) {
          push(@course, $tc)  if( $$tc{id} =~ /^7102.../ );
        }
  }elsif( $cge_lan_flag == 3 ) {        ###  通識中心不可開通識外語課
    @temp_course = Find_All_Course($Dept{id},$Input{grade},"");
    foreach $tc (@temp_course) {
      push(@course, $tc)  if( $$tc{id} !~ /^7102.../ );
    }
  }else{
    @course = Find_All_Course($Input{dept_cd},$Input{grade},"","", $Input{open_dept});
  }

  $temp=@course;
if($temp ne 0)
{
 print "<font size=4>";
 print "共有 $temp 筆開課資料<br><br>\n";
 print "請選擇欲查詢之科目</font><br><br><br>\n";
 print "<select name=id_group>";
  foreach $course (@course) {
 %Course=Read_Course($Input{dept_cd},$$course{id},$$course{group},"");
 print "<option value=$$course{id}_$$course{group}>
        [$$course{id}-$$course{group}]$Course{cname}\n";
 
 
 }
 print "</select>"; 
 print "<br><br>
     <input type=hidden name=dept_cd value=$Input{dept_cd}>
	 <input type=hidden name=open_dept value=$Input{open_dept}>
     <input type=hidden name=grade   value=$Input{grade}>
     <input type=submit name=submit value=顯示此科目資料> 
    </Form>";

}
else
{ print "沒有任何開課資料<br>"; }

#####  如果尚未開設學系服務學習課程，顯示警示訊息
$dept_serv_course_id = Get_Dept_Serv_Course_ID($Input{open_dept});
%serv_course = Read_Course($Dept{id}, $dept_serv_course_id, "01");
#if( (not is_Exceptional_Dept($Dept{id})) and $serv_course{ename} eq "" ) {
if( !$IS_SUMMER and (is_Undergraduate_Dept($Input{open_dept})==1) and (not is_Exceptional_Dept($Input{open_dept})) and ($serv_course{ename} eq "") ) { 

  print "<FONT color=RED>本學期尚未開設學系服務學習課程！</FONT>";
}

print "<hr width=40%><br><br>";
if( $Input{cge_lan_flag} == 2 ) { $Input{dept_cd} = $DEPT_LAN;  $Input{grade} = 1}  ### 若是語言中心開通識外語課，還原系所代碼為語言中心

Links1($Input{dept_cd},$Input{grade},$Input{password},"",$Input{open_dept});
print "
   </center>
   </body>
  </html>
";