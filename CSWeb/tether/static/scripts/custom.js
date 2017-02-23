$(document).ready(function(){
	// Loads the Dota-2 theme
	$("#dota-2-theme").on("click", function(){
		$("#intro-img-1").attr("src", "img/dota_1.jpg");
		$("#intro-img-2").attr("src", "img/dota_3.jpg");
		$("#intro-img-3").attr("src", "img/dota_2.jpg");
	});

	// Loads the CS:GO theme
	$("#cs-go-theme").on("click", function(){
		$("#intro-img-1").attr("src", "img/cs-go-1.jpg");
		$("#intro-img-2").attr("src", "img/cs-go-3.jpg");
		$("#intro-img-3").attr("src", "img/cs-go-2.jpg");
	});

});