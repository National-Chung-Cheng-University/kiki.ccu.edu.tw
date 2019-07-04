#!/usr/local/bin/perl

printf("Content-type:text/html\n\n");
require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Select_Course.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Session.pm";

my(%Student,%Dept);

%Input=User_Input();
($Input{id}, $Input{password}, $login_time, $ip) = Read_Session($Input{session_id});
#print("session_id, id, pass = $Input{session_id}, $Input{id}, $Input{password}<BR>"); 

%Student=Read_Student($Input{id});
%Dept=Read_Dept($Student{dept});
@MyCourse=Course_of_Student($Student{id});

my($HEAD_DATA)=Head_of_Individual($Student{name},$Student{id},$Dept{cname},$Student{grade},$Student{class});
my($LINK)=Select_Course_Link($Input{id},$Input{password});

print << "End_of_HTML"
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <TITLE>�ק�K�X</TITLE>
</head>
<body background="$GRAPH_URL./ccu-sbg.jpg">
<center>
  $HEAD_DATA
  <hr>
  <FORM action="Change_Password01.php" method=POST>
    <TABLE border=0 width=50%>
      <TR><TD>
        �Y��_��Ҩt�αK�X�N�P���y�t�αK�X��X, �z�b�o�̧�諸�K�X,
        �N�|�P�ɧ�s�z�b��Өt�ΤW���K�X.
        ���T�O�N�Өt�ΥD�ʳq���z���n�T��, �ЦP�ɽT�{ email �H�c!
      </TD></TR>
    </TABLE>
    <P>
    <TABLE border=0>
      <TR><TD>�п�J�z��Ӫ��K�X:</TD>
          <TD><INPUT type=password name="old_password"></TD></TR>
      <TR><TD>�п�J�z���s�K�X:</TD>
          <TD><INPUT type=password name="new_password"></TD></TR>
      <TR><TD>�нT�{�s���K�X:</TD>
          <TD><INPUT type=password name="check_password"></TD></TR>
      <TR><TD>
    </TABLE>
    <INPUT type=hidden name="session_id" value="$Input{session_id}">
    <INPUT type="submit" value="�T�w���"><p>
  </FORM>
  $LINK
End_of_HTML
