#!/usr/local/bin/perl
########################################################################
#####  Query_by_time1.cgi
#####  進階開課資料查詢
#####  以系所, 開課節次時間, 科目名稱, 教師姓名等條件, 搜尋當學期開課資料.
#####  Last Update:
#####   2004/03/02
#####	2008/06/03  新增科目名稱與教師姓名查詢選項.  Nidalap :D~
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
if( $Input{session_id} ne "" ) {					###  如果有登入過了, 讀取個人資料
  ($Input{id}, $Input{password}, $login_time, $ip, $add_course_count) = Read_Session($Input{session_id}, 1);
  if($Input{get_my_table} == 1) {					###  讀取個人空堂節次
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
     if( mode == 1 ) {						//  選擇所有節次
       for(var i = 0; i < document.form1.length; i++)  {
         if (document.form1.elements[i].type == "checkbox" ) {
           document.form1.elements[i].checked = true;
         }
       }
     }else if( mode == 2 ) {					//  取消所有節次
       for(var i = 0; i < document.form1.length; i++)  {                              
         if (document.form1.elements[i].type == "checkbox" ) {
           document.form1.elements[i].checked = false; 
         } 
       }
     }else if( mode == 3 ) {					//  選擇所有我的空堂(須登入)
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
    <TITLE>進階開課資料查詢 -- 請選擇條件</TITLE>
    <LINK rel="stylesheet" type="text/css" href="$HOME_URL/font.css">
  </HEAD>
  <body bgcolor=white background=$GRAPH_URL/ccu-sbg.jpg>
  <center>
    <SPAN class="title1">進階開課資料查詢</SPAN><BR>
    <IMG src=$TITLE_LINE>
  <form id=form1 name=form1 method=post action=Query_by_time2.cgi>
    <input type=hidden name=session_id value=$Input{session_id}>
  <TABLE border=0 class="font1">
    <TR><TD valign=TOP align=CENTER rowspan=2>
    <FONT size=2>
    請選擇學系<FONT color=RED>(必填)</FONT><BR>(按Ctrl可複選):<BR>
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

if( $Input{session_id} ne "" ) {							###  如果有傳 session id 進來
  print qq(<INPUT type=hidden name=session_id value="$session_id>");						###  則傳出去
  $select_mine = " | <INPUT type=RADIO name=select_time_mode value=select_mine CHECKED";
  $select_mine .= " onClick=javascript:Select_Time(3)>選擇所有我的空堂";					###  則可選擇此選項
}
print qq(
    </CENTER>
        <INPUT type=RADIO name=select_time_mode value=select_all onClick=javascript:Select_Time(1)>選擇所有節次 |
        <INPUT type=RADIO name=select_time_mode value=deselect_all onClick=javascript:Select_Time(2)>取消所有節次
        $select_mine
        <BR>
        <INPUT type=RADIO name=query_type value=1 CHECKED>查詢所有 "只" 使用到這些時段的科目<BR>
        <INPUT type=RADIO name=query_type value=2>查詢所有使用到這些時段的科目
  </TD>
  <TD>
    科目名稱: <INPUT name="course_cname"><BR>
    教師姓名: <INPUT name="teacher"><BR>
  </TD>
  </TR>
  <TR>
    <TD colspan=2>
    &nbsp;<P>
    請選擇時段<FONT color=RED>(必填)</FONT>:
  );
  
Print_Timetable_Select(@my_table);
  
      
print qq(    
    </TR>
  </TABLE>
  <p>
  <center>
  <input type="submit" value="送出資料">
  <input type="reset" value="重新填寫">
  </form>
  <HR>
  </CENTER>
  <LI><FONT color=GREEN size=-1>科目名稱與教師姓名兩個欄位, 暫不接受萬用字元</FONT>
  </body>
  </html>
);
 
######################################################################################
