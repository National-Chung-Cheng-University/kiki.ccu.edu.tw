<?php
/*********************************************************************
	refreshSso.php
	子系統端延長SSO端的session存活時間
	(子系統的每個page都include此php檔, 每次更新頁面就會自動延長sso存活時間了)
	Last update : 2011/09/29
****系統需求：php4.0****

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

	註：使用if(isset($_SESSION['verifySso']) and trim($_SESSION['verifySso'])=="Y")判斷是否從sso端登入
	    若是改在測試平台，請開啟define('_TEST_PLATFORM',true);這一行
**********************************************************************/
//header('Content-type: text/html; charset=UTF-8'); //代簽入非UTF-8的子系統時不需要這行, 檔案格式也需要存成ansi

//session不存在時，啟用session
if(!isset($_SESSION)) session_start();

//測試平台請開啟這一行
//define('_TEST_PLATFORM', true);

if(!defined('_TEST_PLATFORM')) { //正式平台
	//常數定義
	define('SYS_DOOR_URL', '子系統端登入頁'); //子系統端登入頁
	define('SYS_LOGIN_URL', '子系統端登入確認程式'); //子系統端登入確認程式
	define('SSO_DOOR_URL', 'http://portal.ccu.edu.tw/');
} else { //測試平台
	//常數定義
	define('SYS_DOOR_URL', '子系統端測試平台登入頁'); //子系統端登入頁
	define('SYS_LOGIN_URL', '子系統端測試平台登入確認程式'); //子系統端登入確認程式
	define('SSO_DOOR_URL', 'http://osa.ccu.edu.tw/~porihuang/'); //sso端首頁
}

//取得使用者IP
function sso_getIP(){
	if(!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
		$route=$_SERVER['HTTP_X_FORWARDED_FOR'];
		$ip=split(',', $route);
	}else{
		$route='';
	}
	$ip=(empty($route))? $_SERVER['REMOTE_ADDR']: $ip[0];
	return $ip;
}

//取得sso權限資訊
//接受1個變數(token資訊)，回傳5個變數
function chk_ssoRight($mix_info) {
	$xml_txt = file_get_contents(SSO_DOOR_URL.'ssoCcuRightXML.php?cid='.$mix_info);
	$resultArray = parseXML($xml_txt);

	if(count($resultArray) > 0) {
		if($resultArray['SESS_ALIVE'] == 'N') {
			$err_msg = '錯誤代碼：ENTER_SYS_004\n登入逾時\n~請重新登入~';
			return array(2, $err_msg, null, null, null);
		}else if($resultArray['SESS_ALIVE'] == 'Y') {
			return array(1, (string)$resultArray['IP'], (string)$resultArray['USER_ID'], (string)$resultArray['PERSON_ID']);
		}
	} else {
		$err_msg = '錯誤代碼：ENTER_SYS_003\n系統轉換異常\n~請重新登入~';
		return array(3, $err_msg, null, null, null);
	}
	/*********************************************************************
		$resultArray['SESS_ALIVE'] 	(登入是否逾時---Y/N)->$status(1,2,3)->1為成功，其他為異常
		$resultArray['IP']			(登入時,Client端IP) ->$enter_ip
		$resultArray['USER_ID']		(自訂帳號)          ->$user_id
		$resultArray['PERSON_ID']	(身份證字號)        ->$person_id
		$resultArray['ENTER_TIME']	(登入時間)			->$enter_time
	**********************************************************************/








//以上留白是為了符合說明文件當中的行數(與refreshSso.php同步)
}

