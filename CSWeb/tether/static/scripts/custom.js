$(document).ready(function(){
	// Loads the Dota-2 theme
	$("#dota-2-theme").on("click", function(){
		$("#intro-img-1").attr("src", "images/dota_1.jpg");
		$("#intro-img-2").attr("src", "images/dota_3.jpg");
		$("#intro-img-3").attr("src", "images/dota_2.jpg");
	});

	// Loads the CS:GO theme
	$("#cs-go-theme").on("click", function(){
		$("#intro-img-1").attr("src", "images/cs-go-1.jpg");
		$("#intro-img-2").attr("src", "images/cs-go-3.jpg");
		$("#intro-img-3").attr("src", "images/cs-go-2.jpg");
	});

});