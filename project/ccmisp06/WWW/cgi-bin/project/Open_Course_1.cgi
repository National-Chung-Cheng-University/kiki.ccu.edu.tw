#!/usr/local/bin/perl 
#################################################################################################
#####  開課畫面 1/4
#####  顯示年級/歷年開設科目等供點選到下頁，以帶出空白開課資料，或是某歷史課程。
#####  Updates:
#####   199x/xx/xx 程式撰寫 by 不知道誰
#####   2010/10/11 語言中心可開通識外語課程功能 Nidalap :D~
#####   2011/04/25 新增學系服務學習課程判斷與開課按鈕  Nidalap :D~
#####   2015/04/13 因應文學院需求-委由各系實際執行開課，新增 $open_dept 變數  Nidalap :D~
#####   2015/05/26 整合語言中心可開通識外語課，以及文學院委由各系開課功能 Nidalap :D~
#####              切換年級按鈕改由 Show_Switch_Grade_Buttons() 處理 Nidalap :D~
#####	2016/05/31 「尚未開設學系服務學習課程」排除暑修系統  Nidalap :D~

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Open_Course.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Password.pm";
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

## Begin of HTML ##
print "Content-type: text/html","\n\n";



#foreach $key (keys %Input) {
#  print("$key -> $Input{$key}<BR>\n");
#}

#foreach $key (keys %Input) {
#  print("$key ---> $Input{$key}<br>");
#}
#print "cge_lan_flag = $cge_lan_flag<BR>\n";

#print("Hello!!!");
#Check_Dept_Password($Input{dept_cd}, $Input{password});
#if( $cge_lan_flag == 2 ) {                                      ###  若是語言中心開通識外語課，讀取語言中心密碼檔 salt
#  Check_Dept_Password($DEPT_LAN, $Input{password});
#}else{                                                          ###  其餘一般情形：讀取該系所密碼檔 salt
  Check_Dept_Password($Input{open_dept}, $Input{password});
#}


$su_flag = "(SU)"  if($SUPERUSER == 1);

if( $TERM == 3 ) {
  $show_term = "";
}else{
  $show_term = join("", "第", $TERM, "學期");
}

$grade_show = ($Input{grade} eq "cge_lan") ? "通識外語課" : $Input{grade};

print Print_Open_Course_Header(\%Input, \%Dept, "新增當學期開課科目1/4 - 挑選科目");		###  顯示上方系所年級等資訊
print Show_Switch_Grade_Buttons(\%Input, "Open_Course_1.cgi");								###  顯示切換年級按鈕

print qq(
	  </tr>
   </table>
   <hr width=40%>
     <form action=Open_Course_2.cgi method=post>
      <input type=hidden name=dept_cd value=$Input{dept_cd}>
      <input type=hidden name=grade value=$Input{grade}>
      <input type=hidden name=password value="$Input{password}">
      <input type=hidden name=course_cd value=new>
	  <INPUT type=hidden name=cge_lan_flag value=$cge_lan_flag> 
	  <input type=hidden name=open_dept value=$Input{open_dept}>
      <input type=submit value=新增科目> 
     </form>   
  <FORM action=Open_Course_2.cgi method=post>
   <INPUT type=hidden name=cge_lan_flag value=$cge_lan_flag>   
   <input type=hidden name=password value=$Input{password}>
   <input type=hidden name=open_dept value=$Input{open_dept}>
   <table border=0>
   <tr>
   <th>歷年開課資料</th>
   <th>本學期開課科目</th>
   </tr>
   <td>
     <select name=course_cd size=10>
);
  my(@course,%Course);
  
  if( $cge_lan_flag == 2 ) {		### 語言中心可開通識外語課
 	#$Dept{id}	  = $DEPT_CGE;
	$Input{grade} = 1;
	@temp_course = Find_All_Course($DEPT_CGE,1,"history");
	foreach $tc (@temp_course) {
	  push(@course, $tc)  if( $$tc{id} =~ /^7102.../ );
	}
  }elsif( $cge_lan_flag == 3 ) {	###  通識中心不可開通識外語課
    @temp_course = Find_All_Course($Input{'dept_cd'},$Input{'grade'},"history");
    foreach $tc (@temp_course) {
      push(@course, $tc)  if( $$tc{id} !~ /^7102.../ );
    }
  }else{
    #print "searching for history [$Dept{id},$Input{grade}]";
    @course = Find_All_Course($Input{'dept_cd'},$Input{grade},"history");
#    print "course = " . @course;
  }  

