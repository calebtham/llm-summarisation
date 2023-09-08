window.post = (url, data) => {
  return fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify(data),
  });
};

document.getElementById("summarise").addEventListener("click", () => {
  const summaryDiv = document.getElementById("summary");
  const summariseBtn = document.getElementById("summarise");
  const summariseIcon = document.getElementById("summarise-icon");

  summariseBtn.style.paddingLeft = "6px";
  summariseIcon.src = "../svg/spinner.svg";

  getDOMText().then((text) => {
    post("http://127.0.0.1:8000/summarise", {
      text: text,
    })
      .then((response) => {
        if (response.ok) {
          response.json().then((json) => {
            summaryDiv.hidden = false;
            summaryDiv.innerHTML = textToHTML(json.summary);
            summariseBtn.remove();
          });
        } else {
          alert("HTTP-Error: " + response.status);
        }
      })
      .catch((error) => {
        alert("HTTP-Error: " + error);
      });
  });
});

async function getDOMText() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const result = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => {
      return document.body.innerText;
    },
    args: [],
  });

  return result[0].result;
}

function textToHTML(text) {
  return ("\n" + text)
    .split("\n- ")
    .map((b) => b.replace("\n", " "))
    .map((b) => b.trim())
    .filter((b) => b.length > 0)
    .map(
      (bulletPoint) =>
        `
        <div class="bullet-point">
          <img class="icon" src="../svg/bulletpoint-outline.svg" alt="bulletpoint" width="20" height="20"/>
          <p>
            ${bulletPoint}
          </p>
        </div>
        `
    )
    .join("");
}
