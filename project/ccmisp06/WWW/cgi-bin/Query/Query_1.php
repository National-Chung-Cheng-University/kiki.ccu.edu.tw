<?PHP
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////  查詢修課學生名單
/////  判斷 Login.cgi 傳來的 query_count 參數，以決定要列出某系課科目人數統計表，
/////  或是進入科目選單，供選取科目已顯示學生名單。
/////  Updates:
/////    199x/xx/xx Created
/////    200?/xx/xx 新增「查詢上次篩選完後名單」功能  Nidalap :D~
/////    2009/10/30 新增「列印上課記事簿」功能，由 print_notebook 值判定  Nidalap :D~
/////    2010/03/08 統計表模式中，新增開課年級、必選修等欄位  Nidalap :D~
/////    2010/06/08 馬賽克改為只針對未經系所登入者才會做。  Nidalap :D~
/////	 2010/09/17 依 email 要求，移除選課學生名單，只保留列印上課記事簿  Nidalap :D~
/////    2010/09/23 改為：若是系所登入則連到 Print_Notebook.cgi，否則連到 Query_2.cgi 詢問教師人事代碼  Nidalap :D~ 
/////    2016/11/17 從 perl 改寫為 php 版本，並新增校際生相關欄位。 by Nidalap :D~


require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Student_Course.pm"; 
require $LIBRARY_PATH."Select_Course.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Teacher.pm";
require $LIBRARY_PATH."Classroom.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."System_Settings.pm";
require $LIBRARY_PATH."Error_Message.pm";

my(%Input,@Dept,@Course,%Dept);

%Input = User_Input();
%Input = Sanitize_Input(%Input);
%system_flags = Read_System_Settings();
%Dept = Read_Dept($Input{dept_cd});
%now = gettime();

#foreach $k (keys %Input) {
#  print("$k -> $Input{$k}<BR>\n");
#}


#if( $Input{last_semester} ) {
($year, $term) = Last_Semester($Input{last_semester});
#  $yearterm = $year . $term;
#}else{
#  $yearterm = "";
#}

print qq|
    <html>
      $EXPIRE_META_TAG
      <SCRIPT language="JAVASCRIPT">
        function goto_print_notebook() {
          document.myform.elements["print_notebook"].value = 1;
          document.myform.submit();
        }
        function goto_print_namelist() {
          document.myform.elements["print_notebook"].value = 0;
          document.myform.submit();
        }
      </SCRIPT>
      <head>
        $EXPIRE_META_TAG
        <title>國立中正大學開排選課系統 - 查詢修課學生名單 - $Dept{cname}</title>
      </head>
      <body background=$GRAPH_URL/ccu-sbg.jpg>
        <center><h1>
          <img src=$GRAPH_URL/open.jpg>
        </h1>
       <p>
       <h1>國立中正大學開排選課系統 - 查詢修課學生名單</i></h1>
|;
#print("semester, year, term = $Input{last_semester}, $year, $term<BR>\n");

@Course = Find_All_Course( $Dept{id},"",$year, $term);
@teacher = Read_Teacher_File();

$sys_state = Whats_Sys_State();
if( $sys_state == 0 ) {
  print("目前系統篩選中，暫不開放查詢!");
  exit(1);
}

