<?PHP
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_minor.php
  /////  更新輔系名單 minor.txt
  /////  Coder: Nidalap :D~
  /////  2006/09/25
  ////////////////////////////////////////////////////////////////////////////
  
  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";
  
  $filename   = "fu.txt";
  $outputfile = $REFERENCE_PATH . $filename;
  $time_start = time();

  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>更新輔系名單</H1><HR>");
  db_connect();

  $query_string = "
      SELECT a30tminor.dept,   
             a30tminor.std_no  
      FROM a30tminor 
      WHERE std_no in (
        SELECT a11tstd_rec.std_no  
        FROM a11tstd_rec  
        WHERE a11tstd_rec.status = '0' )";
    
  $result_id	= sybase_query($query_string, $link);
  $rowcount	= sybase_num_rows($result_id);
//  $columncount	= sybase_num_fields($result_id);
  
  $save_succeed = Save_Update_File($outputfile, $result_id, $rowcount);
  
  $time = time() - $time_start;
  if( $save_succeed == 0 ) {
    echo("存檔失敗! 可能是檔案權限問題\n");
  }else{
    echo("更新 $filename		: $rowcount 筆資料, 耗時 $time 秒<P>\n");
    echo("更新完畢!<HR><P>\n");
  }
  
  Update_Log($filename, $rowcount, $time);
    
?>

<INPUT type=button value="關閉視窗" onClick="window.close()">
