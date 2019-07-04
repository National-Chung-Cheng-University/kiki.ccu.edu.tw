<?php
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_qualify_english.php
  /////  更新學生英文檢定成績資料 qualify_english.txt
  /////  Coder: Nidalap :D~
  /////    2006/11/30  Created
  /////    2011/09/21  與語言中心恬恬討論後，得知不需此名單！從此廢除！ Nidalap :D~
  ////////////////////////////////////////////////////////////////////////////

  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename   = "qualify_english.txt";
  $outputfile = $DATA_PATH . "Grade/" . $filename;

  $time_start = time();
  
  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>更新學生英文檢定成績檔</H1><HR>");

  db_connect();
  $query_string = "
        SELECT * FROM a12tqualify_english
  ";
  
#  echo("$query_string,$link<BR>"); 
  $result_id	= sybase_query($query_string,$link);
  $rowcount	= sybase_num_rows($result_id);

#  print("[outputfile, result_id, rowcount] = [$outputfile, $result_id, $rowcount]<BR>\n");
      
  $save_succeed = Save_Update_File($outputfile, $result_id, $rowcount);

  $time = time() - $time_start;
  if( $save_succeed == 0 ) {
    echo("存檔失敗! 可能是檔案權限問題 $outputfile \n");
  }else{
    echo("更新 $filename               : $rowcount 筆資料, 耗時 $time 秒<P>\n");
    echo("更新完畢!<HR><P>\n");    
  }

  Update_Log($filename, $rowcount, $time);
 
?>

<INPUT type=button value="關閉視窗" onClick="window.close()">
