# Gradio Multi-Translator

A lightweight Gradio interface for comparing **Google Translate**,
**DeepL**, and **Baidu Translate** with one shared text input.

Maintained under the `digimarketingai` GitHub account.

> This is a translation website launcher, not a translation engine.
> Results appear on the external websites, not inside Gradio.

## Features

- Native Gradio interface.
- Shared source text.
- English, Chinese, Japanese, and Korean selections.
- Simple automatic source-language estimation.
- Individual translator buttons.
- Open All button.
- Generate Links fallback.
- Best-effort Close All.
- Local and Google Colab launch instructions.
- Optional password protection.
- No translation API keys required by this launcher.
- No model downloads or GPU required.

## Requirements

- Python 3.10 or newer.
- Git.
- A modern browser with JavaScript enabled.
- Internet access for installation and translation websites.

## Quick start

After this repository has been published:

```bash
git clone https://github.com/digimarketingai/gradio-multi-translator.git
cd gradio-multi-translator
python -m pip install -r requirements.txt
python app.py
```

The app attempts to open your browser automatically.

If it does not, open:

```text
http://127.0.0.1:7860
```

Keep the terminal running while using the app.

Press `Ctrl+C` in the terminal to stop the server.

## Recommended: use a virtual environment

### macOS / Linux

```bash
git clone https://github.com/digimarketingai/gradio-multi-translator.git
cd gradio-multi-translator

python3 -m venv .venv
source .venv/bin/activate

python -m pip install -r requirements.txt
python app.py
```

### Windows PowerShell

These commands use the virtual environment's Python directly, so activating
the environment is unnecessary.

```powershell
git clone https://github.com/digimarketingai/gradio-multi-translator.git
cd gradio-multi-translator

py -3 -m venv .venv

.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Make sure the Python interpreter selected is version 3.10 or newer.

## Google Colab

### Cell 1: clone and install

Run once per fresh Colab runtime:

```python
!git clone https://github.com/digimarketingai/gradio-multi-translator.git
%cd /content/gradio-multi-translator
%pip install -r requirements.txt
```

If Colab asks you to restart the runtime after installation, restart it,
change back to the repository directory, and continue.

### Cell 2: launch

```python
import gradio as gr
from app import create_app

demo = create_app("Hello! Welcome to the translation comparison tool.")

demo.launch(
    share=True,
    debug=True,
    theme=gr.themes.Soft(),
)
```

Open the generated public Gradio link in a separate browser tab.
Use that tab if the notebook's embedded interface blocks popups.

The share link is public. Do not use confidential text.

For password protection, use this instead:

```python
from getpass import getpass

import gradio as gr
from app import create_app

username = input("Choose a username: ").strip()
password = getpass("Choose a password: ")

if not username or not password:
    raise ValueError("Username and password must not be empty.")

demo = create_app()

demo.launch(
    share=True,
    debug=True,
    auth=(username, password),
    theme=gr.themes.Soft(),
)
```

Keep the Colab runtime active while using the app.

## How to use

1. Enter text.
2. Select the source language or leave it on Automatic.
3. Select the target language.
4. Click an individual translator or Open All.
5. Allow popups if your browser asks.
6. If popups are blocked, click Generate Links and use the links.
7. Compare results on the external websites.
8. Return to Gradio and click Close All when finished.

Changing the input removes previously generated links.

Existing translator windows do not update automatically.
Click an opening button again to request a new window or tab.

## Command-line options

### Different port

```bash
python app.py --port 7861
```

### Do not automatically open a browser

```bash
python app.py --no-browser
```

### Public share link

```bash
python app.py --share
```

A public share link makes the interface accessible to other people.
Use authentication if access should be restricted.

### Optional authentication

Set both environment variables before starting the app.

macOS / Linux:

```bash
export TRANSLATOR_USERNAME="your-username"
read -s -p "Password: " TRANSLATOR_PASSWORD
echo
export TRANSLATOR_PASSWORD

