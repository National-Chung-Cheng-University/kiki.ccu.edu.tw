<?PHP
  /////  interceptSSO.php
  /////  從 SSO 連過來時，應呼叫此程式，而非標準 readssoCcuRightXML.php
  /////  此程式預先做些許選課系統內部設定。
  /////  Updates:
  /////    2012/09/05 Created by Nidalap :D~
  
  session_save_path("/NFS/session"); 
  require_once("getssoCcuRight.php");
 
?>