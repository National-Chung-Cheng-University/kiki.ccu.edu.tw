<?PHP

/////////////////////////////////////////////////////////////////////////////////////////////////
/////  Grade.php
/////  存取學生成績資料檔
/////  Updates:
/////    2011/03/22 從 perl 版本改寫 Nidalap :D~
/////    2012/11/06 改採 PDO 連線資料庫 Nidalap :D~
////////////////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////////////////////
/////  判斷此學生此分數是否通過
/////  2012/06/06 加入輸入參數 $property, $is_gra，
/////             用以判斷研究生選修「大學部課程」、「教育學程」、(專班)基礎課程  Nidalap :D~
function Grade_Pass($stu_id, $grade, $property, $is_gra) 
{
//  echo "Grade_Pass [ $stu_id, $grade, $property, $is_gra ] <BR>\n";
  $type = substr($stu_id, 0, 1);
  if( ($type=="4") or ($property==6)or($property==7) )	///  大學生、以及研究生選「大學部課程」或「教育學程」
    $pass_grade = 60;
  else if( ($property==4) and ($is_gra==1) ) 		///  專班學生選修「基礎課程」
    $pass_grade = 60;
  else
    $pass_grade = 70;
  
  if( $grade >= $pass_grade )	return 1;
  else				return 0;
}
////////////////////////////////////////////////////////////////////////////////////////////////
/////  從 public_db 的 view 抓取學生當學期/歷年成績資料
function Read_Grade_From_DB($stu_id)
{
  global $IS_GRA, $USE_TEST_DATABASE;
  //db_connect_public();
  $DBH = PDO_connect();

  if ( $IS_GRA == 1 ) {                                 ///  依正式/專班, 選擇不同的 view
    $table_now	= "zv_student_at_ccu_grade_nowpay";
    $table_his	= "zv_student_at_ccu_grade_allpay";
  }else{
    $table_now	= "zv_student_at_ccu_grade_now";
    $table_his	= "zv_student_at_ccu_grade_all";
  }
  if( $USE_TEST_DATABASE ) {
    $table_his .= "_t";
  }
  ///  讀取當學期成績
  $grade = NULL;
  $sql = "SELECT * FROM " . $table_now . " WHERE std_no = '" . $stu_id . "'";
  $STH = $DBH->prepare($sql);
  $STH->execute();
  while( $temp = $STH->fetch() )  $grade[] = $temp;

  ///  讀取歷年成績
  $sql = "SELECT * FROM " . $table_his . " WHERE std_no = '" . $stu_id . "' ORDER BY year, term";
  $STH = $DBH->prepare($sql);
  $STH->execute();
  while( $temp = $STH->fetch() )  $grade[] = $temp;

//  echo $sql;
  return $grade;
}
////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////  從預先下載好的成績文字檔中，透過 grep 抓取學生的成績
/////  並傳回該學生所有歷年與當學期成績陣列。
  function Get_Student_Grade($id, $year="", $term="")
  {
    global $DATA_PATH, $YEAR, $TERM;

    $grade_path = $DATA_PATH . "Grade/score/";
    if( $year && $term ) {
      if( strlen($year) <= 2 )  $year = "0" . $year;
      $grade_file = $grade_path . $year . "_" . $term;
    }else{
      ///  抓取所有歷年，和當學期成績檔案
      $grade_file = $grade_path . "* " . $grade_path . "../now.txt " . $grade_path . "../summer.txt";    
    }
    $tmpfile = "/tmp/" . $id . ".grade";

//    echo "Retrieving data : $id, $year, $term...<BR>\n"; 
    exec("grep $id $grade_file > $tmpfile");
    $handle = fopen($tmpfile, "r");
    if( !$handle )  die("內部錯誤：無法讀取成績暫存檔, 請洽系統管理員!");
    while($temp = fgets($handle))  $lines[] = $temp;
    fclose($handle);

    $i = 0;
	if( empty($lines) )		$GRA = array();
	else{
      foreach( $lines as $line ) {
        $line = rtrim($line);
        list($tmp, $GRA[$i]["year"], $GRA[$i]["term"], $GRA[$i]["cid"], $GRA[$i]["grp"], $GRA[$i]["total_time"],
              $GRA[$i]["property"], $GRA[$i]["trmgrd"], $GRA[$i]["credit"], $GRA[$i]["cname"] )
          = preg_split("/\t/",$line);
        $GRA[$i]["year"] = rtrim($GRA[$i]["year"]);

        if( $GRA[$i]["property"] == "9" )  {             ###  屬性欄==9, 是為棄選
          $GRA[$i]["trmgrd"] = "棄選";
        }
        $i++;
      }
	}
/*    krsort($GRA);
    foreach( $GRA as $year=>$GR ) {
      foreach( $GR as $term=>$G )   {
        ksort($G);
      }
    }
*/
    return($GRA);
  }
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////  從預先下載好的排名文字檔，透過 grep 抓取
/////  並傳回該學生所有歷年與當學期排名陣列。

  function Get_Student_Order($input_id)
  {
    global $DATA_PATH;

    $order_file = $DATA_PATH . "Grade/std_orders.txt";
    $handle = fopen($order_file, "r");
    if( !$handle )  die("內部錯誤：無法讀取排名資料檔，請洽系統管理員！");
    while( $temp = fgets($handle) )  $lines[] = $temp;
    fclose($handle);

    foreach($lines as $temp_order) {
      list($year, $term, $id, $order) = preg_split("/\s+/", $temp_order);
      if( $id == $input_id ) {
        $std_order[$year][$term] = $order;
      }
    }
    return($std_order);
  }
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/*function Read_Grade_From_DB($stu_id)
{
  global $DATA_PATH;
  
  
  


}
*/
?>