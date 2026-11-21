
 1. Introduction and Objective
The Previous Year Question Paper Analyzer is a web-based application developed using Python and Streamlit. It helps students examine previous-year examination papers and identify topics that appear repeatedly. Instead of manually reading several papers and counting topics, a student can upload PDF files and let the application extract question text, classify questions with an AI model, and summarize topic frequency.
The application uses PyMuPDF for extracting text from PDF files, a simple question-detection routine to split extracted text into question entries, Groq-hosted language-model inference for topic classification, Pandas for tabular analysis, Matplotlib for charts, and Streamlit for the user interface. Reports can be downloaded in Excel and PDF formats.
1.1 Main Objective
To develop a simple, accessible application that analyzes multiple previous-year question papers and presents frequently occurring academic topics in a clear and useful format.
1.2 Specific Objectives
•	Allow users to upload one or more examination papers in PDF format.
•	Extract readable text from each uploaded PDF.
•	Identify question entries from the extracted text.
•	Use an AI model to assign a short topic label to each question.
•	Count the frequency of each topic across the uploaded papers.
•	Display results using a table, dashboard metrics, and a bar chart.
•	Allow users to search and filter classified questions.
•	Provide downloadable Excel and PDF reports.
1.3 Scope
The current version is intended for text-based PDFs and an initial set of question-paper layouts. Scanned PDFs that contain only images may require OCR support. The question splitter uses numbering patterns and may need customization for different universities, layouts, multi-part questions, and OR choices. Topic counts should therefore be treated as an aid to revision, not a guarantee of future examination questions.

 2. Design Principles
The application follows a small set of design principles to keep it understandable for students and maintainable for developers.
Design principle	How it is applied
Simplicity	A single Streamlit page provides upload, analysis, results, filtering, and downloads.
Modularity	PDF extraction, question splitting, AI classification, and topic analysis are kept in separate Python modules.
Usability	Clear labels, progress feedback, tables, metrics, and charts help users understand the output.
Automation	AI-assisted classification reduces the need to manually assign a topic to every question.
Transparency	The application displays classified questions so users can review AI-generated topic labels.
Reusability	The same workflow can be used with different subjects and examination-paper collections.
Security	The Groq API key is stored in a local .env file and should not be committed to a public GitHub repository.
Cost awareness	The project uses a provider's available free-tier access where permitted; quotas and terms can change.
2.1 User-Centred Workflow
The intended user workflow is: select PDF papers, start analysis, wait for processing, inspect the dashboard, filter or search questions, and download a report. The application should provide understandable error messages when a PDF cannot be read or an AI request fails.
2.2 Limitations Considered in the Design
•	PDF extraction quality depends on the structure and readability of the source file.
•	The question-detection pattern may combine sub-questions or miss unusual numbering.
•	AI-generated topic names can vary and may require manual review.
•	API availability, rate limits, and free-tier usage limits are controlled by the provider.

 3. Technical Model Details
The system is implemented in Python. Streamlit acts as the presentation layer and runs the application locally in a browser. Each functional stage is implemented as a separate module, allowing individual components to be tested and updated.
Component / Library	Purpose in the project
Python	Main programming language used to implement the application.
Streamlit	Creates the web interface, file uploader, buttons, metrics, filters, and download controls.
PyMuPDF (pymupdf)	Opens PDF files and extracts selectable text from each page.
Regular expressions (re)	Detects common question-number patterns in extracted text.
Groq Python SDK	Sends question batches to a hosted language model for topic classification.
python-dotenv	Loads the API key from a local .env configuration file.
JSON	Structures the AI response as question and topic pairs.
Pandas	Stores results in a DataFrame and calculates topic frequencies.
Matplotlib	Creates the topic-frequency bar chart.
OpenPyXL	Writes analysis data into an Excel workbook.
ReportLab	Creates a formatted PDF report for download.
3.1 Data Flow
Each uploaded PDF is read in memory. Extracted text is passed to the question splitter. The resulting question list is sent to the classifier in small batches to reduce the chance of oversized responses. The returned JSON records are combined and stored in a Pandas DataFrame. Topic frequency is calculated using value_counts(), then the data is rendered and exported.
3.2 AI Classification
The classifier asks the language model to identify the main academic topic for each input question and return a JSON object containing the original question and its topic. The application processes small batches (currently two questions per request) and combines the results. The AI output must be checked because classifications are predictions and can be inaccurate.

 4. System Block Diagram
