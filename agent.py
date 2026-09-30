import html
import gradio as gr

from agent_controller import (
    process_student_material,
    search_student_jobs,
    answer_student_question,
)


# ============================================================
# THEME
# ============================================================

THEME = gr.themes.Base(
    primary_hue="blue",
    secondary_hue="blue",
    neutral_hue="blue",
)


# ============================================================
# PROFESSIONAL BLUE + NAVY UI
# ============================================================

CSS = r"""
/* ============================================================
   GLOBAL
   ============================================================ */

:root {
    --blue-1: #0B5ED7;
    --blue-2: #1677E8;
    --blue-3: #2490F5;

    --navy: #062A55;
    --navy-2: #083B70;

    --cyan: #38D9FF;
    --gold: #FFD166;

    --page-1: #062A55;
    --page-2: #0B5ED7;
    --page-3: #1597EA;

    --card: rgba(6, 42, 85, 0.58);
    --card-2: rgba(5, 31, 65, 0.72);

    --white: #FFFFFF;
    --soft-white: #F4FBFF;

    --muted: #D9F3FF;

    --border: rgba(255, 255, 255, 0.28);
    --border-bright: rgba(56, 217, 255, 0.68);

    --shadow:
        0 18px 45px rgba(0, 18, 45, 0.28);
}


/* ============================================================
   PAGE
   ============================================================ */

.gradio-container {
    font-family:
        Inter,
        "Segoe UI",
        Arial,
        sans-serif !important;

    color: var(--white) !important;

    background:
        radial-gradient(
            circle at 10% 5%,
            rgba(56, 217, 255, 0.22),
            transparent 28%
        ),
        radial-gradient(
            circle at 90% 15%,
            rgba(255, 209, 102, 0.12),
            transparent 22%
        ),
        linear-gradient(
            135deg,
            var(--page-1) 0%,
            var(--page-2) 52%,
            var(--page-3) 100%
        ) !important;

    min-height: 100vh;
}


/* ============================================================
   ALL TEXT WHITE
   ============================================================ */

.gradio-container,
.gradio-container *,
label,
p,
span,
h1,
h2,
h3,
h4,
h5,
h6 {
    color: var(--white) !important;
}


/* ============================================================
   REMOVE DEFAULT BLACK LOOK
   ============================================================ */

input,
textarea,
select,
button,
.gradio-dropdown,
.gradio-textbox,
.gradio-number {
    color: var(--white) !important;
}


/* ============================================================
   MAIN WRAPPER
   ============================================================ */

#main-wrapper {
    width: 100% !important;
    max-width: 1380px !important;

    margin: 0 auto !important;

    padding: 28px 30px 60px !important;

    box-sizing: border-box !important;
}


/* ============================================================
   IMPORTANT:
   KEEP ALL MAJOR SECTIONS ON THE SAME WIDTH
   ============================================================ */

#main-wrapper .schedule-card,
#main-wrapper .result-card,
#main-wrapper .qa-card,
#main-wrapper .upload-card {
    box-sizing: border-box !important;

    width: 100% !important;

    max-width: 100% !important;

    margin-left: 0 !important;
    margin-right: 0 !important;
}


/* ============================================================
   HERO
   ============================================================ */

.hero-card {
    position: relative;

    width: 100% !important;

    box-sizing: border-box !important;

    padding: 36px 42px;

    margin-bottom: 34px;

    border-radius: 26px;

    background:
        linear-gradient(
            135deg,
            rgba(7, 52, 105, 0.90),
            rgba(16, 119, 218, 0.76)
        );

    border: 1px solid
        rgba(56, 217, 255, 0.48);

    box-shadow:
        0 20px 50px rgba(0, 20, 50, 0.30),
        inset 0 1px 0
        rgba(255, 255, 255, 0.25);

    overflow: hidden;
}

.hero-card::before {
    content: "";

    position: absolute;

    top: 0;
    left: 0;
    right: 0;

    height: 4px;

    background:
        linear-gradient(
            90deg,
            var(--cyan),
            #FFFFFF,
            var(--gold),
            var(--cyan)
        );

    opacity: 0.95;
}

.hero-card::after {
    content: "";

    position: absolute;

    inset: 9px;

    border-radius: 19px;

    border: 1px solid
        rgba(255, 255, 255, 0.11);

    pointer-events: none;
}

.hero-title {
    font-size: 38px !important;
    line-height: 1.15 !important;

    font-weight: 800 !important;

    text-align: center;

    margin: 0 0 12px !important;

    letter-spacing: -0.5px;
}

.hero-subtitle {
    font-size: 17px !important;
    line-height: 1.65 !important;

    text-align: center;

    margin: 0 auto !important;

    max-width: 950px;

    color: var(--soft-white) !important;
}


/* ============================================================
   SECTION
   ============================================================ */

.section {
    width: 100% !important;

    box-sizing: border-box !important;

    margin-top: 30px;
    margin-bottom: 30px;
}

.section-heading {
    font-size: 27px !important;

    font-weight: 800 !important;

    margin-bottom: 5px !important;

    letter-spacing: -0.2px;
}

.section-description {
    font-size: 15px !important;

    color: var(--muted) !important;

    margin-bottom: 18px !important;
}


/* ============================================================
   UPLOAD CARDS
   ============================================================ */

.upload-card {
    position: relative;

    box-sizing: border-box !important;

    padding: 18px;

    min-height: 315px;

    border-radius: 22px;

    background:
        linear-gradient(
            145deg,
            rgba(9, 58, 116, 0.80),
            rgba(5, 35, 74, 0.72)
        );

    border: 1px solid
        rgba(56, 217, 255, 0.52);

    box-shadow:
        var(--shadow),
        inset 0 1px 0
        rgba(255, 255, 255, 0.18);

    overflow: hidden;
}

.upload-card::before {
    content: "";

    position: absolute;

    top: 0;
    left: 0;
    right: 0;

    height: 3px;

    background:
        linear-gradient(
            90deg,
            var(--cyan),
            var(--gold)
        );
}

.upload-card::after {
    content: "";

    position: absolute;

    inset: 8px;

    border-radius: 16px;

    border: 1px solid
        rgba(255, 255, 255, 0.09);

    pointer-events: none;
}

.upload-title {
    font-size: 19px !important;

    font-weight: 800 !important;

    margin: 0 0 12px !important;

    text-align: center;
}


/* ============================================================
   GRADIO FILE UPLOAD
   ============================================================ */

.upload-card .file-preview,
.upload-card .upload-container,
.upload-card .wrap,
.upload-card [data-testid="file-upload"] {
    background:
        rgba(255, 255, 255, 0.075) !important;

    border: 1px solid
        rgba(255, 255, 255, 0.34) !important;

    border-radius: 16px !important;

    box-sizing: border-box !important;

    width: 100% !important;
}

.upload-card .upload-container {
    min-height: 210px !important;

    display: flex !important;

    align-items: center !important;
    justify-content: center !important;

    box-shadow:
        inset 0 0 0 1px
        rgba(56, 217, 255, 0.13);
}

.upload-card .upload-container *,
.upload-card .file-preview * {
    color: #FFFFFF !important;
}

.upload-card button {
    color: #FFFFFF !important;

    background:
        rgba(255, 255, 255, 0.10) !important;

    border: 1px solid
        rgba(255, 255, 255, 0.34) !important;

    border-radius: 10px !important;

    font-weight: 700 !important;
}


/* ============================================================
   FILE NAME / PREVIEW
   ============================================================ */

.upload-card .file-preview {
    color: #FFFFFF !important;

    background:
        linear-gradient(
            135deg,
            rgba(5, 48, 96, 0.95),
            rgba(9, 78, 145, 0.92)
        ) !important;

    border: 1px solid
        rgba(56, 217, 255, 0.55) !important;

    min-height: 210px !important;
}

.upload-card .file-preview span,
.upload-card .file-preview p,
.upload-card .file-preview div {
    color: #FFFFFF !important;
}


/* ============================================================
   IMPROVED X / REMOVE BUTTON
   ============================================================ */

.upload-card button[aria-label*="Remove"],
.upload-card button[aria-label*="remove"],
.upload-card button[title*="Remove"],
.upload-card button[title*="remove"],
.upload-card .file-preview button,
.upload-card .upload-container button {
    opacity: 1 !important;

    visibility: visible !important;

    color: #FFFFFF !important;

    background:
        rgba(7, 38, 77, 0.96) !important;

    border: 2px solid
        rgba(255, 255, 255, 0.78) !important;

    border-radius: 50% !important;

    width: 34px !important;
    height: 34px !important;

    min-width: 34px !important;
    min-height: 34px !important;

    display: flex !important;

    align-items: center !important;
    justify-content: center !important;

    font-size: 19px !important;

    font-weight: 900 !important;

    box-shadow:
        0 5px 16px rgba(0, 0, 0, 0.35) !important;

    z-index: 50 !important;
}

.upload-card button[aria-label*="Remove"]:hover,
.upload-card button[aria-label*="remove"]:hover,
.upload-card button[title*="Remove"]:hover,
.upload-card button[title*="remove"]:hover,
.upload-card .file-preview button:hover {
    background:
        #D7263D !important;

    border-color:
        #FFFFFF !important;

    transform:
        scale(1.08) !important;
}


/* ============================================================
   UPLOAD STATUS
   ============================================================ */

.upload-status {
    margin-top: 10px !important;

    padding: 9px 12px !important;

    border-radius: 10px !important;

    background:
        rgba(255, 255, 255, 0.075) !important;

    border: 1px solid
        rgba(255, 255, 255, 0.20) !important;

    font-size: 13px !important;

    text-align: center !important;

    min-height: 22px !important;

    box-sizing: border-box !important;

    width: 100% !important;
}


/* ============================================================
   SCHEDULE CARD
   ============================================================ */

.schedule-card {
    box-sizing: border-box !important;

    width: 100% !important;

    max-width: 100% !important;

    padding: 22px;

    border-radius: 20px;

    background:
        linear-gradient(
            145deg,
            rgba(7, 50, 101, 0.82),
            rgba(4, 33, 70, 0.76)
        );

    border: 1px solid
        rgba(255, 209, 102, 0.42);

    box-shadow:
        var(--shadow),
        inset 0 1px 0
        rgba(255, 255, 255, 0.16);

    margin-left: 0 !important;
    margin-right: 0 !important;
}

.schedule-label {
    font-size: 15px !important;

    font-weight: 700 !important;
}

.schedule-card .gr-row {
    width: 100% !important;

    box-sizing: border-box !important;

    margin-left: 0 !important;
    margin-right: 0 !important;
}

.schedule-card .gr-column {
    min-width: 0 !important;

    box-sizing: border-box !important;
}


/* ============================================================
   INPUTS
   ============================================================ */

.gradio-container input,
.gradio-container textarea,
.gradio-container select {
    background:
        rgba(4, 32, 67, 0.88) !important;

    color: #FFFFFF !important;

    border: 1px solid
        rgba(255, 255, 255, 0.30) !important;

    border-radius: 12px !important;

    box-sizing: border-box !important;
}

.gradio-container input:focus,
.gradio-container textarea:focus,
.gradio-container select:focus {
    border-color:
        var(--cyan) !important;

    box-shadow:
        0 0 0 2px
        rgba(56, 217, 255, 0.15) !important;
}


/* ============================================================
   DROPDOWN / SELECT CONSISTENCY
   ============================================================ */

#main-wrapper .gr-dropdown,
#main-wrapper .gr-dropdown-container,
#main-wrapper .gr-dropdown .wrap,
#main-wrapper .gr-dropdown > div {
    box-sizing: border-box !important;

    width: 100% !important;

    max-width: 100% !important;
}


/* ============================================================
   BUTTON
   ============================================================ */

#analyze-button {
    margin-top: 20px;

    width: 100% !important;

    box-sizing: border-box !important;

    min-height: 56px !important;

    border-radius: 15px !important;

    background:
        linear-gradient(
            135deg,
            #0D63D8,
            #2097F5
        ) !important;

    color: #FFFFFF !important;

    border: 1px solid
        rgba(255, 255, 255, 0.38) !important;

    box-shadow:
        0 10px 25px
        rgba(0, 30, 75, 0.28),
        inset 0 1px 0
        rgba(255, 255, 255, 0.25);

    font-size: 16px !important;

    font-weight: 800 !important;

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease,
        filter 0.18s ease !important;
}

#analyze-button:hover {
    transform:
        translateY(-2px) !important;

    filter:
        brightness(1.08) !important;

    box-shadow:
        0 14px 30px
        rgba(0, 40, 100, 0.38),
        0 0 18px
        rgba(56, 217, 255, 0.16) !important;
}


/* ============================================================
   CLEAR BUTTON
   ============================================================ */

#clear-button {
    width: 100% !important;

    box-sizing: border-box !important;

    min-height: 50px !important;

    border-radius: 13px !important;

    background:
        rgba(255, 255, 255, 0.08) !important;

    color: #FFFFFF !important;

    border: 1px solid
        rgba(255, 255, 255, 0.28) !important;

    font-weight: 700 !important;
}

#clear-button:hover {
    background:
        rgba(215, 38, 61, 0.80) !important;

    border-color:
        rgba(255, 255, 255, 0.55) !important;
}


/* ============================================================
   RESULT CARDS
   ============================================================ */

.result-card {
    position: relative;

    box-sizing: border-box !important;

    width: 100% !important;

    max-width: 100% !important;

    padding: 24px;

    margin-top: 10px;

    margin-left: 0 !important;
    margin-right: 0 !important;

    border-radius: 20px;

    background:
        linear-gradient(
            145deg,
            rgba(5, 43, 88, 0.90),
            rgba(3, 29, 62, 0.82)
        );

    border: 1px solid
        rgba(56, 217, 255, 0.34);

    box-shadow:
        var(--shadow),
        inset 0 1px 0
        rgba(255, 255, 255, 0.14);
}

.result-card::before {
    content: "";

    position: absolute;

    left: 0;
    top: 0;
    bottom: 0;

    width: 4px;

    border-radius: 20px 0 0 20px;

    background:
        linear-gradient(
            180deg,
            var(--cyan),
            var(--gold)
        );
}

.result-title {
    font-size: 20px !important;

    font-weight: 800 !important;

    margin-bottom: 14px !important;
}


/* ============================================================
   PERFORMANCE
   ============================================================ */

.performance-grid {
    display: grid;

    grid-template-columns:
        repeat(
            auto-fit,
            minmax(220px, 1fr)
        );

    gap: 14px;

    width: 100%;

    box-sizing: border-box;
}

.performance-item {
    padding: 17px;

    border-radius: 15px;

    background:
        rgba(255, 255, 255, 0.075);

    border: 1px solid
        rgba(255, 255, 255, 0.20);

    box-shadow:
        inset 0 1px 0
        rgba(255, 255, 255, 0.12);

    box-sizing: border-box;

    min-width: 0;
}

.performance-subject {
    font-size: 16px;

    font-weight: 800;

    margin-bottom: 8px;
}

.grade-badge {
    display: inline-block;

    padding: 5px 11px;

    margin-right: 6px;

    border-radius: 999px;

    background:
        rgba(56, 217, 255, 0.16);

    border: 1px solid
        rgba(56, 217, 255, 0.50);

    font-weight: 800;
}

.priority-text {
    margin-top: 9px;

    color: var(--muted) !important;

    font-size: 13px;
}


/* ============================================================
   STUDY DAYS
   ============================================================ */

.study-day {
    margin-bottom: 16px;

    padding: 19px;

    border-radius: 17px;

    background:
        rgba(255, 255, 255, 0.065);

    border: 1px solid
        rgba(255, 255, 255, 0.21);

    box-shadow:
        inset 0 1px 0
        rgba(255, 255, 255, 0.10);

    box-sizing: border-box;

    width: 100%;
}

.day-title {
    font-size: 21px;

    font-weight: 800;

    margin-bottom: 12px;
}

.day-total {
    float: right;

    font-size: 14px;

    padding: 5px 10px;

    border-radius: 999px;

    background:
        rgba(255, 209, 102, 0.14);

    border: 1px solid
        rgba(255, 209, 102, 0.42);
}

.study-row {
    display: flex;

    justify-content: space-between;

    gap: 15px;

    padding: 10px 0;

    border-bottom:
        1px solid
        rgba(255, 255, 255, 0.10);

    box-sizing: border-box;

    width: 100%;
}

.study-row:last-child {
    border-bottom: none;
}

.study-subject {
    font-weight: 750;
}

.study-topic {
    color: var(--muted) !important;

    font-size: 13px;
}

.study-hours {
    white-space: nowrap;

    font-weight: 800;

    color: var(--cyan) !important;
}


/* ============================================================
   COVERAGE
   ============================================================ */

.coverage-subject {
    margin-bottom: 17px;

    padding: 17px;

    border-radius: 16px;

    background:
        rgba(255, 255, 255, 0.065);

    border: 1px solid
        rgba(255, 255, 255, 0.21);

    box-sizing: border-box;

    width: 100%;
}

.coverage-subject-title {
    font-size: 18px;

    font-weight: 800;

    margin-bottom: 11px;
}

.topic-badge {
    display: inline-block;

    margin: 4px;

    padding: 7px 11px;

    border-radius: 999px;

    font-size: 13px;

    border: 1px solid
        rgba(255, 255, 255, 0.26);
}

.topic-covered {
    background:
        rgba(28, 200, 138, 0.18);

    border-color:
        rgba(28, 200, 138, 0.65);
}

.topic-missing {
    background:
        rgba(255, 193, 7, 0.15);

    border-color:
        rgba(255, 209, 102, 0.68);
}


/* ============================================================
   ASK YOUR MATERIAL / Q&A
   ============================================================ */

.qa-card {
    position: relative;

    box-sizing: border-box;

    width: 100% !important;

    max-width: 100% !important;

    padding: 22px;

    margin-left: 0 !important;
    margin-right: 0 !important;

    border-radius: 20px;

    background:
        linear-gradient(
            145deg,
            rgba(5, 43, 88, 0.90),
            rgba(3, 29, 62, 0.82)
        );

    border: 1px solid
        rgba(56, 217, 255, 0.38);

    box-shadow:
        var(--shadow),
        inset 0 1px 0
        rgba(255, 255, 255, 0.14);

    overflow: hidden;
}

.qa-card::before {
    content: "";

    position: absolute;

    left: 0;
    top: 0;
    bottom: 0;

    width: 4px;

    background:
        linear-gradient(
            180deg,
            var(--cyan),
            var(--gold)
        );
}

.qa-title {
    font-size: 19px !important;

    font-weight: 800 !important;

    margin-bottom: 8px !important;
}

.qa-description {
    color: var(--muted) !important;

    font-size: 14px !important;

    margin-bottom: 16px !important;
}

.qa-examples {
    margin-top: 12px;

    padding: 12px 14px;

    border-radius: 12px;

    background:
        rgba(255, 255, 255, 0.055);

    border: 1px solid
        rgba(255, 255, 255, 0.14);

    font-size: 13px;

    line-height: 1.7;

    box-sizing: border-box;

    width: 100%;
}

.qa-answer {
    margin-top: 16px;

    padding: 17px 19px;

    border-radius: 15px;

    background:
        rgba(56, 217, 255, 0.09);

    border: 1px solid
        rgba(56, 217, 255, 0.38);

    box-shadow:
        inset 0 1px 0
        rgba(255, 255, 255, 0.08);

    box-sizing: border-box;

    width: 100%;
}

.qa-answer-label {
    font-size: 13px;

    font-weight: 800;

    color: var(--cyan) !important;

    margin-bottom: 6px;
}

.qa-answer-text {
    font-size: 15px;

    line-height: 1.6;

    color: #FFFFFF !important;
}


/* ============================================================
   Q&A ROW ALIGNMENT FIX
   ============================================================ */

/*
   IMPORTANT FIX:

   The textbox has a label above it, while the Ask button
   does not have a label.

   Therefore Gradio normally places the Ask button slightly
   higher than the textbox.

   Align the actual controls to the bottom.
*/

.qa-card .gr-row {
    width: 100% !important;

    box-sizing: border-box !important;

    align-items: flex-end !important;

    margin-left: 0 !important;
    margin-right: 0 !important;
}


/* Keep textbox and button columns flexible */
.qa-card .gr-row > .gr-column {
    min-width: 0 !important;

    box-sizing: border-box !important;
}


/* Make Ask button exactly match the input control height */
#qa-button {
    height: 48px !important;

    min-height: 48px !important;

    max-height: 48px !important;

    margin-top: 0 !important;

    align-self: flex-end !important;

    box-sizing: border-box !important;

    border-radius: 13px !important;

    background:
        linear-gradient(
            135deg,
            #0D63D8,
            #2097F5
        ) !important;

    color: #FFFFFF !important;

    border: 1px solid
        rgba(255, 255, 255, 0.38) !important;

    font-size: 15px !important;

    font-weight: 800 !important;

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease,
        filter 0.18s ease !important;
}

#qa-button:hover {
    transform:
        translateY(-2px) !important;

    filter:
        brightness(1.08) !important;

    box-shadow:
        0 12px 27px
        rgba(0, 40, 100, 0.34),
        0 0 16px
        rgba(56, 217, 255, 0.14) !important;
}


/* ============================================================
   JOBS SECTION
   ============================================================ */

#main-wrapper > .gr-row {
    width: 100% !important;

    max-width: 100% !important;

    box-sizing: border-box !important;

    margin-left: 0 !important;
    margin-right: 0 !important;
}


/*
   IMPORTANT FIX:

   Location has an info text below its label, while
   Experience does not.

   flex-end makes the actual dropdown controls line up
   perfectly at the bottom.
*/

#main-wrapper > .gr-row {
    align-items: flex-end !important;
}


/* City and Experience */
#main-wrapper > .gr-row > .gr-column {
    flex: 1 1 0 !important;

    width: 0 !important;

    min-width: 0 !important;

    max-width: none !important;

    box-sizing: border-box !important;
}


/* Job dropdown containers */
#main-wrapper > .gr-row .gr-dropdown,
#main-wrapper > .gr-row .gr-dropdown-container,
#main-wrapper > .gr-row .wrap {
    width: 100% !important;

    max-width: 100% !important;

    box-sizing: border-box !important;
}


/*
   Make the actual dropdown controls the same height.
*/

#main-wrapper > .gr-row .gr-dropdown button,
#main-wrapper > .gr-row .gr-dropdown > div,
#main-wrapper > .gr-row .gr-dropdown-container button {
    min-height: 44px !important;

    height: 44px !important;

    box-sizing: border-box !important;
}


/* ============================================================
   JOB CARDS
   ============================================================ */

.job-card {
    margin-bottom: 14px;

    padding: 18px;

    border-radius: 16px;

    background:
        rgba(255, 255, 255, 0.065);

    border: 1px solid
        rgba(255, 255, 255, 0.20);

    box-sizing: border-box;

    width: 100%;

    max-width: 100%;
}

.job-title {
    font-size: 17px;

    font-weight: 800;
}

.job-company {
    margin-top: 5px;

    color: var(--muted) !important;
}

.job-meta {
    margin-top: 8px;

    font-size: 13px;

    color: var(--muted) !important;
}

.job-link {
    display: inline-block;

    margin-top: 11px;

    padding: 7px 12px;

    border-radius: 9px;

    background:
        rgba(56, 217, 255, 0.12);

    border: 1px solid
        rgba(56, 217, 255, 0.42);

    color: #FFFFFF !important;

    text-decoration: none;
}

.job-link:hover {
    background:
        rgba(56, 217, 255, 0.22);
}


/* ============================================================
   JOBS OUTPUT
   ============================================================ */

#main-wrapper .result-card {
    overflow: hidden;

    word-wrap: break-word;

    overflow-wrap: anywhere;
}


/* ============================================================
   LIGHT MODE - SETTINGS / NATIVE GRADIO TEXT FIX
   ============================================================ */

html.light .settings *,
body.light .settings *,
html[data-theme="light"] .settings *,
body[data-theme="light"] .settings *,
html.light .gradio-settings *,
body.light .gradio-settings *,
html[data-theme="light"] .gradio-settings *,
body[data-theme="light"] .gradio-settings * {
    color: #102A43 !important;
}

html.light .settings input,
html.light .settings textarea,
html.light .settings select,
body.light .settings input,
body.light .settings textarea,
body.light .settings select,
html[data-theme="light"] .settings input,
html[data-theme="light"] .settings textarea,
html[data-theme="light"] .settings select,
body[data-theme="light"] .settings input,
body[data-theme="light"] .settings textarea,
body[data-theme="light"] .settings select {
    color: #102A43 !important;

    background: #FFFFFF !important;

    border-color: #C7D7EA !important;
}

html.light .gradio-settings input,
html.light .gradio-settings textarea,
html.light .gradio-settings select,
body.light .gradio-settings input,
body.light .gradio-settings textarea,
body.light .gradio-settings select,
html[data-theme="light"] .gradio-settings input,
html[data-theme="light"] .gradio-settings textarea,
html[data-theme="light"] .gradio-settings select,
body[data-theme="light"] .gradio-settings input,
body[data-theme="light"] .gradio-settings textarea,
body[data-theme="light"] .gradio-settings select {
    color: #102A43 !important;

    background: #FFFFFF !important;

    border-color: #C7D7EA !important;
}


/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 900px) {

    #main-wrapper {
        padding: 20px 15px 45px !important;
    }

    .hero-card {
        padding: 28px 20px;
    }

    .hero-title {
        font-size: 30px !important;
    }

    .hero-subtitle {
        font-size: 15px !important;
    }
}


@media (max-width: 700px) {

    .upload-card {
        min-height: 290px;
    }

    .upload-card .upload-container,
    .upload-card .file-preview {
        min-height: 190px !important;
    }

    .study-row {
        flex-direction: column;
        gap: 5px;
    }

    .day-total {
        float: none;
        margin-left: 8px;
    }

    #main-wrapper > .gr-row {
        flex-direction: column !important;

        align-items: stretch !important;
    }

    #main-wrapper > .gr-row > .gr-column {
        width: 100% !important;
        max-width: 100% !important;
    }

    #main-wrapper .schedule-card,
    #main-wrapper .qa-card,
    #main-wrapper .result-card,
    #main-wrapper .upload-card {
        width: 100% !important;
        max-width: 100% !important;
    }

    /*
       On mobile, let the Ask button return to normal
       full-width behavior.
    */

    .qa-card .gr-row {
        align-items: stretch !important;
        flex-direction: column !important;
    }

    #qa-button {
        width: 100% !important;

        max-width: 100% !important;

        height: 48px !important;

        min-height: 48px !important;

        margin-top: 10px !important;
    }
}
"""


