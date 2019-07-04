<?php /* Smarty version Smarty-3.1.7, created on 2015-11-13 08:19:47
         compiled from "/NFS/project/ccmisp06/smarty/templates/superuser/My_Program_Approval_List.tpl" */ ?>
<?php /*%%SmartyHeaderCode:59259239256385955945396-74277937%%*/if(!defined('SMARTY_DIR')) exit('no direct access allowed');
$_valid = $_smarty_tpl->decodeProperties(array (
  'file_dependency' => 
  array (
    '7081a273ab3dab32f79f70bd5d686e9e8387797f' => 
    array (
      0 => '/NFS/project/ccmisp06/smarty/templates/superuser/My_Program_Approval_List.tpl',
      1 => 1447373932,
      2 => 'file',
    ),
  ),
  'nocache_hash' => '59259239256385955945396-74277937',
  'function' => 
  array (
  ),
  'version' => 'Smarty-3.1.7',
  'unifunc' => 'content_56385955bb7b0',
  'variables' => 
  array (
    'MPs' => 0,
    'MP' => 0,
    'STATUS' => 0,
  ),
  'has_nocache_code' => false,
),false); /*/%%SmartyHeaderCode%%*/?>
<?php if ($_valid && !is_callable('content_56385955bb7b0')) {function content_56385955bb7b0($_smarty_tpl) {?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
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
  <CENTER><H1>客製化學程審核</H1><HR size=2 width=50%<?php ?>>
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
	 <?php  $_smarty_tpl->tpl_vars['MP'] = new Smarty_Variable; $_smarty_tpl->tpl_vars['MP']->_loop = false;
 $_from = $_smarty_tpl->tpl_vars['MPs']->value; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array');}
foreach ($_from as $_smarty_tpl->tpl_vars['MP']->key => $_smarty_tpl->tpl_vars['MP']->value){
$_smarty_tpl->tpl_vars['MP']->_loop = true;
?>
	   <TR>
		 <TD><SPAN class='std_no'><?php echo $_smarty_tpl->tpl_vars['MP']->value['std_no'];?>
</SPAN></TD>
		 <TD><?php echo $_smarty_tpl->tpl_vars['MP']->value['stu_cname'];?>
</TD>
		 <TD><?php echo $_smarty_tpl->tpl_vars['MP']->value['dept_cname'];?>
 <?php echo $_smarty_tpl->tpl_vars['MP']->value['grade'];?>
 年級</TD>
		 <TD><?php echo $_smarty_tpl->tpl_vars['MP']->value['cname'];?>
</TD>
		 <TD><?php echo $_smarty_tpl->tpl_vars['MP']->value['ename'];?>
</TD>
		 <TD><?php echo $_smarty_tpl->tpl_vars['MP']->value['create_time'];?>
</TD>
		 <TD><?php echo $_smarty_tpl->tpl_vars['MP']->value['update_time'];?>
</TD>
		 <TD><?php echo $_smarty_tpl->tpl_vars['MP']->value['course_count'];?>
</TD>
		 <TD><?php if ($_smarty_tpl->tpl_vars['MP']->value['status']==0){?><FONT color="BLACK"><?php }elseif($_smarty_tpl->tpl_vars['MP']->value['status']==1){?><FONT color="GREEN"><?php }else{ ?><FONT color="RED"><?php }?>
			<?php echo $_smarty_tpl->tpl_vars['STATUS']->value[$_smarty_tpl->tpl_vars['MP']->value['status']];?>
<?php if ($_smarty_tpl->tpl_vars['MP']->value['status']>=1){?>(<?php echo $_smarty_tpl->tpl_vars['MP']->value['verify_time'];?>
審核)<?php }?></FONT></TD>
	   </TR>
	 <?php } ?>
	 
   </TABLE>
   
</FORM>

<?php }} ?>