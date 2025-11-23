import streamlit as st
import yaml
import os
from pathlib import Path
import json
import base64

# ====================== Config ======================
st.set_page_config(page_title="Agentic 醫療器材來源流向流程圖產生器", layout="wide")

# Theme & Language
theme = st.sidebar.selectbox("主題", ["Light", "Dark"], index=0)
lang = st.sidebar.selectbox("語言", ["English", "繁體中文"], index=1)

translations = {
    "English": {
        "title": "Agentic Medical Device Traceability Flowchart Generator",
        "upload": "Upload Document",
        "preview": "Document Preview",
        "gen_flow": "Generate Flowchart",
        "edit_flow": "Edit Flowchart (Mermaid)",
        "styles": "Flowchart Style (Flower Theme)",
        "agents": "Select Agents to Analyze",
        "prompt": "Custom Prompt",
        "max_tokens": "Max Tokens",
        "model": "Model",
        "gen": "Generate with Agents",
        "api_key": "API Key required",
    },
    "繁體中文": {
        "title": "醫療器材來源流向 Agentic 流程圖產生器",
        "upload": "上傳文件",
        "preview": "文件預覽",
        "gen_flow": "產生流程圖",
        "edit_flow": "編輯流程圖 (Mermaid 語法)",
        "styles": "流程圖風格（花卉主題）",
        "agents": "選擇參與分析的 Agents",
        "prompt": "自訂 Prompt",
        "max_tokens": "最大 Tokens",
        "model": "模型",
        "gen": "使用 Agents 產生",
        "api_key": "請輸入 API Key",
    }
}
_ = translations["繁體中文" if lang == "繁體中文" else "English"]

# 20 Flower-themed Mermaid styles
flower_styles = [
    "default", "sakura", "rose", "lotus", "sunflower", "lavender", "hibiscus", "cherry-blossom",
    "peony", "orchid", "lily", "tulip", "daffodil", "magnolia", "camellia", "hydrangea",
    "wisteria", "poppy", "daisy", "jasmine"
]

style_themes = {
    "default": """classDef default fill:#f9f9f9,stroke:#333,stroke-width:2px;
                 linkStyle default stroke:#333,stroke-width:2px;""",
    "sakura": """classDef sakura fill:#ffebf0,stroke:#ff99bb,stroke-width:3px,color:#d4386c;
                 linkStyle default stroke:#ff99bb,stroke-width:3px;""",
    "rose": """classDef rose fill:#fff1f0,stroke:#ff1744,stroke-width:3px;
               linkStyle default stroke:#ff1744,stroke-width:3px;""",
    # ... (you can expand the rest, or I can generate all 20)
}

# Load agents.yaml
@st.cache_data
def load_agents():
    if Path("agents.yaml").exists():
        with open("agents.yaml", encoding="utf-8") as f:
            return yaml.safe_load(f)["agents"]
    return []

agents = load_agents()

# ====================== API Key Handling ======================
def get_api_key(provider: str):
    env_key = os.getenv(provider.upper() + "_API_KEY")
    if env_key:
        return env_key
    session_key = st.session_state.get(provider + "_key")
    if session_key:
        return session_key
    
    with st.sidebar.expander(f"{provider.upper()} API Key"):
        key = st.text_input(f"{provider.upper()} API Key", type="password", key=f"input_{provider}")
        if st.button("Save", key=f"save_{provider}"):
            st.session_state[provider + "_key"] = key
            st.success("Saved!")
        return key if key else None
    return None

# ====================== Main App ======================
st.title(_.get("title", "Agentic Flowchart System"))

# File upload
uploaded = st.file_uploader(_.get("upload"), type=["txt", "md", "csv", "json", "yaml"])

doc_text = ""
if uploaded:
    if uploaded.type == "text/csv":
        doc_text = uploaded.getvalue().decode("utf-8")
    else:
        doc_text = uploaded.read().decode("utf-8")
    
    st.subheader(_.get("preview"))
    st.markdown(f"```markdown\n{doc_text}\n```")

