import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import json
import math
import re
from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape

# ==============================================================================
# 1. PAGE CONFIGURATION & MODERN DARK GLASSMORPHISM STYLING
# ==============================================================================
st.set_page_config(
    page_title="Thought Sweep | Research & Marketing Strategy Engine",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for high-end dark glassmorphism styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c20 0%, #150d2a 50%, #0d0818 100%);
        color: #f1f5f9;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #a78bfa 0%, #c084fc 50%, #e879f9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #94a3b8;
        font-size: 1.0rem;
        margin-bottom: 1.5rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(22, 14, 38, 0.7);
        padding: 8px 12px;
        border-radius: 12px;
        border: 1px solid rgba(167, 139, 250, 0.15);
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        white-space: pre;
        border-radius: 8px;
        color: #cbd5e1;
        font-weight: 600;
        padding: 0px 16px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7c3aed 0%, #9333ea 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
    }
    .glass-card {
        background: rgba(22, 14, 38, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(167, 139, 250, 0.15);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .quad-card {
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(167, 139, 250, 0.2);
    }
    .stButton>button {
        background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #6d28d9 0%, #8b5cf6 100%);
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.4);
        color: white;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: rgba(15, 10, 28, 0.8) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(167, 139, 250, 0.25) !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. FULL CODEBOOK VERSION 0.3 INITIALIZATION (42 PREDEFINED CODES)
# ==============================================================================
def get_full_codebook_v03():
    return [
        # --- CHALLENGE CODES (C) ---
        {"id": "C1", "name": "Lack of ideas", "category": "Challenge Codes (C)", "desc": "Being unable to find or choose a topic or direction, or running out of ideas partway through.", "how_to_apply": "Do NOT code if they have an idea but cannot shape it (use C2), or have too many ideas and feel swamped (use C7)."},
        {"id": "C2", "name": "Idea-to-plan difficulty", "category": "Challenge Codes (C)", "desc": "Having an idea but being unable to narrow it into a research question, scope or plan.", "how_to_apply": "Do NOT code if there is no idea at all (use C1), or a plan exists but is not being carried out (use C5, C6)."},
        {"id": "C3", "name": "Organizing thoughts and sources", "category": "Challenge Codes (C)", "desc": "Notes, sources or drafts that were kept but are scattered, unstructured or hard to find.", "how_to_apply": "Do NOT code if the material was never captured or was forgotten (use C4), or participant feels overwhelmed (use C7)."},
        {"id": "C4", "name": "Idea loss", "category": "Challenge Codes (C)", "desc": "Forgetting, never recording or never revisiting spontaneous ideas.", "how_to_apply": "Do NOT code if the idea was recorded but cannot be found (use C3)."},
        {"id": "C5", "name": "Time management", "category": "Challenge Codes (C)", "desc": "Misjudging how long work takes, scheduling or pacing it, or balancing it against other academic commitments.", "how_to_apply": "Do NOT code if they say they chose to delay (use C6), or work/health/family demands took time (use E5)."},
        {"id": "C6", "name": "Procrastination", "category": "Challenge Codes (C)", "desc": "Knowingly putting off or avoiding thesis work.", "how_to_apply": "Do NOT code if delay came from time genuinely unavailable (use C5) or from not knowing how to proceed (use C2)."},
        {"id": "C7", "name": "Cognitive overwhelm", "category": "Challenge Codes (C)", "desc": "Feeling flooded, frozen or unsure where to start because of the volume or complexity of the work.", "how_to_apply": "Do NOT code if no feeling of overload is described, only a missing system (use C3) or forgotten idea (use C4)."},
        {"id": "C8", "name": "No difficulty or what worked", "category": "Challenge Codes (C)", "desc": "A stage, system or habit that went well, or an expected problem that did not occur.", "how_to_apply": "If the main point is a difficulty, code difficulty as primary and add C8 as secondary only if they state how they overcame it."},

        # --- TOOLS USED (T) ---
        {"id": "T1", "name": "Digital notes", "category": "Tools Used (T)", "desc": "Notes apps, phone notes, Notion, Obsidian, OneNote.", "how_to_apply": "Code when participant explicitly mentions digital note-taking apps."},
        {"id": "T2", "name": "Paper", "category": "Tools Used (T)", "desc": "Notebooks, sticky notes, printed pages, index cards.", "how_to_apply": "Code when physical/paper note systems are mentioned."},
        {"id": "T3", "name": "Voice or message to self", "category": "Tools Used (T)", "desc": "Voice memos, texting or emailing themselves.", "how_to_apply": "Code when audio recording or self-messaging is mentioned."},
        {"id": "T4", "name": "Reference manager", "category": "Tools Used (T)", "desc": "Zotero, Mendeley, EndNote, or a spreadsheet of sources.", "how_to_apply": "Code when bibliographic/citation tracking tools are named."},
        {"id": "T5", "name": "Cloud documents", "category": "Tools Used (T)", "desc": "Google Docs, Drive folders, Word files.", "how_to_apply": "Code when word processors or cloud storage drives are mentioned."},
        {"id": "T6", "name": "Visual mapping", "category": "Tools Used (T)", "desc": "Mind maps, whiteboards, concept diagrams.", "how_to_apply": "Code when visual brainstorming tools are mentioned."},
        {"id": "T7", "name": "Task or calendar tool", "category": "Tools Used (T)", "desc": "To-do apps, planners, calendar blocking.", "how_to_apply": "Code when scheduling, task managers, or calendars are mentioned."},
        {"id": "T8", "name": "AI tool", "category": "Tools Used (T)", "desc": "Chatbots or AI writing and brainstorming tools.", "how_to_apply": "Code when generative AI or AI assistants are named."},
        {"id": "T9", "name": "No system", "category": "Tools Used (T)", "desc": "They explicitly say they have no method.", "how_to_apply": "Code when participant explicitly states they lack any system or method."},
        {"id": "T10", "name": "Other tool", "category": "Tools Used (T)", "desc": "Any tool not listed (write a short note).", "how_to_apply": "Code for any uncategorized tool and write a short explanatory note."},

        # --- TOOL EVALUATION: REASONS CHOSEN (R) ---
        {"id": "R1", "name": "Chosen: fast or convenient", "category": "Tool Evaluation - Chosen (R)", "desc": "Chosen because it was quick to use or easy to reach.", "how_to_apply": "Attach to the specific tool it concerns."},
        {"id": "R2", "name": "Chosen: free or pre-installed", "category": "Tool Evaluation - Chosen (R)", "desc": "Chosen because it cost nothing or came with device/school account.", "how_to_apply": "Attach to the specific tool it concerns."},
        {"id": "R3", "name": "Chosen: recommended", "category": "Tool Evaluation - Chosen (R)", "desc": "Chosen because someone suggested it.", "how_to_apply": "Attach to the specific tool it concerns."},
        {"id": "R4", "name": "Chosen: habit", "category": "Tool Evaluation - Chosen (R)", "desc": "Chosen because they already used it for other things.", "how_to_apply": "Attach to the specific tool it concerns."},

        # --- TOOL EVALUATION: REASONS DROPPED/DISLIKED (A) ---
        {"id": "A1", "name": "Dropped: slow to capture", "category": "Tool Evaluation - Dropped (A)", "desc": "Dropped/disliked because it took too long to get an idea down.", "how_to_apply": "Attach to the specific tool it concerns."},
        {"id": "A2", "name": "Dropped: hard to find later", "category": "Tool Evaluation - Dropped (A)", "desc": "Dropped/disliked because they could not find things again.", "how_to_apply": "Attach to the specific tool it concerns."},
        {"id": "A3", "name": "Dropped: old ideas never resurface", "category": "Tool Evaluation - Dropped (A)", "desc": "Dropped/disliked because they never saw or revisited what they saved.", "how_to_apply": "Attach to the specific tool it concerns."},
        {"id": "A4", "name": "Dropped: not linked to tasks", "category": "Tool Evaluation - Dropped (A)", "desc": "Dropped/disliked because it did not connect to deadlines or tasks.", "how_to_apply": "Attach to the specific tool it concerns."},
        {"id": "A5", "name": "Dropped: too complex", "category": "Tool Evaluation - Dropped (A)", "desc": "Dropped/disliked because it was too complicated, or they juggled too many tools.", "how_to_apply": "Attach to the specific tool it concerns."},
        {"id": "A6", "name": "Dropped: other reason", "category": "Tool Evaluation - Dropped (A)", "desc": "Any other stated reason for dropping or disliking a tool.", "how_to_apply": "Attach to the specific tool it concerns and write a short note."},

        # --- CAPABILITIES WANTED (W) ---
        {"id": "W1", "name": "Faster capture", "category": "Capabilities Wanted (W)", "desc": "Wishes for getting an idea down quickly, anywhere.", "how_to_apply": "Student transcripts only. Code when a missing wish/capability is expressed."},
        {"id": "W2", "name": "Reminders of old ideas", "category": "Capabilities Wanted (W)", "desc": "Wishes for being reminded of ideas they had before.", "how_to_apply": "Student transcripts only. Code when a missing wish/capability is expressed."},
        {"id": "W3", "name": "Better organization or linking", "category": "Capabilities Wanted (W)", "desc": "Wishes for sorting, grouping or connecting notes and ideas.", "how_to_apply": "Student transcripts only. Code when a missing wish/capability is expressed."},
        {"id": "W4", "name": "Turning ideas into tasks", "category": "Capabilities Wanted (W)", "desc": "Wishes for moving from an idea to a to-do, deadline or plan.", "how_to_apply": "Student transcripts only. Code when a missing wish/capability is expressed."},
        {"id": "W5", "name": "Help expanding ideas", "category": "Capabilities Wanted (W)", "desc": "Wishes for support in developing or building on an idea.", "how_to_apply": "Student transcripts only. Code when a missing wish/capability is expressed."},
        {"id": "W6", "name": "Other capability", "category": "Capabilities Wanted (W)", "desc": "Any other stated want or missing capability.", "how_to_apply": "Student transcripts only. Write a short explanatory note."},

        # --- CAPTURE CONTEXT (X) ---
        {"id": "X1", "name": "Away from desk", "category": "Capture Context (X)", "desc": "Idea came while walking, commuting, exercising or doing something unrelated.", "how_to_apply": "Student transcripts only. Apply to specific moment an idea arose."},
        {"id": "X2", "name": "While reading or researching", "category": "Capture Context (X)", "desc": "Idea came during reading, searching or reviewing sources.", "how_to_apply": "Student transcripts only. Apply to specific moment an idea arose."},
        {"id": "X3", "name": "In class or meetings", "category": "Capture Context (X)", "desc": "Idea came during a class, a talk or a meeting.", "how_to_apply": "Student transcripts only. Apply to specific moment an idea arose."},
        {"id": "X4", "name": "Late night or while resting", "category": "Capture Context (X)", "desc": "Idea came while falling asleep, waking up or in the shower.", "how_to_apply": "Student transcripts only. Apply to specific moment an idea arose."},
        {"id": "X5", "name": "At a desk working", "category": "Capture Context (X)", "desc": "Idea came while actively working on the thesis.", "how_to_apply": "Student transcripts only. Apply to specific moment an idea arose."},
        {"id": "X6", "name": "Other context", "category": "Capture Context (X)", "desc": "Any other setting where an idea arose.", "how_to_apply": "Student transcripts only. Write a short note."},

        # --- DEVELOPING IDEAS (D) ---
        {"id": "D1", "name": "Advisor or committee meetings", "category": "Developing Ideas (D)", "desc": "Using meetings to shape or expand ideas.", "how_to_apply": "Code method participant names to turn ideas into a finished thesis."},
        {"id": "D2", "name": "Peer discussion", "category": "Developing Ideas (D)", "desc": "Talking ideas through with classmates or friends.", "how_to_apply": "Code method participant names to turn ideas into a finished thesis."},
        {"id": "D3", "name": "Writing to think", "category": "Developing Ideas (D)", "desc": "Free-writing or drafting early to find the idea.", "how_to_apply": "Code method participant names to turn ideas into a finished thesis."},
        {"id": "D4", "name": "Software support", "category": "Developing Ideas (D)", "desc": "Using software to expand, outline or structure ideas.", "how_to_apply": "Code method participant names to turn ideas into a finished thesis."},
        {"id": "D5", "name": "Other method", "category": "Developing Ideas (D)", "desc": "Any other way of developing ideas.", "how_to_apply": "Code method participant names and write a short note."},

        # --- CHANNELS / WHERE THEY HEAR ABOUT TOOLS (CH) ---
        {"id": "CH1", "name": "Peers", "category": "Where Heard About Tools (CH)", "desc": "Hearing about tools from classmates or friends.", "how_to_apply": "Code source named; do not infer channel from tool chosen."},
        {"id": "CH2", "name": "Faculty or advisors", "category": "Where Heard About Tools (CH)", "desc": "Recommendations from faculty or thesis advisors.", "how_to_apply": "Code source named; do not infer channel from tool chosen."},
        {"id": "CH3", "name": "Barrett or ASU channels", "category": "Where Heard About Tools (CH)", "desc": "Emails, workshops, honors communications, library or writing center.", "how_to_apply": "Code source named; do not infer channel from tool chosen."},
        {"id": "CH4", "name": "Online and social media", "category": "Where Heard About Tools (CH)", "desc": "Social platforms, video sites, forums or search.", "how_to_apply": "Code source named; do not infer channel from tool chosen."},
        {"id": "CH5", "name": "Other channel", "category": "Where Heard About Tools (CH)", "desc": "Any other source of tool information.", "how_to_apply": "Code source named and write a short note."},

        # --- EXTERNAL CODES (E) ---
        {"id": "E1", "name": "Advisor relationship", "category": "External Codes (E)", "desc": "A hard-to-reach advisor, mismatched expectations or unclear feedback.", "how_to_apply": "Do NOT code if confusion is about Barrett or department rules (use E3)."},
        {"id": "E2", "name": "Access to resources", "category": "External Codes (E)", "desc": "No access to data, lab time, equipment, participants, archives or software.", "how_to_apply": "Do NOT code if they had access but lacked skill to use it (use E4)."},
        {"id": "E3", "name": "Unclear requirements", "category": "External Codes (E)", "desc": "Confusion about Barrett or departmental thesis rules, formats, deadlines or milestones.", "how_to_apply": "Do NOT code if unclear part is advisor's feedback (use E1)."},
        {"id": "E4", "name": "Skill gap", "category": "External Codes (E)", "desc": "Lacking a specific method, writing or technical skill the project needs.", "how_to_apply": "Do NOT code if problem is planning or scoping the project (use C2)."},
        {"id": "E5", "name": "Life circumstances", "category": "External Codes (E)", "desc": "Work, health, finances or family demands outside school crowding out thesis time.", "how_to_apply": "Do NOT code if time pressure came from coursework or thesis scheduling (use C5)."}
    ]

def init_session_state():
    default_stages = [
        "Topic Selection / Ideation", "Proposal & Scoping", "Literature Review",
        "Data Collection / Execution", "Analysis & Synthesis", "Drafting & Writing"
    ]
    if "final_stages" not in st.session_state and st.session_state.get("stage_definitions"):
        st.session_state["final_stages"] = list(st.session_state["stage_definitions"])

    defaults = {
        "step1_interviews": [],
        "step2_interviews": [],
        "step3_interviews": [],
        "stage_definitions": {},
        "final_stages": default_stages,
        "edit_final_stages": False,
        "stage_walkthrough_ui": {},
        "codebook": get_full_codebook_v03(),
        "coder_a_annotations": [],
        "coder_b_annotations": [],
        "kappa_locked": False,
        "kappa_value": 0.0,
        "surveys": []
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session_state()

def export_all_data():
    data = {
        "stage_definitions": st.session_state.stage_definitions,
        "final_stages": st.session_state.final_stages,
        "step1_interviews": st.session_state.step1_interviews,
        "step2_interviews": st.session_state.step2_interviews,
        "step3_interviews": st.session_state.step3_interviews,
        "codebook": st.session_state.codebook,
        "coder_a_annotations": st.session_state.coder_a_annotations,
        "coder_b_annotations": st.session_state.coder_b_annotations,
        "kappa_locked": st.session_state.kappa_locked,
        "kappa_value": st.session_state.kappa_value,
        "surveys": st.session_state.surveys
    }
    return json.dumps(data, indent=2)

def import_all_data(uploaded_json):
    try:
        data = json.load(uploaded_json)
        for key, value in data.items():
            st.session_state[key] = value
        if "final_stages" not in data and data.get("stage_definitions"):
            st.session_state.final_stages = list(data["stage_definitions"])
        for stage_number in range(1, 7):
            st.session_state.pop(f"final_stage_edit_{stage_number}", None)
            st.session_state.pop(f"final_stage_definition_edit_{stage_number}", None)
        return True
    except Exception as e:
        st.error(f"Failed to parse JSON file: {e}")
        return False

def clear_all_data():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_session_state()
    st.rerun()

def save_stage_response(interviews, interview_id, group, discipline, stage, responses):
    interview_id = interview_id.strip()
    interview = next((item for item in interviews if item["id"] == interview_id), None)
    if interview is None:
        interview = {
            "id": interview_id,
            "group": group,
            "discipline": discipline,
            "stage_responses": []
        }
        interviews.append(interview)
    else:
        interview["group"] = group
        interview["discipline"] = discipline

    stage_responses = interview.setdefault("stage_responses", [])
    saved_stage = {"stage": stage, "responses": responses}
    existing = next((item for item in stage_responses if item["stage"] == stage), None)
    if existing is None:
        stage_responses.append(saved_stage)
    else:
        existing.update(saved_stage)

def upsert_interview(interviews, entry):
    existing = next((item for item in interviews if item["id"] == entry["id"]), None)
    if existing is None:
        interviews.append(entry)
    else:
        existing.update(entry)

def build_transcript_questions(interview, source):
    prompts = {
        "Step 1": [
            ("a1", "A1. From beginning to end, what are the main areas/phases a student goes through?"),
            ("a2", "A2. What do you call each of these? Is there a name you/your department use?"),
            ("a3", "A3. In what order do students usually move through them?"),
            ("a4", "A4. Is there anything before the first or after the last area we should include?"),
            ("a5", "A5. (Read list back) Does this match how you see the process? What would you change?"),
            ("a6", "A6. Is this list the same for every thesis in your discipline or does it change?"),
            ("b1", "B1. What is [STAGE]? How would you explain it to a new student?"),
            ("b2", "B2. What does a student actually do during [STAGE]?"),
            ("b3", "B3. What does a student have to complete, produce, or have approved?"),
            ("b4", "B4. Which requirements are set officially (Barrett/college) vs advisor/discipline?"),
            ("b5", "B5. How do you know when a student is ready to move on from [STAGE]?"),
            ("b6", "B6. What does a student need to have in place before beginning [STAGE]?"),
            ("b7", "B7. Who is involved in [STAGE], and what does each person do?"),
            ("b8", "B8. How long does [STAGE] take, and where does it fall on the timeline?"),
            ("b9", "B9. What changes about [STAGE] from one project/discipline to another?"),
            ("c1", "C1. Are there areas that overlap or blur together? How do you tell where one ends?"),
            ("c2", "C2. Are there areas that some students skip, combine, or repeat?"),
            ("c3", "C3. Are there official milestones, forms, or deadlines every student must meet?"),
            ("c4", "C4. Is there anything about how the thesis process works that we missed?"),
            ("c5", "C5. Who else should we speak with?")
        ],
        "Step 2": [
            ("a2", "A2. Is there anything about these stages or definitions that is unclear?"),
            ("a3", "A3. Is there any stage you think of differently from how it is defined here?"),
            ("c2", "C2. Why do you think students struggle the most at {stage}?"),
            ("c3", "C3. What does that struggle look like when it is happening?"),
            ("c4", "C4. Can you walk me through a specific example, without naming the student?"),
            ("c5", "C5. What do you notice about students who get through with less struggle?"),
            ("d1", "D1. How do you see students come up with their ideas and keep track of them?"),
            ("d2", "D2. What tools, systems, or methods have you seen students use to track work?"),
            ("d3", "D3. What have you noticed about how well those work for students?"),
            ("d4", "D4. When a student is stuck, what do you suggest and where do you send them?"),
            ("d6", "D6. Is there anything else about what students go through that we missed?")
        ],
        "Step 3": [
            ("01", "01. In a sentence or two, what is your thesis about?"),
            ("02", "02. About how long have you been working on your thesis?"),
            ("03", "03. Is there anything on the stage card that is unclear?"),
            ("04", "04. Which stages have you finished, and which one are you in now?"),
            ("q_11", "11. Where did your thesis idea come from? Walk me through how you first came up with it."),
            ("q_12", "12. Tell me about any other ideas you considered before your current one. What happened to them?"),
            ("q_13", "13. Think about the most recent time a new thesis idea came to you. Where were you & doing?"),
            ("q_14", "14. What was the first thing you did with that idea?"),
            ("q_15", "15. What happened to that idea afterward?"),
            ("q_16", "16. Last time you needed something saved earlier (note, source, idea), what happened?"),
            ("q_17", "17. Walk me through the steps between that first idea and having a plan to work from."),
            ("q_18", "18. Was there a point on the way from idea to plan where you were unsure what to do next?"),
            ("q_19", "19. Walk me through how one part went from an idea to what you have now (deliverable)."),
            ("q_110", "110 (Optional). Last idea that turned into something you had to do (task/deadline)?"),
            ("h1", "H1. What has been the most difficult challenge you have faced with your thesis so far?"),
            ("h3", "H3. What made that so difficult?"),
            ("h4", "H4. What did that look like day to day? What were you doing, or not doing?"),
            ("h5", "H5. How did you get through it, or are you still working through it? What helped?"),
            ("u1", "U1. Last time you wrote down or recorded an idea for your thesis, what did you use?"),
            ("u2", "U2. Where do your thesis notes, readings, and sources live right now? List every place."),
            ("u3", "U3. How did you start using each tool/place? Who/what made you choose it?"),
            ("u4", "U4. What works well about using it, and what is frustrating about it?"),
            ("u5", "U5. Have you stopped using any app, notebook, or method you started out with? Why?"),
            ("u6", "U6. What do you use to turn ideas into your final project (outline, draft, plan)?"),
            ("u7", "U7. Is there anything you do by hand or work around because a tool doesn't do it?"),
            ("u8", "U8. Thinking about the last time you did that workaround, what were you trying to get done?"),
            ("u9", "U9 (Optional). Would you change anything about how you handle notes/ideas weekly?"),
            ("s1", "S1. When in your thesis did you most wish you had more help? What kind of help?"),
            ("s2", "S2. When you have had a question about your thesis, who did you go to?"),
            ("s3", "S3. Where do you usually go to find out about resources/tools? Whose advice do you trust?"),
            ("s4", "S4. Is there anything that made your thesis easier or harder that we haven't talked about?")
        ]
    }

    questions = []
    for field, prompt in prompts.get(source, []):
        answer = str(interview.get(field, "")).strip()
        if answer:
            questions.append({"stage": interview.get("hardest_stage", ""), "question": prompt.format(stage=interview.get("hardest_stage", "the selected stage")), "answer": answer})

    stage_questions = {
        "Step 2": [
            "B1. What struggles do you observe at {stage}?",
            "B2. What does that look like in practice at {stage}? What do you see students doing or not doing?",
            "B3. Can you describe a recent example of a struggle at {stage}, without naming the student?",
            "B4. What do students do when this happens during {stage}?",
            "B5. What do you think is going on when students struggle during {stage}?",
            "B6. How common is this among the students you have advised during {stage}?",
            "B7. What have you seen students do that helps them through {stage}?",
            "B8. Does what you see at {stage} change with project type or discipline?"
        ],
        "Step 3": [
            "B1. Walk me through what you did during {stage}, starting with the first thing.",
            "B2. Think of a moment during {stage} when something didn't go as expected. What happened?",
            "B3. What did you do when that happened during {stage}?",
            "B4. What do you think was going on at that point in {stage}?",
            "B5. What part of {stage} went more smoothly than expected? What helped?",
            "B6. Was anyone else involved in {stage}? What did they do? (Optional)",
            "B7. If doing {stage} again, what would you do differently? (Optional)"
        ]
    }
    for stage_entry in interview.get("stage_responses", []):
        stage = stage_entry.get("stage", "")
        answers = stage_entry.get("responses", {})
        for question_number, prompt in enumerate(stage_questions.get(source, []), 1):
            answer = str(answers.get(f"B{question_number}", "")).strip()
            if answer:
                questions.append({
                    "stage": stage,
                    "question": prompt.format(stage=stage),
                    "answer": answer
                })

    legacy_questions = stage_questions.get(source, [])
    if legacy_questions and not interview.get("stage_responses"):
        legacy_stage = interview.get("hardest_stage", "")
        for question_number, prompt in enumerate(legacy_questions, 1):
            answer = str(interview.get(f"b{question_number}", "")).strip()
            if answer:
                questions.append({
                    "stage": legacy_stage,
                    "question": prompt.format(stage=legacy_stage),
                    "answer": answer
                })
    return questions

def create_transcript_pdf(step_name, interview_id, questions):
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

    font_path = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    if font_path.exists() and "ThoughtSweepSans" not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont("ThoughtSweepSans", str(font_path)))
        font_name = "ThoughtSweepSans"
    else:
        font_name = "Helvetica"

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="TranscriptTitle",
        parent=styles["Title"],
        fontName=font_name,
        fontSize=18,
        leading=23,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#16324F"),
        spaceAfter=12
    ))
    styles.add(ParagraphStyle(
        name="TranscriptQuestion",
        parent=styles["Heading3"],
        fontName=font_name,
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#16324F"),
        spaceBefore=12,
        spaceAfter=5
    ))
    styles.add(ParagraphStyle(
        name="TranscriptBody",
        parent=styles["BodyText"],
        fontName=font_name,
        fontSize=10,
        leading=14,
        spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        name="TranscriptStage",
        parent=styles["Heading2"],
        fontName=font_name,
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#237A72"),
        spaceBefore=12,
        spaceAfter=7
    ))

    buffer = BytesIO()
    document = SimpleDocTemplate(buffer, pagesize=letter, title=f"{step_name} Transcript {interview_id}")
    content = [
        Paragraph(escape(f"{step_name} Transcript"), styles["TranscriptTitle"]),
        Paragraph(escape(f"Interview ID: {interview_id}"), styles["TranscriptBody"]),
        Spacer(1, 8)
    ]
    last_stage = None
    for item in questions:
        stage = item["stage"] or "General Responses"
        if stage != last_stage:
            content.append(Paragraph(escape(stage), styles["TranscriptStage"]))
            last_stage = stage
        content.append(Paragraph(escape(item["question"]), styles["TranscriptQuestion"]))
        content.append(Paragraph(escape(item["answer"]).replace("\n", "<br/>"), styles["TranscriptBody"]))
    document.build(content)
    return buffer.getvalue()

