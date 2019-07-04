<HTML>
  <HEAD>
    <TITLE>我的選課計畫</TITLE>
    <META http-equiv="Content-Type" content="text/html; charset=utf-8">
    <META HTTP-EQUIV="Pragma" CONTENT="NO-CACHE">
    <META HTTP-EQUIV="expires" CONTENT="-1">
  </HEAD>
  <BODY background='../../Graph/ccu-sbg.jpg'>
    <CENTER>
      {{$HEAD_DATA}}
      <HR>
  	  {{if !$my_plan_course}}
	    我尚未建立選課計畫，來去<A href="http://coursemap.ccu.edu.tw/" target="_NEW">課程地圖系統</A>建立！
	  {{else}}
	    我在<A href="http://coursemap.ccu.edu.tw/" target="_NEW">課程地圖系統</A>中擬定的選課計畫，其中以下科目在本學期有開課（點選科目名稱以加選）：<P>
	    <TABLE width=90% border=1 cellspacing=0 cellpadding=3>
	    <TR>
	      <TH bgcolor=yellow><font size=2>加選狀態</font></TH>
	      <TH bgcolor=yellow><font size=2>開課系所</font></TH>
		  <TH bgcolor=yellow><font size=2>開課年級</font></TH>
		  <TH bgcolor=yellow><font size=2>科目代碼</font></TH>
		  <TH bgcolor=yellow><font size=2>科目名稱</font></TH>
	    </TR>
	    {{foreach $my_plan_course as $cou}}
	  	  <TR>
	        <TH><font size=2>{{$sel_status_code[$cou.sel_status]}}</font></TH>
	        <TH><font size=2>{{$cou['dept_name']}}</font></TH>
		    <TH><font size=2>{{$cou['grade']}}</font></TH>
	  	    <TH><font size=2>{{$cou['cid']}}</font></TH>
		    <TH><font size=2>
		      {{if $cou.sel_status == 0}}
		        <A href='Add_Course01.cgi?session_id={{$session_id}}&dept={{$cou['deptcd']}}&grade={{$cou['grade']}}'>
			  {{/if}}
			  {{$cou['cname']}}</A></font>
		    </TH>
	      </TR>	  
	    {{/foreach}}
        </TABLE>
	    <P>
        「加選狀態說明」：
	      <IMG src='../../Graph/O.gif' width=16 height=16>：本學期已加選
		  <IMG src='../../Graph/Checked_blue.gif' width=16 height=16>：過去已選修並通過
    {{/if}}
  </BODY>
</HTML>
		