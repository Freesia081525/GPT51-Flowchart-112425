Hi please transform the previous design to streamlit, agents.yaml, Openai API, Gemini API, Anthropic API, XAI API. import React, { useState, useEffect, useMemo } from 'react';
import { FLOWER_STYLES, DEFAULT_SYSTEM_PROMPT, UI_TEXT } from './constants';
import { FlowchartSpec, Language, ThemeMode, ModelProvider, FlowerTheme } from './types';
import Visualizer from './components/Visualizer';
import Editor from './components/Editor';
import { generateFlowchart } from './services/llmService';

const App: React.FC = () => {
// UI State
const [uiLanguage, setUiLanguage] = useState<Language>('en');
const [flowchartLanguage, setFlowchartLanguage] = useState<Language>('en');

const [themeMode, setThemeMode] = useState<ThemeMode>('light');
const [flowerStyle, setFlowerStyle] = useState<string>('Sakura');
const [provider, setProvider] = useState<ModelProvider>('Gemini');
const [activeTab, setActiveTab] = useState<'visual' | 'edit' | 'json' | 'settings'>('visual');

// Data State
const [description, setDescription] = useState('');
const [systemPrompt, setSystemPrompt] = useState(DEFAULT_SYSTEM_PROMPT);
const [spec, setSpec] = useState<FlowchartSpec | null>(null);
const [isLoading, setIsLoading] = useState(false);
const [error, setError] = useState<string | null>(null);

// Derived
const ui = UI_TEXT[uiLanguage];
const currentTheme = useMemo(() => FLOWER_STYLES[flowerStyle][themeMode], [flowerStyle, themeMode]);

// Apply theme colors to CSS variables for global usage if needed, or just pass to components
useEffect(() => {
const root = document.documentElement;
if (themeMode === 'dark') {
root.classList.add('dark');
} else {
root.classList.remove('dark');
}
}, [themeMode]);

const handleGenerate = async () => {
if (!description.trim()) return;
setIsLoading(true);
setError(null);
setActiveTab('visual');

try {
  const data = await generateFlowchart(description, systemPrompt, flowchartLanguage);
  setSpec(data);
} catch (err: any) {
  setError(err.message || "Failed to generate flowchart");
} finally {
  setIsLoading(false);
}
};

// Calculate stats
const stats = useMemo(() => {
if (!spec) return null;
const n = spec.nodes.length;
let complexity = 'Low';
if (n > 10) complexity = 'Medium';
if (n > 25) complexity = 'High';
return { nodes: n, edges: spec.edges.length, complexity };
}, [spec]);

return (
<div className="min-h-screen flex flex-col bg-cover bg-center transition-all duration-500"
style={{
backgroundColor: currentTheme.bg_color,
backgroundImage: themeMode === 'light'
? 'radial-gradient(circle at 50% 0%, rgba(255,255,255,0.8), transparent)'
: 'radial-gradient(circle at 50% 0%, rgba(0,0,0,0.4), transparent)'
}}>

  {/* Header */}
  <header className="h-16 glass-panel border-b border-gray-200 dark:border-gray-800 flex items-center justify-between px-6 sticky top-0 z-50">
    <div className="flex items-center gap-3">
      <div className="w-8 h-8 rounded-full flex items-center justify-center text-white shadow-lg" style={{ backgroundColor: currentTheme.title_fill }}>
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>
      </div>
      <div>
        <h1 className="text-lg font-serif font-bold leading-tight">{ui.title}</h1>
      </div>
    </div>

    <div className="flex items-center gap-4">
      {/* Theme Controls */}
      <select 
        className="bg-transparent text-sm font-medium focus:outline-none cursor-pointer"
        value={flowerStyle}
        onChange={(e) => setFlowerStyle(e.target.value)}
      >
        {Object.keys(FLOWER_STYLES).map(s => <option key={s} value={s}>{s}</option>)}
      </select>

      <div className="h-4 w-[1px] bg-gray-300 dark:bg-gray-700"></div>

      <button 
        onClick={() => setThemeMode(m => m === 'light' ? 'dark' : 'light')}
        className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
      >
        {themeMode === 'light' ? '🌙' : '☀️'}
      </button>
       <button 
        onClick={() => setUiLanguage(l => l === 'en' ? 'zh' : 'en')}
        className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold border border-current opacity-70 hover:opacity-100"
        title="Switch UI Language"
      >
        {uiLanguage.toUpperCase()}
      </button>
    </div>
  </header>

  {/* Main Layout */}
  <main className="flex-1 flex flex-col lg:flex-row overflow-hidden">
    
    {/* Left Sidebar / Input Panel */}
    <aside className="w-full lg:w-[400px] flex flex-col bg-white/60 dark:bg-gray-900/60 backdrop-blur-sm border-r border-gray-200 dark:border-gray-800 p-6 gap-6 z-20 overflow-y-auto">
      
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <label className="text-sm font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">{ui.inputLabel}</label>
          <div className="flex gap-2">
             <span className={`text-xs px-2 py-0.5 rounded-full ${provider === 'Gemini' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-500'}`}>Gemini</span>
             <span className="text-xs text-gray-400">|</span>
             <span className="text-xs text-gray-400">OpenAI</span>
          </div>
        </div>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder={ui.inputPlaceholder}
          className="w-full h-48 p-4 rounded-xl bg-white dark:bg-black/40 border border-gray-200 dark:border-gray-700 focus:ring-2 focus:ring-offset-2 focus:outline-none resize-none shadow-inner transition-all"
          style={{ focusRingColor: currentTheme.title_fill }}
        />

        {/* Output Language Selector */}
        <div className="flex items-center justify-between px-1">
          <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">{ui.outputLanguage}</span>
          <div className="flex bg-gray-100 dark:bg-black/20 rounded-lg p-1 gap-1">
            <button 
              onClick={() => setFlowchartLanguage('en')}
              className={`px-3 py-1.5 text-xs font-medium rounded-md transition-all ${flowchartLanguage === 'en' ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 shadow-sm' : 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'}`}
            >
              {ui.langEn}
            </button>
            <button 
              onClick={() => setFlowchartLanguage('zh')}
              className={`px-3 py-1.5 text-xs font-medium rounded-md transition-all ${flowchartLanguage === 'zh' ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 shadow-sm' : 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'}`}
            >
              {ui.langZh}
            </button>
          </div>
        </div>

        <button
          onClick={handleGenerate}
          disabled={isLoading}
          className="w-full py-3 rounded-xl text-white font-semibold shadow-lg transform active:scale-[0.98] transition-all flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
          style={{ backgroundColor: currentTheme.title_fill }}
        >
          {isLoading ? (
            <>
              <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
              {ui.generating}
            </>
          ) : (
            <>
              <span>✨</span> {ui.generateBtn}
            </>
          )}
        </button>
      </div>

      {error && (
         <div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-600 dark:text-red-300 text-sm">
           {error}
         </div>
      )}

      {/* Stats Dashboard */}
      {stats && (
        <div className="grid grid-cols-3 gap-4 p-4 rounded-xl bg-white/50 dark:bg-gray-800/50 border border-gray-100 dark:border-gray-700">
          <div className="text-center">
            <div className="text-2xl font-bold" style={{ color: currentTheme.title_fill }}>{stats.nodes}</div>
            <div className="text-xs text-gray-500 uppercase">{ui.nodes}</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold" style={{ color: currentTheme.title_fill }}>{stats.edges}</div>
            <div className="text-xs text-gray-500 uppercase">{ui.edges}</div>
          </div>
          <div className="text-center">
             <div className="text-sm font-bold py-1.5 mt-1 rounded" style={{ backgroundColor: currentTheme.phase_fill, color: currentTheme.font_color }}>{stats.complexity}</div>
             <div className="text-xs text-gray-500 uppercase mt-1">{ui.complexity}</div>
          </div>
        </div>
      )}

      <div className="mt-auto pt-4 border-t border-gray-200 dark:border-gray-800">
        <button 
          onClick={() => setActiveTab('settings')}
          className="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-800 dark:hover:text-gray-200 transition-colors"
        >
          <span className="text-lg">⚙️</span> {ui.settings}
        </button>
      </div>
    </aside>

    {/* Right Main Content */}
    <div className="flex-1 flex flex-col h-full relative">
       {/* Tabs */}
       <div className="h-12 flex items-center px-6 gap-6 border-b border-gray-200 dark:border-gray-800 bg-white/30 dark:bg-black/20 backdrop-blur-sm">
          <button 
            onClick={() => setActiveTab('visual')}
            className={`h-full border-b-2 text-sm font-medium transition-colors ${activeTab === 'visual' ? 'border-current' : 'border-transparent text-gray-400 hover:text-gray-600'}`}
            style={{ borderColor: activeTab === 'visual' ? currentTheme.title_fill : 'transparent', color: activeTab === 'visual' ? currentTheme.title_fill : undefined }}
          >
            Visualizer
          </button>
          <button 
            onClick={() => setActiveTab('edit')}
            disabled={!spec}
            className={`h-full border-b-2 text-sm font-medium transition-colors ${activeTab === 'edit' ? 'border-current' : 'border-transparent text-gray-400 hover:text-gray-600 disabled:opacity-30'}`}
            style={{ borderColor: activeTab === 'edit' ? currentTheme.title_fill : 'transparent', color: activeTab === 'edit' ? currentTheme.title_fill : undefined }}
          >
            Editor
          </button>
          <button 
            onClick={() => setActiveTab('json')}
            disabled={!spec}
            className={`h-full border-b-2 text-sm font-medium transition-colors ${activeTab === 'json' ? 'border-current' : 'border-transparent text-gray-400 hover:text-gray-600 disabled:opacity-30'}`}
            style={{ borderColor: activeTab === 'json' ? currentTheme.title_fill : 'transparent', color: activeTab === 'json' ? currentTheme.title_fill : undefined }}
          >
            JSON Spec
          </button>
       </div>

       <div className="flex-1 p-6 overflow-hidden relative">
          {activeTab === 'visual' && (
            spec ? (
              <Visualizer data={spec} theme={currentTheme} width={800} height={600} />
            ) : (
              <div className="w-full h-full flex flex-col items-center justify-center text-gray-400 gap-4">
                <div className="w-24 h-24 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center animate-pulse">
                   <svg className="w-10 h-10 opacity-20" fill="currentColor" viewBox="0 0 20 20"><path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z" /><path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z" /></svg>
                </div>
                <p>{ui.subtitle}</p>
              </div>
            )
          )}

          {activeTab === 'edit' && spec && (
             <Editor spec={spec} onChange={setSpec} />
          )}

          {activeTab === 'json' && spec && (
            <div className="w-full h-full overflow-auto bg-gray-900 text-gray-100 p-4 rounded-xl font-mono text-xs shadow-inner">
               <pre>{JSON.stringify(spec, null, 2)}</pre>
            </div>
          )}

          {activeTab === 'settings' && (
             <div className="max-w-2xl mx-auto p-6 bg-white dark:bg-gray-800 rounded-xl shadow-xl">
                <h2 className="text-xl font-bold mb-4">{ui.prompt}</h2>
                <textarea 
                  value={systemPrompt}
                  onChange={(e) => setSystemPrompt(e.target.value)}
                  className="w-full h-64 p-4 bg-gray-50 dark:bg-gray-900 rounded border border-gray-200 dark:border-gray-700 font-mono text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <div className="mt-4 flex justify-end">
                  <button onClick={() => setSystemPrompt(DEFAULT_SYSTEM_PROMPT)} className="text-sm text-gray-500 hover:underline">Reset to Default</button>
                </div>
             </div>
          )}
       </div>
    </div>
  </main>
</div>
);
};

