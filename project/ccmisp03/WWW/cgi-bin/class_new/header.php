<?PHP
  include "../library/Reference.php";
  
  $dir = $WWW_PATH . "Graph/title_bg/";
  
  ###  �q $dir ���H����@�i jpg �ϧ@�������I��
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

?>

<body>
<center>
  <TABLE border=0 width=100% cellpadding=0 cellspacing=0>
    <TR>
      <TD align=CENTER background="<?PHP echo $url ?>">
        <IMG src="../../Graph/title.gif">
        <IMG src="../../Graph/gourd.gif">
      </TD>
    </TR>
  </TABLE>

</CENTER>
</BODY>  
