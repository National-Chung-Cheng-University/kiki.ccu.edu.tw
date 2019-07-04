<?PHP
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_allcourse.php
  /////  更新學生抵免成績 allcourse.txt
  /////  Updates: 
  /////    2006/11/16  Coder: Nidalap :D~
  /////    2012/10/30  改採 PDO 連資料庫 by Nidalap :D~
  ////////////////////////////////////////////////////////////////////////////
  
  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Database.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename   = "allcourse.txt";  
  $outputfile = $DATA_PATH . "Transfer/" . $filename;
  $time_start = time();

  echo $EXPIRE_META_TAG;
  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>更新歷年開課資料檔</H1><HR>");            
  $DBH = PDO_connect($DATABASE_NAME);

  $query_string = "
  SELECT distinct
         a.dept AS deptcd,
         a.cour_cd AS coursecd,
         a.class,
         a.grp,
         b.credit,
         a.classtime ,
         a.curcateg,
         a.cour_attr,
         a.attr,
         b.name,
         b.e_name
    FROM a31this_tcurriculum AS a,   
         a30tcourse b 
   WHERE (a.cour_cd = b.cd )  
       and (exists (select *
        from a31vmax_serialno where a.serialno = a31vmax_serialno.serialno))
  UNION
  SELECT distinct
         a.dept,
         a.cour_cd,
         a.class,
         a.grp,
         b.credit,
         a.classtime,
         a.curcateg,
         a.cour_attr,
         a.attr,
         b.name,
         b.e_name
    FROM a31tcurriculum  a,   
         a30tcourse b 
   WHERE (a.cour_cd = b.cd )  
   UNION
   SELECT distinct
         a.dept,
         a.cour_cd,
         a.class,
         a.grp,
         b.credit,
         a.classtime,
         a.curcateg,
         a.cour_attr,
         'N',
         b.name,
         b.e_name
    FROM a31tcurriculum_summer AS a,   
         a30tcourse b 
   WHERE (a.cour_cd = b.cd )
   ORDER BY deptcd, coursecd
  ";

    
  $STH = $DBH->prepare($query_string);
  $STH->execute();
  list($save_succeed, $rowcount) = Save_Update_File_PDO($outputfile);
  
  $time = time() - $time_start;
  if( $save_succeed == 0 ) {
    echo("存檔失敗! 可能是檔案權限問題\n");
	print_r($DBH->errorInfo());
  }else{
    echo("更新 $filename		: $rowcount 筆資料, 耗時 $time 秒<P>\n");
    echo("請繼續執行<BR><A href=Update_allcourse02.cgi>更新資料第二步</A>");   
//    echo("更新完畢!<HR><P>\n");
  }
  
  Update_Log($filename, $rowcount, $time);
    
?>

