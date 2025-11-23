Please create a agentic ai system that user can input text, then system will create flowchart image based on the following sample code (if you find other packages to create flowchart, please let user to choose using which package). Then User can choose light/dark, english//chinese, 20 styles based on flowers of the flowchart. Use can also modify text, add or delet chart elements. Then user can preview the modified results and download the flowchart. :Sample code:!apt-get -qq install graphviz -y > /dev/null 2>&1
!pip install graphviz -q
print("graphviz 安裝完成！")
from graphviz import Digraph
from IPython.display import Image, display
import os

建立流程圖
dot = Digraph(comment='國際醫療器材來源流向管理流程圖', format='png')
dot.attr(rankdir='TB', size='18,25!', dpi='300')
dot.attr('node', fontname='Microsoft JhengHei, Arial Unicode MS, DejaVu Sans', fontsize='12', style='filled', fillcolor='white')
dot.attr('edge', fontname='Microsoft JhengHei, Arial Unicode MS, DejaVu Sans', fontsize='11')

標題
dot.node('TITLE', '國際醫療器材來源流向管理現況研究\n整體執行流程圖',
shape='box', style='filled,bold', fillcolor='#4472C4', fontcolor='white', fontsize='18', height='1.2')

階段1：法規蒐集
dot.node('S1', '階段一：法規與執行現況蒐集', shape='box', fillcolor='#D9E8FF', fontsize='16')
dot.node('C1', '美國 FDA UDI 法規及執行情形\n(21 CFR Part 801, 830, GUDID資料庫)', shape='rect', fillcolor='#F0F8FF')
dot.node('C2', '歐盟 MDR/IVDR UDI 要求\n(EUDAMED、基本UDI-DI、UDI-DI/UDI-PI)', shape='rect', fillcolor='#F0F8FF')
dot.node('C3', '澳洲 TGA UDI 制度\n(AusUDID資料庫、與IMDRF一致性)', shape='rect', fillcolor='#F0F8FF')
dot.node('C4', '中國大陸 NMPA 唯一識別制度\n(UDI資料庫第一階段上線、2022年起分階段實施)', shape='rect', fillcolor='#F0F8FF')
dot.node('C5', '韓國 MFDS UDI 制度\n(K-UDI資料庫、2021-2025分階段實施)', shape='rect', fillcolor='#F0F8FF')
dot.node('C6', '新加坡 HSA UDI 要求\n(與IMDRF高度一致、2022年起實施)', shape='rect', fillcolor='#F0F8FF')
dot.node('C7', 'IMDRF UDI 指導原則\n(UDI系統核心文件、認可機構、資料庫要求)', shape='rect', fillcolor='#F0F8FF')

階段2：比較分析
dot.node('S2', '階段二：各國法規比較分析', shape='box', fillcolor='#FFE6E6', fontsize='16')
dot.node('A1', '法規架構與強制性比較', shape='ellipse', fillcolor='#FFF2CC')
dot.node('A2', 'UDI組成要件與格式規範比較\n(UDI-DI、UDI-PI、AIDC與HRI)', shape='ellipse', fillcolor='#FFF2CC')
dot.node('A3', '資料庫建置與資料上傳要求比較\n(公開程度、資料項目、更新頻率)', shape='ellipse', fillcolor='#FFF2CC')
dot.node('A4', '認可發行機構(Accrediting Agency)比較', shape='ellipse', fillcolor='#FFF2CC')
dot.node('A5', '實施時程與豁免範圍比較', shape='ellipse', fillcolor='#FFF2CC')
dot.node('A6', '與供應鏈追溯整合程度比較', shape='ellipse', fillcolor='#FFF2CC')

階段3：報告產出與我國建議
dot.node('S3', '階段三：報告產出與我國參採建議', shape='box', fillcolor='#E6FFE6', fontsize='16')
dot.node('R1', '各國法規與指引摘要報告', shape='note', fillcolor='#F0FFF0')
dot.node('R2', '國際比較分析矩陣表', shape='note', fillcolor='#F0FFF0')
dot.node('R3', '我國醫療器材唯一識別(UDI)制度建置建議\n(含法規架構、實施時程、分階段策略)', shape='note', fillcolor='#F0FFF0')
dot.node('R4', '我國UDI資料庫規劃建議\n(與國際接軌、資料項目、公開原則)', shape='note', fillcolor='#F0FFF0')
dot.node('R5', '認可發行機構評估與選定建議', shape='note', fillcolor='#F0FFF0')
dot.node('R6', '與GDSN、EPCIS等國際追溯系統整合建議', shape='note', fillcolor='#F0FFF0')
dot.node('FINAL', '完成「國際醫療器材來源流向管理現況研究」\n提報衛生福利部食品藥物管理署',
shape='doubleoctagon', fillcolor='#FFD966', fontsize='15', style='filled,bold')

連線（同前述）
dot.edge('TITLE', 'S1')
dot.edge('S1', 'C1'); dot.edge('S1', 'C2'); dot.edge('S1', 'C3')
dot.edge('S1', 'C4'); dot.edge('S1', 'C5'); dot.edge('S1', 'C6'); dot.edge('S1', 'C7')
for c in ['C1','C2','C3','C4','C5','C6','C7']: dot.edge(c, 'S2')
dot.edge('S2', 'A1'); dot.edge('S2', 'A2'); dot.edge('S2', 'A3')
dot.edge('S2', 'A4'); dot.edge('S2', 'A5'); dot.edge('S2', 'A6')
for a in ['A1','A2','A3','A4','A5','A6']: dot.edge(a, 'S3')
dot.edge('S3', 'R1'); dot.edge('S3', 'R2'); dot.edge('S3', 'R3')
dot.edge('S3', 'R4'); dot.edge('S3', 'R5'); dot.edge('S3', 'R6')
for r in ['R1','R2','R3','R4','R5','R6']: dot.edge(r, 'FINAL')

產生檔案並直接顯示
filename = '國際醫療器材來源流向管理流程圖_高解析度'
dot.render(filename, cleanup=True)  # 產生 .png 檔

直接在 Colab 顯示圖片
display(Image(filename + '.png'))

同時提供下載連結
from google.colab import files
files.download(filename + '.png')

Below is a complete design and sample implementation for your Hugging Face Space + Streamlit “agentic flowchart generator”, including:



- Advanced system prompt (editable by user)

- `agents.yaml` skeleton

