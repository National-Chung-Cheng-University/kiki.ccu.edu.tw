<?PHP
  require_once "../library/Reference.php";
  require_once $LIBRARY_PATH . "English.php";

  
  $dir = $WWW_PATH . "Graph/title_bg/";
  
  ///  從 $dir 內隨機找一張 jpg 圖作為本頁背景
  if( $DIR = opendir($dir) )  {
    while ( ($file = readdir($DIR)) != false) {
      if( preg_match("/.jpg/", $file) )   $files[] = $file;
    }
    closedir($DIR);    
    $num = count($files);
    $id  = rand(0, $num-1);
    $url = $GRAPH_URL . "title_bg/" . $files[$id];
  }else{
    $url = $GRAPH_URL . "title_bg.jpg";
  }
  ///  判斷中英文
  if( $IS_ENGLISH != 1 )
    $title_gif = "title.gif";
  else
    $title_gif = "title_e.gif";

?>

<body>
<center>
  <TABLE border=0 width=100% cellpadding=0 cellspacing=0>
    <TR>
      <TD align=CENTER background="<?PHP echo $url ?>">
        <IMG src="../../Graph/<?PHP echo $title_gif; ?>">
        <IMG src="../../Graph/gourd.gif">
      </TD>
    </TR>
  </TABLE>

</CENTER>
</BODY>  
