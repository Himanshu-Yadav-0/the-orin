const fileInput = document.getElementById("file-input");
const uploadButton = document.getElementById("upload-button");
const statusEl = document.getElementById("status");
const fileList = document.getElementById("file-list");
const dropVeil = document.getElementById("drop-veil");
const themeToggle = document.getElementById("theme-toggle");

const THEME_KEY = "orin-theme";

// Everything visual lives in style.css; only the wording is theme-aware here.
const VOICE = {
  light: {
    pending: "⏳",
    ok: "🌸",
    fail: "💔",
    sending: (n) => `sending ${n} file${n > 1 ? "s" : ""}...`,
    done: "all done! (๑˃ᴗ˂)ﻭ",
    partial: (sent, total) => `${sent}/${total} uploaded... (｡•́︿•̀｡)`,
    switchTo: "switch to the dark side",
  },
  dark: {
    pending: "⌛",
    ok: "🖤",
    fail: "⚔",
    sending: (n) => `claiming ${n} offering${n > 1 ? "s" : ""}...`,
    done: "sealed in the vault. ara ara~",
    partial: (sent, total) => `only ${sent}/${total} surrendered... how disappointing.`,
    switchTo: "switch to the sweet side",
  },
};

function currentTheme() {
  return document.documentElement.dataset.theme === "dark" ? "dark" : "light";
}

function voice() {
  return VOICE[currentTheme()];
}

function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  themeToggle.setAttribute("aria-pressed", String(theme === "dark"));
  themeToggle.setAttribute("aria-label", VOICE[theme].switchTo);
}

applyTheme(currentTheme());

themeToggle.addEventListener("click", () => {
  const next = currentTheme() === "dark" ? "light" : "dark";
  applyTheme(next);
  try {
    localStorage.setItem(THEME_KEY, next);
  } catch (error) {
    // Private browsing can block storage; the toggle still works for this visit.
  }
});

const successSound = new Audio(
  "/assets/shinobu-kocho-ara-ara-sayonara-demon-slayer-type.wav"
);
successSound.preload = "auto";

function playSuccessSound() {
  successSound.currentTime = 0;
  // Browsers reject playback without a user gesture; nothing to do if so.
  successSound.play().catch(() => {});
}

function setStatus(message, kind) {
  statusEl.textContent = message;
  statusEl.className = kind ? `status ${kind}` : "status";
}

// The API takes one file per request, so upload sequentially.
async function uploadFiles(files) {
  if (!files.length) return;

  uploadButton.classList.add("busy");
  fileList.innerHTML = "";
  setStatus(voice().sending(files.length));

  let sent = 0;
  for (const file of files) {
    const body = new FormData();
    body.append("files", file);

    const item = document.createElement("li");
    item.textContent = `${voice().pending} ${file.name}`;
    fileList.appendChild(item);

    try {
      const response = await fetch("/upload-files/", { method: "POST", body });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      item.textContent = `${voice().ok} ${file.name}`;
      sent += 1;
    } catch (error) {
      item.textContent = `${voice().fail} ${file.name} — ${error.message}`;
    }
  }

  uploadButton.classList.remove("busy");
  if (sent === files.length) {
    setStatus(voice().done, "ok");
    playSuccessSound();
  } else {
    setStatus(voice().partial(sent, files.length), "err");
  }
}

uploadButton.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", () => {
  uploadFiles([...fileInput.files]);
  fileInput.value = "";
});

let dragDepth = 0;

window.addEventListener("dragenter", (event) => {
  event.preventDefault();
  dragDepth += 1;
  dropVeil.classList.add("on");
});

window.addEventListener("dragover", (event) => event.preventDefault());

window.addEventListener("dragleave", () => {
  dragDepth = Math.max(0, dragDepth - 1);
  if (dragDepth === 0) dropVeil.classList.remove("on");
});

window.addEventListener("drop", (event) => {
  event.preventDefault();
  dragDepth = 0;
  dropVeil.classList.remove("on");
  uploadFiles([...event.dataTransfer.files]);
});
