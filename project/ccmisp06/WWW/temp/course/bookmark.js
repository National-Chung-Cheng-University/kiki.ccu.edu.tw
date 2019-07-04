//
// Copyright (c) 2006 by Conor O'Mahony.
// For enquiries, please email GubuSoft@GubuSoft.com.
// Please keep all copyright notices below.
// Original author of TreeView script is Marcelino Martins.
//
// This document includes the TreeView script.
// The TreeView script can be found at http://www.TreeView.net.
// The script is Copyright (c) 2006 by Conor O'Mahony.
//
// You can find general instructions for this file at www.treeview.net.
//

USETEXTLINKS = 1
STARTALLOPEN = 1
USEFRAMES = 0
USEICONS = 0
WRAPTEXT = 1
PRESERVESTATE = 1
HIGHLIGHT = 1


//
// The following code constructs the tree.
//
foldersTree = gFld("<b>主選單</b>", "")
  aux2 = insFld(foldersTree, gFld("系統公告", ""))
    insDoc(aux2, gLnk("R", "選課系統公告", "announce.html"))
    insDoc(aux2, gLnk("R", "系統開放時程", "announce2.html"))
    
  aux2 = insFld(foldersTree, gFld("選課系統相關", ""))
    insDoc(aux2, gLnk("R", "加選", "Add_Course00.html"))
    insDoc(aux2, gLnk("R", "退選", "Del_Course00.html"))
    insDoc(aux2, gLnk("R", "檢視已選修科目", "Selected_View00.html"))
    insDoc(aux2, gLnk("R", "檢視篩選公告", "View_Warning.html"))
    insDoc(aux2, gLnk("R", "檢視畢業資格審查表", "Print_Graduate_pdf.html"))
    insDoc(aux2, gLnk("R", "列印選課單", "Print_Course.html"))
    insDoc(aux2, gLnk("R", "更改密碼", "Change_Password00.html"))
    
  aux2 = insFld(foldersTree, gFld("資料查詢", ""))
    insDoc(aux2, gLnk("R", "查詢開課資料", "http://kiki.ccu.edu.tw/~ccmisp06/Course/"))
    insDoc(aux2, gLnk("R", "以時間查詢開課資料", "http://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/Query/Query_by_time1.cgi"))
    insDoc(aux2, gLnk("R", "檢視所有異動科目", "http://kiki.ccu.edu.tw/~ccmisp06/Update_Course.html"))
    insDoc(aux2, gLnk("R", "成績查詢", "http://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/Query/"))

  aux2 = insFld(foldersTree, gFld("常見問題與表單下載", ""))
    insDoc(aux2, gLnk("R", "常見問題", "http://kiki.ccu.edu.tw//contact.html"))
    insDoc(aux2, gLnk("R", "系統操作手冊", "http://kiki.ccu.edu.tw//user_manual/user_manual.htm"))
    insDoc(aux2, gLnk("B", "課表 doc 檔", "http://kiki.ccu.edu.tw/ccu_timetable.doc"))
    
  aux2 = insFld(foldersTree, gFld("其他系統服務", ""))
    insDoc(aux2, gLnk("B", "教務處", "http://www.ccu.edu.tw/oaa/oaa_english/index.php"))
    insDoc(aux2, gLnk("B", "學籍資料登錄系統", "http://mis.cc.ccu.edu.tw/academic/"))
    insDoc(aux2, gLnk("B", "資訊能力檢定", "http://infotest.ccu.edu.tw/"))
    insDoc(aux2, gLnk("B", "英文能力檢定", "http://lconline.ccu.edu.tw/"))
    
    
    

//
// Set this string if TreeView and other configuration files may also be loaded 
// in the same session.
//
foldersTree.treeID = "FramelessHili" 
 