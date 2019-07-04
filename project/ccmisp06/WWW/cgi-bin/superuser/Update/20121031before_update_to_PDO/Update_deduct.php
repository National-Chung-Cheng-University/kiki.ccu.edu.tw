<?PHP
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_deduct.php
  /////  更新學生抵免成績 deduct.txt
  /////  Coder: Nidalap :D~
  /////  2006/09/20
  ////////////////////////////////////////////////////////////////////////////
  
  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename = "deduct.txt";  
  $outputfile = $DATA_PATH . "Grade/" . $filename;
  $time_start = time();

  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>更新抵免成績檔</H1><HR>");            
  db_connect();
  $query_string = "
    SELECT a12tdeduct.std_no,   
         a12tdeduct.cour_cd,   
         a12tdeduct.d_year,   
         a12tdeduct.d_term,   
         a12tdeduct.d_cour_cd,   
         a12tdeduct.credit,   
         a12tdeduct.curattr  
    FROM a12tdeduct  
    WHERE std_no in (  SELECT a11tstd_rec.std_no  
    FROM a11tstd_rec)";
    
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
