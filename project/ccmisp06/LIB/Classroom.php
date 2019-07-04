<?PHP
//////////////////////////////////////////////////////////////
/////  Classroom.php
/////  處理教室資料
/////  若有輸入值 input_id，傳回該教室資料；若無，則傳回所有教室資料。
/////  Updates:
/////    2012/06/28 從 Classroom.pm 修改而來  by Nidalap :D~ 
/////    2016/06/01 將參考檔案 $ClassFile 改為讀取在 ccmisp06 的 $MAIN_HOME_PATH1 的資料。 by Nidalap :D~

function Read_Classroom($input_id="")
{
  global $REFERENCE_PATH, $MAIN_HOME_PATH1;
  
  //$ClassFile = $REFERENCE_PATH . "classroom.txt";
  $ClassFile = $MAIN_HOME_PATH1 . "DATA/Reference/classroom.txt";
  
  $CLASS = fopen($ClassFile, "r") or die("Cannot open file $ClassFile!\n");
  while($temp = fgets($CLASS) )  $lines[] = $temp;
  fclose($CLASS);
  foreach( $lines as $line ) {
    $line = chop($line);
    list($id, $c{"cname"}, $c{"report_dept"}, $c{"size_fit"}, 
         $c{"allow_add"}, $c{"size_max"} ) 
         = preg_split("/\t/", $line);
    if( $input_id != "" ) {			///  如果只抓取一個教室資料
      if( $input_id == $id ) {
        $c{"id"} = $id;
        return $c;				///    抓到該筆資料，return!
      }
    }else{					///  如果要抓取所有教室資料
      $class{$id} = $c;				///    就將該資料一筆一筆存到 $class
    }
  }
  if( $input_id != "" ) {			///  如果只抓取一個教室資料，到頭來都沒有符合項目
    $class{"id"}        = "";			///    那就回傳空值			
    $class{"cname"}     = "";
  }
  return $class;				///  回傳所有教室資料
}


?>