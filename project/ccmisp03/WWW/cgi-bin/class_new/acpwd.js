function star(){	
	var c=document.form1.temp_count.value.length;
	var i;
	var ls_flag=1;	// �w�]�r�ꤤ�S��*��
	var temp;
	var ls_data='';
	if(c<=4){
		var temp=document.form1.temp_count.value.toUpperCase()
		document.form1.id.value=temp;
		document.form1.temp_count.value=temp;
	}
	else{
		// �ˬd�ݦr�ꤤ���S��*��
		for(i=1;i<=c;i++){
			temp=document.form1.temp_count.value.charAt(i-1);
			if(temp == '*'){
				// ��ܦr�ꤤ��*��
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
			// �]���ϥΪ̥i��R���Y�Ӧr��,�Φb�r�ꤤ�W�[�Y�Ӧr��,�N�ثe�Ө�,�L�k�o���ϥΪ̪��ާ@���e,�]���u��N
			// �b�����פ��@�ˮ�,�~Ĳ�o���q�{��			
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
	var ls_flag=1;	// �w�]�r�ꤤ�S��*��
	var ls_data='';
	for(i=1;i<=c;i++){
		temp=document.form1.temp_count.value.charAt(i-1);
		if(temp == '*'){
			// ��ܦr�ꤤ��*��
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
