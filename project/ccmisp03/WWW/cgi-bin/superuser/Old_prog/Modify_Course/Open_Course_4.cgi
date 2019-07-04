#!/usr/local/bin/perl

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Error_Message.pm";

my(@Date,$i);

$i=0;
%Input = User_Input();
if($Input{group} eq "") { $Input{group} = "01" };
%course=%Input;
$course{dept}=$Input{dept_cd};
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

TransToArray("teacher");  ## String trans to hash array
TransToArray("support_dept");
TransToArray("support_grade");
TransToArray("support_class");
TransToArray("ban_dept");
TransToArray("ban_grade");
TransToArray("ban_class");

Modify_Course("add",%course);

%temp=Read_Dept($Input{dept_cd});

print "Content-type: text/html","\n\n";
#print("$Input{password}\n");

print "
<html>
<head>
<title>新增學期開課[開課完成]- $temp{cname} </title>
</head>

<body bgcolor=white background=$GRAPH_URL"."ccu-sbg.jpg>
<center>";
print "
<font size=5 color=brown>下列科目開課完成</font>
<hr>
科目編號: $course{id}<br>
科目班別: $course{group}<br>
科目名稱: $course{cname}（$course{ename}） <br><br>
<hr>";
Links1($Input{dept_cd},$Input{grade},$Input{password},1);
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