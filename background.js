// Give dictionary to content.js
chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
        var replacedText = replaceWords(request.htmlText);
        sendResponse(replacedText);
        // sendResponse(dictionary);
    }
)

// Initialize badge with LOAD
chrome.action.setBadgeText({
    text: 'LOAD'
});

// Ankiconnect
function anki(action, params = {}) {
    return fetch("http://127.0.0.1:8765/", {
        method: "POST",
        body: JSON.stringify({
            action,
            version: 6,
            params
        })
    }).then(res => res.json())
};

// Array of decks for translation
var vocabDecks = ['Korean Vocabulary by Evita']

// Get anki decks from computer
anki("deckNames").then(getCardsFromDecks);

// Get card IDs
function getCardsFromDecks(deckNames) {
    for (i = 0; i < deckNames.result.length; i++) {
        if (vocabDecks.includes(deckNames.result[i])) {
            anki("findCards", {
                query: "deck:" + '"' + deckNames.result[i] + '"'
            }).then(getCards);
        }
    }
}

// Use cardIDs to get card info
function getCards(cardIDs) {
    anki("cardsInfo", {
        cards: cardIDs.result
    }).then(makeTranslationLists);
}

// Add card info into objects which hold Korean and English translations
var dictionary = [];

function makeTranslationLists(cards) {
    for (i = 0; i < cards.result.length; i++) {
        if (cards.result[i].reps > 0) {
            // Sort out multiple English translations for same Korean word
            var _english = cards.result[i].fields.English.value;
            _english = _english.replace(/<div>/g, "");
            _english = _english.replace(/<\/div>/g, "");
            _english = _english.replace(/<br>/g, "");
            _english = _english.replace(/<\/br>/g, "");
            _english = _english.replace(/to /g, "");
            _english = _english.replace(/\(/g, "");
            _english = _english.replace(/\)/g, "");

            _englishWords = _english.split(/[,;]+/);

            for (j = 0; j < _englishWords.length; j++) {
                var _card = {
                    korean: cards.result[i].fields.Korean.value,
                    english: _englishWords[j].trim()
                }
                dictionary.push(_card)
            }
        }
    }
    // Set badge to ON
    chrome.action.setBadgeText({
        text: 'ON'
    });
}

// Replace words
function replaceWords(htmlText) {
    for (i = 0; i < dictionary.length; i++) {
        var searchRegExp = new RegExp(' ' + dictionary[i].english + '( |\\.|,)', 'gi');
        for (j = 0; j < htmlText.length; j++) {
            htmlText[j] = htmlText[j].replace(searchRegExp, ' ' + dictionary[i].korean + ' ');
        }
    }
    console.log(htmlText);
    console.log(dictionary);
    return htmlText;
}