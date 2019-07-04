<?PHP

////////////////////////////////////////////////////////////////////////////////////////////
/////  Student.php
/////  學籍資料相關存取函式
////////////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////////////////
/////  Find_All_Student
/////  Updates:
/////    2009/10/28 改寫自 perl 版本, Nidalap :D~
function Find_All_Student()
{
  global $REFERENCE_PATH;
  $student_file = $REFERENCE_PATH . "student.txt";
  $STUDENTFILE = fopen($student_file, "r")  or
            die("Cannot open file $student_file\n");
  $i=0;
  while( list($dept,$grade,$class,$junk,$status,$id, $personal_id, $sex, $enrollnum, $name, $ename )  =
      fscanf($STUDENTFILE, "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n") ) {
    $student[$i++] = $id;
  }
  fclose($STUDENTFILE);
  return($student);
}

////////////////////////////////////////////////////////////////////////////////////////////
/////  Read_Student
/////  為了效率, 將此函式改為讀取單行的學生資料檔.
/////  2007/02/09 改寫 php version   Nidalap :D~
/////  2013/09/27 加入 dont_die_flag 以避免讀不到資料就整個死掉 by Nidalap :D~
function Read_Student($input_id, $dont_die_flag=NULL)
{
  global $REFERENCE_PATH;
  $student_file = $REFERENCE_PATH . "Student/" . $input_id;

  if( $STUDENT_FILE = fopen($student_file, "r") )  {
    //list($dept,$grade,$class,$junk,$status,$id, $personal_id, $sex, $enrollnum, $name, $ename )  =
    //  fscanf($STUDENT_FILE, "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n");
	
	$temp = fgets($STUDENT_FILE);
	list($dept,$grade,$class,$junk,$status,$id, $personal_id, $sex, $enrollnum, $name, $ename )  =  preg_split("/\t/", $temp);

    $dept = preg_replace("/8$/", "6", $dept);
    if( "" == $ename )  $ename = $name;
	$grade = Determine_Student_Grade($id, $enrollnum);
	
    return array("dept"		=>$dept,
                 "grade"	=>$grade,
                 "class"	=>$class,
                 "class_"	=>$class,
                 "status"	=>$status,
                 "id"		=>$id, 
                 "personal_id"	=>$personal_id, 
                 "sex"		=>$sex, 
                 "enrollnum"	=>$enrollnum,
                 "name"		=>$name,
				 "ename"	=>$ename
           );
  }else if( $dont_die_flag == 1 ) {
    return array();
  }else{
    Show_Student_Error_Message();
  }
}

////////////////////////////////////////////////////////////////////////////////////////////
/////  Read_Student_Rest
/////  讀取休學生資料
/////  2012/10/22 為使成績查詢功能可提供休學生使用，新增此函式  Nidalap :D~
function Read_Student_Rest($sid)
{
  global $REFERENCE_PATH;
  $student_file = $REFERENCE_PATH . "student_rest.txt";
  $STUDENTFILE = fopen($student_file, "r")  or
            die("Cannot open file $student_file\n");
  $i=0;
  while( list($dept,$grade,$class,$junk,$status,$id, $personal_id, $sex, $enrollnum, $name, $ename )  =
      fscanf($STUDENTFILE, "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n") ) {
	if( $sid == $id ) {
	  if( "" == $ename )  $ename = $name;
      return array("dept"         =>$dept,
                   "grade"        =>$grade,
                   "class"        =>$class,
                   "class_"       =>$class,
                   "status"       =>$status,
                   "id"           =>$id,
                   "personal_id"  =>$personal_id,
                   "sex"          =>$sex,
                   "enrollnum"    =>$enrollnum,
                   "name"         =>$name,
				   "ename"		  =>$ename
             );
    }
  }                                      
  return NULL;                            
}

