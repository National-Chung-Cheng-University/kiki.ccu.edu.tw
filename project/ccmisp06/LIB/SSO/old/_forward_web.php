<?php

include "_connect_ssodb.php";
include "comm.php";

$cid=(isset($_GET['cid'])) ? trim($_GET['cid']) : NULL;
$mixID = (isset($_GET['miXD'])) ? trim($_GET['miXD']):NULL;

$_token=NULL;
$_login_id=NULL;
$permit=NULL;

if(!empty($cid)) {

	$_token = $cid;
        //$_login_id=substr($mixID,4);
	//$id = $mixID; //decode($_login_id);
	$id = sso_id_decode($mixID);
	if($id == "F130601084"){
            $member_id = "CCUtest"; //帳號轉換
        }
	if(!checkToken($_token,$SQL)){
                $message = "閒置逾時或權限不足,請重新登錄！";
                show_error_message($message);
        }
	//valid token
	$permit=1;
}

?>