The following block diagram shows the major components and the direction in which information moves through the application.
INPUT
One or more PDF
question papers
↓
PDF EXTRACTION
PyMuPDF
Extract page text
↓
QUESTION SPLITTING
Regex-based parser
Create question list
↓
AI CLASSIFICATION
Groq language model
Assign topic labels
↓
ANALYSIS
Pandas
Count topic frequency
↓
OUTPUT
Streamlit dashboard
Chart + Excel/PDF reports
4.1 Description of Blocks
•	Input: The user selects PDF question papers through the Streamlit file uploader.
•	PDF extraction: Text is extracted page by page using PyMuPDF.
•	Question splitting: Numbered lines are used to identify the start of question entries.
•	AI classification: Groq-hosted model assigns a concise topic to each question.
•	Analysis: Pandas counts how often each topic appears.
•	Output: Streamlit displays the results and offers Excel/PDF downloads.

 5. Application Flowchart
The flowchart represents the application's main execution logic from upload to report generation.
START
Launch Streamlit application
↓
UPLOAD
User uploads PDF question papers
↓
VALIDATE
Check whether PDF files are available
↓
EXTRACT
Extract text from each PDF
↓
SPLIT
Identify question entries
↓
CLASSIFY
Send questions to AI in small batches
↓
ANALYZE
Combine results and count topic frequency
↓
DISPLAY
Show metrics, chart, table, and filters
↓
EXPORT
Generate Excel and PDF reports
↓
END
User reviews or downloads the results
Decision handling: If no files are uploaded, the application asks the user to upload papers. If no questions are detected or processing fails, an error or warning is displayed. When results are available, the dashboard and report downloads become available.

 6. Implementation Details
6.1 PDF Text Extraction
The PDF extraction module opens the uploaded file from its in-memory byte content using PyMuPDF. It loops through each page, reads selectable text, and adds a page marker to the extracted content. This avoids requiring the user to save the uploaded PDF to a permanent folder.
6.2 Question Detection
The question processor examines the extracted text line by line. It uses regular-expression patterns to recognize common formats such as Q1, Question 1, 1. and 1). When a new question marker is detected, the previous question is saved and a new question entry is started. Continuation lines are appended to the current question.
6.3 AI Topic Classification
The classifier receives a list of questions and divides it into batches of two. For each batch, it sends a prompt requesting a JSON object with question and topic fields. The returned records are parsed and combined into one result list. Errors are raised if the response cannot be parsed or the returned question count does not match the batch.
6.4 Topic Analysis and Visualization
The analyzer uses the topic column of the result DataFrame and applies value_counts() to calculate frequency. The resulting table is used to create a bar chart with topics on the horizontal axis and number of questions on the vertical axis.
6.5 Report Generation
The Excel report contains a question-analysis worksheet and a topic-frequency worksheet. The PDF report contains a topic-frequency table and a question-classification table. Both reports are generated in memory and offered through Streamlit download buttons.
6.6 Configuration and API Key Safety
The Groq API key is stored in a local .env file and loaded through python-dotenv. The .env file must be excluded from Git using .gitignore. Never include a real API key in source code, screenshots, reports, or a public repository.

 8. Working Model Screenshots — Step by Step

   


9. Conclusion and Future Enhancements
The Previous Year Question Paper Analyzer demonstrates how document processing, AI-based text classification, data analysis, and a simple web interface can be combined to support exam preparation. It extracts text from PDF papers, identifies question entries, assigns topic labels, calculates topic frequency, visualizes the results, and generates downloadable reports. It can help students prioritize revision by showing which topics occur frequently in the provided papers.
Future enhancements may include OCR for scanned PDFs, improved question and sub-question parsing, subject-specific topic lists, manual correction of AI labels, duplicate-question detection, topic trends by year, and a deployment option so users can access the application online.
References
•	Python documentation: https://docs.python.org/3/
•	Streamlit documentation: https://docs.streamlit.io/
•	PyMuPDF documentation: https://pymupdf.readthedocs.io/
•	Pandas documentation: https://pandas.pydata.org/docs/
•	Matplotlib documentation: https://matplotlib.org/stable/
•	Groq documentation: https://console.groq.com/docs
•	ReportLab documentation: https://docs.reportlab.com/