if( $Input{query_count} == 1 ) {
  Show_Count_List();
}else{
  Show_Course_Select();
}
///////////////////////////////////////////////////////////////////////////#
/////  Show_Count_List
/////  顯示該系所當學期所有開設科目的目前選課人數, 依年級->科目代碼排序
/////  Added 2003/01/08, Nidalap :D~
sub Show_Count_List()
{
  print qq(
        <H4>您查詢的是第 $year 學年度第 $term 學期 $Dept{cname} 的課程</H4>
        <P ALIGN=RIGHT>
          資料查詢時間: $now{time_string}
        </P>
        <TABLE border=1>
          <TR>
            <TH>年級</TH><TH>科目代碼</TH><TH>科目班別</TH>
            <TH>科目名稱</TH><TH>必選修</TH>
            <TH>限修人數</TH><TH>目前修課人數</TH>
            <TH>授課教師</TH><TH>上課教室</TH><TH>上課時間</TH>
          </TR>
  );
  for($grade=1; $grade<=4; $grade++) {
    if($grade%2==1)  {
      $tr_tag = "<TR bgcolor=LIGHTYELLOW>";
    }else{
      $tr_tag = "<TR bgcolor=LIGHTGREEN>";
    }
    
    @course = Find_All_Course($Dept{id}, $grade, $year, $term);
    foreach $course (@course) {
      %course = Read_Course($Dept{id}, $$course{id}, $$course{group}, $year, $term, "");
      $count = Student_in_Course($Dept{id}, $course{id}, $course{group}, $year, $term);
      $teacher_string =  "";
      foreach $teacher (@{$course{teacher}} ) {
        $teacher_string .= "<BR>"  if($teacher_string ne "");
        $teacher_string .= $Teacher_Name{$teacher};
      }
      $time_string = Format_Time_String($course{time});
      %Room=Read_Classroom($course{classroom});
      print qq(
        $tr_tag
          <TD>$grade</TD>
          <TD>$course{id}</TD>
          <TD>$course{group}</TD>
          <TD>$course{cname}</TD>
          <TD>$PROPERTY_TABLE[$course{property}]</TD>
          <TD>$course{number_limit}</TD>
          <TD>$count</TD>
          <TD>$teacher_string</TD>
          <TD>$Room{cname}</TD>
          <TD>$time_string</TD>
        </TR>
      );
    }
  }
  print("</TABLE>");
}
///////////////////////////////////////////////////////////////////////////#
/////  Show_Course_Select
/////  顯示該系所當學期所有開設科目班別, 供選擇查詢名單
sub Show_Course_Select()
{
  if( $Input{login_dept_id} and $Input{password} ) {			###  只有系所登入要傳此值
    $form_target = "Print_Notebook.php";
  }else{
    $form_target = "Query_2.cgi";
  }
  print qq( 
       您查詢的是第 $year 學年度第 $term 學期 $Dept{cname} 的課程
       <h4>請選擇欲查詢之科目</h4><p><br>
         <FORM name=myform method=post action="$form_target">
		 <INPUT type='hidden' name='open_dept' value="$Input{open_dept}">
         <table border=0>
           <tr>
             <th><h3>科目:</h3></th><td>
             <select name=course_cd>
  );

  my($course,%temp,$i,$count);
  $count = @Course;
  for($i=0;$i < $count;$i++) {
    %temp = Read_Course($Dept{id},$Course[$i]{id},$Course[$i]{group}, $year, $term);
    print"<option value=$temp{id}_$temp{group}>[$temp{id}-$temp{group}]$temp{cname}\n";
  }

  print qq(
        </select>
          <input type=hidden name=dept_cd value=$Dept{id}>
          <input type=hidden name=dept_name value=$Dept{cname}> 
          <input type=hidden name=print_notebook value=0>
        </td>
      </tr>
    </table>
    <INPUT type=hidden name=last_semester value=$Input{last_semester}>
    <INPUT type=RADIO name="last_select" value=0 CHECKED>查詢目前選課名單<BR>
  );
  if( ($system_flags{allow_query_last_select_namelist} == 1) and ($year==$YEAR) and ($term eq $TERM)  ) {
    print qq(
      <INPUT type=RADIO name="last_select" value=1>查詢上次篩選完後名單<BR>
    );
  }
  if( $Input{login_dept_id} and $Input{password} ) {		###  只有系所登入要傳此值
    print qq(
      <INPUT type="hidden" name="login_dept_id" value="$Input{login_dept_id}">
      <INPUT type="hidden" name="password"      value="$Input{password}">
    );
  }

  print qq(
    &nbsp<BR>
    <TABLE border=0>
      <TR><TD valign=TOP>
          <!INPUT type=button value="資料填寫完畢" onClick="javascript: goto_print_namelist()">
          <!input type=\"submit\" value=\"資料填寫完畢\">
        </FORM>
      </TD><TD valign=TOP>
          <INPUT type=button value="列印上課記事簿" onClick="javascript: goto_print_notebook()">
      </TD></TR>
    </TABLE>
    </center>
    </body>
    </html>
  );
}

