import streamlit as st
import yaml
import os
from pathlib import Path
import json
import base64
from datetime import datetime
import time

# ====================== Enhanced Config ======================
st.set_page_config(
    page_title="Agentic 醫療器材來源流向流程圖產生器",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/medical-device-flowchart',
        'Report a bug': "https://github.com/yourusername/medical-device-flowchart/issues",
        'About': "# 醫療器材來源流向 Agentic 流程圖產生器\n專業的AI驅動流程圖生成系統"
    }
)

# ====================== 20 Flower Style Definitions ======================
FLOWER_STYLES = {
    "default": {
        "name_en": "Default",
        "name_zh": "預設",
        "colors": {"primary": "#f9f9f9", "stroke": "#333", "text": "#000"},
        "mermaid": """classDef default fill:#f9f9f9,stroke:#333,stroke-width:2px;
                     linkStyle default stroke:#333,stroke-width:2px;"""
    },
    "sakura": {
        "name_en": "Sakura (Cherry Blossom)",
        "name_zh": "櫻花",
        "colors": {"primary": "#ffebf0", "stroke": "#ff99bb", "text": "#d4386c"},
        "mermaid": """classDef sakura fill:#ffebf0,stroke:#ff99bb,stroke-width:3px,color:#d4386c;
                     linkStyle default stroke:#ff99bb,stroke-width:3px;"""
    },
    "rose": {
        "name_en": "Rose",
        "name_zh": "玫瑰",
        "colors": {"primary": "#fff1f0", "stroke": "#ff1744", "text": "#c62828"},
        "mermaid": """classDef rose fill:#fff1f0,stroke:#ff1744,stroke-width:3px,color:#c62828;
                     linkStyle default stroke:#ff1744,stroke-width:3px;"""
    },
    "lotus": {
        "name_en": "Lotus",
        "name_zh": "蓮花",
        "colors": {"primary": "#f3e5f5", "stroke": "#ab47bc", "text": "#6a1b9a"},
        "mermaid": """classDef lotus fill:#f3e5f5,stroke:#ab47bc,stroke-width:3px,color:#6a1b9a;
                     linkStyle default stroke:#ab47bc,stroke-width:3px;"""
    },
    "sunflower": {
        "name_en": "Sunflower",
        "name_zh": "向日葵",
        "colors": {"primary": "#fff9c4", "stroke": "#ffa000", "text": "#f57c00"},
        "mermaid": """classDef sunflower fill:#fff9c4,stroke:#ffa000,stroke-width:3px,color:#f57c00;
                     linkStyle default stroke:#ffa000,stroke-width:3px;"""
    },
    "lavender": {
        "name_en": "Lavender",
        "name_zh": "薰衣草",
        "colors": {"primary": "#ede7f6", "stroke": "#7e57c2", "text": "#512da8"},
        "mermaid": """classDef lavender fill:#ede7f6,stroke:#7e57c2,stroke-width:3px,color:#512da8;
                     linkStyle default stroke:#7e57c2,stroke-width:3px;"""
    },
    "hibiscus": {
        "name_en": "Hibiscus",
        "name_zh": "扶桑花",
        "colors": {"primary": "#fce4ec", "stroke": "#ec407a", "text": "#c2185b"},
        "mermaid": """classDef hibiscus fill:#fce4ec,stroke:#ec407a,stroke-width:3px,color:#c2185b;
                     linkStyle default stroke:#ec407a,stroke-width:3px;"""
    },
    "cherry_blossom": {
        "name_en": "Cherry Blossom",
        "name_zh": "櫻花粉",
        "colors": {"primary": "#ffeef8", "stroke": "#ff80ab", "text": "#f50057"},
        "mermaid": """classDef cherry fill:#ffeef8,stroke:#ff80ab,stroke-width:3px,color:#f50057;
                     linkStyle default stroke:#ff80ab,stroke-width:3px;"""
    },
    "peony": {
        "name_en": "Peony",
        "name_zh": "牡丹",
        "colors": {"primary": "#fde9f3", "stroke": "#d81b60", "text": "#ad1457"},
        "mermaid": """classDef peony fill:#fde9f3,stroke:#d81b60,stroke-width:3px,color:#ad1457;
                     linkStyle default stroke:#d81b60,stroke-width:3px;"""
    },
    "orchid": {
        "name_en": "Orchid",
        "name_zh": "蘭花",
        "colors": {"primary": "#f3e5f5", "stroke": "#ba68c8", "text": "#8e24aa"},
        "mermaid": """classDef orchid fill:#f3e5f5,stroke:#ba68c8,stroke-width:3px,color:#8e24aa;
                     linkStyle default stroke:#ba68c8,stroke-width:3px;"""
    },
    "lily": {
        "name_en": "Lily",
        "name_zh": "百合",
        "colors": {"primary": "#ffffff", "stroke": "#ff6f00", "text": "#e65100"},
        "mermaid": """classDef lily fill:#ffffff,stroke:#ff6f00,stroke-width:3px,color:#e65100;
                     linkStyle default stroke:#ff6f00,stroke-width:3px;"""
    },
    "tulip": {
        "name_en": "Tulip",
        "name_zh": "鬱金香",
        "colors": {"primary": "#ffebee", "stroke": "#ef5350", "text": "#d32f2f"},
        "mermaid": """classDef tulip fill:#ffebee,stroke:#ef5350,stroke-width:3px,color:#d32f2f;
                     linkStyle default stroke:#ef5350,stroke-width:3px;"""
    },
    "daffodil": {
        "name_en": "Daffodil",
        "name_zh": "水仙",
        "colors": {"primary": "#fffde7", "stroke": "#fdd835", "text": "#f9a825"},
        "mermaid": """classDef daffodil fill:#fffde7,stroke:#fdd835,stroke-width:3px,color:#f9a825;
                     linkStyle default stroke:#fdd835,stroke-width:3px;"""
    },
    "magnolia": {
        "name_en": "Magnolia",
        "name_zh": "木蘭",
        "colors": {"primary": "#fafafa", "stroke": "#8d6e63", "text": "#5d4037"},
        "mermaid": """classDef magnolia fill:#fafafa,stroke:#8d6e63,stroke-width:3px,color:#5d4037;
                     linkStyle default stroke:#8d6e63,stroke-width:3px;"""
    },
    "camellia": {
        "name_en": "Camellia",
        "name_zh": "山茶花",
        "colors": {"primary": "#ffebee", "stroke": "#e91e63", "text": "#c2185b"},
        "mermaid": """classDef camellia fill:#ffebee,stroke:#e91e63,stroke-width:3px,color:#c2185b;
                     linkStyle default stroke:#e91e63,stroke-width:3px;"""
    },
    "hydrangea": {
        "name_en": "Hydrangea",
        "name_zh": "繡球花",
        "colors": {"primary": "#e3f2fd", "stroke": "#42a5f5", "text": "#1976d2"},
        "mermaid": """classDef hydrangea fill:#e3f2fd,stroke:#42a5f5,stroke-width:3px,color:#1976d2;
                     linkStyle default stroke:#42a5f5,stroke-width:3px;"""
    },
    "wisteria": {
        "name_en": "Wisteria",
        "name_zh": "紫藤",
        "colors": {"primary": "#f3e5f5", "stroke": "#9c27b0", "text": "#7b1fa2"},
        "mermaid": """classDef wisteria fill:#f3e5f5,stroke:#9c27b0,stroke-width:3px,color:#7b1fa2;
                     linkStyle default stroke:#9c27b0,stroke-width:3px;"""
    },
    "poppy": {
        "name_en": "Poppy",
        "name_zh": "罌粟花",
        "colors": {"primary": "#ffebee", "stroke": "#f44336", "text": "#c62828"},
        "mermaid": """classDef poppy fill:#ffebee,stroke:#f44336,stroke-width:3px,color:#c62828;
                     linkStyle default stroke:#f44336,stroke-width:3px;"""
    },
    "daisy": {
        "name_en": "Daisy",
        "name_zh": "雛菊",
        "colors": {"primary": "#fffde7", "stroke": "#ffeb3b", "text": "#f57f17"},
        "mermaid": """classDef daisy fill:#fffde7,stroke:#ffeb3b,stroke-width:3px,color:#f57f17;
                     linkStyle default stroke:#ffeb3b,stroke-width:3px;"""
    },
    "jasmine": {
        "name_en": "Jasmine",
        "name_zh": "茉莉花",
        "colors": {"primary": "#f1f8e9", "stroke": "#9ccc65", "text": "#558b2f"},
        "mermaid": """classDef jasmine fill:#f1f8e9,stroke:#9ccc65,stroke-width:3px,color:#558b2f;
                     linkStyle default stroke:#9ccc65,stroke-width:3px;"""
    }
}

