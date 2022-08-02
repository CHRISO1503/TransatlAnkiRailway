// Get html elements for translation
var htmlElems = document.querySelectorAll('p,h1,h2,h3,h4,h5,h6');

// Bool which records the current state of the page
var translated = false;

// Convert html elements into their text comoponents
var htmlText = [];
for (i = 0; i < htmlElems.length; i++) {
    htmlText[i] = htmlElems[i].innerText;
}

// Send htmlText to background.js for translation
chrome.runtime.sendMessage({
    'htmlText': htmlText,
}, ).then(storeConvertedText);

// Poo mode
if (Math.random() < 0.01) {
    for (i = 0; i < htmlElems.length; i++) {
        console.log(htmlElems[i].innerText);
        htmlElems[i].innerText = 'poo';
    }
}


var convertedText = [];
// Store the converted text and apply the initial conversion to the page
function storeConvertedText(_convertedText) {
    convertedText = _convertedText;
    toggleTranslation();
    translated = true;
}

// Toggle the pages text's translated state
function toggleTranslation() {
    if (translated) {
        for (i = 0; i < htmlElems.length; i++) {
            htmlElems[i].innerText = htmlText[i];
        }
    } else {
        for (i = 0; i < htmlElems.length; i++) {
            htmlElems[i].innerText = convertedText[i];
        }
    }
}