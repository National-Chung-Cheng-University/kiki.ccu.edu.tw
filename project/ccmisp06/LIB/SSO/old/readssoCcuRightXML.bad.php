<?php
/*********************************************************************
	readssoCcuRightXML.php
	�l�t�κݾɤJSSO������T
	
	�`�ơG
		SYS_DOOR_URL	�l�t�κݵn�J��
		SYS_LOGIN_URL	�l�t�κݵn�J�T�{�{��
		SSO_DOOR_URL	SSO�ݭ���
	���nSESSION�ܼơG
		$_SESSION['verifyChild']	�l�t�κݵn�J�覡���ѰT��
		$_SESSION['verifySso']		SSO�n�J�覡���ѰT��
		$_SESSION['tokenSso']		SSO�n�Jtoken��T
		$_SESSION['sso_enterip']	�ϥΪ̺ݵn�JIP
		$_SESSION['sso_personid']	�����Ҧr��
	�禡�G
		sso_getIP()					���o�ϥΪ�IP
		chk_ssoRight($mix_info)		���osso�v����T
		chk_ssoRefresh($mix_info)	����sso��session�s���ɶ�
		err_msgAlert($msg,$url)		���~�T���ξɦV����
		ssoLogOut()					SSO���n�X�ɦV
**********************************************************************/
//header('Content-type: text/html; charset=UTF-8');

//session���s�b�ɡA�ҥ�session
if(!isset($_SESSION)) session_start();

//�`�Ʃw�q
define('SYS_DOOR_URL',"http://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/Query/index2.html"); //�l�t�κݵn�J��
define('SYS_LOGIN_URL',"http://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/Query/Query_grade.php"); //�l�t�κݵn�J�T�{�{��
define('SSO_DOOR_URL',"http://portal.ccu.edu.tw/");  //sso�ݭ���

//���o�ϥΪ�IP
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

//���osso�v����T
//����1���ܼ�(token��T)�A�^��5���ܼ�
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
		$err_msg='���~�N�X�GENTER_SYS_005\n�t���ഫ���`\n~�Э��s�n�J~';
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
		$err_msg='���~�N�X�GENTER_SYS_004\n�n�J�O��\n~�Э��s�n�J~';
		return array(2,$err_msg,null,null,null);
	}else if($sess_info->sess_alive=='Y'){
		return array(1,(string)$sess_info->ip,(string)$sess_info->user_id,(string)$sess_info->person_id);
	}else{
		$err_msg='���~�N�X�GENTER_SYS_003\n�t���ഫ���`\n~�Э��s�n�J~';
		return array(3,$err_msg,null,null,null);
	}
	/*********************************************************************
		$sess_info->sess_alive 	(�n�J�O�_�O��---Y/N)->$status(1,2,3)->1�����\�A��L�����`
		$sess_info->ip			(�n�J��,Client��IP) ->$enter_ip
		$sess_info->user_id		(�ۭq�b��)          ->$user_id
		$sess_info->person_id	(�����Ҧr��)        ->$person_id
		$sess_info->enter_time	(�n�J�ɶ�)			->$enter_time
	**********************************************************************/
}

//����sso��session�s���ɶ�
//����1���ܼ�(token��T)
function chk_ssoRefresh($mix_info){
	$xml_txt=file_get_contents(SSO_DOOR_URL.'ssoCcuRightXML.php?cid='.$mix_info);
	$order   = array("\r\n", "\n", "\r");
	$replace = '';
	$err_msg = '';
	$newstr = str_replace($order, $replace, $xml_txt);
	$dom = new DOMDocument;
	$dom->loadXML($newstr);
	if (!$dom) {
		$err_msg='���~�N�X�GENTER_SYS_005\n�t���ഫ���`\n~�Э��s�n�J~';
		err_msgAlert($err_msg,SSO_DOOR_URL);
		exit;
	}
	$sess_info = simplexml_import_dom($dom);
	if($sess_info->sess_alive == 'Y'){
		return array(1,'');
	}else{
		return array(0,'���~�N�X�GENTER_SYS_004\n�n�J�O��\n~�Э��s�n�J~');
	}
}

//���~�T���ξɦV����
//����2���ܼ�(���~�T��,�ɦV����)
function err_msgAlert($msg,$url){
	echo '<script>alert("'.$msg.'");window.location.href="'.$url.'";</script>';
}

//�M�Ťl�t��session�^��sso����
function ssoLogOut(){
	//�M�Ťl�t�κݪ�session
	$_SESSION=array();
	session_destroy();
	//�����ܤl�t�κݵn�J�T�{���{���B�z�U�l�t�κݩһݭn���B�~��T
	header('Location: '.SSO_DOOR_URL);
}

if(!isset($_SESSION['verifyChild'])){ //�Y���O�q�l�t�κݵn�J�̡A�~����

	if(isset($_SESSION['verifySso']) and trim($_SESSION['verifySso'])=="Y"){

		//����session�s��
		chk_ssoRefresh($_SESSION['tokenSso']);
		if(isset($_GET['cid']) and (trim($_GET['cid']) != "") and isset($_GET['miXd']) and (trim($_GET['miXd']) != "")){
            header('Location: '.SYS_LOGIN_URL);
        }
		
	}else{

		//�n�J
		if(isset($_GET['cid']) and (trim($_GET['cid']) != "") and isset($_GET['miXd']) and (trim($_GET['miXd']) != "")){
			
			if((md5(sso_getIP().substr($_GET['miXd'],-10)).substr($_GET['miXd'],10,6)==$_GET['cid'])){  
			//����IP�O�_���P�@��IP
			
				//list($status,$enter_info,$enter_ip,$user_id,$person_id)=chk_ssoRight($_GET['miXd']);
				list($status,$enter_ip,$user_id,$person_id)=chk_ssoRight($_GET['miXd']);
				//����SSO���
				
				print_r($status);
				if($status == 1){ //sso�ݵn�J���\
				
					//�n�J���\���ʧ@
					//�N��T�ᵹ�l�t�κݪ�session�h�ާ@
					$_SESSION['sso_enterip']=$enter_ip;		//�ϥΪ̺ݵn�JIP
					$_SESSION['sso_personid']=$person_id;	//�����Ҧr��
					$_SESSION['tokenSso']=$_GET['miXd'];	//sso token
					$_SESSION['verifySso']="Y";				//sso�n�J�ѧO
					
					//�����ܤl�t�κݵn�J�T�{���{���B�z�U�l�t�κݩһݭn���B�~��T
					header('Location: '.SYS_LOGIN_URL); 
					
				}else{
					err_msgAlert($enter_info,SSO_DOOR_URL);
				}
				
			}else{
				err_msgAlert("���~�N�X�GENTER_SYS_002\n�n�J��T���~�I\n~�Э��s�n�J~",SSO_DOOR_URL);
			}
			
		}else{
			err_msgAlert("���~�N�X�GENTER_SYS_001\n�n�J��T���~�I\n~�Э��s�n�J~",SSO_DOOR_URL);
		}
		
	}

}

?>