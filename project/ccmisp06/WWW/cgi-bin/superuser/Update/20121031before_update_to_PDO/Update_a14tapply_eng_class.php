<?PHP
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_a14tapply_eng_class.php
  /////  更新應用英外語學程生名單.
  /////  Coder: Nidalap :D~
  /////  2010/12/29
  ////////////////////////////////////////////////////////////////////////////
  
  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename   = "a14tapply_eng_class.txt";  
  $outputfile = $REFERENCE_PATH . $filename;
  $time_start = time();

  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>更新開課代碼檔</H1><HR>");            
  db_connect();
//  $query_string = "";
  $query_string = "
     SELECT a14tapply_eng_class.year,
            a14tapply_eng_class.term,
            a14tapply_eng_class.std_no,
            a14tapply_eng_class.type
       FROM a14tapply_eng_class 
  ";
    
  $result_id	= sybase_query($query_string, $link);
  $rowcount	= sybase_num_rows($result_id);
//  $columncount	= sybase_num_fields($result_id);
  
  $save_succeed = Save_Update_File($outputfile, $result_id, $rowcount);
  
  $time = time() - $time_start;
  if( $save_succeed == 0 ) {
    echo("存檔失敗! 可能是檔案權限問題\n");
    echo sybase_get_last_message();
  }else{
    echo("更新 $filename		: $rowcount 筆資料, 耗時 $time 秒<P>\n");
    echo("更新完畢!<HR><P>\n");
  }
  
  Update_Log($filename, $rowcount, $time);
    
?>

<INPUT type=button value="關閉視窗" onClick="window.close()">
