from google import genai
import uuid
from string import Template
import sys
import subprocess
from django.core.files import File
import os
from bs4 import BeautifulSoup
from celery_progress.backend import ProgressRecorder
from google.genai import types
from .models import Source, ArxivSource, WebSource, Article, ArticleVideo
from typing import List
from .get_module_info import top_level_module_info
import requests
import tempfile
import manim


client = None

model = "models/gemini-3-pro-preview"


def get_genai_client():
    global client
    if client is not None:
        return client
    client = genai.Client()
    return client


manim_docs = {}


def get_manim_docs(system_prompt):
    global manim_docs

    if system_prompt in manim_docs:
        return manim_docs[system_prompt]

    context = top_level_module_info(manim)
    manim_docs[system_prompt] = client.caches.create(
        model=model,
        config={
            "display_name": "Manim Docs",
            "contents": types.Content(
                role="user", parts=[types.Part.from_text(text=context)]
            ),
            "system_instruction": system_prompt,
        },
    )

    return manim_docs[system_prompt]


class AIArticleGenerator:
    source: Source
    chat: genai.chats.Chat
    total_steps: int
    current_step: int = 0

    system_prompt = """
        You are an expert article writer. Based on the provided sources, generate a comprehensive article.
        Ensure the article is well-structured, informative, and engaging.
        Use proper citations where necessary.
        Don't use references in the article, for figures or anything else.
        You will generate the parts of the article step by step.
        Don't add anything extra outside of the requested sections.
        Don't use any syntax outside of markdown, only output the markdown, nothing else.
        NOTE: All sections are required, do not skip any sections.
        Use markdown lists for highlighting key points and insights.
        Use markdown tables for higlighting key differences.
        Add a line break before adding in markdown lists.
        The article should include the following sections:
        Make sure a single line is not very long, ensure frequent line breaks and shorter and more numerous paragraphs
        Always write in third person, never assume you are the writer of the original article.
        Since we are going to be generating the article step by step, only respond with text of what was requested at each step
        We are going to be generating title and lead_paragraph at the very end.
        Don't add things like "title:" etc. that will be handled externally, only output text

        The title should be short, 50 to 60 charactes maximum

        title = models.TextField(description="Short catchy title that will be displayed at the top of article and in listings. This will have no markdown.")

        For the following, use as much markdown as possible to format the text properly.

        lead_paragraph = models.TextField(description="Catchy leading paragraph that will be shown on the article listing along with the title")

    """

    def increment_step(self, message=None):
        self.current_step += 1
        print(f"Processing item {self.current_step}...")
        self.progress_recorder.set_progress(
            self.current_step,
            self.total_steps,
            f"Processing item {self.current_step}..." if message is None else message,
        )

    def __init__(
        self,
        progress_recorder: ProgressRecorder,
        source: Source,
        model: str = model,
    ):
        self.client = get_genai_client()
        self.model = model
        self.source = source
        self.progress_recorder = progress_recorder
        files = []
        sources = source.sources()
        self.total_steps = len(sources) + 1 + 10
        for single_source in sources:
            if isinstance(single_source, ArxivSource):
                self.increment_step("Processing Arxiv Source")
                files.append(self._process_arxiv_source(single_source))
            elif isinstance(single_source, WebSource):
                self.increment_step("Processing Web Source")
                files.append(self._process_web_source(single_source))

        self.chat = self.client.chats.create(
            model=self.model,
            history=[
                types.Content(
                    role="user",
                    parts=files,
                )
            ],
        )

    def _process_arxiv_source(self, arxiv_source: ArxivSource):
        arxiv_id = arxiv_source.arxiv_id
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"
        response = requests.get(pdf_url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        with tempfile.NamedTemporaryFile(mode="w+b", delete=True) as temp:
            for chunk in response.iter_content(chunk_size=8192):
                temp.write(chunk)
            temp.flush()
            temp.seek(0)
            return types.Part.from_bytes(data=temp.read(), mime_type="application/pdf")

    def _process_web_source(self, web_source: WebSource):
        """Downloads the web page content from the URL and appends the text to conversation."""
        url = web_source.url
        response = requests.get(url, stream=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        text = bytearray("\n".join(soup.find_all(text=lambda s: len(s) > 32)), "utf-8")
        return types.Part.from_bytes(data=text, mime_type="text/plain")

    def _run_model(self, text: List[str]):
        resp = self.chat.send_message(
            [types.Part.from_text(text=text_segment) for text_segment in text],
            config=types.GenerateContentConfig(system_instruction=[self.system_prompt]),
        )
        return resp.text

    def generate_article(self) -> Article:
        lead_paragraph = self._run_model(
            [
                "Now, generate the lead paragraph for the completed article. Remember to make sure this paragraph is only 50 - 60 words, and can be read at a glance."
            ],
        )

        self.increment_step("Generating the lead paragraph")

        title = self._run_model(
            ["Now, generate the title for the completed article."],
        )

        self.increment_step("Generating the title")

        article = Article(
            title=title,
            lead_paragraph=lead_paragraph,
            based_on=self.source,
        )
        return article

runner_template = Template("""
with tempconfig({'output_file': '$filename', 'quality': 'low_quality'}):
        scene = Video()
        scene.render()
""")

class VideoGenerator:
    article: Article
    chat: genai.chats.Chat
    total_steps: int
    current_step: int = 0

    script_system_prompt = """
        You are a youtube shorts script writer for educational videos,
        you are to generate a short script for a short form video that will be generated using minimal text animations and colors and black background.

        The context for generating the video will be provided by the user, this content will include short summaries and original article, Make sure that the essence of the article is captured.
    """

    manim_system_prompt = """
        You are a professional python programmer with experience in working with the manim library to generate videos
        Your task is to read the generated script, that the user will provide, to generate a python program using manim community 0.19 library and the base python libraries to generate a video that follows the script.
        Additionally the entire conversation history will also be present for cross referencing.
        ONLY OUTPUT THE PYTHON CODE, NOTHING ELSE, as this will be going straight for execution in a python sandbox.
        Make sure that you are importing anything that you need, and don't assume that anything is imported or predefined.
        Import or define colors explicitly, don't assume that they are already imported
    """

    def increment_step(self, message=None):
        self.current_step += 1
        print(f"Processing item {self.current_step} {message}...")
        self.progress_recorder.set_progress(
            self.current_step,
            self.total_steps,
            f"Processing item {self.current_step}..." if message is None else message,
        )

    def _run_model(self, system_prompt: str, text: List[str], manim: bool = False):
        if manim:
            config = types.GenerateContentConfig(cached_content=get_manim_docs(system_prompt).name)
        else:
            config = types.GenerateContentConfig(system_instruction=[system_prompt])

        resp = self.chat.send_message(
            message=[types.Part.from_text(text=text_segment) for text_segment in text],
            config=config
        )
        return resp.text

    def _process_arxiv_source(self, arxiv_source: ArxivSource):
        arxiv_id = arxiv_source.arxiv_id
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"
        response = requests.get(pdf_url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        with tempfile.NamedTemporaryFile(mode="w+b", delete=True) as temp:
            for chunk in response.iter_content(chunk_size=8192):
                temp.write(chunk)
            temp.flush()
            temp.seek(0)
            return types.Part.from_bytes(data=temp.read(), mime_type="application/pdf")

    def _process_web_source(self, web_source: WebSource):
        """Downloads the web page content from the URL and appends the text to conversation."""
        url = web_source.url
        response = requests.get(url, stream=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        text = bytearray("\n".join(soup.find_all(text=lambda s: len(s) > 32)), "utf-8")
        return types.Part.from_bytes(data=text, mime_type="text/plain")

    def __init__(
        self,
        progress_recorder: ProgressRecorder,
        article: Article,
        model: str = model,
    ):
        self.client = get_genai_client()
        self.model = model
        self.article = article
        self.progress_recorder = progress_recorder
        files = []
        if article.based_on is None:
            return

        sources = article.based_on.sources()
        self.total_steps = len(sources) + 1 + 10
        for single_source in sources:
            if isinstance(single_source, ArxivSource):
                self.increment_step("Processing Arxiv Source")
                files.append(self._process_arxiv_source(single_source))
            elif isinstance(single_source, WebSource):
                self.increment_step("Processing Web Source")
                files.append(self._process_web_source(single_source))

        self.chat = self.client.chats.create(
            model=self.model,
            history=[
                types.Content(
                    role="user",
                    parts=files,
                )
            ],
        )

    def generate_script(self) -> str:
        self.increment_step("Generating the script")
        script = self._run_model(
            self.script_system_prompt,
            [
                "Now, generate the script for the short form video based on the provided context. make sure that video length is around 60 seconds"
            ],
        )

        return script

    def generate_manim_script(self) -> str:
        script = self.generate_script()

        print(script)
        self.increment_step("Generating the manim python script.")
        manim_script = (
            self._run_model(
                self.manim_system_prompt,
                [
                    script,
                    "Now generate the corresponding python script that will generate the video for this script, Remember to make sure the class name for the scene is 'Video'",
                ],
                manim=True
            )
            .strip()
            .strip("```python")
            .strip()
        )

        filename = f"/tmp/VIDEO-{uuid.uuid4().hex}.mp4"
        manim_script += runner_template.substitute(filename=filename)
        print(manim_script)
        with tempfile.NamedTemporaryFile(delete_on_close=False) as script_file:
            self.increment_step("Running manim script.")
            script_file.write(bytes(manim_script, encoding="utf-8"))
            script_file.flush()
            print(script_file.name)
            print(script_file.read())
            ## FUCK IT, TRUST AI
            # Do as i say, not as i do
            subprocess.Popen(
                [sys.executable, script_file.name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ).wait()



        self.increment_step("Saving manim video to db")

        with open(filename, "rb") as f:
            video_file = File(f, name=os.path.basename(filename))

            # 4. Create and save the ArticleVideo instance
            article_video_instance = ArticleVideo(
                article=self.article,
                file=video_file,  # Assign the File object to the FileField
            )
            article_video_instance.save()

        return manim_script

