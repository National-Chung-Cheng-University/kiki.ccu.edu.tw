<?PHP
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_a30tcourse.php
  /////  ��s�}�ҥN�X�� a30tcourse
  /////  Coder: Nidalap :D~
  /////  2008/06/05
  ////////////////////////////////////////////////////////////////////////////
  
  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename   = "a30tcourse.txt";  
  $outputfile = $REFERENCE_PATH . $filename;
  $time_start = time();

  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>��s�}�ҥN�X��</H1><HR>");            
  db_connect();
//  $query_string = "";
  $query_string = "
  SELECT cd, cre_yt, name, e_name, credit
  FROM a30tcourse    
  ";
    
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

  if( !$IS_GRA ) {
    echo "
      <FORM action='Update_a30tcourse02.cgi'>
        <INPUT type=submit value='�~���sstep2/2'>
      </FORM>
    ";
  }

?>
