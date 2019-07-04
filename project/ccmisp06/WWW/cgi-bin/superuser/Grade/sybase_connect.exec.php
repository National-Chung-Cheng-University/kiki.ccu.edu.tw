<?PHP
	$host="140.123.30.7";
	$user="ccureader";
	$password="xzsbcs2!";

	echo "start connect<BR>";
	if ($link=sybase_pconnect($host,$user,$password))
	{
		echo "succeed<BR>";
	}
	else { echo "failed<BR>";};

	$database="public_run";
	sybase_select_db($database);
?>
