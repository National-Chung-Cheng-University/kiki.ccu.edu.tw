<?PHP
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_a30tcourse.php
  /////  更新開課代碼檔 a30tcourse
  /////  Coder: Nidalap :D~
  /////  2008/06/05
  ////////////////////////////////////////////////////////////////////////////
  
  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename   = "a30tcourse.txt";  
  $outputfile = $REFERENCE_PATH . $filename;
  $time_start = time();

  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>更新開課代碼檔</H1><HR>");            
  db_connect();
//  $query_string = "";
  $query_string = "
  SELECT cd, cre_yt, name, e_name, credit
  FROM a30tcourse    
  ";
    
  $result_id	= sybase_query($query_string, $link);
  $rowcount	= sybase_num_rows($result_id);
//  $columncount	= sybase_num_fields($result_id);
  
  $save_succeed = Save_Update_File($outputfile, $result_id, $rowcount);
  
  $time = time() - $time_start;
  if( $save_succeed == 0 ) {
    echo("存檔失敗! 可能是檔案權限問題\n");
  }else{
    echo("更新 $filename		: $rowcount 筆資料, 耗時 $time 秒<P>\n");
    echo("更新完畢!<HR><P>\n");
  }
  
  Update_Log($filename, $rowcount, $time);

  if( !$IS_GRA ) {
    echo "
      <FORM action='Update_a30tcourse02.cgi'>
        <INPUT type=submit value='繼續更新step2/2'>
      </FORM>
    ";
  }

?>
