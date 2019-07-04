<?php
/*********************************************************************
	getssoCcuRight.php
	子系統端導入SSO接收資訊
	Last update : 2012/11/23
	系統需求：php4.0/5.0 + DOM
	常數與變數說明請見getssoCcuRight_config.php
**********************************************************************/
include_once('getssoCcuRight_config.php');

$miXd  = (isset($_GET['miXd'])) ? trim($_GET['miXd']) : '';
$ticket = (isset($_GET['ticket'])) ? trim($_GET['ticket']) : '';

if($miXd != '' && $ticket != '') {
	//接收SSO資料
	list($status, $enter_ip, $user_id, $person_id) = chk_ssoRight($miXd, $ticket);
	if($status == 1) {//sso端登入成功的動作
		//將資訊丟給子系統端的session去操作
		$_SESSION['sso_enterip']	= $enter_ip;	//使用者端登入IP
		$_SESSION['sso_personid']	= $person_id;	//學號或身份證字號(教職員工)
		$_SESSION['tokenSso']		= $miXd;		//sso token
		$_SESSION['verifySso']		= 'Y';			//sso登入識別

		//換頁至子系統端登入確認的程式處理各子系統端所需要的額外資訊
		header('Location: '.SYS_LOGIN_URL);
	} else {
		sso_err_msgAlert($enter_ip, SYS_DOOR_URL);//失敗時enter_ip會是錯誤訊息
	}
} else {
	sso_err_msgAlert('錯誤代碼：ENTER_SYS_001\n登入資訊錯誤！\n~請重新登入~', SYS_DOOR_URL);
}

?>