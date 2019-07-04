<?php
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_grade_all02.php
  /////  更新學生歷年成績資料
  /////  Coder: Nidalap :D~
  /////  Updates:
  /////    2009/12/18 Created by Nidalap :D~
  /////    2010/06/24 存檔檔名將學年學期隔開，以避免民國百年 bug Nidalap :D~
  ////////////////////////////////////////////////////////////////////////////

  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $year = $_POST["year"];
  $term = $_POST["term"];
  
  $filename   = $year . "_" . $term . ".txt";
  $outputfile = $DATA_PATH . "Grade/score/" . $filename;
//  $outputfile = "./ccc.txt";

  $time_start = time();
  
  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>更新歷年成績檔</H1><HR>");

  db_connect_public();
  if ( $IS_GRA == 1 ) {					///  依正式/專班, 選擇不同的 view
    $table	= "zv_student_at_ccu_grade_allpay";
  }else{
    $table	= "zv_student_at_ccu_grade_all";
  }
  if( substr($year,0,1) == 0 )  $year = substr($year,1,2);   /// 資料庫的 year 是 98 而非 098
  $query_string	= "select * from " . $table . " WHERE year='" . $year . "' and term='" . $term . "' order by std_no";
  
//  echo("$query_string,$link<BR>"); 

  $result_id	= sybase_query($query_string,$link);
  $rowcount	= sybase_num_rows($result_id);

//  print("[outputfile, result_id, rowcount] = [$outputfile, $result_id, $rowcount]<BR>\n");
      
  $save_succeed = Save_Update_File($outputfile, $result_id, $rowcount);

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
