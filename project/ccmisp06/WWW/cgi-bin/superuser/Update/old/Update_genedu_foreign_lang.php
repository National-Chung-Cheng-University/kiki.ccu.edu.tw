<?php
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_genedu_foreign_lang.php
  /////  新生英檢成績檔, 用於判別學生修習通識外語課程依據.
  /////  Coder: Nidalap :D~
  /////  Updates:
  /////    2010/09/02  Created by Nidalap :D~
  /////    2011/09/20  由原先從 email 得到的名單，改為從資料庫抓  Nidalap :D~ 
  /////    2011/09/21  與語言中心恬恬討論後，得知不需此名單！從此廢除！ Nidalap :D~
  ////////////////////////////////////////////////////////////////////////////

  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename	= "genedu_foreign_lang.txt";
  $infile	= $DATA_PATH . "Grade/" . $filename;
  $outpath	= $DATA_PATH . "Grade/genedu_foreign_lang/";
  
  $outputfile = $DATA_PATH . "Grade/genedu_foreign_lang.txt";

  $time_start = time();

  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>更新新生英檢成績檔</H1><HR>");  
  

  db_connect();  
  $query_string	= "SELECT std_no, eng_score FROM a11tnewstd_engchi_score";

//  echo("$query_string,$link<BR>"); 
  $result_id	= sybase_query($query_string,$link);
  $rowcount	= sybase_num_rows($result_id);

//  print("[outputfile, result_id, rowcount] = [$outputfile, $result_id, $rowcount]<BR>\n");
      
  $save_succeed = Save_Update_File($outputfile, $result_id, $rowcount);
  $fp = fopen($outputfile, "a");
  fclose($fp);

  $save_succeed = 0;
  if( ($fp = fopen($infile, "r")) == 0 ) {				///  開啟語言中心傳來的新生英檢成績檔
    $save_succeed = 0;
  }else{
    if( $dir = opendir($outpath) ) {					///  開啟目錄準備清空
      echo("正在清除舊有的新生英檢個人成績資料...<BR>\n");
      while( false !== ($old_file = readdir($dir)) ) {
        if ($old_file != "." && $old_file != "..") {
          $temp_file = $outpath . $old_file;
//          echo("deleting $temp_file...<BR>\n");     
          if( !unlink($temp_file) ) {
            echo "Failed to unlink file $temp_file!";
          } 
        }
      }
      closedir($outpath);
      while( $line = fgets($fp) ) {					/// 將檔案細分為多個小檔案
        $rowcount++;
        $temp = preg_split("/\t/", $line);
        $outfile = $outpath . $temp[0];
        $fp2 = fopen($outfile, "w");
//        echo("writing data into $outfile: $line<BR>\n");
        if( fwrite($fp2, $line) )  $save_succeed++;
        fclose($fp2);
        
      }
    }else{
      $save_flag = 0;
    }
  }

  $time = time() - $time_start;
  if( $save_succeed == 0 ) {
    echo("讀檔失敗! 可能是檔案根本不存在\n");
  }else{
    echo("更新 $filename               : $rowcount 筆資料, 耗時 $time 秒<P>\n");
    Update_Log($filename, $rowcount, $time);
  }
?>