# ============================================================
# HTML HELPERS
# ============================================================

def safe_text(value):

    return html.escape(
        str(value)
    )


# ============================================================
# PERFORMANCE FORMATTER
# ============================================================

def format_performance(performance):

    if not performance:

        return """
        <div class="result-card">
            <div class="result-title">
                Academic Performance
            </div>

            <p>
                No transcript was uploaded.
                Upload a transcript to analyze grades.
            </p>
        </div>
        """

    cards = []

    for item in performance:

        subject = safe_text(
            item.get(
                "subject",
                "Unknown Subject"
            )
        )

        grade = safe_text(
            item.get(
                "grade",
                "-"
            )
        )

        status = safe_text(
            item.get(
                "status",
                ""
            )
        )

        priority = safe_text(
            item.get(
                "priority",
                ""
            )
        )

        cards.append(
            f"""
            <div class="performance-item">

                <div class="performance-subject">
                    {subject}
                </div>

                <span class="grade-badge">
                    Grade: {grade}
                </span>

                <span class="grade-badge">
                    {status}
                </span>

                <div class="priority-text">
                    {priority}
                </div>

            </div>
            """
        )

    return f"""
    <div class="result-card">

        <div class="result-title">
            Academic Performance
        </div>

        <div class="performance-grid">
            {''.join(cards)}
        </div>

    </div>
    """


