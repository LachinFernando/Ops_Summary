import streamlit as st
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi

from rag import helper_graph as llm_graph


HOMEWORK_CHECK_BENCHMARK = 10 * 60
IMPORTANT_KEYS = ['topics', 'review', 'directions', 'homework', 'code_error', 'technical_issue']
TOPIC_DICT = {
    "topics": "Topics Discussed",
    "review": "Homework Review",
    "directions": "Future Directions",
    "homework": "Homework for the Next Session",
    "code_error": "Code Erros Occured",
    "technical_issue": "Technical Issues Occured"
}


def convert_seconds(seconds):
    # Calculate hours
    hours = int(seconds // 3600)
    seconds %= 3600

    # Calculate minutes
    minutes = int(seconds // 60)
    seconds %= 60

    # Remaining seconds and milliseconds
    remaining_seconds = int(seconds)
    milliseconds = int((seconds - remaining_seconds) * 1000)

    # Format the result as HH:MM:SS.mmm
    return f"{hours:02}:{minutes:02}:{remaining_seconds:02}.{milliseconds:03}"


def get_video_id_from_url(url: str) -> str:
    url_chunks = urlparse(url)
    if not url_chunks.query:
        video_id = url_chunks.path.split("/")[-1]
        return video_id

    video_id = parse_qs(url_chunks.query).get("v", [""])[0]

    if not video_id:
        video_id = url_chunks.path.split("/")[-1]
        return video_id

    return video_id


def extract_youtube_content(youtube_url: str) -> tuple:
    extract_id = get_video_id_from_url(youtube_url)
    # extract the youtube content
    ytt_api = YouTubeTranscriptApi()
    script = ytt_api.fetch(extract_id)

    # get the ten minutes bench mark
    end_benchmark = script[0].start + HOMEWORK_CHECK_BENCHMARK

    st_view_text_set = []
    original_text_set = []
    homework_check_text = []
    # VTT format generation
    for index, script_ in enumerate(script):
        start_time = convert_seconds(script_.start)
        end_time = convert_seconds(script_.start + script_.duration)
        text = script_.text
        st_view_text_set.append("{} --> {}:  \n{}".format(start_time, end_time, text))
        original_text_set.append("{} --> {}:\n{}".format(start_time, end_time, text))

        # check and attach homework check prompts
        if script_.start <= end_benchmark:
            homework_check_text.append(text)

    transcript = "  \n".join(st_view_text_set)
    original_script = "\n".join(original_text_set)
    homework_Script = "\n".join(homework_check_text)

    return (transcript, original_script, homework_Script)


# web application
st.title("New Summary Generator")

# text input 
youtube_url = st.text_input("Enter the Youtube URL")

if not youtube_url:
    st.error("Enter a Valid URL")
    st.stop()

# extract the transcript
# try:
#     view_version_script, video_transcript, homework_ten_script = extract_youtube_content(youtube_url)
# except Exception as error:
#     message = "Transcript Generation Failed: {}".format(str(error))
#     print(message)
#     st.error("Transcript Generation Fails! Please Try Again with a valid URL")
#     st.stop()

view_version_script, video_transcript, homework_ten_script = extract_youtube_content(youtube_url)

# display the transcript in side bar
with st.sidebar:
    st.subheader("Transcript")
    st.write(view_version_script)

# getting predictions
with st.spinner("Analysing the script.......", show_time=True):
    get_invoke_response = llm_graph.invoke({"full_script": video_transcript, "ten_minute_script": homework_ten_script})

if get_invoke_response:
    for response_key in IMPORTANT_KEYS:
        with st.expander(f"{TOPIC_DICT[response_key]}"):
            st.markdown(get_invoke_response[f"{response_key}"])


