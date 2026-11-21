
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm

from pdf_extractor import extract_text_from_pdf
from question_processor import extract_questions
from llm_classifier import classify_questions
from analyzer import analyze_topics


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Previous Year Question Paper Analyzer",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Previous Year Question Paper Analyzer")
st.write("Analyze previous-year papers and discover important exam topics.")
st.divider()


# ---------------- FILE UPLOAD ----------------

st.subheader("📄 Upload Question Papers")

uploaded_files = st.file_uploader(
    "Upload PDF files",
    type=["pdf"],
    accept_multiple_files=True
)


# ---------------- ANALYSIS ----------------

if uploaded_files:

    if st.button("🚀 Analyze Question Papers", type="primary"):

        all_results = []

        progress = st.progress(0)
        status = st.empty()

        for file_index, file in enumerate(uploaded_files):

            status.write(f"Processing: {file.name}")

            try:
                text = extract_text_from_pdf(file)
                questions = extract_questions(text)

                if not questions:
                    st.warning(f"No questions found in {file.name}")
                    continue

                results = classify_questions(questions)

                for item in results:
                    item["paper"] = file.name
                    all_results.append(item)

            except Exception as e:
                st.error(f"Error processing {file.name}: {e}")

            progress.progress((file_index + 1) / len(uploaded_files))

        status.empty()

        if all_results:
            st.session_state["results"] = pd.DataFrame(all_results)
            st.success("Analysis completed successfully!")

        else:
            st.error("No questions could be analyzed.")


# ---------------- DISPLAY RESULTS ----------------

if "results" in st.session_state:

    df = st.session_state["results"]

    topic_counts = analyze_topics(df)

    st.divider()
    st.header("📊 Analysis Dashboard")

    # Dashboard metrics
    col1, col2, col3 = st.columns(3)

    total_questions = len(df)
    total_topics = df["topic"].nunique()
    top_topic = topic_counts.iloc[0]["Topic"]
    top_frequency = topic_counts.iloc[0]["Frequency"]

    col1.metric("Total Questions", total_questions)
    col2.metric("Unique Topics", total_topics)
    col3.metric("Most Repeated Topic", top_topic)

    st.info(
        f"⭐ {top_topic} appeared {top_frequency} times."
    )

    # Topic chart
    st.subheader("📈 Topic Frequency Chart")

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(
        topic_counts["Topic"],
        topic_counts["Frequency"]
    )

    ax.set_xlabel("Topics")
    ax.set_ylabel("Frequency")
    ax.set_title("Frequently Asked Topics")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

    # Topic filter
    st.divider()
    st.header("🔍 Explore Questions")

    topics = ["All Topics"] + sorted(df["topic"].dropna().unique().tolist())

    selected_topic = st.selectbox(
        "Filter by topic",
        topics
    )

    search_text = st.text_input(
        "Search questions",
        placeholder="Enter a keyword..."
    )

    filtered_df = df.copy()

    if selected_topic != "All Topics":
        filtered_df = filtered_df[
            filtered_df["topic"] == selected_topic
        ]

    if search_text:
        filtered_df = filtered_df[
            filtered_df["question"].str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

    st.write(f"Showing {len(filtered_df)} questions")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    # Excel download
    st.divider()
    st.header("📥 Download Reports")

    excel_buffer = BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            sheet_name="Question Analysis",
            index=False
        )

        topic_counts.to_excel(
            writer,
            sheet_name="Topic Frequency",
            index=False
        )

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            "📊 Download Excel Report",
            data=excel_buffer.getvalue(),
            file_name="Question_Analysis.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # PDF download
    pdf_buffer = BytesIO()

    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm
    )

    elements = []
    styles = getSampleStyleSheet()

    elements.append(
        Paragraph(
            "Previous Year Question Paper Analysis",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 15))

    elements.append(
        Paragraph("Topic Frequency", styles["Heading2"])
    )

    topic_data = [["Topic", "Frequency"]]

    for _, row in topic_counts.iterrows():
        topic_data.append([
            str(row["Topic"]),
            str(row["Frequency"])
        ])

    topic_table = Table(
        topic_data,
        repeatRows=1
    )

    topic_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6)
    ]))

    elements.append(topic_table)
    elements.append(Spacer(1, 15))

    elements.append(
        Paragraph("Question Classification", styles["Heading2"])
    )

    question_data = [["Question", "Topic"]]

    for _, row in df.iterrows():
        question_data.append([
            Paragraph(str(row["question"]), styles["BodyText"]),
            Paragraph(str(row["topic"]), styles["BodyText"])
        ])

    question_table = Table(
        question_data,
        colWidths=[125 * mm, 55 * mm],
        repeatRows=1
    )

    question_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 5)
    ]))

    elements.append(question_table)

    doc.build(elements)

    with col2:
        st.download_button(
            "📄 Download PDF Report",
            data=pdf_buffer.getvalue(),
            file_name="Question_Analysis.pdf",
            mime="application/pdf"
        )

else:
    st.info("Upload your question papers and click Analyze to begin.")



#Your individual folder/ ├── Report.pdf          ├── Code.zip            ├── github_link.txt     ├── screenshots/        └── demo_video.mp4      (2-page procedure report) (full project code, without API keys) (your GitHub repository URL) (3–5 output screenshots) (optional, 1–2 minutes)