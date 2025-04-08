IMPORTANT_TOPICS_PROMPT = """
You are a highly skilled language model trained to expertly analyze session transcripts between a student and a machine learning instructor.

Your task is to carefully examine the provided transcript to identify and extract the most critical topics centered around technical discussions, implementations, and collaborations.

Session transcript is given below.

{transcript}

For each identified topic, provide a succinct description summarizing the core points and dialogues as bullet points under each topic. 

Additionally, include the exact start and end timestamps of each topic discussion, indicating when the topic began and ended within the transcript.

Focus on how these discussions demonstrate technical expertise, collaborative learning, or practical implementations. Ensure the number of topics ranges from 2 to 5 for comprehensive coverage.

Instructions:

1. Carefully analyze the transcript to discern key themes or subjects related to machine learning technical aspects and learning collaborations between the student and instructor.

2. Identify 2 to 5 primary topics that are distinctly tied to technical discussions, collaborative learning, or practical implementation strategies discussed during the session.

3. Present each topic as a clear section with a descriptive heading formatted as follows:
   - Main Topic [number]: [Topic Name] ([Start Timestamp] - [End Timestamp])
   For example, "Main Topic 1: Project Updates and Data Collection (00:03:51.583 - 00:13:11.192)".

4. For each topic, provide a brief and focused summary as bullet points, capturing the essence of the conversation, emphasizing technical insights, instructional methods, or collaborative problem-solving approaches.

5. Use clear and concise language to convey your summaries, facilitating easy understanding and effective reference for readers.

6. Formatting: Use plain text without any markdown styles beyond simple bullet points.

"""

HOMEWORK_CHECK_PROMPT = """
Your task is to summarize the given session transcript between a student and a machine learning instructor by extracting specific elements related to homework. 

{transcript}

Follow these steps:

1. Identify any homework assigned to the student in the previous week from the summary.

2. Determine the status of each piece of homework, classifying each as "Completed," "Partially Completed," or "Not Completed."

3. Extract any feedback provided for the homework.

4. If no homework was assigned, indicate "No Homework" and use "NA" for both status and feedback.

5. Format your response in the following structure:
    Homework: <comma-separated list of homeworks>
    Status: <"Completed", "Partially Completed", or "Not Completed">
    Feedback: <comma-separated list of feedbacks>
"""

FUTURE_TOPICS_PROMPT = """
You are a highly skilled language model trained to analyze session transcripts between a student and a machine learning instructor. 

Your task is to carefully read the transcript below and extract 2 to 5 key "Future Directions" that are explicitly discussed for future experimentation, implementation, or further discussion.

{transcript}

Future Directions Focus:
These should center on techniques, methodologies, or approaches that the participants intend to try, implement, or explore further.

Output Requirements:

Topics: Identify 2 to 5 distinct future direction topics. Do not include topics that only summarize what was already discussed; focus on areas proposed for future work.

Structure: For each identified future direction topic, create a clear section with a descriptive heading formatted as follows:
Future Direction [number]: [Topic Name] ([Start Timestamp] - [End Timestamp])
For example: Future Direction 1: New Data Augmentation Techniques (00:12:34.567 - 00:15:22.890)

Bullet Points: Under each heading, provide 2 to 4 bullet points summarizing the discussion points related to that future direction. Each bullet point must start with a "-" (dash).

Scope: Only use information directly from the transcript. Do not add or infer details that are not explicitly mentioned.

Formatting: Do not use markdown styles (e.g., bold, italics) beyond plain text and bullet points. Do not use any start sign for heading.

Tone: Maintain a formal and instructional tone throughout your response.

Follow these instructions precisely to extract and present the future direction topics from the transcript.

"""

