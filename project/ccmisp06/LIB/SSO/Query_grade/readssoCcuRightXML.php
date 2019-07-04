<?php
/*********************************************************************
	readssoCcuRightXML.php
	子系統端導入SSO接收資訊
	Last update : 2011/09/20
	系統需求：php4.0/5.0 + DOM
	常數與變數說明請見refreshSso.php
**********************************************************************/
include_once('refreshSso.php');

//登入
if(isset($_GET['cid']) and (trim($_GET['cid']) != '') and isset($_GET['miXd']) and (trim($_GET['miXd']) != '')) {
	if((md5(sso_getIP().substr($_GET['miXd'],-10)).substr($_GET['miXd'], 10, 6) == $_GET['cid'])) {//驗證IP是否為同一個IP
		list($status, $enter_ip, $user_id, $person_id) = chk_ssoRight($_GET['miXd']);
		//接收SSO資料

		if($status == 1) {//sso端登入成功的動作
			//將資訊丟給子系統端的session去操作
			$_SESSION['sso_enterip']	= $enter_ip;	//使用者端登入IP
			$_SESSION['sso_personid']	= $person_id;	//學號或身份證字號(教職員工)
			$_SESSION['tokenSso']		= $_GET['miXd'];//sso token
			$_SESSION['verifySso']		= 'Y';			//sso登入識別

			//換頁至子系統端登入確認的程式處理各子系統端所需要的額外資訊
			header('Location: '.SYS_LOGIN_URL);
		} else {
			//err_msgAlert($enter_info,SSO_DOOR_URL);
			err_msgAlert($enter_ip, SSO_DOOR_URL);//失敗時enter_ip會是錯誤訊息
		}
	} else {
		err_msgAlert('錯誤代碼：ENTER_SYS_002\n登入資訊錯誤！\n~請重新登入~', SSO_DOOR_URL);
	}
} else {
	err_msgAlert('錯誤代碼：ENTER_SYS_001\n登入資訊錯誤！\n~請重新登入~', SSO_DOOR_URL);
}

?>