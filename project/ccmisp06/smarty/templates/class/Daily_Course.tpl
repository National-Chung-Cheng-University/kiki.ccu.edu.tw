<!-- 
  今日課表 portal 小工具 
  此為 BIG5 版本，若有更新，請務必記得更新 utf-8 版本
  Updates:
    2012/06/29 Completed by Nidalap :D~
    2012/08/16 加入「您今天不需上課」訊息 by Nidalap :D~
    2012/09/05 移除引入 jquery.min.js 的程式碼，以免干擾 SSO 正常運作 by Nidalap :D~
-->

<!-- script type="text/JavaScript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script> -->
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
      day = day.substr(17,1);						//  抓取使用者點選哪一天
      var day_diff = day - today;
//      alert(day);
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
        {{foreachelse}}
          您今天不需上課
        {{/foreach}}
      </TABLE>
    </SPAN>
  {{/foreach}}
</CENTER>
</DIV>