////////////////////////////////////////////////////////////////////////////////////////////
/////  Read_Student_by_pid
/////  因應 SSO 單一簽入，輸入身份證號，傳回該學生的學籍(可能多筆)
/////  2010/09/23 Created by Nidalap :D~
function Read_Student_by_pid($input_pid)
{
  global $REFERENCE_PATH;
  $student_file = $REFERENCE_PATH . "Student_pid/" . $input_pid;

//  echo "Locate $student_file<BR>";
  if( $STUDENT_FILE = fopen($student_file, "r") )  {
    while(  list($dept,$grade,$class,$junk,$status,$id, $personal_id, $sex, $enrollnum, $name, $ename )  =
        fscanf($STUDENT_FILE, "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n") )   {
		$dept = preg_replace("/8$/", "6", $dept);
		if( "" == $ename )  $ename = $name;
		$grade = Determine_Student_Grade($id, $enrollnum);

		$student[] =  array("dept"		=>$dept,
					 "grade"	=>$grade,
					 "class"	=>$class,
					 "class_"	=>$class,
					 "status"	=>$status,
					 "id"		=>$id, 
					 "personal_id"	=>$personal_id, 
					 "sex"		=>$sex, 
					 "enrollnum"	=>$enrollnum,
					 "name"		=>$name,
					 "ename"	=>$ename
			   );
	}
	return $student;
  }else{
//    echo "error not found : $input_pid<BR>\n";
    Show_Student_Error_Message();
  }
}

////////////////////////////////////////////////////////////////////////////////////////////
/////  Show_Student_Error_Message
/////  帳號錯誤
/////  找不到學籍資料
function Show_Student_Error_Message($type)
{
  global $BG_PIC, $EXPIRE_META_TAG;

  if( $type = 1 ) {                                     ###  在右側視窗顯示
    echo("<HTML>$EXPIRE_META_TAG<HEAD><TITLE>帳號有誤</TITLE></HEAD>");
    echo("<BODY background=$BG_PIC>");
    echo("<Center><FONT color=RED>密碼確認結果</FONT><hr>");
    echo("<FONT size=-1>您輸入的帳號密碼有誤,<BR>請重新輸入!<p>");
    echo("<A href=\"login.php\">重新登入</A>");
    exit(2);
  }else{
    echo("<HTML>$EXPIRE_META_TAG<HEAD><TITLE>帳號有誤</TITLE></HEAD>");
    echo("<BODY background=$BG_PIC>");
    echo("<Center><H1>密碼確認結果<hr></H1>");
    echo("您輸入的帳號密碼有誤, 請重新輸入!<p>");
    echo("<FONT color=RED>請區分英文字母大小寫(新生密碼身份證號一律為大寫)</FONT><P>");
    exit(2);
  }

}
////////////////////////////////////////////////////////////////////////////////////////////
/////  Need_Special_Message
/////  檢查是否要給該學生特殊公告訊息
/////  2007 趕工製成. 將來若需再用請檢查是否需要修改程式
/////  2007/09/06
function Need_Special_Message($id)
{
  global $HOME_PATH, $YEAR, $TERM, $TEMP_20070904_FLAG;
  
  $need_flag = 0;

  if( ($TEMP_20070904_FLAG == 1) and ($YEAR==96) and ($TERM==1) ) {
    $namelist_file = $HOME_PATH . "BIN/One_time_jobs/Restore_Student_LOG/restore_student_log.namelist";
    if( $FP_NAMELIST = fopen($namelist_file, "r") )  {  
      while( list($list_id, $misc) = fscanf($FP_NAMELIST, "%s\t%s\n") ) {
        if( $id == $list_id ) {
          $need_flag = 1;
        }
      }
      fclose($FP_NAMELIST);
    }
  }
#  $need_flag = 1;
  return($need_flag);
}


////////////////////////////////////////////////////////////////////
/////  Find_Change_School_Student
/////  此函數供系統篩選使用,找出轉學生名單,並將轉學生的學號記錄下來 
/////  ps. 此函數也提供選課時使用, 轉學生視同新生
/////  傳入: 限制學號前三碼
/////  傳回: hash
/////  從 perl 版本改寫而來  2008/09/08 Nidalap :D~

