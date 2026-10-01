import html
from textwrap import dedent
import streamlit as st
from model.recommendation_model import recommend_skills


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Smart SkillPath",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CAREER-WISE SKILLS
# =========================================================

CAREER_SKILLS = {
    "Data Scientist": [
        "Python", "SQL", "Excel", "Machine Learning", "Statistics",
        "Pandas", "NumPy", "Data Visualization", "Scikit-learn",
        "TensorFlow", "PyTorch", "Deep Learning", "Data Mining",
        "Data Wrangling", "R", "Spark", "Hadoop"
    ],
    "Data Analyst": [
        "Python", "SQL", "Excel", "Power BI", "Tableau", "Statistics",
        "Pandas", "NumPy", "Data Visualization", "Data Cleaning",
        "Data Analysis", "MySQL", "Microsoft Excel", "DAX"
    ],
    "Machine Learning Engineer": [
        "Python", "SQL", "Machine Learning", "Deep Learning",
        "Scikit-learn", "TensorFlow", "PyTorch", "Pandas", "NumPy",
        "Statistics", "Data Structures", "Algorithms", "Git", "Docker",
        "MLOps", "AWS", "Azure"
    ],
    "Software Engineer": [
        "Python", "Java", "C", "C++", "JavaScript", "Data Structures",
        "Algorithms", "OOP", "Git", "GitHub", "SQL", "MySQL",
        "Software Development", "Testing", "Debugging", "REST API"
    ],
    "Web Developer": [
        "HTML", "CSS", "JavaScript", "PHP", "Python", "React", "Node.js",
        "MySQL", "MongoDB", "Git", "GitHub", "REST API", "Bootstrap",
        "Responsive Design"
    ],
    "Backend Developer": [
        "Python", "Java", "PHP", "Node.js", "SQL", "MySQL", "MongoDB",
        "REST API", "Django", "Flask", "Git", "Docker", "Linux",
        "Database Management"
    ],
    "Frontend Developer": [
        "HTML", "CSS", "JavaScript", "React", "Bootstrap", "TypeScript",
        "Git", "GitHub", "Responsive Design", "UI/UX", "Figma", "REST API"
    ],
    "DevOps Engineer": [
        "Linux", "Git", "GitHub", "Docker", "Kubernetes", "AWS", "Azure",
        "CI/CD", "Jenkins", "Python", "Bash", "Terraform",
        "Cloud Computing", "Networking"
    ],
    "Cloud Engineer": [
        "AWS", "Microsoft Azure", "Google Cloud", "Cloud Computing",
        "Linux", "Networking", "Docker", "Kubernetes", "Python",
        "Terraform", "Security", "Virtualization"
    ],
    "Cybersecurity Analyst": [
        "Cybersecurity", "Network Security", "Linux", "Python",
        "Ethical Hacking", "Cryptography", "Firewalls", "SIEM",
        "Penetration Testing", "Networking", "Risk Management",
        "Incident Response"
    ],
    "Database Administrator": [
        "SQL", "MySQL", "Oracle", "MongoDB", "Database Management",
        "Database Security", "Backup and Recovery", "Python", "Linux",
        "Data Modeling", "PL/SQL"
    ],
    "Business Intelligence Analyst": [
        "SQL", "Power BI", "Tableau", "Excel", "DAX", "Data Analysis",
        "Data Visualization", "Statistics", "MySQL", "Data Cleaning",
        "Business Intelligence"
    ]
}


# =========================================================
# SESSION STATE
# =========================================================

if "recommendation_result" not in st.session_state:
    st.session_state.recommendation_result = None

if "last_career" not in st.session_state:
    st.session_state.last_career = None

if "last_skills" not in st.session_state:
    st.session_state.last_skills = []


# =========================================================
# HELPERS
# =========================================================

def safe(value):
    """Safely display text inside HTML."""
    return html.escape(str(value))


def render_html(content):
    """Render HTML without Streamlit treating indented tags as code."""
    st.markdown(
        dedent(content),
        unsafe_allow_html=True
    )


