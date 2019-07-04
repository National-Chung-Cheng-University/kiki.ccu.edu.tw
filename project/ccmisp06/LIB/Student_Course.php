<?PHP

//////////////////////////////////////////////////////////////////////////////////////////
///// Student_in_Course
///// 找出某科目目前選修的學生清單。
///// 輸入：($id, $group)
///// Updates:
/////	2016/07/12  加入支援 $year, $term 等輸入參數 by Nidalap :D~
function Student_in_Course($id, $group,$year="",$term="")
{
  global $DATA_PATH, $HISTORY_PATH, $YEAR, $TERM;

  if( ($year == "") and ($term == "") ) {
    $year = $YEAR; $term = $TERM;
  }
  if( $year == "last")  {											/// 要讀上次篩選後資料
    $STUDENT_OF_COURSE_PATH = $DATA_PATH . "Student_of_course_last/";
  }else if( $year == "last_semester")  {							/// 要讀上學期選課資料
    $STUDENT_OF_COURSE_PATH = $DATA_PATH . "Student_of_course_last_semester/";
  }else if( !( ($year==$YEAR)and($term==$TERM) ) ) {				/// 要讀以前某學期資料
#    print("[$year <-> $YEAR; $term <-> $TERM] 讀舊學期資料... <BR>\n");
    $STUDENT_OF_COURSE_PATH = $HISTORY_PATH . "Student_of_course/" . $year . "_" . $term . "/";
  }else{															/// 要讀目前選課名單
    $STUDENT_OF_COURSE_PATH = $DATA_PATH . "Student_of_course/";
  }
  
  $FILENAME = $STUDENT_OF_COURSE_PATH . $id . "_" . $group;
  if( file_exists($FILENAME) ){
    if( !($FILE = fopen($FILENAME, "r")) )  return;
  }else{
	die("not found: $FILENAME<BR>\n");
    //return;
  }
  
  while( $temp = fgets($FILE) )  $stu[] = rtrim($temp);
  fclose($FILE);
  
  return $stu;
}


//////////////////////////////////////////////////////////////////////////////////////////
/////  Student_Course.php
/////  處理學生選課資料與相關判斷.
/////  這裡是 Student_Course.pm 的 PHP 版本，只有少部份功能。
/////  Updates:
/////    2011/08/05 為了線上申請加簽功能，移植一些相關函式  by Nidalap :D~
   
function Course_of_Student($id, $year=NULL, $term=NULL)
{
    global $STUDENT_PATH, $HISTORY_PATH, $YEAR, $TERM;

    if( ($year=="") or ($term=="") ) {                          ###  如果沒有傳入 $year, $term
#      print("1");
      $student_path = $STUDENT_PATH;                            ###  或是不是本學年學期
    }else if( ($year==$YEAR) and ($term==$TERM) ) {               ###    那就讀取本學年學期資料
#      print("2");
      $student_path = $STUDENT_PATH;                            ###  else讀取歷史資料
    }else{
#      print("3");
      $student_path = $HISTORY_PATH . "Student/" . $year . "_" . $term . "/";
    }
    $FILENAME = $student_path . $id;

//    print("Trying to access $FILENAME<BR>\n");

    if( file_exists($FILENAME) ){
      $FILE = fopen($FILENAME, "r");
    }else{
      return;
    }
    while( $temp=fgets($FILE) )  $lines[] = $temp;
    fclose($FILE);

    if( !isset($lines) )  return;    
//    print_r($lines);

    $i = 0;
    foreach( $lines as $line ){
        rtrim($line);
//        print $line . "<BR>";
        $temp = preg_split("/\s+/", $line);
        $Course_of_the_Student[$i]["id"]=$temp[0];
        $Course_of_the_Student[$i]["dept"]=$temp[1];
        $Course_of_the_Student[$i]["group"]=$temp[2];
        $Course_of_the_Student[$i]["credit"]=$temp[3];
        $Course_of_the_Student[$i]["property"]=$temp[4];
        $i++;
    }
//    print_r($Course_of_the_Student);

    return $Course_of_the_Student;
}

