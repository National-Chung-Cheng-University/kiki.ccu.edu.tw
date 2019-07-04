<?php
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_std_orders.php
  /////  ��s�ǥ;��~�ƦW��� std_orders.txt
  /////  Coder: Nidalap :D~
  /////  2006/09/26
  ////////////////////////////////////////////////////////////////////////////

  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename   = "std_orders.txt";
  $outputfile = $DATA_PATH . "Grade/" . $filename;

  $time_start = time();
  
  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>��s�ǥ;��~�ƦW��</H1><HR>");

  db_connect();
  $query_string = "
  	SELECT a12this_tot_avg.year,   
         	a12this_tot_avg.term,   
         	a12this_tot_avg.std_no,   
         	a12this_tot_avg.order_s  
    	FROM a12this_tot_avg  
   	WHERE 
       		a12this_tot_avg.std_no in (  SELECT a11tstd_rec.std_no  
                                        FROM a11tstd_rec )  
	ORDER BY a12this_tot_avg.std_no ASC,   
         	a12this_tot_avg.year ASC,   
         	a12this_tot_avg.term ASC
  ";
  
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
