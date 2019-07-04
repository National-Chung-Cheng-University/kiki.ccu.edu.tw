<?PHP
  ///////////////////////////////////////////////////////////////////////
  /////  「通識課程與向度關聯表」
  /////  因應 2014 通識中心制度改革，將原本的五大領域改變為四個向度，
  /////  此程式提供管理介面，以維護科目與所屬向度的關聯。
  /////  只有通識中心會在主選單看到此功能連結。
  /////  Updates:
  /////    2013/11/22 Created by Nidalap :D~

  require_once "../library/Reference.php";
  require_once $LIBRARY_PATH . "Database.php";
  require_once $LIBRARY_PATH . "Common_Utility.php";
  require_once $LIBRARY_PATH . "Error_Message.php";
  require_once $LIBRARY_PATH . "Dept.php";
  require_once $LIBRARY_PATH . "Course.php";
  require_once $LIBRARY_PATH . "Password.php";
  require_once $LIBRARY_PATH . "System_Settings.php";
  
  $dept_limit = $DEPT_CGE;		///  只有物理系適用
  
  if( strlen($YEAR)==2 )  $YEAR = "0" . $YEAR;  ///  把兩碼學年度填為三碼
  $DBH = PDO_connect();
  $DBH_a = PDO_connect("academic");

  $dept_id	= $_POST["dept_id"];
  $inpassword	= $_POST["password"];
  Check_Dept_Password($dept_id, $inpassword);

  Print_Banner();
  
