<HTML>
  <HEAD>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <TITLE>特殊符號輸入測試</TITLE>

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
      <INPUT type=BUTTON value="上標字" onClick=sup_text();>
      <INPUT type=BUTTON value="下標字" onClick=sub_text();>
      <INPUT type=BUTTON value="粗體字" onClick=bold_text()>
      <P>
      Enter Title: <INPUT type=text id="title" name="title" value="<?php echo $title ?>" size=100 onBlur=refresh()>
      <P>
      您輸入的是: 
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
        <LI>Solving △u+K(|x|)u<SUP>p</SUP> = 0 in <B>R</B><SUP>n</SUP>
            <INPUT size=100 value="Solving △u+K(|x|)u<SUP>p</SUP> = 0 in <B>R</B><SUP>n</SUP>">
        <LI>Minimizing ∫<SUB>Ω</SUB>|▽u|<SUP>2</SUP> /(∫<SUB>Ω</SUB>u<SUP>p+1</SUP>)<SUP>2/p+1</SUP>
            <INPUT size=100 value="Minimizing ∫<SUB>Ω</SUB>|▽u|<SUP>2</SUP> /(∫<SUB>Ω</SUB>u<SUP>p+1</SUP>)<SUP>2/p+1</SUP>">
        <LI>∞ -x<SUP>2</SUP><BR> ∫ e   dx = √π<BR>-∞ 
            <BR><INPUT size=100 value="∞ -x<SUP>2</SUP><BR> ∫ e   dx = √π<BR>-∞ ">
            <BR><FONT color=RED>Warning! 這種多行的作法, 將面臨用大量空白調整位置的窘境, 故不建議.</FONT>
        <LI>要求漂亮的 <IMG align=center src="complex.jpg"> 和無法解決的  <IMG align=center src="complex2.jpg">, 只有用圖..
            <INPUT size=100 value="要求漂亮的 <IMG align=center src=complex.jpg> 和無法解決的 <IMG  align=center src=complex2.jpg>, 只有用圖..">
            <BR><FONT color=RED>Warning: 使用圖形檔的話, 輸入介面需要再仔細設計,  複雜度較高.</FONT>
      </OL>
      <HR>
      Unsolved technical problems:
      <UL> 
        <LI>寫完後自動 refresh
        <LI>上標下標等字的滑鼠操作輸入
        <FONT color=RED>
        <LI>無法 copy&paste 的字或符號  <--- 造字或圖形檔
        <LI>同時有上下標  <---  使用 ex.4 的多行法湊, 或使用造字或圖形檔.
        </FONT>
      </UL>
    </FORM>

  </BODY>
</HTML>