# ============================================================
# STUDY PLAN FORMATTER
# ============================================================

def format_schedule(plan):

    if not plan:

        return """
        <div class="result-card">
            No study plan could be generated.
        </div>
        """

    entries = plan.get(
        "entries",
        []
    )

    if not entries:

        return f"""
        <div class="result-card">

            <div class="result-title">
                Study Plan
            </div>

            <p>
                {safe_text(
                    plan.get(
                        "message",
                        "No plan available."
                    )
                )}
            </p>

        </div>
        """

    days = plan.get(
        "days",
        1
    )

    hours = plan.get(
        "hours_per_day",
        2
    )

    total_hours = plan.get(
        "total_hours",
        days * hours
    )

    html_parts = [
        f"""
        <div class="result-card">

            <div class="result-title">
                Study Plan
            </div>

            <p>
                {days} day(s) •
                {hours} hour(s) per day •
                {total_hours} total hours
            </p>
        """
    ]

    for day in entries:

        day_number = day.get(
            "day",
            1
        )

        day_hours = day.get(
            "hours",
            hours
        )

        rows = []

        for item in day.get(
            "items",
            []
        ):

            subject = safe_text(
                item.get(
                    "subject",
                    "Study"
                )
            )

            topic = safe_text(
                item.get(
                    "topic",
                    "Revision"
                )
            )

            item_hours = item.get(
                "hours",
                1
            )

            rows.append(
                f"""
                <div class="study-row">

                    <div>
                        <div class="study-subject">
                            {subject}
                        </div>

                        <div class="study-topic">
                            {topic}
                        </div>
                    </div>

                    <div class="study-hours">
                        {item_hours} hour(s)
                    </div>

                </div>
                """
            )

        html_parts.append(
            f"""
            <div class="study-day">

                <div class="day-title">
                    Day {day_number}

                    <span class="day-total">
                        {day_hours} hour(s)
                    </span>
                </div>

                {''.join(rows)}

            </div>
            """
        )

    html_parts.append(
        "</div>"
    )

    return "".join(html_parts)


