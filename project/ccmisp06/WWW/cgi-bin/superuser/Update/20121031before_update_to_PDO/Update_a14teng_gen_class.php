<?php
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_a14teng_gen_class.php
  /////  更新學生通識英文成績資料  a14teng_gen_class.txt
  /////  Coder: Nidalap :D~
  /////  2011/08/30
  ////////////////////////////////////////////////////////////////////////////

  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename   = "a14teng_gen_class.txt";
  $outputfile = $DATA_PATH . "Grade/" . $filename;

  $time_start = time();
  
  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>更新學生通識英文成績檔</H1><HR>");

  db_connect();
  $query_string = "
        SELECT std_no, type FROM a14teng_gen_class
  ";
  
#  echo("$query_string,$link<BR>"); 
  $result_id	= sybase_query($query_string,$link);
  $rowcount	= sybase_num_rows($result_id);

#  print("[outputfile, result_id, rowcount] = [$outputfile, $result_id, $rowcount]<BR>\n");
      
  $save_succeed = Save_Update_File($outputfile, $result_id, $rowcount);

  if( !Split_Little_Files() )  $save_succeed = 0;

  $time = time() - $time_start;
  if( $save_succeed == 0 ) {
    echo("存檔失敗! 可能是檔案權限問題 $outputfile \n");
  }else{
    echo("更新 $filename               : $rowcount 筆資料, 耗時 $time 秒<P>\n");
    echo("更新完畢!<HR><P>\n");    
  }

  Update_Log($filename, $rowcount, $time);
  ////////////////////////////////////////////////////////////////////////////////////
  /////  將大名單以學號分割為多個小檔案，用於選課時即時判斷
  function Split_Little_Files()
  {
    global $DATA_PATH, $outputfile;
    $outpath  = $DATA_PATH . "Grade/genedu_foreign_lang/";
    
    if( ($fp = fopen($outputfile, "r")) == 0 ) {                          ///  開啟剛傳上來熱騰騰的檔案
      $save_succeed = 0;
    }else{
      if( $dir = opendir($outpath) ) {                                    ///  開啟目錄準備清空
        echo("正在清除舊有的新生英檢個人成績資料...<BR>\n");
        while( false !== ($old_file = readdir($dir)) ) {
          if ($old_file != "." && $old_file != "..") {
            $temp_file = $outpath . $old_file;
//            echo("deleting $temp_file...<BR>\n");     
            if( !unlink($temp_file) ) {
              echo "Failed to unlink file $temp_file!";
            }
          }
        }
        closedir($outpath);
        while( $line = fgets($fp) ) {                                     /// 將檔案細分為多個小檔案
          $rowcount++;
          $temp = preg_split("/\t/", $line);
          $outfile = $outpath . $temp[0];
          $fp2 = fopen($outfile, "w");
//          echo("writing data into $outfile: $line<BR>\n");
          if( fwrite($fp2, $line) )  $save_succeed++;
          fclose($fp2);
        }
      }else{
        $save_succeed = 0;
      }
    }
    return $save_succeed;
  }
 
?>

<INPUT type=button value="關閉視窗" onClick="window.close()">
