<?php
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_student.php
  /////  ��s�ǥ;��y�����
  /////  Coder: Nidalap :D~
  /////  2006/09/22
  ////////////////////////////////////////////////////////////////////////////

  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename   = "student.txt";
  $outputfile = $DATA_PATH . "Reference/" . $filename;
//  $outputfile = "./ccc.txt";

  $time_start = time();

  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>��s���y�����</H1><HR>");  
  
  db_connect();
  
  $query_string	= 
    "SELECT now_dept,now_grade, now_class, enroll ,status, std_no,personid,sex_id, enrollnum, name 
     FROM a11tstd_rec  where (status = '0') ";
  if( $_GET["include_rest"] == 1) {			//  �p�G�]�t�w�p�_�ǥ�
    $query_string .=
      "OR 
        (status  = '5' and std_no in (select  std_no from a11trest_std_rec where 
        ryear = '" . $YEAR ."' and rterm = '" . $TERM . "' and (syear <> '" . $YEAR 
        . "' or sterm <> '". $TERM ."'))
        and std_no not in (select  std_no from a11trest_std_rec where 
        syear = '" . $YEAR ."' and sterm = '" . $TERM . "'))";
  }
  $query_string .= "order by 1 ,6";    

  echo("$query_string,$link<BR>"); 
  $result_id	= sybase_query($query_string,$link);
  $rowcount	= sybase_num_rows($result_id);

//  print("[outputfile, result_id, rowcount] = [$outputfile, $result_id, $rowcount]<BR>\n");
      
  $save_succeed = Save_Update_File($outputfile, $result_id, $rowcount);
  $fp = fopen($outputfile, "a");
  fputs($fp, "1104\t1\tA\tY\t0\t999999999\tQ120578558\tM\t2\t���ձb��\n");
  fclose($fp);
///  �������ǥ͸�Ƥ]�t�s�@���ɮ�  2012/10/22  Nidalap :D~
  $outputfile = $DATA_PATH . "Reference/student_rest.txt";
  $sql = "SELECT now_dept,now_grade, now_class, enroll ,status, std_no,personid,sex_id, enrollnum, name 
          FROM a11tstd_rec where (status = '5') order by 1";
  $result_id    = sybase_query($sql,$link);
  $rowcount     = sybase_num_rows($result_id);
    
  $save_succeed *= Save_Update_File($outputfile, $result_id, $rowcount);

  $time = time() - $time_start;
  if( $save_succeed == 0 ) {
    echo("�s�ɥ���! �i��O�ɮ��v�����D\n");
  }else{
    echo("��s $filename               : $rowcount �����, �Ӯ� $time ��<P>\n");
    echo("�t�P�B��s�F��ǥ͸����(�ثe�ȨѾǥͬd�ߦ��Z��)<P>\n");
    echo("���~�����<BR><A href=Update_student03.cgi>��s��ƲĤG�B</A>");
  }

  Update_Log($filename, $rowcount, $time);
 
?>
