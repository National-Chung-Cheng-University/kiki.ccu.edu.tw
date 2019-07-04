<?PHP
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_teacher_edu.php
  /////  ��s�Ш|�ǵ{���W�� teacher_edu.txt
  /////  Coder: Nidalap :D~
  /////  2006/09/25
  ////////////////////////////////////////////////////////////////////////////
  
  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";
  
  $filename   = "teacher_edu.txt";
  $outputfile = $DATA_PATH . "Reference/" . $filename;
  $time_start = time();

  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>��s�ǵ{���W��</H1><HR>");            
  db_connect();

  $query_string = " SELECT a30tedu_proc.year,   
                           a30tedu_proc.term,   
                           a30tedu_proc.std_no,   
                           a30tedu_proc.dept,   
                           a30tedu_proc.applydate,   
                           a30tedu_proc.waivedate,   
                           a30tedu_proc.sfx,   
                           a30tedu_proc.edu_type  
                    FROM a30tedu_proc  
                    WHERE a30tedu_proc.std_no in (  SELECT a11tstd_rec.std_no  
                    FROM a11tstd_rec )";
    
  $result_id	= sybase_query($query_string, $link);
  $rowcount	= sybase_num_rows($result_id);
//  $columncount	= sybase_num_fields($result_id);
  
  $save_succeed = Save_Update_File($outputfile, $result_id, $rowcount);
  
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
