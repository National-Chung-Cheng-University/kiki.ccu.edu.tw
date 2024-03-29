#!/usr/local/bin/perl

require "../../../LIB/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Error_Message.pm";

print("Content-type:text/html\n\n");
%input = User_Input();
%dept  = Read_Dept($input{dept_id});
Check_Dept_Password($input{dept_id}, $input{password});

Print_Title();
Delete_Course_Data()  if( $input{action} eq "delete" );
Modify_Course_Data()  if( $input{action} eq "modify" );

#foreach $k (keys %input) {
#  print("$k ---> $input{$k}<br>");
#}

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
  $course{id}		=	$input{course_id};
  $course{dept}		=	$input{dept_id};
  $course{cname}	=	$input{cname};
  $course{ename}	=	$input{ename};
  $course{total_time}	=	$input{total_time};
  $course{credit}	=	$input{credit};
  $course{classroom}	=	$input{classroom};
  $course{property}	=	$input{property};
  $course{grade}	=	$input{grade};
  $course{principle}	=	$input{principle};
  $course{group}	=	$input{group};
  $course{number_limit}	=	$input{number_limit};
  $course{reserved_number} =	$input{reserved_number};
  $course{note}		=	$input{note};
  $temp	= $input{Teacher};
     @{$course{teacher}} = split(/\*:::\*/, $temp);
  $temp	= $input{support_dept};
     @{$course{support_dept}} = split(/\*:::\*/, $temp);
  $temp = $input{support_grade};
     @{$course{support_grade}} = split(/\*:::\*/, $temp);
  $temp = $input{support_class};
     @{$course{support_class}} = split(/\*:::\*/, $temp);
  $temp = $input{ban_dept};
     @{$course{ban_dept}} = split(/\*:::\*/, $temp);
  $temp = $input{ban_grade};
     @{$course{ban_grade}} = split(/\*:::\*/, $temp);
  $temp = $input{ban_class};
     @{$course{ban_class}} = split(/\*:::\*/, $temp);
  $i=0;
  my @day = split(/\*:::\*/, $input{date});
  foreach $day (@day) {
    ($week, $time) = split(/_/, $day);
    $course{time}[$i]{week} = $week;
    $course{time}[$i]{time} = $time;
    $i++;
  } 

  $result = Modify_Course("modify", %course);  
#  print("result = $result");
  if  ( $result eq "TRUE" ) {
    print("<font color=red>本科目已成功\修改!</font>");
  }elsif  ( $result eq "NOT_FOUND" ) {
    print("<font color=red>系統發現錯誤: 科目資料不存在!</font>");
  }
  print("<p>");
  Links3($input{dept_id} ,$input{grade}, $input{password} );
}
