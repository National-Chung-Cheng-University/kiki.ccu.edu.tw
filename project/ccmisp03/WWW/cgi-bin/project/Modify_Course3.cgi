#!/usr/local/bin/perl

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."Open_Course.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Teacher.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Error_Message.pm";

print("Content-type:text/html\n\n");
my(%Input,@Date,$i,@teacher);
%Input = User_Input();
$Input{dept_cd} = $Input{dept_id};
%input = %Input;
%dept  = Read_Dept($input{dept_id});
%cge = Read_Cge();
%original_course = Read_Course($input{dept_id}, $input{id}, $input{group}, "", "");

Check_Dept_Password($Input{dept_id}, $Input{password});
%classroom = Read_Classroom($Input{classroom});

Print_Title();

#foreach $k (keys %Input) {
#  print("$k ---> $Input{$k}<br>");
#}

Delete_Course_Data()  if( $Input{action} eq "delete" );
Modify_Course_Data()  if( $Input{action} eq "modify" );


###########################################################################
sub Print_Title()
{
  $action = "�ק�"  if( $input{action} eq "modify" );
  $action = "�R��"  if( $input{action} eq "delete" );
  print qq(
   <html><head><title>�}�ƽҨt��--$action���Ǵ��w�}���</title></head>
   <body background=../../Graph/ccu-sbg.jpg>
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

  $result=Delete_Course($input{id},$input{course_group},$input{dept_id});
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

  @selected_time = Find_Selected_Time(); 

  foreach $selected_time (@selected_time) {
    if($$selected_time{time} >= 1) {           ### �p�G�O�Ʀr�I�� -> 1 hr
      $total_selected_time ++;
    }else{                                     ### �p�G�O�^��I�� -> 1.5 hr
      $total_selected_time += 1.5;
    }
  }

  @teacher = Read_Teacher_File();
  $i=0;
  foreach $key(%Input)
  {
   if($Input{$key} eq "999")
   {
    $Date[$i++]=$key;
   }
  }

  if($Input{group} eq "") { $Input{group} = "01" };

  %temp=Read_Dept($Input{dept_id});
  ########  �D�޲z��, �Y������, �h ���פH�� == �Ыǳ̾A�e�q
  if( $SUPERUSER != 1 ) {                    ###  �D�޲z��
    if( $Input{principle} == 0 ) {           ###   �Y������
      $Input{number_limit_0} = $Input{number_limit_1} = $Input{number_limit2} = 0;
    }else{                                   ###   �Y������
      %original_classroom = Read_Classroom($original_course{classroom});
      if( ($original_classroom{size_fit} != $original_course{number_limit}) and ($original_course{principle}!=0) ) {
					     ###   �Y������޲z�̧�L���פH�� -> ���פH�Ƥ��@�ק�
        ($Input{number_limit_0}, $Input{number_limit_1}, $Input{number_limit_2})
          = Numeric_to_chars($original_course{number_limit});
      }else{ 		                     ###     �Y�����بõL�S���ק�L���פH�� -> ���פH�Ƹ�۱ЫǮe�q��
        ($Input{number_limit_0}, $Input{number_limit_1}, $Input{number_limit_2})
          = Numeric_to_chars($classroom{size_fit}); 
      }
    }
  }else{                                     ###  �޲z��
    ### (do nothing)
  }
  #########################################################################
  print qq(
    <html>
      <head><title>�s�W�Ǵ��}��[�}�ҽT�{]- $temp{cname}</title></head>
      <body bgcolor=white background=$GRAPH_URL/ccu-sbg.jpg>
        <center>
  );
  ###################################################################
  ($warning_count, $error_count, @error_message) =
                            Check_Open_Course_Restrictions("modify", %Input);

  if( $warning_count + $error_count > 0) {
    print("<FONT size=4 color=red>�t���ˬd�}�Ҹ�Ƶ��G�p�U</FONT><BR>\n");
    print("<TABLE border=0 size=85%>");
    print("  <TR><TD><OL>");
    foreach $error (@error_message) {
      print("<LI>$error");
      $temp++;
    }
    print("</TD></TR></TABLE>");
    if( $error_count > 0 ) {
      exit(1);
    }
  }
  
  ###################################################################  
#  $temp=join("*:::*",@Date);
  $temp = "";
  foreach $time (@selected_time) {
    if( $temp ne "" ) {
      $temp .= "*:::*";
    }
    $temp = $temp . $$time{week} . "_" . $$time{time};
  }