//////////////////////////////////////////////////////////////////////////////////////////
/////  Check_Ban_Limit
/////  檢查擋修系所年級班別
/////  檢查學生選修的科目, 是否有限定擋修系所年級班別. 如果有, 判斷該生身份,
/////  判斷是否可選修. (管理者不在此限)
/////  只要系所年級班別任一項有擋, 其他沒選的視同全部選. 三者以AND連結
/////  輸入      : $The_Course, $Student
/////  輸出      : $ban_flag                       $ban_flag:(0,1) = (不擋, 擋修)
/////  Updates: 
/////    2011/08/09 從 perl 版本改寫 by Nidalap :D~
//////////////////////////////////////////////////////////////////////////////////////////
function Check_Ban_Limit($The_Course, $Student)
{
//  my($Ban_Dept_Num, $Ban_Grade_Num, $Ban_Class_Num);
//  my($L1, $L2, $L3);
//  my(%The_Course) = @_;
  global $DEPT_MIL, $DEPT_CGE, $FU, $DOUBLE, $SUPERUSER;

  $Ban_Dept_Num  = sizeof($The_Course["ban_dept"]);
  $Ban_Grade_Num = sizeof($The_Course["ban_grade"]); 
  $Ban_Class_Num = sizeof($The_Course["ban_class"]);
  
  $system_flags = Get_System_State();
//  print_r($The_Course);
//  echo "<HR>";
//  echo "[$Ban_Dept_Num, $Ban_Grade_Num, $Ban_Class_Num]<BR>";

  if( ($Ban_Dept_Num==0) and ($Ban_Grade_Num==0) and ($Ban_Class_Num==0) ) {
    return(0);                       ##  不擋修, return
  }else{                             ##  擋修, 繼續檢查
    if($Ban_Dept_Num == 0){             ##  如果沒有檔系所，則預設為所有系所
      $Ban_Dept=Find_All_Dept();
    }else{
      $Ban_Dept=$The_Course["ban_dept"];
    }

    if($Ban_Grade_Num == 0){            ##  如果沒有擋年級，則預設為所有年級
      $Ban_Grade=array(1,2,3,4,5,6,7,8,9,10);
    }else{
      $Ban_Grade=$The_Course["ban_grade"];
    }

    if($Ban_Class_Num == 0){            ##  如果沒有擋班級，則預設為所有班級
      $Ban_Class=array("A","B","C","D","E");
    }else{
      $Ban_Class=$The_Course["ban_class"];
    }
    $L1=$L2=$L3=0;
//    print_r($Ban_Dept);

    foreach( $Ban_Dept as $BD ){
//      echo "$BD <-> " . $Student["dept"] . "<BR>\n";
      if($BD == $Student["dept"]){
        $L1 = 1;
      }
    }
/*
#    print("fu : $FU{$Student{id}}<BR>");
#    print("double : $DOUBLE{$Student{id}}<BR>");
#    print("this : $The_Course{dept}<BR>");
    if( ($The_Course["dept"] == "6104") or ($The_Course["dept"] == "6154") or
        ($The_Course["dept"] == "6204") ) {       ### 如果開課系所是法律系任一組
       if( $FU{$Student["id"] eq "6054" ) {      ### 且學生是法律系輔系生
         $FU{$Student{id}} = $The_Course{dept}; ### 則視同是該組的輔系生
       }
    }
    if( $FU{$Student{id}} eq $The_Course{dept}) {
      $L1 = 0;                            ##  輔系不受擋修系所限制2002/02/26
    }
    if( $DOUBLE{$Student{id}} eq $The_Course{dept}) {
      $L1 = 0;                            ##  雙主修不受擋修系所限制2002/02/26
    }
*/
    foreach( $Ban_Grade as $item ) {            ##  要在意，升級後與升級前不同...
//      echo $item  . "<->" . $Student["grade"] . "<BR>\n";
      if($item == $Student["grade"] ){      ##  小心，不在意會發生重大危機...
        $L2 = 1;
      }
    }
    foreach( $Ban_Class as $item ){
      if($item == $Student["class"]){
        $L3 = 1;
      }
    }

//    echo "[L1, L2, L3] = [$L1, $L2, $L3]<BR>\n";

    if(($L1 == 1) && ($L2 == 1) && ($L3 == 1)){   ###  學生符合擋修系所年級班級
      if( isset($SUPERUSER) ) {                ##  管理者不擋修
        return(0);
      }else if($system_flags["no_ban"] == 1) {   ##  若設定第二階段設定擋修無效:
        if( $Ban_Dept_Num < 10 ) {           ##    -> 擋修系所少於 10 個(視同於限本系), 要檔修
          return(1);
        }else if( ($The_Course["dept"] == $DEPT_MIL) or ($The_Course["dept"] == $DEPT_CGE ) ) {
          return(1);                         ##    -> 軍訓與通識仍要擋修
        }else{
          return(0);                         ##    -> 其他課程依設定不擋修
        }
      }else{
        return(1);                           ##  符合限制, 要擋修
      }
    }
  }
}


