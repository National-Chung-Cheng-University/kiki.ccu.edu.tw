<?php
/*********************************************************************
	refreshSso.php
	子系統端延長SSO端的session存活時間
	(子系統的每個page都include此php檔, 每次更新頁面就會自動延長sso存活時間了)
	Last update : 2012/07/19
	系統需求：php5.0 + DOM

	常數：
		SYS_DOOR_URL	子系統端登入頁
		SYS_LOGIN_URL	子系統端登入確認程式
		SSO_DOOR_URL	SSO端首頁
	重要SESSION變數：
		$_SESSION['verifySso']		SSO登入方式辨識訊號
		$_SESSION['tokenSso']		SSO登入token資訊
		$_SESSION['sso_enterip']	使用者端登入IP
		$_SESSION['sso_personid']	學號或身份證字號(教職員工)
	函式：
		sso_getIP()					取得使用者IP
		chk_ssoRight($mix_info)		取得sso權限資訊
		chk_ssoRefresh($mix_info)	延長sso的session存活時間
		err_msgAlert($msg,$url)		錯誤訊息及導向頁面
		ssoLogOut()					SSO的登出導向
		
	註1：使用if(isset($_SESSION['verifySso']) and trim($_SESSION['verifySso'])=="Y")判斷是否從sso端登入
	     若是改在正式平台，請註解掉define('_TEST_PLATFORM',true);這一行
	註2：若是非UTF-8的子系統請註解掉header('Content-type: text/html; charset=UTF-8')
**********************************************************************/
//header('Content-type: text/html; charset=UTF-8'); //代簽入非UTF-8的子系統時不需要這行, 檔案格式也需要存成ansi

//require "../main.php";

//session不存在時，啟用session
if(!isset($_SESSION)) session_start();

//正式平台請註解掉這一行
define('_TEST_PLATFORM', true);

if(defined('_TEST_PLATFORM')) { //測試平台
	//常數定義
        define('SYS_DOOR_URL', 'http://140.123.30.101/~ccmisp08/cgi-bin/Query/'); //子系統端登入頁
        define('SYS_LOGIN_URL', 'http://140.123.30.101/~ccmisp08/cgi-bin/Query/Query_grade.php'); //子系統端登入確認程式
        define('SSO_DOOR_URL', 'http://140.123.4.217/'); //sso端首頁
} else { //正式平台
        define('SYS_DOOR_URL', 'http://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/Query/'); //子系統端登入頁
        define('SYS_LOGIN_URL', 'http://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/Query/Query_grade.php'); //子系統端登入確認程式
        define('SSO_DOOR_URL', 'http://portal.ccu.edu.tw/');
}

//取得使用者IP
function sso_getIP() {
	if(!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
		$route = $_SERVER['HTTP_X_FORWARDED_FOR'];
		$ip = split(',', $route);
	} else {
		$route = '';
	}
	$ip = (empty($route)) ? $_SERVER['REMOTE_ADDR'] : $ip[0];
	return $ip;
}

//取得sso權限資訊
//接受1個變數(token資訊)，回傳5個變數
function chk_ssoRight($mix_info) {
	$xml_txt = file_get_contents(SSO_DOOR_URL.'ssoCcuRightXML.php?cid='.$mix_info);
	$order   = array('\r\n', '\n', '\r');
	$replace = '';
	$err_msg = '';
	$newstr = str_replace($order, $replace, $xml_txt);
	$dom = new DOMDocument;
	$dom->loadXML($newstr);
	if(!$dom) {
		$err_msg = '錯誤代碼：ENTER_SYS_005\n系統轉換異常\n~請重新登入~';
		err_msgAlert($err_msg, SSO_DOOR_URL);
		exit;
	}

	$sess_info = simplexml_import_dom($dom);
	if($sess_info->sess_alive == 'N') {
		$err_msg = '錯誤代碼：ENTER_SYS_004\n登入逾時\n~請重新登入~';
		return array(2, $err_msg, null, null, null);
	} else if($sess_info->sess_alive == 'Y') {
		return array(1, (string)$sess_info->ip, (string)$sess_info->user_id, (string)$sess_info->person_id);
	} else {
		$err_msg = '錯誤代碼：ENTER_SYS_003\n系統轉換異常\n~請重新登入~';
		return array(3, $err_msg, null, null, null);
	}
	/*********************************************************************
		$sess_info->sess_alive 	(登入是否逾時---Y/N)->$status(1,2,3)->1為成功，其他為異常
		$sess_info->ip			(登入時,Client端IP) ->$enter_ip
		$sess_info->user_id		(自訂帳號)          ->$user_id
		$sess_info->person_id	(身份證字號)        ->$person_id
		$sess_info->enter_time	(登入時間)			->$enter_time
	**********************************************************************/
}