#  print(" temp = $temp<BR>\n");

  print "<hr>
  <form method=post action=Modify_Course4.cgi>
  <input type=hidden name=action value=\"modify\">
  <input type=hidden name=password value=$Input{password}>
  <input type=hidden name=grade value=$Input{grade}>
  <input type=hidden name=dept_id value=$Input{dept_id}>
  <input type=hidden name=date value=$temp>
  <table border=1>
  <tr>
  <th bgcolor=yellow>��ئW��(����)</th><th>";
   print "$Input{cname}<input type=hidden name=cname value=\"$Input{cname}\">";
  print "
  </th></tr>
  <tr>
  <th bgcolor=yellow>��ئW��(�^��)</th><th>";
   print "$Input{ename}<input type=hidden name=ename value=\"$Input{ename}\">";
  print "</th></tr>
  </table><br>
  <table border=1>
  <tr>
    <th colspan=2 rowspan=13>
  ";

  %time_table_cells = Format_Time(@selected_time);
  $time_table = Print_Timetable(%time_table_cells);
  print $time_table;

  print "
  </th>
  <th bgcolor=yellow>�}�Ҧ~��</th><th>";
  $g_string[1]="�@";
  $g_string[2]="�G";
  $g_string[3]="�T";
  $g_string[4]="�|";
  print "$g_string[$Input{grade}]�~��</th></tr><tr>
  <th bgcolor=yellow>��ؽs��:</th><th>";
   print "$Input{id} <input type=hidden name=course_id value=$Input{id}>";
  print "</th></tr><tr>
  <th bgcolor=yellow>�Z�O</th>
  <th>$Input{group}</th><input type=hidden name=group value=\"$Input{group}\">";
  print "</th>
  </tr>
  <tr>
  <th bgcolor=yellow>�½ҦѮv</th><th>";
   @temp = split(/\*:::\*/,$Input{Teacher});
   foreach $temp(@temp)
   {
    print $Teacher_Name{$temp},"<br>\n";
   }
   print ("<input type=hidden name=teacher value=$Input{Teacher}>");
   $Input{Teacher} = join(/ /,@temp);
  print "</th>
  </tr>
  <tr>
  <th bgcolor=yellow>�ɼ�:</th>
  <th>$Input{total_time}
  <input type=hidden name=total_time value=$Input{total_time}></th></tr>";
############################################################################
print qq(
  <tr><th bgcolor=yellow>����/������/�ѳ��Q�׮ɼ�:</th>
      <th>$Input{lab_time1}/$Input{lab_time2}/$Input{lab_time3}</th>
  <input type=hidden name=lab_time1 value=$Input{lab_time1}>
  <input type=hidden name=lab_time2 value=$Input{lab_time2}>
  <input type=hidden name=lab_time3 value=$Input{lab_time3}>
);
############################################################################

  print "
  <tr>
  <th bgcolor=yellow>�Ǥ�:</th>
 <th>$Input{credit}
  <input type=hidden name=credit value=$Input{credit}>";
####################################################################
  print "
  </th>
  </tr>
  <tr>
  <th bgcolor=yellow>����/���/�q��</th>
  <th>";
   if($Input{property}==1) { $name="����"; }
   if($Input{property}==2) { $name="���"; }
   if($Input{property}==3) { $name="�q��"; }
  print $name;
  print "<input type=hidden name=property value=$Input{property}>";