# ============================================================
# COVERAGE FORMATTER
# ============================================================

def format_coverage(coverage):

    if not coverage:

        return """
        <div class="result-card">
            No syllabus coverage information available.
        </div>
        """

    subjects = coverage.get(
        "subjects",
        []
    )

    if not subjects:

        return f"""
        <div class="result-card">

            <div class="result-title">
                Syllabus Coverage
            </div>

            <p>
                {safe_text(
                    coverage.get(
                        "message",
                        "No syllabus uploaded."
                    )
                )}
            </p>

        </div>
        """

    blocks = []

    for subject_data in subjects:

        subject = safe_text(
            subject_data.get(
                "subject",
                "Subject"
            )
        )

        topic_badges = []

        for topic_data in subject_data.get(
            "topics",
            []
        ):

            topic = safe_text(
                topic_data.get(
                    "topic",
                    ""
                )
            )

            covered = bool(
                topic_data.get(
                    "covered",
                    False
                )
            )

            if covered:

                topic_badges.append(
                    f"""
                    <span class="topic-badge topic-covered">
                        ✓ {topic}
                    </span>
                    """
                )

            else:

                topic_badges.append(
                    f"""
                    <span class="topic-badge topic-missing">
                        ! {topic}
                    </span>
                    """
                )

        blocks.append(
            f"""
            <div class="coverage-subject">

                <div class="coverage-subject-title">
                    {subject}
                </div>

                {''.join(topic_badges)}

            </div>
            """
        )

    return f"""
    <div class="result-card">

        <div class="result-title">
            Syllabus Coverage
        </div>

        <p>
            {safe_text(
                coverage.get(
                    "message",
                    ""
                )
            )}
        </p>

        {''.join(blocks)}

    </div>
    """


