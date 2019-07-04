<?php /* Smarty version Smarty-3.1.7, created on 2015-11-13 08:19:55
         compiled from "/NFS/project/ccmisp06/smarty/templates/superuser/My_Program_Approval.tpl" */ ?>
<?php /*%%SmartyHeaderCode:163084149256385975b90db7-95179982%%*/if(!defined('SMARTY_DIR')) exit('no direct access allowed');
$_valid = $_smarty_tpl->decodeProperties(array (
  'file_dependency' => 
  array (
    '339c254a0533f4d9bc40cd78970c03ffc5a5f85b' => 
    array (
      0 => '/NFS/project/ccmisp06/smarty/templates/superuser/My_Program_Approval.tpl',
      1 => 1447373932,
      2 => 'file',
    ),
  ),
  'nocache_hash' => '163084149256385975b90db7-95179982',
  'function' => 
  array (
    'list_course' => 
    array (
      'parameter' => 
      array (
      ),
      'compiled' => '',
    ),
  ),
  'version' => 'Smarty-3.1.7',
  'unifunc' => 'content_56385975e300c',
  'variables' => 
  array (
    'student' => 0,
    'MPC' => 0,
    'cou' => 0,
    'PROPERTY_TABLE' => 0,
    'credits' => 0,
    'MP' => 0,
    'err_msg' => 0,
    'msg' => 0,
    'STATUS' => 0,
    'status_id' => 0,
    'status_txt' => 0,
    'error_msg' => 0,
    'dept' => 0,
  ),
  'has_nocache_code' => 0,
),false); /*/%%SmartyHeaderCode%%*/?>
<?php if ($_valid && !is_callable('content_56385975e300c')) {function content_56385975e300c($_smarty_tpl) {?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
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


<?php if (!function_exists('smarty_template_function_list_course')) {
    function smarty_template_function_list_course($_smarty_tpl,$params) {
    $saved_tpl_vars = $_smarty_tpl->tpl_vars;
    foreach ($_smarty_tpl->smarty->template_functions['list_course']['parameter'] as $key => $value) {$_smarty_tpl->tpl_vars[$key] = new Smarty_variable($value);};
    foreach ($params as $key => $value) {$_smarty_tpl->tpl_vars[$key] = new Smarty_variable($value);}?>
  <TABLE border=1>
    <TR>
	  <TH>科目代碼</TH><TH>科目名稱</TH><TH>學分數</TH><TH>系所</TH>
	  <TH>屬性</TH><TH>修習狀態</TH><TH>本系與否</TH>
	  <?php if ($_smarty_tpl->tpl_vars['student']->value['is_under']!=1){?><TH>學士班與否</TH><?php }?>		
	</TR>
	<?php  $_smarty_tpl->tpl_vars['cou'] = new Smarty_Variable; $_smarty_tpl->tpl_vars['cou']->_loop = false;
 $_smarty_tpl->tpl_vars['cid'] = new Smarty_Variable;
 $_from = $_smarty_tpl->tpl_vars['MPC']->value; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array');}
foreach ($_from as $_smarty_tpl->tpl_vars['cou']->key => $_smarty_tpl->tpl_vars['cou']->value){
$_smarty_tpl->tpl_vars['cou']->_loop = true;
 $_smarty_tpl->tpl_vars['cid']->value = $_smarty_tpl->tpl_vars['cou']->key;
?>
	  <TR>
	    <TD><?php echo $_smarty_tpl->tpl_vars['cou']->value['course_id'];?>
</TD>
		<TD><?php echo $_smarty_tpl->tpl_vars['cou']->value['cname'];?>
</TD>
		<TD><?php echo $_smarty_tpl->tpl_vars['cou']->value['credit'];?>
</TD>
		<TD><?php echo $_smarty_tpl->tpl_vars['cou']->value['dept_cname'];?>
</TD>
		<TD><?php if ($_smarty_tpl->tpl_vars['cou']->value['attr']==1){?><FONT color="RED"><?php echo $_smarty_tpl->tpl_vars['PROPERTY_TABLE']->value[$_smarty_tpl->tpl_vars['cou']->value['attr']];?>
</FONT><?php }else{ ?><?php echo $_smarty_tpl->tpl_vars['PROPERTY_TABLE']->value[$_smarty_tpl->tpl_vars['cou']->value['attr']];?>
<?php }?></TD>
		<TD><?php if ($_smarty_tpl->tpl_vars['cou']->value['is_taken']==1){?><FONT color="RED">已修</FONT><?php }else{ ?>未修<?php }?></TD>
		<TD><?php if ($_smarty_tpl->tpl_vars['cou']->value['is_my_dept']==1){?><FONT color="RED">是</FONT><?php }else{ ?>否<?php }?></TD>
		<?php if ($_smarty_tpl->tpl_vars['student']->value['is_under']!=1){?>
		    <TD><?php if ($_smarty_tpl->tpl_vars['cou']->value['is_under']==1){?><FONT color="RED">是</FONT><?php }else{ ?>否<?php }?></TD>
		<?php }?>		
	  </TR>
	<?php }
if (!$_smarty_tpl->tpl_vars['cou']->_loop) {
?>
		<TR>
		  <TD colspan=9 align="CENTER">
		    請先在<A href='my_cart.php' title='我的選課購物車'>
			<IMG src='_img/person/mainmenu_1_off.png' border=0 width=20 height=20>選課購物車</A>功能中，<BR>
			將您所想要的課程存入客製化學程中！
		  </TD>
		</TR>
	<?php } ?>
  </TABLE>
  學程可修學分總數：<?php echo $_smarty_tpl->tpl_vars['credits']->value['total_max'];?>
<BR>
  學程應修學分總數：<?php echo $_smarty_tpl->tpl_vars['MP']->value['total_credit'];?>

  <P>
  
  <?php if ($_smarty_tpl->tpl_vars['err_msg']->value){?>
    <?php  $_smarty_tpl->tpl_vars['msg'] = new Smarty_Variable; $_smarty_tpl->tpl_vars['msg']->_loop = false;
 $_from = $_smarty_tpl->tpl_vars['err_msg']->value; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array');}
foreach ($_from as $_smarty_tpl->tpl_vars['msg']->key => $_smarty_tpl->tpl_vars['msg']->value){
$_smarty_tpl->tpl_vars['msg']->_loop = true;
?>
	  <FONT color="RED"><?php echo $_smarty_tpl->tpl_vars['msg']->value;?>
</FONT><BR>
	<?php } ?>
  <?php }?>
<?php $_smarty_tpl->tpl_vars = $saved_tpl_vars;}}?>


<!---------  網頁標題、顯示特定學號輸入欄位、列表按鈕等  ----------------------------------------------------------------------------------------------------!>
<HEAD>
  <TITLE>客製化學程審核</TITLE>
      
  <META http-equiv="Content-Type" content="text/html; charset=utf-8">
  <META HTTP-EQUIV="Pragma" CONTENT="NO-CACHE">
  <META HTTP-EQUIV="expires" CONTENT="-1">
</HEAD>

  <BODY background='https://kiki.ccu.edu.tw/~ccmisp12/Graph/manager.jpg'>
  <CENTER><H1>客製化學程審核</H1><HR size=2 width=50%<?php ?>>
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
  <INPUT type='hidden' name='stu_id' value='<?php echo $_smarty_tpl->tpl_vars['student']->value['id'];?>
'>
  審核狀態：
  <SELECT name="approve" id="approve">
    <?php  $_smarty_tpl->tpl_vars['status_txt'] = new Smarty_Variable; $_smarty_tpl->tpl_vars['status_txt']->_loop = false;
 $_smarty_tpl->tpl_vars['status_id'] = new Smarty_Variable;
 $_from = $_smarty_tpl->tpl_vars['STATUS']->value; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array');}
foreach ($_from as $_smarty_tpl->tpl_vars['status_txt']->key => $_smarty_tpl->tpl_vars['status_txt']->value){
$_smarty_tpl->tpl_vars['status_txt']->_loop = true;
 $_smarty_tpl->tpl_vars['status_id']->value = $_smarty_tpl->tpl_vars['status_txt']->key;
?>
	  <OPTION value='<?php echo $_smarty_tpl->tpl_vars['status_id']->value;?>
' <?php if ($_smarty_tpl->tpl_vars['MP']->value['status']==$_smarty_tpl->tpl_vars['status_id']->value){?>SELECTED<?php }?>><?php echo $_smarty_tpl->tpl_vars['status_txt']->value;?>

	<?php } ?>
  </SELECT>
  <INPUT type="SUBMIT" value='送出'>
</FORM>

  <?php if ($_smarty_tpl->tpl_vars['error_msg']->value!=''){?>錯誤：<?php echo $_smarty_tpl->tpl_vars['error_msg']->value;?>

  <?php }else{ ?>
  
  <FONT color='RED' size=6><?php echo $_smarty_tpl->tpl_vars['msg']->value;?>
</FONT>
  <TABLE border=0 width=100% align="center">
	 <?php if ($_smarty_tpl->tpl_vars['MP']->value['update_time']!=null){?>
	   <TR>
	     <TD align="RIGHT">
		   上次修改時間：<?php echo $_smarty_tpl->tpl_vars['MP']->value['update_time'];?>
<BR>
		   上次申請時間：<?php if ($_smarty_tpl->tpl_vars['MP']->value['apply_time']==null){?>尚未申請<?php }else{ ?><?php echo $_smarty_tpl->tpl_vars['MP']->value['apply_time'];?>
<?php }?>
		 </TD>
	   </TR>
	 <?php }?>
	 <TR>
	   <TD>
	     <TABLE width=100% border=1>
		   <TR>
		     <TD width='7%'>學號</TD><TD width='15%'><?php echo $_smarty_tpl->tpl_vars['student']->value['id'];?>
</TD>
			 <TD width='7%'>姓名</TD><TD width='15%'><?php echo $_smarty_tpl->tpl_vars['student']->value['name'];?>
</TD>
			 <TD width='56%' rowspan=9 valign='TOP'><?php smarty_template_function_list_course($_smarty_tpl,array());?>
</TD>
		   </TR>
		   <TR>
		     <TD>系所年級班級</TD>
			 <TD colspan=3><?php echo $_smarty_tpl->tpl_vars['dept']->value['cname'];?>
 <?php echo $_smarty_tpl->tpl_vars['student']->value['grade'];?>
 年級 <?php echo $_smarty_tpl->tpl_vars['student']->value['class'];?>
 班</TD>
		   </TR>
		   <TR>
		     <TD>e-mail</TD><TD><?php echo $_smarty_tpl->tpl_vars['student']->value['email'];?>
</TD><TD>聯絡電話</TD><TD><?php echo $_smarty_tpl->tpl_vars['student']->value['tel'];?>
</TD>
		   </TR>
		   <TR>
		     <TD valign="TOP">應繳資料</TD> 
			 <TD colspan=3>
			   <INPUT type="checkbox" name="transcript" id="transcript" checked='checked'>歷年成績單<BR>
			   <?php if ($_smarty_tpl->tpl_vars['MP']->value['others']){?>其他：<?php echo $_smarty_tpl->tpl_vars['MP']->value['others_detail'];?>
 <?php }?>
			 </TD>
		   </TR>
		   <TR>
		     <TD>中文學程名稱</TD>
			 <TD colspan=3><?php echo $_smarty_tpl->tpl_vars['MP']->value['cname'];?>
</TD>
		   </TR>
		   <TR>
		     <TD>英文學程名稱</TD>
			 <TD colspan=3><?php echo $_smarty_tpl->tpl_vars['MP']->value['ename'];?>
</TD>
		   </TR>
		   <TR>
		     <TD>學程規劃目標</TD>
			 <TD colspan=3>
			   <TEXTAREA name="purpose" id="purpose" COLS="60" ROWS="10"><?php echo $_smarty_tpl->tpl_vars['MP']->value['purpose'];?>
</TEXTAREA>
			 </TD>
		   </TR>
		   <TR>
		     <TD>學程學習動機</TD>
			 <TD colspan=3>
			   <TEXTAREA name="motive" id="motive" COLS="60" ROWS="10"><?php echo $_smarty_tpl->tpl_vars['MP']->value['motive'];?>
</TEXTAREA>
			 </TD>
		   </TR>
		   <TR>
		     <TD>學程設計之構想、理念與邏輯</TD>
			 <TD colspan=3>
			   <TEXTAREA name="detail" id="detail" COLS="60" ROWS="10"><?php echo $_smarty_tpl->tpl_vars['MP']->value['detail'];?>
</TEXTAREA>
			 </TD>
		   </TR>
         </TABLE>
	   </TD>
	   
	 </TR>
   </TABLE>
   
   </FORM>

<?php }?><?php }} ?>