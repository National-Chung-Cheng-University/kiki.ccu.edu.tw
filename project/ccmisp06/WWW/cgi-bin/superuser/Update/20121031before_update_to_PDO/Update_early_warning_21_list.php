<?PHP
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_early_warning_21_list.php
  /////  ��s�G�@��t���ɾǥͦW�� early_warning_21_list.txt
  /////  Coder: Nidalap :D~
  /////  2011/02/06
  ////////////////////////////////////////////////////////////////////////////
  
  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename = "Early_Warning_21_List.txt";
  $outputfile = $DATA_PATH . "Reference/" . $filename;
  $time_start = time();

  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>��s�G�@��t���ɾǥͦW��</H1><HR>");            
  db_connect("", 1);

  if( strlen($YEAR)==2 )  $YEAR = "0" . $YEAR;  ///  ���X�Ǧ~�׶񬰤T�X
  $query_string = "SELECT year,term,id,status 
                     FROM early_warning_21_list
                    WHERE year='$YEAR' AND term='$TERM'";
  
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
