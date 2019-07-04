<?PHP
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_change_school_student.php
  /////  更新轉學生名單 change_school_student.txt
  /////  Coder: Nidalap :D~
  /////  2010/09/17
  ////////////////////////////////////////////////////////////////////////////
  
  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename = "Change_School_Student.txt";  
  $outputfile = $DATA_PATH . "Reference/" . $filename;
  $time_start = time();

  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>更新轉學生名單</H1><HR>");            
  db_connect();
  $query_string = "
	SELECT now_dept,now_grade, now_class, enroll ,status, std_no,personid,sex_id, name 
	  FROM a11tstd_rec  
	 WHERE (status = '0') AND (enrid2cd = '02') 
	   AND year IN ( SELECT a11vyear_max.year FROM a11vyear_max)
        ORDER BY 1 ,6
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
