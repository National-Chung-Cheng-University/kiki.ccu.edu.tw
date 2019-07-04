#!/usr/local/bin/perl

################################################################################################
#####  Course_Alias.cgi
#####  課程別名對應檔維護
#####  供系所輸入「新課程」、「原課程」的對應輸入，將來在重複修習篩選時，
#####  系統會將修過原課程的學生視同修過新課程處理。
#####  修改:
#####    2009/04/24 建立此程式  Nidalap :D~
#####    2010/05/18 修正讀取歷年科目錯誤，以及修正「若新科目為當學期新增，則無法顯示名稱與學分數」 bug  Nidalap :D~
#####    2016/05/17 修正因 open_dept 及 dept_cd 混淆導致文學院系所切換身份後顯示密碼錯誤訊息之 BUG  Nidalap :D~

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Open_Course.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Teacher.pm";

print("Content-type:text/html\n\n");
%input = User_Input();
%dept  = Read_Dept($input{dept_id});
@teacher = Read_Teacher_File();

Check_Dept_Password($input{open_dept}, $input{password});
Print_Header();

if( $input{add_del_flag} eq "add" ) {		###  新增對應資料
  ($add_result, $result_string) = 
      Add_Course_Alias($input{input_new_id}, $input{input_old_id}, $input{dept_id});
  print("<FONT color=RED>$result_string</FONT><P>");
}elsif( $input{add_del_flag} eq "del" ) {	###  刪除對應資料
  foreach $key (keys %input) {
    if( $input{$key} eq "on" ) {
      ($new_id, $old_id) = split(/_/,$key);
      ($del_result, $result_string) = Del_Course_Alias($new_id, $old_id, $input{dept_id});
      print("<FONT color=RED>$result_string</FONT><P>");
    }
  }
}


%course_alias = Read_Course_Alias();
%a30tcourse = Read_a30tcourse();		###  在執行新增/刪除以後，再讀取資料

###############################################################################################

print qq(
  <TABLE border=1 width=60%>
    <TR><TD>

  以下表格供維護「課程別名對應檔」，若貴系所曾有課程變更課碼，
  兩門(或更多)課實質上仍為同一課程者，應在此輸入該資料，以便系統進行重複修習篩選時，
  辨識兩者為同一科目，避免學生重複修習用。(ex.若新課程代碼為7304010，
  原課程代碼為7304005，則所有曾經修過7304005的學生，視同修過7304010進行重複篩選。)
  <P>
  &nbsp;
  <CENTER>
  <FORM action="Course_Alias.cgi" method=POST>
    新課程代碼：<INPUT name=input_new_id type=text size=7>&nbsp;&nbsp;&nbsp;&nbsp;
    原課程代碼：<INPUT name=input_old_id type=text size=7>&nbsp;&nbsp;&nbsp;&nbsp;

    <input type=hidden name="dept_id"	value="$input{dept_id}">
	<input type=hidden name="open_dept" value="$input{open_dept}">
    <input type=hidden name=grade value=$input{grade}>
    <input type=hidden name=password value=$input{password}>
    <INPUT type=hidden name="add_del_flag" value="add">
    <INPUT type=submit value="新增對應資料">    
  </FORM>
  
  <FORM action="Course_Alias.cgi" method=POST>
    <TABLE border=1 width=100%>
      <TR><TH ROWSPAN=2>刪除</TH><TH colspan=3>新課程</TH><TH colspan=3>原課程</TH></TR>
      <TR><TH>代碼</TH><TH>名稱</TH><TH>學分數</TH>
          <TH>代碼</TH><TH>名稱</TH><TH>學分數</TH></TR>
);

foreach $old_id (keys %course_alias) {
  $new_id = $course_alias{$old_id}{"new_id"};
  if( $course_alias{$old_id}{"dept"} eq $input{dept_id} ) {			###  只顯示本系的資料
    if( $a30tcourse{$new_id}{cname} ne "" ) {						###  「新科目」以前曾開過
      $new_course{cname}  = $a30tcourse{$new_id}{cname};
      $new_course{credit} = $a30tcourse{$new_id}{credit};
    }else{										###  「新科目」是本學期新增
      %new_course = Read_Course($input{dept_id}, $new_id, "01");
    }
    $del_id = $new_id . "_" . $old_id;
    print qq( 
        <TR><TD align=CENTER><INPUT type=checkbox name=$del_id></TD>
            <TD>$new_id</TD><TD>$new_course{cname}</TD><TD>$new_course{credit}</TD>
            <TD>$old_id</TD><TD>$a30tcourse{$old_id}{cname}</TD><TD>$a30tcourse{$old_id}{credit}</TD>
        </TR>        
    );
  }
}

print qq(
      </TABLE>
    <input type=hidden name="dept_id"	value="$input{dept_id}">
	<input type=hidden name="open_dept" value="$input{open_dept}">
    <input type=hidden name=grade value=$input{grade}>
    <input type=hidden name=password value=$input{password}>
    <INPUT type=hidden name="add_del_flag" value="del">
    <INPUT type=SUBMIT value="刪除以上科目">
  </FORM>
);

print("</TD></TR></TABLE><HR>");

Links3($dept{id},$input{grade},$input{password});

#############################################################################################
sub Print_Header() 
{
  print qq(
   <html>
     <head>
       $EXPIRE_META_TAG
       <title>$SUB_SYSTEM_NAME開排課系統--課程別名對應檔維護</title>
     </head>
   <body background=$GRAPH_URL/ccu-sbg.jpg>
   <center>
    <table border=0 width=60%>
     <tr>
      <td>系別:</td><td> $dept{cname} </td>
      <td>年級:</td><td> $input{grade} </td></tr><tr>
      <th colspan=4><H1><FONT face="標楷體">
          <FONT COLOR=RED>$SUB_SYSTEM_NAME</FONT>
          開排課系統--課程別名對應檔維護</FONT></H1></th>
     </tr>
    </table>
    <hr width=80%>
  );
}