####################################################################
#  print qq(
#    </th></tr><tr>
#    <th bgcolor=yellow>�@��/�x�V/��|</th>
#    <th>
#  );
#   if($Input{suffix_cd}==0) { $suffix_cd="�@��"; }
#   if($Input{suffix_cd}==1) { $suffix_cd="�x�V"; }
#   if($Input{suffix_cd}==2) { $suffix_cd="��|"; }
#  print $suffix_cd;
#  print "<input type=hidden name=suffix_cd value=$Input{suffix_cd}>";
####################################################################

  print "
  </th>
  </tr>
  <tr>
  <th bgcolor=yellow>�W�ұЫ�:</th>
  <th>";
  print "[$classroom{id}]$classroom{cname}";
  print "<input type=hidden name=classroom value=\"$classroom{id}\">\n";
  print "</th>
  </tr>
  <tr><th bgcolor=yellow>�z���h</th><th>\n";
  my($p,@p_string);
  $p_string[0]="���ݿz��";
  $p_string[1]="�@���z��";
  $p_string[2]="�G���z��";
  print "$p_string[$Input{principle}]";
  print "<input type=hidden name=principle value=$Input{principle}>";
  print "</th></tr></table>\n";
  
  ## draw table for �Ƶ� ##
  print "<table border=1>";
  print "</select></th></tr>\n";
  print "<tr><th bgcolor=yellow>���פH��</th><th>\n";

  $temp=$Input{number_limit_2}*100+$Input{number_limit_1}*10+$Input{number_limit_0};
  if($temp ne "0") {
    print "$temp �H";
  }else{
    print "�L";
  }

  print "<input type=hidden name=number_limit value=$temp>\n";
  print "</th>";
  ### �O�d�ǥͦW�B ###
  print "<th bgcolor=yellow>�O�d�s�ͦW�B</th><th>\n";
  $temp=$Input{reserved_number_2}*100+$Input{reserved_number_1}*10+$Input{reserved_number_0};
  if($temp ne "0")
  {
   print "$temp �H";
  }
  else
  {
   print "�L";
  }
  print "<input type=hidden name=reserved_number value=$temp>\n";
  print "</th></tr>\n";
  print "<tr><th bgcolor=yellow rowspan=2>�䴩�t��</th><th rowspan=2>\n";
  my(@temp,$temp,%temp);
  if($Input{support_dept} ne "")
  {
   @temp=split(/\*:::\*/,$Input{support_dept});
   foreach $temp(@temp)
   {
    %dept=Read_Dept($temp);
    print $dept{cname},"<br>";
   }
  }
  else
  {
   print "�L";
  }
  print "</th><th bgcolor=yellow>�䴩�~��</th><th>\n";
  my(@g_string);
  $g_string[1]="�@";
  $g_string[2]="�G";
  $g_string[3]="�T";
  $g_string[4]="�|";
  if($Input{support_grade} ne "")
  {
   @temp=split(/\*:::\*/,$Input{support_grade});
   foreach $temp(@temp)
   {
    print $g_string[$temp],"�~��<br>";
   }
  }
  else
  {
   print "�L";
  }
  print "</th></tr><tr><th bgcolor=yellow>�䴩�Z��</th><th>\n";
  if($Input{support_class} ne "")
  {
   @temp=split(/\*:::\*/,$Input{support_class});
   foreach $temp(@temp)
   {
    print $temp,".";
   }
  }
  else
  {
   print "�L";
  }
  print "</th>";
  print "<input type=hidden name=support_dept value=$Input{support_dept}>\n";
  print "<input type=hidden name=support_grade value=$Input{support_grade}>\n";
  print "<input type=hidden name=support_class value=$Input{support_class}>\n";
  print "</th></tr>\n";
  ### �׭רt�� ###
  print "<tr><th bgcolor=YELLOW rowspan=2>�׭רt��</th><th rowspan=2>\n";
  if($Input{ban_dept} ne "")
  {
   @temp=split(/\*:::\*/,$Input{ban_dept});
   foreach $temp(@temp)
   {
    %dept=Read_Dept($temp);
    print $dept{cname},"<br>";
   }
  }
  else
  {
   print "�L";
  }
  print "</th><th bgcolor=YELLOW>�׭צ~��</th><th>\n";
  my(@g_string);
  $g_string[1]="�@";
  $g_string[2]="�G";
  $g_string[3]="�T";
  $g_string[4]="�|";
  if($Input{ban_grade} ne "")
  {
   @temp=split(/\*:::\*/,$Input{ban_grade});
   foreach $temp(@temp)
   {
    print $g_string[$temp],"�~��<br>";
   }
  }
  else
  {
   print "�L";
  }
  print "</th></tr><tr><th bgcolor=YELLOW>�׭ׯZ��</th><th>\n";
  if($Input{ban_class} ne "")
  {
   @temp=split(/\*:::\*/,$Input{ban_class});
   foreach $temp(@temp)
   {
    print $temp,".";
   }
  }
  else
  {
   print "�L";
  }
  print "</th>";
  print "<input type=hidden name=ban_dept value=$Input{ban_dept}>\n";
  print "<input type=hidden name=ban_grade value=$Input{ban_grade}>\n";
  print "<input type=hidden name=ban_class value=$Input{ban_class}>\n";
  print "</th></tr>\n";

