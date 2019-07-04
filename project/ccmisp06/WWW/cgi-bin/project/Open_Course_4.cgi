#!/usr/local/bin/perl
#############################################################################
#####  Open_Course_4.cgi
#####  系所開課(最後寫入資料)
#####   2009/05/05 加入暑修課程類型 remedy 欄位 (1為一般，2為補救)
#####   2010/03/19 加入 教師專長與授課科目是否符合 $s_match 欄位 Nidalap :D~
#####   2010/10/11 語言中心可開通識外語課程功能 Nidalap :D~
#####   2012/01/12 加入要求確認功能(目前只有教師/教室衝堂)  Nidalap :D~
#####   2015/04/14 因應文學院需求-委由各系實際執行開課，新增切換身份按鈕以及 $open_dept 變數  Nidalap :D~
#############################################################################
require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Open_Course.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Common_Utility.pm";

my(@Date,$i);

$i=0;
%Input = User_Input();
if($Input{group} eq "") { $Input{group} = "01" };
%course=%Input;
$course{dept}=$Input{dept_cd};

#foreach $k (keys %Input) {
#  print("$k --> $Input{$k}<br>\n");
#}

#Check_SU_Password($Input{password}, "dept", $Input{dept_cd});
$cge_lan_flag = $Input{"cge_lan_flag"};

if( $cge_lan_flag == 2 ) {                                      ###  若是語言中心開通識外語課，讀取語言中心密碼檔 salt
  Check_Dept_Password($DEPT_LAN, $Input{password});
}else{                                                          ###  其餘一般情形：讀取該系所密碼檔 salt
  Check_Dept_Password($Input{open_dept}, $Input{password});
}

@Date=split(/\*:::\*/,$Input{date});
$i=0;
foreach $temp(@Date)
{
 ($t1,$t2)=split(/_/,$temp);
 $course{time}[$i]{week}=$t1;
 $course{time}[$i++]{time}=$t2;
}
## 沒有輸入教師資料..設定為教師未定
if($course{teacher} eq "")
{
 $course{teacher} = "99999"; 
}

## multiple input 的資料需要更改 ##
foreach $key(%course)
{
 $course{$key} =~ s/\*:::\*/ /g;
}

# $course{cname} =~ s/」/"/g;  ### 做此轉換會導致部份中文字出錯(4105790_01)
# $course{ename} =~ s/」/"/g;  ### 故把這一段取代取消 (2003/08/20, Nidalap :D~)

TransToArray("teacher");  ## String trans to hash array
TransToArray("support_dept");
TransToArray("support_grade");
TransToArray("support_class");
TransToArray("ban_dept");
TransToArray("ban_grade");
TransToArray("ban_class");
#TransToArray("prerequisite_course");
@temp = split(/\*:::\*/, $Input{Precourse});
for($i=0; $i<@temp; $i++) {
  ($predept, $precourse, $pregrade) = split(/:/,$temp[$i]);
  $course{prerequisite_course}[$i]{dept}	= $predept;
  $course{prerequisite_course}[$i]{id}		= $precourse;
  $course{prerequisite_course}[$i]{grade}	= $pregrade;
}
$course{prerequisite_logic}	= $Input{prerequisite_logic};
$course{s_match}		= $Input{s_match};

#Modify_Course("add",%course);			###  實際將開課資料寫入

%temp=Read_Dept($Input{open_dept});

print "Content-type: text/html","\n\n";
#print("$Input{password}\n");

#####  若前一頁要求確認卻沒有確認，到此為止(請回上頁確認  Added 2012/01/12
if( ($Input{"need_confirmation"} == 1) and ($Input{"yes_i_agree"} ne "on") ) {
  print qq'
    <html>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <head><title>新增學期開課[開課尚未完成]- $temp{cname} </title></head>
      <body bgcolor=white background=$GRAPH_URL/ccu-sbg.jpg>
        <center>
        <FONT color=RED>
          請回上頁點選「好的，我知道了」！<P>
          <A href="javascript:history.back()">回上頁</A>
  ';
  exit();
}

#Print_Hash(%course);
Modify_Course("add",%course);                   ###  實際將開課資料寫入

print qq(
  <html>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <head><title>新增學期開課[開課完成]- $temp{cname} </title></head>
    <body bgcolor=white background=$GRAPH_URL/ccu-sbg.jpg>
      <center>
);
print qq(
  <font size=5 color=brown>下列科目開課完成</font>
  <hr>
  科目編號: $course{id}<br>
  科目班別: $course{group}<br>
  科目名稱: $course{cname}（$course{ename}） <br><br>
  <hr>
);

$Input{open_dept} = $DEPT_LAN  if( $Input{cge_lan_flag} == 2 );  ### 若是語言中心開通識外語課，還原系所代碼為語言中心

#Links1($Input{open_dept},$Input{grade},$Input{password},1);
Links1($Input{dept_cd},$Input{grade},$Input{password}, 1, $Input{open_dept});

print "</body></html> ";

#foreach $k (keys %Input) {
#  print($k -> $Input{$k}<br>");
#}
## end of html file ##


## sub function TransToArray ##

sub TransToArray
{
 my($key);
 ($key)=@_;
 @{ $course{$key} } = split(/\s+/,$course{$key});
}