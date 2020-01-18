'use strict';
window.onload = function() {
    console.log("BREITBART");
    //window.alert("Breitbart!!!");

    var title = document.getElementsByTagName("h1")[0];
    title.innerHTML = "Hello World!";

    var desc = document.getElementsByClassName("subheading")[0];
    //var hasDesc = false;
    console.log(desc);
    if (desc) {
        //hasDesc = true;
        console.log("Description exists");
    } else {
        var desc = document.getElementsByClassName("entry-content")[0].childNodes[1];
    }
    var descText = desc.innerHTML;
    console.log(descText);
    console.log(desc);
    var generatedText = "REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE";
    document.getElementsByClassName("entry-content")[0].innerHTML = '<p class="subheading">'+descText+"<\p>"+"<p>"+generatedText+"<\p>";
    
};