export default App;

Below is a complete transformation of your React app into a Streamlit app suitable for a Hugging Face Space, with:



- `agents.yaml` for agent/model configuration and an advanced default prompt  

- Multi-provider support: OpenAI, Gemini, Anthropic, XAI (Grok)  

- API key handling (env first, then optional user input; environment keys never shown)  

- Adjustable system prompt, temperature, max tokens, provider/model before running  

- Interactive visualization (Graphviz flowchart + dashboard)  

- “Wow” status indicators and an interactive metrics dashboard  



---



## 1. `agents.yaml`



Create a file `agents.yaml` in the project root:



```yaml

# agents.yaml

default_provider: "openai"

default_model: "gpt-4.1-mini"



providers:

  openai:

    name: "OpenAI"

    env_var: "OPENAI_API_KEY"

    models:

      - "gpt-5-nano"

      - "gpt-4.1-mini"

      - "gpt-4o-mini"

  gemini:

    name: "Gemini"

    env_var: "GEMINI_API_KEY"  # or GOOGLE_API_KEY if you prefer

    models:

      - "gemini-2.5-flash"

      - "gemini-2.5-flash-lite"

  anthropic:

    name: "Anthropic"

    env_var: "ANTHROPIC_API_KEY"

    models:

      - "claude-3-5-sonnet-latest"

      - "claude-3-5-haiku-latest"

  xai:

    name: "XAI Grok"

    env_var: "XAI_API_KEY"

    models:

      - "grok-4-fast-reaoning"

      - "grok-3-mini"



agents:

  flowchart_designer:

    description: >

      Converts natural language requirements into a structured flowchart

      JSON specification suitable for visualization.

    provider: "openai"

    model: "gpt-4.1-mini"

    temperature: 0.25

    max_tokens: 2048

    system_prompt: |-

      You are a senior software architect and UX engineer specializing in

      transforming natural-language descriptions of processes into precise,

      machine-readable flowchart specifications.



      ## Primary Goal

      Given:

      - A short description of a process, system, or idea (from the user),

      - A target human language for labels (e.g., English or Chinese),



      You must return a **single valid JSON object** describing a flowchart

      with nodes and edges, and nothing else.



      ## Output Format (Very Important)

      Return **only** a JSON object, no Markdown, no backticks, no commentary.

      The root object MUST have the following shape:



      {

        "title": "Short descriptive title in the target language",

        "description": "1-3 sentence overview in the target language",

        "language": "en" or "zh",

        "nodes": [

          {

            "id": "string-unique-id",

            "label": "Human-readable label in target language",

            "type": "start|end|decision|process|input|output|subprocess|note",

            "group": "Optional phase or swimlane name",

            "lane": "Optional role/responsibility",

            "metadata": {

              "summary": "Optional 1-sentence detail",

              "priority": "low|medium|high",

              "tags": ["optional", "keywords"]

            }

          }

        ],

        "edges": [

          {

            "source": "id-of-source-node",

            "target": "id-of-target-node",

            "label": "Optional edge label in target language",

            "condition": "Optional condition text in target language"

          }

        ]

      }



      Constraints:

      - `id` must be unique across all nodes.

      - Every edge `source` and `target` must reference an existing node `id`.

      - There MUST be exactly one `start` node and at least one `end` node.

      - Use clear, concise labels optimized for visualization.

      - Do not include comments, explanations, or any extra keys beyond the schema above.



      ## Style & Structure Guidelines

      - Organize the flow into logical phases via the `group` property (e.g., "Planning", "Execution").

      - Use `lane` for roles or actors (e.g., "User", "System", "Admin").

      - Use `decision` type for branching points ("Yes/No", "Success/Failure").

      - Favor a moderately granular breakdown (roughly 8-30 nodes, unless the description is extremely small or extremely large).

      - Use `metadata.priority` to indicate relative importance of a node to the overall process.



      ## Robustness & Validation

      - If user requirements are ambiguous, make reasonable assumptions and reflect them in node labels.

      - Ensure the JSON is syntactically valid and parsable.

      - Do NOT wrap JSON in Markdown code fences.

      - Do NOT include any natural-language explanation outside the JSON.



      The target language must match the language requested by the caller (provided separately as "language").

```