def card(title, value, icon):
    return dedent(f"""
    <div class="summary-card">
        <div class="summary-icon">{icon}</div>
        <div class="summary-title">{safe(title)}</div>
        <div class="summary-value">{safe(value)}</div>
    </div>
    """)


def skill_card(skill, icon="✓"):
    return dedent(f"""
    <div class="skill-card">
        <span class="skill-icon">{icon}</span>
        <span class="skill-text">{safe(skill)}</span>
    </div>
    """)


def info_card(title, text, icon):
    return dedent(f"""
    <div class="info-card">
        <div class="info-card-title">{icon} {safe(title)}</div>
        <div class="info-card-text">{safe(text)}</div>
    </div>
    """)


def role_card(role_name, score):
    return dedent(f"""
    <div class="role-card">
        <div class="role-top">
            <div class="role-name">💼 {safe(role_name)}</div>
            <div class="score-badge">{score:.2f}%</div>
        </div>
        <div class="role-label">Skill profile match</div>
    </div>
    """)


def certification_card(number, certification):
    return dedent(f"""
    <div class="cert-card">
        <div class="cert-number">{number}</div>
        <div>
            <div class="cert-title">🏆 {safe(certification)}</div>
            <div class="cert-subtitle">Relevant to your selected career path</div>
        </div>
    </div>
    """)


# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>

/* =====================================================
   GLOBAL
   ===================================================== */

.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    border-right: 1px solid #e5e7eb;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
}

h1, h2, h3 {
    color: #172554 !important;
}

div[data-testid="stButton"] > button {
    border-radius: 12px;
    min-height: 46px;
    font-weight: 700;
}

div[data-testid="stFormSubmitButton"] > button {
    border-radius: 12px;
    min-height: 48px;
    font-weight: 700;
}

/* =====================================================
   HERO
   ===================================================== */

.hero {
    background: linear-gradient(135deg, #eff6ff 0%, #f8fafc 100%);
    border: 1px solid #dbeafe;
    border-radius: 24px;
    padding: 42px 38px;
    margin-bottom: 28px;
    text-align: center;
}

.hero-kicker {
    display: inline-block;
    background: #ffffff;
    border: 1px solid #dbeafe;
    border-radius: 999px;
    padding: 7px 14px;
    font-size: 12px;
    font-weight: 700;
    color: #2563eb;
    margin-bottom: 14px;
}

.hero-title {
    font-size: 42px;
    line-height: 1.15;
    font-weight: 800;
    color: #172554;
    margin-bottom: 10px;
}

.hero-subtitle {
    font-size: 18px;
    font-weight: 600;
    color: #334155;
    margin-bottom: 10px;
}

.hero-description {
    max-width: 760px;
    margin: auto;
    color: #64748b;
    font-size: 15px;
    line-height: 1.7;
}

/* =====================================================
   SECTION
   ===================================================== */

.section-heading {
    font-size: 25px;
    font-weight: 800;
    color: #172554;
    margin: 24px 0 5px 0;
}

.section-subheading {
    color: #64748b;
    font-size: 14px;
    margin-bottom: 18px;
}

/* =====================================================
   STEP HEADER
   ===================================================== */

.step-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 22px 0 10px 0;
}

.step-number {
    min-width: 36px;
    height: 36px;
    border-radius: 50%;
    background: #172554;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 13px;
}

.step-title {
    font-size: 18px;
    font-weight: 750;
    color: #172554;
}

.step-description {
    color: #64748b;
    font-size: 13px;
    margin: -3px 0 12px 50px;
}

/* =====================================================
   SUMMARY CARDS
   ===================================================== */

.summary-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 20px;
    min-height: 145px;
    box-shadow: 0 3px 12px rgba(15, 23, 42, 0.04);
}

.summary-icon {
    font-size: 22px;
    margin-bottom: 12px;
}

.summary-title {
    font-size: 12px;
    color: #64748b;
    font-weight: 650;
    margin-bottom: 6px;
}

.summary-value {
    font-size: 21px;
    color: #172554;
    font-weight: 800;
    line-height: 1.3;
}

