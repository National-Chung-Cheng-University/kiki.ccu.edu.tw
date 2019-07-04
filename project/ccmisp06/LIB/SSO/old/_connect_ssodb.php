<?PHP
/**
 * "single sign on" db_info
 */
$DB_SERVER='140.123.5.202';
$DB_DATABASE='ssoman_db';
$DB_USER='root';
$DB_PASSWORD='mysql@ccu';

$message = "資料庫沒有回應,請稍候再試!!!!!";
$message2 = "資料庫不存在,請通知電算中心!~~";

$SQL=mysql_connect($DB_SERVER,$DB_USER,$DB_PASSWORD)
                or show_error_message($message);
mysql_select_db($DB_DATABASE,$SQL)
                or show_error_message($message2);
?>