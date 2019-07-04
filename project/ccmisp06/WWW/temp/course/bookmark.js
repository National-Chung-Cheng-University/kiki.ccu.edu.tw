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
foldersTree = gFld("<b>�D���</b>", "")
  aux2 = insFld(foldersTree, gFld("�t�Τ��i", ""))
    insDoc(aux2, gLnk("R", "��Ҩt�Τ��i", "announce.html"))
    insDoc(aux2, gLnk("R", "�t�ζ}��ɵ{", "announce2.html"))
    
  aux2 = insFld(foldersTree, gFld("��Ҩt�ά���", ""))
    insDoc(aux2, gLnk("R", "�[��", "Add_Course00.html"))
    insDoc(aux2, gLnk("R", "�h��", "Del_Course00.html"))
    insDoc(aux2, gLnk("R", "�˵��w��׬��", "Selected_View00.html"))
    insDoc(aux2, gLnk("R", "�˵��z�綠�i", "View_Warning.html"))
    insDoc(aux2, gLnk("R", "�˵����~���f�d��", "Print_Graduate_pdf.html"))
    insDoc(aux2, gLnk("R", "�C�L��ҳ�", "Print_Course.html"))
    insDoc(aux2, gLnk("R", "���K�X", "Change_Password00.html"))
    
  aux2 = insFld(foldersTree, gFld("��Ƭd��", ""))
    insDoc(aux2, gLnk("R", "�d�߶}�Ҹ��", "http://kiki.ccu.edu.tw/~ccmisp06/Course/"))
    insDoc(aux2, gLnk("R", "�H�ɶ��d�߶}�Ҹ��", "http://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/Query/Query_by_time1.cgi"))
    insDoc(aux2, gLnk("R", "�˵��Ҧ����ʬ��", "http://kiki.ccu.edu.tw/~ccmisp06/Update_Course.html"))
    insDoc(aux2, gLnk("R", "���Z�d��", "http://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/Query/"))

  aux2 = insFld(foldersTree, gFld("�`�����D�P���U��", ""))
    insDoc(aux2, gLnk("R", "�`�����D", "http://kiki.ccu.edu.tw//contact.html"))
    insDoc(aux2, gLnk("R", "�t�ξާ@��U", "http://kiki.ccu.edu.tw//user_manual/user_manual.htm"))
    insDoc(aux2, gLnk("B", "�Ҫ� doc ��", "http://kiki.ccu.edu.tw/ccu_timetable.doc"))
    
  aux2 = insFld(foldersTree, gFld("��L�t�ΪA��", ""))
    insDoc(aux2, gLnk("B", "�аȳB", "http://www.ccu.edu.tw/oaa/oaa_english/index.php"))
    insDoc(aux2, gLnk("B", "���y��Ƶn���t��", "http://mis.cc.ccu.edu.tw/academic/"))
    insDoc(aux2, gLnk("B", "��T��O�˩w", "http://infotest.ccu.edu.tw/"))
    insDoc(aux2, gLnk("B", "�^���O�˩w", "http://lconline.ccu.edu.tw/"))
    
    
    

//
// Set this string if TreeView and other configuration files may also be loaded 
// in the same session.
//
foldersTree.treeID = "FramelessHili" 
 