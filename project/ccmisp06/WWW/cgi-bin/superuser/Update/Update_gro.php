<?PHP
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_gro.php
  /////  更新跨領域學程資料檔 gro_name.txt; gro_dept.txt, gro_cour.txt, gro_std.txt
  /////  Updates: 
  /////    2008/06/05 Coder: Nidalap :D~
  /////    2012/10/31 改採 PDO 連資料庫 by Nidalap :D~
  ////////////////////////////////////////////////////////////////////////////
  
  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Database.php";
  include $LIBRARY_PATH . "Error_Message.php";

//  $filename = "gro_name.txt";  
//  $outputfile = $REFERENCE_PATH . $filename;
  $time_start = time();

  print $EXPIRE_META_TAG;
  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>更新跨領域學程檔</H1><HR>");
  $DBH = PDO_connect($DATABASE_NAME);
  
/////  gro_name
  $filename = "gro_name.txt";
  $outputfile = $REFERENCE_PATH . $filename;  
  echo("正在更新 $filename...<BR>\n");
  $query_string = "
    SELECT gro_no, gro_name, gro_e_name
    FROM a13tgro_name";
    
  $STH = $DBH->prepare($query_string);
  $STH->execute();
  list($save_succeed1, $rowcount) = Save_Update_File_PDO($outputfile);

/////  gro_dept
  $filename = "gro_dept.txt";  
  $outputfile = $REFERENCE_PATH . $filename;    
  echo("正在更新 $filename...<BR>\n");                 
  $query_string = "
    SELECT gro_no, dept
    FROM a13tgro_dept";  
    
  $STH = $DBH->prepare($query_string);
  $STH->execute();
  list($save_succeed2, $rowcount) = Save_Update_File_PDO($outputfile);

/////  gro_cour
  $filename = "gro_cour.txt";
  $outputfile = $REFERENCE_PATH . $filename;
  echo("正在更新 $filename...<BR>\n");
  $query_string = "
    SELECT gro_no, cour_cd   
    FROM a13tgro_cour";

  $STH = $DBH->prepare($query_string);
  $STH->execute();
  list($save_succeed3, $rowcount) = Save_Update_File_PDO($outputfile);

/////  gro_std
  $filename = "gro_std.txt";
  $outputfile = $REFERENCE_PATH . $filename;
  echo("正在更新 $filename...<BR>\n");
  $query_string = "
    SELECT std_no, gro_no, schoolcd, groyear, gromonth, prn_date, prn_e_date
    FROM a13tgro_std";

  $STH = $DBH->prepare($query_string);
  $STH->execute();
  list($save_succeed4, $rowcount) = Save_Update_File_PDO($outputfile);
////////////////////////////////////////////
 
  $save_succeed = $save_succeed1 * $save_succeed2 * $save_succeed3 * $save_succeed4;
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
