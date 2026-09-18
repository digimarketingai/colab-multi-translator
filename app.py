"""Gradio launcher for comparing external translation websites."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from uuid import uuid4

import gradio as gr


ROOT = Path(__file__).resolve().parent

LANGUAGES = [
    ("English", "en"),
    ("Chinese", "zh"),
    ("Japanese", "ja"),
    ("Korean", "ko"),
]

WELCOME = (
    "Ready. Enter text, select languages, and open a translator. "
    "Use Generate Links if your browser blocks popups."
)


def create_app(initial_text: str = "") -> gr.Blocks:
    """Build the Gradio interface without starting its server."""
    js_file = ROOT / "translator.js"

    if not js_file.is_file():
        raise FileNotFoundError(
            f"Missing {js_file.name}. Keep it next to app.py."
        )

    js_template = js_file.read_text(encoding="utf-8")

    # Each built interface gets its own browser-side window registry.
    app_key = "digimarketingai_translator_" + uuid4().hex

    def handler(action: str) -> str:
        return (
            js_template
            .replace("__APP_KEY__", json.dumps(app_key))
            .replace("__ACTION__", json.dumps(action))
        )

    with gr.Blocks(
        title="Gradio Multi-Translator",
        analytics_enabled=False,
    ) as demo:
        gr.Markdown(
            """
# Gradio Multi-Translator

Compare **Google Translate**, **DeepL**, and **Baidu Translate**
using the same text.

This tool opens external translation websites.
Translated results are displayed on those websites, not inside this app.
"""
        )

        text = gr.Textbox(
            label="Text to translate",
            placeholder="Type or paste your text here...",
            value=initial_text,
            lines=8,
            max_lines=20,
        )

        with gr.Row():
            source = gr.Dropdown(
                label="Source language",
                choices=[
                    ("Automatic — simple heuristic", "auto"),
                    *LANGUAGES,
                ],
                value="auto",
                allow_custom_value=False,
            )

            target = gr.Dropdown(
                label="Target language",
                choices=LANGUAGES,
                value="en",
                allow_custom_value=False,
            )

        with gr.Row():
            google = gr.Button("Google Translate")
            deepl = gr.Button("DeepL")
            baidu = gr.Button("Baidu Translate")

        with gr.Row():
            open_all = gr.Button(
                "Open All",
                variant="primary",
            )
            generate = gr.Button("Generate Links")
            close_all = gr.Button(
                "Close All",
                variant="stop",
            )

        status = gr.Textbox(
            label="Status",
            value=WELCOME,
            lines=4,
            interactive=False,
        )

        links = gr.HTML(
            value="",
            label="Translation links",
        )

        gr.Markdown(
            """
**Popup blocked?** Click **Generate Links**, then open the links individually.

**Close All** only requests closure of windows opened by this app's buttons.
It does not control tabs opened through the fallback links.

Text is included in the destination URL. Do not enter passwords,
credentials, or confidential information.
"""
        )

        with gr.Accordion("Language detection and limitations", open=False):
            gr.Markdown(
                """
- Automatic source selection is a simple script heuristic, not an AI model.
- Japanese kana → Japanese.
- Korean Hangul → Korean.
- CJK ideographs → Chinese.
- Other input → English.
- For mixed text or Japanese containing only kanji, select the source manually.
- Google is configured to request Traditional Chinese as the Chinese target.
  DeepL and Baidu use a general Chinese language code.
- Provider URL formats may change. If text is not prefilled, paste it manually.
- Clicking an opening button again requests a new window or tab.
- Close translator windows before refreshing or closing this app.
"""
            )

        inputs = [text, source, target]
        outputs = [status, links]

        actions = [
            (google, "google"),
            (deepl, "deepl"),
            (baidu, "baidu"),
            (open_all, "all"),
            (generate, "links"),
            (close_all, "close"),
        ]

        for button, action in actions:
            button.click(
                fn=None,
                inputs=inputs,
                outputs=outputs,
                js=handler(action),
                queue=False,
            )

        # Remove stale links when text or language selections change.
        # These are frontend-only handlers, with no Python callback.
        reset_js = """
        () => [
            "Input changed. Open a translator or generate new links.",
            ""
        ]
        """

        text.input(
            fn=None,
            inputs=[],
            outputs=outputs,
            js=reset_js,
            queue=False,
        )

        for dropdown in (source, target):
            dropdown.change(
                fn=None,
                inputs=[],
                outputs=outputs,
                js=reset_js,
                queue=False,
            )

    return demo


def authentication_from_environment() -> tuple[str, str] | None:
    """Read optional credentials without putting passwords in source code."""
    username = os.environ.get("TRANSLATOR_USERNAME")
    password = os.environ.get("TRANSLATOR_PASSWORD")

    if bool(username) != bool(password):
        raise ValueError(
            "Set both TRANSLATOR_USERNAME and TRANSLATOR_PASSWORD, "
            "or leave both unset."
        )

    if username and password:
        return username, password

    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Launch the Gradio Multi-Translator."
    )

    parser.add_argument(
        "--share",
        action="store_true",
        help="Create a public Gradio share link.",
    )

    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Server bind address. Default: 127.0.0.1",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=7860,
        help="Server port. Default: 7860",
    )

    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not automatically open a browser.",
    )

    args = parser.parse_args()

    try:
        auth = authentication_from_environment()
    except ValueError as error:
        parser.error(str(error))

    if args.share and auth is None:
        print(
            "WARNING: --share creates a public link without login. "
            "Set TRANSLATOR_USERNAME and TRANSLATOR_PASSWORD "
            "to enable authentication."
        )

    demo = create_app()

    demo.launch(
        share=True,
        server_name=args.host,
        server_port=args.port,
        share=args.share,
        inbrowser=not args.no_browser,
        auth=auth,
        theme=gr.themes.Soft(),
    )


if __name__ == "__main__":
    main()