#  foreach $course (@course) {
#    print("<OPTION value=$$course{id}> [$$course{id} $$course{group} ]");
#  }

  #####  顯示歷年開課資料的 OPTION
  foreach $course (@course) {
     if($$course{group} eq "01")  # 只顯示 01 班別的資料
     {
      %Course=Read_Course($Input{'dept_cd'},$$course{id},$$course{group},"history");
      print "<option value=$$course{id}>[$$course{id}]$Course{cname}\n";
     }
  }
#  @course = Find_All_Course($Dept{id},$Input{grade},"");
  @course = ();
  if( $cge_lan_flag == 2 ) {  ### 語言中心可開通識外語課
        @temp_course = Find_All_Course($Input{'dept_cd'},1,"");
        foreach $tc (@temp_course) {
          push(@course, $tc)  if( $$tc{id} =~ /^7102.../ );
        }
  }elsif( $cge_lan_flag == 3 ) {        ###  通識中心不可開通識外語課
    @temp_course = Find_All_Course($Input{'dept_cd'},$Input{grade},"");
    foreach $tc (@temp_course) {
      push(@course, $tc)  if( $$tc{id} !~ /^7102.../ );
    }
  }else{
    @course = Find_All_Course($Input{'dept_cd'},$Input{grade},"");
  }

  #print "dept id = " . $Dept{'id'} . "<BR>\n";
  
  foreach $course (@course) {
     if($$course{group} eq "01")  # 只顯示 01 班別的資料
     {
         #%Course=Read_Course($Input{'dept_cd'},$$course{id},$$course{group},"");
		 %Course=Read_Course($Input{'dept_cd'},$$course{id},$$course{group},"");
         print "<option value=\"$$course{id} new\">(本學期)[$$course{id}]$Course{cname}\n";
     }
  }
print "
     </select>
     </td>
     <td>";
         
print "
     <textarea cols=60 rows=10 readonly=readonly disabled=disabled>\n<<本欄位僅供參考,不必於本欄填選資料>>\n";

# my(@course,%Course);

#  @course = Find_All_Course($Dept{id},$Input{grade},"");

  foreach $course (@course) {
    %Course=Read_Course($Input{'dept_cd'}, $$course{id},$$course{group},"");
    print "[$$course{id}-$$course{group}]$Course{cname}\n";
  }
print "</textarea>
     </td>
     </tr></table>
     <input type=hidden name=dept_cd value=$Input{dept_cd}>
     <input type=hidden name=grade   value=$Input{grade}>
     <input type=submit name=submit value=以此科目開課> 
    </Form>";

#####  如果尚未開設學系服務學習課程，顯示警示訊息 
$dept_serv_course_id = Get_Dept_Serv_Course_ID($Dept{id});
%serv_course = Read_Course($Dept{id}, $dept_serv_course_id, "01");

if( !$IS_SUMMER and (is_Undergraduate_Dept($Dept{id})==1) and (not is_Exceptional_Dept($Dept{id})) and $serv_course{ename} eq "" ) {
  print "<FONT color=RED>本學期尚未開設學系服務學習課程！</FONT>";
  print "<FORM action='Open_Course_2.cgi' method=GET>
           <INPUT type=hidden name=cge_lan_flag value=$cge_lan_flag>
           <input type=hidden name=password value=$Input{password}>
           <INPUT type=hidden name=course_cd value=$dept_serv_course_id>
           <INPUT type=hidden name=dept_cd value=$Input{dept_cd}>
		   <input type=hidden name=open_dept value=$Input{open_dept}>
           <input type=hidden name=grade   value=$Input{grade}>
           <input type=submit name=submit value='開設本系服務學習課程'>
         </FORM>
         <HR>
  ";
}

$Dept{id} = $DEPT_LAN  if( $cge_lan_flag == 2 );  ### 若是語言中心開通識外語課，還原系所代碼為語言中心
#Links3($Dept{id},$Input{grade},$Input{password});
Links1($Input{dept_cd},$Input{grade},$Input{password}, "", $Input{open_dept});
print "
   </center>
   </body>
  </html>
";