<?
	$host="SYBCCU:4100";
	$user="ccureader";
	$password="!reader!ccu";

//	sybase_min_message_severity(1000);
//	echo "start connect<BR>";
	if ($link=sybase_pconnect($host,$user,$password))
	{
//		echo "succeed<BR>";
	}
	else { echo "內部錯誤: 無法連結資料庫. 請洽系統維護人員!<BR>";};

	$database="public_run";
	sybase_select_db($database);
?>