# ============================================================
# JOB FORMATTER
# ============================================================

def format_jobs(jobs):

    if not jobs:

        return """
        <div class="result-card">

            <div class="result-title">
                Jobs & Internships
            </div>

            <p>
                No job information available yet.
            </p>

        </div>
        """

    if jobs.get("error"):

        return f"""
        <div class="result-card">

            <div class="result-title">
                Jobs & Internships
            </div>

            <p>
                {safe_text(
                    jobs.get("error")
                )}
            </p>

        </div>
        """

    job_list = jobs.get(
        "jobs",
        []
    )

    keywords = jobs.get(
        "search_keywords",
        []
    )

    role_averages = jobs.get(
        "role_averages",
        {}
    )

    if not job_list:

        message = jobs.get(
            "message",
            "No matching jobs were found."
        )

        return f"""
        <div class="result-card">

            <div class="result-title">
                Jobs & Internships
            </div>

            <p>
                {safe_text(message)}
            </p>

            <p>
                Search based on:
                {safe_text(
                    ", ".join(keywords)
                    if keywords
                    else "uploaded coursework"
                )}
            </p>

        </div>
        """

    average_html = ""

    if role_averages:

        average_items = []

        for role, average in role_averages.items():

            if average is None:
                continue

            average_items.append(
                f"""
                <span class="topic-badge topic-covered">
                    {safe_text(role)}:
                    ₹{average:,.0f} average
                </span>
                """
            )

        if average_items:

            average_html = f"""
            <div style="margin-bottom:18px;">
                {''.join(average_items)}
            </div>
            """

    cards = []

    for job in job_list[:30]:

        title = safe_text(
            job.get(
                "title",
                "Unknown Role"
            )
        )

        company = safe_text(
            job.get(
                "company",
                "Unknown Company"
            )
        )

        location = safe_text(
            job.get(
                "location",
                "Location not specified"
            )
        )

        experience = safe_text(
            job.get(
                "experience",
                "Fresher"
            )
        )

        keyword = safe_text(
            job.get(
                "keyword",
                ""
            )
        )

        url = job.get(
            "url",
            ""
        )

        salary_min = job.get(
            "salary_min"
        )

        salary_max = job.get(
            "salary_max"
        )

        salary_text = ""

        if (
            salary_min is not None
            and salary_max is not None
        ):

            try:
                salary_text = (
                    f"₹{float(salary_min):,.0f}"
                    f" – "
                    f"₹{float(salary_max):,.0f}"
                )
            except Exception:
                salary_text = ""

        elif salary_min is not None:

            try:
                salary_text = (
                    f"From ₹{float(salary_min):,.0f}"
                )
            except Exception:
                pass

        elif salary_max is not None:

            try:
                salary_text = (
                    f"Up to ₹{float(salary_max):,.0f}"
                )
            except Exception:
                pass

        link_html = ""

        if url:

            safe_url = html.escape(
                url,
                quote=True
            )

            link_html = (
                f"""
                <a
                    class="job-link"
                    href="{safe_url}"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    View Job
                </a>
                """
            )

        cards.append(
            f"""
            <div class="job-card">

                <div class="job-title">
                    {title}
                </div>

                <div class="job-company">
                    {company}
                </div>

                <div class="job-meta">
                    {location}
                    • {experience}
                    • {keyword}
                </div>

                {
                    f'<div class="job-meta">Salary: {salary_text}</div>'
                    if salary_text
                    else ''
                }

                {link_html}

            </div>
            """
        )

    return f"""
    <div class="result-card">

        <div class="result-title">
            Jobs & Internships
        </div>

        <p>
            Matching opportunities were searched using
            skills inferred from the uploaded academic material.
        </p>

        {average_html}

        {''.join(cards)}

    </div>
    """