# ====================== Translations ======================
TRANSLATIONS = {
    "English": {
        "title": "🌸 Agentic Medical Device Traceability Flowchart Generator",
        "dashboard": "Dashboard",
        "upload": "📤 Upload Document",
        "preview": "📄 Document Preview",
        "gen_flow": "✨ Generate Flowchart",
        "edit_flow": "✏️ Edit Flowchart (Mermaid Syntax)",
        "styles": "🎨 Flowchart Style (Flower Theme)",
        "agents": "🤖 Select Analysis Agents",
        "prompt": "💬 Custom Prompt",
        "max_tokens": "🔢 Max Tokens",
        "model": "🧠 Model",
        "gen": "🚀 Generate with Agents",
        "api_key": "🔑 API Key Required",
        "status": "Status",
        "total_agents": "Total Agents",
        "active_agents": "Active Agents",
        "flowcharts_generated": "Flowcharts Generated",
        "tokens_used": "Tokens Used",
        "theme": "Theme",
        "language": "Language",
        "light": "Light",
        "dark": "Dark",
        "select_style": "Select a flower style",
        "processing": "Processing...",
        "success": "Success!",
        "error": "Error",
        "sample_text": "Load Sample Text",
        "export": "Export",
        "download_svg": "Download SVG",
        "download_png": "Download PNG",
        "copy_code": "Copy Code",
        "questions": "20 Follow-up Questions",
        "recent_activity": "Recent Activity",
        "performance": "Performance Metrics",
    },
    "繁體中文": {
        "title": "🌸 醫療器材來源流向 Agentic 流程圖產生器",
        "dashboard": "儀表板",
        "upload": "📤 上傳文件",
        "preview": "📄 文件預覽",
        "gen_flow": "✨ 產生流程圖",
        "edit_flow": "✏️ 編輯流程圖（Mermaid 語法）",
        "styles": "🎨 流程圖風格（花卉主題）",
        "agents": "🤖 選擇分析 Agents",
        "prompt": "💬 自訂提示詞",
        "max_tokens": "🔢 最大 Tokens",
        "model": "🧠 模型",
        "gen": "🚀 使用 Agents 產生",
        "api_key": "🔑 請輸入 API Key",
        "status": "狀態",
        "total_agents": "總 Agents 數",
        "active_agents": "啟用 Agents",
        "flowcharts_generated": "已產生流程圖",
        "tokens_used": "已使用 Tokens",
        "theme": "主題",
        "language": "語言",
        "light": "淺色",
        "dark": "深色",
        "select_style": "選擇花卉風格",
        "processing": "處理中...",
        "success": "成功！",
        "error": "錯誤",
        "sample_text": "載入範例文字",
        "export": "匯出",
        "download_svg": "下載 SVG",
        "download_png": "下載 PNG",
        "copy_code": "複製程式碼",
        "questions": "20 個延伸問題",
        "recent_activity": "最近活動",
        "performance": "效能指標",
    }
}