@st.dialog("Stage saved to transcript")
def ask_document_more_stages(state_key):
    st.write("Document more stages?")
    more_col, finished_col = st.columns(2)
    with more_col:
        if st.button("Document more stages", key=f"{state_key}:more"):
            st.session_state.stage_walkthrough_ui[state_key]["pending"] = False
            st.rerun()
    with finished_col:
        if st.button("Finished.", key=f"{state_key}:finished"):
            st.session_state.stage_walkthrough_ui[state_key]["pending"] = False
            st.session_state.stage_walkthrough_ui[state_key]["finished"] = True
            st.rerun()

# ==============================================================================
# HEADER & GLOBAL DATA CONTROL DRAWER
# ==============================================================================
col_title, col_ctrl = st.columns([0.70, 0.30])
with col_title:
    st.markdown("<div class='main-title'>🧠 Thought Sweep Research Engine</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Barrett Honors Thesis Qualitative & Quantitative Strategy System</div>", unsafe_allow_html=True)

with col_ctrl:
    with st.expander("⚙️ System Data Controls"):
        st.markdown("**📥 Import Dataset (JSON)**")
        uploaded_file = st.file_uploader("Upload Research JSON", type=["json"], label_visibility="collapsed")
        if uploaded_file is not None:
            if st.button("Apply Uploaded Data", use_container_width=True):
                if import_all_data(uploaded_file):
                    st.toast("✅ Dataset imported successfully!", icon="🎉")
                    st.rerun()

        st.markdown("---")
        st.markdown("**📤 Export / Reset Data**")
        st.download_button(
            label="📥 Export Current JSON",
            data=export_all_data(),
            file_name="thought_sweep_research_data.json",
            mime="application/json",
            use_container_width=True
        )
        if st.button("🗑️ Reset All Data", use_container_width=True):
            clear_all_data()

