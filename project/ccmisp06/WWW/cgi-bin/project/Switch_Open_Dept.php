<HTML>
  <HEAD>
    <SCRIPT type="text/javascript" src="../../javascript/jquery.js"></SCRIPT>
	<SCRIPT language="JavaScript">
	  $(document).ready(function() {
        $('#form1').submit();					///  註解此行可避免自動 submit，幫助 debug
	  });
	</SCRIPT>
  </HEAD>
    
<?PHP
  ////////////////////////////////////////////////////////////////////////
  /////  切換開課系所功能
  /////  用在文學院委由各系實際執行開課需求。文學院下各系所，在開課主選單可看到「切換身份開設文學院課程」、
  /////  「切換身份開設本系課程」等按鈕，透過此程式執行值入 POST 變數 switch，
  /////  若為 1 則為切換身份以開設文學院課程，若為 0 則為開設本系課程。
  /////  此程式接收上一頁傳來的 POST 以及 GET 變數，全部丟到 POST 自動傳回給主選單。
  /////  Updates:
  /////    2015/04/10 Created by Nidalap :D~
  /////    2015/05/26 結合更早以前就有的語言中心開設通識外語課功能 by Nidalap :D~
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