# ============================================================
# UPLOAD STATUS
# ============================================================

def upload_status(
    file_path,
    name
):

    if not file_path:

        return f"""
        <div class="upload-status">
            No {safe_text(name)} uploaded
        </div>
        """

    filename = safe_text(
        str(file_path).replace(
            "\\",
            "/"
        ).split("/")[-1]
    )

    return f"""
    <div class="upload-status">
        ✓ {safe_text(name)} uploaded:
        <strong>{filename}</strong>
    </div>
    """


# ============================================================
# MAIN PROCESS
# ============================================================

def process_all(
    transcript_file,
    syllabus_file,
    notes_file,
    days,
    hours_per_day
):

    try:

        result = process_student_material(
            transcript_file=transcript_file,
            syllabus_file=syllabus_file,
            notes_file=notes_file,
            days=int(days or 1),
            hours_per_day=int(
                hours_per_day or 2
            )
        )

        if not result.get(
            "success",
            False
        ):

            error = result.get(
                "message",
                "Unknown processing error."
            )

            error_html = f"""
            <div class="result-card">

                <div class="result-title">
                    Processing Error
                </div>

                <p>
                    {safe_text(error)}
                </p>

            </div>
            """

            return (
                error_html,
                error_html,
                error_html,
                error_html,
                result
            )

        return (
            format_performance(
                result.get(
                    "performance",
                    []
                )
            ),

            format_schedule(
                result.get(
                    "study_plan",
                    {}
                )
            ),

            format_coverage(
                result.get(
                    "coverage",
                    {}
                )
            ),

            format_jobs(
                result.get(
                    "jobs",
                    {}
                )
            ),

            result
        )

    except Exception as error:

        error_html = f"""
        <div class="result-card">

            <div class="result-title">
                Processing Error
            </div>

            <p>
                {safe_text(error)}
            </p>

        </div>
        """

        return (
            error_html,
            error_html,
            error_html,
            error_html,
            None
        )


# ============================================================
# MANUAL JOB SEARCH
# ============================================================

def find_jobs(
    state,
    location,
    experience
):

    if not state:

        return """
        <div class="result-card">

            <div class="result-title">
                Jobs & Internships
            </div>

            <p>
                Analyze your academic material first.
            </p>

        </div>
        """

    subjects = state.get(
        "subjects",
        []
    )

    try:

        jobs = search_student_jobs(
            subjects=subjects,
            location=location or "Hyderabad",
            experience=experience or "Fresher"
        )

        return format_jobs(jobs)

    except Exception as error:

        return f"""
        <div class="result-card">

            <div class="result-title">
                Jobs & Internships
            </div>

            <p>
                {safe_text(error)}
            </p>

        </div>
        """


# ============================================================
# BASIC Q&A
# ============================================================

def ask_material(
    question,
    state
):

    if not question or not str(question).strip():

        return """
        <div class="qa-answer">
            <div class="qa-answer-label">
                Answer
            </div>

            <div class="qa-answer-text">
                Type a question about your transcript,
                syllabus, notes, study plan, or the agent.
            </div>
        </div>
        """

    try:

        answer = answer_student_question(
            str(question).strip(),
            state
        )

        return f"""
        <div class="qa-answer">

            <div class="qa-answer-label">
                Answer
            </div>

            <div class="qa-answer-text">
                {safe_text(answer)}
            </div>

        </div>
        """

    except Exception as error:

        return f"""
        <div class="qa-answer">

            <div class="qa-answer-label">
                Answer
            </div>

            <div class="qa-answer-text">
                {safe_text(error)}
            </div>

        </div>
        """