function Find_Change_School_Student($limit_id=NULL)
{
  global $REFERENCE_PATH;
  $change_file = $REFERENCE_PATH . "Change_School_Student.txt";

//  if( !isset($limit_id) )  $limit_id = "";
  $i = 0;
  if( $CHANGE_FILE = fopen($change_file, "r") )  {
    while( list($dept,$grade,$class,$junk,$status,$id, $personal_id, $sex, $name, $ename )  =
       fscanf($CHANGE_FILE, "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n") )  {
     // 4154    4    A     Y     0    482415021   M   李永祥
      if( $limit_id != NULL ) {                   ###  如果有限制學號前三碼
        if( preg_match("/^$limit_id/", $id) )   $student{$id}=1;
      }else{                                      ###  如果要看所有轉學生
        $student{$id}=1;
      }
    }
  }
  fclose($CHANGE_FILE);
  return($student);
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////
/////  Determine_Student_Grade
/////  由學生的學號、註冊次數、以及系統是否升級的設定，來判斷學生年級
/////  Updates:
/////   2009/06/05 開始使用  Nidalap :D~
/////   2013/01/11 升級設定由原本「升級年級」改為「升級註冊次數」，以符合實際需求 by Nidalap :D~  
function Determine_Student_Grade($id, $enrollnum) 
{
//  my($grade, @grade_table);

  $system_settings = Get_System_State();

  if( $system_settings{"grade_upgrade"} == 1 ) {          ###  如果系統設定升級
    //$grade = floor( $enrollnum / 2 ) + 1;
	$grade = ceil( ($enrollnum+1)/ 2 );
  }else{                                                ###  如果系統設定不升級
    $grade = ceil( $enrollnum / 2 );
  }

  if( preg_match("/^4/", $id) ) {			###  大學生最高四年級
    if( $grade > 4 )  $grade = 4;
  }else{                                                ###  碩博士生最高三年級
    if( $grade > 3 )  $grade = 3;
  }

  if( $grade == 0 )  $grade = 1;			###  註冊次數為零的新生，為一年級
//  if( ($grade==1) and ($enrollnum==2) )  $grade=2;		###  20090909 違章建築！！！！！！！！！！！！！！！！！！

  return($grade);
}
///////////////////////////////////////////////////////////////////////////////////////////////////
/////  SSO登入的身份證號對應到兩筆學號，顯示畫面供選擇學號
function Select_Student_ID($student_by_id)
{
	
	$count = count($student_by_id);
	echo("<H1>您有 $count 筆學籍紀錄！</H1>");
	//print_r($student_by_id);
	echo("請選擇您要以哪個學號登入:");
	$i=0;
	foreach( $student_by_id as $std) {
		$temp = $_SERVER["PHP_SELF"]  . "?" . $_SERVER["QUERY_STRING"];
		$url = $temp . "&student_rec=" . $i ;
		//echo $temp . "<->" . $url . "<BR>";
		echo "<LI><A href='" . $url . "'>" . $std["id"] . "</A>\n";
//		print_r($std);
		$i++;
	}
	echo "<BR>\n";
}

///////////////////////////////////////////////////////////////////////////////////////////////////
/////  紀錄 LOG 資料 -> Student.log
//function Student_Log($action, $id,$password_original)
/////  2015/11/10  新增 $version 紀錄是否行動版，且將原有額外紀錄的 $su 變數也使用標準分隔字元做分隔(不相容於舊版)。 by Nidalap :D~
function Student_Log($action, $id, $course_id=NULL, $course_group=null, $property=null, $by_whom=null)
{
  global $LOG_PATH1, $SUPERUSER, $LOG_IGNORE_IP, $IS_MOBILE;

  $log_file = $LOG_PATH1 . "Student.log";
  if( ($file_handle = fopen($log_file, "a")) == 0 ) {
    echo("系統運作內部錯誤!<BR>");
    $error_code = "ERROR_WRITE_LOG_FOR_LOGIN";
    Error_Please_Report($error_code);
  }
  list($timestring, $junk) = gettime("");
  $ip = getenv("HTTP_X_FORWARDED_FOR");
  if( $ip == "" ) { $ip = getenv("REMOTE_ADDR"); }
  $ip = preg_replace("/, $LOG_IGNORE_IP/", "", $ip);
  
  if( $IS_MOBILE == 1 )		$version = "MOBILE";
  else								$version = "";
  if( $SUPERUSER == 1 )	$su = "SU";
  else								$su = "";

  if( ($action == "Login")or($action == "LoginFail") ) {
    $password_original = $course_id;              ///  用以與舊版本接軌
    $message = implode(" : ", array($action, $timestring, $ip, $id, $password_original, $su, $version));
//	$message = $action . " : " . $timestring . " : " . $ip . " : " . $id 
//               . " : " . $password_original . " :  : ";
  }else{
	$message = implode(" : ", array($action, $timestring, $ip, $id, $course_id, $course_group, $property, $su, $version));
//    $message = $action . " : " . $timestring . " : " . $ip . " : " . $id 
//                   . " : " . $course_id . " : " . $course_group . " : " . $property . " : ";
  }
//  if( $SUPERUSER == 1 ) {
//    $message .= "SU";
//  }
  $message .= "\n";
  fputs($file_handle, $message);
  fclose($file_handle);
}

/////////////////////////////////////////////////////////////////////////////////////////////
/////  Read_Student_State_Files()
/////    讀入輔系及雙學位（雙主修、双主修）等名單檔
/////    輸入: (None)
/////    輸出: $double, $minor (都是一維的關聯式陣列)
/////    需求: 輔系名單FU.txt, DOUBLE.txt
/////    Updates:
/////       2016/09/14 從 perl 版本修改而來(改為輸出兩個陣列變數，而非建立全域變數) Nidalap :D~
/////////////////////////////////////////////////////////////////////////////////////////////
function Read_Student_State_Files()
{
  global $REFERENCE_PATH;
  
  $minor_file   = $REFERENCE_PATH . "fu.txt";
  $double_file  = $REFERENCE_PATH . "double.txt";
  
  if( !($fp = fopen($minor_file, "r") ) ) {
    die("Cannot open file $minor_file<BR>\n");
  }
  while( $line = fgets($fp) ) {
    list($dept_id, $stu_id) = preg_split("/\s+/", $line);
    $minor[$stu_id] = $dept_id;    
  }
  
  if( !($fp = fopen($double_file, "r") ) ) {
    die("Cannot open file $double_file<BR>\n");
  }
  while( $line = fgets($fp) ) {
    list($dept_id, $stu_id) = preg_split("/\s+/", $line);
    $double[$stu_id] = $dept_id;    
  }
  
  return array($double, $minor);
}

/*
function Append_Login_LOG($id, $action)
{
  global $LOG_PATH1;

  $log_file = $LOG_PATH1 . "Student.log";
  if( ($file_handle = fopen($log_file, "a")) == 0 ) {
    echo("系統運作內部錯誤!<BR>");
    $error_code = "ERROR_WRITE_LOG_FOR_LOGIN";
    Error_Please_Report($error_code);
  }
  list($timestring, $junk) = gettime("");
  $ip = getenv("HTTP_X_FORWARDED_FOR");
  if( $ip == "" ) { $ip = getenv("REMOTE_ADDR"); }

  $message = $action . " : " . $timestring . " : " . $ip . " : " . $id . " :  :  : ";
  global $SUPERUSER;
  if( $SUPERUSER == 1 ) {
    $message .= "SU";
  }
  $message .= "\n";
  fputs($file_handle, $message);
  fclose($file_handle);
}
*/


?>