//延長sso的session存活時間
//接受1個變數(token資訊)
function chk_ssoRefresh($mix_info) {
	$xml_txt = file_get_contents(SSO_DOOR_URL.'ssoCcuRightXML.php?cid='.$mix_info);
	$resultArray = parseXML($xml_txt);
	if(count($resultArray) > 0) {
		if($resultArray['SESS_ALIVE'] == 'N') {
			$err_msg = '錯誤代碼：ENTER_SYS_004\n登入逾時\n~請重新登入~';
			return array(0, $err_msg, null, null, null);
		} else if($resultArray['SESS_ALIVE'] == 'Y') {
			return array(1, '');
		}
	} else {
		$err_msg = '錯誤代碼：ENTER_SYS_003\n系統轉換異常\n~請重新登入~';
		return array(3, $err_msg, null, null, null);
	}




//以上留白是為了符合說明文件當中的行數(與refreshSso.php同步)
}

//錯誤訊息及導向頁面
//接受2個變數(錯誤訊息,導向頁面)
function err_msgAlert($msg, $url) {
	echo '<script>alert("'.$msg.'");window.location.href="'.$url.'";</script>';
}

//登出
function ssoLogOut() {
	//清空子系統端的session
	session_start();//have to start the session before you can unset or destroy it.
	session_unset();
	session_destroy();
	$_SESSION = array();
}

//如果是從sso代簽入的情況才延長session(in sso server)存活時間
if(isset($_SESSION['verifySso']) and trim($_SESSION['verifySso'])=='Y') {
	//延長session存活
	list($status,$errorMsg) = chk_ssoRefresh($_SESSION['tokenSso']);
	if($status != 1){ //sso端登入失敗
		err_msgAlert($errorMsg, SSO_DOOR_URL);
	}

	//已經登入，又再從SSO按下連結到子系統的情況，也需要重新導向到子系統的登入頁面
	if(isset($_GET['cid']) and (trim($_GET['cid']) != '') and isset($_GET['miXd']) and (trim($_GET['miXd']) != '')) {
		if((md5(sso_getIP().substr($_GET['miXd'],-10)).substr($_GET['miXd'],10,6)==$_GET['cid'])) {
			list($status,$enter_ip,$user_id,$person_id) = chk_ssoRight($_GET['miXd']);
			if($status == 1) //sso端登入成功
				header('Location: '.SYS_LOGIN_URL);
			else
				//err_msgAlert($enter_info,SSO_DOOR_URL);
				err_msgAlert($enter_ip, SSO_DOOR_URL);//失敗時enter_ip會是錯誤訊息
		}
	}
}

// php4.0不使用DOM分析XML
function parseXML($xml_txt) {
	$order = array("\r\n", "\n", "\r");
	$replace = '';
	$err_msg = '';
	$newstr = str_replace($order, $replace, $xml_txt);
	//$newstr=eregi_replace(">"."[[:space:]]+"."< ",">< ",$newstr);
	if($xmlparser = xml_parser_create()) {
		xml_parser_set_option($xmlparser, XML_OPTION_SKIP_WHITE, 1);
		xml_parse_into_struct($xmlparser, $newstr, $vals, $index);
		xml_parser_free($xmlparser);

		// 本來要動態加入array element,不過搞不定,只好寫死, 以後xml有變動的話,這邊再來改了
		$resultArray = array($vals[1]['tag'] => $vals[1]['value'], $vals[2]['tag'] => $vals[2]['value'], $vals[3]['tag'] => $vals[3]['value'], $vals[4]['tag'] => $vals[4]['value'], $vals[5]['tag'] => $vals[5]['value']);
		/* 搞不定
		$i=0;
		$resultArray=array('test','test');
		foreach($vals as $element)
		{
			if($element['level'] == '2')
			{
				$s1=$element['tag'];
				$s2=$element['value'];
				//if($i==0){
				//	$resultArray = array($s1 => $s2);
				//}else{
					$tmpArray = array($s1 => $s2);
					//echo"tmpArray is</br>";
					//print_r($tmpArray);
					//echo"</br>";
					array_push($resultArray,$tmpArray);
				//}
				//$i++;
			}else{
				$i++;
				continue;
			}
		}
		*/
		return $resultArray;
	} else {
		// return an empty array when failure
		$resultArray;
		return $resultArray;
	}
}

?>