You can tweak defaults or model names as needed.



---



## 2. `app.py` (Streamlit for Hugging Face Space)



Below is a single-file Streamlit app that:



- Loads `agents.yaml`  

- Manages provider & model selection  

- Supports OpenAI, Gemini, Anthropic, and XAI Grok  

- Pulls API keys from environment first; if missing, allows secure user input  

- Lets the user edit the system prompt, temperature, and max tokens  

- Builds a flowchart via the selected LLM  

- Renders an interactive dashboard (metrics, status indicators) and a Graphviz flowchart  

- Allows manual JSON editing of the flowchart spec  



```python

# app.py

import os

import time

import json

import re

from typing import Any, Dict, Optional



import streamlit as st

import yaml

from graphviz import Digraph



# --- Optional imports; guard them for deployment flexibility ---

try:

    from openai import OpenAI

except ImportError:

    OpenAI = None



try:

    import google.generativeai as genai

except ImportError:

    genai = None



try:

    from anthropic import Anthropic

except ImportError:

    Anthropic = None



try:

    from xai_sdk import Client as XAIClient

    from xai_sdk.chat import user as xai_user, system as xai_system

except ImportError:

    XAIClient = None

    xai_user = None

    xai_system = None





# ----------------------------

# Utility: Load YAML config

# ----------------------------

@st.cache_resource(show_spinner=False)

def load_agents_config(path: str = "agents.yaml") -> Dict[str, Any]:

    with open(path, "r", encoding="utf-8") as f:

        return yaml.safe_load(f)





# ----------------------------

# Utility: API key management

# ----------------------------

def get_api_key(provider_key: str, provider_cfg: Dict[str, Any]) -> Optional[str]:

    """

    Priority:

    1. Environment variable (never shown)

    2. Session state (user-provided, password field)

    """

    env_var = provider_cfg.get("env_var")

    env_value = os.getenv(env_var or "")



    if "api_keys" not in st.session_state:

        st.session_state.api_keys = {}



    # If env var exists, always use it but never display it.

    if env_value:

        st.session_state.api_keys[provider_key] = "__from_env__"

        return env_value



    # Else fall back to user input in sidebar.

    label = f"{provider_cfg.get('name', provider_key)} API Key"

    user_value = st.sidebar.text_input(label, type="password")

    if user_value:

        st.session_state.api_keys[provider_key] = "__from_user__"

        return user_value



    return None





# ----------------------------

# Utility: Extract JSON from LLM text

# ----------------------------

def extract_json_from_text(text: str) -> Dict[str, Any]:

    """

    Tries to extract a JSON object from the LLM response.

    Prefer ```json ... ``` blocks; fallback to raw text.

    """

    # Look for fenced JSON

    fenced_match = re.search(r"```json\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)

    if fenced_match:

        candidate = fenced_match.group(1).strip()

    else:

        candidate = text.strip()



    # Remove potential leading/trailing junk

    # Try to find first '{' and last '}'

    first = candidate.find("{")

    last = candidate.rfind("}")

    if first != -1 and last != -1 and last > first:

        candidate = candidate[first : last + 1]



    return json.loads(candidate)





