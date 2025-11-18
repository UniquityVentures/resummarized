from google import genai
from celery_progress.backend import ProgressRecorder
from google.genai import types
from .models import Source, ArxivSource, WebSource, Article
from typing import List
import requests
import tempfile

client = genai.Client()


class AIArticleGenerator:
    source: Source
    chat: genai.chats.Chat
    total_steps: int
    current_step: int

    def increment_step(self, message=None):
        self.current_step += 1
        self.progress_recorder.set_progress(
            self.current_step,
            self.total_steps,
            f"Processing item {self.current_step}..."
            if message is not None
            else message,
        )

    def __init__(
        self,
        progress_recorder: ProgressRecorder,
        source: Source,
        model: str = "models/gemini-2.5-flash",
    ):
        self.model = model
        self.source = source
        self.progress_recorder = progress_recorder
        files = []
        sources = source.sources()
        self.total_steps = len(sources) + 1 + 10
        for single_source in sources:
            if isinstance(single_source, ArxivSource):
                files.append(self._process_arxiv_source(single_source))
            elif isinstance(single_source, WebSource):
                files.append(self._process_web_source(single_source))

        self.chat = client.chats.create(
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
        response.raise_for_status()  # Raise an exception for bad status codes
        with tempfile.NamedTemporaryFile(mode="w+b", delete=True) as temp:
            for chunk in response.iter_content(chunk_size=8192):
                temp.write(chunk)
            temp.flush()
            temp.seek(0)
            return types.Part.from_bytes(data=temp.read(), mime_type="text/html")

    def _run_model(self, text: List[str], max_output_tokens: int):
        return self.chat.send_message(
            message=[types.Part.from_text(text=text_segment) for text_segment in text],
            config=types.GenerateContentConfig(max_output_tokens=max_output_tokens),
        ).text

    def generate_article(self) -> Article:
        prompt = """
        You are an expert article writer. Based on the provided sources, generate a comprehensive article.
        Ensure the article is well-structured, informative, and engaging.
        Use proper citations where necessary.
        Don't use references in the article, for figures or anything else.
        You will generate the parts of the article step by step.
        Don't add anything extra outside of the requested sections.
        Don't use any syntax outside of markdown, only output the markdown, nothing else.
        The article should include the following sections:

        title = models.TextField(description="Short catchy title that will be displayed at the top of article and in listings.")

        For the following, use as much markdown as is required to format the text properly.

        background_context = models.TextField(description="Contextual information leading up to the research.")
        research_question = models.TextField(description="The primary question the research aims to answer.")
        simplified_methods = models.TextField(description="A simplified explanation of the methods used in the study.")
        core_findings = models.TextField(description="The main findings of the research.")
        surprise_finding = models.TextField(description="Any unexpected results from the study.")
        future_implications = models.TextField(description="The potential implications of the research findings.")
        study_limitations = models.TextField(description="Limitations of the study that may affect interpretation of results.")
        next_steps = models.TextField(description="Suggested future research directions based on the study.")
            """

        lead_response_paragraph = self._run_model(
            [
                prompt,
                "Based on the provided sources, please generate the article step by step.",
                "We will be generating title in the final step."
                "Please generate the lead paragraph of the article.",
            ],
            max_output_tokens=250,
        )

        self.increment_step("Generating the lead paragraph")

        background_context = self._run_model(
            [
                "Great! Now, based on the lead paragraph please generate the background context."
            ],
            max_output_tokens=1000,
        )

        self.increment_step("Generating the background context")

        research_question = self._run_model(
            [
                "Now, please generate the research question based on the background context."
            ],
            max_output_tokens=500,
        )

        self.increment_step("Generating the research question")

        simplified_methods = self._run_model(
            ["Next, please generate the simplified methods section."],
            max_output_tokens=1000,
        )

        self.increment_step("Generating the simplified methods")

        core_findings = self._run_model(
            ["Now, please generate the core findings of the research."],
            max_output_tokens=1000,
        )

        self.increment_step("Generating the core findings")

        surprise_finding = self._run_model(
            ["Please generate any surprise findings from the study."],
            max_output_tokens=500,
        )

        self.increment_step("Generating the surprise finding")

        future_implications = self._run_model(
            ["Now, please generate the future implications of the research findings."],
            max_output_tokens=500,
        )

        self.increment_step("Generating the future implications")

        study_limitations = self._run_model(
            [
                "Please outline the study limitations that may affect interpretation of results."
            ],
            max_output_tokens=500,
        )

        self.increment_step("Generating the study limitations")

        next_steps = self._run_model(
            [
                "Finally, please suggest next steps for future research based on the study."
            ],
            max_output_tokens=500,
        )

        self.increment_step("Generating the next steps")

        title = self._run_model(
            ["Now, generate the title for the completed article."],
            max_output_tokens=100,
        )

        self.increment_step("Generating the title")

        article = Article(
            title=title,
            lead_paragraph=lead_response_paragraph,
            background_context=background_context,
            research_question=research_question,
            simplified_methods=simplified_methods,
            core_findings=core_findings,
            surprise_finding=surprise_finding,
            future_implications=future_implications,
            study_limitations=study_limitations,
            next_steps=next_steps,
            based_on=self.source,
        )
        return article