//////////////////////////////////////////////////////////////////////////////////////////
/////  Stu_Can_Apply_Concent_Form
/////  判斷學生是否可加簽某科目
/////  符合以下條件任一，即可加簽：
/////    1. 科目目前選修人數 >= 限修人數
/////    2. 科目要求先修科目
/////    3. 科目擋修學生所屬系所年級班級
/////    4. 科目為軍訓，且學生當學期已選修其他軍訓
/////    5. 科目為語言中心課程(190開頭)
/////    6. 科目為學系服務學習課程
/////  輸入：($Student, $the_Course, $Course_of_Student, $student_count, $stu_grade)
/////  回傳：array($can_apply, $reasons)
/////  Updates:
/////    2011/08/05 Coded by Nidalap :D~
/////    2015/09/15 發現判別及格分數的部份 substr 丟錯參數，導致一律 70 分及格！馬上修正！   Nidalap :D~
function Stu_Can_Apply_Concent_Form($Student, $the_Course, $Course_of_Student, $student_count, $stu_grade)
{
  $can_apply = 0;
  global $DEPT_PHY;
  
//  print_r($Student);
//  print_r($the_Course);
//  print_r($Course_of_Student);
//  print_r($student_count);

//  print_r($Student);
//  print_r($the_Course);
//  print"<HR>";
//  print $student_count . "<BR>";
//  print $Course_of_Student;

  //////////  1. 科目目前選修人數 >= 限修人數
  if( $the_Course["number_limit"] ) {
    if( $student_count >= $the_Course["number_limit"] ) {
      $can_apply = 1;
      $reasons[] = "本科目限修 " . $the_Course["number_limit"] . "人，修課人數已額滿。";
    }
  }

//  print_r($stu_grade);
  /// 將一般陣列 $stu_grade 轉換為關聯式陣列 $grade
  if( $stu_grade ) {
    foreach( $stu_grade as $g ) {
      //echo $g["cour_cd"] . ":" . $g["trmgrd"] . "<BR>\n";
      $grade[$g["cour_cd"]] = $g["trmgrd"];
    }  
  }
  
//  print_r($grade);

 //////////  2. 學生不符先修科目規定  
//  print_r($the_Course);
  if( sizeof($the_Course["prerequisite_course"]) > 0 ) {
    $multi_pre_cou = 0;
    if( $the_Course["prerequisite_logic"] == "OR" ) {			///  OR: 預設不通過
      $pre_satisfied = 0;      
    }else{								///  AND: 預設通過
      $pre_satisfied = 1;
    }
    foreach( $the_Course["prerequisite_course"] as $pre_cou) {
	  //echo "checking " . $pre_cou["id"] , "<BR>\n";;

	  if( $pre_cou["grade"] == "pass" ) {				///  將 "pass" 的先修分數要求轉換為數字
        if( substr($Student["id"], 0,1) == 4 )	$pre_cou["grade"] = 60;
        else					$pre_cou["grade"] = 70;
      }
      if( ($pre_cou["dept"]!="")and($pre_cou["dept"]!="99999")) {  ///       先修課目所屬系所為「無」
        if( $the_Course["prerequisite_logic"] == "OR" ) {		///  OR: 這一科過就算過
          if( $grade[$pre_cou["id"]] >= $pre_cou["grade"] )  $pre_satisfied = 1;
		  //echo $pre_cou["id"] . " - $pre_satisfied - " . $grade[$pre_cou["id"]] . "  -  " . $pre_cou["grade"] .  " - " . substr($Student["id"], 0,1)  . "<BR>\n";
        }else{								///  AND: 這一科不過就算不過
          if( $grade[$pre_cou["id"]] < $pre_cou["grade"] ) {
            $pre_satisfied = 0;
            $can_apply = 1;
            $pre_cou_detail = Read_Course($pre_cou["dept"], $pre_cou["id"], "01", "HISTORY", "");
            $reasons[] = "本科目要求先修科目" . $pre_cou["id"] . "(" . $pre_cou_detail["cname"] . " )";
//			         . " 分數為 " . $grade[$pre_cou["id"]];
			
            break;
          }
        }
      }
    }
//    echo $pre_satisfied;
    if( ($pre_satisfied == 0) and ($the_Course["prerequisite_logic"] == "OR") ) {
      $reasons[] = "學生不符合此科目所有先修條件";
      $can_apply = 1;
    }

//    if( $multi_pre_cou ) {
//      $pre_logic = array("AND"=>"所有先修科目條件都必須符合" , "OR"=>"只要符合任一先修條件");
//      $temp_reason .= "(" . $pre_logic[$the_Course["prerequisite_logic"]] . ")";
//    }
//    if( isset($temp_reason) )  
//      $reasons[] = $temp_reason;
  }



//  print sizeof($the_Course["prerequisite_course"]);
//  print_r($the_Course["prerequisite_course"]);

  if( Check_Ban_Limit($the_Course, $Student)==1 ) {
    $can_apply = 1;                             ///  3. 科目擋修學生所屬系所年級班級
    $reasons[] = "此科目限制學生所屬系所不得選修。";
  }

  if( preg_match("/^903/", $the_Course["id"]) ) {
    foreach( $Course_of_Student as $cou) {
      if( preg_match("/^903/", $cou["id"]) ) {
        $can_apply = 1;                         ///  4. 科目為軍訓，且學生當學期已選修其他軍訓
        $reasons[] = "學生當學期已選修其他軍訓。";
      }
    }
  }
  //////////  5. 科目為語言中心所開設
  if( preg_match("/^190/", $the_Course["id"]) ) {
    $can_apply = 1;
    $reasons[] = "第二階段選課不開放加選語言中心課程。";
  }

  //////////  6. 科目為學系服務學習課程
  if( $the_Course["id"] == Get_Dept_Serv_Course_ID($the_Course["dept"]) ) {
    $can_apply = 1;
    $reasons[] = "因故退選學系服務學習課程。";
  }
  
  /////////   7. 科目為體育課
  if( $the_Course["dept"] == $DEPT_PHY ) {
//    $can_apply = 1;
    $reasons[] = "欲申請加簽體育課程，請先洽體育中心！";
  }

//  print_r($reasons);

  return array($can_apply, $reasons);
}
//////////////////////////////////////////////////////////////////////////////////////////
/////  加簽單學生申請狀態
/////  回傳值：
/////    查詢單筆：傳回單筆紀錄，或是 -1 代表尚未申請
/////    查詢多筆：傳回多筆紀錄
function Concent_Form_Apply_Status($stu_id, $cou_id, $grp, $year, $term)
{
  global $YEAR, $TERM, $DATABASE_NAME; // $DBH;
  if( $year == "" )  $year = $YEAR;
  if( $term == "" )  $term = $TERM;
  
  $DBH = PDO_connect("academic");
  $DBH_kiki = PDO_connect("academic_kiki");
  
  $table = "concent_form";
  if( $cou_id == NULL )	$query_stu_all_applications = 1;
  else                	$query_stu_all_applications = 0;
  
//  echo "[$year, $term, $stu_id, $query_stu_all_applications]<BR>";

  $sql = "SELECT DISTINCT year, term, course_id, grp, stu_id, serialno, verified, 
                 apply_time,
                 verify_time,
                 add_time
            FROM concent_form
           WHERE year = '$year'
             AND term = '$term'
             AND stu_id = '$stu_id'";
  
  if( $query_stu_all_applications == 0 ) {	///  查詢單筆紀錄        
    $sql .= " AND course_id = '$cou_id' AND grp = '$grp'";
  }else{					///  查詢多筆紀錄
//    $sql .= " AND course_id = '$cou_id' AND grp = '$grp'";
    $sql .= " ORDER BY apply_time";
  }
  
  //echo $sql;
  $STH = $DBH_kiki->query($sql);
  $forms = $STH->fetchAll(PDO::FETCH_ASSOC);
  
  $i = 0;
  foreach($forms as $form) {
    $sql = "SELECT DISTINCT cname, ename FROM a31vallcourse WHERE coursecd = '" . $form['course_id'] . "'";
	$STH = $DBH->query($sql);
	$course = $STH->fetch(PDO::FETCH_ASSOC);
	
//	echo $sql . "<BR>\n";
//	print_r($course);
//	print_r($DBH->errorInfo());
	
	$forms[$i]['cname'] = $course['cname'];
	$forms[$i]['ename'] = $course['ename'];
	$i++;
  }

//    $sql .= " ORDER BY apply_time";
//  echo "<HR>\n";	
//  print_r($forms);
  
  if( empty($forms) ) {								///  抓不到資料
    return(-1);
  }else if( $query_stu_all_applications == 0 ) {	///  查詢單筆紀錄
    return $forms[0];
  }else{
    return $forms;
  }

}
//////////////////////////////////////////////////////////////////////////////////////////
/////  傳回加簽/棄選單中某科目的最大 serialno
function Get_Form_Max_Serialno($cou_id, $grp, $form)
{
  global $DBH;
  //$DBH = PDO_connect();
  
  $tables = array("concent"=>"concent_form", "withdrawal"=>"withdrawal_form");
  
  $sql = "SELECT max(serialno) FROM " . $tables[$form] . " WHERE course_id = '$cou_id' AND grp='$grp'";
  $STH = $DBH->prepare($sql);
  $STH->execute();
  $row = $STH->fetch(PDO::FETCH_NUM);
  
//  echo $sql;
  
  if( $row[0] == "" )  $row[0] = 0;
  return($row[0]);  
}
//////////////////////////////////////////////////////////////////////////////////////////
/////  傳回加簽單中某科目的最大 serialno
function Get_Concent_Form_Max_Serialno($cou_id, $grp)
{
  global $DBH;
  //$DBH = PDO_connect("academic_kiki");
  $sql = "SELECT max(serialno) FROM concent_form WHERE course_id = '$cou_id' AND grp='$grp'";
  $STH = $DBH->prepare($sql);
  $STH->execute();
  $row = $STH->fetch(PDO::FETCH_NUM);  
//  echo $sql;
  
  if( $row[0] == "" )  $row[0] = 0;
  return($row[0]);  
}
//////////////////////////////////////////////////////////////////////////////////////////
/////  學生申請加簽
/////  執行 SQL INSERT 
/////  此處還不能寫入 local file，因為審核核可了才可，以便接軌舊的 Course_Upper_Limit_Immune 相關函式!
function Concent_Form_Stu_Apply($stu_id, $cou_id, $grp)
{
  global $YEAR, $TERM, $DBH;
  
  $serialno = Get_Concent_Form_Max_Serialno($cou_id, $grp) + 1;
  list($t, $now, $t2) = gettime("");
  
  $sql = "INSERT INTO concent_form
            (year, term, course_id, grp, stu_id, serialno, verified, apply_time)
          VALUES
            ('$YEAR', '$TERM', '$cou_id', '$grp', '$stu_id', $serialno, '0', '$now')";
  $STH = $DBH->query($sql);
  if( $STH === FALSE ) {
    echo "申請加簽出現內部錯誤，請洽電算中心校內分機 14203!";
	//print_r($DBH->errorInfo());
    die();
  }else{
    return 1;
  }
}

