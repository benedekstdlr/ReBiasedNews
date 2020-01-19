'use strict';
var titleText = document.getElementsByTagName("h1")[0].textContent;

var desc = document.getElementsByClassName("subheading")[0];
//var hasDesc = false;
if (desc) {
    //hasDesc = true;
    console.log("Description exists");
} else {
    var desc = document.getElementsByClassName("entry-content")[0].childNodes[1];
}
var descText = desc.textContent;
console.log("DESC: "+descText);
console.log("DESC: "+desc);

var request = new XMLHttpRequest();

request.open('POST', 'https://rebiasednews.ddns.net', true);
request.onload = function() {
    if(this.response === undefined || this.response.length == 0) {
        // TODO: nothing found
        console.log(this.response);
        console.log("Nothing found");
    } else {
        var resp = this.response;
        console.log(resp);
        document.getElementsByClassName("entry-content")[0].innerHTML = '<p class="subheading">'+descText+"<\p>"+"<p>"+resp+"<\p>";
    }
};
request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
var data = JSON.stringify({"title": titleText, "body": descText});
request.send(data);