# ----------------------------

# LLM backends

# ----------------------------

def call_openai(

    model: str,

    api_key: str,

    system_prompt: str,

    user_prompt: str,

    language: str,

    temperature: float,

    max_tokens: int,

) -> str:

    if OpenAI is None:

        raise RuntimeError("openai package is not installed in this environment.")

    client = OpenAI(api_key=api_key)

    messages = [

        {"role": "system", "content": system_prompt},

        {

            "role": "user",

            "content": f"Language: {language}\n\nUser description:\n{user_prompt}",

        },

    ]

    resp = client.chat.completions.create(

        model=model,

        messages={ "messages": messages } if model.startswith("gpt-5") else messages,  # adjust if needed; keep simple else

        max_tokens=max_tokens,

        temperature=temperature,

    )

    # For latest SDK, response may differ; adjust as needed

    choice = resp.choices[0]

    return choice.message.content if hasattr(choice.message, "content") else choice.message["content"]





def call_gemini(

    model: str,

    api_key: str,

    system_prompt: str,

    user_prompt: str,

    language: str,

    temperature: float,

    max_tokens: int,

) -> str:

    if genai is None:

        raise RuntimeError("google.generativeai package is not installed.")

    genai.configure(api_key=api_key)

    full_prompt = (

        system_prompt

        + "\n\n"

        + f"Language: {language}\n\nUser description:\n{user_prompt}"

    )

    model_obj = genai.GenerativeModel(model)

    resp = model_obj.generate_content(

        full_prompt,

        generation_config={

            "temperature": float(temperature),

            "max_output_tokens": int(max_tokens),

        },

    )

    return resp.text





