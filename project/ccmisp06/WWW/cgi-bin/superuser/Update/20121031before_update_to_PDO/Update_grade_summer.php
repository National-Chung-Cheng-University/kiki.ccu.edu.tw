<?php
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_grade_summer.php
  /////  更新學生歷年暑修成績資料 summer.txt
  /////  Coder: Nidalap :D~
  /////  2006/09/26
  ////////////////////////////////////////////////////////////////////////////

  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename   = "summer.txt";
  $outputfile = $DATA_PATH . "Grade/" . $filename;
//  $outputfile = "./ccc.txt";

  $time_start = time();
  
  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>更新歷年暑修成績檔</H1><HR>");

  db_connect();
  $query_string = "
	  SELECT a32t_sel_score_summer.std_no,   
         	a32t_sel_score_summer.year,   
         	a32t_sel_score_summer.term,   
         	a32t_sel_score_summer.cour_cd,   
         	a32t_sel_score_summer.grp,   
         	a32t_sel_score_summer.courkind,   
         	a32t_sel_score_summer.curattr,   
         	a32t_sel_score_summer.trmgrd,
         	a30tcourse.credit, 
         	a30tcourse.name
    	  FROM a32t_sel_score_summer,
         	a30tcourse
	  WHERE a32t_sel_score_summer.cour_cd = a30tcourse.cd
	  ORDER BY a32t_sel_score_summer.std_no ASC
  ";
  
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
