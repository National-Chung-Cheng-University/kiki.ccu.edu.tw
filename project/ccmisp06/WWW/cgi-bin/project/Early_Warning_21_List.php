<?PHP
  ///////////////////////////////////////////////////////////////////////
  /////  物理系輔導學生選課機制
  /////  (目前只有物理系)填寫 21 邊緣學生名單。此名單中的學生不可選課，
  /////  除非與導師談過，導師會通知系所再來填寫，勾選為已與導師談過，
  /////  然後學生才可以選課。
  /////  Updates:
  /////    2011/01/18 Created by Nidalap :D~
  /////    2012/11/01 改採 PDO 連線資料庫 by Nidalap :D~
  /////    2013/09/13 修正因資料庫轉換導致的問題、檢查學籍資料不允許輸入休學生 Nidalap :D~

  require_once "../library/Reference.php";
  require_once $LIBRARY_PATH . "Database.php";
  require_once $LIBRARY_PATH . "Common_Utility.php";
  require_once $LIBRARY_PATH . "Error_Message.php";
  require_once $LIBRARY_PATH . "Dept.php";
  require_once $LIBRARY_PATH . "Student.php";
  require_once $LIBRARY_PATH . "Password.php";
  require_once $LIBRARY_PATH . "System_Settings.php";
  
  $dept_limit = $EARLY_WARNING_21_DEPT;		///  只有物理系適用
  
  if( strlen($YEAR)==2 )  $YEAR = "0" . $YEAR;  ///  把兩碼學年度填為三碼
  $DBH = PDO_connect();
//  db_connect("", 1);
  
