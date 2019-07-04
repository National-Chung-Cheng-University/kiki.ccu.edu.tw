1;

##  取得使用者輸入          			 	  ##
##  input : none            				  ##
##  output: %FORM           				  ##
##  98/01/20  ionic  整理   				  ##
##  sub function User_Input                               ##
##  輸入欄位名稱為 $name 時，其使用者輸入為 $FORM{$name}  ##
##  NOTICE: 如果輸入為複選時, 其多重輸入以 *:::* 作為區隔 ##
##  2005/02/15 新增修改:
##    為了讓本函式和 CGI.pm 並存, 若使用 CGI.pm 的程式,
##    會丟一個 $fake_query_string 進來, 讓這裡也能讀到資料.
##    Nidalap :D~

##  特別注意：若透過 POST 傳值，第二次呼叫此函式會抓不到資料！
sub User_Input
{
  local ($buffer,@datas,$data,$name,$value,%FORM);
  my ($fake_query_string) = @_;
  if( $fake_query_string eq "") {
    $ENV{'REQUEST_METHOD'}=~ tr/a-z/A-Z/;
    if($ENV{'REQUEST_METHOD'} eq "POST")  {
       read(STDIN,$buffer,$ENV{'CONTENT_LENGTH'});
    }else{
       $buffer=$ENV{'QUERY_STRING'};
    }
  }else{
    $buffer = $fake_query_string;
  }
  
  #print "buffer = " . $buffer;
  
  @datas=split(/&/,$buffer);
  foreach $data(@datas)  {
    ($name,$value)=split(/=/,$data);
    $value=~ tr/+/ /;
    $value=~ s/%(..)/pack("C",hex($1))/eg;
    
    if( $FORM{$name} )   ## 如果 $FORM{$name} 已經有值, 代表為複選
    {
     $FORM{$name} = join ("*:::*",$FORM{$name},$value) ; 
    }
    else
    {
     $FORM{$name}=$value;
    }
  }
  %FORM;
} 
##################################################################################
#####  檢查非法字元
#####  2008/06/02 Nidalap :D~
#####  輸入: 要檢查的字串, 可能是要查詢的教師姓名, 科目名稱 etc
#####  輸出: ($illigal_flag, $output) = (是否包含非法字元, 將非法字元 escape 後的結果)
sub Check_Input_Illigal
{
  my($input) = @_;
  my $output = $input;
  my($illegal_flag);
#  $illegal_chars = array('~', ';', '\\\\', '\\.', '\\`', '"');
  
  my @illegal_chars = ( '\\\\', '\/', '~', ';', '%', '\*', '\?', '\|' );

  foreach $char (@illegal_chars) {
#    print("comparing $input with $char ...<BR>\n");
    if( $input =~ /$char/ ) {
      $illegal_flag = 1;
      
      $output =~ s/$char/\\$char/;

#      print("請勿輸入非法字元, 諸如 \\, /, %, *. ? 等 <BR>\n");
#      exit();
    }
  }
  $output = quotes($output);
  
  return ($illegal_flag, $output);
#  if( $illegal_flag == 1 ) {
#    print("非法字元!<BR>\n");
#  }
}

