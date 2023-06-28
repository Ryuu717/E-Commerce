////////////////////////////////////////////////////////////////////////////////////
// Carousel
////////////////////////////////////////////////////////////////////////////////////
var scrollPosition = 0; 

// Top Categories
var carouselWidthTopCategories = $('.carousel-inner-top-categories')[0].scrollWidth; 
var TopCategories = $('.carousel-item-top-categories').width(); 

$('.carousel-control-top-categories-next').on('click', function(){
    if(scrollPosition < (carouselWidthTopCategories - (TopCategories * 4))){ 
        console.log('next'); 
        scrollPosition = scrollPosition + TopCategories; 
        $('.carousel-inner-top-categories').animate({scrollLeft: scrollPosition},600); 
    } 
}); 
$('.carousel-control-top-categories-prev').on('click', function(){
    if(scrollPosition > 0){ 
        console.log('prev'); 
        scrollPosition = scrollPosition - TopCategories; 
        $('.carousel-inner-top-categories').animate({scrollLeft: scrollPosition},600); 
    } 
}); 


// For You
var carouselWidthForYou = $('.carousel-inner-for-you')[0].scrollWidth; 
var cardWidthForYou = $('.carousel-item-for-you').width(); 

$('.carousel-control-for-you-next').on('click', function(){
    if(scrollPosition < (carouselWidthForYou - (cardWidthForYou * 4))){ 
        console.log('next'); 
        scrollPosition = scrollPosition + cardWidthForYou; 
        $('.carousel-inner-for-you').animate({scrollLeft: scrollPosition},600); 
    } 
}); 
$('.carousel-control-for-you-prev').on('click', function(){
    if(scrollPosition > 0){ 
        console.log('prev'); 
        scrollPosition = scrollPosition - cardWidthForYou; 
        $('.carousel-inner-for-you').animate({scrollLeft: scrollPosition},600); 
    } 
}); 