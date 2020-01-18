'use strict';
console.log("BREITBART");
chrome.tabs.executeScript(
          tabs[0].id,
          {code: 'document.body.style.backgroundColor = "' + color + '"; console.log("BREITBART");'});