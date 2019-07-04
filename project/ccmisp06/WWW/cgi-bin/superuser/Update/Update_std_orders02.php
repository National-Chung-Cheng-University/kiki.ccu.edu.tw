<?php
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_std_orders.php
  /////  更新學生歷年排名資料 std_orders.txt
  /////  Updates: 
  /////    2006/09/26  Coder: Nidalap :D~
  /////    2012/10/30  改採 PDO 連資料庫 by Nidalap :D~
  ////////////////////////////////////////////////////////////////////////////

  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Database.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename   = "std_orders.txt";
  $outputfile = $DATA_PATH . "Grade/" . $filename;

  $time_start = time();
  
  echo $EXPIRE_META_TAG;
  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>更新學生歷年排名檔</H1><HR>");

  $DBH = PDO_connect($DATABASE_NAME);
  $query_string = "
  	SELECT a12this_tot_avg.year,   
         	a12this_tot_avg.term,   
         	a12this_tot_avg.std_no,   
         	a12this_tot_avg.order_s  
    	FROM a12this_tot_avg  
   	WHERE 
       		a12this_tot_avg.std_no in (  SELECT a11tstd_rec.std_no  
                                        FROM a11tstd_rec )  
	ORDER BY a12this_tot_avg.std_no ASC,   
         	a12this_tot_avg.year ASC,   
         	a12this_tot_avg.term ASC
  ";
  
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
