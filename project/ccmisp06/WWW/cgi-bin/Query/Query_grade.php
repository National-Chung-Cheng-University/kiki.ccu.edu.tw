<?PHP
  //////////////////////////////////////////////////////////////////////////////////////////////////////////
  /////  Query_grade.php
  /////  查詢在校生成績。此網頁可能由專屬入口 index.html 進入，或是由 SSO 登入進入。
  /////  Updates:
  /////    2010/??/?? 重寫 PHP 版本  Nidalap :D~
  /////    2010/09/23 加入 Single Sign On 機制 Nidalap :D~
  /////    2011/09/28 加入暑修成績 Nidalap :D~
  /////    2012/10/22 加入休學生也可查詢功能  Nidalap :D~
  /////    2014/02/10 修正成績未到也計入平均之 BUG  Nidalap :D~
  /////    2015/03/03 比照畢業資格審查表，允許從教專系統連過來查詢  Nidalap :D~
  
  if(!isset($_SESSION))  session_start();
  include "../library/Reference.php";
  include $LIBRARY_PATH . "Error_Message.php";
  include $LIBRARY_PATH . "Common_Utility.php";
  include $LIBRARY_PATH . "Password.php";
  include $LIBRARY_PATH . "Session.php";
  include $LIBRARY_PATH . "Student.php";
  include $LIBRARY_PATH . "Dept.php";
  include $LIBRARY_PATH . "Select_Course.php";
  include $LIBRARY_PATH . "Grade.php";
  include $LIBRARY_PATH . "System_Settings.php";

  define("DEBUG", 0);
    
  $system_settings = Get_System_State();

  //if( DEBUG ) print_r($_SESSION);
  
  if( $_GET["SSOLogout"] == 1 ) {
	require_once $LIBRARY_PATH . "SSO/Query_grade/getssoCcuRight_config.php";
    ssoLogOut();
  }

  if( !( empty($_POST) AND isset($_SESSION['verifySso']) AND trim($_SESSION['verifySso'])=='Y' ) ){  ///  傳統入口登入
    if( array_key_exists("key", $_GET) )  {
	  if( DEBUG )  echo "from academic...";
	  Check_From_Academic();
	  $id = $_GET["id"];
	}else{	
	  $SSO_LOGIN = 0;
      if( DEBUG )  echo "traditional...";

//      $_SESSION['verifyChild']= "Y";
      $id                 = $_POST{"id"};
      $password           = $_POST{"password"};
    
      Validate_Input($id, "id");
      Validate_Input($password, "password");

      $password_original = $password;
      if( $USE_MD5_PASSWORD == 1 ) {
        $password = MD5($password);
      }else{
        $salt = Read_Crypt_Salt($id);
        $password = my_Crypt($password, $salt);
      }
 
      $password_validation = Check_Password($id, $password, "new", $password_original);
	}
  }else{											///  SSO 登入
    $SSO_LOGIN = 1;
    if( DEBUG ) echo "SSO...";
    $id = $_SESSION["sso_personid"];
//    Write_Session($session_id, $id, $password, 0);
//    $session_data       = Read_Session($session_id);
  }
  
  //echo "id = $id";
  if( !($student = Read_Student_Rest($id)) ) {        ///  優先先讀休學生資料
    $student = Read_Student($id);                     ///  再找在學生
  }


  Print_Banner();

  $grade = Get_Student_Grade($id);
  $order = Get_Student_Order($id);
  //print_r($grade);
  //print_r($order);
  
  Print_Grade_Table($grade, $order);
  if( $SSO_LOGIN == 1 ) {
    echo "<A href='Query_grade.php?SSOLogout=1'>返回SSO選單</A>";
  }
  

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  function Print_Banner()
  {
    global $GRAPH_URL, $id, $student, $SSO_LOGIN, $LIBRARY_PATH;
	$dept = Read_Dept($student["dept"]);
    
    if( preg_match("/^8/", $id) ) {
      if( preg_match("/碩士班$/", $dept["cname"]) ) {
        $dept["cname"] = preg_replace("/碩士班$/", "博士班", $dept["cname"]);
      }
    }
    
    $head_data = Form_Head_Data($id, $student["name"], $dept["cname"], $student["grade"], $student["class"]);
    
    echo "
	  <HTML>
	    <HEAD>
		  <META http-equiv='Content-Type' content='text/html; charset=utf-8'>
		</HEAD>
	    <BODY background='" . $GRAPH_URL . "bk.jpg'>
		  <CENTER>
		  <H1>國立中正大學 學生成績查詢系統</H1>
		  <HR>
		  $head_data
		</BODY>
	  </HTML>
	";  
  }
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  function Print_Grade_Table($grade, $order)
  {  
    global $PROPERTY_TABLE2, $DEPT_SERV_CODE, $id;
	
    $PROPERTY_TABLE2[9] = "<FONT color=RED>棄選</FONT>";
    $count_course = 0;
    $count_credit = 0;
    $total = 0;
    $avg = 0;

//    print_r($grade);      
//    print_r($order);

    foreach($grade as $g) {
      if( ($g["year"] != $last_year) or ($g["term"] != $last_term) ) {
        if( isset($last_year) ) {							///  結束一個學年學期
	  echo "</TABLE>";
	  $avg = round($total/$count_credit, 2);
	  echo "本學期共修習 $count_course 門課， $count_credit 學分，平均 $avg 分";
	  //echo "|$last_year|$last_term|" . $order[$last_year][$last_term] . "|<BR>\n";
          if( isset($order[$last_year][$last_term]) )  echo "(第 " . $order[$last_year][$last_term] . " 名)";
          echo ".<P>&nbsp;<P>";
          $count_course = 0;
          $count_credit = 0;
          $total = 0;
          $avg = 0;
        }
        if( $g["term"] == 3 ) { 
          echo "<H3>" . $g["year"] . " 學年度暑修</H3>";
        }else{
          echo "<H3>" . $g["year"] . " 學年度第 " . $g["term"] . " 學期</H3>"; 
        }
        echo "<TABLE border=1 width=80%>";
        echo "  <TR bgcolor=LIGHTYELLOW>
                  <TH width=100>科目代碼</TH>
                  <TH width=50>班別</TH>
                  <TH>科目名稱</TH>
                  <TH width=120>選課學分屬性</TH>
                  <TH width=50>學分</TH>
                  <TH width=80>成績</TH>
                </TR>";
      }
	  
      //////  $g["trmgrd"] 是原始成績， $trmgrd 是用來顯示的包含 HTML 醒目標籤
      if( $g["trmgrd"] == NULL )  $trmgrd = "<FONT color='#999999'>成績未到</FONT>";
      else if( preg_match("/$DEPT_SERV_CODE$/", $g["cid"]) ) {
         if( $g["trmgrd"] >= 60 )	$trmgrd = "通過";
         else				$trmgrd = "<FONT color=RED>未過</FONT>";
      }
      else if( !Grade_Pass($id, $g["trmgrd"], $g["property"], is_GRA()) )
         $trmgrd = "<FONT color=RED>" . $g["trmgrd"] . "</FONT>";
      else $trmgrd = $g["trmgrd"];
	  
      if( $g["property"] == 9 )  {			///  棄選 -> 不列入平均與總學分，不列入修課數
        $trmgrd = "無";						
      }else if( $g["property"] == 6 ) {		///  大學部課程 -> 不列入平均與總學分
	    $count_course++;
	  }else if( $g["property"] == 8 ) {		///  不列入畢業總學分 -> 不列入平均與總學分
        $count_course++;
      }else if( $g["trmgrd"] == NULL ) {	///  成績未到 -> 不列入平均與總學分
	    $count_course++;	  
	  }else{								///  一般成績已經送達之科目 -> 累加總學分數和總成績
        $count_course++;
        $count_credit += $g["credit"];
        $total += ($g["trmgrd"] * $g["credit"]);
      }
      echo "<TR>" . 
             "<TD>" . $g["cid"] . "</TD>" .
             "<TD>" . $g["grp"] . "</TD>" .
	     "<TD>" . $g["cname"] . "</TD>" .
	     "<TD>" . $PROPERTY_TABLE2[$g["property"]] . "</TD>" .
	     "<TD>" . $g["credit"] . "</TD>" .
	     "<TD>" . $trmgrd . "</TD>" .
           "</TR>";
      $last_year = $g["year"]; 
      $last_term = $g["term"];	
    }
    ///  最後一個學期的表尾
    echo "</TABLE>";
    $avg = round($total/$count_credit, 2);
    echo "本學期共修習 $count_course 門課， $count_credit 學分，平均 $avg 分";
    if( isset($order[$last_year][$last_term]) )  echo "(第 " . $order[$last_year][$last_term] . " 名)";

    echo ".<P>&nbsp;<P>";
	
//    $smarty = init_smarty();
//    $smarty->assign("Query_grade.tpl");
  }
  ////////////////////////////////////////////////////////////////////////////////////////////
  /////  檢查從教專系統過來的 key 等資訊
  /////  Added 2015/03/03  Nidalap :D~
  function Check_From_Academic()
  {
	global $EXPIRE_META_TAG;
	
	$id				= $_GET["id"];
	$in_key			= $_GET["key"];
	$in_timestamp	= $_GET["key1"];
	$call_system	= array_key_exists("call_system", $_GET) ? $_GET["call_system}"] : "academic";

    /////  各個連過來的系統使用不同的 seed 產生 key
    $key_seeds = array("academic"		=> "bOsSlesSLESswORK", 
	                   "coursemap"	=> "thISisfORCoursEMaP");
    $key_seed = $key_seeds[$call_system];
    $key = Generate_Key($id, $key_seed, 0, $in_timestamp);

    //print("[id, key, key_seed, key1, call_system] = [$id, $key, $key_seed, $in_timestamp, $call_system]...<BR>\n");
    if( $key == $in_key ) {
	  return;
	}else{
      echo("<HTML><HEAD>$EXPIRE_META_TAG<TITLE>輸入資訊錯誤</TITLE></HEAD>");
      echo("<BODY background=$BG_PIC>");
      echo("<Center><H1>輸入資訊錯誤<hr></H1>");
      echo("您輸入的資訊有誤, 若見到此訊息, <BR>請於上班時間電洽教務處教學組或電算中心, 並告知底下的錯誤訊息:<p>");
      echo("錯誤訊息: <FONT color=RED>KEY_ERROR</FONT><P>");
	  die();
	}
    //Check_HTTP_REFERER();
  }


?>