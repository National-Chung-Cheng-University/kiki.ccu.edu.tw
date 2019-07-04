<?PHP
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_allcourse.php
  /////  更新學生抵免成績 allcourse.txt
  /////  Coder: Nidalap :D~
  /////  2006/11/16
  ////////////////////////////////////////////////////////////////////////////
  
  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename   = "allcourse.txt";  
  $outputfile = $DATA_PATH . "Transfer/" . $filename;
  $time_start = time();

  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>更新歷年開課資料檔</H1><HR>");            
  db_connect();
//  $query_string = "";
  $query_string = "
  SELECT distinct
         a.dept     \"DEPTCD\",
         a.cour_cd  \"coursecd\",
         a.class    \"classcd\",
         a.grp      \"GROUP\",
         b.credit   \"CURPOINT\",
         a.classtime \"HOUR\" ,
         a.curcateg  \"CURCATEG\",
         a.cour_attr \"SUFFIX_CD\",
         b.name      \"CNAME\" ,
         b.e_name    \"ENAME\"
    FROM a31this_tcurriculum  a,   
         a30tcourse b 
   WHERE (a.cour_cd = b.cd )  
     and (exists (select *
        from a31vmax_serialno where a.serialno = a31vmax_serialno.serialno))
  union
  SELECT distinct
         a.dept     \"DEPTCD\",
         a.cour_cd  \"coursecd\",
         a.class    \"classcd\",
         a.grp      \"GROUP\",
         b.credit   \"CURPOINT\",
         a.classtime \"HOUR\" ,
         a.curcateg  \"CURCATEG\",
         a.cour_attr \"SUFFIX_CD\",
         b.name      \"CNAME\" ,
         b.e_name    \"ENAME\"
    FROM a31tcurriculum  a,   
         a30tcourse b 
   WHERE (a.cour_cd = b.cd )  
   union
   SELECT distinct
         a.dept     \"DEPTCD\",
         a.cour_cd  \"coursecd\",
         a.class    \"classcd\",
         a.grp      \"GROUP\",
         b.credit   \"CURPOINT\",
         a.classtime \"HOUR\" ,
         a.curcateg  \"CURCATEG\",
         a.cour_attr \"SUFFIX_CD\",
         b.name      \"CNAME\" ,
         b.e_name    \"ENAME\"
    FROM a31tcurriculum_summer  a,   
         a30tcourse b 
   WHERE (a.cour_cd = b.cd )
   ORDER BY coursecd
  ";
    
  $result_id	= sybase_query($query_string, $link);
  $rowcount	= sybase_num_rows($result_id);
//  $columncount	= sybase_num_fields($result_id);
//  echo("$query_string");
  
  $save_succeed = Save_Update_File($outputfile, $result_id, $rowcount);
  
  $time = time() - $time_start;
  if( $save_succeed == 0 ) {
    echo("存檔失敗! 可能是檔案權限問題\n");
  }else{
    echo("更新 $filename		: $rowcount 筆資料, 耗時 $time 秒<P>\n");
    echo("請繼續執行<BR><A href=Update_allcourse02.cgi>更新資料第二步</A>");   
//    echo("更新完畢!<HR><P>\n");
  }
  
  Update_Log($filename, $rowcount, $time);
    
?>

