document.addEventListener("DOMContentLoaded", function() {
    var headerContainer = document.getElementById("header-container");
    var headerRequest = new XMLHttpRequest();
    headerRequest.open("GET", "header.html", true);
    headerRequest.onreadystatechange = function() {
        if (headerRequest.readyState === 4 && headerRequest.status === 200) {
            headerContainer.innerHTML = headerRequest.responseText;
        }
    };
    headerRequest.send();

    var footerContainer = document.getElementById("footer-container");
    var footerRequest = new XMLHttpRequest();
    footerRequest.open("GET", "footer.html", true);
    footerRequest.onreadystatechange = function() {
        if (footerRequest.readyState === 4 && footerRequest.status === 200) {
            footerContainer.innerHTML = footerRequest.responseText;
        }
    };
    footerRequest.send();

    const sendButton = document.getElementById('send');
    const promptText = document.getElementById('prompt-text');
    let eventSource;

    function setupSSE() {
        eventSource = new EventSource('/api/stream');
        eventSource.onopen = function(event) {
            sendButton.disabled = false;
        };
        eventSource.onmessage = function(event) {
            let formattedData = event.data.trim(); // Remove leading and trailing whitespace
            if (formattedData.endsWith('\n\n')) {
                formattedData = formattedData.slice(0, -2); 
            }
            appendContent(formattedData);
        };
        eventSource.onerror = function(event) {
            console.error("SSE error:", event);
            sendButton.disabled = true;
        };
    }

    setupSSE();

    sendButton.addEventListener('click', function() {
        const promptValue = promptText.value;
        promptText.value = ''; // Clear the input after sending
        fetch('/api/promptinput', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: promptValue }),
        })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
        })
        .catch(error => console.error('Error:', error));
    });
});


/**
 * Appends content to the document's output area with special handling for code blocks and titles.
 * Replaces escaped quotes with actual quotes and handles tab characters.
 * 
 * @param {string} data - The content to be appended. Can be plain text or JSON string with a message field.
 * @param {none}
 * @returns {void}
 */

// Global variables to manage the state of code blocks
let inCodeBlock = false;
let currentCodeWindow = null;
let currentCodeWindowTitle = null;

function appendContent(data) {
    const outputArea = document.getElementById('ai-prompt-output-area');

    try {
        const jsonData = JSON.parse(data.replace(/\\"/g, '"').replace(/\\t/g, '\t'));
        data = jsonData.message || data;
    } catch (e) {
        data = data.replace(/\\"/g, '"').replace(/\\t/g, '\t');
    }

    data = data.substring(1, data.length - 1);

    if (data === '```') {
        if (inCodeBlock) {
            inCodeBlock = false;
        } else {
            inCodeBlock = true;
            const codeBlockContainer = document.createElement('div');
            codeBlockContainer.classList.add('code-block-container');

            const codeHeader = document.createElement('div');
            codeHeader.classList.add('code-header');

            currentCodeWindow = document.createElement('pre');

            const copyBtn = document.createElement('button');
            copyBtn.textContent = 'Copy';
            copyBtn.id = 'copy-btn';
            // Update the onclick function to reference the specific pre element
            copyBtn.onclick = function () {
                navigator.clipboard.writeText(currentCodeWindow.textContent).then(() => {
                    console.log('Text copied to clipboard');
                }).catch(err => {
                    console.error('Failed to copy text: ', err);
                });
            };

            codeHeader.appendChild(copyBtn);
            codeBlockContainer.appendChild(codeHeader);
            codeBlockContainer.appendChild(currentCodeWindow);
            outputArea.appendChild(codeBlockContainer);
        }
    } else if (inCodeBlock && currentCodeWindowTitle === null) {
        currentCodeWindowTitle = data.trim();
        const titleElement = document.createElement('span');
        titleElement.textContent = currentCodeWindowTitle;
        titleElement.classList.add('code-title');
        const codeHeader = currentCodeWindow.previousSibling;
        codeHeader.insertBefore(titleElement, codeHeader.firstChild);
    } else if (inCodeBlock) {
        data.split('\\n').forEach((line, index, array) => {
            currentCodeWindow.textContent += line;
            if (index < array.length - 1) {
                currentCodeWindow.textContent += '\n';
            }
        });
    } else {
        data = data.replace(/\\n/g, '<br>').replace(/\\t/g, '&nbsp;&nbsp;&nbsp;&nbsp;');
        outputArea.innerHTML += data;
    }

    outputArea.scrollTop = outputArea.scrollHeight;
}
