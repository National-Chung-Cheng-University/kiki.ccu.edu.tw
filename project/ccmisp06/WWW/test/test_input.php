<HTML>
  <HEAD>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <TITLE>�S���Ÿ���J����</TITLE>

    <SCRIPT type="text/javascript">
      var copied_text
      
      function refresh()
      {
        document.getElementById("submit").click()
      }

      function copy_text()
      {
        copied_text = document.getElementById("title").value
      }

      function sup_text()
      {
        var string_content = document.getElementById("title").value
        string_content = string_content.concat("<SUP></SUP>")
        document.getElementById("title").value = string_content
      }
      function sub_text()
      {
        var string_content = document.getElementById("title").value
        string_content = string_content.concat("<SUB></SUB>")
        document.getElementById("title").value = string_content
      }
      function bold_text()
      {
        var string_content = document.getElementById("title").value
        string_content = string_content.concat("<B></B>")
        document.getElementById("title").value = string_content
      }

    </SCRIPT>
    
  </HEAD>
  
  <BODY>
    <FORM>
      <INPUT type=BUTTON value="�W�Цr" onClick=sup_text();>
      <INPUT type=BUTTON value="�U�Цr" onClick=sub_text();>
      <INPUT type=BUTTON value="����r" onClick=bold_text()>
      <P>
      Enter Title: <INPUT type=text id="title" name="title" value="<?php echo $title ?>" size=100 onBlur=refresh()>
      <P>
      �z��J���O: 
        <TABLE border=1>
          <TR><TD bgcolor=LIGHTYELLOW>
            <FONT face="Arial" size=5><?php echo $title ?></FONT>
          </TD></TR>
        </TABLE>
      <P>
      <INPUT type=SUBMIT id=submit>
      <HR>
      Examples:
      <OL>
        <LI>Transport properties of La<SUB>0.67</SUB>Ca<SUB>0.33</SUB>MnO<SUB>3</SUB>
            <INPUT size=100 value="Transport properties of La<SUB>0.67</SUB>Ca<SUB>0.33</SUB>MnO<SUB>3</SUB>">
        <LI>Solving ��u+K(|x|)u<SUP>p</SUP> = 0 in <B>R</B><SUP>n</SUP>
            <INPUT size=100 value="Solving ��u+K(|x|)u<SUP>p</SUP> = 0 in <B>R</B><SUP>n</SUP>">
        <LI>Minimizing ��<SUB>�[</SUB>|��u|<SUP>2</SUP> /(��<SUB>�[</SUB>u<SUP>p+1</SUP>)<SUP>2/p+1</SUP>
            <INPUT size=100 value="Minimizing ��<SUB>�[</SUB>|��u|<SUP>2</SUP> /(��<SUB>�[</SUB>u<SUP>p+1</SUP>)<SUP>2/p+1</SUP>">
        <LI>�� -x<SUP>2</SUP><BR> �� e   dx = �ԣk<BR>-�� 
            <BR><INPUT size=100 value="�� -x<SUP>2</SUP><BR> �� e   dx = �ԣk<BR>-�� ">
            <BR><FONT color=RED>Warning! �o�ئh�檺�@�k, �N���{�Τj�q�ťսվ��m���~��, �G����ĳ.</FONT>
        <LI>�n�D�}�G�� <IMG align=center src="complex.jpg"> �M�L�k�ѨM��  <IMG align=center src="complex2.jpg">, �u���ι�..
            <INPUT size=100 value="�n�D�}�G�� <IMG align=center src=complex.jpg> �M�L�k�ѨM�� <IMG  align=center src=complex2.jpg>, �u���ι�..">
            <BR><FONT color=RED>Warning: �ϥιϧ��ɪ���, ��J�����ݭn�A�J�ӳ]�p,  �����׸���.</FONT>
      </OL>
      <HR>
      Unsolved technical problems:
      <UL> 
        <LI>�g����۰� refresh
        <LI>�W�ФU�е��r���ƹ��ާ@��J
        <FONT color=RED>
        <LI>�L�k copy&paste ���r�βŸ�  <--- �y�r�ιϧ���
        <LI>�P�ɦ��W�U��  <---  �ϥ� ex.4 ���h��k��, �Ψϥγy�r�ιϧ���.
        </FONT>
      </UL>
    </FORM>

  </BODY>
</HTML>