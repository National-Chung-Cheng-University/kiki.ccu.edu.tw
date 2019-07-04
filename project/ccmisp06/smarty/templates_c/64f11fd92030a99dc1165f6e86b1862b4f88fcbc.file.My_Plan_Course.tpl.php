<?php /* Smarty version Smarty-3.1.7, created on 2013-05-05 14:35:41
         compiled from "/NFS/project/ccmisp12/smarty/templates/class/My_Plan_Course.tpl" */ ?>
<?php /*%%SmartyHeaderCode:7200560385185fdbd3a1866-93209975%%*/if(!defined('SMARTY_DIR')) exit('no direct access allowed');
$_valid = $_smarty_tpl->decodeProperties(array (
  'file_dependency' => 
  array (
    '64f11fd92030a99dc1165f6e86b1862b4f88fcbc' => 
    array (
      0 => '/NFS/project/ccmisp12/smarty/templates/class/My_Plan_Course.tpl',
      1 => 1367735669,
      2 => 'file',
    ),
  ),
  'nocache_hash' => '7200560385185fdbd3a1866-93209975',
  'function' => 
  array (
  ),
  'variables' => 
  array (
    'HEAD_DATA' => 0,
    'my_plan_course' => 0,
    'cou' => 0,
    'sel_status_code' => 0,
    'session_id' => 0,
  ),
  'has_nocache_code' => false,
  'version' => 'Smarty-3.1.7',
  'unifunc' => 'content_5185fdbd52357',
),false); /*/%%SmartyHeaderCode%%*/?>
<?php if ($_valid && !is_callable('content_5185fdbd52357')) {function content_5185fdbd52357($_smarty_tpl) {?><HTML>
  <HEAD>
    <TITLE>我的選課計畫</TITLE>
    <META http-equiv="Content-Type" content="text/html; charset=utf-8">
    <META HTTP-EQUIV="Pragma" CONTENT="NO-CACHE">
    <META HTTP-EQUIV="expires" CONTENT="-1">
  </HEAD>
  <BODY background='../../Graph/ccu-sbg.jpg'>
    <CENTER>
      <?php echo $_smarty_tpl->tpl_vars['HEAD_DATA']->value;?>

      <HR>
  	  <?php if (!$_smarty_tpl->tpl_vars['my_plan_course']->value){?>
	    我尚未建立選課計畫，來去<A href="http://coursemap.ccu.edu.tw/" target="_NEW">課程地圖系統</A>建立！
	  <?php }else{ ?>
	    我在<A href="http://coursemap.ccu.edu.tw/" target="_NEW">課程地圖系統</A>中擬定的選課計畫，其中以下科目在本學期有開課（點選科目名稱以加選）：<P>
	    <TABLE width=90% border=1 cellspacing=0 cellpadding=3>
	    <TR>
	      <TH bgcolor=yellow><font size=2>加選狀態</font></TH>
	      <TH bgcolor=yellow><font size=2>開課系所</font></TH>
		  <TH bgcolor=yellow><font size=2>開課年級</font></TH>
		  <TH bgcolor=yellow><font size=2>科目代碼</font></TH>
		  <TH bgcolor=yellow><font size=2>科目名稱</font></TH>
	    </TR>
	    <?php  $_smarty_tpl->tpl_vars['cou'] = new Smarty_Variable; $_smarty_tpl->tpl_vars['cou']->_loop = false;
 $_from = $_smarty_tpl->tpl_vars['my_plan_course']->value; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array');}
foreach ($_from as $_smarty_tpl->tpl_vars['cou']->key => $_smarty_tpl->tpl_vars['cou']->value){
$_smarty_tpl->tpl_vars['cou']->_loop = true;
?>
	  	  <TR>
	        <TH><font size=2><?php echo $_smarty_tpl->tpl_vars['sel_status_code']->value[$_smarty_tpl->tpl_vars['cou']->value['sel_status']];?>
</font></TH>
	        <TH><font size=2><?php echo $_smarty_tpl->tpl_vars['cou']->value['dept_name'];?>
</font></TH>
		    <TH><font size=2><?php echo $_smarty_tpl->tpl_vars['cou']->value['grade'];?>
</font></TH>
	  	    <TH><font size=2><?php echo $_smarty_tpl->tpl_vars['cou']->value['cid'];?>
</font></TH>
		    <TH><font size=2>
		      <?php if ($_smarty_tpl->tpl_vars['cou']->value['sel_status']==0){?>
		        <A href='Add_Course01.cgi?session_id=<?php echo $_smarty_tpl->tpl_vars['session_id']->value;?>
&dept=<?php echo $_smarty_tpl->tpl_vars['cou']->value['deptcd'];?>
&grade=<?php echo $_smarty_tpl->tpl_vars['cou']->value['grade'];?>
'>
			  <?php }?>
			  <?php echo $_smarty_tpl->tpl_vars['cou']->value['cname'];?>
</A></font>
		    </TH>
	      </TR>	  
	    <?php } ?>
        </TABLE>
	    <P>
        「加選狀態說明」：
	      <IMG src='../../Graph/O.gif' width=16 height=16>：本學期已加選
		  <IMG src='../../Graph/Checked_blue.gif' width=16 height=16>：過去已選修並通過
    <?php }?>
  </BODY>
</HTML>
		<?php }} ?>