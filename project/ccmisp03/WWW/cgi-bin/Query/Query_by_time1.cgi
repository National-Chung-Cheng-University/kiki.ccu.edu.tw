#!/usr/local/bin/perl
########################################################################
#####  Query_by_time1.cgi
#####  �i���}�Ҹ�Ƭd��
#####  �H�t��, �}�Ҹ`���ɶ�, ��ئW��, �Юv�m�W������, �j�M��Ǵ��}�Ҹ��.
#####  Last Update:
#####   2004/03/02
#####	2008/06/03  �s�W��ئW�ٻP�Юv�m�W�d�߿ﶵ.  Nidalap :D~
########################################################################
print "Content-type: text/html","\n\n";

require "../library/Reference.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Open_Course.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Session.pm";


%Input = User_Input();
#Check_SU_Password($Input{password}, "dept", $Input{dept_cd});
if( $Input{session_id} ne "" ) {					###  �p�G���n�J�L�F, Ū���ӤH���
  ($Input{id}, $Input{password}, $login_time, $ip, $add_course_count) = Read_Session($Input{session_id}, 1);
  if($Input{get_my_table} == 1) {					###  Ū���ӤH�Ű�`��
    @my_table = Get_My_Table($Input{id}, "free");
  }
}

#foreach $cell (@my_table) {
#  print("my table=$cell<BR>\n");
#}

@dept = Find_All_Dept();

print qq(
  <SCRIPT language=JAVASCRIPT>
   function Select_Time(mode) {
     if( mode == 1 ) {						//  ��ܩҦ��`��
       for(var i = 0; i < document.form1.length; i++)  {
         if (document.form1.elements[i].type == "checkbox" ) {
           document.form1.elements[i].checked = true;
         }
       }
     }else if( mode == 2 ) {					//  �����Ҧ��`��
       for(var i = 0; i < document.form1.length; i++)  {                              
         if (document.form1.elements[i].type == "checkbox" ) {
           document.form1.elements[i].checked = false; 
         } 
       }
     }else if( mode == 3 ) {					//  ��ܩҦ��ڪ��Ű�(���n�J)
       for(var i = 0; i < document.form1.length; i++)  {
         if (document.form1.elements[i].type == "checkbox" ) {
           document.form1.elements[i].checked = document.form1.elements[i].defaultChecked;
         }
       }
     }
   }
  </SCRIPT>

);

print qq(
  <HEAD>
    <TITLE>�i���}�Ҹ�Ƭd�� -- �п�ܱ���</TITLE>
    <LINK rel="stylesheet" type="text/css" href="$HOME_URL/font.css">
  </HEAD>
  <body bgcolor=white background=$GRAPH_URL/ccu-sbg.jpg>
  <center>
    <SPAN class="title1">�i���}�Ҹ�Ƭd��</SPAN><BR>
    <IMG src=$TITLE_LINE>
  <form id=form1 name=form1 method=post action=Query_by_time2.cgi>
    <input type=hidden name=session_id value=$Input{session_id}>
  <TABLE border=0 class="font1">
    <TR><TD valign=TOP align=CENTER rowspan=2>
    <FONT size=2>
    �п�ܾǨt<FONT color=RED>(����)</FONT><BR>(��Ctrl�i�ƿ�):<BR>
    <SELECT name=dept multiple size=27>
);
foreach $dept (@dept) {
  %dept = Read_Dept($dept);
  print("  <OPTION value=\"$dept\">$dept{cname2}\n");  
}
print qq(
    </SELECT>
  </TD>
  <TD valign=TOP>
);

if( $Input{session_id} ne "" ) {							###  �p�G���� session id �i��
  print qq(<INPUT type=hidden name=session_id value="$session_id>");						###  �h�ǥX�h
  $select_mine = " | <INPUT type=RADIO name=select_time_mode value=select_mine CHECKED";
  $select_mine .= " onClick=javascript:Select_Time(3)>��ܩҦ��ڪ��Ű�";					###  �h�i��ܦ��ﶵ
}
print qq(
    </CENTER>
        <INPUT type=RADIO name=select_time_mode value=select_all onClick=javascript:Select_Time(1)>��ܩҦ��`�� |
        <INPUT type=RADIO name=select_time_mode value=deselect_all onClick=javascript:Select_Time(2)>�����Ҧ��`��
        $select_mine
        <BR>
        <INPUT type=RADIO name=query_type value=1 CHECKED>�d�ߩҦ� "�u" �ϥΨ�o�Ǯɬq�����<BR>
        <INPUT type=RADIO name=query_type value=2>�d�ߩҦ��ϥΨ�o�Ǯɬq�����
  </TD>
  <TD>
    ��ئW��: <INPUT name="course_cname"><BR>
    �Юv�m�W: <INPUT name="teacher"><BR>
  </TD>
  </TR>
  <TR>
    <TD colspan=2>
    &nbsp;<P>
    �п�ܮɬq<FONT color=RED>(����)</FONT>:
  );
  
Print_Timetable_Select(@my_table);
  
      
print qq(    
    </TR>
  </TABLE>
  <p>
  <center>
  <input type="submit" value="�e�X���">
  <input type="reset" value="���s��g">
  </form>
  <HR>
  </CENTER>
  <LI><FONT color=GREEN size=-1>��ئW�ٻP�Юv�m�W������, �Ȥ������U�Φr��</FONT>
  </body>
  </html>
);
 
######################################################################################
