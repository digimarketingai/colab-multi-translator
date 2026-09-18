"""Translation website launcher for Google Colab and desktop browsers."""

from html import escape
from pathlib import Path
from uuid import uuid4

__version__ = "0.1.0"
__all__ = ["TranslatorInterface", "create_translator"]


_PAGE = r'''
<div id="__UID__" tabindex="-1">
<style>
#__UID__ {
    max-width: 1000px;
    margin: 20px auto;
    padding: 28px;
    background: #fff;
    color: #202124;
    border-radius: 16px;
    box-shadow: 0 4px 22px #00000015;
    font-family: Arial, sans-serif;
}
#__UID__, #__UID__ * { box-sizing: border-box; }
#__UID__ h2 {
    color: #356fe5;
    text-align: center;
    font-size: 30px;
    margin: 0 0 12px;
}
#__UID__ .subtitle {
    text-align: center;
    color: #5f6368;
    margin-bottom: 22px;
}
#__UID__ .note {
    background: #fff8df;
    border: 1px solid #ffe7a0;
    padding: 14px;
    border-radius: 10px;
    margin-bottom: 20px;
    line-height: 1.6;
}
#__UID__ textarea {
    width: 100%;
    min-height: 170px;
    padding: 16px;
    border: 2px solid #e2e5ea;
    border-radius: 9px;
    font-size: 17px;
    line-height: 1.6;
    resize: vertical;
}
#__UID__ textarea:focus, #__UID__ select:focus {
    outline: 2px solid #aecbfa;
    border-color: #4285f4;
}
#__UID__ .languages, #__UID__ .buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin: 18px 0;
    align-items: center;
}
#__UID__ select {
    padding: 9px;
    border-radius: 7px;
    border: 1px solid #dadce0;
    background: white;
    color: #202124;
    font-size: 15px;
}
#__UID__ button {
    flex: 1 1 125px;
    padding: 13px 15px;
    border: 0;
    border-radius: 8px;
    background: #356fe5;
    color: white;
    cursor: pointer;
    font-size: 14px;
    font-weight: bold;
}
#__UID__ button:hover { filter: brightness(1.1); }
#__UID__ button:focus-visible {
    outline: 3px solid #fbbc04;
    outline-offset: 2px;
}
#__UID__ [data-action="google"] { background: #4285f4; }
#__UID__ [data-action="deepl"] { background: #102f50; }
#__UID__ [data-action="baidu"] { background: #3030dd; }
#__UID__ [data-action="close"] { background: #cf3e49; }
#__UID__ [data-action="panel"] { background: #586579; }
#__UID__ .box {
    padding: 16px;
    background: #f8f9fa;
    border: 1px solid #e3e6eb;
    border-radius: 9px;
    margin-top: 18px;
    line-height: 1.6;
}
#__UID__ [data-role="preview"] {
    white-space: pre-wrap;
    overflow-wrap: anywhere;
    max-height: 250px;
    overflow: auto;
    margin-top: 8px;
}
#__UID__ [data-role="status"] {
    white-space: pre-wrap;
    overflow-wrap: anywhere;
    background: #eef3ff;
}
#__UID__ [data-error="true"] {
    background: #fff0ef;
    color: #9e2424;
}
#__UID__ .small { font-size: 13px; color: #5f6368; }
#__UID__ kbd {
    background: white;
    padding: 3px 6px;
    border: 1px solid #dadce0;
    border-radius: 4px;
}
@media (max-width: 600px) {
    #__UID__ { padding: 16px; }
    #__UID__ h2 { font-size: 24px; }
}
</style>

<h2>Multi-Translator Interface</h2>
<div class="subtitle">
    Compare translations from Google, DeepL, and Baidu
</div>

<div class="note">
    Allow popups before clicking <b>Open All</b>.
    If only the control panel opens, use its individual translator buttons.
    <br>
    請允許瀏覽器彈出視窗；若只開啟控制面板，請逐一點擊翻譯按鈕。
</div>

<textarea
    data-role="text"
    aria-label="Text to translate"
    placeholder="Enter text to translate..."
>__TEXT__</textarea>

<div class="languages">
    <label>
        Source:
        <select data-role="source">
            <option value="auto">Automatic (simple heuristic)</option>
            <option value="en">English</option>
            <option value="zh">Chinese</option>
            <option value="ja">Japanese</option>
            <option value="ko">Korean</option>
        </select>
    </label>
    <label>
        Target:
        <select data-role="target">
            <option value="en">English</option>
            <option value="zh">Chinese</option>
            <option value="ja">Japanese</option>
            <option value="ko">Korean</option>
        </select>
    </label>
</div>

<div class="small" data-role="detected"></div>

<div class="buttons">
    <button type="button" data-action="all">OPEN ALL</button>
    <button type="button" data-action="google">GOOGLE</button>
    <button type="button" data-action="deepl">DEEPL</button>
    <button type="button" data-action="baidu">BAIDU</button>
    <button type="button" data-action="close">CLOSE ALL</button>
</div>

<div class="buttons">
    <button type="button" data-action="panel">OPEN CONTROL PANEL</button>
</div>

<div class="box" data-role="status" role="status" aria-live="polite">
    Ready. Enter text and choose a target language.
</div>

<div class="box">
    <b>Current Text</b>
    <div data-role="preview"></div>
</div>

<div class="box">
    <b>Keyboard shortcuts</b><br>
    Open all: <kbd>Ctrl / ⌘ + Enter</kbd><br>
    Close controlled windows: <kbd>Esc</kbd>
    <div class="small">
        Shortcuts work when this interface or its control panel has focus.
        Close windows before clearing or rerunning this notebook output.
    </div>
</div>
</div>

<script>
(() => {
    "use strict";

    const root = document.getElementById("__UID__");
    const get = role => root.querySelector(`[data-role="${role}"]`);
    const input = get("text");
    const source = get("source");
    const target = get("target");
    const status = get("status");

    const services = ["google", "deepl", "baidu"];
    const labels = {google: "Google", deepl: "DeepL", baidu: "Baidu"};
    const languages = {
        en: "English", zh: "Chinese", ja: "Japanese", ko: "Korean"
    };

    const refs = {
        google: null, deepl: null, baidu: null, panel: null
    };

    const mapping = {
        google: {en: "en", zh: "zh-TW", ja: "ja", ko: "ko"},
        deepl: {en: "en", zh: "zh", ja: "ja", ko: "ko"},
        baidu: {en: "en", zh: "zh", ja: "jp", ko: "kor"}
    };

    let panelStatus = null;

    function alive(w) {
        try {
            return Boolean(w && !w.closed);
        } catch (_) {
            return false;
        }
    }

    function focus(w) {
        try {
            if (alive(w)) w.focus();
        } catch (_) {}
    }

    function report(message, error = false) {
        status.textContent = message;
        status.dataset.error = String(error);

        try {
            if (alive(refs.panel) && panelStatus) {
                panelStatus.textContent = message;
            }
        } catch (_) {}
    }

    function detect(text) {
        if (/[\u3040-\u30ff\uff66-\uff9f]/u.test(text)) return "ja";
        if (/[\u1100-\u11ff\u3130-\u318f\uac00-\ud7af]/u.test(text)) {
            return "ko";
        }
        if (/[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]/u.test(text)) {
            return "zh";
        }
        return "en";
    }

    function sourceLanguage() {
        return source.value === "auto" ? detect(input.value) : source.value;
    }

    function updatePreview() {
        get("preview").textContent = input.value || "Enter text above";
        get("detected").textContent =
            `${source.value === "auto" ? "Estimated" : "Selected"} source: `
            + languages[sourceLanguage()]
            + ". Select the source manually for ambiguous or mixed text.";
    }

    function makeURL(service) {
        const from = sourceLanguage();
        const to = target.value;
        const map = mapping[service];

        if (service === "google") {
            const url = new URL("https://translate.google.com/");
            url.searchParams.set("sl", from === "zh" ? "zh-CN" : map[from]);
            url.searchParams.set("tl", map[to]);
            url.searchParams.set("text", input.value);
            url.searchParams.set("op", "translate");
            return url.href;
        }

        const base = service === "deepl"
            ? "https://www.deepl.com/translator#"
            : "https://fanyi.baidu.com/#";

        return base + map[from] + "/" + map[to] + "/"
            + encodeURIComponent(input.value);
    }

    function features(index = 0, panel = false) {
        const s = window.screen;
        const sw = s.availWidth || 1280;
        const sh = s.availHeight || 800;

        const width = panel
            ? Math.min(540, sw)
            : Math.min(sw, Math.max(320, Math.floor(sw / 3)));

        const height = panel
            ? Math.min(440, sh)
            : Math.min(sh, Math.max(400, Math.floor(sh * 0.8)));

        const originX = Number.isFinite(s.availLeft) ? s.availLeft : 0;
        const originY = Number.isFinite(s.availTop) ? s.availTop : 0;

        const left = originX + (panel
            ? Math.floor((sw - width) / 2)
            : Math.min(index * width, Math.max(0, sw - width)));

        const top = originY + (panel
            ? Math.floor((sh - height) / 2)
            : 0);

        return `popup=yes,width=${width},height=${height},`
            + `left=${left},top=${top},resizable=yes,scrollbars=yes`;
    }

    function openService(service) {
        const label = labels[service];

        if (!input.value.trim()) {
            return {ok: false, message: "Enter some text first."};
        }

        let url;
        try {
            url = makeURL(service);
        } catch (error) {
            return {ok: false, message: `${label}: ${error.message}`};
        }

        const existing = refs[service];

        if (alive(existing)) {
            try {
                existing.location.href = url;
                focus(existing);
                return {ok: true, message: `${label}: update requested.`};
            } catch (_) {
                return {
                    ok: false,
                    message: `${label}: cannot update the existing window. `
                        + "Close it manually and try again."
                };
            }
        }

        let popup = null;

        try {
            // Keep window.open synchronous in the click handler.
            popup = window.open(
                "about:blank",
                "__UID___" + service,
                features(services.indexOf(service))
            );

            if (!popup) {
                return {
                    ok: false,
                    message: `${label}: popup blocked. Allow popups, `
                        + "then click its individual button."
                };
            }

            refs[service] = popup;

            // The external website should not retain an opener reference.
            // We retain our own reference for best-effort close().
            popup.opener = null;
            popup.location.href = url;
            focus(popup);

            return {ok: true, message: `${label}: open requested.`};

        } catch (error) {
            try {
                if (popup) popup.close();
            } catch (_) {}

            refs[service] = null;

            return {
                ok: false,
                message: `${label}: ${error.message}`
            };
        }
    }

    function closeAll() {
        let requested = 0;
        let unavailable = 0;
        let failed = 0;

        for (const service of services) {
            const w = refs[service];
            if (!w) continue;

            try {
                if (w.closed) {
                    // A disconnected reference may appear closed even
                    // when the external website is still visible.
                    unavailable++;
                    refs[service] = null;
                    continue;
                }

                w.close();
                requested++;

                // Retain a still-live reference so closing can be retried.
                if (w.closed) refs[service] = null;

            } catch (_) {
                failed++;
            }
        }

        report(
            `Close requested for ${requested} translator window(s).`
            + (unavailable
                ? ` ${unavailable} reference(s) already closed or disconnected.`
                : "")
            + (failed ? ` ${failed} request(s) failed.` : "")
            + "\nIf a translator remains visible, close it manually.",
            failed > 0
        );

        // Close the controller last.
        try {
            if (alive(refs.panel)) refs.panel.close();
        } catch (_) {}

        if (!alive(refs.panel)) {
            refs.panel = null;
            panelStatus = null;
        }
    }

    function shortcut(event) {
        if (event.isComposing) return;

        if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) {
            event.preventDefault();
            event.stopPropagation();
            openAll();
        } else if (event.key === "Escape") {
            event.preventDefault();
            event.stopPropagation();
            closeAll();
        }
    }

    function openPanel() {
        if (alive(refs.panel)) {
            focus(refs.panel);
            return {ok: true, message: "Control panel is open."};
        }

        let popup = null;

        try {
            popup = window.open(
                "about:blank",
                "__UID___panel",
                features(0, true)
            );

            if (!popup) {
                return {
                    ok: false,
                    message: "Control panel blocked. Allow popups and "
                        + "click OPEN CONTROL PANEL separately."
                };
            }

            refs.panel = popup;

            const doc = popup.document;
            doc.open();
            doc.write(`<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Translation Control Panel</title>
<style>
    * { box-sizing: border-box; }
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 24px;
        background: #f4f7fc;
        color: #202124;
        text-align: center;
    }
    h2 { color: #356fe5; margin-top: 0; }
    p { line-height: 1.5; }
    .buttons {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 8px;
    }
    button {
        padding: 12px 16px;
        border: 0;
        border-radius: 8px;
        background: #356fe5;
        color: white;
        font-weight: bold;
        cursor: pointer;
    }
    #close {
        display: block;
        width: 100%;
        margin: 20px 0;
        background: #cf3e49;
        font-size: 18px;
    }
    #status {
        white-space: pre-wrap;
        overflow-wrap: anywhere;
        text-align: left;
        font-size: 13px;
        line-height: 1.5;
    }
</style>
</head>
<body>
    <h2>Translation Control Panel</h2>
    <p>Uses the current text and language selections in the main interface.</p>
    <div class="buttons">
        <button id="google">Google</button>
        <button id="deepl">DeepL</button>
        <button id="baidu">Baidu</button>
    </div>
    <button id="close">CLOSE ALL WINDOWS</button>
    <p>Press Esc here to close controlled windows.</p>
    <div id="status" role="status"></div>
</body>
</html>`);
            doc.close();

            panelStatus = doc.getElementById("status");
            panelStatus.textContent = status.textContent;

            // Direct callbacks avoid depending on a global function
            // such as window.opener.closeAllWindows().
            doc.getElementById("close").addEventListener("click", closeAll);

            for (const service of services) {
                doc.getElementById(service).addEventListener("click", () => {
                    const result = openService(service);
                    report(result.message, !result.ok);
                });
            }

            doc.addEventListener("keydown", shortcut);
            focus(popup);

            return {ok: true, message: "Control panel is open."};

        } catch (error) {
            try {
                if (popup) popup.close();
            } catch (_) {}

            refs.panel = null;
            panelStatus = null;

            return {
                ok: false,
                message: "Control panel error: " + error.message
            };
        }
    }

    function openAll() {
        if (!input.value.trim()) {
            report("Enter some text first.", true);
            input.focus();
            return;
        }

        // Open the panel first. If only one popup is allowed, its
        // individual buttons provide a separate-click fallback.
        const results = [openPanel()];

        for (const service of services) {
            results.push(openService(service));
        }

        report(
            results.map(result => result.message).join("\n"),
            results.some(result => !result.ok)
        );

        focus(refs.panel);
    }

    root.querySelectorAll("[data-action]").forEach(button => {
        button.addEventListener("click", () => {
            const action = button.dataset.action;

            if (action === "all") {
                openAll();
            } else if (action === "close") {
                closeAll();
            } else {
                const result = action === "panel"
                    ? openPanel()
                    : openService(action);

                report(result.message, !result.ok);
            }
        });
    });

    input.addEventListener("input", updatePreview);
    source.addEventListener("change", updatePreview);
    root.addEventListener("keydown", shortcut);

    // Best-effort cleanup; normal closing should use the Close All button.
    window.addEventListener("pagehide", () => {
        for (const w of Object.values(refs)) {
            try {
                if (alive(w)) w.close();
            } catch (_) {}
        }
    });

    updatePreview();
})();
</script>
'''