python app.py --share
```

The application refuses to start if only one credential is set.

### Listen on all network interfaces

```bash
python app.py --host 0.0.0.0 --no-browser
```

Use this only when you intend to expose the server to your network.
Configure authentication and your network firewall appropriately.

## Automatic language estimation

The app uses a simple script heuristic:

| Text contains | Estimated language |
| --- | --- |
| Japanese kana | Japanese |
| Korean Hangul | Korean |
| CJK ideographs | Chinese |
| None of the above | English |

This is not a trained language-detection model.

Mixed text, languages outside the supported selections, and Japanese
containing only kanji can be misclassified. Select the source manually
when needed.

The Chinese target mapping requests Traditional Chinese on Google.
The DeepL and Baidu URLs use a general Chinese code; output variants
are not standardized across providers.

## Browser limitations

- Browsers may block multiple popups from one click.
- Requested popup windows may appear as tabs instead.
- External websites may disconnect their window references.
- Close All can only request closure of windows it still controls.
- Tabs opened through fallback links must be closed manually.
- Refreshing the app loses its window registry.
- Close translator windows before refreshing or closing the app.

The status says “opening requested” rather than “translation successful”
because the app cannot inspect or verify the external website's result.

## Text length and provider compatibility

The app limits input to 5,000 Unicode code points per action.

This is an application limit, not a guarantee that every provider accepts
that much text through a URL. Shorter passages are more reliable.

Translation websites may change their URL formats, require login,
redirect requests, or impose their own restrictions.

If a website opens without the text:

1. Try a shorter passage.
2. Check the language selections.
3. Paste the text directly into the website.

URL construction is in `buildURLs()` inside `translator.js`.

## Privacy

- The project's translation actions use frontend JavaScript, not Python
  callbacks that process your text.
- The project does not implement a database or text logging.
- Gradio analytics are disabled in the app configuration.
- Opening a translator includes your text in its destination URL.
- Translation providers can receive and process that text.
- URLs may remain in browser history.
- A shared or remotely hosted app is not an offline or confidential
  processing environment.
- Avoid passwords, credentials, personal records, and confidential text.

Each translation provider has its own terms and privacy practices.

## Project files

```text
gradio-multi-translator/
├── app.py             # Gradio interface and launch options
├── translator.js      # Frontend URL and window handling
├── requirements.txt   # Python dependency
├── README.md
└── .gitignore
```

No Node.js installation is required.

## Troubleshooting

### `ModuleNotFoundError: No module named 'gradio'`

Install dependencies using the same interpreter used to run the app:

```bash
python -m pip install -r requirements.txt
python app.py
```

### The port is already in use

```bash
python app.py --port 7861
```

### The repository directory already exists

Skip the clone command and enter the existing directory.

### Popups are blocked

Click Generate Links, then open each link individually.

In Colab, open the public Gradio link in a separate browser tab.

### Close All leaves windows open

The browser or destination website may have disconnected the references.
Close those windows manually.

### A provider no longer opens with prefilled text

Its URL format may have changed. Paste the text manually and update
`buildURLs()` if necessary.

## Manual testing checklist

Before publishing a release:

- [ ] Install dependencies in a fresh virtual environment.
- [ ] Start the app with `python app.py`.
- [ ] Test each translator individually.
- [ ] Test Generate Links with popups blocked.
- [ ] Test Open All with popups allowed.
- [ ] Test Close All and manually close disconnected windows.
- [ ] Test English, Chinese, Japanese, and Korean.
- [ ] Test quotes, ampersands, emoji, and line breaks.
- [ ] Confirm blank input is rejected.
- [ ] Confirm input over 5,000 code points is rejected.
- [ ] Confirm editing text removes stale links.
- [ ] Test the Colab instructions.
- [ ] Test authentication before sharing a protected instance.

## Disclaimer

This project is not affiliated with Google, DeepL, or Baidu.
Availability and behavior of their translation websites are outside
this project's control.
