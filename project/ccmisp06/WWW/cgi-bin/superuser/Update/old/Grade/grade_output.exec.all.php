#!/usr/local/bin/php
<?php
	set_time_limit(3600);
	echo "connecting database<br>";
	include("sybase_connect.exec.php");

	$outputfile="grade_all.txt";
	$table="zv_student_at_ccu_grade_all";
	$query="select * from ".$table." order by std_no";
	$time_start=time();

	echo "this will take longer time .....<br>";
	flush();

	$result_id=sybase_query($query,$link);
	$rowcount=sybase_num_rows($result_id);
	$columncount=sybase_num_fields($result_id);
	echo "going to output ".$rowcount." records<br>";
	$time_db=time();

	echo "time in db select : ",$time_db - $time_start ,"<br>";

	$fp = fopen ($outputfile,"w+");
	if ($fp)
	{
		echo "open $outputfile<br>";
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
		echo "closing $outputfile<br>";
  		fclose($fp);
		$time_end=time();
		echo "file write time : ",$time_end - $time_db,"<br>";
	}
	else { echo "failed to open $outputfile";}
	sybase_close($link);
	echo "done<br>";
?>
