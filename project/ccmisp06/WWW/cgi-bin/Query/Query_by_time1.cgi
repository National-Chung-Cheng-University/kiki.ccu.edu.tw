#!/usr/local/bin/perl
########################################################################
#####  Query_by_time1.cgi
#####  進階開課資料查詢
#####  以系所, 開課節次時間, 科目名稱, 教師姓名等條件, 搜尋當學期開課資料.
#####  Last Update:
#####    2004/03/02
#####	 2008/06/03  新增科目名稱與教師姓名查詢選項.  Nidalap :D~
#####    2009/06/04  為 Find_All_Dept 加上 "NO_COM_DEPT" 參數，只讀取可以開課的系所 Nidalap :D~
#####    2013/08/27  英文版相關增修：將顯示文字拉到 Init_Text_Values() 中設定。 Nidalap :D~
#####    2016/01/20  因為新增「選擇所有學系」功能失敗，先將所有學系預設為選取狀態  Nidalap XD~
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
require $LIBRARY_PATH."English.pm";

%Input = User_Input();
%txt	  = Init_Text_Values();

#Print_Hash(%txt);

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

@dept = Find_All_Dept("NO_COM_DEPT");

#foreach $dept (@dept) {
#  print("$dept<BR>\n");
#}


print qq|
  <SCRIPT type="text/javascript" src="../../javascript/jquery.js"></SCRIPT>
  <SCRIPT language=JAVASCRIPT>
    /////  選擇所有學系功能  added 2015/12/15 Nidalap :D~
	\$(document).ready(function() {
	  \$('#select_all_dept').click(function(){
		});
		//var temp = \$('#dept').val();
//		alert(all_dept);
	})
  
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

|;

if( $IS_ENGLISH ) {
  $input_hidden_e = "<INPUT TYPE='hidden' name='e' value='1'>";
}else{
  $input_hidden_e = "<INPUT TYPE='hidden' name='e' value='0'>";
}

print "
  <HEAD>
    $EXPIRE_META_TAG
    <TITLE>" . $txt{'title'} . "</TITLE>
    <LINK rel='stylesheet' type='text/css' href='$HOME_URL/font.css'>
  </HEAD>
  <body bgcolor=white background=$GRAPH_URL/ccu-sbg.jpg>
  <center>
    <SPAN class='title1'>" . $txt{'title'} . "</SPAN><BR>
    <IMG src=$TITLE_LINE>
  <form id='form1' name='form1' method='post' action='Query_by_time2.cgi'>
    <input type=hidden name=session_id value=$Input{session_id}>
	$input_hidden_e
  <TABLE border=0 class='font1'>
    <TR><TD valign=TOP align=CENTER rowspan=2>
    <FONT size=2>
    " . $txt{'choose_dept'} . "<BR>
	<INPUT type='checkbox' id='select_all_dept'>" . $txt{'select_all_dept'} . "<BR>
    <SELECT name=dept_multi id=dept_multi multiple size=27>
";
foreach $dept (@dept) {
  %dept = Read_Dept($dept);
  if( $IS_ENGLISH ) {
    print("  <OPTION value='$dept' SELECTED>$dept{ename}\n");
  }else{
    print("  <OPTION value='$dept' SELECTED>$dept{cname2}\n");
  }
}
print qq(
    </SELECT>
  </TD>
  <TD valign=TOP>
);

if( $Input{session_id} ne "" ) {							###  如果有傳 session id 進來
  print qq(<INPUT type=hidden name=session_id value="$session_id>");						###  則傳出去
  $select_mine = " | <INPUT type=RADIO name=select_time_mode value=select_mine CHECKED";
  $select_mine .= " onClick=javascript:Select_Time(3)>" . $txt{'sel_time3'};					###  則可選擇此選項
}
print "
    </CENTER>
        <INPUT type=RADIO name=select_time_mode value=select_all onClick=javascript:Select_Time(1)>" . $txt{'sel_time1'} . " |
        <INPUT type=RADIO name=select_time_mode value=deselect_all onClick=javascript:Select_Time(2)>" . $txt{'sel_time2'} . "
        $select_mine
        <BR>
        <INPUT type=RADIO name=query_type value=1 CHECKED>" . $txt{'sel_time4'} . "<BR>
        <INPUT type=RADIO name=query_type value=2>" . $txt{'sel_time5'} . "
  </TD>
  <TD>
    " . $txt{'cname'} . ": <INPUT name='course_cname'><BR>
    " . $txt{'teacher'} . ": <INPUT name='teacher_cname'><BR>
  </TD>
  </TR>
  <TR>
    <TD colspan=2>
    &nbsp;<P>
    " . $txt{'sel_time6'} . ":
";
  
Print_Timetable_Select(@my_table);
  
      
print "    
    </TR>
  </TABLE>
  <p>
  <center>
  <input type='submit' value='" . $txt{'submit'} . "'>
  <input type='reset' value='" . $txt{'reset'} . "'>
  </form>
  <HR>
  </CENTER>
  <LI><FONT color=GREEN size=-1>" . $txt{'no_wildcard'} . "</FONT>
  </body>
  </html>
";
 
######################################################################################
#####  因應英文版本，將所有要顯示的文字在此整理，依照 $IS_ENGLISH 自動判別  2013/07/25
sub Init_Text_Values
{
  my %txtall;
    
  %txtall = (
    'title'		=> {'c'=>'進階開課資料查詢 -- 開課資料列表', 'e'=>'Advanced Course Search'},
	'choose_dept'=> {'c'=>'請選擇學系<FONT color=RED>(必填)</FONT>', 'e'=>'Select department(required)'},
	'select_all_dept'=>{'c'=>'選擇所有學系', 'e'=>'Select ALL departments'},
	'ctrl_multi'=> {'c'=>'(按Ctrl可複選): ', 'e'=>'(You can choose more than one department by pressing "Ctrl" key)'},

	'sel_time1'	=> {'c'=>'選擇所有節次', 'e'=>'Select all periods'},
	'sel_time2'	=> {'c'=>'取消所有節次', 'e'=>'Cancel all periods'},
	'sel_time3'	=> {'c'=>'選擇所有我的空堂', 'e'=>'Select all periods without schedule conflict'},
	'sel_time4'	=> {'c'=>'查詢所有"只"使用到這些時段的科目', 'e'=>'Search courses involving with the selected period'},
	'sel_time5'	=> {'c'=>'查詢所有使用到這些時段的科目', 'e'=>'Search courses offered at the selected period'},
	'sel_time6'	=> {'c'=>'請選擇時段(必填)', 'e'=>'Please choose period (required)'},
	
	'cname'		=> {'c'=>'科目名稱', 'e'=>'Course title'},
	'teacher'	=> {'c'=>'教師姓名', 'e'=>'Instructor name'},
	
	'submit'	=> {'c'=>'送出查詢', 'e'=>'Submit'},
	'reset'		=> {'c'=>'清除資料', 'e'=>'Clear Form'},
	
	'no_wildcard'=> {'c'=>'科目名稱與教師姓名兩個欄位, 不接受萬用字元', 
					 'e'=>'No wildcard allowed in course title and instructor name fields.'},
	'a'		=> {'c'=>'a', 'e'=>'a'}	
  );
  
  foreach $k (keys %txtall) {
	if( $IS_ENGLISH ) {
	  $txt{$k} = $txtall{$k}{'e'};
	}else{
	  $txt{$k} = $txtall{$k}{'c'};
	}
  }
 
  return %txt;  
}