- Streamlit app with:

  - Multi‑provider LLM (Gemini, OpenAI/OPENAAI, Grok) with model selection

  - Env‑based API keys + optional user input keys (never displayed if from env)

  - Text → flowchart spec → Graphviz/Mermaid rendering

  - 20 flower‑based style themes (light/dark)

  - English/Chinese language mode

  - Edit/add/delete nodes/edges, preview, download

  - “Wow” status indicators + interactive dashboard elements



---



## 1. Advanced system prompt (default, user‑editable)



You’ll expose this in the UI as an editable text area. This is the default:



```python

DEFAULT_SYSTEM_PROMPT = """

You are an expert information architect and visualization designer.

Your task is to transform a natural-language description of a process into a clean, well-structured, directed flowchart.



General requirements:

- You MUST strictly follow the output schema described below.

- Output MUST be valid JSON only (no markdown, no comments, no code fences).

- Node IDs must be unique, short, and safe for Graphviz (letters, digits, underscores only).

- Assume the rendering engine will handle colors, fonts, and layout; you only define structure and labels.

- Respect the requested language for ALL labels and the title (English or Chinese).



User will provide:

- A textual description of a process or workflow.

- A preferred language: "en" (English) or "zh" (Chinese).

- Optional hints like stages, phases, or key entities.



Your job:

1. Understand the process.

2. Break it into stages/phases (if applicable).

3. Define nodes and directed edges.

4. Choose reasonable shapes for nodes.

5. Produce a JSON object matching the SCHEMA below.



SCHEMA (JSON):



{

  "title": "string, human-friendly title for the flowchart in the requested language",

  "direction": "string, one of: 'TB' (top-bottom), 'BT', 'LR' (left-right), 'RL'",

  "nodes": [

    {

      "id": "short_unique_identifier",

      "label": "node label, in the requested language",

      "category": "one of: 'title', 'phase', 'step', 'decision', 'input', 'output', 'note', 'end'",

      "shape": "one of: 'box', 'ellipse', 'diamond', 'parallelogram', 'note', 'doubleoctagon'",

      "group": "optional logical grouping, e.g. 'Phase 1', can be empty string",

      "order": "integer indicating approximate vertical or horizontal ordering within its group"

    }

  ],

  "edges": [

    {

      "from": "source_node_id",

      "to": "target_node_id",

      "label": "optional edge label in the requested language (can be empty string)",

      "style": "one of: 'solid', 'dashed', 'dotted'",

      "priority": "integer; smaller means more important/central edges"

    }

  ]

}



Guidance:



- Use "title" category with shape "box" or "note" for the overall diagram title (single node).

- Use "phase" for high-level stages (e.g., Phase 1, Step A, etc.).

- Use "step" for ordinary actions/tasks.

- Use "decision" (diamond) for yes/no or branching conditions.

- Use "input" or "output" for start/end or I/O artifacts, as appropriate.

- Use "end" for the final completion node(s).

- "group" is typically a human-readable phase name; nodes with same group belong to same logical stage.

- "order" should be consistent and roughly from 1, 2, 3, ... following process flow within each group.



Language behavior:



- The assistant will be given a parameter "language" with value "en" or "zh".

- If language is "en", all labels and title must be in English.

- If language is "zh", all labels and title must be in Chinese (Traditional or Simplified is acceptable, but be consistent).

- Do NOT mix languages unless the user explicitly does so inside the description.



Output rules:



- Return ONLY a single JSON object conforming to the schema.

- Do NOT wrap in ```json or any markdown.

- Do NOT add explanations, comments, or extra keys.

- Make sure the JSON parses without errors.

"""

```



You will append a short “runtime” hint to this system prompt before sending to the model:



```python

runtime_hint = f"User-selected language code: {language}. Base theme: {theme}. Flower style: {flower_style}. You only handle structure and labels; styling is purely handled by the renderer."

system_prompt = DEFAULT_SYSTEM_PROMPT + "\n\n" + runtime_hint

```



---



## 2. `agents.yaml` (skeleton)



This file describes the logical agents; the actual provider/model will be chosen in the UI, so we keep it generic.



```yaml

version: 1



agents:

  - id: flowchart-architect

    name: Flowchart Architect

    description: >

      Takes a natural-language description of a workflow and returns a structured JSON

      specification of nodes and edges for a flowchart.

    type: llm

    model: "${MODEL_NAME}"   # Will be supplied from the UI (Gemini, OpenAI/OPENAAI, or Grok).

    system_prompt: |

      {{ DEFAULT_SYSTEM_PROMPT }}

    inputs:

      - id: description

        type: text

      - id: language

        type: enum

        options: ["en", "zh"]



  - id: flowchart-renderer

    name: Flowchart Renderer

    description: >

      Pure Python / Graphviz renderer that converts the JSON specification into a final

      diagram (DOT, PNG, SVG, Mermaid, etc.). This is not an LLM agent.

    type: tool

    tool: "python.flowchart_renderer"



  - id: flowchart-editor

    name: Flowchart Editor

    description: >

      UI editing layer inside Streamlit that lets users add, delete, or modify nodes and edges

      before rendering or downloading.

    type: ui



flows:

  - id: full-pipeline

    name: Text-to-Flowchart Pipeline

    description: >

      1) Flowchart Architect LLM → JSON spec;

      2) Flowchart Editor UI → optional structural edits;

      3) Flowchart Renderer → final downloadable image.

    steps:

      - agent: flowchart-architect

      - agent: flowchart-editor

      - agent: flowchart-renderer

```



You don’t have to strictly wire this into Streamlit, but it documents the architecture and roles.



---



## 3. Streamlit app (`app.py`) for Hugging Face Space



This is a single-file example. Adjust imports and requirements (`streamlit`, `graphviz`, `pydantic`, optional `google-generativeai`, `openai`, `xai-sdk`) in `requirements.txt`.



```python

import os

import json

import re

from io import BytesIO

from typing import Dict, Any, List



import streamlit as st

import pandas as pd

import graphviz



# Optional LLM libraries

try:

    import google.generativeai as genai

except ImportError:

    genai = None



try:

    from openai import OpenAI

except ImportError:

    OpenAI = None



try:

    from xai_sdk import Client as XAIClient

    from xai_sdk.chat import user as grok_user, system as grok_system

except ImportError:

    XAIClient = None

    grok_user = grok_system = None





# ---------------------------

# 1. Prompts & style presets

# ---------------------------



DEFAULT_SYSTEM_PROMPT = """