//////////////////////////////////////////////////////////////////////////////////////////
/////  棄選單學生申請狀態狀態
/////  傳入值：(學號、只抓回特定狀態的棄選資料、學年、學期)
/////  $status 的值：[NULL, "verified", "all"] 
/////              = [只抓回現在作用中的棄選單(不管是否審核過)、只抓回已核可、抓取全部]
/////  回傳值：
/////    不要包含已取消的資料：傳回單筆紀錄，或是 -1 代表尚未申請, -2 代表已經有資料核可（不可再申請）
/////    只抓回已核可：		   傳回單筆紀錄，或是 -1 代表不存在
/////    要包含已取消的資料：  傳回多筆紀錄，或是 -1 代表尚未申請
function Withdrawal_Form_Apply_Status($stu_id, $status=NULL, $year, $term)
{
  global $YEAR, $TERM, $DATABASE_NAME, $DBH;
  if( $year == "" )  $year = $YEAR;
  if( $term == "" )  $term = $TERM;
  
  $table = "withdrawal_form";
  
//  echo "[$year, $term, $stu_id, $query_stu_all_applications]<BR>";

  $sql = "SELECT DISTINCT year, term, course_id, grp, stu_id, verified, apply_time, verify_time
            FROM $table
           WHERE year = '$year'
             AND term = '$term'
             AND stu_id = '$stu_id'";

  if( $status == "all" ) {								///  抓取全部
    $sql .= " ORDER BY apply_time";
//  echo $sql;
    
    $STH = $DBH->prepare($sql);
	$STH->execute();
	$rows = $STH->fetchAll(PDO::FETCH_ASSOC);
    
    if( $rows == false ) {
      return(-1);
    }else{
      return $row;
    }    
  }else if( $status == "verified" ) {					///  只抓回已審核的(最多應該只有一筆)
    $sql .= " AND verified = '1'";
	
	//echo $sql . "<BR>\n";
	$STH = $DBH->prepare($sql);
	$STH->execute();
	$row = $STH->fetch(PDO::FETCH_ASSOC);
	if( $row == false ) {
      return(-1);
    }else{
      return $row;
    }    
  }else{												///  只抓回現在作用中的棄選單(應該只會有一筆)
	$sql .= " AND COALESCE(verified, '') = ''";				/// 不抓取狀態為 'a'(abandoned) 的紀錄
	
    //echo $sql;
	
    $STH = $DBH->prepare($sql);
	$STH->execute();
	$row = $STH->fetch(PDO::FETCH_ASSOC);

	if( $row == false ) {			///  如果抓不到資料，還要確認一下是否已經有核可的棄選單
	  $sql = "SELECT count(*) FROM $table
           WHERE year = '$year'
             AND term = '$term'
             AND stu_id = '$stu_id'
			 AND verified = '1'";
	  $STH = $DBH->prepare($sql);
	  $STH->execute();
	  $row2 = $STH->fetch(PDO::FETCH_NUM);
	  if( $row2[0] != 0 ) {
	    return(-2);
	  }else{
	    return(-1);
	  }
	}else{
	  return $row;
	}
  }
}

