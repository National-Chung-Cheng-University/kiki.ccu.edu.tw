<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<SCRIPT type='text/javascript' src='https://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js'></SCRIPT>
<script type="text/javascript">
	$(function() {
		$('#approve').change(function(){
			//alert($(this).val());
			//$('#form1').submit();
		})
	})
</script>
<link href="css/css01.css" rel="stylesheet" type="text/css">

{{***  顯示科目清單並提供選擇必選修的 TABLE TD ***}}
{{function name=list_course}}
  <TABLE border=1>
    <TR>
	  <TH>科目代碼</TH><TH>科目名稱</TH><TH>學分數</TH><TH>系所</TH>
	  <TH>屬性</TH><TH>修習狀態</TH><TH>本系與否</TH>
	  {{if $student.is_under != 1}}<TH>學士班與否</TH>{{/if}}		{{***  大學生不顯示此欄位  ***}}
	</TR>
	{{foreach $MPC as $cid => $cou}}
	  <TR>
	    <TD>{{$cou.course_id}}</TD>
		<TD>{{$cou.cname}}</TD>
		<TD>{{$cou.credit}}</TD>
		<TD>{{$cou.dept_cname}}</TD>
		<TD>{{if $cou.attr==1}}<FONT color="RED">{{$PROPERTY_TABLE[$cou.attr]}}</FONT>{{else}}{{$PROPERTY_TABLE[$cou.attr]}}{{/if}}</TD>
		<TD>{{if $cou.is_taken==1}}<FONT color="RED">已修</FONT>{{else}}未修{{/if}}</TD>
		<TD>{{if $cou.is_my_dept==1}}<FONT color="RED">是</FONT>{{else}}否{{/if}}</TD>
		{{if $student.is_under != 1}}
		    <TD>{{if $cou.is_under==1}}<FONT color="RED">是</FONT>{{else}}否{{/if}}</TD>
		{{/if}}		{{***  大學生不顯示此欄位  ***}}
	  </TR>
	{{foreachelse}}
		<TR>
		  <TD colspan=9 align="CENTER">
		    請先在<A href='my_cart.php' title='我的選課購物車'>
			<IMG src='_img/person/mainmenu_1_off.png' border=0 width=20 height=20>選課購物車</A>功能中，<BR>
			將您所想要的課程存入客製化學程中！
		  </TD>
		</TR>
	{{/foreach}}
  </TABLE>
  學程可修學分總數：{{$credits.total_max}}<BR>
  學程應修學分總數：{{$MP.total_credit}}
  <P>
  
  {{if $err_msg }}
    {{foreach $err_msg as $msg}}
	  <FONT color="RED">{{$msg}}</FONT><BR>
	{{/foreach}}
  {{/if}}
{{/function}}

<!---------  網頁標題、顯示特定學號輸入欄位、列表按鈕等  ----------------------------------------------------------------------------------------------------!>
<HEAD>
  <TITLE>客製化學程審核</TITLE>
      
  <META http-equiv="Content-Type" content="text/html; charset=utf-8">
  <META HTTP-EQUIV="Pragma" CONTENT="NO-CACHE">
  <META HTTP-EQUIV="expires" CONTENT="-1">
</HEAD>

  <BODY background='https://kiki.ccu.edu.tw/~ccmisp12/Graph/manager.jpg'>
  <CENTER><H1>客製化學程審核</H1><HR size=2 width=50%>
  <TABLE border=0 bgcolor=YELLOW>
    <TR>
      <TD>
        <FORM action='My_Program_Approval.php' method='POST'>
          <INPUT maxsize=9 name=stu_id id = stu_id>
          <INPUT type=hidden name=action value='show_details'>
          <INPUT type='SUBMIT' value='顯示此學生申請資料(學號)'>
        </FORM>
	  </TD>
	  <TD>
	    <FORM name="form2" id="form2" method=POST action="My_Program_Approval.php">
          <INPUT type='hidden' name='action' value='list_records'>
          <INPUT type='submit' value='列出申請資料清單'>
        </FORM>
	  </TD>
    </TR>
  </TABLE>
<!--------------------------------------------------------------------------------------------------------------------------!>  
	
<FORM name="form1" id="form1" method=POST action="My_Program_Approval.php">
  <INPUT type='hidden' name='action' value='show_details'>
  <INPUT type='hidden' name='stu_id' value='{{$student.id}}'>
  審核狀態：
  <SELECT name="approve" id="approve">
    {{foreach $STATUS as $status_id => $status_txt}}
	  <OPTION value='{{$status_id}}' {{if $MP.status == $status_id}}SELECTED{{/if}}>{{$status_txt}}
	{{/foreach}}
  </SELECT>
  <INPUT type="SUBMIT" value='送出'>
</FORM>

  {{if $error_msg != ""}}錯誤：{{$error_msg}}
  {{else}}
  
  <FONT color='RED' size=6>{{$msg}}</FONT>
  <TABLE border=0 width=100% align="center">
	 {{if $MP.update_time != null}}
	   <TR>
	     <TD align="RIGHT">
		   上次修改時間：{{$MP.update_time}}<BR>
		   上次申請時間：{{if $MP.apply_time == null}}尚未申請{{else}}{{$MP.apply_time}}{{/if}}
		 </TD>
	   </TR>
	 {{/if}}
	 <TR>
	   <TD>
	     <TABLE width=100% border=1>
		   <TR>
		     <TD width='7%'>學號</TD><TD width='15%'>{{$student.id}}</TD>
			 <TD width='7%'>姓名</TD><TD width='15%'>{{$student.name}}</TD>
			 <TD width='56%' rowspan=9 valign='TOP'>{{call list_course}}</TD>
		   </TR>
		   <TR>
		     <TD>系所年級班級</TD>
			 <TD colspan=3>{{$dept.cname}} {{$student.grade}} 年級 {{$student.class}} 班</TD>
		   </TR>
		   <TR>
		     <TD>e-mail</TD><TD>{{$student.email}}</TD><TD>聯絡電話</TD><TD>{{$student.tel}}</TD>
		   </TR>
		   <TR>
		     <TD valign="TOP">應繳資料</TD> 
			 <TD colspan=3>
			   <INPUT type="checkbox" name="transcript" id="transcript" checked='checked'>歷年成績單<BR>
			   {{if $MP.others}}其他：{{$MP.others_detail}} {{/if}}
			 </TD>
		   </TR>
		   <TR>
		     <TD>中文學程名稱</TD>
			 <TD colspan=3>{{$MP.cname}}</TD>
		   </TR>
		   <TR>
		     <TD>英文學程名稱</TD>
			 <TD colspan=3>{{$MP.ename}}</TD>
		   </TR>
		   <TR>
		     <TD>學程規劃目標</TD>
			 <TD colspan=3>
			   <TEXTAREA name="purpose" id="purpose" COLS="60" ROWS="10">{{$MP.purpose}}</TEXTAREA>
			 </TD>
		   </TR>
		   <TR>
		     <TD>學程學習動機</TD>
			 <TD colspan=3>
			   <TEXTAREA name="motive" id="motive" COLS="60" ROWS="10">{{$MP.motive}}</TEXTAREA>
			 </TD>
		   </TR>
		   <TR>
		     <TD>學程設計之構想、理念與邏輯</TD>
			 <TD colspan=3>
			   <TEXTAREA name="detail" id="detail" COLS="60" ROWS="10">{{$MP.detail}}</TEXTAREA>
			 </TD>
		   </TR>
         </TABLE>
	   </TD>
	   
	 </TR>
   </TABLE>
   
   </FORM>

{{/if}}