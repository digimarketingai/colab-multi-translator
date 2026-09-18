# Colab Multi-Translator

A lightweight interface for opening **Google Translate**, **DeepL**, and
**Baidu Translate** with the same source text.

Designed for Google Colab, with an optional standalone HTML mode for
desktop browsers.

> This tool opens translation websites. It does not run a translation
> model, scrape results, or display translated output inside Colab.

## Features

- Shared text input for three translation websites.
- English, Chinese, Japanese, and Korean language selections.
- Simple automatic source-language estimation.
- Manual source-language override.
- Live source-text preview.
- Individual translator buttons.
- Open All button.
- Separate popup control panel.
- Best-effort Close All functionality.
- Keyboard shortcuts.
- Standalone HTML export.
- No translation API keys required by this launcher.

## Quick start: Google Colab

Run the following in a new Colab notebook:

```python
!git clone https://github.com/digimarketingai/colab-multi-translator.git
%cd colab-multi-translator

from multi_translator import create_translator

translator = create_translator("Hello World!")
```

Run the clone command once per fresh notebook runtime.

If you have already cloned the repository into `/content`, skip cloning:

```python
%cd /content/colab-multi-translator

from multi_translator import create_translator

translator = create_translator("Enter your text here.")
```

If the import reports that IPython is missing, install the dependency:

```python
%pip install -r requirements.txt
```

### How to use

1. Enter or paste your text.
2. Select a source language, or use the automatic heuristic.
3. Select the target language.
4. Allow popups when your browser asks.
5. Click **Open All**.
6. If only the control panel opens, click its **Google**, **DeepL**, and
   **Baidu** buttons individually.
7. Compare the results in the external translator windows.
8. Click **Close All** when finished.

The control panel uses the current text and language selections in the
main interface.

Changing the text does not automatically update external websites.
Click a translator button again to request an update.

## Keyboard shortcuts

| Shortcut | Action |
| --- | --- |
| Ctrl + Enter | Open all, on Windows/Linux |
| Command + Enter | Open all, on macOS |
| Esc | Close windows the interface still controls |

Shortcuts require focus inside the main interface or its control panel.
They do not operate while an external translation website has focus.

## Desktop usage

Clone the repository and run the Python file:

```bash
git clone https://github.com/digimarketingai/colab-multi-translator.git
cd colab-multi-translator
python multi_translator.py
```

This creates `translator.html` and attempts to open it in your default
browser. If the browser does not open, open the file manually.

The desktop HTML-export path uses Python's standard library.
IPython is only imported when displaying the interface in a notebook.

Do not use `!python multi_translator.py` to launch the notebook interface
in Colab. Use `create_translator()` instead.

## Python examples

### Start with empty text

```python
from multi_translator import create_translator

translator = create_translator()
```

### Start with Chinese text

```python
from multi_translator import create_translator

translator = create_translator("你好，歡迎使用多引擎翻譯比較工具！")
```

### Export a standalone HTML page

```python
from multi_translator import TranslatorInterface

interface = TranslatorInterface()

path = interface.save_html(
    filename="my_translator.html",
    text="Hello World!",
)

print(path)
```

When exporting from Colab, download the generated file and open it on
your own computer:

```python
from google.colab import files

files.download(str(path))
```

## Popup and Close All limitations

Browser security rules take priority over this tool.

- Browsers may block multiple popups from one click.
- Use the individual translator buttons if Open All is partially blocked.
- Browsers may open tabs instead of windows.
- Requested window sizes and positions may be ignored.
- External websites may disconnect their window references through
  cross-origin security policies.
- Close All can only request closure of windows it still controls.
- A disconnected window may remain visible and require manual closing.
- Close All does not close unrelated tabs or windows opened manually.
- Close translator windows before clearing the output, rerunning the
  interface cell, or closing the notebook.

The status area says "open requested" or "close requested" intentionally:
the interface cannot verify the external website's final behavior.

## Language detection

Automatic detection is a simple script heuristic, not a trained
language-identification model:

- Japanese kana → Japanese.
- Korean Hangul → Korean.
- Chinese/CJK ideographs → Chinese.
- Other input → English.

Japanese containing only kanji, mixed-language passages, and languages
outside these four choices may be misclassified.

Select the source language manually when needed.

The Chinese target mapping requests Traditional Chinese on Google.
The other launch URLs use a general Chinese language code; output
variants are not normalized across services.

## Privacy

- Clicking a translator button includes your text in the destination URL.
- The destination website can receive and process that text.
- Text may remain in browser history or other browser-managed storage.
- Initial text can also be retained in notebook output or exported HTML.
- Avoid entering passwords, credentials, or confidential information.
- This project's code does not implement analytics or a separate backend.

Each translation provider has its own terms and privacy practices.

## Troubleshooting

### Only the control panel opens

Allow popups and click the translator buttons individually.

### Close All leaves a translator open

The browser or website may have disconnected the window reference.
Close the remaining window manually.

### The preview displays incorrectly

Use the current `multi_translator.py` file and rerun the interface.
This version initializes the preview from the textarea rather than
inserting text directly into JavaScript.

### A translator opens without the expected text

The provider may have changed its URL format or redirected the request.
Try a shorter passage or paste the text into the translator manually.

URL construction is contained in the JavaScript `makeURL()` function
inside `multi_translator.py`.

### The interface appears but buttons do nothing

Rerun the cell in an active Colab session. Static notebook previews may
not execute the interface's JavaScript.

Alternatively, export the standalone HTML page and open it locally.

### The clone command says the directory already exists

Skip cloning and change into the existing repository directory.

## Project files

```text
colab-multi-translator/
├── README.md
├── multi_translator.py
├── requirements.txt
└── .gitignore
```

## Credits

This repository is not affiliated with Google, DeepL, or Baidu.