# ====================== Initialize Session State ======================
if 'theme' not in st.session_state:
    st.session_state.theme = 'Light'
if 'lang' not in st.session_state:
    st.session_state.lang = '繁體中文'
if 'mermaid' not in st.session_state:
    st.session_state.mermaid = ""
if 'flowcharts_count' not in st.session_state:
    st.session_state.flowcharts_count = 0
if 'tokens_used' not in st.session_state:
    st.session_state.tokens_used = 0
if 'activity_log' not in st.session_state:
    st.session_state.activity_log = []
if 'selected_style' not in st.session_state:
    st.session_state.selected_style = 'sakura'

# ====================== Sidebar Configuration ======================
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/ffebf0/d4386c?text=Medical+Device", use_column_width=True)
    
    st.markdown("---")
    
    # Theme & Language Selection
    col1, col2 = st.columns(2)
    with col1:
        theme_label = TRANSLATIONS[st.session_state.lang]["theme"]
        new_theme = st.selectbox(
            theme_label,
            ["Light", "Dark"],
            index=0 if st.session_state.theme == "Light" else 1,
            key="theme_selector"
        )
        if new_theme != st.session_state.theme:
            st.session_state.theme = new_theme
            st.rerun()
    
    with col2:
        lang_label = TRANSLATIONS[st.session_state.lang]["language"]
        new_lang = st.selectbox(
            lang_label,
            ["English", "繁體中文"],
            index=1 if st.session_state.lang == "繁體中文" else 0,
            key="lang_selector"
        )
        if new_lang != st.session_state.lang:
            st.session_state.lang = new_lang
            st.rerun()
    
    _ = TRANSLATIONS[st.session_state.lang]
    
    st.markdown("---")
    
    # Status Indicators
    st.markdown(f"### 📊 {_['status']}")
    
    # Metrics
    metric_col1, metric_col2 = st.columns(2)
    with metric_col1:
        st.metric(_["flowcharts_generated"], st.session_state.flowcharts_count, delta="+1" if st.session_state.flowcharts_count > 0 else None)
    with metric_col2:
        st.metric(_["tokens_used"], f"{st.session_state.tokens_used:,}", delta="+500" if st.session_state.tokens_used > 0 else None)
    
    # Progress indicators
    if 'processing' in st.session_state and st.session_state.processing:
        st.progress(st.session_state.get('progress', 0))
    
    st.markdown("---")
    
    # API Key Management
    st.markdown("### 🔐 API Keys")
    providers = ["openai", "anthropic", "gemini", "xai"]
    for provider in providers:
        with st.expander(f"{provider.upper()} API Key"):
            key = st.text_input(f"{provider.upper()} Key", type="password", key=f"input_{provider}")
            if st.button("💾 Save", key=f"save_{provider}"):
                st.session_state[provider + "_key"] = key
                st.success("✅ Saved!")