You are an expert information architect and visualization designer.

Your task is to transform a natural-language description of a process into a clean, well-structured, directed flowchart.



General requirements:

- You MUST strictly follow the output schema described below.

- Output MUST be valid JSON only (no markdown, no comments, no code fences).

- Node IDs must be unique, short, and safe for Graphviz (letters, digits, underscores only).

- Assume the rendering engine will handle colors, fonts, and layout; you only define structure and labels.

- Respect the requested language for ALL labels and the title (English or Chinese).



User will provide:

- A textual description of a process or workflow.

- A preferred language: "en" (English) or "zh" (Chinese).

- Optional hints like stages, phases, or key entities.



Your job:

1. Understand the process.

2. Break it into stages/phases (if applicable).

3. Define nodes and directed edges.

4. Choose reasonable shapes for nodes.

5. Produce a JSON object matching the SCHEMA below.



SCHEMA (JSON):



{

  "title": "string, human-friendly title for the flowchart in the requested language",

  "direction": "string, one of: 'TB' (top-bottom), 'BT', 'LR' (left-right), 'RL'",

  "nodes": [

    {

      "id": "short_unique_identifier",

      "label": "node label, in the requested language",

      "category": "one of: 'title', 'phase', 'step', 'decision', 'input', 'output', 'note', 'end'",

      "shape": "one of: 'box', 'ellipse', 'diamond', 'parallelogram', 'note', 'doubleoctagon'",

      "group": "optional logical grouping, e.g. 'Phase 1', can be empty string",

      "order": "integer indicating approximate vertical or horizontal ordering within its group"

    }

  ],

  "edges": [

    {

      "from": "source_node_id",

      "to": "target_node_id",

      "label": "optional edge label in the requested language (can be empty string)",

      "style": "one of: 'solid', 'dashed', 'dotted'",

      "priority": "integer; smaller means more important/central edges"

    }

  ]

}



Guidance:



- Use "title" category with shape "box" or "note" for the overall diagram title (single node).

- Use "phase" for high-level stages (e.g., Phase 1, Step A, etc.).

- Use "step" for ordinary actions/tasks.

- Use "decision" (diamond) for yes/no or branching conditions.

- Use "input" or "output" for start/end or I/O artifacts, as appropriate.

- Use "end" for the final completion node(s).

- "group" is typically a human-readable phase name; nodes with same group belong to same logical stage.

- "order" should be consistent and roughly from 1, 2, 3, ... following process flow within each group.



Language behavior:



- The assistant will be given a parameter "language" with value "en" or "zh".

- If language is "en", all labels and title must be in English.

- If language is "zh", all labels and title must be in Chinese (Traditional or Simplified is acceptable, but be consistent).

- Do NOT mix languages unless the user explicitly does so inside the description.



Output rules:



- Return ONLY a single JSON object conforming to the schema.

