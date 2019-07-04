<?php
/*********************************************************************
	readssoCcuRightXML.php
	子系統端導入SSO接收資訊
	
	常數：
		SYS_DOOR_URL	子系統端登入頁
		SYS_LOGIN_URL	子系統端登入確認程式
		SSO_DOOR_URL	SSO端首頁
	重要SESSION變數：
		$_SESSION['verifyChild']	子系統端登入方式辨識訊號
		$_SESSION['verifySso']		SSO登入方式辨識訊號
		$_SESSION['tokenSso']		SSO登入token資訊
		$_SESSION['sso_enterip']	使用者端登入IP
		$_SESSION['sso_personid']	身份證字號
	函式：
		sso_getIP()					取得使用者IP
		chk_ssoRight($mix_info)		取得sso權限資訊
		chk_ssoRefresh($mix_info)	延長sso的session存活時間
		err_msgAlert($msg,$url)		錯誤訊息及導向頁面
		ssoLogOut()					SSO的登出導向
**********************************************************************/
//header('Content-type: text/html; charset=UTF-8');

//session不存在時，啟用session
if(!isset($_SESSION)) session_start();

//常數定義
define('SYS_DOOR_URL',"http://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/Query/index2.html"); //子系統端登入頁
define('SYS_LOGIN_URL',"http://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/Query/Query_grade.php"); //子系統端登入確認程式
define('SSO_DOOR_URL',"http://portal.ccu.edu.tw/");  //sso端首頁

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
function chk_ssoRight($mix_info){
        $xml_file = SSO_DOOR_URL.'ssoCcuRightXML.php?cid='.$mix_info;
	$xml_txt=file_get_contents($xml_file);
	$order   = array("\r\n", "\n", "\r");
	$replace = '';
	$err_msg = '';
	$newstr = str_replace($order, $replace, $xml_txt);
	$dom = new DOMDocument;
	$dom->loadXML($newstr);
	if (!$dom) {
		$err_msg='錯誤代碼：ENTER_SYS_005\n系統轉換異常\n~請重新登入~';
		err_msgAlert($err_msg,SSO_DOOR_URL);
		exit;
	}
	$sess_info = simplexml_import_dom($dom);
/*        echo "xml_file = $xml_file<BR>";
        echo "dom = ";
        print_r($dom);
        echo "<HR>";
        echo "mix_info = $mix_info<HR>";
        echo "xml_txt = $xml_txt<HR>";
        echo "newstr = $newstr<HR>";
        echo "session_info = ";
	print_r($session_info);
        echo "<HR>";
*/
	if($sess_info->sess_alive=='N'){
		$err_msg='錯誤代碼：ENTER_SYS_004\n登入逾時\n~請重新登入~';
		return array(2,$err_msg,null,null,null);
	}else if($sess_info->sess_alive=='Y'){
		return array(1,(string)$sess_info->ip,(string)$sess_info->user_id,(string)$sess_info->person_id);
	}else{
		$err_msg='錯誤代碼：ENTER_SYS_003\n系統轉換異常\n~請重新登入~';
		return array(3,$err_msg,null,null,null);
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
function chk_ssoRefresh($mix_info){
	$xml_txt=file_get_contents(SSO_DOOR_URL.'ssoCcuRightXML.php?cid='.$mix_info);
	$order   = array("\r\n", "\n", "\r");
	$replace = '';
	$err_msg = '';
	$newstr = str_replace($order, $replace, $xml_txt);
	$dom = new DOMDocument;
	$dom->loadXML($newstr);
	if (!$dom) {
		$err_msg='錯誤代碼：ENTER_SYS_005\n系統轉換異常\n~請重新登入~';
		err_msgAlert($err_msg,SSO_DOOR_URL);
		exit;
	}
	$sess_info = simplexml_import_dom($dom);
	if($sess_info->sess_alive == 'Y'){
		return array(1,'');
	}else{
		return array(0,'錯誤代碼：ENTER_SYS_004\n登入逾時\n~請重新登入~');
	}
}

//錯誤訊息及導向頁面
//接受2個變數(錯誤訊息,導向頁面)
function err_msgAlert($msg,$url){
	echo '<script>alert("'.$msg.'");window.location.href="'.$url.'";</script>';
}

//清空子系統session回到sso首頁
function ssoLogOut(){
	//清空子系統端的session
	$_SESSION=array();
	session_destroy();
	//換頁至子系統端登入確認的程式處理各子系統端所需要的額外資訊
	header('Location: '.SSO_DOOR_URL);
}

if(!isset($_SESSION['verifyChild'])){ //若不是從子系統端登入者，才執行

	if(isset($_SESSION['verifySso']) and trim($_SESSION['verifySso'])=="Y"){

		//延長session存活
		chk_ssoRefresh($_SESSION['tokenSso']);
		if(isset($_GET['cid']) and (trim($_GET['cid']) != "") and isset($_GET['miXd']) and (trim($_GET['miXd']) != "")){
            header('Location: '.SYS_LOGIN_URL);
        }
		
	}else{

		//登入
		if(isset($_GET['cid']) and (trim($_GET['cid']) != "") and isset($_GET['miXd']) and (trim($_GET['miXd']) != "")){
			
			if((md5(sso_getIP().substr($_GET['miXd'],-10)).substr($_GET['miXd'],10,6)==$_GET['cid'])){  
			//驗證IP是否為同一個IP
			
				//list($status,$enter_info,$enter_ip,$user_id,$person_id)=chk_ssoRight($_GET['miXd']);
				list($status,$enter_ip,$user_id,$person_id)=chk_ssoRight($_GET['miXd']);
				//接收SSO資料
				
				print_r($status);
				if($status == 1){ //sso端登入成功
				
					//登入成功的動作
					//將資訊丟給子系統端的session去操作
					$_SESSION['sso_enterip']=$enter_ip;		//使用者端登入IP
					$_SESSION['sso_personid']=$person_id;	//身份證字號
					$_SESSION['tokenSso']=$_GET['miXd'];	//sso token
					$_SESSION['verifySso']="Y";				//sso登入識別
					
					//換頁至子系統端登入確認的程式處理各子系統端所需要的額外資訊
					header('Location: '.SYS_LOGIN_URL); 
					
				}else{
					err_msgAlert($enter_info,SSO_DOOR_URL);
				}
				
			}else{
				err_msgAlert("錯誤代碼：ENTER_SYS_002\n登入資訊錯誤！\n~請重新登入~",SSO_DOOR_URL);
			}
			
		}else{
			err_msgAlert("錯誤代碼：ENTER_SYS_001\n登入資訊錯誤！\n~請重新登入~",SSO_DOOR_URL);
		}
		
	}

}

?>