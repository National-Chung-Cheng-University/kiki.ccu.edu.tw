<?PHP
  //////////////////////////////////////////////////////////////////////////////////////////////////////////
  /////  Query_grade.php
  /////  查詢在校生成績。此網頁可能由專屬入口 index.html 進入，或是由 SSO 登入進入。
  /////  Updates:
  /////    2010/??/?? 重寫 PHP 版本  Nidalap :D~
  /////    2010/09/23 加入 Single Sign On 機制 Nidalap :D~
  /////    2011/09/28 加入暑修成績 Nidalap :D~

  session_start();
    
  include "../library/Reference.php";
  include $LIBRARY_PATH . "Error_Message.php";
  include $LIBRARY_PATH . "Common_Utility.php";
  include $LIBRARY_PATH . "Password.php";
  include $LIBRARY_PATH . "Session.php";
  include $LIBRARY_PATH . "Student.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Dept.php";
  include $LIBRARY_PATH . "Select_Course.php";
  include $LIBRARY_PATH . "Grade.php";
  include $LIBRARY_PATH . "System_Settings.php";
//  include_once $LIBRARY_PATH . "SSO/comm.php";
//  include $LIBRARY_PATH . "SSO/_forward_web.php";
//  include $LIBRARY_PATH . "SSO/_expiretime.php";

  echo "GET = ";
  print_r($_GET);
  echo "<P>SESSION = ";
  print_r($_SESSION);

  require_once $LIBRARY_PATH . "SSO/readssoCcuRightXML.php";

//  define("DEBUG", 1);
  define("DEBUG", 1);
//  session_start();
//  $permit = 1;
//  $id = $_GET["miXD"];
    
  $system_settings = Get_System_State();
  //db_connect_public();
//  db_connect();
  
  // echo "permit = "  .  $permit;
  // echo "cid = " .  $cid;
  // echo "id = " . $id;

  //    $session_id = Create_Session_ID($id, $password);
//    echo("new session<BR>\n");
//  echo "PHP session :";
  if( DEBUG ) print_r($_SESSION);

  if( !( empty($_POST) AND isset($_SESSION['verifySso']) AND trim($_SESSION['verifySso'])=='Y' ) ){  ///  傳統入口登入
    if( DEBUG )  echo "traditional...";

    $_SESSION['verifyChild']= "Y";
    $id                 = $_POST{"id"};
    $password           = $_POST{"password"};
    Validate_Input($id, "id");
    Validate_Input($password, "password");
    $session_id = Create_Session_ID($id, $password);

    $password_original = $password;
    if( $USE_MD5_PASSWORD == 1 ) {
      $password = MD5($password);
    }else{
      $salt = Read_Crypt_Salt($id);
      $password = my_Crypt($password, $salt);
    }

    Write_Session($session_id, $id, $password, 0);
    $session_data       = Read_Session($session_id);
    $student = Read_Student($id);
    $password_validation = Check_Password($id, $password, "new", $password_original);
  }else{											///  SSO 登入
    if( DEBUG ) echo "SSO...";
    $id = $_SESSION["sso_personid"];
    $student_by_pid = Read_Student_by_pid($id);				///  此時 $id 尚為身份證代碼
//	echo "temp = ";
//	print_r($student_by_pid);
    if( count($student_by_pid) == 1 ) {					///  如果該身份證號對應的學籍資料只有一筆(絕大多數情況)
      $student = $student_by_pid[0];
      $id = $student["id"];
    }else{
      if( isset($_REQUEST["student_rec"]) ) {
        $rec = $_REQUEST["student_rec"];
        $student = $student_by_pid[$rec];
        $id = $student["id"];						///  為了與傳統入口並行相容，此行以後 $id 是學號
      }else{
        Select_Student_ID($student_by_pid);
        exit(1);
      }
    }	
  }

//  echo "student = ";
 //  print_r($student);
//  echo("temp = $temp<BR>\n");
//  print_r($session_data);

//  $salt = Read_Crypt_Salt($_POST['id']);
//  $password = my_Crypt($_POST['password'], $salt);
//  $password_validation = Check_Password($id, $password, "new");

  Print_Banner();

  if( DEBUG )  print_r($_SESSION);

//  Student_Log("Login  ", $id, "");            ///  若是由密碼輸入頁面連結過來 -> 紀錄 Login
  $grade = Get_Student_Grade($id);
  $order = Get_Student_Order($id);
  //print_r($grade);
  //print_r($order);
  
  Print_Grade_Table($grade, $order);
  // foreach( $_POST as $k => $v ) {
    // echo("$k -> $v<BR>\n");
  // } 

 
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  function Print_Banner()
  {
    global $GRAPH_URL, $id, $student;
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
//    print_r($grade);
    $count_course = 0;
    $count_credit = 0;
    $total = 0;
    $avg = 0;
    
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
      else if( !Grade_Pass($id, $g["trmgrd"]) )  $trmgrd = "<FONT color=RED>" . $g["trmgrd"] . "</FONT>";
      else $trmgrd = $g["trmgrd"];      
      if( $g["property"] == 9 )  {
        $trmgrd = "無";						///  棄選
      }else{							///  非棄選課程，累加總學分數和總成績
        $count_course ++;
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
/*      if( $g["property"] != 9 )  {				///  非棄選課程，累加總學分數和總成績
        $count_course ++;
        $count_credit += $g["credit"];
        $total += ($g["trmgrd"] * $g["credit"]);
      }
*/
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
  /////  起始並設定 Smarty
  /////
/*  function init_smarty()
  {
    $smarty_php = "Smarty.class.php";
    require_once("$smarty_php");

    $smarty = new Smarty;
    $smarty->template_dir       = "./";
    $smarty->compile_dir        = "smarty/templates_c";
    $smarty->cache_dir          = "smarty/cache";
    $smarty->config_dir = "smarty/configs";

    $smarty->left_delimiter     = "{{";
    $smarty->right_delimiter    = "}}";

    return $smarty;
  }
*/
?>