<?PHP
///////////////////////////////////////////////////////////////////////////////////////////
/////  Course.php
/////  Course.pm 的 PHP 版本，用來讀取一些開課資料
/////  Updates:
/////    2011/08/04 從 Course.pm 改寫，目前只有 Read_Course().  Nidalap :D~
///////////////////////////////////////////////////////////////////////////////////////////

/////  Find_All_Course
/////  找出某系所所有開課資料
/////  詳見 perl 版本 @ Course.pm
function Find_All_Course($dept, $grade, $year="", $term="", $history_flag="")
{
  global $YEAR, $TERM, $HISTORY_PATH, $CHANGE_COURSE_PATH, $COURSE_PATH;
  
  if( $year == "" )  $year=$YEAR;
  if( $term == "" )  $term=$TERM;
  
  if( ($year == "history") or ($year == "HISTORY") ) {			  /// 所有歷年開課檔
    $course_path = $HISTORY_PATH."Course/".$dept."/";   
  }else if( $year == "change" ) {                                 /// 開課異動前的開課檔
    $course_path = $CHANGE_COURSE_PATH . $dept . "/";
  }else if( !(($year == $YEAR) and ($term == $TERM))) {           /// 特定某學期開課資料  
    $course_path = $HISTORY_PATH . "Course_last/" . $year . "_" . $term . "/" . $dept . "/";  
  }else{								  ### 目前開課檔
    $course_path = $COURSE_PATH.$dept."/";
  }

  //print("Trying to locate $course_path<BR>\n");
  
  $index_file = $course_path . "classindex";
  if( !file_exists($index_file) ) {
	return(NULL);
  }
  if( !($handle = fopen($index_file, "r")) )  return(NULL);
  while( $temp  = fgets($handle) )  $lines[] = $temp;
  fclose($handle);

//  print_r($lines);
//  echo "<HR>\n\n\n";
  
  $i=0;
  foreach($lines as $line) {
    $line = rtrim($line);
    list($course[$i]['id'], $course[$i]['grade'], $course[$i]['grp']) = preg_split("/\s+/", $line);
	$i++;
  }
//  print_r($course);
  return($course);
}

