<?PHP
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_early_warning_21_list.php
  /////  更新二一邊緣輔導學生名單 early_warning_21_list.txt
  /////  Updates: 
  /////    2011/06/10  Coder: Nidalap :D~
  /////    2012/10/30  改採 PDO 連資料庫 by Nidalap :D~
  ////////////////////////////////////////////////////////////////////////////
  
  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Database.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename = "Early_Warning_21_List.txt";
  $outputfile = $DATA_PATH . "Reference/" . $filename;
  $time_start = time();
  
  echo $EXPIRE_META_TAG;
  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>更新二一邊緣輔導學生名單</H1><HR>");            
  $DBH = PDO_connect();

  if( strlen($YEAR)==2 )  $YEAR = "0" . $YEAR;  ///  把兩碼學年度填為三碼
  $query_string = "SELECT year,term,id,status 
                     FROM early_warning_21_list
                    WHERE year='$YEAR' AND term='$TERM'";
  
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
