<?PHP
	$host="SYBCCU";
	$user="ccuwriter";
	$password="!writer!ccu";

//	sybase_min_message_severity(1000);
	echo "start connect<BR>";
	if ($link=sybase_pconnect($host,$user,$password))
	{
		echo "succeed<BR>";
	}
	else { echo "failed<BR>";};

	$database="academic";
	sybase_select_db($database);
?>