//////////////////////////////////////////////////////////////////////////////////////////
/////  學生申請棄選
/////  執行 SQL INSERT 
function Withdrawal_Form_Stu_Apply($stu_id, $cou_id, $grp)
{
  global $YEAR, $TERM, $DBH, $system_settings;
  
  if( !isset($system_settings) )   $system_settings = Get_System_State();
  if( $system_settings['redirect_to_query'] == 1 ) {			//  判別 year, term 該是這學期還是「上學期」
    list($year, $term) = Last_Semester(1);  
  }else{
    $year = $YEAR;
	$term = $TERM;
  }
  //$serialno = Get_Form_Max_Serialno($cou_id, $grp, "withdrawal") + 1;
  list($t, $now, $t2) = gettime("");
  
  $sql = "INSERT INTO withdrawal_form
            (year, term, course_id, grp, stu_id, verified, apply_time)
          VALUES
            ('$year', '$term', '$cou_id', '$grp', '$stu_id', '', '$now')";
  $STH = $DBH->query($sql);

  if( $STH === FALSE ) {
    echo "申請棄選出現內部錯誤，請洽電算中心校內分機 14203!";
    print_r($DBH->errorInfo());
    die();
  }else{
    return 1;
  }
}

//////////////////////////////////////////////////////////////////////////////////////////
/////  學生「放棄」棄選
/////  執行 SQL DELETE
function Withdrawal_Form_Stu_Abandon($stu_id, $cou_id, $grp)
{
  global $YEAR, $TERM, $DBH;
  //$serialno = Get_Form_Max_Serialno($cou_id, $grp, "withdrawal") + 1;
  list($t, $now, $t2) = gettime("");
  
/*  $sql = "DELETE FROM withdrawal_form
          WHERE year = '$YEAR'
		    AND term = '$TERM'
			AND course_id = '$cou_id'
			AND grp = '$grp'
			AND stu_id = '$stu_id'";
*/
  $sql = "UPDATE withdrawal_form
		  SET verified = 'a'
          WHERE year = '$YEAR'
		    AND term = '$TERM'
			AND course_id = '$cou_id'
			AND grp = '$grp'
			AND stu_id = '$stu_id'";
//  die($sql); 
  $STH = $DBH->query($sql);
  
  if( $STH === FALSE ) {
    echo "申請棄選出現內部錯誤，請洽電算中心校內分機 14203!";
    print_r($DBH->errorInfo());
    die();
  }else{
    return 1;
  }
}
//////////////////////////////////////////////////////////////////////////////////////
/////  抓取課程地圖中「我的選課計畫」資料，
/////  檢查其中哪些課程是本學期有開設的，並回傳這些課程資料。
/////  輸入： $sid = 學生學號
/////  輸出： $my_plan_course = 課程資料陣列(同一科目不同班別視為一科)
function Get_My_Plan_Course($sid) 
{
  global $DBH, $IS_GRA, $DEPT_CGE;
  $DBH_a = PDO_connect("academic");
  $DBH_map = PDO_connect("coursemap");
  
  $student_course = Course_of_Student($sid);
  if( $student_course ) {
    foreach( $student_course as $course ) {
      $stu_cour[$course["id"]] = 1;				///  學生本學期已選修科目資料
	}
  }
  $student_grade = Get_Student_Grade($sid);
  $stu_cour_pass = array();
  foreach( $student_grade as $grade ) {
    if( Grade_Pass($sid, $grade["trmgrd"], $grade["property"], $IS_GRA) )  {
	  $stu_cour_pass[$grade["cid"]] = 1;		///  學生過往已選修並通過的科目資料
	}
  }  
   
//  print_r($stu_cour_pass);
  
  /////  sql 特別排除系所代碼 7006，以避免與本系統內使用的通識代碼 I001 重複
  /*$sql = "SELECT DISTINCT mp.cid, ac.deptcd
            FROM a36vmy_plan as mp, a31vallcourse as ac
           WHERE mp.cid = ac.coursecd
		     AND deptcd != '7006'
		     AND sid = ?";
  
  $sth = $DBH->prepare($sql);
  $sth->execute(array("$sid"));  
  */
  $sql = "SELECT cid FROM a36tmy_plan WHERE sid = ?";
  $STH = $DBH_map->prepare($sql);
  $STH->execute(array("$sid"));
  $my_plan = $STH->fetchAll(PDO::FETCH_ASSOC);
  
  $i=0;
  //while( $row = $sth->fetch(PDO::FETCH_ASSOC) ) {
  $my_plan_course = array();
  foreach( $my_plan as $row ) {
    $sql = "SELECT deptcd FROM a31vallcourse WHERE coursecd = '" . $row['cid'] . "' AND deptcd != '7006'";
	$STH = $DBH_a->query($sql);
	$temp = $STH->fetch(PDO::FETCH_ASSOC);
	$my_plan[$i]['deptcd'] = $temp['deptcd'];
	$row['deptcd'] = $temp['deptcd'];
	
    if( $row["deptcd"] == "7006" )	$row["deptcd"] = $DEPT_CGE;
//	echo "row: ";
//	print_r($row);
	$course = Read_Course($row["deptcd"], $row["cid"], "01");
	$my_plan_course[$i] = $row;
	$dept_data = Read_Dept($row["deptcd"]);
//	echo "course : ";
//	print_r($course);
	
	if( array_key_exists("ename", $course) ) {			/// 如果當學期有開課
	  $my_plan_course[$i]["cname"]		= $course["cname"];
	  $my_plan_course[$i]["ename"]		= $course["ename"];
	  $my_plan_course[$i]["dept_name"]	= $dept_data["cname"];
	  $my_plan_course[$i]["dept_ename"]	= $dept_data["ename"];
	  $my_plan_course[$i]["grade"]		= $course["grade"];
	  
//	  echo "stu_cour_pass of " . $row["cid"] . " is " . $stu_cour_pass["cid"] . "<BR>\n";
	  if( isset($stu_cour) && array_key_exists($row["cid"], $stu_cour) && $stu_cour[$row["cid"]] == 1 ) {
		$my_plan_course[$i]["sel_status"] = 1;			///  當學期已選修
	  }else if( array_key_exists($row["cid"], $stu_cour_pass) && $stu_cour_pass[$row["cid"]] == 1 ) {
	    $my_plan_course[$i]["sel_status"] = 2;			///  過去已選修並通過
	  }else{
	    $my_plan_course[$i]["sel_status"] = 0;			///  其他(可點選以加選)
	  }
		
	  //print_r($my_plan_course);
	  //echo "course " . $row["cid"] . " exists : " .  $course["cname"] . "<BR>\n"; 
	}else{
	  unset($my_plan_course[$i]);
	}
	$i++;
  }
  return($my_plan_course);
}


