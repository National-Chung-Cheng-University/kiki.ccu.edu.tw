<?php
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_grade_now.php
  /////  更新學生當學期成績資料 now.txt
  /////  Coder: Nidalap :D~
  /////  2006/09/21
  ////////////////////////////////////////////////////////////////////////////

  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename   = "now.txt";
  $outputfile = $DATA_PATH . "Grade/" . $filename;
//  $outputfile = "./ccc.txt";

  $time_start = time();
  
  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>更新當學期成績檔</H1><HR>");          

  db_connect_public();
  if ( $IS_GRA == 1 ) {					///  依正式/專班, 選擇不同的 view
    $table	= "zv_student_at_ccu_grade_nowpay";
  }else{
    $table	= "zv_student_at_ccu_grade_now";
  }
  $query_string	= "select * from " . $table . " order by std_no";
  
  echo("$query_string,$link<BR>"); 
  $result_id	= sybase_query($query_string,$link);
  $rowcount	= sybase_num_rows($result_id);

  print("[outputfile, result_id, rowcount] = [$outputfile, $result_id, $rowcount]<BR>\n");
      
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
