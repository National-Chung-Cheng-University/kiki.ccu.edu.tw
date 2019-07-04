#!/usr/local/bin/perl
#############################################################################
#####  Open_Course_4.cgi
#####  �t�Ҷ}��(�̫�g�J���)
#############################################################################
require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Error_Message.pm";

my(@Date,$i);

$i=0;
%Input = User_Input();
if($Input{group} eq "") { $Input{group} = "01" };
%course=%Input;
$course{dept}=$Input{dept_cd};

Check_SU_Password($Input{password}, "dept", $Input{dept_cd});

@Date=split(/\*:::\*/,$Input{date});
$i=0;
foreach $temp(@Date)
{
 ($t1,$t2)=split(/_/,$temp);
 $course{time}[$i]{week}=$t1;
 $course{time}[$i++]{time}=$t2;
}
## �S����J�Юv���..�]�w���Юv���w
if($course{teacher} eq "")
{
 $course{teacher} = "99999"; 
}

## multiple input ����ƻݭn��� ##
foreach $key(%course)
{
 $course{$key} =~ s/\*:::\*/ /g;
}

# $course{cname} =~ s/��/"/g;  ### �����ഫ�|�ɭP��������r�X��(4105790_01)
# $course{ename} =~ s/��/"/g;  ### �G��o�@�q���N���� (2003/08/20, Nidalap :D~)

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
$course{prerequisite_logic} = $Input{prerequisite_logic};

Modify_Course("add",%course);

%temp=Read_Dept($Input{dept_cd});

print "Content-type: text/html","\n\n";
#print("$Input{password}\n");

print qq(
  <html>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <head><title>�s�W�Ǵ��}��[�}�ҧ���]- $temp{cname} </title></head>
    <body bgcolor=white background=$GRAPH_URL/ccu-sbg.jpg>
      <center>
);
print qq(
  <font size=5 color=brown>�U�C��ض}�ҧ���</font>
  <hr>
  ��ؽs��: $course{id}<br>
  ��دZ�O: $course{group}<br>
  ��ئW��: $course{cname}�]$course{ename}�^ <br><br>
  <hr>
);

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