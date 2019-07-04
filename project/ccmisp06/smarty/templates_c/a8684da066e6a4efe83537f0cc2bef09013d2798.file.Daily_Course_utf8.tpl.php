<?php /* Smarty version Smarty-3.1.7, created on 2014-02-17 16:28:12
         compiled from "/NFS/project/ccmisp06/smarty/templates/class/Daily_Course_utf8.tpl" */ ?>
<?php /*%%SmartyHeaderCode:167333582850569702cc2368-32288000%%*/if(!defined('SMARTY_DIR')) exit('no direct access allowed');
$_valid = $_smarty_tpl->decodeProperties(array (
  'file_dependency' => 
  array (
    'a8684da066e6a4efe83537f0cc2bef09013d2798' => 
    array (
      0 => '/NFS/project/ccmisp06/smarty/templates/class/Daily_Course_utf8.tpl',
      1 => 1392625680,
      2 => 'file',
    ),
  ),
  'nocache_hash' => '167333582850569702cc2368-32288000',
  'function' => 
  array (
  ),
  'version' => 'Smarty-3.1.7',
  'unifunc' => 'content_50569702e123b',
  'variables' => 
  array (
    'session_id' => 0,
    'day_to_show_c' => 0,
    'day_to_show' => 0,
    'days' => 0,
    'day_chinese' => 0,
    'day' => 0,
    'schedule' => 0,
    'day_schedule' => 0,
    'sche' => 0,
    'welcome_msg' => 0,
  ),
  'has_nocache_code' => false,
),false); /*/%%SmartyHeaderCode%%*/?>
<?php if ($_valid && !is_callable('content_50569702e123b')) {function content_50569702e123b($_smarty_tpl) {?><!-- 
  Daily Course widget for SSO and kiki course selection system
  Updates:
    2012/06/29 Completed by Nidalap :D~
-->
<?php if ($_smarty_tpl->tpl_vars['session_id']->value!=''){?>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE">
  <meta name='viewport' content='width=device-width, initial-scale=1.0, user-scalable=no, minimum-scale=1.0, maximum-scale=1.0' /> 
  <script type="text/JavaScript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
  
  <!--- 行動板要加上 jQuery Mobile  --->
  <?php if ($_GET['m']>=1){?>
    <link rel="stylesheet" href="http://code.jquery.com/mobile/1.0a1/jquery.mobile-1.0a1.min.css" />
    <script src="http://code.jquery.com/jquery-1.4.3.min.js"></script>
    <script src="http://code.jquery.com/mobile/1.0a1/jquery.mobile-1.0a1.min.js"></script>
  <?php }?>
  
  <BODY background="http://kiki.ccu.edu.tw/~ccmisp06/Graph/ccu-sbg.jpg">
<?php }?>

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
<?php if ($_GET['m']>=1){?>
  <DIV data-role='page'>
	<CENTER>
	<DIV data-role='header' data-theme='b'>
	  <IMG src='../../Graph/mobile/title310px.gif'>
	</DIV>
	<DIV data-role='content'>
<?php }?>

<div id="w_DailyCourse">
<CENTER>
  <H2>
    <DIV id="daily_course_title">
      <?php echo $_smarty_tpl->tpl_vars['day_to_show_c']->value;?>

      星期<?php echo $_smarty_tpl->tpl_vars['days']->value[$_smarty_tpl->tpl_vars['day_to_show']->value];?>

      課表
    </DIV>
  </H2>
[ 
  <?php  $_smarty_tpl->tpl_vars['day_chinese'] = new Smarty_Variable; $_smarty_tpl->tpl_vars['day_chinese']->_loop = false;
 $_smarty_tpl->tpl_vars['day'] = new Smarty_Variable;
 $_from = $_smarty_tpl->tpl_vars['days']->value; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array');}
 $_smarty_tpl->tpl_vars['day_chinese']->total= $_smarty_tpl->_count($_from);
 $_smarty_tpl->tpl_vars['day_chinese']->iteration=0;
foreach ($_from as $_smarty_tpl->tpl_vars['day_chinese']->key => $_smarty_tpl->tpl_vars['day_chinese']->value){
$_smarty_tpl->tpl_vars['day_chinese']->_loop = true;
 $_smarty_tpl->tpl_vars['day']->value = $_smarty_tpl->tpl_vars['day_chinese']->key;
 $_smarty_tpl->tpl_vars['day_chinese']->iteration++;
 $_smarty_tpl->tpl_vars['day_chinese']->last = $_smarty_tpl->tpl_vars['day_chinese']->iteration === $_smarty_tpl->tpl_vars['day_chinese']->total;
?>
    <?php if ($_smarty_tpl->tpl_vars['day_chinese']->value!=''){?>
      <SPAN style="background-color:YELLOW" 
            class="daily_course_day" 
            id="daily_course_day_<?php echo $_smarty_tpl->tpl_vars['day']->value;?>
"><?php echo $_smarty_tpl->tpl_vars['day_chinese']->value;?>
</SPAN>
      <?php if (!$_smarty_tpl->tpl_vars['day_chinese']->last){?>|<?php }?>
    <?php }?>
  <?php } ?>
]
  
<BR>

  <?php  $_smarty_tpl->tpl_vars['day_schedule'] = new Smarty_Variable; $_smarty_tpl->tpl_vars['day_schedule']->_loop = false;
 $_smarty_tpl->tpl_vars['day'] = new Smarty_Variable;
 $_from = $_smarty_tpl->tpl_vars['schedule']->value; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array');}
foreach ($_from as $_smarty_tpl->tpl_vars['day_schedule']->key => $_smarty_tpl->tpl_vars['day_schedule']->value){
$_smarty_tpl->tpl_vars['day_schedule']->_loop = true;
 $_smarty_tpl->tpl_vars['day']->value = $_smarty_tpl->tpl_vars['day_schedule']->key;
?>
    <SPAN class="daily_course_content" id="daily_course_content_<?php echo $_smarty_tpl->tpl_vars['day']->value;?>
">
      <?php if ($_smarty_tpl->tpl_vars['day_schedule']->value==''){?>
	    您今天不需上課
	  <?php }else{ ?>
	    <TABLE border=1 width="90%">
          <TR>
            <TH>時間</TH>
            <TH>課程</TH>
            <TH>地點</TH>
          </TR>
   
          <?php  $_smarty_tpl->tpl_vars['sche'] = new Smarty_Variable; $_smarty_tpl->tpl_vars['sche']->_loop = false;
 $_from = $_smarty_tpl->tpl_vars['day_schedule']->value; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array');}
foreach ($_from as $_smarty_tpl->tpl_vars['sche']->key => $_smarty_tpl->tpl_vars['sche']->value){
$_smarty_tpl->tpl_vars['sche']->_loop = true;
?>
            <TR>
              <TD><?php echo $_smarty_tpl->tpl_vars['sche']->value['time'];?>
</TD>
              <TD><?php echo $_smarty_tpl->tpl_vars['sche']->value['course'];?>
</TD>
              <TD><?php echo $_smarty_tpl->tpl_vars['sche']->value['classroom'];?>
</TD>
            </TR>
          <?php } ?>
        </TABLE>
	  <?php }?>
    </SPAN>
  <?php } ?>
</CENTER>
</DIV>


<!--- 行動板要加上系統 LOGO  --->
<?php if ($_GET['m']>=1){?>
  </DIV>
  <DIV data-role='footer'  data-theme='b'>
	<?php echo $_smarty_tpl->tpl_vars['welcome_msg']->value;?>

  </DIV>
 </DIV>  <!-- page -->
<?php }?><?php }} ?>