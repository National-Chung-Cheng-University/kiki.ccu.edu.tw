<?php
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_grade_now.php
  /////  更新學生當學期成績資料 now.txt
  /////  Updates: 
  /////    2006/09/21 Coder: Nidalap :D~
  /////    2012/10/31 改採 PDO 連資料庫 by Nidalap :D~
  ////////////////////////////////////////////////////////////////////////////

  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Database.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename   = "now.txt";
  $outputfile = $DATA_PATH . "Grade/" . $filename;

  $time_start = time();
  
  echo $EXPIRE_META_TAG;
  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>更新當學期成績檔</H1><HR>");          

  //$DBH = PDO_connect($PUBLIC_DB_NAME);
  $DBH = PDO_connect();
  
  if ( $IS_GRA == 1 ) {					///  依正式/專班, 選擇不同的 view
    $table	= "zv_student_at_ccu_grade_nowpay";
  }else{
    $table	= "zv_student_at_ccu_grade_now";
  }
  $query_string	= "select * from " . $table . " order by std_no";
  
//  echo("$query_string<BR>"); 
  $STH = $DBH->prepare($query_string);
  $STH->execute();
  list($save_succeed, $rowcount) = Save_Update_File_PDO($outputfile);

  $time = time() - $time_start;
  if( $save_succeed == 0 ) {
    echo("存檔失敗! 可能是檔案權限問題\n");
  }else{
    echo("更新 $filename               : $rowcount 筆資料, 耗時 $time 秒<P>\n");
    echo("更新完畢!<HR><P>\n");    
  }

  Update_Log($filename, $rowcount, $time);
 
?>

<INPUT type=button value="關閉視窗" onClick="window.close()">