- Do NOT wrap in ```json or any markdown.

- Do NOT add explanations, comments, or extra keys.

- Make sure the JSON parses without errors.

"""



# 20 flower-based style presets (each has light/dark variants)

FLOWER_STYLES: Dict[str, Dict[str, Dict[str, str]]] = {

    "Sakura": {

        "light": {

            "bg_color": "#FFF7FB",

            "title_fill": "#F78FB3",

            "phase_fill": "#FADDE1",

            "step_fill": "#FFFFFF",

            "decision_fill": "#FFE4EE",

            "end_fill": "#FFD1DC",

            "font_color": "#333333",

            "edge_color": "#F78FB3",

        },

        "dark": {

            "bg_color": "#2B1B2D",

            "title_fill": "#F78FB3",

            "phase_fill": "#5A2B4D",

            "step_fill": "#3A223A",

            "decision_fill": "#6A3058",

            "end_fill": "#C65B7C",

            "font_color": "#FCE4EC",

            "edge_color": "#F78FB3",

        },

    },

    "Rose": {

        "light": {

            "bg_color": "#FFF5F7",

            "title_fill": "#E63946",

            "phase_fill": "#FFC8D8",

            "step_fill": "#FFFFFF",

            "decision_fill": "#FFB3C6",

            "end_fill": "#FFE0E9",

            "font_color": "#2B2626",

            "edge_color": "#E63946",

        },

        "dark": {

            "bg_color": "#2B1B1D",

            "title_fill": "#E63946",

            "phase_fill": "#5B2227",

            "step_fill": "#3C2224",

            "decision_fill": "#7A2931",

            "end_fill": "#F28482",

            "font_color": "#FFECEC",

            "edge_color": "#F1A7B3",

        },

    },

    "Lotus": {

        "light": {

            "bg_color": "#F6FFF7",

            "title_fill": "#2A9D8F",

            "phase_fill": "#C9F2E9",

            "step_fill": "#FFFFFF",

            "decision_fill": "#B5EAD7",

            "end_fill": "#E8F8F5",

            "font_color": "#1B2B2B",

            "edge_color": "#2A9D8F",

        },

        "dark": {

            "bg_color": "#0B1C19",

            "title_fill": "#2A9D8F",

            "phase_fill": "#17453F",

            "step_fill": "#102825",

            "decision_fill": "#1E5C52",

            "end_fill": "#3AAFA9",

            "font_color": "#E0F7F4",

            "edge_color": "#2A9D8F",

        },

    },

    "Sunflower": {

        "light": {

            "bg_color": "#FFFBEB",

            "title_fill": "#F59E0B",

            "phase_fill": "#FDE68A",

            "step_fill": "#FFFFFF",

            "decision_fill": "#FBBF24",

            "end_fill": "#FEF3C7",

            "font_color": "#3F2A1C",

            "edge_color": "#D97706",

        },

        "dark": {

            "bg_color": "#1F170C",

            "title_fill": "#F59E0B",

            "phase_fill": "#78350F",

            "step_fill": "#3B2F1C",

            "decision_fill": "#C47F1A",

            "end_fill": "#FBBF24",

            "font_color": "#FEF9C3",

            "edge_color": "#FBBF24",

        },

    },

    "Lavender": {

        "light": {

            "bg_color": "#F9F5FF",

            "title_fill": "#7C3AED",

            "phase_fill": "#DDD6FE",

            "step_fill": "#FFFFFF",

            "decision_fill": "#C4B5FD",

            "end_fill": "#EDE9FE",

            "font_color": "#312E81",

            "edge_color": "#7C3AED",

        },

        "dark": {

            "bg_color": "#18122B",

            "title_fill": "#7C3AED",

            "phase_fill": "#44337A",

            "step_fill": "#251C49",

            "decision_fill": "#553C9A",

            "end_fill": "#A78BFA",

            "font_color": "#EDE9FE",

            "edge_color": "#A78BFA",

        },

    },

    "Orchid": {

        "light": {

            "bg_color": "#FFF7FF",

            "title_fill": "#C026D3",

            "phase_fill": "#F5D0FE",

            "step_fill": "#FFFFFF",

            "decision_fill": "#E9D5FF",

            "end_fill": "#FAE8FF",

            "font_color": "#3B0764",

            "edge_color": "#C026D3",

        },

        "dark": {

            "bg_color": "#24002F",

            "title_fill": "#C026D3",

            "phase_fill": "#581C87",

            "step_fill": "#3B0764",

            "decision_fill": "#6B21A8",

            "end_fill": "#E879F9",

            "font_color": "#FCE7F3",

            "edge_color": "#E879F9",

        },

    },

    "Peony": {

        "light": {

            "bg_color": "#FFF5F5",

            "title_fill": "#DB2777",

            "phase_fill": "#FBCFE8",

            "step_fill": "#FFFFFF",

            "decision_fill": "#F9A8D4",

            "end_fill": "#FCE7F3",

            "font_color": "#4A0019",

            "edge_color": "#DB2777",

        },

        "dark": {

            "bg_color": "#330013",

            "title_fill": "#DB2777",

            "phase_fill": "#831843",

            "step_fill": "#500724",

            "decision_fill": "#9D174D",

            "end_fill": "#F472B6",

            "font_color": "#FFE4F0",

            "edge_color": "#F472B6",

        },

    },

    "Camellia": {

        "light": {

            "bg_color": "#FFF8F3",

            "title_fill": "#EA580C",

            "phase_fill": "#FED7AA",

            "step_fill": "#FFFFFF",

            "decision_fill": "#FDBA74",

            "end_fill": "#FFEDD5",

            "font_color": "#3B1F0B",

            "edge_color": "#EA580C",

        },

        "dark": {

            "bg_color": "#2B1608",

            "title_fill": "#EA580C",

            "phase_fill": "#7C2D12",

            "step_fill": "#431407",

            "decision_fill": "#9A3412",

            "end_fill": "#FDBA74",

            "font_color": "#FFEDD5",

            "edge_color": "#FDBA74",

        },

    },

    "Hydrangea": {

        "light": {

            "bg_color": "#F3F8FF",

            "title_fill": "#2563EB",

            "phase_fill": "#BFDBFE",

            "step_fill": "#FFFFFF",

            "decision_fill": "#93C5FD",

            "end_fill": "#DBEAFE",

            "font_color": "#1E293B",

            "edge_color": "#2563EB",

        },

        "dark": {

            "bg_color": "#0B1220",

            "title_fill": "#2563EB",

            "phase_fill": "#1E3A8A",

            "step_fill": "#111827",

            "decision_fill": "#1D4ED8",

            "end_fill": "#60A5FA",

            "font_color": "#E5E7EB",

            "edge_color": "#60A5FA",

        },

    },

    "Tulip": {

        "light": {

            "bg_color": "#FFF7ED",

            "title_fill": "#EA580C",

            "phase_fill": "#FED7AA",

            "step_fill": "#FFFFFF",

            "decision_fill": "#FDBA74",

            "end_fill": "#FFEDD5",

            "font_color": "#4B2E1A",

            "edge_color": "#EA580C",

        },

        "dark": {

            "bg_color": "#26160C",

            "title_fill": "#EA580C",

            "phase_fill": "#7C2D12",

            "step_fill": "#3F2010",

            "decision_fill": "#9A3412",

            "end_fill": "#FDBA74",

            "font_color": "#FFE7D6",

            "edge_color": "#FDBA74",

        },

    },

    "Daisy": {

        "light": {

            "bg_color": "#FDFDF5",

            "title_fill": "#FACC15",

            "phase_fill": "#FEF9C3",

            "step_fill": "#FFFFFF",

            "decision_fill": "#FDE047",

            "end_fill": "#FEFCE8",

            "font_color": "#292524",

            "edge_color": "#FACC15",

        },

        "dark": {

            "bg_color": "#1F1F12",

            "title_fill": "#FACC15",

            "phase_fill": "#854D0E",

            "step_fill": "#292524",

            "decision_fill": "#EAB308",

            "end_fill": "#FEF08A",

            "font_color": "#FEFCE8",

            "edge_color": "#FEF08A",

        },

    },

    "Cherry Blossom": {

        "light": {

            "bg_color": "#FFF7FB",

            "title_fill": "#EC4899",

            "phase_fill": "#F9A8D4",

            "step_fill": "#FFFFFF",

            "decision_fill": "#F472B6",

            "end_fill": "#FCE7F3",

            "font_color": "#4B1025",

            "edge_color": "#EC4899",

        },

        "dark": {

            "bg_color": "#2B0B1D",

            "title_fill": "#EC4899",

            "phase_fill": "#831843",

            "step_fill": "#500724",

            "decision_fill": "#9D174D",

            "end_fill": "#F472B6",

            "font_color": "#FCE7F3",

            "edge_color": "#F472B6",

        },

    },

    "Gardenia": {

        "light": {

            "bg_color": "#FBFEFF",

            "title_fill": "#0EA5E9",

            "phase_fill": "#BFDBFE",

            "step_fill": "#FFFFFF",

            "decision_fill": "#7DD3FC",

            "end_fill": "#E0F2FE",

            "font_color": "#082F49",

            "edge_color": "#0EA5E9",

        },

        "dark": {

            "bg_color": "#03141F",

            "title_fill": "#0EA5E9",

            "phase_fill": "#075985",

            "step_fill": "#082F49",

            "decision_fill": "#0369A1",

            "end_fill": "#38BDF8",

            "font_color": "#E0F2FE",

            "edge_color": "#38BDF8",

        },

    },

    "Magnolia": {

        "light": {

            "bg_color": "#FFFBFF",

            "title_fill": "#9333EA",

            "phase_fill": "#E9D5FF",

            "step_fill": "#FFFFFF",

            "decision_fill": "#D8B4FE",

            "end_fill": "#F3E8FF",

            "font_color": "#2E1065",

            "edge_color": "#9333EA",

        },

        "dark": {

            "bg_color": "#1D102A",

            "title_fill": "#9333EA",

            "phase_fill": "#5B21B6",

            "step_fill": "#341567",

            "decision_fill": "#7C3AED",

            "end_fill": "#C4B5FD",

            "font_color": "#F5EFFF",

            "edge_color": "#C4B5FD",

        },

    },

    "Iris": {

        "light": {

            "bg_color": "#F5F3FF",

            "title_fill": "#4F46E5",

            "phase_fill": "#C7D2FE",

            "step_fill": "#FFFFFF",

            "decision_fill": "#A5B4FC",

            "end_fill": "#E0E7FF",

            "font_color": "#111827",

            "edge_color": "#4F46E5",

        },

        "dark": {

            "bg_color": "#050716",

            "title_fill": "#4F46E5",

            "phase_fill": "#312E81",

            "step_fill": "#111827",

            "decision_fill": "#4338CA",

            "end_fill": "#818CF8",

            "font_color": "#E5E7EB",

            "edge_color": "#818CF8",

        },

    },

    "Poppy": {

        "light": {

            "bg_color": "#FFF6F5",

            "title_fill": "#F97316",

            "phase_fill": "#FED7AA",

            "step_fill": "#FFFFFF",

            "decision_fill": "#FDBA74",

            "end_fill": "#FFEDD5",

            "font_color": "#3B1F0B",

            "edge_color": "#F97316",

        },

        "dark": {

            "bg_color": "#2A1408",

            "title_fill": "#F97316",

            "phase_fill": "#7C2D12",

            "step_fill": "#431407",

            "decision_fill": "#C2410C",

            "end_fill": "#FB923C",

            "font_color": "#FFEDD5",

            "edge_color": "#FB923C",

        },

    },

    "Marigold": {

        "light": {

            "bg_color": "#FFFBE6",

            "title_fill": "#F59E0B",

            "phase_fill": "#FEF3C7",

            "step_fill": "#FFFFFF",

            "decision_fill": "#FCD34D",

            "end_fill": "#FEF9C3",

            "font_color": "#3F2A1C",

            "edge_color": "#F59E0B",

        },

        "dark": {

            "bg_color": "#241809",

            "title_fill": "#F59E0B",

            "phase_fill": "#854D0E",

            "step_fill": "#422006",

            "decision_fill": "#EAB308",

            "end_fill": "#FACC15",

            "font_color": "#FEF9C3",

            "edge_color": "#FACC15",

        },

    },

    "Lilac": {

        "light": {

            "bg_color": "#FBF5FF",

            "title_fill": "#8B5CF6",

            "phase_fill": "#E9D5FF",

            "step_fill": "#FFFFFF",

            "decision_fill": "#DDD6FE",

            "end_fill": "#F5F3FF",

            "font_color": "#312E81",

            "edge_color": "#8B5CF6",

        },

        "dark": {

            "bg_color": "#15111E",

            "title_fill": "#8B5CF6",

            "phase_fill": "#4C1D95",

            "step_fill": "#2E1065",

            "decision_fill": "#6D28D9",

            "end_fill": "#C4B5FD",

            "font_color": "#EDE9FE",

            "edge_color": "#C4B5FD",

        },

    },

    "Bluebell": {

        "light": {

            "bg_color": "#EFF6FF",

            "title_fill": "#2563EB",

            "phase_fill": "#BFDBFE",

            "step_fill": "#FFFFFF",

            "decision_fill": "#93C5FD",

            "end_fill": "#DBEAFE",

            "font_color": "#0F172A",

            "edge_color": "#2563EB",

        },

        "dark": {

            "bg_color": "#020617",

            "title_fill": "#2563EB",

            "phase_fill": "#1D4ED8",

            "step_fill": "#0F172A",

            "decision_fill": "#3B82F6",

            "end_fill": "#60A5FA",

            "font_color": "#E5E7EB",

            "edge_color": "#60A5FA",

        },

    },

    "Wisteria": {

        "light": {

            "bg_color": "#F5F3FF",

            "title_fill": "#7C3AED",

            "phase_fill": "#DDD6FE",

            "step_fill": "#FFFFFF",

            "decision_fill": "#C4B5FD",

            "end_fill": "#EDE9FE",

            "font_color": "#312E81",

            "edge_color": "#7C3AED",

        },

        "dark": {

            "bg_color": "#1D1232",

            "title_fill": "#7C3AED",

            "phase_fill": "#4C1D95",

            "step_fill": "#2E1065",

            "decision_fill": "#6D28D9",

            "end_fill": "#A855F7",

            "font_color": "#F5F3FF",

            "edge_color": "#A855F7",

        },

    },

}



FLOWER_STYLE_NAMES = list(FLOWER_STYLES.keys())





# ---------------------------

# 2. LLM call helpers

# ---------------------------



def extract_json_from_text(text: str) -> Dict[str, Any]:

    """Extract the first JSON object from a string and parse it."""

    try:

        match = re.search(r'\{.*\}', text, re.S)

        if match:

            json_str = match.group(0)

        else:

            json_str = text

        return json.loads(json_str)

    except Exception as e:

        raise ValueError(f"Failed to parse JSON from LLM response: {e}\nRaw content:\n{text[:2000]}")





def call_llm(

    provider: str,

    model: str,

    system_prompt: str,

    user_prompt: str,

    max_tokens: int,

    api_key: str,

) -> str:

    messages = [

        {"role": "system", "content": system_prompt},

        {"role": "user", "content": user_prompt},

    ]



    if provider == "Gemini":

        if genai is None:

            raise RuntimeError("google-generativeai is not installed.")

        genai.configure(api_key=api_key)

        gmodel = genai.GenerativeModel(model)

        resp = gmodel.generate_content(

            [

                {"role": "system", "parts": [system_prompt]},

                {"role": "user", "parts": [user_prompt]},

            ],

            generation_config={"max_output_tokens": max_tokens},

        )

        return resp.text



    elif provider == "OpenAI / OPENAAI":

        if OpenAI is None:

            raise RuntimeError("openai Python SDK is not installed.")

        # If using OPENAAI-compatible endpoint, allow custom base URL via env

        base_url = os.getenv("OPENAAI_BASE_URL") or os.getenv("OPENAI_BASE_URL")

        if base_url:

            client = OpenAI(api_key=api_key, base_url=base_url)

        else:

            client = OpenAI(api_key=api_key)

        resp = client.chat.completions.create(

            model=model,

            messages=messages,

            max_tokens=max_tokens,

        )

        return resp.choices[0].message.content



    elif provider == "Grok":

        if XAIClient is None or grok_user is None:

            raise RuntimeError("xai_sdk is not installed.")

        # Sample code adapted from your snippet

        client = XAIClient(api_key=api_key, timeout=3600)

        chat = client.chat.create(model=model)

        chat.append(grok_system(system_prompt))

        chat.append(grok_user(user_prompt))

        response = chat.sample()

        return response.content



    else:

        raise ValueError(f"Unknown provider: {provider}")





# ---------------------------

# 3. Graph rendering helpers

# ---------------------------



def build_graphviz_from_spec(

    spec: Dict[str, Any],

    theme: str,

    flower_style: str,

    dpi: int = 300,

) -> graphviz.Digraph:

    style = FLOWER_STYLES.get(flower_style, FLOWER_STYLES[FLOWER_STYLE_NAMES[0]])[theme]



    dot = graphviz.Digraph(

        comment=spec.get("title", "Flowchart"),

        format="png"

    )



    direction = spec.get("direction", "TB")

    dot.attr(rankdir=direction, dpi=str(dpi))

    dot.attr(

        "graph",

        bgcolor=style["bg_color"],

        fontname="Microsoft JhengHei, Arial Unicode MS, DejaVu Sans",

    )

    dot.attr(

        "node",

        fontname="Microsoft JhengHei, Arial Unicode MS, DejaVu Sans",

        fontsize="12",

        style="filled",

        fillcolor=style["step_fill"],

        fontcolor=style["font_color"],

    )

    dot.attr(

        "edge",

        fontname="Microsoft JhengHei, Arial Unicode MS, DejaVu Sans",

        fontsize="11",

        color=style["edge_color"],

    )



    # Node rendering with category-specific colors

    for node in spec.get("nodes", []):

        nid = node["id"]

        label = node.get("label", nid)

        category = node.get("category", "step")

        shape = node.get("shape", "box")



        fillcolor = style["step_fill"]

        extra_style = "filled"



        if category == "title":

            fillcolor = style["title_fill"]

            extra_style = "filled,bold"

        elif category == "phase":

            fillcolor = style["phase_fill"]

        elif category == "decision":

            fillcolor = style["decision_fill"]

        elif category in ("end", "output"):

            fillcolor = style["end_fill"]

        elif category == "note":

            fillcolor = style["step_fill"]



        dot.node(

            nid,

            label,

            shape=shape,

            fillcolor=fillcolor,

            style=extra_style,

        )



    # Edge rendering

    for edge in spec.get("edges", []):

        src = edge.get("from")

        dst = edge.get("to")

        label = edge.get("label", "")

        style_edge = edge.get("style", "solid")

        attrs = {"style": style_edge}

        if label:

            attrs["label"] = label

        dot.edge(src, dst, **attrs)



    return dot





def build_mermaid_from_spec(spec: Dict[str, Any]) -> str:

    """

    Generate a Mermaid flowchart definition string (text only).

    This can be exported or used in other frontends.

    """

    direction = spec.get("direction", "TB")

    direction_map = {"TB": "TB", "BT": "BT", "LR": "LR", "RL": "RL"}

    mdir = direction_map.get(direction, "TB")



    lines = [f"flowchart {mdir}"]



    # Node shapes (simplified mapping)

    for node in spec.get("nodes", []):

        nid = node["id"]

        label = node.get("label", nid)

        shape = node.get("shape", "box")



        if shape == "diamond":

            # decision

            lines.append(f'    {nid}{{"{label}"}}')

        elif shape in ("ellipse", "parallelogram"):

            lines.append(f'    {nid}("{label}")')

        elif shape == "doubleoctagon":

            lines.append(f'    {nid}(["{label}"])')

        else:

            lines.append(f'    {nid}["{label}"]')



    for edge in spec.get("edges", []):

        src = edge.get("from")

        dst = edge.get("to")

        label = edge.get("label", "")

        if label:

            lines.append(f'    {src} -->|{label}| {dst}')

        else:

            lines.append(f'    {src} --> {dst}')



    return "\n".join(lines)





# ---------------------------

# 4. Streamlit UI

# ---------------------------



def get_localized_texts(language: str) -> Dict[str, str]:

    if language == "zh":

        return {

            "title": "AI 流程圖生成與編輯儀表板",

            "description": "輸入文字描述，由智能代理設計流程圖，並支援樣式切換、編輯與下載。",

            "input_label": "流程 / 專案文字描述",

            "generate_button": "生成流程圖規格",

            "preview_button": "套用編輯並預覽流程圖",

            "download_button": "下載流程圖圖片",

            "provider_label": "選擇模型提供者",

            "model_label": "選擇模型",

            "prompt_label": "進階系統提示詞（可編輯）",

            "max_tokens": "最大 Token 數",

            "theme": "主題模式",

            "flower_style": "花卉風格樣式",

            "language_label": "流程圖語言",

            "renderer_label": "繪圖套件 / 格式",

            "wow_status": "代理執行狀態",

            "metrics_title": "流程圖概況",

            "nodes": "節點數",

            "edges": "連線數",

            "complexity": "複雜度",

            "spec_tab": "JSON 規格",

            "dot_tab": "Graphviz DOT 原始碼",

            "mermaid_tab": "Mermaid 程式碼",

            "image_tab": "流程圖預覽",

        }

    else:

        return {

            "title": "Agentic AI Flowchart Generator & Editor",

            "description": "Turn text into styled flowcharts with AI agents, live editing, and downloads.",

            "input_label": "Process / project description",

            "generate_button": "Generate flowchart spec",

            "preview_button": "Apply edits & preview flowchart",

            "download_button": "Download flowchart image",

            "provider_label": "Model provider",

            "model_label": "Model",

            "prompt_label": "Advanced system prompt (editable)",

            "max_tokens": "Max tokens",

            "theme": "Theme",

            "flower_style": "Flower style",

            "language_label": "Flowchart language",

            "renderer_label": "Renderer / format",

            "wow_status": "Agent pipeline status",

            "metrics_title": "Flowchart metrics",

            "nodes": "Nodes",

            "edges": "Edges",

            "complexity": "Complexity",

            "spec_tab": "JSON spec",

            "dot_tab": "Graphviz DOT",

            "mermaid_tab": "Mermaid code",

            "image_tab": "Diagram preview",

        }





def init_session_state():

    if "flow_spec" not in st.session_state:

        st.session_state.flow_spec = None

    if "dot_source" not in st.session_state:

        st.session_state.dot_source = ""

    if "png_bytes" not in st.session_state:

        st.session_state.png_bytes = None

    if "mermaid_code" not in st.session_state:

        st.session_state.mermaid_code = ""

    if "user_api_keys" not in st.session_state:

        st.session_state.user_api_keys = {}





def main():

    init_session_state()



    # Top-level layout

    st.set_page_config(page_title="Agentic Flowchart Generator", layout="wide")



    # Language & theme selectors (top bar)

    col_top1, col_top2, col_top3 = st.columns([1, 1, 2])

    with col_top1:

        language = st.selectbox("UI / flowchart language", ["en", "zh"], index=0)

    texts = get_localized_texts(language)



    with col_top2:

        theme = st.radio(texts["theme"], ["light", "dark"], index=0, horizontal=True)



    with col_top3:

        flower_style = st.selectbox(texts["flower_style"], FLOWER_STYLE_NAMES, index=0)



    st.title(texts["title"])

    st.write(texts["description"])



    # Sidebar: model / provider / prompt / tokens

    with st.sidebar:

        st.header("LLM & Agent Settings")



        provider = st.selectbox(

            texts["provider_label"],

            ["Gemini", "OpenAI / OPENAAI", "Grok"],

        )



        if provider == "Gemini":

            model = st.selectbox(

                texts["model_label"],

                ["gemini-2.5-flash", "gemini-2.5-flash-lite"],

            )

            env_key = os.getenv("GEMINI_API_KEY")

            if env_key:

                st.success("Using GEMINI_API_KEY from environment.")

                api_key = env_key

            else:

                api_key = st.text_input("Gemini API key", type="password")

                st.session_state.user_api_keys["gemini"] = api_key



        elif provider == "OpenAI / OPENAAI":

            model = st.selectbox(

                texts["model_label"],

                ["gpt-5-nano", "gpt-4o-mini", "gpt-4.1-mini"],

            )

            env_key = os.getenv("OPENAAI_API_KEY") or os.getenv("OPENAI_API_KEY")

            if env_key:

                st.success("Using OPENAAI_API_KEY / OPENAI_API_KEY from environment.")

                api_key = env_key

            else:

                api_key = st.text_input("OPENAI/OPENAAI API key", type="password")

                st.session_state.user_api_keys["openai"] = api_key



        else:  # Grok

            model = st.selectbox(

                texts["model_label"],

                ["grok-4-fast-reaoning", "grok-3-mini"],

                help="Behind the scenes, 'grok-4-fast-reaoning' will use 'grok-4' model ID.",

            )

            # Map UI label to actual xAI model ids

            model_map = {

                "grok-4-fast-reaoning": "grok-4",

                "grok-3-mini": "grok-3-mini",

            }

            model = model_map[model]

            env_key = os.getenv("XAI_API_KEY")

            if env_key:

                st.success("Using XAI_API_KEY from environment.")

                api_key = env_key

            else:

                api_key = st.text_input("Grok (xAI) API key", type="password")

                st.session_state.user_api_keys["grok"] = api_key



        max_tokens = st.slider(texts["max_tokens"], min_value=256, max_value=4096, value=1024, step=128)



        st.markdown("---")

        show_prompt = st.checkbox("Show / edit advanced system prompt", value=True)

        if show_prompt:

            system_prompt = st.text_area(

                texts["prompt_label"],

                value=DEFAULT_SYSTEM_PROMPT,

                height=280,

            )

        else:

            system_prompt = DEFAULT_SYSTEM_PROMPT



    # Main layout: left = input + editing; right = preview / dashboard

    col_left, col_right = st.columns([1.1, 1.3])



    with col_left:

        st.subheader("1. " + texts["input_label"])

        user_description = st.text_area(

            "",

            height=200,

            placeholder=(

                "Describe your process here (e.g., international medical device UDI regulation "

                "comparison and reporting workflow)..."

                if language == "en"

                else "請輸入您要繪製的流程（例如：國際醫療器材 UDI 法規比較與報告流程）..."

            ),

        )



        renderer = st.selectbox(

            texts["renderer_label"],

            ["Graphviz (PNG)", "Mermaid (text only)"],

        )



        generate_clicked = st.button(texts["generate_button"], type="primary")



        if generate_clicked:

            if not api_key:

                st.error("Please provide an API key or configure it in the environment.")

            elif not user_description.strip():

                st.error("Please provide a description of the process.")

            else:

                runtime_hint = (

                    f"User-selected language code: {language}. "

                    f"Base theme: {theme}. Flower style: {flower_style}. "

                    "You only handle structure and labels; styling is handled by the renderer."

                )

                full_system_prompt = system_prompt + "\n\n" + runtime_hint



                with st.status(texts["wow_status"], expanded=True) as status:

                    status.write("Step 1/2: Calling LLM agent to design flowchart...")

                    try:

                        response_text = call_llm(

                            provider=provider,

                            model=model,

                            system_prompt=full_system_prompt,

                            user_prompt=user_description,

                            max_tokens=max_tokens,

                            api_key=api_key,

                        )

                        status.update(label="Step 2/2: Parsing JSON and building spec...", state="running")

                        spec = extract_json_from_text(response_text)

                        st.session_state.flow_spec = spec



                        # Build initial render

                        if renderer.startswith("Graphviz"):

                            dot = build_graphviz_from_spec(spec, theme=theme, flower_style=flower_style)

                            png_bytes = dot.pipe(format="png")

                            st.session_state.dot_source = dot.source

                            st.session_state.png_bytes = png_bytes

                        else:

                            mermaid_code = build_mermaid_from_spec(spec)

                            st.session_state.mermaid_code = mermaid_code



                        status.update(label="Agent pipeline complete.", state="complete")

                    except Exception as e:

                        status.update(label="Error during agent pipeline.", state="error")

                        st.error(str(e))



        # Editing UI (nodes / edges) once we have a spec

        spec = st.session_state.flow_spec

        if spec:

            st.subheader("2. Edit nodes & edges")



            nodes_df = pd.DataFrame(spec.get("nodes", []))

            edges_df = pd.DataFrame(spec.get("edges", []))



            st.markdown("**Nodes**")

            edited_nodes_df = st.data_editor(

                nodes_df,

                num_rows="dynamic",

                key="nodes_editor",

                use_container_width=True,

            )



            st.markdown("**Edges**")

            edited_edges_df = st.data_editor(

                edges_df,

                num_rows="dynamic",

                key="edges_editor",

                use_container_width=True,

            )



            if st.button(texts["preview_button"]):

                spec["nodes"] = edited_nodes_df.to_dict(orient="records")

                spec["edges"] = edited_edges_df.to_dict(orient="records")

                st.session_state.flow_spec = spec



                if renderer.startswith("Graphviz"):

                    dot = build_graphviz_from_spec(spec, theme=theme, flower_style=flower_style)

                    st.session_state.dot_source = dot.source

                    st.session_state.png_bytes = dot.pipe(format="png")

                else:

                    st.session_state.mermaid_code = build_mermaid_from_spec(spec)



    with col_right:

        st.subheader("3. " + texts["metrics_title"])



        spec = st.session_state.flow_spec

        if spec:

            n_nodes = len(spec.get("nodes", []))

            n_edges = len(spec.get("edges", []))

            if n_nodes <= 5:

                complexity = "Very Low" if language == "en" else "非常低"

            elif n_nodes <= 15:

                complexity = "Moderate" if language == "en" else "中等"

            elif n_nodes <= 30:

                complexity = "High" if language == "en" else "高"

            else:

                complexity = "Very High" if language == "en" else "非常高"



            m1, m2, m3 = st.columns(3)

            m1.metric(texts["nodes"], n_nodes)

            m2.metric(texts["edges"], n_edges)

            m3.metric(texts["complexity"], complexity)



        tabs = st.tabs([texts["image_tab"], texts["spec_tab"], texts["dot_tab"], texts["mermaid_tab"]])



        with tabs[0]:  # Diagram preview

            if renderer.startswith("Graphviz"):

                if st.session_state.png_bytes:

                    st.image(st.session_state.png_bytes, use_column_width=True)

                    st.download_button(

                        label=texts["download_button"],

                        data=st.session_state.png_bytes,

                        file_name="flowchart.png",

                        mime="image/png",

                    )

                else:

                    st.info("Generate a flowchart spec to see the preview.")

            else:

                st.info("Mermaid renderer is text-only in this demo; copy the code from the Mermaid tab into a Mermaid viewer.")



        with tabs[1]:  # JSON spec

            if spec:

                st.code(json.dumps(spec, ensure_ascii=False, indent=2), language="json")

            else:

                st.info("No spec yet. Generate a flowchart first.")



        with tabs[2]:  # Graphviz DOT

            if st.session_state.dot_source:

                st.code(st.session_state.dot_source, language="dot")

            else:

                st.info("No Graphviz diagram generated yet.")



        with tabs[3]:  # Mermaid

            if st.session_state.mermaid_code:

                st.code(st.session_state.mermaid_code, language="markdown")

            else:

                st.info("No Mermaid code yet. Switch renderer to Mermaid and generate/preview.")





if __name__ == "__main__":

    main()

```