# ============================================================
# CITY LIST
# ============================================================

CITIES = [
    "Hyderabad",
    "Bengaluru",
    "Chennai",
    "Mumbai",
    "Delhi NCR",
    "Pune",
    "Kolkata",
    "Ahmedabad",
    "Jaipur",
    "Kochi",
    "Coimbatore",
    "Visakhapatnam",
    "Vijayawada",
    "Lucknow",
    "Chandigarh",
    "Indore",
    "Bhopal",
    "Bhubaneswar",
    "Mysuru",
    "Noida",
    "Gurugram",
    "Thiruvananthapuram",
    "Surat",
    "Nagpur",
    "Patna",
    "Ranchi",
    "Vadodara",
    "Nashik",
    "Agra",
    "Kanpur",
]


# ============================================================
# CLEAR EVERYTHING
# ============================================================

def clear_everything():

    return (
        None,
        None,
        None,

        upload_status(
            None,
            "Transcript"
        ),

        upload_status(
            None,
            "Syllabus"
        ),

        upload_status(
            None,
            "Course Notes"
        ),

        1,
        2,

        """
        <div class="result-card">
            <div class="result-title">
                Academic Performance
            </div>
            <p>
                Upload material and click Analyze.
            </p>
        </div>
        """,

        """
        <div class="result-card">
            <div class="result-title">
                Study Plan
            </div>
            <p>
                Your study timetable will appear here.
            </p>
        </div>
        """,

        """
        <div class="result-card">
            <div class="result-title">
                Syllabus Coverage
            </div>
            <p>
                Syllabus coverage will appear here.
            </p>
        </div>
        """,

        "",

        """
        <div class="qa-answer">
            <div class="qa-answer-label">
                Answer
            </div>

            <div class="qa-answer-text">
                Ask a basic question about your material
                or the agent.
            </div>
        </div>
        """,

        """
        <div class="result-card">
            <div class="result-title">
                Jobs & Internships
            </div>
            <p>
                Relevant opportunities will appear here.
            </p>
        </div>
        """,

        "Hyderabad",
        "Fresher",

        None
    )


# ============================================================
# UI
# ============================================================

