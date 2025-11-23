Please create a agentic ai system that user can input text, then system will create flowchart image based on the followin code:
建立流程圖
dot = Digraph(comment='國際醫療器材來源流向管理流程圖', format='png')
dot.attr(rankdir='TB', size='15,20', dpi='300')
dot.attr('node', fontname='Microsoft JhengHei', fontsize='12', style='filled', fillcolor='white')
dot.attr('edge', fontname='Microsoft JhengHei', fontsize='11')
標題
dot.node('TITLE', '國際醫療器材來源流向管理現況研究\n整體執行流程圖',
shape='box', style='filled,bold', fillcolor='#4472C4', fontcolor='white', fontsize='16')
階段1：法規蒐集
dot.node('S1', '階段一：法規與執行現況蒐集', shape='box', fillcolor='#D9E8FF', fontsize='14')
dot.node('C1', '美國 FDA UDI 法規及執行情形\n(21 CFR Part 801, 830, GUDID資料庫)', shape='rect', fillcolor='#F0F8FF')
dot.node('C2', '歐盟 MDR/IVDR UDI 要求\n(EUDAMED、基本UDI-DI、UDI-DI/UDI-PI)', shape='rect', fillcolor='#F0F8FF')
dot.node('C3', '澳洲 TGA UDI 制度\n(AusUDID資料庫、與IMDRF一致性)', shape='rect', fillcolor='#F0F8FF')
dot.node('C4', '中國大陸 NMPA 唯一識別制度\n(UDI資料庫第一階段上線、2022年起分階段實施)', shape='rect', fillcolor='#F0F8FF')
dot.node('C5', '韓國 MFDS UDI 制度\n(K-UDI資料庫、2021-2025分階段實施)', shape='rect', fillcolor='#F0F8FF')
dot.node('C6', '新加坡 HSA UDI 要求\n(與IMDRF高度一致、2022年起實施)', shape='rect', fillcolor='#F0F8FF')
dot.node('C7', 'IMDRF UDI 指導原則\n(UDI系統核心文件、認可機構、資料庫要求)', shape='rect', fillcolor='#F0F8FF')
階段2：比較分析
dot.node('S2', '階段二：各國法規比較分析', shape='box', fillcolor='#FFE6E6', fontsize='14')
dot.node('A1', '法規架構與強制性比較', shape='ellipse', fillcolor='#FFF2CC')
dot.node('A2', 'UDI組成要件與格式規範比較\n(UDI-DI、UDI-PI、AIDC與HRI)', shape='ellipse', fillcolor='#FFF2CC')
dot.node('A3', '資料庫建置與資料上傳要求比較\n(公開程度、資料項目、更新頻率)', shape='ellipse', fillcolor='#FFF2CC')
dot.node('A4', '認可發行機構(Accrediting Agency)比較', shape='ellipse', fillcolor='#FFF2CC')
dot.node('A5', '實施時程與豁免範圍比較', shape='ellipse', fillcolor='#FFF2CC')
dot.node('A6', '與供應鏈追溯整合程度比較', shape='ellipse', fillcolor='#FFF2CC')
階段3：報告產出與我國建議
dot.node('S3', '階段三：報告產出與我國參採建議', shape='box', fillcolor='#E6FFE6', fontsize='14')
dot.node('R1', '各國法規與指引摘要報告', shape='note', fillcolor='#F0FFF0')
dot.node('R2', '國際比較分析矩陣表', shape='note', fillcolor='#F0FFF0')
dot.node('R3', '我國醫療器材唯一識別(UDI)制度建置建議\n(含法規架構、實施時程、分階段策略)', shape='note', fillcolor='#F0FFF0')
dot.node('R4', '我國UDI資料庫規劃建議\n(與國際接軌、資料項目、公開原則)', shape='note', fillcolor='#F0FFF0')
dot.node('R5', '認可發行機構評估與選定建議', shape='note', fillcolor='#F0FFF0')
dot.node('R6', '與GDSN、EPCIS等國際追溯系統整合建議', shape='note', fillcolor='#F0FFF0')
dot.node('FINAL', '完成「國際醫療器材來源流向管理現況研究」\n提報衛生福利部食品藥物管理署',
shape='doubleoctagon', fillcolor='#FFD966', fontsize='14')
連線
dot.edge('TITLE', 'S1')
dot.edge('S1', 'C1'); dot.edge('S1', 'C2'); dot.edge('S1', 'C3')
dot.edge('S1', 'C4'); dot.edge('S1', 'C5'); dot.edge('S1', 'C6'); dot.edge('S1', 'C7')
dot.edge('C1', 'S2'); dot.edge('C2', 'S2'); dot.edge('C3', 'S2')
dot.edge('C4', 'S2'); dot.edge('C5', 'S2'); dot.edge('C6', 'S2'); dot.edge('C7', 'S2')
dot.edge('S2', 'A1'); dot.edge('S2', 'A2'); dot.edge('S2', 'A3')
dot.edge('S2', 'A4'); dot.edge('S2', 'A5'); dot.edge('S2', 'A6')
dot.edge('A1', 'S3'); dot.edge('A2', 'S3'); dot.edge('A3', 'S3')
dot.edge('A4', 'S3'); dot.edge('A5', 'S3'); dot.edge('A6', 'S3')
dot.edge('S3', 'R1'); dot.edge('S3', 'R2'); dot.edge('S3', 'R3')
dot.edge('S3', 'R4'); dot.edge('S3', 'R5'); dot.edge('S3', 'R6')
dot.edge('R1', 'FINAL'); dot.edge('R2', 'FINAL'); dot.edge('R3', 'FINAL')
dot.edge('R4', 'FINAL'); dot.edge('R5', 'FINAL'); dot.edge('R6', 'FINAL')
產生圖檔
dot.render('國際醫療器材來源流向管理流程圖_完整版', cleanup=True)
print("已成功產生「國際醫療器材來源流向管理流程圖_完整版.png」")
若要直接顯示在Jupyter Notebook，可加這行
dot
