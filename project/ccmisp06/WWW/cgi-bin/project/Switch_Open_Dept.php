<HTML>
  <HEAD>
    <SCRIPT type="text/javascript" src="../../javascript/jquery.js"></SCRIPT>
	<SCRIPT language="JavaScript">
	  $(document).ready(function() {
        $('#form1').submit();					///  ���Ѧ���i�קK�۰� submit�A���U debug
	  });
	</SCRIPT>
  </HEAD>
    
<?PHP
  ////////////////////////////////////////////////////////////////////////
  /////  �����}�Ҩt�ҥ\��
  /////  �Φb��ǰ|�e�ѦU�t��ڰ���}�һݨD�C��ǰ|�U�U�t�ҡA�b�}�ҥD���i�ݨ�u���������}�]��ǰ|�ҵ{�v�B
  /////  �u���������}�]���t�ҵ{�v�����s�A�z�L���{������ȤJ POST �ܼ� switch�A
  /////  �Y�� 1 �h�����������H�}�]��ǰ|�ҵ{�A�Y�� 0 �h���}�]���t�ҵ{�C
  /////  ���{�������W�@���ǨӪ� POST �H�� GET �ܼơA������� POST �۰ʶǦ^���D���C
  /////  Updates:
  /////    2015/04/10 Created by Nidalap :D~
  /////    2015/05/26 ���X�󦭥H�e�N�����y�����߶}�]�q�ѥ~�y�ҥ\�� by Nidalap :D~
/*
  print_r($_POST);
  echo "<BR>\n";
  print_r($_GET);
*/

  require_once("../library/Reference.php");
  require_once $LIBRARY_PATH . "Dept.php";
  $input = "<INPUT type='hidden' name='crypt' value='1'>\n";
  
  foreach( $_POST as $k=>$v ) {
	if( $k == "switch" ) {
	  $v = ($v+1)%2;
	  $input .= "<INPUT type='hidden' name='$k' value='$v'>\n";
	}else if( ($k == "dept_id")  or ($k == "dept_cd") ) {
	  if( $_GET["switch"] == 1 )  { 
		$open_dept = Find_Dept_College($_POST['dept_cd']);
//		$open_dept = "4321";
		$input .= "<INPUT type='hidden' name='$k' value='$open_dept'>\n";
	  }else{
		$input .= "<INPUT type='hidden' name='$k' value='" . $_POST['open_dept'] . "'>\n";
	  }
	}else{
	  $input .= "<INPUT type='hidden' name='$k' value='$v'>\n";
    }
  }
  
  foreach( $_GET as $k=>$v ) {
	$input .= "<INPUT type='hidden' name='$k' value='$v'>\n";
  }
  
  echo "
    <FORM action='Class_Menu.cgi' METHOD='POST' id='form1'>
      $input
	  <INPUT type='submit'>
    </FORM>
  ";



?>