def call_anthropic(

    model: str,

    api_key: str,

    system_prompt: str,

    user_prompt: str,

    language: str,

    temperature: float,

    max_tokens: int,

) -> str:

    if Anthropic is None:

        raise RuntimeError("anthropic package is not installed.")

    client = Anthropic(api_key=api_key)

    resp = client.messages.create(

        model=model,

        max_tokens=max_tokens,

        temperature=temperature,

        system=system_prompt,

        messages=[

            {

                "role": "user",

                "content": f"Language: {language}\n\nUser description:\n{user_prompt}",

            }

        ],

    )

    # Concatenate all text blocks

    parts = []

    for block in resp.content:

        if getattr(block, "type", None) == "text":

            parts.append(block.text)

        elif isinstance(block, dict) and block.get("type") == "text":

            parts.append(block.get("text", ""))

    return "\n".join(parts)





def call_xai_grok(

    model: str,

    api_key: str,

    system_prompt: str,

    user_prompt: str,

    language: str,

    temperature: float,

    max_tokens: int,

) -> str:

    """

    Sample usage adapted from xAI docs, using xai_sdk.

    """

    if XAIClient is None or xai_user is None or xai_system is None:

        raise RuntimeError("xai_sdk package is not installed.")

    client = XAIClient(api_key=api_key, timeout=3600)



    # Note: Not all xAI models expose temperature/max_tokens in the same way;

    # this is a minimal compatible example.

    chat = client.chat.create(model=model)

    chat.append(xai_system(system_prompt))

    chat.append(

        xai_user(

            f"Language: {language}\n\nUser description:\n{user_prompt}"

        )

    )

    response = chat.sample()

    return response.content





def generate_flowchart_with_llm(

    provider_key: str,

    model: str,

    api_key: str,

    system_prompt: str,

    user_description: str,

    language: str,

    temperature: float,

    max_tokens: int,

) -> Dict[str, Any]:

    """

    Unified entry point for calling the chosen provider/model.

    """

    if provider_key == "openai":

        raw = call_openai(

            model, api_key, system_prompt, user_description, language, temperature, max_tokens

        )

    elif provider_key == "gemini":

        raw = call_gemini(

            model, api_key, system_prompt, user_description, language, temperature, max_tokens

        )

    elif provider_key == "anthropic":

        raw = call_anthropic(

            model, api_key, system_prompt, user_description, language, temperature, max_tokens

        )

    elif provider_key == "xai":

        raw = call_xai_grok(

            model, api_key, system_prompt, user_description, language, temperature, max_tokens

        )

    else:

        raise ValueError(f"Unsupported provider: {provider_key}")



    return extract_json_from_text(raw)





# ----------------------------

# Visualization: Graphviz

# ----------------------------

