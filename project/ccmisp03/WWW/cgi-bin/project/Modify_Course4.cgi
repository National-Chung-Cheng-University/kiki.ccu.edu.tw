#!/usr/local/bin/perl
###########################################################################
#####  Modify_Course4.cgi
#####  �ק�}�Ҹ��(�̫�g�J���)
###########################################################################
require "../library/Reference.pm";
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
  $action = "�ק�"  if( $input{action} eq "modify" );
  $action = "�R��"  if( $input{action} eq "delete" );  
  print qq(
   <html><head><title>�}�ƽҨt��--$action���Ǵ��w�}���</title></head>
   <body background=$GRAPH_URL/ccu-sbg.jpg>
     <center>
      <br>
      <table border=0 width=40%>
       <tr>
        <td>�t�O:</td><td> $dept{cname} </td>
        <td>�~��:</td><td> $input{grade} </td></tr><tr>
        <th colspan=4><H1>$action���Ǵ��w�}���</H1></th>
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
    print("<font color=red>����ؤw���\\�R��!</font>");
  }elsif  ( $result eq "NOT_FOUND" ) {
    print("<font color=red>�t�εo�{���~: ��ظ�Ƥ��s�b!</font>");
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
  $course{lab_time1}	=	$input{lab_time1};   ### Apr,2000  Nidalap
  $course{lab_time2}    =       $input{lab_time2};   ### Apr,2000  Nidalap
  $course{lab_time3}    =       $input{lab_time3};   ### Apr,2000  Nidalap
  $course{credit}	=	$input{credit};
  $course{classroom}	=	$input{classroom};
  $course{property}	=	$input{property};
  $course{grade}	=	$input{grade};
  $course{principle}	=	$input{principle};
  $course{group}	=	$input{group};
  $course{number_limit}	=	$input{number_limit};
  $course{reserved_number} =	$input{reserved_number};
#  $course{suffix_cd}	=	$input{suffix_cd};      ### Apr,2000 Nidalap
  $course{support_cge_type} =	$input{support_cge_type};  ### Nov07,2000
  $course{support_cge_number} =	$input{support_cge_number}; ## Nov07,2000 Nidalap
  $course{distant_learning} =	$input{distant_learning};	## 2006/11/14 Nidalap :D~
  $course{english_teaching} =	$input{english_teaching};	## 2006/11/14 Nidalap :D~
  $course{note}		=	$input{note};
  $temp	= $input{teacher};
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
#  $temp = $input{prerequisite_course};
#     @{$course{prerequisite_course}} = split(/\*:::\*/, $temp);

  $i=0;
  my @day = split(/\*:::\*/, $input{date});
  foreach $day (sort @day) {
    ($week, $time) = split(/_/, $day);
    $course{time}[$i]{week} = $week;
    $course{time}[$i]{time} = $time;
    $i++;
  } 
  @temp = split(/\*:::\*/, $input{Precourse});
  for($i=0; $i<@temp; $i++) {
    ($predept, $precourse, $pregrade) = split(/:/,$temp[$i]);
    $course{prerequisite_course}[$i]{dept}        = $predept;
    $course{prerequisite_course}[$i]{id}          = $precourse;
    $course{prerequisite_course}[$i]{grade}       = $pregrade;
  }
  $course{prerequisite_logic} = $input{prerequisite_logic};

  $result = Modify_Course("modify", %course);  
#  print("result = $result");
  if  ( $result eq "TRUE" ) {
    print("<font color=red>����ؤw���\\�ק�!</font>");
  }elsif  ( $result eq "NOT_FOUND" ) {
    print("<font color=red>�t�εo�{���~: ��ظ�Ƥ��s�b!</font>");
  }
  print("<p>");
  Links3($input{dept_id} ,$input{grade}, $input{password} );
}