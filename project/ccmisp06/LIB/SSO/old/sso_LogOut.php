<?php

	//sso登出頁
	include 'readssoCcuRightXML.php';
	if(isset($_SESSION['verifySso']) and $_SESSION['verifySso']=="Y"){
		ssoLogOut();
	}

?>