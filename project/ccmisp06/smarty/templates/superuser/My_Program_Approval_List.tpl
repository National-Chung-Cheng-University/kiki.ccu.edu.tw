<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<SCRIPT type='text/javascript' src='https://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js'></SCRIPT>
<script type="text/javascript">
	$(function() {
		$('.std_no').click(function(){
			var std_no = $(this).text();
			//alert(std_no);
			$('#stu_id').val(std_no);
			$('#form1').submit();
		})
	})
</script>
<link href="css/css01.css" rel="stylesheet" type="text/css">
<STYLE type='text/css'>
	th {
		background-color: LIGHTGREEN;
	}
	
	.std_no {
		color: BLUE;
	}
	
</STYLE>

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
        <FORM name='form1' id='form1' action='My_Program_Approval.php' method='POST'>
          <INPUT maxsize=9 name='stu_id' id='stu_id'>
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

<FORM name="form1" id="form1" method=POST action="my_program1.php">
	
  <TABLE border=0 width=100% align="center">
     <TR>
		<TH>學號</TH><TH>姓名</TH><TH>系所年級</TH><TH>中文名稱</TH><TH>英文名稱</TH>
		<TH>(第一次)申請時間</TH><TH>修改時間</TH><TH>科目數</TH><TH>審核狀態</TH>
	 </TR>
	 {{foreach $MPs as $MP}}
	   <TR>
		 <TD><SPAN class='std_no'>{{$MP.std_no}}</SPAN></TD>
		 <TD>{{$MP.stu_cname}}</TD>
		 <TD>{{$MP.dept_cname}} {{$MP.grade}} 年級</TD>
		 <TD>{{$MP.cname}}</TD>
		 <TD>{{$MP.ename}}</TD>
		 <TD>{{$MP.create_time}}</TD>
		 <TD>{{$MP.update_time}}</TD>
		 <TD>{{$MP.course_count}}</TD>
		 <TD>{{if $MP.status == 0}}<FONT color="BLACK">{{else if $MP.status==1}}<FONT color="GREEN">{{else}}<FONT color="RED">{{/if}}
			{{$STATUS[$MP.status]}}{{if $MP.status >= 1}}({{$MP.verify_time}}審核){{/if}}</FONT></TD>
	   </TR>
	 {{/foreach}}
	 
   </TABLE>
   
</FORM>

