<?PHP
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_gro.php
  /////  ��s����ǵ{����� gro_name.txt; gro_dept.txt, gro_cour.txt, gro_std.txt
  /////  Coder: Nidalap :D~
  /////  2008/06/05
  ////////////////////////////////////////////////////////////////////////////
  
  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";

//  $filename = "gro_name.txt";  
//  $outputfile = $REFERENCE_PATH . $filename;
  $time_start = time();

  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>��s����ǵ{��</H1><HR>");
  db_connect();

/////  gro_name
  $filename = "gro_name.txt";
  $outputfile = $REFERENCE_PATH . $filename;  
  echo("���b��s $filename...<BR>\n");
  $query_string = "
    SELECT gro_no, gro_name, gro_e_name
    FROM a13tgro_name";
    
  $result_id	= sybase_query($query_string, $link);
  $rowcount	= sybase_num_rows($result_id);
  $save_succeed = Save_Update_File($outputfile, $result_id, $rowcount);


/////  gro_dept
  $filename = "gro_dept.txt";  
  $outputfile = $REFERENCE_PATH . $filename;    
  echo("���b��s $filename...<BR>\n");                 
  $query_string = "
    SELECT gro_no, dept
    FROM a13tgro_dept";  
    
  $result_id    = sybase_query($query_string, $link);
  $rowcount     = sybase_num_rows($result_id);
  $save_succeed = Save_Update_File($outputfile, $result_id, $rowcount);  

/////  gro_cour
  $filename = "gro_cour.txt";
  $outputfile = $REFERENCE_PATH . $filename;
  echo("���b��s $filename...<BR>\n");
  $query_string = "
    SELECT gro_no, cour_cd   
    FROM a13tgro_cour";

  $result_id    = sybase_query($query_string, $link);
  $rowcount     = sybase_num_rows($result_id);
  $save_succeed = Save_Update_File($outputfile, $result_id, $rowcount);

/////  gro_std
  $filename = "gro_std.txt";
  $outputfile = $REFERENCE_PATH . $filename;
  echo("���b��s $filename...<BR>\n");
  $query_string = "
    SELECT std_no, gro_no, schoolcd, groyear, gromonth, prn_date, prn_e_date
    FROM a13tgro_std";

  $result_id    = sybase_query($query_string, $link);
  $rowcount     = sybase_num_rows($result_id);
  $save_succeed = Save_Update_File($outputfile, $result_id, $rowcount);
////////////////////////////////////////////
 
  $time = time() - $time_start;
  if( $save_succeed == 0 ) {
    echo("�s�ɥ���! �i��O�ɮ��v�����D\n");
  }else{
    echo("��s $filename		: $rowcount �����, �Ӯ� $time ��<P>\n");
    echo("��s����!<HR><P>\n");
  }


  
  Update_Log($filename, $rowcount, $time);
    
?>

<INPUT type=button value="��������" onClick="window.close()">
