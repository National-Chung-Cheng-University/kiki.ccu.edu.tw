<?PHP
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_teacher_edu.php
  /////  更新教育學程資格名單 teacher_edu.txt
  /////  Updates: 
  /////    2006/09/25  Coder: Nidalap :D~
  /////    2012/10/30  改採 PDO 連資料庫 by Nidalap :D~
  ////////////////////////////////////////////////////////////////////////////
  
  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Database.php";
  include $LIBRARY_PATH . "Error_Message.php";
  
  $filename   = "teacher_edu.txt";
  $outputfile = $DATA_PATH . "Reference/" . $filename;
  $time_start = time();

  echo $EXPIRE_META_TAG;
  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>更新學程資格名單</H1><HR>");            
  $DBH = PDO_connect($DATABASE_NAME);

  $query_string = " SELECT a30tedu_proc.year,   
                           a30tedu_proc.term,   
                           a30tedu_proc.std_no,   
                           a30tedu_proc.dept,   
                           a30tedu_proc.applydate,   
                           a30tedu_proc.waivedate,   
                           a30tedu_proc.sfx,   
                           a30tedu_proc.edu_type  
                    FROM a30tedu_proc  
                    WHERE a30tedu_proc.std_no in (  SELECT a11tstd_rec.std_no  
                    FROM a11tstd_rec )";
    
  $STH = $DBH->prepare($query_string);
  $STH->execute();
  list($save_succeed, $rowcount) = Save_Update_File_PDO($outputfile);
  
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
