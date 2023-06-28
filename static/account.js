////////////////////////////////////////////////////////////////////////////////////
// Carousel
////////////////////////////////////////////////////////////////////////////////////
var scrollPosition = 0; 


// Order History
var carouselWidthOrderHistory = $('.carousel-inner-order-history')[0].scrollWidth; 
var cardWidthOrderHistory = $('.carousel-item-order-history').width(); 

$('.carousel-control-order-history-next').on('click', function(){
    if(scrollPosition < (carouselWidthOrderHistory - (cardWidthOrderHistory * 4))){ 
        console.log('next'); 
        scrollPosition = scrollPosition + cardWidthOrderHistory; 
        $('.carousel-inner-order-history').animate({scrollLeft: scrollPosition},600); 
    } 
}); 
$('.carousel-control-order-history-prev').on('click', function(){
    if(scrollPosition > 0){ 
        console.log('prev'); 
        scrollPosition = scrollPosition - cardWidthOrderHistory; 
        $('.carousel-inner-order-history').animate({scrollLeft: scrollPosition},600); 
    } 
}); 

// Wish List
var carouselWidthWishList = $('.carousel-inner-wish-list')[0].scrollWidth; 
var cardWidthWishList = $('.carousel-item-wish-list').width(); 

$('.carousel-control-wish-list-next').on('click', function(){
    if(scrollPosition < (carouselWidthWishList - (cardWidthWishList * 4))){ 
        console.log('next'); 
        scrollPosition = scrollPosition + cardWidthWishList; 
        $('.carousel-inner-wish-list').animate({scrollLeft: scrollPosition},600); 
    } 
}); 
$('.carousel-control-wish-list-prev').on('click', function(){
    if(scrollPosition > 0){ 
        console.log('prev'); 
        scrollPosition = scrollPosition - cardWidthWishList; 
        $('.carousel-inner-wish-list').animate({scrollLeft: scrollPosition},600); 
    } 
}); 