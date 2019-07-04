<!-- 
  Daily Course widget for SSO and kiki course selection system
  Updates:
    2012/06/29 Completed by Nidalap :D~
-->
{{if $session_id != ""}}
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE">
  <meta name='viewport' content='width=device-width, initial-scale=1.0, user-scalable=no, minimum-scale=1.0, maximum-scale=1.0' /> 
  <script type="text/JavaScript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
  
  <!--- 行動板要加上 jQuery Mobile  --->
  {{if $smarty.get.m >= 1}}
    <link rel="stylesheet" href="http://code.jquery.com/mobile/1.0a1/jquery.mobile-1.0a1.min.css" />
    <script src="http://code.jquery.com/jquery-1.4.3.min.js"></script>
    <script src="http://code.jquery.com/mobile/1.0a1/jquery.mobile-1.0a1.min.js"></script>
  {{/if}}
  
  <BODY background="http://kiki.ccu.edu.tw/~ccmisp06/Graph/ccu-sbg.jpg">
{{/if}}

<SCRIPT type="text/javascript">
  var nearby_days = new Object;
  nearby_days['-2'] = "前天";
  nearby_days['-1'] = "昨天";
  nearby_days['0']  = "今天";
  nearby_days['1']  = "明天";
  nearby_days['2']  = "後天";
  
  var days = ["", "一", "二", "三", "四", "五", "六", "日"];
  
  $(document).ready(function() {
    var now = new Date;
    var day = now.getDay();						//  今天星期幾
    var today = day;
    $("#daily_course_title").html("今天(星期"+ days[day] + ")課表");
    $(".daily_course_day").css("background-color", "#FFF")
                          .css("cursor", "pointer")
                          .css("color", "BLUE");			//  改變星期一到日樣式  
    $("#daily_course_day_"+day).css("background-color", "YELLOW");
    $(".daily_course_content").hide();
    $("#daily_course_content_"+day).show();
    $(".daily_course_day").click(function(){
      var day = $(this).attr("id");
      day = day.substr(-1,1);						//  抓取使用者點選哪一天
      var day_diff = day - today;
//      alert(day_diff);
      if( typeof nearby_days[day_diff] != 'undefined' ) {
        $("#daily_course_title").html(nearby_days[day_diff]+"(星期"+ days[day] + ")課表");
      }else{
        $("#daily_course_title").html("星期"+ days[day] + "課表");
      }      
      $(".daily_course_day").css("background-color", "#FFF");		//  改變星期一到日樣式
      $("#daily_course_day_"+day).css("background-color", "YELLOW");            
      $(".daily_course_content").hide();				//  將所選日期的課表顯示，其他隱藏
      $("#daily_course_content_"+day).show();
    });
  });
</SCRIPT>
<!--------  以上是 javascipt 部份  -------->

<!--- 行動板要加上系統 LOGO  --->
{{if $smarty.get.m >= 1}}
  <DIV data-role='page'>
	<CENTER>
	<DIV data-role='header' data-theme='b'>
	  <IMG src='../../Graph/mobile/title310px.gif'>
	</DIV>
	<DIV data-role='content'>
{{/if}}

<div id="w_DailyCourse">
<CENTER>
  <H2>
    <DIV id="daily_course_title">
      {{$day_to_show_c}}
      星期{{$days.$day_to_show}}
      課表
    </DIV>
  </H2>
[ 
  {{foreach $days as $day=>$day_chinese}}
    {{if $day_chinese != ""}}
      <SPAN style="background-color:YELLOW" 
            class="daily_course_day" 
            id="daily_course_day_{{$day}}">{{$day_chinese}}</SPAN>
      {{if !$day_chinese@last}}|{{/if}}
    {{/if}}
  {{/foreach}}
]
  
<BR>

  {{foreach $schedule as $day=>$day_schedule}}
    <SPAN class="daily_course_content" id="daily_course_content_{{$day}}">
      {{if $day_schedule == ""}}
	    您今天不需上課
	  {{else}}
	    <TABLE border=1 width="90%">
          <TR>
            <TH>時間</TH>
            <TH>課程</TH>
            <TH>地點</TH>
          </TR>
   
          {{foreach $day_schedule as $sche}}
            <TR>
              <TD>{{$sche.time}}</TD>
              <TD>{{$sche.course}}</TD>
              <TD>{{$sche.classroom}}</TD>
            </TR>
          {{/foreach}}
        </TABLE>
	  {{/if}}
    </SPAN>
  {{/foreach}}
</CENTER>
</DIV>


<!--- 行動板要加上系統 LOGO  --->
{{if $smarty.get.m >= 1}}
  </DIV>
  <DIV data-role='footer'  data-theme='b'>
	{{$welcome_msg}}
  </DIV>
 </DIV>  <!-- page -->
{{/if}}