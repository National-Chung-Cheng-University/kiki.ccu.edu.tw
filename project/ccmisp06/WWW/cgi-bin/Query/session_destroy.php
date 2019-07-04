<?PHP


session_start();
$_SESSION = array();
session_destroy();

echo "ok!";
echo "Session = ";
print_r($_SESSION);

?>