<?PHP
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_a14tapply_eng_deduct_c.php
  /////  ��s���έ^�~�y�i�׽ҩ貦�~���e�ǥͦW��
  /////  Coder: Nidalap :D~
  /////  2010/12/29
  ////////////////////////////////////////////////////////////////////////////
  
  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename   = "a14tapply_eng_deduct_c.txt";  
  $outputfile = $REFERENCE_PATH . $filename;
  $time_start = time();

  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>��s�}�ҥN�X��</H1><HR>");            
  db_connect();
//  $query_string = "";
  $query_string = "
    SELECT a14tapply_eng_deduct_c.year,
           a14tapply_eng_deduct_c.term,
           a14tapply_eng_deduct_c.std_no,
           a14tapply_eng_deduct_c.type
      FROM a14tapply_eng_deduct_c
  ";
    
  $result_id	= sybase_query($query_string, $link);
  $rowcount	= sybase_num_rows($result_id);
//  $columncount	= sybase_num_fields($result_id);
  
  $save_succeed = Save_Update_File($outputfile, $result_id, $rowcount);
  
  $time = time() - $time_start;
  if( $save_succeed == 0 ) {
    echo("�s�ɥ���! �i��O�ɮ��v�����D\n");
    echo sybase_get_last_message();
  }else{
    echo("��s $filename		: $rowcount �����, �Ӯ� $time ��<P>\n");
    echo("��s����!<HR><P>\n");
  }
  
  Update_Log($filename, $rowcount, $time);
    
?>

<INPUT type=button value="��������" onClick="window.close()">