/* =====================================================
   SKILLS
   ===================================================== */

.skill-card {
    display: flex;
    align-items: center;
    gap: 11px;
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    border-radius: 13px;
    padding: 13px 15px;
    margin-bottom: 9px;
    min-height: 48px;
}

.skill-icon {
    color: #2563eb;
    font-weight: 800;
}

.skill-text {
    color: #172554;
    font-weight: 650;
    font-size: 14px;
}

/* =====================================================
   INFO CARDS
   ===================================================== */

.info-card {
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 12px;
}

.info-card-title {
    color: #172554;
    font-size: 16px;
    font-weight: 750;
    margin-bottom: 6px;
}

.info-card-text {
    color: #64748b;
    font-size: 13px;
    line-height: 1.5;
}

/* =====================================================
   CERTIFICATIONS
   ===================================================== */

.cert-card {
    display: flex;
    align-items: center;
    gap: 15px;
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 16px 18px;
    margin-bottom: 10px;
}

.cert-number {
    width: 34px;
    height: 34px;
    min-width: 34px;
    border-radius: 50%;
    background: #eff6ff;
    color: #2563eb;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
}

.cert-title {
    color: #172554;
    font-weight: 750;
    font-size: 14px;
}

.cert-subtitle {
    color: #94a3b8;
    font-size: 12px;
    margin-top: 3px;
}

/* =====================================================
   JOB ROLES
   ===================================================== */

.role-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 17px 18px;
    margin-bottom: 7px;
}

.role-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 15px;
}

.role-name {
    color: #172554;
    font-size: 15px;
    font-weight: 750;
}

.score-badge {
    background: #eff6ff;
    color: #2563eb;
    border: 1px solid #dbeafe;
    border-radius: 999px;
    padding: 5px 10px;
    font-size: 12px;
    font-weight: 800;
    white-space: nowrap;
}

.role-label {
    color: #94a3b8;
    font-size: 12px;
    margin-top: 6px;
}

/* =====================================================
   RESULT HEADER
   ===================================================== */

.result-banner {
    background: #172554;
    color: white;
    border-radius: 20px;
    padding: 24px 26px;
    margin: 28px 0 20px 0;
}

.result-banner-title {
    font-size: 22px;
    font-weight: 800;
}

.result-banner-text {
    color: #cbd5e1;
    font-size: 13px;
    margin-top: 5px;
}

/* =====================================================
   FOOTER
   ===================================================== */

.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 12px;
    padding: 35px 0 10px 0;
}


/* =====================================================
   SIDEBAR REDESIGN
   ===================================================== */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1f46 0%, #172b59 100%);
    border-right: none;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 1.5rem 1rem;
}

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 11px;
    padding: 8px 6px 18px 6px;
}

.sidebar-logo {
    width: 42px;
    height: 42px;
    border-radius: 13px;
    background: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 23px;
}

.sidebar-brand-name {
    font-size: 19px;
    font-weight: 800;
    color: #ffffff;
}

.sidebar-brand-sub {
    color: #b8c7e6;
    font-size: 11px;
    margin-top: 2px;
}

.sidebar-intro {
    background: rgba(255,255,255,0.09);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 16px;
    margin: 4px 0 22px 0;
}

.sidebar-intro-title {
    color: #ffffff;
    font-size: 15px;
    font-weight: 750;
    margin-bottom: 6px;
}

.sidebar-intro-text {
    color: #c8d4eb;
    font-size: 12px;
    line-height: 1.55;
}

.sidebar-menu-title {
    color: #93a8d1;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.3px;
    margin: 0 6px 10px 6px;
}

.sidebar-item {
    display: flex;
    align-items: center;
    gap: 11px;
    padding: 12px 10px;
    border-radius: 13px;
    margin-bottom: 7px;
}

.sidebar-item.active {
    background: rgba(255,255,255,0.12);
}

.sidebar-item-icon {
    width: 34px;
    height: 34px;
    min-width: 34px;
    border-radius: 10px;
    background: rgba(255,255,255,0.10);
    display: flex;
    align-items: center;
    justify-content: center;
}

