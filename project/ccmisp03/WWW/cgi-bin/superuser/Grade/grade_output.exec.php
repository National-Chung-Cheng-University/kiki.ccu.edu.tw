#!/usr/local/bin/php
<?
	# connect to database 
	include("sybase_connect.exec.php");

	$table="zv_student_at_ccu_grade_all";
	$query="
		select * 
		from zv_student_at_ccu_grade_now
		where std_no like \"588410%\"
	";

	$result_id=sybase_query($query,$link);
	$rowcount=sybase_num_rows($result_id);
	$columncount=sybase_num_fields($result_id);
	echo $result_id." ".$rowcount." ".$columncount;
	echo "<table width=900 border=0 cellspacing=3>";
	echo "<tr><td>";
	echo "<table width=800 border=1 cellspacing=3>";
	for ($i=0;$i<$rowcount;$i++)
	{
	$datarow=sybase_fetch_row($result_id);
	echo "<TR align=center>";
		for ($j=0;$j<$columncount;$j++)
			echo "<TD>".$datarow[$j]."</TD>";
	echo "</TR>\n";
	}
	echo "</table>";
	echo "</td><td valign=top align=left><pre>";
	$calendar=system("/bin/date");
	echo "</pre></td></tr></table>";
	sybase_close($link);
?>
