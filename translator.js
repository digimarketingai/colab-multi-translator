(text, source, target) => {
    "use strict";

    const APP_KEY = __APP_KEY__;
    const ACTION = __ACTION__;

    const state = window[APP_KEY] || (
        window[APP_KEY] = { windows: [] }
    );

    const labels = {
        google: "Google Translate",
        deepl: "DeepL",
        baidu: "Baidu Translate"
    };

    const languageNames = {
        en: "English",
        zh: "Chinese",
        ja: "Japanese",
        ko: "Korean"
    };

    const services = ["google", "deepl", "baidu"];

    function detectLanguage(value) {
        if (/[\u3040-\u30ff\uff66-\uff9f]/u.test(value)) {
            return "ja";
        }

        if (/[\u1100-\u11ff\u3130-\u318f\uac00-\ud7af]/u.test(value)) {
            return "ko";
        }

        if (/[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]/u.test(value)) {
            return "zh";
        }

        return "en";
    }

    function buildURLs(value, from, to) {
        const google = new URL("https://translate.google.com/");

        google.searchParams.set(
            "sl",
            from === "zh" ? "zh-CN" : from
        );
        google.searchParams.set(
            "tl",
            to === "zh" ? "zh-TW" : to
        );
        google.searchParams.set("text", value);
        google.searchParams.set("op", "translate");

        const baiduCodes = {
            en: "en",
            zh: "zh",
            ja: "jp",
            ko: "kor"
        };

        const encodedText = encodeURIComponent(value);

        return {
            google: google.href,
            deepl:
                "https://www.deepl.com/translator#" +
                from + "/" + to + "/" + encodedText,
            baidu:
                "https://fanyi.baidu.com/#" +
                baiduCodes[from] + "/" +
                baiduCodes[to] + "/" +
                encodedText
        };
    }

    function renderLinks(urls) {
        // Construct HTML with DOM methods rather than interpolating
        // user-controlled text into HTML.
        const container = document.createElement("div");
        const heading = document.createElement("p");

        heading.textContent =
            "Fallback links — each opens in a new tab:";
        container.appendChild(heading);

        const list = document.createElement("ul");

        for (const service of services) {
            const item = document.createElement("li");
            const anchor = document.createElement("a");

            anchor.href = urls[service];
            anchor.target = "_blank";
            anchor.rel = "noopener noreferrer";
            anchor.textContent = "Open " + labels[service];

            item.appendChild(anchor);
            list.appendChild(item);
        }

        container.appendChild(list);

        const note = document.createElement("p");
        note.textContent =
            "Close tabs opened through these links manually.";
        container.appendChild(note);

        return container.outerHTML;
    }

    function openTranslator(service, url) {
        let popup = null;

        try {
            // Opening occurs in the frontend handler, without waiting
            // for a Python request or a network response.
            popup = window.open(
                "about:blank",
                "_blank",
                "popup=yes,width=1000,height=760,resizable=yes,scrollbars=yes"
            );

            if (!popup) {
                return labels[service] +
                    ": popup blocked. Use its fallback link below.";
            }

            // Remove the external page's reference to this app.
            // Keep our own reference for best-effort closing.
            popup.opener = null;
            popup.location.replace(url);

            state.windows.push(popup);

            return labels[service] + ": opening requested.";
        } catch (_) {
            if (popup) {
                try {
                    popup.close();
                } catch (_) {
                    // Browser restrictions may prevent cleanup.
                }
            }

            return labels[service] +
                ": browser refused the request. Use the link below.";
        }
    }

    function closeWindows() {
        let requested = 0;
        let disconnected = 0;
        let failed = 0;

        const remaining = [];

        for (const popup of state.windows) {
            try {
                if (!popup || popup.closed) {
                    disconnected++;
                    continue;
                }

                popup.close();
                requested++;

                // Retain live references so the user can retry.
                if (!popup.closed) {
                    remaining.push(popup);
                }
            } catch (_) {
                failed++;
                remaining.push(popup);
            }
        }

        state.windows = remaining;

        return [
            `Close requested for ${requested} window(s).`,
            `${disconnected} reference(s) already closed or disconnected.`,
            `${failed} request(s) failed.`,
            "If any translator remains visible, close it manually.",
            "Tabs opened through fallback links must be closed manually."
        ].join("\n");
    }

    if (ACTION === "close") {
        return [closeWindows(), ""];
    }

    text = String(text ?? "");

    if (!text.trim()) {
        return ["Enter some text first.", ""];
    }

    // An application-level limit, not a claimed provider limit.
    const characterCount = Array.from(text).length;

    if (characterCount > 5000) {
        return [
            "Please use 5,000 characters or fewer. " +
            "For longer documents, paste text directly into a translator.",
            ""
        ];
    }

    if (
        !Object.prototype.hasOwnProperty.call(languageNames, target) ||
        (
            source !== "auto" &&
            !Object.prototype.hasOwnProperty.call(languageNames, source)
        )
    ) {
        return ["Select valid source and target languages.", ""];
    }

    const detected = source === "auto";
    const from = detected ? detectLanguage(text) : source;

    let urls;
    let linksHTML;

    try {
        urls = buildURLs(text, from, target);
        linksHTML = renderLinks(urls);
    } catch (_) {
        return [
            "Could not encode the text. Remove invalid characters and retry.",
            ""
        ];
    }

    const messages = [
        `${detected ? "Estimated" : "Selected"} source: ` +
        `${languageNames[from]}. Target: ${languageNames[target]}.`
    ];

    if (from === target) {
        messages.push(
            "Source and target are the same. Change the target if needed."
        );
    }

    if (ACTION === "links") {
        messages.push(
            "Links generated. Open them individually below."
        );
        return [messages.join("\n"), linksHTML];
    }

    const selectedServices = ACTION === "all"
        ? services
        : services.filter(service => service === ACTION);

    if (!selectedServices.length) {
        return ["Unknown action.", linksHTML];
    }

    for (const service of selectedServices) {
        messages.push(openTranslator(service, urls[service]));
    }

    messages.push(
        "Opening requested does not confirm that the provider loaded " +
        "or accepted the text."
    );

    return [messages.join("\n"), linksHTML];
}
