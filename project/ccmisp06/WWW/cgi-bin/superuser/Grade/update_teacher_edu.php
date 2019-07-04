<?php
	set_time_limit(600);
	include("sybase_connect_academic.php");

	//$outputfile="../../../../DATA/Reference/teacher_edu.txt";
	//$outputfile="teacher_edu.txt";
	$outputfile = "/ultra2/project/ccmisp06/DATA/Reference/teacher_edu.txt";

        $query = "  SELECT a30tedu_proc.year,   
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
	$time_start=time();
	$result_id=sybase_query($query,$link);
	$rowcount=sybase_num_rows($result_id);
	$columncount=sybase_num_fields($result_id);
	echo "<HEAD><TITLE>�}�ƿ�Һ޲z�t�� -- ��steacher_edu���</TITLE></HEAD>";
	echo "<BODY background=../../../Graph/bk.jpg>";
	echo "  <CENTER><H1>��steacher_edu���</H1><HR>";
	echo "  ���b���� ".$rowcount." �����......<br>";
	$time_db=time();

	echo "�����Ʀ@��O ",$time_db - $time_start ," ����<br>";

	$fp = fopen ($outputfile,"w+");
	if ($fp)
	{
//		echo "open $outputfile<br>";
  		set_file_buffer($fp, 65536);
		for ($i=0;$i<$rowcount;$i++)
		{
			$output="";
			$datarow=sybase_fetch_row($result_id);
			for ($j=0;$j<$columncount;$j++)
			{
				$output=$output.$datarow[$j]."\t";
			}
			$output=$output."\n";
  			fputs($fp, $output);
		}
//		echo "closing $outputfile<br>";
  		fclose($fp);
		$time_end=time();
		echo "�g�J��Ʀ@��O ",$time_end - $time_db," ����<br>";
	}
	else { echo "�������~: �L�k�g�J�ɮ� $outputfile, �Ь��t�κ��@�H��!<BR>";}
	sybase_close($link);
	echo "������ɧ���!<br>";
?>
