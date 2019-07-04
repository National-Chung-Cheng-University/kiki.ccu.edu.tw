<?php
require_once "comm.php";
if(isset($_SESSION["sso_token"])) {
	if(!checkToken($_SESSION["sso_token"],$SQL)) {
		session_destroy();
                $message = "閒置逾時或權限不足,請重新登錄！";
                show_error_message($message);
        }
}
?>
