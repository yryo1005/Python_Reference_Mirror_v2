"use strict";

const _OFFLINE_LANGUAGES = new Map([
  ["en", "English"],
  ["ja", "Japanese | 日本語"],
]);

const _CURRENT_VERSION = (() => {
  const release = window.DOCUMENTATION_OPTIONS?.VERSION || "3.14.6";
  return release.split(".", 2).join(".");
})();

const _detect_language = () => {
  const configured = window.DOCUMENTATION_OPTIONS?.LANGUAGE?.toLowerCase() || "en";
  if (configured === "none") return "en";
  if (configured === "ja") return "ja";
  return window.location.pathname.replace(/^\/+/, "").startsWith("ja") ? "ja" : "en";
};

const _CURRENT_LANGUAGE = _detect_language();

const _join_url = (...parts) =>
  "/" +
  parts
    .filter(Boolean)
    .map((part) => part.replace(/^\/+|\/+$/g, ""))
    .filter(Boolean)
    .join("/");

const _relative_page_path = () => {
  let path = window.location.pathname.replace(/^\/+/, "");
  if (path === "ja") {
    return "index.html";
  }
  if (path.startsWith("ja/")) {
    path = path.slice(3);
  }
  return path.replace(/^\/+/, "") || "index.html";
};

const _local_url_for = (language, pagePath) => {
  if (language === "ja") {
    return _join_url("ja", pagePath);
  }
  return _join_url(pagePath);
};

const _navigate_to_first_existing = async (urls) => {
  for (const url of urls) {
    try {
      const response = await fetch(url, { method: "HEAD" });
      if (response.ok) {
        window.location.href = url;
        return;
      }
    } catch (error) {
      console.error(`Error when fetching '${url}':`, error);
    }
  }
};

const _create_version_select = () => {
  const select = document.createElement("select");
  select.className = "version-select";
  select.setAttribute("aria-label", "Python version");
  select.disabled = true;
  select.title = "オフライン版では 3.14 のみ利用できます";

  const option = document.createElement("option");
  option.value = _CURRENT_VERSION;
  option.text = window.DOCUMENTATION_OPTIONS?.VERSION || _CURRENT_VERSION;
  option.selected = true;
  select.add(option);
  return select;
};

const _create_language_select = () => {
  const select = document.createElement("select");
  select.className = "language-select";
  select.setAttribute("aria-label", "Language");

  for (const [language, title] of _OFFLINE_LANGUAGES) {
    const option = document.createElement("option");
    option.value = language;
    option.text = title;
    option.selected = language === _CURRENT_LANGUAGE;
    select.add(option);
  }

  select.addEventListener("change", async (event) => {
    const selected = event.target.value;
    if (selected === _CURRENT_LANGUAGE) {
      return;
    }

    const pagePath = _relative_page_path();
    await _navigate_to_first_existing([
      _local_url_for(selected, pagePath),
      _local_url_for(selected, "index.html"),
    ]);
  });

  return select;
};

const _initialise_switchers = () => {
  document.querySelectorAll(".version_switcher_placeholder").forEach((placeholder) => {
    placeholder.replaceChildren(_create_version_select());
  });

  document.querySelectorAll(".language_switcher_placeholder").forEach((placeholder) => {
    placeholder.replaceChildren(_create_language_select());
  });
};

if (document.readyState !== "loading") {
  _initialise_switchers();
} else {
  document.addEventListener("DOMContentLoaded", _initialise_switchers);
}
