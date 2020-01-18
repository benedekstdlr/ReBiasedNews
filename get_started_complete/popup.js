'use strict';

let change = document.getElementById('change');
change.onclick = function(element) {
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    var url = tabs[0].url;
    var re = new RegExp(".*\.breitbart\.com/politics/..../../../.*");
    if (re.test(url)) {
        chrome.tabs.executeScript(
            tabs[0].id,
            {file: 'breitbart.js'});
    } else {
        chrome.tabs.executeScript(
            tabs[0].id,
            {file: 'cnn.js'});
    }
  });
};
