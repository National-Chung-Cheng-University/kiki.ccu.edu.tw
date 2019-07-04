function AddWin()
{
	win=open("./AddTeacherWindow.html","openwin","width=200,height=350");
	win.creator=self;
}

function ClearAll(Select_Obj)
{
	Select_Obj.length=1;
	Select_Obj.options[0].value=99999;
	Select_Obj.options[0].text="教師未定";
}

//function RemoveWin()
//{
//	alert("HA HA HA....u r played by me....Y^_^Y");
//}

function isDelete(Select_Obj)
{
	//if(confirm("是否將未選擇之教師除去 ??")){
        if(confirm("DO YOU WANT TO REMOVE THESE UNSELECTED ITEMS??")){
		for(i=1; i<=Select_Obj.length; i++){
			if(Select_Obj.options[i-1].selected == false){
				Select_Obj.options[i-1]=null;
			}
		}
	}else{
		for(i=1; i<=Select_Obj.length; i++){
			if(Select_Obj.options[i-1].selected == false){
				Select_Obj.options[i-1].selected=true;
			}
		}
	}
}
