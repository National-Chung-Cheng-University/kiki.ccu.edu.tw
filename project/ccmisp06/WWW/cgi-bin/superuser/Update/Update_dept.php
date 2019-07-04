<?PHP
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_dept.php
  /////  更新系所代碼檔 Dept
  /////  Updates: 
  /////    2006/06/01  警告：未完成!!!
  /////    2012/10/30  改採 PDO 連資料庫 by Nidalap :D~
  ////////////////////////////////////////////////////////////////////////////
  
  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Database.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename   = "Dept";  
  $outputfile = $REFERENCE_PATH . $filename;
  $time_start = time();

  echo $EXPIRE_META_TAG;
  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>更新系所代碼檔</H1><HR>");            
  $DBH = PDO_connect($DATABASE_NAME);
//  $query_string = "";
  $query_string = "
select cd, name, abbrev, faculty_cd, e_name from h0rtunit_a_
where ( in_use = 'y' 
        or cd like '_016'
        or cd like '_014'
      ) 
      and
        ( cd not like '_000' )
      and
        ( cd not like '%8' )
order by cd
  ";
    
  $STH = $DBH->prepare($query_string);
  $STH->execute();
  list($save_succeed, $rowcount) = Save_Update_File_PDO($outputfile);
  
  $time = time() - $time_start;
  if( $save_succeed == 0 ) {
    echo("存檔失敗! 可能是檔案權限問題<BR>\n");
	echo $query_string;
  }else{
    echo("更新 $filename		: $rowcount 筆資料, 耗時 $time 秒<P>\n");
    echo("更新完畢!<HR><P>\n");
  }
  
  Update_Log($filename, $rowcount, $time);
    
?>

<INPUT type=button value="關閉視窗" onClick="window.close()">
