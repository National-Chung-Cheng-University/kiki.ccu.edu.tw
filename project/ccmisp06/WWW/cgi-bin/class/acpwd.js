function star(){	
	var c=document.form1.temp_count.value.length;
	var i;
	var ls_flag=1;	// 預設字串中沒有*號
	var temp;
	var ls_data='';
	if(c<=4){
		var temp=document.form1.temp_count.value.toUpperCase()
		document.form1.id.value=temp;
		document.form1.temp_count.value=temp;
	}
	else{
		// 檢查看字串中有沒有*號
		for(i=1;i<=c;i++){
			temp=document.form1.temp_count.value.charAt(i-1);
			if(temp == '*'){
				// 表示字串中有*號
				ls_flag=2;
			}	
		}
		
		if(ls_flag==1){			
			document.form1.id.value=document.form1.temp_count.value.toUpperCase();
			for(i=1;i<=c;i++){
				temp=document.form1.temp_count.value.charAt(i-1);
				if (i>4){
					ls_data = ls_data + '*';
				}
				else{
					ls_data = ls_data + temp.toUpperCase();
				}
			}
			document.form1.temp_count.value=ls_data;
		}
		else{
			// 因為使用者可能刪除某個字元,或在字串中增加某個字元,就目前而言,無法得知使用者的操作內容,因此只能就
			// 帳號長度不一樣時,才觸發此段程式			
			if(document.form1.temp_count.value.length != document.form1.id.value.length){
				temp=document.form1.temp_count.value.charAt(c-1);
				temp=temp.toUpperCase();
				document.form1.id.value += temp;
				temp=document.form1.id.value.substr(0,4);
				temp=temp.toUpperCase();
				for(i=4;i<c;i++)
				{temp +=  '*' ;}
				document.form1.temp_count.value=temp;
			}
		}
	}
	
	delete_cookie('profession_cookie');
}


function key_end(){
	var c=document.form1.temp_count.value.length;
	var i;
	var temp;
	var ls_flag=1;	// 預設字串中沒有*號
	var ls_data='';
	for(i=1;i<=c;i++){
		temp=document.form1.temp_count.value.charAt(i-1);
		if(temp == '*'){
			// 表示字串中有*號
			ls_flag=2;
		}	
	}
	
	if(ls_flag==1){
		document.form1.id.value=document.form1.temp_count.value.toUpperCase();
		for(i=1;i<=c;i++){
			temp=document.form1.temp_count.value.charAt(i-1);
			if (i>4){
				ls_data = ls_data + '*';
			}
			else{
				ls_data = ls_data + temp.toUpperCase();
			}
		}
		document.form1.temp_count.value=ls_data;
	}
}


function Submitform()
{
	var user =document.form1.id.value;
	set_procookie('profession_cookie',user);
}

function sf()
{
	document.form1.temp_count.focus(); 

	var user=get_cookie('profession_cookie');
	if (user!=null)
		{
			document.form1.id.value=user;
			var temp=user.substr(0,4);
			var templen=user.length - 4
			var i;
			for(i=1;i<=templen;i++)
			{temp +=  '*' ;}
			document.form1.temp_count.value=temp;			
			document.form1.pwd.focus(); 
		}
}


var today= new Date();
var end_day= new Date();
var mspermonth=24*3600*1000*31;
end_day.setTime(today.getTime() + mspermonth);
function set_procookie( cookiename,cookievalue){	document.cookie=cookiename +"=" + cookievalue +"; expires=" + end_day.toGMTString();}

function get_cookie(key)
{
	var search=key + "=";
	begin= document.cookie.indexOf(search);
	if(begin != -1)
	{
		begin += search.length;
		end=document.cookie.indexOf(";",begin);
		if(end == -1)	end = document.cookie.length;
		return document.cookie.substring(begin,end);
		
	}
}

function delete_cookie ( cookie_name )
{
  today.setTime ( today.getTime() - 1 );
  document.cookie = cookie_name += "=; expires=" + today.toGMTString();
}


;