# ====================== Load Agents ======================
@st.cache_data
def load_agents():
    if Path("agents.yaml").exists():
        with open("agents.yaml", encoding="utf-8") as f:
            return yaml.safe_load(f)["agents"]
    return []

agents = load_agents()

# ====================== Helper Functions ======================
def get_api_key(provider: str):
    env_key = os.getenv(provider.upper() + "_API_KEY")
    if env_key:
        return env_key
    return st.session_state.get(provider + "_key")

def log_activity(message: str, status: str = "info"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.activity_log.insert(0, {
        "time": timestamp,
        "message": message,
        "status": status
    })
    if len(st.session_state.activity_log) > 10:
        st.session_state.activity_log.pop()

def apply_theme():
    if st.session_state.theme == "Dark":
        return """
        <style>
        .stApp {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        .stMetric {
            background-color: #2d2d2d;
            padding: 10px;
            border-radius: 10px;
        }
        </style>
        """
    else:
        return """
        <style>
        .stApp {
            background-color: #ffffff;
            color: #000000;
        }
        .stMetric {
            background-color: #f9f9f9;
            padding: 10px;
            border-radius: 10px;
        }
        </style>
        """

st.markdown(apply_theme(), unsafe_allow_html=True)

# ====================== WOW Dashboard ======================
_ = TRANSLATIONS[st.session_state.lang]

# Custom CSS for beautiful cards
st.markdown("""
<style>
.dashboard-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 15px;
    color: white;
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    margin: 10px 0;
}
.flower-card {
    border: 2px solid #ff99bb;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    background: linear-gradient(135deg, #fff 0%, #ffebf0 100%);
    transition: transform 0.3s ease;
    cursor: pointer;
}
.flower-card:hover {
    transform: scale(1.05);
    box-shadow: 0 5px 15px rgba(255, 153, 187, 0.3);
}
.activity-item {
    padding: 10px;
    margin: 5px 0;
    border-left: 4px solid #667eea;
    background: #f8f9fa;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)

# Main Title with Animation
st.markdown(f"# {_['title']}")

# Dashboard Section
with st.expander("📊 " + _["dashboard"], expanded=True):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="dashboard-card">
            <h3>🤖 {_["total_agents"]}</h3>
            <h1>{len(agents)}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        active = sum(1 for agent in agents if agent.get("enabled", True))
        st.markdown(f"""
        <div class="dashboard-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <h3>✅ {_["active_agents"]}</h3>
            <h1>{active}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="dashboard-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <h3>📊 {_["flowcharts_generated"]}</h3>
            <h1>{st.session_state.flowcharts_count}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="dashboard-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <h3>🔢 {_["tokens_used"]}</h3>
            <h1>{st.session_state.tokens_used:,}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent Activity
    st.markdown(f"### 📝 {_['recent_activity']}")
    if st.session_state.activity_log:
        for activity in st.session_state.activity_log[:5]:
            status_emoji = "✅" if activity["status"] == "success" else "❌" if activity["status"] == "error" else "ℹ️"
            st.markdown(f"""
            <div class="activity-item">
                {status_emoji} <strong>{activity["time"]}</strong> - {activity["message"]}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No recent activity")

st.markdown("---")

# ====================== Flower Style Selector ======================
st.markdown(f"## 🌸 {_['styles']}")

# Display flower styles in a beautiful grid
cols = st.columns(5)
for idx, (key, style) in enumerate(FLOWER_STYLES.items()):
    with cols[idx % 5]:
        style_name = style["name_zh"] if st.session_state.lang == "繁體中文" else style["name_en"]
        color = style["colors"]["primary"]
        stroke = style["colors"]["stroke"]
        
        if st.button(
            f"🌺 {style_name}",
            key=f"style_{key}",
            use_container_width=True,
            type="primary" if st.session_state.selected_style == key else "secondary"
        ):
            st.session_state.selected_style = key
            log_activity(f"Changed style to {style_name}", "success")
            st.rerun()

st.markdown("---")

# ====================== File Upload Section ======================
st.markdown(f"## {_['upload']}")

col_upload, col_sample = st.columns([3, 1])

with col_upload:
    uploaded = st.file_uploader(
        _["upload"],
        type=["txt", "md", "csv", "json", "yaml"],
        help="Upload your document to analyze"
    )

with col_sample:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(_["sample_text"], type="secondary", use_container_width=True):
        sample = """國際醫療器材來源流向管理現況研究：
(1) 蒐集美國、歐盟、澳洲、中國大陸、韓國、新加坡及國際醫療器材法規調合組織醫療器材來源流向暨單一識別之法規、執行情形及相關應用。
(2) 分析比較各國管理法規異同。
(3) 完成各國法規/指引摘要及我國相關指引參採建議。"""
        st.session_state.sample_text = sample
        log_activity("Loaded sample text", "success")
        st.rerun()

doc_text = ""
if uploaded:
    try:
        if uploaded.type == "text/csv":
            doc_text = uploaded.getvalue().decode("utf-8")
        else:
            doc_text = uploaded.read().decode("utf-8")
        log_activity(f"Uploaded file: {uploaded.name}", "success")
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        log_activity(f"Error uploading file: {str(e)}", "error")
elif 'sample_text' in st.session_state:
    doc_text = st.session_state.sample_text

# Document Preview
if doc_text:
    with st.expander(f"📄 {_['preview']}", expanded=False):
        st.markdown(f"```markdown\n{doc_text[:1000]}{'...' if len(doc_text) > 1000 else ''}\n```")
        st.caption(f"Document length: {len(doc_text)} characters")

# ====================== Flowchart Generation ======================
if doc_text:
    st.markdown("---")
    st.markdown(f"## {_['gen_flow']}")
    
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        if st.button(_["gen_flow"], type="primary", use_container_width=True):
            with st.spinner(_["processing"]):
                # Simulate processing
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                # Get selected style
                selected_style_obj = FLOWER_STYLES[st.session_state.selected_style]
                style_class = st.session_state.selected_style
                
                # Generate flowchart
                mermaid_code = f"""flowchart TD
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
    
    {selected_style_obj['mermaid']}
    class A,B,C {style_class}
"""
                st.session_state.mermaid = mermaid_code
                st.session_state.flowcharts_count += 1
                st.session_state.tokens_used += 1500
                log_activity("Generated flowchart successfully", "success")
                st.success(_["success"])
                st.rerun()
    
    with col_right:
        # Style preview
        selected_style_obj = FLOWER_STYLES[st.session_state.selected_style]
        style_name = selected_style_obj["name_zh"] if st.session_state.lang == "繁體中文" else selected_style_obj["name_en"]
        st.markdown(f"""
        <div class="flower-card">
            <h4>🎨 Current Style: {style_name}</h4>
            <div style="background: {selected_style_obj['colors']['primary']}; 
                        border: 3px solid {selected_style_obj['colors']['stroke']}; 
                        padding: 20px; 
                        border-radius: 10px;
                        color: {selected_style_obj['colors']['text']};">
                <strong>Sample Preview</strong><br>
                Primary: {selected_style_obj['colors']['primary']}<br>
                Stroke: {selected_style_obj['colors']['stroke']}<br>
                Text: {selected_style_obj['colors']['text']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ====================== Flowchart Display & Edit ======================
if "mermaid" in st.session_state and st.session_state.mermaid:
    st.markdown("---")
    st.markdown(f"## {_['edit_flow']}")
    
    tab1, tab2, tab3 = st.tabs(["👁️ Preview", "✏️ Edit Code", "📥 Export"])
    
    with tab1:
        # Mermaid Preview
        theme_param = "default" if st.session_state.theme == "Light" else "dark"
        bg_color = "white" if st.session_state.theme == "Light" else "#1e1e1e"
        
        mermaid_html = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background: {bg_color};
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 500px;
        }}
        .mermaid {{
            background: {bg_color};
            padding: 20px;
            border-radius: 10px;
        }}
    </style>
</head>
<body>
    <div class="mermaid">
{st.session_state.mermaid}
    </div>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: '{theme_param}',
            flowchart: {{
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'basis'
            }}
        }});
    </script>