.sidebar-item b {
    display: block;
    color: #ffffff;
    font-size: 13px;
}

.sidebar-item small {
    display: block;
    color: #aebedc;
    font-size: 10px;
    margin-top: 2px;
}

.sidebar-divider {
    height: 1px;
    background: rgba(255,255,255,0.12);
    margin: 20px 5px;
}

.sidebar-tip {
    display: flex;
    gap: 10px;
    background: rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 13px;
}

.sidebar-tip-icon {
    font-size: 18px;
}

.sidebar-tip b {
    font-size: 12px;
    color: #ffffff;
}

.sidebar-tip p {
    color: #b8c7e6;
    font-size: 10px;
    line-height: 1.5;
    margin: 4px 0 0 0;
}

[data-testid="stSidebar"] button {
    background: #ffffff !important;
    color: #172554 !important;
    border: none !important;
}

/* =====================================================
   MOBILE
   ===================================================== */

@media (max-width: 768px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .hero {
        padding: 28px 18px;
    }

    .hero-title {
        font-size: 31px;
    }

    .hero-subtitle {
        font-size: 16px;
    }
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    render_html("""
    <div class="sidebar-brand">
        <div class="sidebar-logo">🎯</div>
        <div>
            <div class="sidebar-brand-name">Smart SkillPath</div>
            <div class="sidebar-brand-sub">Career Assistant</div>
        </div>
    </div>

    <div class="sidebar-intro">
        <div class="sidebar-intro-title">Find your next step</div>
        <div class="sidebar-intro-text">
            Discover the skills, certifications and roles
            connected to your career goal.
        </div>
    </div>

    <div class="sidebar-menu-title">YOUR JOURNEY</div>

    <div class="sidebar-item active">
        <span class="sidebar-item-icon">🎯</span>
        <div>
            <b>Career Goal</b>
            <small>Choose your target role</small>
        </div>
    </div>

    <div class="sidebar-item">
        <span class="sidebar-item-icon">💻</span>
        <div>
            <b>Your Skills</b>
            <small>Tell us what you know</small>
        </div>
    </div>

    <div class="sidebar-item">
        <span class="sidebar-item-icon">🚀</span>
        <div>
            <b>SkillPath</b>
            <small>Get your recommendations</small>
        </div>
    </div>

    <div class="sidebar-item">
        <span class="sidebar-item-icon">🏆</span>
        <div>
            <b>Career Options</b>
            <small>Explore roles & certifications</small>
        </div>
    </div>

    <div class="sidebar-divider"></div>

    <div class="sidebar-tip">
        <div class="sidebar-tip-icon">💡</div>
        <div>
            <b>Quick tip</b>
            <p>Select only the skills you are comfortable with for more meaningful recommendations.</p>
        </div>
    </div>
    """)

    if st.session_state.recommendation_result is not None:

        st.markdown("")

        if st.button(
            "↻  Start a New Path",
            use_container_width=True
        ):

            st.session_state.recommendation_result = None
            st.session_state.last_career = None
            st.session_state.last_skills = []
            st.rerun()


# HERO
# =========================================================

render_html("""
<div class="hero">
    <div class="hero-kicker">AI / ML CAREER ASSISTANT</div>
    <div class="hero-title">🎯 Smart SkillPath</div>
    <div class="hero-subtitle">Build a clearer path toward your IT career.</div>
    <div class="hero-description">
        Select your target career and the skills you already have.
        Smart SkillPath will identify relevant skills, certifications
        and job roles using your recommendation model.
    </div>
</div>
""")



# =========================================================
# INPUT AREA
# =========================================================

st.markdown(
    '<div class="section-heading">🚀 Build Your SkillPath</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subheading">'
    'Complete the two simple steps below. You can change your choices before generating your results.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# INPUTS
# =========================================================

# ---------------------------------------------------------
# STEP 1
# ---------------------------------------------------------

render_html("""
<div class="step-header">
    <div class="step-number">1</div>
    <div class="step-title">Choose your career goal</div>
</div>
<div class="step-description">
    Which IT career are you preparing for?
</div>
""")

career = st.selectbox(
    "Target career",
    list(CAREER_SKILLS.keys()),
    label_visibility="collapsed"
)

st.markdown("")


# ---------------------------------------------------------
# STEP 2
# ---------------------------------------------------------

render_html("""
<div class="step-header">
    <div class="step-number">2</div>
    <div class="step-title">Tell us about your current skills</div>
</div>
<div class="step-description">
    Select the skills you already know. You can choose more than one.
</div>
""")

# This field was missing. It now changes automatically
# according to the selected career.
selected_skills = st.multiselect(
    "Current skills",
    CAREER_SKILLS.get(career, []),
    placeholder="Select the skills you already know...",
    label_visibility="collapsed"
)

st.markdown("")

submitted = st.button(
    "🚀 Generate My Personalized SkillPath",
    use_container_width=True
)


# =========================================================
# FORM SUBMISSION
# =========================================================

if submitted:

    if not selected_skills:

        st.warning(
            "Please select at least one current skill before continuing."
        )

    else:

        with st.spinner(
            "Analyzing your skills and building your personalized path..."
        ):

            try:

                current_skills = ", ".join(selected_skills)

                result = recommend_skills(
                    current_skills,
                    career
                )

                st.session_state.recommendation_result = result
                st.session_state.last_career = career
                st.session_state.last_skills = selected_skills

            except Exception:

                st.error(
                    "We couldn't generate your SkillPath right now. "
                    "Please try again with a different skill selection."
                )


# =========================================================
# RESULTS
# =========================================================

result = st.session_state.recommendation_result

if result is not None:

    career = st.session_state.last_career
    selected_skills = st.session_state.last_skills

    skill_gap = list(
        dict.fromkeys(
            result.get("skill_gap", [])
        )
    )

    recommended_skills = list(
        dict.fromkeys(
            result.get("recommended_skills", [])
        )
    )

    certifications = list(
        dict.fromkeys(
            result.get("certifications", [])
        )
    )

    matching_roles = result.get(
        "matching_roles",
        []
    )


    # =====================================================
    # REMOVE ALREADY KNOWN SKILLS
    # =====================================================

    selected_lower = {
        str(skill).strip().lower()
        for skill in selected_skills
    }

    recommended_skills = [
        skill
        for skill in recommended_skills
        if str(skill).strip().lower()
        not in selected_lower
    ]

    skill_gap = [
        skill
        for skill in skill_gap
        if str(skill).strip().lower()
        not in selected_lower
    ]


    # =====================================================
    # RESULT BANNER
    # =====================================================

    render_html(f"""
<div class="result-banner">
    <div class="result-banner-title">📊 Your Personalized SkillPath</div>
    <div class="result-banner-text">
        Career goal: {safe(career)}
        &nbsp; • &nbsp;
        {len(selected_skills)} current skill(s) selected
    </div>
</div>
""")



    # =====================================================
    # OVERVIEW CARDS
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            card("Career Goal", career, "🎯"),
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            card(
                "Current Skills",
                str(len(selected_skills)),
                "💻"
            ),
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            card(
                "Skills to Focus On",
                str(len(skill_gap)),
                "🔍"
            ),
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            card(
                "Certifications",
                str(len(certifications)),
                "🏆"
            ),
            unsafe_allow_html=True
        )


    # =====================================================
    # RESULTS TABS
    # =====================================================

    st.markdown("")

    tab1, tab2, tab3 = st.tabs(
        [
            "📚 Skills",
            "🏆 Certifications",
            "💼 Job Roles"
        ]
    )


    # =====================================================
    # TAB 1 — SKILLS
    # =====================================================

    with tab1:

        st.markdown(
            '<div class="section-heading">💻 Your Current Skills</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-subheading">'
            'These are the skills you told us you already have.'
            '</div>',
            unsafe_allow_html=True
        )

        if selected_skills:

            cols = st.columns(3)

            for i, skill in enumerate(selected_skills):

                with cols[i % 3]:

                    st.markdown(
                        skill_card(
                            skill,
                            "✓"
                        ),
                        unsafe_allow_html=True
                    )

        else:

            st.info("No current skills selected.")


        st.markdown("---")


        # -------------------------------------------------
        # SKILL GAP
        # -------------------------------------------------

        st.markdown(
            '<div class="section-heading">🔍 Skills to Focus On</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-subheading">'
            'These are the skills returned by the recommendation model '
            'as areas to focus on next.'
            '</div>',
            unsafe_allow_html=True
        )

        if skill_gap:

            cols = st.columns(2)

            for i, skill in enumerate(skill_gap):

                with cols[i % 2]:

                    st.markdown(
                        skill_card(
                            skill,
                            "→"
                        ),
                        unsafe_allow_html=True
                    )

        else:

            st.success(
                "🎉 No additional skill gap was returned by the model."
            )


        st.markdown("---")


        # -------------------------------------------------
        # TOP RECOMMENDATIONS
        # -------------------------------------------------

        st.markdown(
            '<div class="section-heading">⭐ Recommended Skills</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-subheading">'
            'Prioritized skills from the ML recommendation model.'
            '</div>',
            unsafe_allow_html=True
        )

        if recommended_skills:

            cols = st.columns(2)

            for i, skill in enumerate(recommended_skills):

                with cols[i % 2]:

                    st.markdown(
                        skill_card(
                            skill,
                            "⭐"
                        ),
                        unsafe_allow_html=True
                    )

        else:

            st.info(
                "No additional skills were recommended."
            )


    # =====================================================
    # TAB 2 — CERTIFICATIONS
    # =====================================================

    with tab2:

        st.markdown(
            '<div class="section-heading">🏆 Recommended Certifications</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-subheading">'
            'Certifications associated with the relevant job profiles '
            'identified by the model.'
            '</div>',
            unsafe_allow_html=True
        )

        if certifications:

            for i, certification in enumerate(
                certifications,
                start=1
            ):

                st.markdown(
                    certification_card(
                        i,
                        certification
                    ),
                    unsafe_allow_html=True
                )

        else:

            st.info(
                "No certification recommendations were returned for this profile."
            )


        st.markdown("")


        st.markdown(
            info_card(
                "How to use these results",
                "Choose certifications that match the skills you want to develop next. "
                "The recommendations shown here come from the project's existing dataset and model.",
                "💡"
            ),
            unsafe_allow_html=True
        )


    # =====================================================
    # TAB 3 — JOB ROLES
    # =====================================================

    with tab3:

        st.markdown(
            '<div class="section-heading">💼 Matching Job Roles</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-subheading">'
            'The model compares your selected skills with relevant job-role skill profiles.'
            '</div>',
            unsafe_allow_html=True
        )

        if matching_roles:

            for role in matching_roles:

                if isinstance(role, dict):

                    role_name = role.get(
                        "role",
                        role.get(
                            "job_title",
                            "Unknown Role"
                        )
                    )

                    raw_score = role.get(
                        "similarity",
                        role.get(
                            "score",
                            0
                        )
                    )

                    try:
                        score = float(raw_score)
                    except (ValueError, TypeError):
                        score = 0.0

                    score = min(
                        max(score, 0.0),
                        100.0
                    )

                    st.markdown(
                        role_card(
                            role_name,
                            score
                        ),
                        unsafe_allow_html=True
                    )

                    st.progress(
                        score / 100
                    )

                else:

                    st.markdown(
                        skill_card(
                            role,
                            "💼"
                        ),
                        unsafe_allow_html=True
                    )

        else:

            st.info(
                "No matching job roles were returned by the model."
            )


    # =====================================================
    # COMPLETION MESSAGE
    # =====================================================

    st.markdown("---")

    st.success(
        "Your SkillPath is ready. Review the results above and use them to plan your next learning steps."
    )


# =========================================================
# FOOTER
# =========================================================

render_html("""
<div class="footer">
    🎯 <b>Smart SkillPath</b><br>
    AI/ML-Based Career & Skill Recommendation System
</div>
""")