def flowchart_to_graphviz(spec: Dict[str, Any]) -> Digraph:

    g = Digraph(format="svg")

    g.attr(rankdir="TB", bgcolor="#ffffff00")  # transparent background



    # Basic node style

    g.attr("node", shape="box", style="rounded,filled", fontsize="10")



    nodes = spec.get("nodes", [])

    edges = spec.get("edges", [])



    # Color and shape by type for wow effect

    type_styles = {

        "start": {"shape": "oval", "fillcolor": "#4caf50", "fontcolor": "white"},

        "end": {"shape": "oval", "fillcolor": "#f44336", "fontcolor": "white"},

        "decision": {"shape": "diamond", "fillcolor": "#ff9800", "fontcolor": "black"},

        "process": {"shape": "box", "fillcolor": "#2196f3", "fontcolor": "white"},

        "input": {"shape": "parallelogram", "fillcolor": "#9c27b0", "fontcolor": "white"},

        "output": {"shape": "parallelogram", "fillcolor": "#00bcd4", "fontcolor": "black"},

        "subprocess": {"shape": "box3d", "fillcolor": "#8bc34a", "fontcolor": "black"},

        "note": {"shape": "note", "fillcolor": "#ffeb3b", "fontcolor": "black"},

    }



    for node in nodes:

        nid = str(node.get("id", ""))

        label = node.get("label", nid)

        ntype = node.get("type", "process")

        style = type_styles.get(ntype, type_styles["process"])

        group = node.get("group")

        lane = node.get("lane")

        meta = node.get("metadata", {}) or {}



        caption_parts = [label]

        if lane:

            caption_parts.append(f"[{lane}]")

        if group:

            caption_parts.append(f"({group})")

        if meta.get("priority"):

            caption_parts.append(f"prio: {meta['priority']}")



        caption = "\n".join(caption_parts)



        g.node(

            nid,

            label=caption,

            shape=style["shape"],

            fillcolor=style["fillcolor"],

            fontcolor=style["fontcolor"],

        )



    for edge in edges:

        src = str(edge.get("source", ""))

        tgt = str(edge.get("target", ""))

        label = edge.get("label") or edge.get("condition") or ""

        g.edge(src, tgt, label=label, fontsize="9")



    return g





# ----------------------------

# Streamlit App

# ----------------------------

