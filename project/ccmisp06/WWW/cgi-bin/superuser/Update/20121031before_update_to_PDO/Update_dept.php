<?PHP
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_dept.php
  /////  更新系所代碼檔 Dept
  /////  Coder: Nidalap :D~
  /////  2009/06/01  警告：未完成!!!
  ////////////////////////////////////////////////////////////////////////////
  
  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename   = "Dept";  
  $outputfile = $REFERENCE_PATH . $filename;
  $time_start = time();

  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>更新系所代碼檔</H1><HR>");            
  db_connect();
//  $query_string = "";
  $query_string = "
select cd, name, abbrev, faculty_cd from h0rtunit_a_
where ( in_use = 'y' 
        or cd like '_016'
        or cd like '_014'
      ) 
      and
        ( cd not like '_000' )
      and
        ( cd not like '%8' )
order by cd
;
  ";
    
  $result_id	= sybase_query($query_string, $link);
  $rowcount	= sybase_num_rows($result_id);
  $columncount	= sybase_num_fields($result_id);

//  echo("query_string = $query_string<BR>\n");
  echo("result_id = $result_id<BR>\n");
//  echo("count = $columncount<BR>\n");  
  $save_succeed = Save_Update_File($outputfile, $result_id, $rowcount);
  
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