/////  管理者審核加簽單
/////  除了寫入 table 外，還要在 local file 寫入資料，以便 perl 程式讀取
function Concent_Form_SU_Verify()
{

}

/////////////////////////////////////////////////////////////////////////////////////////
/////  抓取學生在課程地圖「我的客製化學程」中，預定要修習的科目清單資料。
/////  只抓取已經核可的資料。
/////  輸入： $sid = 學生學號
/////  輸出： $my_program_courses = 課程資料陣列(同一科目不同班別視為一科)

function Get_My_Program_Course($sid) 
{
  $DBH_map = PDO_connect("coursemap");
  
  if( $sid == "999999999" )  $sid = 'guest';            ///  轉換為課程地圖中的訪客帳號
  
  $sql = "
    SELECT MPC.course_id
      FROM a36tmy_program MP, a36tmy_program_course MPC
     WHERE MP.std_no = MPC.std_no
       AND MP.status = '1'
       AND MP.std_no = ?
  ";
  
  $STH = $DBH_map->prepare($sql);
  $STH->execute(array($sid));
  //$my_program_courses = $STH->fetchAll(PDO::FETCH_NUM);
  while( $row = $STH->fetch(PDO::FETCH_NUM) ) {
    $my_program_courses[] = $row[0];
  }
 
  return $my_program_courses;
}
/*
/////////////////////////////////////////////////////////////////////////////////////////
/////  尚待加入的（目前只有 perl 版本有的）函式：
/////  2014/10/14
function Add_Student_Course($student_id,$course_dept,$course_id,$course_group,$property)
{}
function Delete_Student_Course($student_id,$course_dept,$course_id,$course_group,$by_whom)
{}
function Delayed_Delete_Student_Course($student_id,$course_dept,$course_id,$course_group,$by_whom)
{}
function Upper_Limit_Immune_Delete($course_id, $course_group, $stu_id)
{}
function Get_My_Table($id, $free_flag)
{}
function Lower_Credit_Limit($student)
{}
function Check_Ban_Limit($Ban_Dept_Num, $Ban_Grade_Num, $Ban_Class_Num)
{}
function Stu_Can_Apply_Concent_Form($Student, $the_Course, $Course_of_Student, $student_count)
{}
*/


?>