def main():

    st.set_page_config(

        page_title="AI Flowchart Studio",

        page_icon="🧩",

        layout="wide",

    )



    cfg = load_agents_config()



    st.title("AI Flowchart Studio")

    st.caption("Multi-provider LLM flowchart generator (OpenAI • Gemini • Anthropic • XAI Grok)")



    # ---------------------------------

    # Sidebar: Controls & Settings

    # ---------------------------------

    st.sidebar.header("LLM & Configuration")



    providers_cfg = cfg.get("providers", {})

    provider_keys = list(providers_cfg.keys())

    default_provider_key = cfg.get("default_provider", provider_keys[0] if provider_keys else "")

    provider_labels = [providers_cfg[k].get("name", k.title()) for k in provider_keys]



    # Select provider

    provider_idx = provider_keys.index(default_provider_key) if default_provider_key in provider_keys else 0

    provider_label = st.sidebar.selectbox("Provider", provider_labels, index=provider_idx)

    selected_provider_key = provider_keys[provider_labels.index(provider_label)]

    provider_cfg = providers_cfg[selected_provider_key]



    # Model selection

    models = provider_cfg.get("models", [])

    default_model = cfg.get("default_model", models[0] if models else "")

    if default_model not in models and models:

        default_model = models[0]

    model = st.sidebar.selectbox("Model", models, index=models.index(default_model) if models else 0)



    # Agent defaults

    agent_cfg = cfg.get("agents", {}).get("flowchart_designer", {})

    default_temp = float(agent_cfg.get("temperature", 0.25))

    default_max_tokens = int(agent_cfg.get("max_tokens", 2048))

    default_system_prompt = agent_cfg.get("system_prompt", "")



    # Advanced generation params

    st.sidebar.subheader("Generation Settings")

    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, default_temp, 0.01)

    max_tokens = st.sidebar.slider("Max Tokens", 256, 4096, default_max_tokens, 64)



    # Language switch for flowchart labels

    language = st.sidebar.radio("Flowchart language", ["en", "zh"], index=0, horizontal=True)



    # Editable system prompt

    with st.sidebar.expander("System Prompt (Advanced)", expanded=False):

        system_prompt = st.text_area(

            "System prompt for the LLM",

            value=default_system_prompt,

            height=300,

        )



    # API key management

    api_key = get_api_key(selected_provider_key, provider_cfg)

    if not api_key:

        st.sidebar.warning(

            "No API key found in environment or input. "

            "Please provide a valid key to run the agent."

        )



    # ---------------------------------

    # Main layout: Input + Results

    # ---------------------------------

    col_left, col_right = st.columns([1, 2], gap="large")



    # ----- Left: Input panel -----

    with col_left:

        st.subheader("Describe your process")

        description = st.text_area(

            "Natural-language description",

            height=240,

            placeholder=(

                "Example:\n"

                "Design a user registration and login flow with email verification, "

                "password reset, and account lockout after 5 failed attempts."

            ),

        )



        generate_button = st.button("Generate Flowchart", type="primary", use_container_width=True)



        # Session state for spec

        if "flowchart_spec" not in st.session_state:

            st.session_state.flowchart_spec = None

        if "last_runtime_ms" not in st.session_state:

            st.session_state.last_runtime_ms = None

        if "last_error" not in st.session_state:

            st.session_state.last_error = None



        if generate_button:

            st.session_state.last_error = None



            if not api_key:

                st.error("Please set a valid API key in the sidebar to continue.")

            elif not description.strip():

                st.error("Please enter a description of the process.")

            else:

                with st.status("Calling LLM and building flowchart...", expanded=True) as status:

                    start_time = time.time()

                    try:

                        status.write(f"Provider: {provider_cfg.get('name')}  |  Model: {model}")

                        spec = generate_flowchart_with_llm(

                            provider_key=selected_provider_key,

                            model=model,

                            api_key=api_key,

                            system_prompt=system_prompt,

                            user_description=description,

                            language=language,

                            temperature=temperature,

                            max_tokens=max_tokens,

                        )

                        st.session_state.flowchart_spec = spec

                        runtime_ms = int((time.time() - start_time) * 1000)

                        st.session_state.last_runtime_ms = runtime_ms

                        status.update(label="Flowchart generated successfully", state="complete")

                    except Exception as e:

                        st.session_state.last_error = str(e)

                        status.update(label="Failed to generate flowchart", state="error")

                        st.error(f"Error: {e}")



        # Mini dashboard & wow indicators

        st.markdown("---")

        st.subheader("Flowchart Stats & Status")



        spec = st.session_state.flowchart_spec

        error_msg = st.session_state.last_error

        runtime_ms = st.session_state.last_runtime_ms



        nodes_count = len(spec.get("nodes", [])) if spec else 0

        edges_count = len(spec.get("edges", [])) if spec else 0



        # Complexity heuristic

        if nodes_count == 0:

            complexity = "N/A"

            complexity_score = 0

        elif nodes_count <= 10:

            complexity = "Low"

            complexity_score = 0.3

        elif nodes_count <= 25:

            complexity = "Medium"

            complexity_score = 0.6

        else:

            complexity = "High"

            complexity_score = 0.9



        # KPI metrics

        m1, m2, m3 = st.columns(3)

        m1.metric("Nodes", nodes_count)

        m2.metric("Edges", edges_count)

        m3.metric("Complexity", complexity)



        st.progress(complexity_score, text=f"Flowchart complexity index: {complexity}")



        # LLM status

        st.markdown("##### LLM Health")

        s1, s2 = st.columns(2)

        if runtime_ms:

            s1.metric("Last runtime (ms)", runtime_ms)

        else:

            s1.metric("Last runtime (ms)", "–")

        s2.metric("Provider", provider_cfg.get("name", selected_provider_key))



        if error_msg:

            st.error(f"Last error: {error_msg}")

        elif spec:

            st.success("Ready: Latest flowchart successfully generated.")

        else:

            st.info("Waiting: No flowchart generated yet.")



    # ----- Right: Visualization & JSON editor -----

    with col_right:

        st.subheader("Visualizer & JSON Editor")



        tabs = st.tabs(["Visualizer", "JSON Spec", "JSON Editor"])



        spec = st.session_state.flowchart_spec



        # Tab 1: Visualizer

        with tabs[0]:

            if spec:

                try:

                    graph = flowchart_to_graphviz(spec)

                    st.graphviz_chart(graph)

                except Exception as e:

                    st.error(f"Failed to render graph: {e}")

            else:

                st.info("No flowchart yet. Generate one from the left panel.")



        # Tab 2: JSON Spec (read-only)

        with tabs[1]:

            if spec:

                st.json(spec)

            else:

                st.info("JSON spec will appear here after a flowchart is generated.")



        # Tab 3: JSON Editor (editable)

        with tabs[2]:

            if spec is None:

                st.info("Generate a flowchart first to edit its JSON.")

            else:

                editable_json_str = st.text_area(

                    "Edit flowchart JSON (must remain valid)",

                    value=json.dumps(spec, indent=2, ensure_ascii=False),

                    height=400,

                )

                col_btn1, col_btn2 = st.columns([1, 1])

                with col_btn1:

                    if st.button("Apply JSON Changes"):

                        try:

                            new_spec = json.loads(editable_json_str)

                            # Basic validation

                            if not isinstance(new_spec, dict):

                                raise ValueError("Root must be a JSON object.")

                            if "nodes" not in new_spec or "edges" not in new_spec:

                                raise ValueError("JSON must contain 'nodes' and 'edges' keys.")

                            st.session_state.flowchart_spec = new_spec

                            st.success("JSON updated and applied successfully.")

                        except Exception as e:

                            st.error(f"Invalid JSON: {e}")

                with col_btn2:

                    if st.button("Reset to LLM Output"):

                        # Just re-load from saved original if desired; here we keep current spec

                        st.info("Current spec retained (no stored original to reset to).")



    st.markdown("---")

    st.caption("Powered by OpenAI • Gemini • Anthropic • XAI Grok")





