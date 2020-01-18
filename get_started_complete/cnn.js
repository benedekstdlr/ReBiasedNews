'use strict';
console.log("CNN");
window.onload = function (){
	var title=document.getElementsByClassName("pg-headline")[0];
	var firstpar=document.getElementsByClassName("el__leafmedia el__leafmedia--sourced-paragraph")[0];
	var input =title.innerHTML + " " +firstpar.innerHTML;
	var footer = document.getElementsByClassName("zn-body__paragraph zn-body__footer")[0];
		  output="<p>asdasdsads</p><p>agadhgagadgadg</p>"
	var content = document.getElementsByClassName("l-container")[0];
	content.innerHTML=firstpar + output + footer;
	};
		  