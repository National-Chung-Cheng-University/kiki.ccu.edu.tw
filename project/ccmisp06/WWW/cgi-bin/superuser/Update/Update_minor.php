<?PHP
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_minor.php
  /////  更新輔系名單 minor.txt
  /////  Updates: 
  /////    2006/09/25  Coder: Nidalap :D~
  /////    2012/10/30  改採 PDO 連資料庫 by Nidalap :D~
  /////	   2013/01/09  取消原本 status='0' 的限制  by Nidalap :D~
  /////    2013/06/11  因應 PostgreSQL 更改 query string by Nidalap :D~
  /////    2016/06/15  修正 sql 語法加入 trim() 以避開嘉耀程式 BUG  by Nidalap :D~
  ////////////////////////////////////////////////////////////////////////////
  
  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Database.php";
  include $LIBRARY_PATH . "Error_Message.php";
  
  $filename   = "fu.txt";
  $outputfile = $REFERENCE_PATH . $filename;
  $time_start = time();

  echo $EXPIRE_META_TAG;
  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>更新輔系名單</H1><HR>");
  $DBH = PDO_connect($DATABASE_NAME);

  $query_string = "SELECT dept, std_no FROM a30tminor WHERE isnull(waivedate,'') = ''";
  $query_string = "SELECT dept, std_no FROM a30tminor WHERE trim(waivedate) = '' OR waivedate IS NULL";
//      AND std_no  in (         
//        SELECT std_no              
//        FROM a11tstd_rec  
//        WHERE status = '0' )";
    
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