//  print_r($_POST);
  $dept_id	= $_POST["dept_id"];
  $inpassword	= $_POST["password"];
  Check_Dept_Password($dept_id, $inpassword);
  
  Print_Banner();
  
  if( isset($_POST["add_stu_id"]) ) {		///  新增一筆紀錄
    Add_New_Record($_POST["add_stu_id"]);
  }
  if( isset($_POST["change_status"]) ) {	///  改變現有紀錄狀態
    Change_Status();
  }
  List_Records();
  
  //////////////////////////////////////////////////////////////////////////////////////
  function Print_Banner()
  {
    global $dept_id, $inpassword, $EXPIRE_META_TAG;
    echo "<HTML><HEAD>" . $EXPIRE_META_TAG . "</HEAD><BODY>";
    echo "<CENTER><H1>物理系輔導學生選課機制</H1><HR>";
    echo "
      <FORM action='Early_Warning_21_List.php' method='POST'>
        <INPUT type=hidden name=dept_id value='$dept_id'>
        <INPUT type=hidden name=password value='$inpassword'>
        新增學生(請輸入學號): <INPUT name='add_stu_id' size=9>
        <INPUT type='SUBMIT' value='加入預警名單'>
      </FORM>
    ";
    echo "<A href='../superuser/Update/Update_early_warning_21_list.php' target=_NEW>從資料庫更新名單</A><P>";
  }
  //////////////////////////////////////////////////////////////////////////////////////
  /////  2013/09/13 因 PostgreSQL 跨資料庫連線太麻煩，改用比較笨的方法結合名單與學籍資料 Nidalap :D~
  function List_Records() 
  {
    global $YEAR, $TERM, $dept_limit, $dept_id, $inpassword, $DBH;
    echo "以下列出需輔導的學生名單:<BR>";
    /*$sql = "SELECT EW.*, SR.name, SR.now_grade
              FROM early_warning_21_list EW, 
                   a11tstd_rec SR
             WHERE EW.id = SR.std_no
               AND SR.now_dept = '" . $dept_limit . "'
               AND year = '" . $YEAR . "'
               AND term = '" . $TERM . "'";
	*/
	$sql = "SELECT * FROM early_warning_21_list                   
             WHERE year = '$YEAR' AND term = '$TERM'";
    $STH = $DBH->prepare($sql);
	$STH->execute();
	
    echo "
      <FORM action='Early_Warning_21_List.php' method='POST'>
        <INPUT type='hidden' name='change_status' value=1>
        <INPUT type=hidden name=dept_id value='$dept_id'>
        <INPUT type=hidden name=password value='$inpassword'>
      <TABLE border=1>
        <TR><TH>學號</TH><TH>年級</TH><TH>姓名</TH><TH>狀態</TH></TR>
    ";
    $status_count_0 = $status_count_1 = 0;
    $count = 0;
	while( $r = $STH->fetch(PDO::FETCH_ASSOC) ) {
	  //echo "stu id = " . $r['id'];
	  $stu = Read_Student($r['id']);
	  
	  //print_r($stu);
	  //echo implode(" - ", array($r['id'], $stu['dept'], $dept_limit)) . "<BR>\n";
	  
	  if( $stu['dept'] != $dept_limit )  continue;
	  $r['now_grade']	= $stu['grade'];
	  $r['name']		= $stu['name'];
	
      $status_options = Create_Status_Options($r["status"]);
      if( $r["status"] == 0 ) {
        $status_count_0++;
        $bgcolor = "LIGHTYELLOW";
      }
      if( $r["status"] == 1 ) {
        $status_count_1++;
        $bgcolor = "WHITE";
      }
      $count++;
      echo "<TR bgcolor=$bgcolor><TD>" . $r["id"] . 
             "<TD>" . $r["now_grade"] .
             "<TD>" . $r["name"] . 
             "<TD>" . "<SELECT name='" . $r["id"] . "'>" .
                      $status_options . "</SELECT>" .
           "</TD></TR>\n";
    }
    echo "
        </TABLE>
          目前共 " . $count . " 筆紀錄，其中 " . 
          $status_count_0 . " 名學生尚未與導師洽談，" . 
          $status_count_1 . " 名學生已與導師洽談。
          <P>
          <INPUT type=submit value='改變狀態'>
      </FORM>
    ";
  }
  //////////////////////////////////////////////////////////////////////////////////////
  function Create_Status_Options($status)
  {
    $options = array("0" => "尚未與導師洽談，不得選課", "1" => "已與導師洽談，可以選課", 
                     "-1" => "誤輸入，取消此人限制！");
    $str = "";
	foreach($options as $opcode=>$opname) {
      $str .= "<OPTION value=" . $opcode;
      if( $status == $opcode ) {
        $str .= " SELECTED";
      }
      $str .=  ">" . $opname . "</OPTION>";
    }  
    return $str;
  }
  //////////////////////////////////////////////////////////////////////////////////////
  function Add_New_Record($id)
  {
    global $YEAR, $TERM, $dept_limit, $DBH;
    
    echo "<FONT color=RED>";
    switch( is_Legal_Student_ID($id, $dept_limit) ) {
      case -1: 						///  不是合法學號
        echo "您輸入的並非正確學號，請重新輸入！";
        break;
      case 0:						///  不是適用學系的學號
        echo "您輸入的並非適用學系的學號，請重新輸入！";
        break;
      case 1:						///  是適用學系的學號
        $sql = "INSERT INTO early_warning_21_list (year, term, id, status)
                VALUES ('" .implode("','", array($YEAR, $TERM, $id, "0") ) . "')";
        $STH = $DBH->prepare($sql);
		if( $STH->execute() ) {
          echo "成功加入學號 $id 紀錄。";
        }else{
          echo "加入資料錯誤！";
        }
        break;
    }
    echo "</FONT><BR>";
  }
  /////////////////////////////////////////////////////////////////////////////////////
  function Change_Status()
  {
    global $dept_limit, $YEAR, $TERM, $DBH;
    $count_succeed = $count_fail = 0;
    foreach($_POST as $k=>$v) {
      if( is_Legal_Student_ID($k, $dept_limit) ) {		///  如果是適用學系的學號
        if( $v == "-1" ) {					  ///  誤輸入，取消此限制
          $sql = "DELETE FROM early_warning_21_list 
                   WHERE id = '$k' AND year='$YEAR' AND term='$TERM'";
        }else{							  ///  更改狀態
//          $sql = "UPDATE early_warning_21_list SET status='" . $v . "' WHERE id='" . $k . "'";
          $sql = "UPDATE early_warning_21_list SET status='$v' 
                   WHERE id='$k' AND year='$YEAR' AND term='$TERM'";
        }
        $STH = $DBH->prepare($sql);
		if( $STH->execute() ) {
          $count_succeed++;
        }else{
          $count_fail++;
        }
//        echo $sql . "<BR>";
//      }else{
//        echo "skipping $k => $v<BR>\n";
      }
    }
    echo "<FONT color=RED>完成更新 $count_succeed 筆紀錄， $count_fail 筆紀錄更新失敗。</FONT><BR>";
  }
  //////////////////////////////////////////////////////////////////////////////////////
  /////  檢查輸入學號 $id 是否為 $dept_limit 學系的學生
  /////  傳回值： [1,0] = [是，不是 or 不是合法學號]  
  function is_Legal_Student_ID($id, $dept_limit)
  {
    //global $DBH;
	$DBH_a = PDO_connect("academic");
    if(preg_match("/^4\d{8}$/", $id))  {			///  如果是正確學號格式
      $sql = "SELECT now_dept FROM a11tstd_rec WHERE std_no = '$id'
              AND now_dept='$dept_limit' AND status != '5'";
      $STH = $DBH_a->prepare($sql);
	  $STH->execute();
	  $row = $STH->fetch();
	  
	  //echo $sql . "<BR>\n";
	  //echo "row = ";
	  //print_r($row);
	  
	  
      if( !empty($row) )
        return 1;
      else
        return 0;
    }else{
      return 0;
    }
  }
?>