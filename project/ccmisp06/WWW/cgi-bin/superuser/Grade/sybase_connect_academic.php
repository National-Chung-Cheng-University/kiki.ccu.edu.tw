<?PHP
	$host="SYBCCU:4100";
	$user="ccureader";
	$password="More?read!";

//	sybase_min_message_severity(1000);
//	echo "start connect<BR>";
	if ($link=sybase_pconnect($host,$user,$password))
	{
//		echo "succeed<BR>";
	}
	else { echo "�������~: �L�k�s����Ʈw. �Ь��t�κ��@�H��!<BR>";};

	$database="academic";
	sybase_select_db($database);
?>
