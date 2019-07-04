<?PHP
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_allcourse.php
  /////  ��s�ǥͩ�K���Z allcourse.txt
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
  echo("<CENTER><H1>��s���~�}�Ҹ����</H1><HR>");            
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
    echo("�s�ɥ���! �i��O�ɮ��v�����D\n");
  }else{
    echo("��s $filename		: $rowcount �����, �Ӯ� $time ��<P>\n");
    echo("���~�����<BR><A href=Update_allcourse02.cgi>��s��ƲĤG�B</A>");   
//    echo("��s����!<HR><P>\n");
  }
  
  Update_Log($filename, $rowcount, $time);
    
?>

