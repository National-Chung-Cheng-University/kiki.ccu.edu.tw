<?PHP
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_a14tapply_eng_class.php
  /////  更新應用英外語學程生名單.
  /////  Updates: 
  /////    2010/12/29  Coder: Nidalap :D~
  /////    2012/10/30  改採 PDO 連資料庫 by Nidalap :D~
  ////////////////////////////////////////////////////////////////////////////
  
  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Database.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename   = "a14tapply_eng_class.txt";  
  $outputfile = $REFERENCE_PATH . $filename;
  $time_start = time();

  echo $EXPIRE_META_TAG;
  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>更新開課代碼檔</H1><HR>");            
  
  $DBH = PDO_connect($DATABASE_NAME);

  $query_string = "
     SELECT a14tapply_eng_class.year,
            a14tapply_eng_class.term,
            a14tapply_eng_class.std_no,
            a14tapply_eng_class.type
       FROM a14tapply_eng_class 
  ";
    
  $STH = $DBH->prepare($query_string);
  $STH->execute();
  list($save_succeed, $rowcount) = Save_Update_File_PDO($outputfile);
  
  $time = time() - $time_start;
  if( $save_succeed == 0 ) {
    echo("存檔失敗! 可能是檔案權限問題\n");
    print_r($STH->errorInfo());
  }else{
    echo("更新 $filename		: $rowcount 筆資料, 耗時 $time 秒<P>\n");
    echo("更新完畢!<HR><P>\n");
  }
  
  Update_Log($filename, $rowcount, $time);
    
?>

<INPUT type=button value="關閉視窗" onClick="window.close()">
