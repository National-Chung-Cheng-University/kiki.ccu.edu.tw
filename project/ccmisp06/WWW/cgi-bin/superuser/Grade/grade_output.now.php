<?php
	set_time_limit(600);
	include("sybase_connect.php");

	$outputfile="../../../../DATA/Grade/now.txt";
	$table="zv_student_at_ccu_grade_now";
	$query="select * from ".$table." order by std_no";
	$time_start=time();

	$result_id=sybase_query($query,$link);
	$rowcount=sybase_num_rows($result_id);
	$columncount=sybase_num_fields($result_id);
	echo "<HEAD><TITLE>�}�ƿ�Һ޲z�t�� -- ��s�ǥͦ��Z���</TITLE></HEAD>";
	echo "<BODY background=../../../Graph/bk.jpg>";
	echo "  <CENTER><H1>��s�ǥͦ��Z���</H1><HR>";
	echo "  ���b���� ".$rowcount." �����Z���......<br>";
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