/////////////////////////////////////////////////////////////////////////////////////////
function Read_Course($dept, $cid, $group, $year="", $term="")
{
  global $YEAR, $TERM, $LIBRARY_PATH, $HISTORY_PATH, $COURSE_PATH;

  require_once $LIBRARY_PATH . "Error_Message.php";

  $course["dept"]	= $dept;
  $course["id"]		= $cid;
  $course["group"]	= $group;
/*   my(%course, $history_flag, $course_exists_flag);
   my($course_path, $course_file, @lines, $temp, $i, $j, $id, $grade, $group);
   my($dept_temp, $pre_course_temp, $grade_temp);
*/

//   ($course{dept},$course{id},$course{group},$year, $term, $stu_id) = @_;
//  print("$course{dept},$course{id},$course{group},$year, $term, $stu_id<BR>\n");

  if( $year=="" )  $year = $YEAR;
  if( $term=="" )  $term = $TERM;

//  print("$dept,$cid,$group,$year, $term<BR>\n");

   if( ($year == "history") or ($year == "HISTORY") ) {                   ### 所有歷年開課檔
      $course_path = $HISTORY_PATH."Course/".$dept."/";
   }else if( $year == "change" ) {                                          ### 開課異動前的開課檔
      $course_path = $CHANGE_COURSE_PATH . $dept . "/";
   }else if( !(($year == $YEAR)and($term == $TERM))) {                    ### 特定某學期開課資料
      $course_path = $HISTORY_PATH . "Course_last/" . $year . "_" . $term . "/" . $dept . "/";
   }else{                                                                 ### 目前開課檔
      $course_path = $COURSE_PATH.$dept."/";
   }

//   print("Trying to locate $course_path<BR>\n");

   $index_file = $course_path . "classindex";

   if( !($handle = fopen($index_file, "r")) )  return;

//     print("Cannot open file $index_file in Course::Read_Course() from $stu_id!<BR>\n");

   while( $temp  = fgets($handle) )  $lines[] = $temp;
   fclose($handle);
 
//   echo "<HR>\n";
//   print_r($lines);
//   echo "<HR>\n";
  
//   @lines = <INDEX>;
//   close(INDEX);
   $course_exists_flag = 0;
   foreach($lines as $line) {
     $line = rtrim($line);
     list($id, $grade, $grp) = preg_split("/\s+/", $line);
     if( ($cid == $id) and ($group == $grp) ) {
       $course_exists_flag = 1;
       $course["grade"]=$grade;
     }
   }
//   print_r($course);

   if( $course_exists_flag !=1 )  {             ### 如果在 classindex 中沒有讀到該課程
     $course["cname"]     =       "<FONT color=RED>(此科目已取消)</FONT>";
     return($course);
   }
   $course_file = $course_path . $course["id"] . "_" . $course["group"];
   
   //echo "Trying to open course file $course_file...<BR>\n";
   
   if( !($handle = fopen($course_file, "r")) )  return;
   $lines = NULL;
   while( $temp  = fgets($handle) )  $lines[] = $temp;
   fclose($handle);

   for($i=0; $i<sizeof($lines); $i++) {
     $lines[$i] = rtrim($lines[$i]);
   }

   $course["cname"]       =       $lines[0];
   $course["ename"]       =       $lines[1];
   global $IS_ENGLISH;							### 因應英文版新增此欄位 2015/05/11 Nidalap :D~
   if( isset($IS_ENGLISH) ) {
     $course["name"] = $course["ename"];
   }else{
	 $course["name"] = $course["cname"];
   }
   $course["total_time"]  =       $lines[2];   ### 發現時數和學分顛倒!!!
   $course["credit"]      =       $lines[3];   ### Nov22,1999發現並修正(Nidalap)
   $course["classroom"]   =       $lines[4];
   $course["property"]    =       $lines[5];
   $temp                  =       $lines[6];
      $course["teacher"] = preg_split("/\s+/",$temp);
   $temp                  =       preg_split("/\s+/",$lines[7]);
      for($i=0, $j=0; isset($temp[$j]); $i++, $j+=2) {
         if( $temp[$j] ) {
           $course["time"][$i]["week"] = $temp[$j];
           $course["time"][$i]["time"] = $temp[$j+1];
         }
      }
//      /////                                     2009/05/10 終於搞定，知道怎麼對這樣的資料結構做 sort  Nidalap :D~
//      @{$course{time}}  =       sort {
//                                      if( $$a{week} eq $$b{week} )      { return ( $$a{time} cmp $$b{time} );  }
//                                      else                              { return ( $$a{week} cmp $$b{week} );  }
//                                     }  @{$course{time}};

   $course["number_limit"]=       $lines[8];

   $course["support_dept"]  = preg_split("/\s+/",$lines[9]);
     if( $course["support_dept"][0]=="" ) $course["support_dept"] = NULL;
   $course["support_grade"] = preg_split("/\s+/",$lines[10]);
     if( $course["support_grade"][0]=="" ) $course["support_grade"] = NULL;
   $course["support_class"] = preg_split("/\s+/",$lines[11]);
     if( $course["support_class"][0]=="" ) $course["support_class"] = NULL;
//     if( (@{$course{support_dept}}!=0) and (@{$course{support_class}}==0) ) {
//       @{$course{support_class}} = @AVAILABLE_CLASSES;         ### 若勾選支援系所卻沒有溝選支援班級，預設為全部
//     }
   $course["ban_dept"]	= preg_split("/\s+/",$lines[12]);
     if( $course["ban_dept"][0]=="" ) $course["ban_dept"] = NULL;
   $course["ban_grade"] = preg_split("/\s+/",$lines[13]);
     if( $course["ban_grade"][0]=="" ) $course["ban_grade"] = NULL;
   $course["ban_class"] = preg_split("/\s+/",$lines[14]);
     if( $course["ban_class"][0]=="" ) $course["ban_class"] = NULL;
   $course["reserved_number"] =   $lines[15];
   $course["principle"]   =       $lines[16];
   $course["suffix_cd"]   =       $lines[17];     ### Apr,2000加入此欄位
   $course["lab_time1"]   =       $lines[18];     ### Apr,2000加入此欄位
   $course["lab_time2"]   =       $lines[19];     ### Apr,2000加入此欄位
   $course["lab_time3"]   =       $lines[20];     ### Apr,2000加入此欄位
   $course["support_cge_type"] =  $lines[21];     ### Nov,2000加入支援通識領域
   $course["support_cge_number"]= $lines[22];     ### Nov,2000加入支援通識人數

   $temp  = preg_split("/\s+/",$lines[23]);  ### Nov,2000加入先修科目,Apr2001修改
   
//   echo $lines[23];
     for($i=0; $i < count($temp); $i++) {
       if( $temp[$i] )  {
         list($dept_temp, $pre_course_temp, $grade_temp) = preg_split("/,/",$temp[$i]);
         $course["prerequisite_course"][$i]["dept"] = $dept_temp;
         $course["prerequisite_course"][$i]["id"]   = $pre_course_temp;
         $course["prerequisite_course"][$i]["grade"]= $grade_temp;
       }
//       print_r($course["prerequisite_course"][$i]);

//     if($grade_temp == "pass") {
#       $course{prerequisite_course}[$i]{grade_show} = "及格";
#     }elsif( $grade_temp == 0 ){
#       $course{prerequisite_course}[$i]{grade_show} = "曾經修習";
#     }else{
#       $course{prerequisite_course}[$i]{grade_show} = "$grade_temp分以上";
#     }
     }
//     if( !$course["prerequisite_course"][0]["id"] ) $course["prerequisite_course"] = NULL;
	 if( !array_key_exists("prerequisite_course", $course) ) 
		$course["prerequisite_course"] = NULL;
          
     

   $course["prerequisite_logic"]  = $lines[24];
   $course["distant_learning"]    = $lines[25];
   $course["english_teaching"]    = $lines[26];
   $course["remedy"]              = $lines[27];   ###  2009/05 加入，暑修課程類型(1為一般，2為補救)
   $course["s_match"]             = $lines[28];   ###  2010/03 加入，教師專長與授課科目是否符合
   $course["gender_eq"]           = $lines[29];   ###  2010/11 加入，性別平等教育課程(0,1)
   $course["env_edu"]             = $lines[30];   ###  2010/11 加入，環境教育相關課程(0,1)
   $course["attr"] 	          = $lines[31];	  ###  2012/04 加入，開課學制(碩士/博士/碩博合開課程)(1,2,3,N)
   $course["open_dept"]           = $lines[32];
   $course["reserved3"]           = $lines[33];
   $course["reserved4"]           = $lines[34];

   $course["note"] = "";
   for( $i=35; isset($lines[$i]); $i++) {     ### 備註
      $course["note"]     =       $course["note"] . $lines[$i];
   }
   $history_file_test = $HISTORY_PATH."Course/".$course["dept"]."/".$course["id"]."_01";

   if( !file_exists($history_file_test) ) {
      $course["isNEW"] = "TRUE";
   }else{
      $course["isNEW"] = "FALSE";
   }
   $course["ename"] = preg_replace("/\n/", "", $course["ename"]);    ### 2005/11/24 發現奇怪bug的修正

//   if( $course["id"] == "7301036" ) {
//     echo "Trying to open course file $course_file...<BR>\n";
//     print_r($course);
//   }

  return $course;
  
}
//////////////////////////////////////////////////////////////////////////////////////////###
/////  判斷該系的「學系服務學習課程」代碼
/////  傳入：系所代碼
/////  傳回：科目代碼
/////  Updates:
/////    2011/04/20 以 perl 版本改寫 by Nidalap :D~
function Get_Dept_Serv_Course_ID($dept)
{
//  my($dept) = @_;
//  my($file, @line, $temp_dept, $temp_cour);
  global $REFERENCE_PATH;  
  
  $file = $REFERENCE_PATH . "dept_serv_course_id.txt";
  $handle = fopen($file, "r") or die("內部錯誤：無法開啟學系服務學習科目對照檔！");
  while( $temp = fgets($handle) )  $lines[] = $temp; 
  fclose($handle);   
    
  foreach ($lines as $line) {
    list($temp_dept, $temp_cour) =  preg_split("/\s+/", $line);
#    print("$temp_dept <-> $dept<BR>");
    if($temp_dept == $dept)  return $temp_cour;		/// 傳回該系的科目代碼 
  }
  return "";                                            /// 比對全部不成功
}
////////////////////////////////////////////////////////////////////////////////////////////////
/////  以通識向度抓取科目清單
/////  傳入：[$category, $subcategory] = [向度代碼, 次向度代碼]
/////  傳回：科目清單 array(含 cid, group)
/////  若沒有傳入向度/次向度代碼，則傳回所有通識科目代碼清單（含向度等欄位）
/////  Updates：
/////    2013/11/26 Created by Nidalap :D~
function Find_All_Course_by_CGE_Category($category=NULL, $subcategory=NULL)
{
  if( !isset($DBH_a) )  $DBH_a = PDO_connect("academic");
  if( ($category==NULL) and ($subcategory==NULL) ) {			///  抓取全部向度
    $sql = "SELECT * FROM a31tcge_category_cour_map";
	$STH = $DBH_a->query($sql);
  }else{													///  抓取特定向度
    $sql = "SELECT * FROM a31tcge_category_cour_map 
             WHERE category = ? AND subcategory = ?
			 ORDER BY cid";
    $STH = $DBH_a->prepare($sql);
    $STH->execute(array($category, $subcategory));
  }  
  
  //echo "returning list of $category _ $subcategory... <BR>\n";
  //echo $sql . "<BR>\n";
  
  $temp = $STH->fetchAll(PDO::FETCH_ASSOC);
  
  if( ($category!=NULL) or ($subcategory!=NULL) ) {		///  抓取特定向度：直接回傳科目清單
    return($temp);
  }else{													///  抓取全部向度：回傳二維陣列科目清單
    foreach($temp as $course) {
	  //$course_list[$course['category']][$course['subcategory']][] = $course;
	  $course_list[$course['cid']]['category']		= $course['category'];
	  $course_list[$course['cid']]['subcategory']	= $course['subcategory'];
	}
    return($course_list);
  }
} 
//////////////////////////////////////////////////////////////////////////////////////////////////
/////  抓取通識向度/次向度(2014以後的新制)
/////  傳入：(無)
/////  傳回：向度/次向度二維陣列
function Get_CGE_Categories()
{
  if( !isset($DBH_a) )  $DBH_a = PDO_connect("academic");
  
  ///  (主)向度資料表
  $sql = "SELECT * FROM a31tcge_category ORDER BY category";
  $STH = $DBH_a->query($sql);
  while( $tmp = $STH->fetch(PDO::FETCH_ASSOC) ) {
    $category[$tmp['category']]['cname'] = $tmp['cname'];
	$category[$tmp['category']]['ename'] = $tmp['e_name'];
  }
  ///  次向度資料表
  $sql = "SELECT * FROM a31tcge_subcategory ORDER BY category, subcategory";
  $STH = $DBH_a->query($sql);
  while( $tmp = $STH->fetch(PDO::FETCH_ASSOC) ) {
    $category[$tmp['category']]['sub'][$tmp['subcategory']]['cname'] = $tmp['cname'];
	$category[$tmp['category']]['sub'][$tmp['subcategory']]['ename'] = $tmp['e_name'];
  }
  
  //print_r($category);
  //echo "<BR>\n";
  
  return($category);
}
///////////////////////////////////////////////////////////////////////////
/////  Read_All_Course_Dept
/////  讀取所有科目的所屬系所
/////  同 Read_Course_Dont_Know_Dept 用意, 但此函式讀取所有開課資料,
/////  並將開課系所紀錄在 hash 中, 如此便可知道某們課開在哪個系所
/////  Updates: 
/////    2016/05/18 從 perl 版本改寫，為求效率加入了 $need_property 參數 XD~
///////////////////////////////////////////////////////////////////////////
function Read_All_Course_Dept($history=NULL, $need_property=0)
{
  $now = time();
  
  $depts = Find_All_Dept();
  foreach($depts as $dept) {
    $course = Find_All_Course($dept, "", $history);	
	
	//echo "course of $dept = ";
	//print_r($course);
	//echo "<P>\n";
	
	if( is_null($course) ) {
	  // echo "course = ";
	  // var_dump($course);
	  continue;
	}
    foreach($course as $cour) {
      $c[$cour['id']]['dept_id']		= $dept;
	  if( $need_property == 1 ) {
		$cou = Read_Course($dept, $cour['id'], $cour['group'], "", "");
		$c[$cour['id']]['property']	= $cou['property'];
	  }
	  #print $$course{id} . " : " . $dept . " : " . $$course_dept{$$course{id}}{dept} . "<BR>\n";
    }
  }
 
  //$time = time() - $now;
  //echo "time: $time<BR>\n";
  //print_r($c);


  return($c);
}



?>