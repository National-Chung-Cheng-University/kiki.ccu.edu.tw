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
	echo "<HEAD><TITLE>開排選課管理系統 -- 更新學生成績資料</TITLE></HEAD>";
	echo "<BODY background=../../../Graph/bk.jpg>";
	echo "  <CENTER><H1>更新學生成績資料</H1><HR>";
	echo "  正在產生 ".$rowcount." 筆成績資料......<br>";
	$time_db=time();

	echo "抓取資料共花費 ",$time_db - $time_start ," 秒鐘<br>";

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
		echo "寫入資料共花費 ",$time_end - $time_db," 秒鐘<br>";
	}
	else { echo "內部錯誤: 無法寫入檔案 $outputfile, 請洽系統維護人員!<BR>";}
	sybase_close($link);
	echo "資料轉檔完成!<br>";
?>