//延長sso的session存活時間
//接受1個變數(token資訊)
function chk_ssoRefresh($mix_info) {
	$xml_txt = file_get_contents(SSO_DOOR_URL.'ssoCcuRightXML.php?cid='.$mix_info);
	$order   = array('\r\n', '\n', '\r');
	$replace = '';
	$err_msg = '';
	$newstr = str_replace($order, $replace, $xml_txt);
	$dom = new DOMDocument;
	$dom->loadXML($newstr);	
	if(!$dom) {
		//$err_msg = '錯誤代碼：ENTER_SYS_004\n系統轉換異常\n~請重新登入~';
		$err_msg = '錯誤代碼：ENTER_SYS_007\n系統轉換異常\n~請重新登入~';
		err_msgAlert($err_msg, SSO_DOOR_URL);
		exit;
	}
	$sess_info = simplexml_import_dom($dom);
	if($sess_info->sess_alive == 'Y') {
		return array(1, '');
	} else {
		//return array(0, '錯誤代碼：ENTER_SYS_003\n登入逾時\n~請重新登入~');
		return array(0, '錯誤代碼：ENTER_SYS_006\n登入逾時\n~請重新登入~');
	}
}

//錯誤訊息及導向頁面
//接受2個變數(錯誤訊息,導向頁面)
function err_msgAlert($msg, $url) {
	echo '<script>alert("'.$msg.'");window.location.href="'.$url.'";</script>';
}

//清空子系統session並關閉分頁
function ssoLogout() {
	//清空子系統端的session
	if(!isset($_SESSION))
		session_start();//have to start the session before you can unset or destroy it.
	session_unset();
	session_destroy();
	$_SESSION = array();
	//header('Location: '.SSO_DOOR_URL);
	echo '<noscript> <meta HTTP-EQUIV="REFRESH" content="0; url='.SSO_DOOR_URL.'"> </noscript>';//未開啟JS的話,用HTML轉到SSO入口
	echo '<script> window.close(); </script>';
}

/*
//如果是從sso代簽入的情況才延長session(in sso server)存活時間
if(isset($_SESSION['verifySso']) and trim($_SESSION['verifySso']) == 'Y') {
	//延長session存活
	list($status,$errorMsg) = chk_ssoRefresh($_SESSION['tokenSso']);
	if($status != 1) { //sso端登入失敗
		err_msgAlert($errorMsg, SSO_DOOR_URL);
	}

	//子系統已經登入,又再從SSO按下連結到子系統的情況,也需要重新導向到子系統的登入確認程式跑sso登入流程,補齊sso登入資訊
	if(isset($_GET['cid']) and (trim($_GET['cid']) != '') and isset($_GET['miXd']) and (trim($_GET['miXd']) != '')) {
		if((md5(sso_getIP().substr($_GET['miXd'],-10)).substr($_GET['miXd'], 10, 6) == $_GET['cid'])) {
			list($status, $enter_ip, $user_id, $person_id) = chk_ssoRight($_GET['miXd']);
			if($status == 1) //sso端登入成功
				header('Location: '.SYS_LOGIN_URL);
			else
				//err_msgAlert($enter_info,SSO_DOOR_URL);
				err_msgAlert($enter_ip, SSO_DOOR_URL);//失敗時enter_ip會是錯誤訊息
		}
	}
}
*/
?>