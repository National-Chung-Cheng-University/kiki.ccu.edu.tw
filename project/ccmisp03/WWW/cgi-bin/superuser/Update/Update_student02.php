<?php
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_student.php
  /////  更新學生學籍資料檔
  /////  Coder: Nidalap :D~
  /////  2006/09/22
  ////////////////////////////////////////////////////////////////////////////

  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename   = "student.txt";
  $outputfile = $DATA_PATH . "Reference/" . $filename;
//  $outputfile = "./ccc.txt";

  $time_start = time();

  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>更新學籍資料檔</H1><HR>");  
  
  db_connect();
  
  $query_string	= 
    "SELECT now_dept,now_grade, now_class, enroll ,status, std_no,personid,sex_id, name 
     FROM a11tstd_rec  where (status = '0') ";
  if( $include_rest == 1) {			//  如果包含預計復學生
    $query_string .=
      "OR 
        (status  = '5' and std_no in (select  std_no from a11trest_std_rec where 
        ryear = '" . $YEAR ."' and rterm = '" . $TERM . "' and (syear <> '" . $YEAR 
        . "' or sterm <> '". $TERM ."'))
        and std_no not in (select  std_no from a11trest_std_rec where 
        syear = '" . $YEAR ."' and sterm = '" . $TERM . "'))";
  }
  $query_string .= "order by 1 ,6";    

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
    echo("請繼續執行<BR><A href=Update_student03.cgi>更新資料第二步</A>");
  }

  Update_Log($filename, $rowcount, $time);
 
?>
