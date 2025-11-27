from google import genai
from bs4 import BeautifulSoup
from celery_progress.backend import ProgressRecorder
from google.genai import types
from .models import Source, ArxivSource, WebSource, Article
from typing import List
import requests
import tempfile


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
            f"Processing item {self.current_step}..."
            if message is None
            else message,
        )

    def __init__(
        self,
        progress_recorder: ProgressRecorder,
        source: Source,
        model: str = "models/gemini-2.5-pro",
    ):
        self.client = genai.Client()
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
            message=[types.Part.from_text(text=text_segment) for text_segment in text],
            config=types.GenerateContentConfig(system_instruction=[self.system_prompt]),
        )
        return resp.text

    def generate_article(self) -> Article:

        lead_paragraph = self._run_model(
            ["Now, generate the lead paragraph for the completed article. Remember to make sure this paragraph is only 50 - 60 words, and can be read at a glance."],
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