with gr.Blocks(
    theme=THEME
) as demo:

    state = gr.State(
        value=None
    )

    with gr.Column(
        elem_id="main-wrapper"
    ):

        # ----------------------------------------------------
        # HERO
        # ----------------------------------------------------

        gr.HTML(
            """
            <div class="hero-card">

                <div class="hero-title">
                    Transcript & Study Plan Agent
                </div>

                <div class="hero-subtitle">
                    Analyze academic performance, identify weak
                    areas, build a prioritized study timetable and
                    discover relevant career opportunities.
                </div>

            </div>
            """
        )

        # ----------------------------------------------------
        # UPLOAD SECTION
        # ----------------------------------------------------

        gr.HTML(
            """
            <div class="section">

                <div class="section-heading">
                    Upload Academic Material
                </div>

                <div class="section-description">
                    Upload any one, any two, or all three.
                    The agent responds using whatever material
                    is available.
                </div>

            </div>
            """
        )

        with gr.Row(
            equal_height=True
        ):

            with gr.Column(
                elem_classes="upload-card"
            ):

                gr.HTML(
                    """
                    <div class="upload-title">
                        Transcript
                    </div>
                    """
                )

                transcript_upload = gr.File(
                    label="",
                    file_types=[
                        ".pdf",
                        ".txt",
                        ".md"
                    ],
                    file_count="single",
                    type="filepath",
                    height=220,
                    elem_id="transcript-upload"
                )

                transcript_status = gr.HTML(
                    upload_status(
                        None,
                        "Transcript"
                    ),
                    elem_classes="upload-status"
                )

            with gr.Column(
                elem_classes="upload-card"
            ):

                gr.HTML(
                    """
                    <div class="upload-title">
                        Syllabus
                    </div>
                    """
                )

                syllabus_upload = gr.File(
                    label="",
                    file_types=[
                        ".pdf",
                        ".txt",
                        ".md"
                    ],
                    file_count="single",
                    type="filepath",
                    height=220,
                    elem_id="syllabus-upload"
                )

                syllabus_status = gr.HTML(
                    upload_status(
                        None,
                        "Syllabus"
                    ),
                    elem_classes="upload-status"
                )

            with gr.Column(
                elem_classes="upload-card"
            ):

                gr.HTML(
                    """
                    <div class="upload-title">
                        Course Notes
                    </div>
                    """
                )

                notes_upload = gr.File(
                    label="",
                    file_types=[
                        ".pdf",
                        ".txt",
                        ".md"
                    ],
                    file_count="single",
                    type="filepath",
                    height=220,
                    elem_id="notes-upload"
                )

                notes_status = gr.HTML(
                    upload_status(
                        None,
                        "Course Notes"
                    ),
                    elem_classes="upload-status"
                )


        # ----------------------------------------------------
        # UPLOAD EVENTS
        # ----------------------------------------------------

        transcript_upload.change(
            fn=lambda x: upload_status(
                x,
                "Transcript"
            ),
            inputs=transcript_upload,
            outputs=transcript_status
        )

        syllabus_upload.change(
            fn=lambda x: upload_status(
                x,
                "Syllabus"
            ),
            inputs=syllabus_upload,
            outputs=syllabus_status
        )

        notes_upload.change(
            fn=lambda x: upload_status(
                x,
                "Course Notes"
            ),
            inputs=notes_upload,
            outputs=notes_status
        )


        # ----------------------------------------------------
        # STUDY SCHEDULE
        # ----------------------------------------------------

        gr.HTML(
            """
            <div class="section">

                <div class="section-heading">
                    Study Schedule
                </div>

                <div class="section-description">
                    Choose how many days you want to study
                    and how many hours you can study each day.
                </div>

            </div>
            """
        )

        with gr.Group(
            elem_classes="schedule-card"
        ):

            with gr.Row():

                days_input = gr.Dropdown(
                    choices=list(
                        range(1, 31)
                    ),
                    value=1,
                    label="Days",
                    info="1–30 days"
                )

                hours_input = gr.Dropdown(
                    choices=list(
                        range(1, 13)
                    ),
                    value=2,
                    label="Hours per Day",
                    info="1–12 hours"
                )


        # ----------------------------------------------------
        # ANALYZE BUTTON
        # ----------------------------------------------------

        analyze_button = gr.Button(
            "Analyze & Generate Study Plan",
            variant="primary",
            elem_id="analyze-button"
        )

        clear_button = gr.Button(
            "Clear All",
            elem_id="clear-button"
        )


        # ----------------------------------------------------
        # 1. PERFORMANCE
        # ----------------------------------------------------

        gr.HTML(
            """
            <div class="section">

                <div class="section-heading">
                    1. Academic Performance
                </div>

                <div class="section-description">
                    Academic grades are analyzed to identify
                    subjects requiring more attention.
                </div>

            </div>
            """
        )

        performance_output = gr.HTML(
            """
            <div class="result-card">
                <div class="result-title">
                    Academic Performance
                </div>
                <p>
                    Upload a transcript or other academic
                    material and click Analyze.
                </p>
            </div>
            """
        )


        # ----------------------------------------------------
        # 2. STUDY PLAN
        # ----------------------------------------------------

        gr.HTML(
            """
            <div class="section">

                <div class="section-heading">
                    2. Study Plan
                </div>

                <div class="section-description">
                    The available material is converted into
                    a prioritized timetable.
                </div>

            </div>
            """
        )

        schedule_output = gr.HTML(
            """
            <div class="result-card">
                <div class="result-title">
                    Study Plan
                </div>
                <p>
                    Your timetable will appear here.
                </p>
            </div>
            """
        )


        # ----------------------------------------------------
        # 3. SYLLABUS COVERAGE
        # ----------------------------------------------------

        gr.HTML(
            """
            <div class="section">

                <div class="section-heading">
                    3. Syllabus Coverage
                </div>

                <div class="section-description">
                    Syllabus topics are compared against
                    the available course material.
                </div>

            </div>
            """
        )

        coverage_output = gr.HTML(
            """
            <div class="result-card">
                <div class="result-title">
                    Syllabus Coverage
                </div>
                <p>
                    Upload a syllabus and, if available,
                    course notes to see topic coverage.
                </p>
            </div>
            """
        )


        # ----------------------------------------------------
        # 4. ASK YOUR MATERIAL
        # ----------------------------------------------------

        gr.HTML(
            """
            <div class="section">

                <div class="section-heading">
                    4. Ask Your Material
                </div>

                <div class="section-description">
                    Ask short questions about your transcript,
                    syllabus, notes, study plan, or the agent.
                </div>

            </div>
            """
        )

        with gr.Group(
            elem_classes="qa-card"
        ):

            gr.HTML(
                """
                <div class="qa-title">
                    Basic Q&A
                </div>

                <div class="qa-description">
                    Try questions such as:
                </div>

                <div class="qa-examples">
                    • What grade did I get in DBMS?<br>
                    • Is normalization covered?<br>
                    • Which subject needs more time?<br>
                    • Which topics are missing?<br>
                    • What can this agent do?<br>
                    • How does the study plan work?<br>
                    • How does job search work?<br>
                    • What files can I upload?
                </div>
                """
            )

            with gr.Row():

                qa_input = gr.Textbox(
                    label="Your Question",
                    placeholder="e.g. What grade did I get in DBMS?",
                    lines=1,
                    max_lines=2
                )

                qa_button = gr.Button(
                    "Ask",
                    variant="primary",
                    elem_id="qa-button"
                )

            qa_output = gr.HTML(
                """
                <div class="qa-answer">

                    <div class="qa-answer-label">
                        Answer
                    </div>

                    <div class="qa-answer-text">
                        Ask a basic question about your material
                        or the agent.
                    </div>

                </div>
                """
            )


        # ----------------------------------------------------
        # 5. JOBS
        # ----------------------------------------------------

        gr.HTML(
            """
            <div class="section">

                <div class="section-heading">
                    5. Jobs & Internships
                </div>

                <div class="section-description">
                    Relevant opportunities are searched using
                    skills inferred from the uploaded academic
                    material.
                </div>

            </div>
            """
        )

        with gr.Row(
            equal_height=True
        ):

            location_input = gr.Dropdown(
                choices=CITIES,
                value="Hyderabad",
                label="Location",
                info="Select the city where you want to find jobs",
                allow_custom_value=False
            )

            experience_input = gr.Dropdown(
                choices=[
                    "Fresher",
                    "1 year",
                    "2 years",
                    "3 years",
                    "4+ years"
                ],
                value="Fresher",
                label="Experience"
            )

        jobs_output = gr.HTML(
            """
            <div class="result-card">
                <div class="result-title">
                    Jobs & Internships
                </div>
                <p>
                    Analyze your material to search for
                    relevant opportunities.
                </p>
            </div>
            """
        )

        find_jobs_button = gr.Button(
            "Refresh Jobs & Internships",
            variant="secondary"
        )


        # ----------------------------------------------------
        # ANALYZE EVENT
        # ----------------------------------------------------

        analyze_button.click(
            fn=process_all,

            inputs=[
                transcript_upload,
                syllabus_upload,
                notes_upload,
                days_input,
                hours_input
            ],

            outputs=[
                performance_output,
                schedule_output,
                coverage_output,
                jobs_output,
                state
            ]
        )


        # ----------------------------------------------------
        # Q&A EVENT
        # ----------------------------------------------------

        qa_button.click(
            fn=ask_material,

            inputs=[
                qa_input,
                state
            ],

            outputs=qa_output
        )

        qa_input.submit(
            fn=ask_material,

            inputs=[
                qa_input,
                state
            ],

            outputs=qa_output
        )


        # ----------------------------------------------------
        # JOB REFRESH EVENT
        # ----------------------------------------------------

        find_jobs_button.click(
            fn=find_jobs,

            inputs=[
                state,
                location_input,
                experience_input
            ],

            outputs=jobs_output
        )


        # ----------------------------------------------------
        # CLEAR EVENT
        # ----------------------------------------------------

        clear_button.click(
            fn=clear_everything,

            inputs=[],

            outputs=[
                transcript_upload,
                syllabus_upload,
                notes_upload,

                transcript_status,
                syllabus_status,
                notes_status,

                days_input,
                hours_input,

                performance_output,
                schedule_output,
                coverage_output,

                qa_input,
                qa_output,

                jobs_output,

                location_input,
                experience_input,

                state
            ]
        )


# ============================================================
# LAUNCH
# ============================================================

if __name__ == "__main__":

    demo.launch(
        theme=THEME,
        css=CSS,
        inbrowser=True,
        server_name="127.0.0.1",
        server_port=7860,
        max_file_size="20mb"
    )