Notes:



- Graphviz is used as the primary renderer (image output + download).

- Mermaid output is provided as text; you can later integrate a JS viewer or another library if desired.

- Users can:

  - choose provider/model,

  - override the advanced system prompt,

  - set max tokens,

  - toggle light/dark and 20 flower styles,

  - edit nodes/edges via `st.data_editor`,

  - preview and download PNG.



---



## 4. 20 comprehensive follow‑up questions



1. Do you want the advanced system prompt to vary automatically depending on the chosen provider/model (e.g., slightly different instructions for Grok vs Gemini) or keep a single unified prompt for all models?  

2. Should the language setting control only the flowchart labels and title, or also fully localize the entire Streamlit UI (including error messages and sidebar labels) into Chinese?  

3. For the 20 flower themes, would you like additional fine‑tuning controls in the UI (e.g., sliders for saturation/contrast, custom accent color overrides) beyond the presets?  

4. Do you want the flowchart direction (`TB`, `LR`, etc.) to be user‑selectable in the UI, or should it always be inferred/decided by the LLM from the description?  

5. Would you like a “layout mode” selector (e.g., linear, hierarchical, swimlane) that the LLM should consider when constructing the JSON spec?  

6. Should the user be able to save and load flowchart JSON specs (e.g., as `.json` files) so they can resume editing later within the app?  

