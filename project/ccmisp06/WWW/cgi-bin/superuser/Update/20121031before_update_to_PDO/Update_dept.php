<?PHP
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_dept.php
  /////  ��s�t�ҥN�X�� Dept
  /////  Coder: Nidalap :D~
  /////  2009/06/01  ĵ�i�G������!!!
  ////////////////////////////////////////////////////////////////////////////
  
  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename   = "Dept";  
  $outputfile = $REFERENCE_PATH . $filename;
  $time_start = time();

  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>��s�t�ҥN�X��</H1><HR>");            
  db_connect();
//  $query_string = "";
  $query_string = "
select cd, name, abbrev, faculty_cd from h0rtunit_a_
where ( in_use = 'y' 
        or cd like '_016'
        or cd like '_014'
      ) 
      and
        ( cd not like '_000' )
      and
        ( cd not like '%8' )
order by cd
;
  ";
    
  $result_id	= sybase_query($query_string, $link);
  $rowcount	= sybase_num_rows($result_id);
  $columncount	= sybase_num_fields($result_id);

//  echo("query_string = $query_string<BR>\n");
  echo("result_id = $result_id<BR>\n");
//  echo("count = $columncount<BR>\n");  
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
