window.post = (url, data) => {
  return fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify(data),
  });
};

document.getElementById("summarise").addEventListener("click", () => {
  getDOMText().then((text) => {
    post("http://127.0.0.1:8000/summarise", {
      text: text,
    })
      .then((response) => {
        if (response.ok) {
          response.json().then((json) => {
            document.getElementById("summary").innerHTML = json.summary;
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
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  result = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => {
      return document.body.innerText;
    },
    args: [],
  });

  return result[0].result;
}