class TranslatorInterface:
    """Create, display, or export the translator interface."""

    def create_page(self, text=""):
        """Return the interface as an HTML fragment."""
        uid = "translator_" + uuid4().hex

        # Insert escaped user text last to prevent HTML/script injection
        # and accidental replacement of placeholder-like user content.
        return (
            _PAGE
            .replace("__UID__", uid)
            .replace("__TEXT__", escape(str(text), quote=True))
        )

    def display(self, text=""):
        """Display the interface in a notebook with HTML/JS support."""
        from IPython.display import HTML, display

        display(HTML(self.create_page(text)))
        return self

    def save_html(self, filename="translator.html", text=""):
        """Save a standalone HTML page and return its absolute Path."""
        destination = Path(filename).expanduser().resolve()

        document = (
            "<!doctype html>\n"
            '<html lang="en">\n<head>\n'
            '<meta charset="utf-8">\n'
            '<meta name="viewport" '
            'content="width=device-width, initial-scale=1">\n'
            "<title>Multi-Translator</title>\n"
            "</head>\n<body>\n"
            + self.create_page(text)
            + "\n</body>\n</html>\n"
        )

        destination.write_text(document, encoding="utf-8")
        return destination


def create_translator(initial_text=""):
    """Display the translator and return its interface object."""
    return TranslatorInterface().display(initial_text)


if __name__ == "__main__":
    # Desktop usage: python multi_translator.py
    # In Colab, import create_translator instead.
    import webbrowser

    output = TranslatorInterface().save_html(text="Hello World!")
    print(f"Saved interface to: {output}")

    if not webbrowser.open(output.as_uri()):
        print("Open the saved HTML file manually in your browser.")