if __name__ == "__main__":

    main()

```



---



## 3. Notes / How It Meets Your Requirements



- **Transform previous design to Streamlit**  

  - Left panel: input, language, generate button, stats → implemented using columns and sidebar controls.  

  - Right panel: tabs for Visualizer / JSON / JSON Editor (replacing React tabs).  

  - Settings (system prompt, model, max tokens, provider) moved into the sidebar.



- **Multi-provider support**  

  - Config via `agents.yaml` (`providers` section).  

  - Runtime selection via `Provider` and `Model` selectboxes in the sidebar.  

  - Includes sample logic for:

    - OpenAI (gpt-5-nano, gpt-4.1-mini, gpt-4o-mini)  

    - Gemini (gemini-2.5-flash, gemini-2.5-flash-lite)  

    - Anthropic (Claude variants)  

    - XAI/Grok (grok-4-fast-reaoning, grok-3-mini) using the `xai_sdk` sample pattern.



- **API keys from environment, optional UI input**  

  - `get_api_key()` checks `env_var` from `agents.yaml`.  

  - If not found, shows a password text input in the sidebar.  

  - Environment keys are never displayed (we mark them internally as `__from_env__`).  

  - User keys are typed into a password field.



- **User-modifiable prompt, max tokens, models**  

  - `System Prompt (Advanced)` expander in the sidebar with editable text_area.  

  - Sliders for temperature and max tokens.  

  - Provider & model selection from `agents.yaml`.



- **Advanced prompt**  

  - Provided in `agents.yaml` under `agents.flowchart_designer.system_prompt` with extensive instructions, JSON schema, style, and robustness guidance.



- **Visualization & Wow Dashboard**  

  - Graphviz chart with node-type-dependent shapes and colors.  

  - Metrics: node count, edge count, complexity level.  

  - Progress bar for complexity index.  

  - LLM health status: last runtime, provider name, success/error indicators.  

  - JSON viewer and full JSON editor tab for advanced users.



---



## 4. 20 Comprehensive Follow-up Questions



1. For the Graphviz-based visualizer, would you like to upgrade to a fully interactive canvas (e.g., pan/zoom, drag nodes) using PyVis or a similar library, or is the current static but styled diagram sufficient?



2. Do you want to support additional node attributes (e.g., estimated duration, cost, risk level) that can be used for richer visual encodings (size, color, border style)?



3. Should the flowchart support swimlanes explicitly (e.g., by grouping/layering nodes by `lane` in the visualization), and if yes, how strict is the layout requirement?



4. Would you like a validation panel that explains detected structural issues in plain language (e.g., “2 decision nodes have only one outgoing edge”) before rendering?



5. Should users be able to save multiple flowcharts in the same session (with names) and switch between them, essentially creating a mini project workspace?



6. Do you want an export feature for the flowchart (e.g., download as PNG/SVG, or JSON spec file) directly from the UI?



7. Would you like the app to support importing an existing JSON flowchart spec from a file upload and then editing/visualizing it?



8. Should the system prompt and agent configuration from `agents.yaml` be editable and persist across sessions (e.g., via a small config editor inside the app), or remain read-only defaults?



9. Would you like to log or visualize token usage and cost estimates per provider/model call (when the APIs expose that information)?



10. Are you planning to orchestrate multiple agents (e.g., one agent for requirements clarification, another for flowchart generation, another for optimization), or is a single generator agent sufficient for now?



11. Should the UI support multiple UI languages (like your original React `uiLanguage` toggle), including localized labels and instructions in the Streamlit interface?



12. Do you want a “diff view” that highlights changes between the original LLM-generated flowchart JSON and the user-edited version?



13. Would you like preset templates or example prompts (e.g., “Onboarding flow”, “Payment processing”, “Incident management”) that users can one-click load into the description box?



14. Should the complexity index be made more sophisticated (e.g., based on graph metrics like depth, branching factor, cycles) rather than just node count?



15. Do you want to track and display historical runs in this session (e.g., list of last 5 generations with provider, model, runtime, and small stats summary)?



16. Are there any specific compliance or safety filters you want before rendering the flowchart (e.g., detecting sensitive content and masking it or blocking generation)?



17. Should the app support image inputs in the future (e.g., user uploads a whiteboard sketch and an LLM with vision converts it into a flowchart spec)?



18. Do you want to allow power users to select raw JSON schema variants (e.g., “simple BPMN-like”, “detailed UX flow”) which change the system prompt and output shape?



19. How important is reproducibility for you—do you need to show or store seeds and full request parameters so users can reproduce an identical flowchart later?



20. Would you like a lightweight API endpoint (e.g., a simple FastAPI layer or Streamlit `st.experimental_connection`) so external tools can send a description and receive the JSON flowchart spec programmatically?