# ==============================================================================
# TOP TAB NAVIGATION (INTERFACES 1 - 7)
# ==============================================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "1. Thesis Stages",
    "2. Faculty Obs.",
    "3. Student Exp.",
    "4. Transcript Coding",
    "5. Subtag Drill-Down",
    "6. Survey Stats",
    "7. Strategy Matrix"
])

# ------------------------------------------------------------------------------
# INTERFACE 1: STEP 1 INTERVIEW GUIDE (FULL QUESTIONS)
# ------------------------------------------------------------------------------
with tab1:
    st.markdown("### Interface 1: Step 1 Interview Guide — Defining Thesis Process")
    st.caption("Record full Step 1 interviews with faculty/advisors and standardize concrete thesis process stages.")

    col1, col2 = st.columns([1.1, 0.9])

    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Log Complete Step 1 Interview Entry")
        with st.form("step1_full_form", clear_on_submit=True):
            s1_id = st.text_input("Interviewee ID *", placeholder="e.g. S1-01")
            group = st.selectbox("Group *", ["Faculty", "Student-In-process", "Student-Completed"])
            disc = st.selectbox("Discipline *", ["STEM", "Creative", "Humanities", "Social Science"])
            unit_word = st.text_input("Unit Word Used (stage, phase, step, area)", value="stage")

            st.markdown("---")
            st.markdown("#### Part A: Main Areas (A1 – A6)")
            q_a1 = st.text_area("A1. From beginning to end, what are the main areas/phases a student goes through?", height=70)
            q_a2 = st.text_area("A2. What do you call each of these? Is there a name you/your department use?", height=70)
            q_a3 = st.text_area("A3. In what order do students usually move through them?", height=70)
            q_a4 = st.text_area("A4. Is there anything before the first or after the last area we should include?", height=70)
            q_a5 = st.text_area("A5. (Read list back) Does this match how you see the process? What would you change?", height=70)
            q_a6 = st.text_area("A6. Is this list the same for every thesis in your discipline or does it change?", height=70)

            st.markdown("---")
            st.markdown("#### Part B: Defining Each Stage (B1 – B9)")
            q_b1 = st.text_area("B1. What is [STAGE]? How would you explain it to a new student?", height=70)
            q_b2 = st.text_area("B2. What does a student actually do during [STAGE]?", height=70)
            q_b3 = st.text_area("B3. What does a student have to complete, produce, or have approved?", height=70)
            q_b4 = st.text_area("B4. Which requirements are set officially (Barrett/college) vs advisor/discipline?", height=70)
            q_b5 = st.text_area("B5. How do you know when a student is ready to move on from [STAGE]?", height=70)
            q_b6 = st.text_area("B6. What does a student need to have in place before beginning [STAGE]?", height=70)
            q_b7 = st.text_area("B7. Who is involved in [STAGE], and what does each person do?", height=70)
            q_b8 = st.text_area("B8. How long does [STAGE] take, and where does it fall on the timeline?", height=70)
            q_b9 = st.text_area("B9. What changes about [STAGE] from one project/discipline to another?", height=70)

            st.markdown("---")
            st.markdown("#### Part C: Boundaries and Wrap-Up (C1 – C5)")
            q_c1 = st.text_area("C1. Are there areas that overlap or blur together? How do you tell where one ends?", height=70)
            q_c2 = st.text_area("C2. Are there areas that some students skip, combine, or repeat?", height=70)
            q_c3 = st.text_area("C3. Are there official milestones, forms, or deadlines every student must meet?", height=70)
            q_c4 = st.text_area("C4. Is there anything about how the thesis process works that we missed?", height=70)
            q_c5 = st.text_area("C5. Who else should we speak with?", height=70)

            if st.form_submit_button("Save Complete Step 1 Interview", use_container_width=True):
                if s1_id:
                    entry = {
                        "id": s1_id, "group": group, "discipline": disc, "unit_word": unit_word,
                        "a1": q_a1, "a2": q_a2, "a3": q_a3, "a4": q_a4, "a5": q_a5, "a6": q_a6,
                        "b1": q_b1, "b2": q_b2, "b3": q_b3, "b4": q_b4, "b5": q_b5, "b6": q_b6, "b7": q_b7, "b8": q_b8, "b9": q_b9,
                        "c1": q_c1, "c2": q_c2, "c3": q_c3, "c4": q_c4, "c5": q_c5
                    }
                    st.session_state.step1_interviews.append(entry)
                    st.toast(f"✅ Saved Step 1 Interview {s1_id}! Available in Coding Repository.", icon="💾")
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Finalize Thesis Stage Names")
        st.caption("Saved stage names fill the stage choices used throughout the interview guides.")

        if st.session_state.edit_final_stages:
            with st.form("final_stage_names_form"):
                proposed_stages = []
                proposed_definitions = []
                for stage_number, stage_name in enumerate(st.session_state.final_stages, 1):
                    with st.container(border=True):
                        proposed_stages.append(st.text_input(
                            f"Final Stage {stage_number}",
                            value=stage_name,
                            key=f"final_stage_edit_{stage_number}"
                        ))
                        proposed_definitions.append(st.text_area(
                            "Definition",
                            value=st.session_state.stage_definitions.get(stage_name, ""),
                            placeholder=f"Define {stage_name}...",
                            key=f"final_stage_definition_edit_{stage_number}"
                        ))
                save_stages = st.form_submit_button("Save Final Stage Names", use_container_width=True)

            if save_stages:
                cleaned_stages = [stage.strip() for stage in proposed_stages]
                if any(not stage for stage in cleaned_stages):
                    st.error("Enter a name for each final stage before saving.")
                elif len(set(cleaned_stages)) != len(cleaned_stages):
                    st.error("Each final stage name must be unique.")
                else:
                    st.session_state.stage_definitions = {
                        stage: definition.strip()
                        for stage, definition in zip(cleaned_stages, proposed_definitions)
                    }
                    st.session_state.final_stages = cleaned_stages
                    st.session_state.edit_final_stages = False
                    st.toast("✅ Final stage names and definitions saved!", icon="🔒")
                    st.rerun()
        else:
            for stage_number, stage_name in enumerate(st.session_state.final_stages, 1):
                with st.container(border=True):
                    st.text_input(
                        f"Final Stage {stage_number}",
                        value=stage_name,
                        disabled=True,
                        key=f"final_stage_display_{stage_number}"
                    )
                    st.text_area(
                        "Definition",
                        value=st.session_state.stage_definitions.get(stage_name, ""),
                        disabled=True,
                        key=f"final_stage_definition_display_{stage_number}"
                    )
            if st.button("Edit Final Stage Names", use_container_width=True):
                st.session_state.edit_final_stages = True
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# INTERFACE 2: STEP 2 FACULTY OBSERVATIONS (FULL QUESTIONS)
# ------------------------------------------------------------------------------
with tab2:
    st.markdown("### Interface 2: Step 2 Faculty Interview Guide — Observed Challenges")
    st.caption("Capture faculty advisor observations across all stages, hardest stage identification, tools, and referrals.")
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    id_col, discipline_col = st.columns(2)
    with id_col:
        s2_id = st.text_input("Faculty Interviewee ID *", placeholder="e.g. F-01", key="step2_interview_id")
    with discipline_col:
        s2_discipline = st.selectbox("Faculty Discipline *", ["STEM", "Creative", "Humanities", "Social Science"], key="step2_discipline")

    stage_options = st.session_state.final_stages or ["Topic Selection / Ideation"]
    stage_state_key = f"step2:{s2_id.strip() or 'new-interview'}"
    walk_state = st.session_state.stage_walkthrough_ui.setdefault(
        stage_state_key, {"version": 0, "pending": False, "finished": False}
    )
    st.markdown("#### Part B: Observed Struggles by Stage")
    if walk_state["finished"]:
        st.success("Stage walkthrough finished. Saved stage responses are in the transcript.")
    else:
        walk_stage = st.selectbox("Select Stage", stage_options, key=f"{stage_state_key}:stage-select")
        widget_prefix = f"{stage_state_key}:v{walk_state['version']}:{walk_stage}"
        with st.form(f"{stage_state_key}:stage-form", clear_on_submit=True):
            stage_answers = {
                f"B{question_number}": st.text_area(
                    prompt.format(stage=walk_stage),
                    height=70,
                    key=f"{widget_prefix}:B{question_number}"
                )
                for question_number, prompt in [
                    (1, "What struggles do you observe at {stage}?"),
                    (2, "What does that look like in practice at {stage}? What do you see students doing or not doing?"),
                    (3, "Can you describe a recent example of a struggle at {stage}, without naming the student?"),
                    (4, "What do students do when this happens during {stage}?"),
                    (5, "What do you think is going on when students struggle during {stage}?"),
                    (6, "How common is this among the students you have advised during {stage}?"),
                    (7, "What have you seen students do that helps them through {stage}?"),
                    (8, "Does what you see at {stage} change with project type or discipline?")
                ]
            }
            save_stage = st.form_submit_button(f"Save {walk_stage} to Transcript", use_container_width=True)

        if save_stage:
            if not s2_id.strip():
                st.error("Enter the faculty interviewee ID before saving stage responses.")
            else:
                save_stage_response(
                    st.session_state.step2_interviews,
                    s2_id,
                    "Faculty",
                    s2_discipline,
                    walk_stage,
                    stage_answers
                )
                walk_state["version"] += 1
                walk_state["pending"] = True
                st.session_state.stage_walkthrough_ui[stage_state_key] = walk_state
        if walk_state["pending"]:
            ask_document_more_stages(stage_state_key)

    with st.form("step2_full_form", clear_on_submit=True):
        stages_list = st.session_state.final_stages or ["Topic Selection / Ideation"]
        hardest_stage = st.selectbox("Stage with Greatest Struggle (C1) *", stages_list)

        st.markdown("#### Part A: Confirming Stages")
        q_a2 = st.text_area("A2. Is there anything about these stages or definitions that is unclear?", height=60)
        q_a3 = st.text_area("A3. Is there any stage you think of differently from how it is defined here?", height=60)

        st.markdown("#### Part C: Stage with Greatest Struggle (C1 – C5)")
        q_c2 = st.text_area(f"C2. Why do you think students struggle the most at {hardest_stage}?", height=70)
        q_c3 = st.text_area("C3. What does that struggle look like when it is happening?", height=70)
        q_c4 = st.text_area("C4. Can you walk me through a specific example, without naming the student?", height=70)
        q_c5 = st.text_area("C5. What do you notice about students who get through with less struggle?", height=70)

        st.markdown("#### Part D: Ideas, Tools, and Support (D1 – D6)")
        q_d1 = st.text_area("D1. How do you see students come up with their ideas and keep track of them?", height=70)
        q_d2 = st.text_area("D2. What tools, systems, or methods have you seen students use to track work?", height=70)
        q_d3 = st.text_area("D3. What have you noticed about how well those work for students?", height=70)
        q_d4 = st.text_area("D4. When a student is stuck, what do you suggest and where do you send them?", height=70)
        q_d6 = st.text_area("D6. Is there anything else about what students go through that we missed?", height=70)

        if st.form_submit_button("Save Complete Faculty Interview", use_container_width=True):
            if s2_id.strip():
                entry = {
                    "id": s2_id.strip(), "group": "Faculty", "discipline": s2_discipline, "hardest_stage": hardest_stage,
                    "a2": q_a2, "a3": q_a3,
                    "c2": q_c2, "c3": q_c3, "c4": q_c4, "c5": q_c5,
                    "d1": q_d1, "d2": q_d2, "d3": q_d3, "d4": q_d4, "d6": q_d6
                }
                upsert_interview(st.session_state.step2_interviews, entry)
                st.toast(f"✅ Saved Faculty Interview {s2_id}! Ready for coding in Interface 4.", icon="💾")
                st.rerun()
            st.error("Enter the faculty interviewee ID before saving the interview.")
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# INTERFACE 3: STEP 3 STUDENT EXPERIENCES (FULL QUESTIONS)
# ------------------------------------------------------------------------------
with tab3:
    st.markdown("### Interface 3: Step 3 Student Interview Guide — Thesis Experience")
    st.caption("Capture complete Barrett student interview responses across warm-up, stage experience, ideas, challenges, tools, and support.")
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    id_col, group_col, discipline_col = st.columns(3)
    with id_col:
        s3_id = st.text_input("Student Participant ID *", placeholder="e.g. S-01", key="step3_interview_id")
    with group_col:
        s3_group = st.selectbox("Student Status *", ["Student-In-process", "Student-Completed", "Student-Beginning"], key="step3_group")
    with discipline_col:
        s3_discipline = st.selectbox("Discipline *", ["STEM", "Creative", "Humanities", "Social Science"], key="step3_discipline")

    warmup_key = f"step3:{s3_id.strip() or 'new-interview'}:warmup"
    stages_list = st.session_state.final_stages or ["Topic Selection / Ideation"]
    hardest_stage = st.selectbox("Hardest Stage (H2)", stages_list, key=f"{warmup_key}:hardest-stage")

    st.markdown("#### Warm-Up & Stage Status (01 – 04)")
    q_01 = st.text_area("01. In a sentence or two, what is your thesis about?", height=60, key=f"{warmup_key}:01")
    q_02 = st.text_area("02. About how long have you been working on your thesis?", height=60, key=f"{warmup_key}:02")
    q_03 = st.text_area("03. Is there anything on the stage card that is unclear?", height=60, key=f"{warmup_key}:03")
    q_04 = st.text_area("04. Which stages have you finished, and which one are you in now?", height=60, key=f"{warmup_key}:04")

    stage_options = st.session_state.final_stages or ["Topic Selection / Ideation"]
    stage_state_key = f"step3:{s3_id.strip() or 'new-interview'}"
    walk_state = st.session_state.stage_walkthrough_ui.setdefault(
        stage_state_key, {"version": 0, "pending": False, "finished": False}
    )
    st.markdown("#### Stage by Stage Experience (B1 – B7)")
    if walk_state["finished"]:
        st.success("Stage walkthrough finished. Saved stage responses are in the transcript.")
    else:
        walk_stage = st.selectbox("Select Stage", stage_options, key=f"{stage_state_key}:stage-select")
        widget_prefix = f"{stage_state_key}:v{walk_state['version']}:{walk_stage}"
        with st.form(f"{stage_state_key}:stage-form", clear_on_submit=True):
            stage_answers = {
                f"B{question_number}": st.text_area(
                    prompt.format(stage=walk_stage),
                    height=height,
                    key=f"{widget_prefix}:B{question_number}"
                )
                for question_number, prompt, height in [
                    (1, "Walk me through what you did during {stage}, starting with the first thing.", 70),
                    (2, "Think of a moment during {stage} when something didn't go as expected. What happened?", 70),
                    (3, "What did you do when that happened during {stage}?", 70),
                    (4, "What do you think was going on at that point in {stage}?", 70),
                    (5, "What part of {stage} went more smoothly than expected? What helped?", 70),
                    (6, "Was anyone else involved in {stage}? What did they do? (Optional)", 60),
                    (7, "If doing {stage} again, what would you do differently? (Optional)", 60)
                ]
            }
            save_stage = st.form_submit_button(f"Save {walk_stage} to Transcript", use_container_width=True)

        if save_stage:
            if not s3_id.strip():
                st.error("Enter the student participant ID before saving stage responses.")
            else:
                save_stage_response(
                    st.session_state.step3_interviews,
                    s3_id,
                    s3_group,
                    s3_discipline,
                    walk_stage,
                    stage_answers
                )
                walk_state["version"] += 1
                walk_state["pending"] = True
                st.session_state.stage_walkthrough_ui[stage_state_key] = walk_state
        if walk_state["pending"]:
            ask_document_more_stages(stage_state_key)

    with st.form("step3_full_form", clear_on_submit=True):
        st.markdown("#### Your Ideas (11 – 110)")
        q_11 = st.text_area("11. Where did your thesis idea come from? Walk me through how you first came up with it.", height=70)
        q_12 = st.text_area("12. Tell me about any other ideas you considered before your current one. What happened to them?", height=70)
        q_13 = st.text_area("13. Think about the most recent time a new thesis idea came to you. Where were you & doing?", height=70)
        q_14 = st.text_area("14. What was the first thing you did with that idea?", height=60)
        q_15 = st.text_area("15. What happened to that idea afterward?", height=60)
        q_16 = st.text_area("16. Last time you needed something saved earlier (note, source, idea), what happened?", height=70)
        q_17 = st.text_area("17. Walk me through the steps between that first idea and having a plan to work from.", height=70)
        q_18 = st.text_area("18. Was there a point on the way from idea to plan where you were unsure what to do next?", height=70)
        q_19 = st.text_area("19. Walk me through how one part went from an idea to what you have now (deliverable).", height=70)
        q_110 = st.text_area("110 (Optional). Last idea that turned into something you had to do (task/deadline)?", height=60)

        st.markdown("#### Most Difficult Challenge (H1 – H5)")
        q_h1 = st.text_area("H1. What has been the most difficult challenge you have faced with your thesis so far?", height=70)
        q_h3 = st.text_area("H3. What made that so difficult?", height=70)
        q_h4 = st.text_area("H4. What did that look like day to day? What were you doing, or not doing?", height=70)
        q_h5 = st.text_area("H5. How did you get through it, or are you still working through it? What helped?", height=70)

        st.markdown("#### Tools (U1 – U9)")
        q_u1 = st.text_area("U1. Last time you wrote down or recorded an idea for your thesis, what did you use?", height=60)
        q_u2 = st.text_area("U2. Where do your thesis notes, readings, and sources live right now? List every place.", height=70)
        q_u3 = st.text_area("U3. How did you start using each tool/place? Who/what made you choose it?", height=60)
        q_u4 = st.text_area("U4. What works well about using it, and what is frustrating about it?", height=70)
        q_u5 = st.text_area("U5. Have you stopped using any app, notebook, or method you started out with? Why?", height=60)
        q_u6 = st.text_area("U6. What do you use to turn ideas into your final project (outline, draft, plan)?", height=60)
        q_u7 = st.text_area("U7. Is there anything you do by hand or work around because a tool doesn't do it?", height=70)
        q_u8 = st.text_area("U8. Thinking about the last time you did that workaround, what were you trying to get done?", height=60)
        q_u9 = st.text_area("U9 (Optional). Would you change anything about how you handle notes/ideas weekly?", height=60)

        st.markdown("#### Support and Wrap-Up (S1 – S4)")
        q_s1 = st.text_area("S1. When in your thesis did you most wish you had more help? What kind of help?", height=70)
        q_s2 = st.text_area("S2. When you have had a question about your thesis, who did you go to?", height=60)
        q_s3 = st.text_area("S3. Where do you usually go to find out about resources/tools? Whose advice do you trust?", height=70)
        q_s4 = st.text_area("S4. Is there anything that made your thesis easier or harder that we haven't talked about?", height=70)

        if st.form_submit_button("Save Complete Student Interview", use_container_width=True):
            if s3_id.strip():
                entry = {
                    "id": s3_id.strip(), "group": s3_group, "discipline": s3_discipline, "hardest_stage": hardest_stage,
                    "01": q_01, "02": q_02, "03": q_03, "04": q_04,
                    "q_11": q_11, "q_12": q_12, "q_13": q_13, "q_14": q_14, "q_15": q_15, "q_16": q_16, "q_17": q_17, "q_18": q_18, "q_19": q_19, "q_110": q_110,
                    "h1": q_h1, "h3": q_h3, "h4": q_h4, "h5": q_h5,
                    "u1": q_u1, "u2": q_u2, "u3": q_u3, "u4": q_u4, "u5": q_u5, "u6": q_u6, "u7": q_u7, "u8": q_u8, "u9": q_u9,
                    "s1": q_s1, "s2": q_s2, "s3": q_s3, "s4": q_s4
                }
                upsert_interview(st.session_state.step3_interviews, entry)
                st.toast(f"✅ Saved Student Interview {s3_id}! Ready for qualitative coding.", icon="💾")
                st.rerun()
            st.error("Enter the student participant ID before saving the interview.")
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# INTERFACE 4: QUALITATIVE CODING & ICR ENGINE
# ------------------------------------------------------------------------------
with tab4:
    st.markdown("### Interface 4: Transcript Coding Repository & Reliability Engine")
    
    sub_code, sub_annot, sub_icr = st.tabs(["📖 Living Codebook v0.3", "🏷️ Coding Interface (Coder A)", "🛡️ Coder B & Kappa Verification"])

    # Subtab 1: Codebook
    with sub_code:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Manage Living Codebook v0.3")
        
        with st.expander("➕ Add New Emergent Code (EM)"):
            c_id = st.text_input("Code ID", placeholder="EM-01")
            c_name = st.text_input("Code Title", placeholder="Citation Confusion")
            c_cat = st.selectbox("Category", [
                "Challenge Codes (C)", "Tools Used (T)", "Tool Evaluation - Chosen (R)", 
                "Tool Evaluation - Dropped (A)", "Capabilities Wanted (W)", "Capture Context (X)", 
                "Developing Ideas (D)", "Where Heard About Tools (CH)", "External Codes (E)", "Emergent Themes (EM)"
            ])
            c_desc = st.text_area("Definition & Boundaries")
            c_apply = st.text_area("How to Apply / Do Not Code When")
            if st.button("Add Code to Codebook"):
                if c_id and c_name:
                    st.session_state.codebook.append({"id": c_id, "name": c_name, "category": c_cat, "desc": c_desc, "how_to_apply": c_apply})
                    st.toast(f"✅ Added {c_id} ({c_name}) to Codebook!", icon="📖")
                    st.rerun()

        cb_df = pd.DataFrame(st.session_state.codebook)
        st.dataframe(cb_df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Subtab 2: Coding Interface
    with sub_annot:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        all_transcripts = (
            [{"source": "Step 2", "id": x["id"], "group": x["group"], "discipline": x["discipline"], "questions": build_transcript_questions(x, "Step 2")} for x in st.session_state.step2_interviews] +
            [{"source": "Step 3", "id": x["id"], "group": x["group"], "discipline": x["discipline"], "questions": build_transcript_questions(x, "Step 3")} for x in st.session_state.step3_interviews]
        )

        if not all_transcripts:
            st.warning("No Step 2 or Step 3 transcripts are available for coding yet.")
        else:
            transcript_options = [
                f"{item['source']} | {item['id']} | {index + 1}"
                for index, item in enumerate(all_transcripts)
            ]
            selected_transcript = st.selectbox(
                "Select Interview Transcript:",
                transcript_options,
                key="coder_a_selected_transcript"
            )
            transcript_index = transcript_options.index(selected_transcript)
            curr_item = all_transcripts[transcript_index]

            st.markdown(f"**Group:** `{curr_item['group']}` | **Discipline:** `{curr_item['discipline']}`")

            questions = curr_item["questions"]
            if not questions:
                st.info("This interview does not have any answered questions to code yet.")
            else:
                question_indices = st.session_state.setdefault("coding_question_indices", {})
                question_index = min(question_indices.get(selected_transcript, 0), len(questions) - 1)
                question = questions[question_index]
                total_questions = len(questions)
                st.markdown(
                    f"**Question {question_index + 1} / {total_questions}** · "
                    f"{question_index} completed · {total_questions - question_index - 1} remaining"
                )
                st.progress((question_index + 1) / total_questions)

                question_col, coding_col = st.columns([1.5, 1])
                with question_col:
                    with st.container(border=True):
                        st.caption(f"Stage: {question['stage'] or 'Not specified'}")
                        st.markdown(f"### {question['question']}")
                        st.markdown("**Response**")
                        st.write(question["answer"])

                    previous_col, next_col = st.columns(2)
                    with previous_col:
                        if st.button("← Previous", disabled=question_index == 0, use_container_width=True):
                            question_indices[selected_transcript] = question_index - 1
                            st.rerun()
                    with next_col:
                        if st.button("Next →", disabled=question_index >= total_questions - 1, use_container_width=True):
                            question_indices[selected_transcript] = question_index + 1
                            st.rerun()

                with coding_col:
                    with st.container(border=True):
                        st.subheader("Apply Code")
                        with st.form("coding_tag_form", clear_on_submit=True):
                            selected_text = st.text_area(
                                "Paste Excerpt / Thought Unit to Code:",
                                height=180
                            )
                            code_options = [f"{c['id']} - {c['name']}" for c in st.session_state.codebook]
                            selected_code = st.selectbox("Apply Code:", code_options)

                            if st.form_submit_button("Save Code", type="primary", use_container_width=True):
                                if selected_text and selected_code:
                                    code_id = selected_code.split(" - ")[0]
                                    tag_entry = {
                                        "interview_id": curr_item["id"],
                                        "selected_text": selected_text,
                                        "code_id": code_id,
                                        "group": curr_item["group"],
                                        "discipline": curr_item["discipline"]
                                    }
                                    st.session_state.coder_a_annotations.append(tag_entry)
                                    st.toast(f"✅ Tagged excerpt with {code_id}!", icon="🏷️")
                                    st.rerun()

            st.markdown("---")
            st.subheader("Existing Annotations (Coder A)")
            st.dataframe(pd.DataFrame(st.session_state.coder_a_annotations), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Subtab 3: Coder B & Kappa Check
    with sub_icr:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Inter-Coder Reliability (ICR) Verification")
        st.caption("Requirement: Cohen's Kappa ≥ 0.70 to lock data for statistical modeling.")

        if not st.session_state.coder_a_annotations:
            st.info("Coder A must apply annotations before ICR verification can begin.")
        else:
            sample_size = max(1, math.ceil(len(st.session_state.coder_a_annotations) * 0.25))
            sample_items = st.session_state.coder_a_annotations[:sample_size]
            
            st.markdown(f"**Required Coder B Verification Sample Size:** `{sample_size}` items")

            coder_b_inputs = []
            for idx, item in enumerate(sample_items):
                st.markdown(f"**Item {idx+1} (ID: {item['interview_id']}):** *\"{item['selected_text']}\"*")
                b_code = st.selectbox(
                    f"Coder B Code for Item {idx+1}:", 
                    [c["id"] for c in st.session_state.codebook], 
                    key=f"b_code_{idx}"
                )
                coder_b_inputs.append(b_code)

            if st.button("Calculate Cohen's Kappa Score", use_container_width=True):
                a_codes = [item["code_id"] for item in sample_items]
                matches = sum(1 for a, b in zip(a_codes, coder_b_inputs) if a == b)
                po = matches / sample_size
                pe = 1.0 / len(st.session_state.codebook)
                kappa = (po - pe) / (1 - pe) if (1 - pe) != 0 else 1.0
                
                st.session_state.kappa_value = round(kappa, 3)
                if kappa >= 0.70:
                    st.session_state.kappa_locked = True
                    st.toast(f"✅ PASSED! Cohen's Kappa = {kappa:.3f}", icon="🛡️")
                else:
                    st.session_state.kappa_locked = False
                    st.toast(f"❌ FAILED! Cohen's Kappa = {kappa:.3f}", icon="⚠️")
        st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# INTERFACE 5: SUBTAG DRILL-DOWN & FREQUENCY
# ------------------------------------------------------------------------------
with tab5:
    st.markdown("### Interface 5: Qualitative Frequencies & Subtag Filters")

    frequency_tab, uncoded_tab = st.tabs(["Qualitative Frequencies", "Transcripts (Uncoded)"])
    with frequency_tab:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        if not st.session_state.coder_a_annotations:
            st.info("No qualitative coding annotations recorded yet.")
        else:
            df_annot = pd.DataFrame(st.session_state.coder_a_annotations)
            df_unique = df_annot.drop_duplicates(subset=["interview_id", "code_id"])

            st.subheader("Top 5 Codes Overall (Unique Participant Counts)")
            top_overall = df_unique["code_id"].value_counts().head(5)
            st.bar_chart(top_overall)

            st.markdown("---")
            st.subheader("Subtag Filter Breakdown")
            filter_type = st.radio("Drill Down By:", ["Discipline", "Group (Faculty vs Student)", "Individual Interview ID"], horizontal=True)
            
            if filter_type == "Discipline":
                all_disciplines = ["STEM", "Creative", "Humanities", "Social Science"]
                disc = st.selectbox("Select Discipline:", all_disciplines)
                filtered = df_unique[df_unique["discipline"] == disc]
                if filtered.empty:
                    st.caption(f"No qualitative tags recorded yet under '{disc}'.")
                else:
                    st.table(filtered["code_id"].value_counts().head(5))
            elif filter_type == "Group (Faculty vs Student)":
                all_groups = ["Faculty", "Student-In-process", "Student-Completed", "Student-Beginning"]
                grp = st.selectbox("Select Group:", all_groups)
                filtered = df_unique[df_unique["group"] == grp]
                if filtered.empty:
                    st.caption(f"No qualitative tags recorded yet under '{grp}'.")
                else:
                    st.table(filtered["code_id"].value_counts().head(5))
            else:
                all_uids = df_unique["interview_id"].unique() if not df_unique.empty else ["S1-01"]
                iid = st.selectbox("Select Interview ID:", all_uids)
                filtered = df_unique[df_unique["interview_id"] == iid]
                if filtered.empty:
                    st.caption(f"No qualitative tags recorded for Interview ID '{iid}'.")
                else:
                    st.table(filtered["code_id"].value_counts().head(5))
        st.markdown("</div>", unsafe_allow_html=True)

    with uncoded_tab:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Transcripts (Uncoded)")
        st.caption("Full interview transcripts grouped by interview step. Each document can be downloaded as a PDF.")

        transcripts_by_step = [
            ("Step 1", st.session_state.step1_interviews),
            ("Step 2", st.session_state.step2_interviews),
            ("Step 3", st.session_state.step3_interviews)
        ]
        if not any(interviews for _, interviews in transcripts_by_step):
            st.info("No interview transcripts have been recorded yet.")
        else:
            for step_name, interviews in transcripts_by_step:
                st.markdown(f"#### {step_name}")
                if not interviews:
                    st.caption("No transcripts for this step yet.")
                    continue
                for interview_index, interview in enumerate(interviews):
                    interview_id = str(interview.get("id", "Unknown"))
                    questions = build_transcript_questions(interview, step_name)
                    with st.expander(f"Interview ID: {interview_id}", expanded=False):
                        st.caption(f"{step_name} | Interview ID: {interview_id}")
                        with st.container(border=True):
                            if not questions:
                                st.info("This interview has no recorded answers yet.")
                            else:
                                current_stage = None
                                for question in questions:
                                    stage_name = question["stage"] or "General Responses"
                                    if stage_name != current_stage:
                                        st.markdown(f"### {stage_name}")
                                        current_stage = stage_name
                                    st.markdown(f"**{question['question']}**")
                                    st.write(question["answer"])

                        safe_interview_id = re.sub(r"[^A-Za-z0-9._-]+", "_", interview_id).strip("._") or "interview"
                        st.download_button(
                            "Download PDF",
                            data=create_transcript_pdf(step_name, interview_id, questions),
                            file_name=f"{step_name.lower().replace(' ', '_')}_{safe_interview_id}.pdf",
                            mime="application/pdf",
                            key=f"uncoded_transcript_pdf_{step_name}_{interview_index}"
                        )
        st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# INTERFACE 6: QUANTITATIVE SURVEY STATS
# ------------------------------------------------------------------------------
with tab6:
    st.markdown("### Interface 6: Quantitative Survey Entry & Statistical Tests")
    
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Record Survey Response")
        with st.form("survey_form", clear_on_submit=True):
            s_id = st.text_input("Survey ID *", placeholder="e.g. R-001")
            survey_codes = [f"C{code_number}" for code_number in range(1, 9)]
            responses = []
            for section_number in range(1, 6):
                st.markdown(f"#### Section {section_number}")
                code_id = st.selectbox(
                    f"Target Code {section_number} *", survey_codes
                )
                eligible = st.checkbox(
                    f"Eligible for Stage? (Section {section_number})", value=True
                )
                experienced = st.checkbox(
                    f"Experienced Difficulty? (Section {section_number})", value=True
                )
                severity = st.slider(
                    f"Pain Severity Rating (1-5) (Section {section_number})", 1, 5, 4
                )
                responses.append((code_id, eligible, experienced, severity))

            if st.form_submit_button("Record Response", use_container_width=True):
                if s_id:
                    for section_number, (code_id, eligible, experienced, severity) in enumerate(responses, 1):
                        st.session_state.surveys.append({
                            "survey_id": s_id,
                            "section": section_number,
                            "code_id": code_id,
                            "eligible": eligible,
                            "experienced": experienced,
                            "severity": severity
                        })
                    st.toast(f"✅ Saved 5 survey responses for {s_id}!", icon="📊")
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Automated Background Statistical Tests")
        if not st.session_state.surveys:
            st.info("No survey response entries recorded yet.")
        else:
            df_surv = pd.DataFrame(st.session_state.surveys)
            results = []
            for c in st.session_state.codebook:
                cid = c["id"]
                sub = df_surv[df_surv["code_id"] == cid]
                n_el = len(sub[sub["eligible"] == True])
                n_high = len(sub[(sub["eligible"] == True) & (sub["experienced"] == True) & (sub["severity"] >= 4)])
                
                pain_rate = (n_high / n_el) if n_el > 0 else 0.0
                
                if n_el > 0:
                    z = 1.96
                    p = pain_rate
                    denom = 1 + (z**2)/n_el
                    center = p + (z**2)/(2*n_el)
                    dev = z * math.sqrt((p*(1-p) + (z**2)/(4*n_el))/n_el)
                    wilson_low = max(0.0, (center - dev)/denom)
                    wilson_high = min(1.0, (center + dev)/denom)
                else:
                    wilson_low, wilson_high = 0.0, 0.0

                p_val_binom = stats.binomtest(n_high, n_el, p=0.20, alternative='greater').pvalue if n_el > 0 else 1.0

                results.append({
                    "Code": cid,
                    "Eligible N": n_el,
                    "High Pain N": n_high,
                    "Pain Rate %": f"{pain_rate*100:.1f}%",
                    "Wilson 95% CI": f"[{wilson_low*100:.1f}%, {wilson_high*100:.1f}%]",
                    "Exact Binomial p-val": f"{p_val_binom:.4f}"
                })

            st.dataframe(pd.DataFrame(results), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# INTERFACE 7: 2x2 STRATEGY MATRIX
# ------------------------------------------------------------------------------
with tab7:
    st.markdown("### Interface 7: Integrated 2x2 Opportunity Prioritization Engine")
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    df_annot = pd.DataFrame(st.session_state.coder_a_annotations) if st.session_state.coder_a_annotations else pd.DataFrame()
    df_surv = pd.DataFrame(st.session_state.surveys) if st.session_state.surveys else pd.DataFrame()

    total_students = df_annot[df_annot["group"].str.contains("Student", na=False)]["interview_id"].nunique() if not df_annot.empty else 1
    matrix_data = []

    for c in st.session_state.codebook:
        cid = c["id"]
        
        if not df_annot.empty:
            code_students = df_annot[(df_annot["code_id"] == cid) & (df_annot["group"].str.contains("Student", na=False))]["interview_id"].nunique()
            qual_freq = (code_students / total_students) if total_students > 0 else 0.0
            faculty_count = df_annot[(df_annot["code_id"] == cid) & (df_annot["group"] == "Faculty")]["interview_id"].nunique()
        else:
            qual_freq, faculty_count, code_students = 0.0, 0, 0

        if not df_surv.empty:
            sub = df_surv[df_surv["code_id"] == cid]
            n_el = len(sub[sub["eligible"] == True])
            n_high = len(sub[(sub["eligible"] == True) & (sub["experienced"] == True) & (sub["severity"] >= 4)])
            pain_rate = (n_high / n_el) if n_el > 0 else 0.0
        else:
            pain_rate, n_el = 0.0, 0

        p_val = stats.binomtest(code_students, max(1, total_students), p=0.25, alternative='greater').pvalue if total_students > 0 else 1.0
        is_triangulated = (faculty_count > 0 and code_students > 0) or (code_students > 0 and pain_rate >= 0.20)

        matrix_data.append({
            "code": c,
            "qual_freq": qual_freq,
            "pain_rate": pain_rate,
            "triangulated": is_triangulated,
            "p_val": p_val
        })

    matrix_data.sort(key=lambda x: x["p_val"])
    m = len(matrix_data)
    for idx, item in enumerate(matrix_data):
        alpha = 0.05 / (m - idx)
        item["significant"] = item["p_val"] <= alpha

    st.subheader("Strategic Opportunity Positioning Grid")
    q_lead, q_supp, q_niche, q_drop = [], [], [], []

    for item in matrix_data:
        is_high_freq = (item["qual_freq"] >= 0.25) or (item["qual_freq"] > 0)
        is_high_pain = item["pain_rate"] >= 0.20
        
        if is_high_freq and is_high_pain and item["triangulated"]:
            q_lead.append(item)
        elif not is_high_freq and is_high_pain:
            q_supp.append(item)
        elif is_high_freq and not is_high_pain:
            q_niche.append(item)
        else:
            q_drop.append(item)

    g1, g2 = st.columns(2)
    with g1:
        st.markdown("<div class='quad-card' style='background: rgba(245, 158, 11, 0.15); border-color: #f59e0b;'><b>SUPPORTING MESSAGE</b><br><small>Low Frequency / High Pain Rate</small></div>", unsafe_allow_html=True)
        for x in q_supp: st.write(f"• **{x['code']['id']}** ({x['code']['name']})")
        
    with g2:
        st.markdown("<div class='quad-card' style='background: rgba(16, 185, 129, 0.2); border-color: #10b981;'><b>⭐ LEAD MESSAGE</b><br><small>High Frequency / High Pain / Triangulated</small></div>", unsafe_allow_html=True)
        for x in q_lead: 
            sig_badge = "🛡️ Sig" if x["significant"] else ""
            st.write(f"• **{x['code']['id']}** ({x['code']['name']}) {sig_badge}")

    g3, g4 = st.columns(2)
    with g3:
        st.markdown("<div class='quad-card' style='background: rgba(51, 65, 85, 0.3); border-color: #64748b;'><b>DROP FOR NOW</b><br><small>Low Frequency / Low Pain Rate</small></div>", unsafe_allow_html=True)
        for x in q_drop: st.write(f"• **{x['code']['id']}** ({x['code']['name']})")
        
    with g4:
        st.markdown("<div class='quad-card' style='background: rgba(99, 102, 241, 0.15); border-color: #6366f1;'><b>NICHE / BROAD CONCERN</b><br><small>High Frequency / Low Pain Rate</small></div>", unsafe_allow_html=True)
        for x in q_niche: st.write(f"• **{x['code']['id']}** ({x['code']['name']})")

    st.markdown("---")
    st.subheader("Automated Campaign Messaging Strategy Output")
    selected_matrix_code = st.selectbox("Select Code for Campaign Strategy Brief:", [x["code"]["id"] for x in matrix_data])
    target_item = next(x for x in matrix_data if x["code"]["id"] == selected_matrix_code)
    
    st.info(f"**Target Code:** {target_item['code']['id']} - {target_item['code']['name']}")
    st.write(f"**Primary Campaign Headline:** Stop Drowning in {target_item['code']['name']} — Build Your Thesis Plan Fast with Thought Sweep.")
    st.write(f"**Recommended Channel:** Barrett Honors College Weekly Digest & Academic Advisor Referrals")
    st.markdown("</div>", unsafe_allow_html=True)