GIVEN_HOMEWORK_PROMPT = """
You are tasked with extracting homework assignments from a given session transcript between a student and an instructor.

Below is the transcript
{transcript}

Follow these instructions and refer to the examples section for clarity on how to format your output:

Instructions:

1. Read the Transcript: Carefully review the entire session transcript to understand the context and identify any tasks or instructions given.

2. Identify Homework Tasks: Focus on statements or requests that imply tasks to be completed in the future, especially those that are clearly instructional or formulated as homework.

3. Format Your Findings: If homework is identified, list each task in a clear, numbered format. Make sure to be concise and precise in your wording.

4. No Homework Confirmation: If there are no identifiable homework assignments in the transcript, clearly indicate this with "Homework: No homework."

5. Presentation: Present your analysis without using markdown styles like bold or titles.

Example Section:

Example 1:

Text: Hi Good Morning! Today we have to train the models and record the accuracy values. Could you please open up the notebook I shared last week. Okay sure. Please run the notebook and get the accuracy values. Great! Accuracy seems good. Could you please note them down in a documentation. I have shared a notebook to draw plots for accuracies. Please generate those accuracy graphs when you are coming to the next session. Then you can add them to the documentation. Thank You, Bye see you in the next session. Bye
Homework: 1. Generate accuracy graphs using the shared notebook. 2. Add the generated graphs to the documentation.

Example 2:

Text: Hi, how are you doing? doing fine, thank you. Great, today we will focus on completing the introduction and related work sections in your research paper. Could you please open the google doc. I have shared the link in the chat. Good, could you write three, four sentences for the introduction regarding your project. Specify why the project is important and differ from others. Please find some references using google and google scholar. Search for similar studies as yours and read the abstracts. Just add overall idea to the related work section and ensure you add references to the references section. Our time is up. For the homework, please add all figures to the results sections and add fig numbers. And please bring all the necessary applications to fill them and register for the competition. Thank You! see you in the next session. Bye!
Homework: 1. Add all the figures to the result section of the documentation and add relevant figure numbers for them. 2. Reminded to bring all the necessary applications which need to be filled up in order to register for the competition.

Example 3:

Text: Hi, how are you? fine, so let's check what we have to change in our streamlit web app. I tried to change the drop down menu but it didn't work, could you please take a look? Sure, let's check, can you open up the notebook? Here, you have to mention the drop down items inside a list. Copy paste them inside a list and run the web app. Okay cool, now it is working. Since you have already hosted it, again upload the app.py to your github repository. Okay, seems all good now. See you in the next session. Bye!
Homework: No homework.
"""

ERROR_CHECKS = """
You are a highly skilled language model trained to analyze session transcripts between a student and a machine learning instructor.

Your task is to carefully examine the transcript below and extract any instances where code errors occurred or were discussed during the session.

Note that there might be no code errors at all; in such cases, your response should clearly state that no code errors were identified.

{transcript}

For each code error identified, provide the following details:
1. Timestamp: Extract the exact timestamp from the transcript when the code error was mentioned or discussed.
2. Error Description: Summarize the issue or error that was mentioned.
3. Steps Taken: Describe the steps that were taken during the session to resolve or address the error.

Output Requirements:
- If code errors are found, create a clear section for each error with the following format:
  Code Error [number]: ([Timestamp])
  - Issue: [Brief description of the error or issue]
  - Steps Taken: [Description of the steps taken to solve the error]
- If no code errors are present in the transcript, output a clear statement indicating that no code errors were identified.

Scope: Only use information directly from the transcript. Do not add or infer details that are not explicitly mentioned.

Formatting: Use plain text without any markdown styles beyond simple bullet points.

Tone: Maintain a formal and instructional tone throughout your response.

Follow these instructions precisely to extract and present the code error details from the transcript.


"""

TECHNICAL_ISSUE = """
You are a highly skilled language model trained to analyze session transcripts between a student and a machine learning instructor.

Your task is to carefully examine the transcript below and extract any instances where technical issues related to connectivity or multimedia problems are mentioned during the session. 

Do not include any code errors that occurred during the session; focus only on technical glitches such as audio, video, or network issues.

These technical issues may include, but are not limited to, statements such as "your mic is not working", "your camera is not working", "your bandwidth is low", or "My zoom is having trouble".

{transcript}

For each technical issue identified, provide the following details:
1. Timestamp: Extract the exact timestamp from the transcript when the technical issue was mentioned.
2. Issue Description: Summarize the technical issue that was mentioned (e.g., microphone issues, camera problems, low bandwidth, zoom difficulties).

Output Requirements:
- If technical issues are found, create a clear section for each issue with the following format:
  Technical Issue [number]: ([Timestamp])
  - Issue: [Brief description of the technical issue]
- If no technical issues are present in the transcript, output a clear statement indicating that no technical issues were identified.

Scope: Only use information directly from the transcript. Do not add or infer details that are not explicitly mentioned.

Formatting: Use plain text without any markdown styles beyond simple bullet points.

Tone: Maintain a formal and instructional tone throughout your response.

Follow these instructions precisely to extract and present the technical issue details from the transcript.


"""