</body>
</html>
        """
        st.components.v1.html(mermaid_html, height=600, scrolling=True)
    
    with tab2:
        # Code Editor
        edited = st.text_area(
            _["edit_flow"],
            st.session_state.mermaid,
            height=400,
            help="Edit the Mermaid code directly"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Changes", use_container_width=True):
                st.session_state.mermaid = edited
                log_activity("Updated flowchart code", "success")
                st.success(_["success"])
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset to Original", use_container_width=True):
                log_activity("Reset flowchart to original", "info")
                st.rerun()
    
    with tab3:
        # Export Options
        st.markdown("### Export Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Copy Mermaid Code", use_container_width=True):
                st.code(st.session_state.mermaid, language="mermaid")
                st.success("Code displayed above - copy manually")
        
        with col2:
            # Download as text file
            st.download_button(
                label="💾 Download .mmd",
                data=st.session_state.mermaid,
                file_name="flowchart.mmd",
                mime="text/plain",
                use_container_width=True
            )
        
        with col3:
            st.info("💡 Use mermaid.live to export as SVG/PNG")

# ====================== Agent Section ======================
if doc_text:
    st.markdown("---")
    st.markdown(f"## {_['agents']}")
    
    with st.expander("🤖 Configure AI Agents", expanded=False):
        selected_agents = st.multiselect(
            _["agents"],
            options=agents,
            format_func=lambda x: f"{x['name']} ({x['model']}) - {x['description']}"
        )
        
        custom_prompt = st.text_area(
            _["prompt"],
            value="請根據以上文件，產生更詳細、專業的醫療器材來源流向管理流程圖（使用Mermaid語法），並用繁體中文標註。",
            height=150
        )
        
        max_tokens = st.slider(_["max_tokens"], 500, 8000, 4000)
        
        if st.button(_["gen"], type="primary", use_container_width=True):
            if not selected_agents:
                st.error("❌ Please select at least one agent")
            else:
                full_prompt = f"文件內容如下：\n\"\"\"\n{doc_text}\n\"\"\"\n\n{custom_prompt}"
                
                for agent in selected_agents:
                    with st.status(f"Processing with {agent['name']}...", expanded=True) as status:
                        st.write(f"Model: {agent['model']}")
                        st.write(f"Provider: {agent['provider']}")
                        
                        try:
                            # Add your API calling logic here
                            # This is a placeholder
                            time.sleep(2)
                            
                            status.update(label=f"✅ Completed: {agent['name']}", state="complete")
                            log_activity(f"Agent {agent['name']} completed successfully", "success")
                            st.session_state.tokens_used += max_tokens
                            
                        except Exception as e:
                            status.update(label=f"❌ Error: {agent['name']}", state="error")
                            st.error(f"Error with {agent['name']}: {str(e)}")
                            log_activity(f"Agent {agent['name']} failed: {str(e)}", "error")

# ====================== 20 Follow-up Questions ======================
st.markdown("---")
st.markdown(f"## 💡 {_['questions']}")

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

# Display questions in a nice format
cols = st.columns(2)
for idx, q in enumerate(questions):
    with cols[idx % 2]:
        with st.expander(f"❓ Question {idx + 1}"):
            st.write(q)
            if st.button(f"Ask this question", key=f"q_{idx}"):
                st.session_state.custom_question = q
                log_activity(f"Selected question {idx + 1}", "info")
                st.info("Question added to prompt (implement agent call here)")

# ====================== Footer ======================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 20px;">
    <p>🌸 Medical Device Traceability Flowchart Generator v2.0</p>
    <p>Made with ❤️ using Streamlit | © 2024</p>
</div>
""", unsafe_allow_html=True)
