#!/usr/local/bin/perl 

#########################################################################################
#####  Class_Menu.cgi
#####  開課主選單
#####  確認使用者帳密，並且提供各項功能連結。
#####  Updates:
#####    199?/??/?? Created
#####    2009/11/23 密碼改為 MD5 編碼，相關增修  Nidalap :D~
#####    2010/01/18 物理系需求：新增 21預警名單相關連結 Nidalap :D~
#####    2013/11/22 （只有通識中心）提供「通識課程與向度關聯表」 Nidalap :D~
#####    2015/04/13 因應文學院需求-委由各系實際執行開課，新增切換身份按鈕以及 $open_dept 變數  Nidalap :D~
#####    2015/04/21 新增「複製上學年同學期開課資料」按鈕 by Nidalap :D~

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."Checking_State_Map.pm";
require $LIBRARY_PATH."Open_Course.pm";

my(%Input,%Dept);
my($crypt_salt);

print "Content-type: text/html"."\n\n";
%Input= User_Input();

#foreach $key (keys %Input) {
#  print("$key -> $Input{$key}<BR>\n");
#}
if( !$Input{'open_dept'} ) {
  $Input{'open_dept'} =  $Input{'dept_cd'};
}

if( $Input{dept_cd} eq "dilimiter" ) {
  print qq(
    <CENTER>
      <FONT color=RED>
        <H1>就說了請勿選擇分隔線！</H1>
      </FONT>
      <HR>
      <A href="Login.cgi">回登入網頁</A>  
  );
  exit(0);  
}


if( $Input{crypt} ne "1" ) {			### 此變數註明傳進來的密碼是否已經加密
  if( $USE_MD5_PASSWORD == 1 ) {
    $Input{password} = md5_hex($Input{password});
  }else{
    $crypt_salt = Read_Crypt_Salt($Input{dept_cd}, "dept");
    $Input{password} = Crypt($Input{password}, $crypt_salt);
  }
}
Check_Dept_Password($Input{open_dept}, $Input{password});

#print("input pass = $Input{password}<br>"); 
#print("DEPT_NEED_TO_CHANGE_PASSWORD = $DEPT_NEED_TO_CHANGE_PASSWORD<BR>\n");


if((Check_Dept_State($Input{dept_cd}) == 0) and ($SUPERUSER ne "1")){
   SYS_NOT_ALLOWED();
   exit();
}

if($Input{grade} eq "") {$Input{grade}=1;}

%Dept=Read_Dept($Input{open_dept});
$su_flag = "(SU)"  if($SUPERUSER == 1);

## Begin of HTML ##

if( $TERM == 3 ) {
  $show_term = "";
}else{
  $show_term = join("", "第", $TERM, "學期");
}
print Print_Open_Course_Header(\%Input, \%Dept, "功能選單");

