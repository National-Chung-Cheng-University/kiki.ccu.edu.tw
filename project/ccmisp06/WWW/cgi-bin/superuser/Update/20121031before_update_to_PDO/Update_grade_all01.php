<?php
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_grade_all.php
  /////  ��s�ǥͩҦ��Ǵ����Z���
  /////  Coder: Nidalap :D~
  /////  Updates:
  /////    2009/12/18  Created by Nidalap :D~
  /////    2010/06/24  �Ǧ~�קאּ�Ѥj�ܤp�Ƨ� Nidalap :D~
  ////////////////////////////////////////////////////////////////////////////

  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $year_from = 78;						///  �}�l�����Z���~��
  
  $filename   = "now.txt";
  $outputfile = $DATA_PATH . "Grade/" . $filename;
//  $outputfile = "./ccc.txt";

  $time_start = time();
  
  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>��s���~���Z�� - 1/2</H1><HR>");
  echo("<FORM action=Update_grade_all02.php method=POST>");
  echo("�Ǧ~��: <SELECT name=year>");
  for( $year=$YEAR; $year>=$year_from; $year-- ) {
    if( strlen($year) == 2 ) {
      $year_ = "0" . $year;
    }else{
      $year_ = $year;
    }
    echo("<OPTION>$year_</OPTION>");
  }
  echo("</SELECT><BR>");
  echo("�Ǵ�: <SELECT name=term><OPTION>1</OPTION><OPTION>2</OPTION></SELECT><P>");
  echo("<INPUT type=SUBMIT value='�U�@�B'></FORM>");

/*  db_connect_public();
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
*/ 
?>

<INPUT type=button value="��������" onClick="window.close()">
