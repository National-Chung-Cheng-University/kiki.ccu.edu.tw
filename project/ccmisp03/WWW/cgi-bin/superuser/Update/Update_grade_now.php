<?php
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_grade_now.php
  /////  ��s�ǥͷ��Ǵ����Z��� now.txt
  /////  Coder: Nidalap :D~
  /////  2006/09/21
  ////////////////////////////////////////////////////////////////////////////

  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename   = "now.txt";
  $outputfile = $DATA_PATH . "Grade/" . $filename;
//  $outputfile = "./ccc.txt";

  $time_start = time();
  
  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>��s���Ǵ����Z��</H1><HR>");          

  db_connect_public();
  if ( $IS_GRA == 1 ) {					///  �̥���/�M�Z, ��ܤ��P�� view
    $table	= "zv_student_at_ccu_grade_nowpay";
  }else{
    $table	= "zv_student_at_ccu_grade_now";
  }
  $query_string	= "select * from " . $table . " order by std_no";
  
  echo("$query_string,$link<BR>"); 
  $result_id	= sybase_query($query_string,$link);
  $rowcount	= sybase_num_rows($result_id);

  print("[outputfile, result_id, rowcount] = [$outputfile, $result_id, $rowcount]<BR>\n");
      
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