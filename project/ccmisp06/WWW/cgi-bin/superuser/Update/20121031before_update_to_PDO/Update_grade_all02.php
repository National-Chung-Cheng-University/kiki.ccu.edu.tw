<?php
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_grade_all02.php
  /////  ��s�ǥ;��~���Z���
  /////  Coder: Nidalap :D~
  /////  Updates:
  /////    2009/12/18 Created by Nidalap :D~
  /////    2010/06/24 �s���ɦW�N�Ǧ~�Ǵ��j�}�A�H�קK����ʦ~ bug Nidalap :D~
  ////////////////////////////////////////////////////////////////////////////

  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $year = $_POST["year"];
  $term = $_POST["term"];
  
  $filename   = $year . "_" . $term . ".txt";
  $outputfile = $DATA_PATH . "Grade/score/" . $filename;
//  $outputfile = "./ccc.txt";

  $time_start = time();
  
  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>��s���~���Z��</H1><HR>");

  db_connect_public();
  if ( $IS_GRA == 1 ) {					///  �̥���/�M�Z, ��ܤ��P�� view
    $table	= "zv_student_at_ccu_grade_allpay";
  }else{
    $table	= "zv_student_at_ccu_grade_all";
  }
  if( substr($year,0,1) == 0 )  $year = substr($year,1,2);   /// ��Ʈw�� year �O 98 �ӫD 098
  $query_string	= "select * from " . $table . " WHERE year='" . $year . "' and term='" . $term . "' order by std_no";
  
//  echo("$query_string,$link<BR>"); 

  $result_id	= sybase_query($query_string,$link);
  $rowcount	= sybase_num_rows($result_id);

//  print("[outputfile, result_id, rowcount] = [$outputfile, $result_id, $rowcount]<BR>\n");
      
  $save_succeed = Save_Update_File($outputfile, $result_id, $rowcount);

  $time = time() - $time_start;
  if( $save_succeed == 0 ) {
    echo("�s�ɥ���! �i��O�ɮ��v�����D\n");
  }else{
    echo("��s $filename               : $rowcount �����, �Ӯ� $time ��<P>\n");
    echo("��s����!<HR><P>\n");    
  }

  Update_Log($filename, $rowcount, $time);
 
?>

<INPUT type=button value="��������" onClick="window.close()">