if( $DEPT_NEED_TO_CHANGE_PASSWORD == 1 ) {
  $html_pass		= Print_Button("Change_Password00.cgi", "更改密碼");
  print qq(
    <FONT color=RED>即日起本系統採用較為安全的密碼編碼方法。<BR>
    為了您的密碼安全，請更新開課密碼，不便之處，敬請見諒！<BR>
	$html_pass
    &nbsp;<P>
  );
}else{
  $html_open		= Print_Button("Open_Course_1.cgi", "新增當學期開課科目");
  $html_modify		= Print_Button("Modify_Course.cgi", "修改及刪除當學期已開科目"); 
  $html_show		= Print_Button("Show_Course_1.cgi", "查詢當學期已開科目"); 
  $html_print		= Print_Button("Print_Course.cgi", "列印當學期已開科目"); 
  $html_query		= Print_Button("../Query/Login.cgi", "查詢修課學生名單");
  $html_pass		= Print_Button("Change_Password00.cgi", "更改密碼"); 
  $html_view_stu_cou= Print_Button("View_Student_Course1.cgi", "檢視學生選課資料與畢業資格審查表"); 
  $html_view_change	= Print_Button("View_Change.cgi", "課程異動一覽表"); 
  $html_cou_alias	= Print_Button("Course_Alias.cgi", "課程別名對應檔維護");
  if( $Input{dept_cd} =~ /^1...$/ ) {
    if( $Input{dept_cd} != $Input{open_dept} ) {
	  $html_switch_dept	= Print_Button("Switch_Open_Dept.php?switch=0", "切換身份開設本系課程");
	}else{
	  $html_switch_dept	= Print_Button("Switch_Open_Dept.php?switch=1", "切換身份開設文學院課程");
	}
  }  
  if( $Input{dept_cd} eq $DEPT_PHYSICS ) {
    $html_early_warn	= Print_Button("Early_Warning_21_List.php", "物理系輔導學生選課機制");
  }
  if( $Input{dept_cd} eq $DEPT_EDU ) {
    $html_edu_stu_cou	= Print_Button("EDU_Stu_Courses.php", "檢視師培生選師培課程");
  }
  if( $Input{dept_cd} eq $DEPT_CGE ) {
    $html_CGE_map	= Print_Button("CGE_Category_Cour_Map.php", "通識課程與向度關聯表");
  }
}

  print qq(
    $html_open
	$html_modify
	$html_show
	$html_print
	$html_query
	$html_pass
	$html_view_stu_cou
	$html_view_change
	$html_cou_alias
	$html_switch_dept
	$html_early_warn
	$html_edu_stu_cou
	$html_CGE_map
	
    <IMG src="$GRAPH_URL/new1.gif">
    [<a href=$HOME_URL/UserGuide/project.doc>開課系統操作手冊</a>|
    <A href=$HOME_URL/UserGuide/project/faq.html><fontcolor=RED>疑難雜症請看這</font></font>]
    <br><br>
   <hr>
    [<A href="http://www.ccu.edu.tw">中正大學首頁</A>| 
     <A href=$HOME_URL>開排選課系統首頁</A>
    ]
    <br>
   </center>
   </body>
  </html>
);
############################################################################################

sub SYS_NOT_ALLOWED
{
  if($Input{grade} eq "") {$Input{grade}=1;}
  
  %Dept=Read_Dept($Input{dept_cd});
  $su_flag = "(SU)"  if($SUPERUSER == 1);

  Print_Header();  

  $html_show		= Print_Button("Show_Course_1.cgi", "查詢當學期已開科目");
  $html_print		= Print_Button("Print_Course.cgi", "列印當學期已開科目");
  $html_query		= Print_Button("../Query/Login.cgi", "查詢修課學生名單");
  $html_view_stu	= Print_Button("View_Student_Course1.cgi", "檢視學生選課資料與畢業資格審查表");
  $html_pass		= Print_Button("Change_Password00.cgi", "更改密碼");
  if( $Input{dept_cd} eq $DEPT_PHYSICS ) {
    $html_early_warn	= Print_Button("Early_Warning_21_List.php", "物理系輔導學生選課機制");
  }
  if( $Input{dept_cd} eq $DEPT_CGE ) {
    $html_CGE_map		= Print_Button("CGE_Category_Cour_Map.php", "通識課程與向度關聯表");
  }
  print qq(
    <font size=5 color=#cc4444>目前並非開課或課程異動時間！！<br>
    請向教學組確認開排課及課程異動時間，謝謝<br></font>
	  $html_show
	  $html_print
	  $html_query
	  $html_view_stu
	  $html_pass
	  $html_early_warn
	  $html_CGE_map  
    </center>
    </body>
    </html>
  );
}

#############################################################################################
sub Print_Button()
{
  my($target_prog, $text) = @_;
  my $html;

  $html =  qq( 
   <FORM action="$target_prog" method="POST">
     <INPUT type=hidden name=password value=$Input{password}>
     <INPUT type=hidden name=id value=$Input{'dept_cd'}>
     <INPUT type=hidden name=dept_id value=$Input{'dept_cd'}>
     <INPUT type=hidden name=dept_cd value=$Input{'dept_cd'}>
	 <INPUT type=hidden name=open_dept value=$Input{open_dept}>
     <INPUT type=hidden name=grade value=$Input{grade}>
     <INPUT type=submit value="$text">
   </FORM>
  );
  return $html;
}