//  echo "POST:<BR>\n";
//  print_r($_POST);
//  echo "<HR>\n";
  
  $category = Get_CGE_Categories();
  $all_course = Find_All_Course($DEPT_CGE, "", "HISTORY");			///  全部的通識歷年課程(不分班別)
  
  if( $_POST['action'] == 'set' ) {									///  顯示此次共設定幾門科目
    $set_count = Set_Category();
  }else if(  $_POST['action'] == 'unset' ) {
    $set_count = Unset_Category();
  }
  if( $set_count )  echo "<FONT color=RED>共設定/取消 $set_count 門科目所屬向度<P></FONT>\n";
  
  $no_category_sel_html = Create_No_Category_Selection_Box_HTML();
  $i = 0;
  foreach( $category as $cate_id => $cate ) {
    foreach( $cate['sub'] as $subcate_id => $subcate ) {
	  
	  //echo "processing $cate_id - $subcate_id ... <BR>\n";	  
	  
	  $category_sel_box_html	= Create_Category_Selection_Box_HTML($cate_id, $subcate_id);
	  $category_set_button_html	= Create_Category_Set_Button_HTML($cate_id, $subcate_id);
	  
      if( $i++ == 0 ) {
	    $print_no_category_sel_html = "<TD rowspan=10>$no_category_sel_html</TD>";
	  }else{
	    $print_no_category_sel_html = "";
	  }
	  echo "
	    <TR>
	      <TD>$category_sel_box_html</TD>
	      <TD>$category_set_button_html</TD>
		  $print_no_category_sel_html
		</TR>
	  ";	
	}
  }
  echo "</TABLE></FORM>";
  
  //////////////////////////////////////////////////////////////////////////////////////
  function Print_Banner()
  {
    global $dept_id, $inpassword, $EXPIRE_META_TAG;
	
	$javascript_code = Print_Javascript();
    echo "<HTML><HEAD>" . $EXPIRE_META_TAG . "</HEAD>
	  $javascript_code
	<BODY>";
    echo "<CENTER><H1>通識課程與向度關聯表</H1><HR>";

    echo "
      <FORM id='form1' action='CGE_Category_Cour_Map.php' method='POST'>
        <INPUT type=hidden name='dept_id' value='$dept_id'>
        <INPUT type=hidden name='password' value='$inpassword'>
		<INPUT type=hidden name='action'value='' id='action'>
		<INPUT type=hidden name='cate_subcate'value='' id='cate_subcate'>
		
		<TABLE border=0>
		  <TR><TH>通識向度</TH><TH>設定</TH><TH>尚未歸類向度</TH></TR>
		
    ";

  }
  //////////////////////////////////////////////////////////////////////////////////////
  /////  印出右側尚未選取向度/次向度的課程多選方塊
  function Create_No_Category_Selection_Box_HTML()
  {
    global $all_course, $DEPT_CGE;
	$selection_size = 80;					////  多選方塊的長度
	
    $course_list_with_category = Find_All_Course_by_CGE_Category();
	Save_CGE_Category_to_File($course_list_with_category);			/// 偷偷將資料存在 local file

    $html = "<SELECT id='no_cate_sel' name='no_cate_sel[]' MULTIPLE size=$selection_size>\n";
	
	foreach ($all_course as $course) {
	  if( !array_key_exists($course['id'], $course_list_with_category) ) {
	    $cour = Read_Course($DEPT_CGE, $course['id'], "01", "HISTORY");
	    $html .= "<OPTION value='" . $course['id'] . "'>" . $course['id'] . "-" . $cour['cname'] . "\n";
	  }
	}
	$html .= "</SELECT>\n";
	
    return $html;
  }
  //////////////////////////////////////////////////////////////////////////////////////
  function Save_CGE_Category_to_File($course_list_with_category)
  {
    global $REFERENCE_PATH;
	
	$file = $REFERENCE_PATH . "cge_category_cour_map.txt";
	if( !($fp = fopen($file, "w")) )  die("系統內部錯誤：無法寫入課程與向度關聯資料檔！");
	foreach( $course_list_with_category as $cid => $list ) {
	  $line = implode("\t", array($cid, $list['category'], $list['subcategory'])) . "\n";
	  fputs($fp, $line);
	}
	fclose($fp);
  }
  //////////////////////////////////////////////////////////////////////////////////////
  /////  印出左側各個向度/次向度的課程多選方塊
  function Create_Category_Selection_Box_HTML($cate_id, $subcate_id) 
  {
//	echo "[cate, sub] = [$cate_id, $subcate_id]<BR>\n";
	global $category, $DEPT_CGE, $course_list_without_category;
	$selection_size = 7;					////  多選方塊的長度

	$course_list = Find_All_Course_by_CGE_Category($cate_id, $subcate_id);
//	array_push($course_list_without_category, $course_list);		///  設定全域變數紀錄那些課已經設定向度
	
	$this_id = "cate_sel_" . $cate_id . "_" . $subcate_id;
	
	$html = "向度: $cate_id. " . $category[$cate_id]['cname'] . " : " 
	        . $subcate_id . ". " . $category[$cate_id]['sub'][$subcate_id]['cname'] . "<BR>\n";
	$html .= "<SELECT id='$this_id' class='cate_sel' name='$this_id" . "[]' MULTIPLE size=$selection_size>\n";
	
	foreach( $course_list as $course ) {
	  $cour = Read_Course($DEPT_CGE, $course['cid'], "01", "HISTORY");
	  $html .= "<OPTION value='" . $course['cid'] . "'>" . $course['cid'] . "-" . $cour['cname'] . "\n";
	}
	$html .= "</SELECT>\n";
	//print_r($course_list);
	return $html;
  }
  //////////////////////////////////////////////////////////////////////////////////////
  /////  印出中間各個向度/次向度的課程的左移右移設定按鈕
  function Create_Category_Set_Button_HTML($cate_id, $subcate_id) 
  {
    $html  = "<BUTTON class = 'set' 
	                     id = 'set_" . $cate_id . "_" . $subcate_id . "
					   name = 'set_" . $cate_id . "_" . $subcate_id . "
					  value = '" . $cate_id . "_" . $subcate_id . "'><-</BUTTON><P>\n";
	$html .= "<BUTTON class = 'unset'
	                     id = 'unset_" . $cate_id . "_" . $subcate_id . "
					   name = 'unset_" . $cate_id . "_" . $subcate_id . "
					  value = '" . $cate_id . "_" . $subcate_id . "'>-></BUTTON>";
    
    return $html;
  }
  
  //////////////////////////////////////////////////////////////////////////////////////
  /////  設定課程向度關聯
  function Set_Category()
  {
    global $DBH_a;
	
	list($category, $subcategory) = preg_split("/_/", quotes($_POST['cate_subcate']));
	
	$set_count = $error_count = 0;
	foreach( $_POST['no_cate_sel'] as $cid ) {
	  $cid = quotes($cid);
	  $sql = "INSERT INTO a31tcge_category_cour_map (cid, category, subcategory) VALUES (?, ?, ?)";
	  $STH = $DBH_a->prepare($sql);
	  if( $STH->execute(array($cid, $category, $subcategory)) )  {
	    $set_count++;
	  }else{
	    $error_count++;
		print_r($DBH_a->errorInfo());
		echo "<BR>\n";
	  }
	}
	if( $error_count > 0 ) {
	  echo "<H1><FONT color=RED>設定出錯，請勿關閉此視窗，並通知系統管理員！</FONT></H1>\n";
	}
	return($set_count);
  }
  //////////////////////////////////////////////////////////////////////////////////////
  /////  取消課程向度關聯
  function Unset_Category()
  {
    global $DBH_a;
	
	list($category, $subcategory) = preg_split("/_/", quotes($_POST['cate_subcate']));
	
	$course_list = $_POST['cate_sel_' . $category . '_' . $subcategory];
	$set_count = $error_count = 0;
	
	//echo "course_list: ";
	//print_r($course_list);
	foreach( $course_list as $cid ) {
	  $cid = quotes($cid);
	  //$sql = "INSERT INTO a31tcge_category_cour_map (cid, category, subcategory) VALUES (?, ?, ?)";
	  $sql = "DELETE FROM a31tcge_category_cour_map WHERE cid = ?";
	  //echo $sql . "<BR>\n";
	  $STH = $DBH_a->prepare($sql);
	  if( $STH->execute(array($cid)) )  {
	    $set_count++;
	  }else{
	    $error_count++;
		print_r($DBH_a->errorInfo());
		echo "<BR>\n";
	  }
	  
	}
	if( $error_count > 0 ) {
	  echo "<H1><FONT color=RED>設定出錯，請勿關閉此視窗，並通知系統管理員！</FONT></H1>\n";
	}
	return($set_count);
  }
  //////////////////////////////////////////////////////////////////////////////////////
  function Print_Javascript()
  {
    $js = "
	  <SCRIPT type='text/javascript' src='../../javascript/jquery.js'></SCRIPT>
      <SCRIPT language='JavaScript'>
	    $(document).ready(function() {
		  $('.set').click(function(){
		    var cate_subcate = $(this).val();
		    $('#action').val('set');
			$('#cate_subcate').val(cate_subcate);
			$('#form1').submit();
		  });
		  
		  $('.unset').click(function(){
		    var cate_subcate = $(this).val();
		    $('#action').val('unset');
			$('#cate_subcate').val(cate_subcate);
			$('#form1').submit();
		  });
		});
	  </SCRIPT>
	";
    return $js;
  }

?>