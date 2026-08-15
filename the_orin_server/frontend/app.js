const fileInput = document.getElementById("file-input");
const uploadButton = document.getElementById("upload-button");
const statusEl = document.getElementById("status");
const fileList = document.getElementById("file-list");
const dropVeil = document.getElementById("drop-veil");

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
  setStatus(`sending ${files.length} file${files.length > 1 ? "s" : ""}...`);

  let sent = 0;
  for (const file of files) {
    const body = new FormData();
    body.append("files", file);

    const item = document.createElement("li");
    item.textContent = `⏳ ${file.name}`;
    fileList.appendChild(item);

    try {
      const response = await fetch("/upload-files/", { method: "POST", body });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      item.textContent = `🌸 ${file.name}`;
      sent += 1;
    } catch (error) {
      item.textContent = `💔 ${file.name} — ${error.message}`;
    }
  }

  uploadButton.classList.remove("busy");
  if (sent === files.length) {
    setStatus("all done! (๑˃ᴗ˂)ﻭ", "ok");
    playSuccessSound();
  } else {
    setStatus(`${sent}/${files.length} uploaded... (｡•́︿•̀｡)`, "err");
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