####################  �䴩�q��  ####################################
$Input{support_cge_number} = $Input{support_cge_number_1} * 10 + $Input{support_cge_number_0};
print("<INPUT type=hidden name=support_cge_type value=$Input{support_cge_type}>\n");
print("<INPUT type=hidden name=support_cge_number value=$Input{support_cge_number}>\n");
print qq(
  <TR><TH bgcolor=YELLOW>�䴩�q�ѻ��</TH>
     <TH colspan=3>$cge{$Input{support_cge_type}}{sub_cge_id_show} $cge{$Input{support_cge_type}}{cge_name}</TH>
  </TR>
  <TR><TH bgcolor=YELLOW>�䴩�q�ѤH��</TH>
      <TH colspan=3>$Input{support_cge_number}</TH>
  </TR>
);
######################################################################
print qq(
  <TR>
    <TH bgcolor=YELLOW>���׬��</TH>
    <TD colspan=3>
);
if($Input{Precourse} !~ "99999") {
  @temp=split(/\*:::\*/,$Input{Precourse});
  print("<FONT size=-1>\n");
  foreach $temp(@temp) {
    ($predept, $precourse, $pregrade) = split(/:/, $temp);
    %dept_temp = Read_Dept($predept);
    %prerequisite_course = Read_Course($predept, $precourse, "01", "history");
    print("($dept_temp{cname2})($precourse)$prerequisite_course{cname} - $GRADE{$pregrade}<BR> ");
  }
} else {
  print "�L<BR>";
}
print("<input type=hidden name=Precourse value=$Input{Precourse}>\n");
print("($PREREQUISITE_LOGIC{$Input{prerequisite_logic}})<BR>\n");
print("<INPUT type=hidden name=prerequisite_logic value=$Input{prerequisite_logic}>");
print("</TD></TR>");
######################################################################
#print qq(
#  <TR>
#    <TH bgcolor=PINK>���׬���޿����Y</TH>
#    <TD colspan=3>$Input{prerequisite_logic}</TD>
#  </TR>
#  <INPUT type=hidden name=prerequisite_logic value=$Input{prerequisite_logic}>
#);

######################################################################

if ($Input{distant_learning} eq "on") {
  $flag_dis = "���Z�оǽҵ{";
  $Input{distant_learning} = 1;
}else{
  $flag_dis = "<FONT color=RED>�D</FONT>���Z�оǽҵ{";
  $Input{distant_learning} = 0;
}

if ($Input{english_teaching} eq "on") {
  $flag_eng = "���^�y�½�";
  $Input{english_teaching} = 1;
}else{
  $flag_eng = "<FONT color=RED>�D</FONT>���^�y�½�";
  $Input{english_teaching} = 0;
}

print qq(
  <TR>
    <TH bgcolor=YELLOW>�W�Ҥ覡</TH>
    <TD colspan=3>
      $flag_dis<BR>
      $flag_eng
    </TD>
  </TR>
  <INPUT type=hidden name=distant_learning value=$Input{distant_learning}>
  <INPUT type=hidden name=english_teaching value=$Input{english_teaching}>
);
########################################################################


  print "<tr><th bgcolor=yellow>�Ƶ���</th>";
  print "<th colspan=3>";
  print $Input{note};
  print "<input type=hidden name=note value=\"$Input{note}\">";
  print "</th></tr>
  </table>
  ";
  print "<p>
  <center>
  <input type=\"submit\" value=\"�T�w�ק��ظ��\">
  </form>";
  END:
  print "
  <form>
  <input type=button onclick=history.back() value=�^��W�@���ק���>
  </form>
  <hr>";
  Links1($Input{dept_id},$Input{grade},$Input{password});
  print "
  </center>
  </body>
  </html>";
  ## end of html file ##
}
############################################################################
#####  Find Selected_Time
#####  Ū���W�@���ҿ�����}�ҺI��
############################################################################
sub Find_Selected_Time
{
  my(@time, $i, $week, $time);
  $i = 0;
  foreach $key (sort %Input) {
    if($Input{$key} eq "999") {
#      print("$key<BR>\n");
      ($week, $time) = split(/_/, $key);
      $time[$i]{week} = $week;
      $time[$i]{time} = $time;
      $i++;
    }
  }
  return(@time);
}
############################################################################