7. Are you interested in supporting multiple flowcharts in a single session (e.g., tabs or a gallery of generated diagrams) rather than only the most recent one?  

8. Do you want to add role-specific constraints, such as “regulatory research”, “clinical workflow”, or “software architecture”, that change how the LLM structures the flowchart?  

9. For Grok usage, do you need image-based flowchart generation (user uploads an existing diagram image and asks the system to reconstruct or extend it), leveraging the xAI image APIs?  

10. Should the app log anonymized metrics (e.g., number of nodes, edges, generation time, model used) for later analysis, or must it avoid all server-side logging for privacy?  

11. Would you like the editing UI to support drag-and-drop reordering or grouping of nodes (e.g., by phase) instead of just tabular editing via `st.data_editor`?  

12. Are there any specific compliance or security requirements for handling user-provided API keys in the UI (e.g., encryption at rest, strict session cleanup) that we should incorporate?  

13. Should the system detect and warn about potential logical issues in the flowchart (e.g., unreachable nodes, cycles where not expected, missing end nodes) using an additional validation step/agent?  

14. Would you like integration with Hugging Face Agents (or Tools) beyond the `agents.yaml` description, for example running the architect agent via an HF-hosted LLM instead of external APIs?  

15. Do you want to support custom node icons or emojis (for certain categories like “database”, “API”, “user”) or keep all nodes pure text for maximal portability?  

16. Should the “wow status indicators” also include timing information (e.g., how long each step of the agent pipeline took) and display performance statistics over multiple runs?  

17. Are you interested in adding a “comparison view” that shows the original LLM-generated spec side-by-side with the manually edited spec, highlighting the differences?  

18. Would you like the system to auto-generate a short textual summary or narrative explanation of the final flowchart for documentation purposes (possibly as a second LLM call)?  

19. Do you need export formats beyond PNG and Mermaid text (e.g., SVG, PDF, or direct PowerPoint/Keynote slide snippets) for your downstream workflows?  

20. Are there specific domain templates (e.g., “international medical device UDI research pipeline”) you want pre-configured so users can start from an example and then customize instead of always starting from scratch?