if doc_text:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button(_.get("gen_flow"), type="primary"):
            with st.spinner("產生流程圖中..."):
                # Simple built-in flowchart from sample
                mermaid_code = f"""
flowchart TD
    subgraph 國際法規蒐集
        A[蒐集美國、歐盟、澳洲<br/>中國大陸、韓國、新加坡<br/>及IMDRF法規]
    end
    subgraph 分析比較
        B[分析各國管理法規異同]
    end
    subgraph 產出報告
        C[完成各國法規摘要<br/>及我國參採建議]
    end
    A --> B --> C
    click A href "#" "詳細法規"
    click C href "#" "參採建議"
    
    {style_themes.get("sakura", style_themes["default"])}
    class A,B,C sakura
"""
                st.session_state.mermaid = mermaid_code

    with col2:
        selected_style = st.selectbox(_.get("styles"), flower_styles, index=1)
        if "mermaid" in st.session_state:
            edited = st.text_area(_.get("edit_flow"), st.session_state.mermaid, height=400)
            st.session_state.mermaid = edited

            theme_param = "theme=base" if theme == "Light" else "theme=dark"
            mermaid_html = f"""
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<div class="mermaid" style="background:{"white" if theme=="Light" else "#1e1e1e"};padding:20px;border-radius:10px;">
{edited}
</div>
<script>mermaid.initialize({{startOnLoad:true, {theme_param},
    flowchart: {{ useMaxWidth: true, htmlLabels: true }}
}});</script>
            """
            st.components.v1.html(mermaid_html, height=600, scrolling=True)

    # ====================== Agent Execution ======================
    st.divider()
    st.subheader(_.get("agents"))

    selected_agents = st.multiselect(
        _.get("agents"),
        options=agents,
        format_func=lambda x: f"{x['name']} ({x['model']}) - {x['description']}"
    )

    custom_prompt = st.text_area(_.get("prompt"), value="請根據以上文件，產生更詳細、專業的醫療器材來源流向管理流程圖（使用Mermaid語法），並用繁體中文標註。", height=150)
    max_tokens = st.slider(_.get("max_tokens"), 500, 8000, 4000)
    
    if st.button(_.get("gen"), type="primary"):
        if not selected_agents:
            st.error("請至少選擇一個 Agent")
        else:
            full_prompt = f"文件內容如下：\n\"\"\"\n{doc_text}\n\"\"\"\n\n{custom_prompt}"
            results = []
            for agent in selected_agents:
                with st.status(f"正在呼叫 {agent['name']}..."):
                    st.write(f"模型：{agent['model']}")
                    try:
                        if agent["provider"] == "openai":
                            from openai import OpenAI
                            client = OpenAI(api_key=get_api_key("openai"))
                            resp = client.chat.completions.create(
                                model=agent["model"],
                                messages=[{"role": "system", "content": agent.get("system_prompt", "")},
                                          {"role": "user", "content": full_prompt}],
                                max_tokens=max_tokens
                            )
                            content = resp.choices[0].message.content
                            
                        elif agent["provider"] == "anthropic":
                            import anthropic
                            client = anthropic.Anthropic(api_key=get_api_key("anthropic"))
                            resp = client.messages.create(
                                model=agent["model"],
                                system=agent.get("system_prompt", ""),
                                messages=[{"role": "user", "content": full_prompt}],
                                max_tokens=max_tokens
                            )
                            content = resp.content[0].text
                            
                        elif agent["provider"] == "gemini":
                            import google.generativeai as genai
                            genai.configure(api_key=get_api_key("gemini"))
                            model = genai.GenerativeModel(agent["model"])
                            response = model.generate_content(full_prompt)
                            content = response.text
                            
                        elif agent["provider"] == "xai":
                            from openai import OpenAI
                            client = OpenAI(
                                api_key=get_api_key("xai"),
                                base_url="https://api.x.ai/v1"
                            )
                            resp = client.chat.completions.create(
                                model=agent["model"],
                                messages=[{"role": "user", "content": full_prompt}],
                                max_tokens=max_tokens
                            )
                            content = resp.choices[0].message.content
                            
                        st.success("完成")
                        st.markdown(content)
                        if "```mermaid" in content:
                            code = content.split("```mermaid")[1].split("```")[0].strip()
                            st.session_state.mermaid = code
                            st.rerun()
                            
                    except Exception as e:
                        st.error(f"{agent['name']} 錯誤：{str(e)}")

# ====================== Sample Text Button ======================
if st.button("載入範例文字（國際醫療器材來源流向管理現況研究）"):
    sample = """國際醫療器材來源流向管理現況研究：
(1)   蒐集美國、歐盟、澳洲、中國大陸、韓國、新加坡及國際醫療器材法規調合組織醫療器材來源流向暨單一識別之法規、執行情形及相關應用。
(2)   分析比較各國管理法規異同。
(3)   完成各國法規/指引摘要及我國相關指引參採建議。"""
    doc_text = sample
    st.session_state.sample_loaded = True
    st.rerun()

# ====================== 20 Follow-up Questions ======================
st.divider()
st.subheader("20 個後續可延伸問題（供使用者進一步提問）")
questions = [
    "1. 美國FDA的UDI系統與歐盟EUDAMED在資料流向上的最大差異是什麼？",
    "2. IMDRF的UDI指引對亞洲國家有約束力嗎？實際採用率如何？",
    "3. 台灣目前醫療器材來源流向管理規範與國際差距在哪？",
    "4. 韓國MFDS的UDI實施進度與強制時程為何？",
    "5. 新加坡HSA的GUDID資料提交要求與美國有何不同？",
    "6. 中國NMPA的UDI第二階段（2024-2026）涵蓋哪些風險等級器材？",
    "7. 澳洲TGA是否要求本地代理商負責UDI資料上傳？",
    "8. 目前各國UDI資料庫是否已相互串聯或有互通計畫？",
    "9. 台灣若要導入UDI，建議先從Class幾開始？",
    "10. 各國對植入式醫療器材的來源流向追蹤有何特殊要求？",
    "11. 歐盟MDR Annex VI的UDI-DI與PI結構與美國有何差異？",
    "12. 日本PMDA的UDI規範與IMDRF一致性程度？",
    "13. 目前國際上是否有成功的UDI區塊鏈應用案例？",
    "14. 台灣醫療器材商業同業公會對UDI的立場為何？",
    "15. 各國UDI資料庫的公開程度比較（公開/部分公開/不公開）？",
    "16. 未來GS1與HIBC兩大標準是否會統一？",
    "17. 低風險醫療器材（Class I）是否也有UDI強制要求？各國差異？",
    "18. UDI系統對醫療器材召回效率的實證提升數據？",
    "19. 台灣衛福部食藥署目前UDI試辦計畫進度如何？",
    "20. 若要向立法院提案修法導入UDI，建議優先參採哪一國模式？"
]
for q in questions:
    st.write(q)
