<?php

/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
/**
 * HTTP_X_FORWARDED_FOR只有使用Transparent Proxy(#1)時,裡面才會有東西
 * 否則裡面的資料是空的,使用Anonymous(#2),High Anonymity Proxy(#3)也是空的
 *
 * #1 透明代理伺服器,Transparent Proxy(Hinet的Proxy是Transparent Proxy)
 * #2 匿名代理伺服器,Anonymous Proxy
 * #3 高隱匿代理伺服器,High Anonymity Proxy
 */

function getIP(){
	if(!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
		$route=$_SERVER['HTTP_X_FORWARDED_FOR'];
		$ip=split(',', $route);
	}else{
		$route='';
	}
	$ip=(empty($route))? $_SERVER['REMOTE_ADDR']: $ip[0];

	return $ip;
}
function decode($id){
        $temp = array("v","X","d","w","Z","o","R","U","e","_");
        for($i=0;$i<strlen($id);$i++){
                $id_temp[$i] = substr($id,$i,1);
                if($i>1){
                        for($j=0;$j<10;$j++){
                                if($id_temp[$i] === $temp[$j]){
                                        $id_temp[$i] = $j;
                                }
                        }
                }
        }
        $id = implode("",$id_temp);
        return $id;
}

/**
 * check ip,loginout and renew the ExpireTime from DB
 */
function checkToken($token,$SQL) {
	$ip = getIP();
	$now_date=date("Y/m/d H:i:s",time());

	$qry="SELECT * FROM m13t_SsoToken
		WHERE TokenMd5 = '$token' and ExpireTime >= '$now_date'";
	$tbResult=mysql_query($qry,$SQL);
	$row=mysql_fetch_array($tbResult);
	if($row){
	        //check ip and logout
		if($row['LoginIp']!=$ip || $row['LogOut']){
			return false;
		}
		//in the expiretime,update 'ModDate','ExpireTime'
		$now_time=time();
//		$now_date=date("Y/m/d H:i:s",$now_time);
		$expire_time=date("Y/m/d H:i:s",$now_time+30*60);
		$sql2="UPDATE m13t_SsoToken
			SET ModDate = '$now_date',ExpireTime = '$expire_time'
			WHERE TokenMd5 ='$token'";
		$result1 = mysql_query($sql2,$SQL);
		return true;
	}else{
	        //invalid token or out of time
		return false;
	}
}

/**
 * show error message
 */

function show_error_message($msg){
        echo "<script>alert('$msg');";
        echo "window.close();</script>";
        exit();
}
?>
