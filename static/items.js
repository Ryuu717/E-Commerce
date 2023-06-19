////////////////////////////////////////////////////////////////////////////////////
// Carousel
////////////////////////////////////////////////////////////////////////////////////
// const multipleItemCarousel = document.querySelector('#carousel-top-categories'); 
// const carousel = new bootstrap.Carousel(multipleItemCarousel, {
//     interval: false
// })

var scrollPosition = 0; 


// Related Items
var carouselWidthRelatedItems = $('.carousel-inner-related-items')[0].scrollWidth; 
var RelatedItems = $('.carousel-item-related-items').width(); 

$('.carousel-control-related-items-next').on('click', function(){
    if(scrollPosition < (carouselWidthRelatedItems - (RelatedItems * 4))){ 
        console.log('next'); 
        scrollPosition = scrollPosition + RelatedItems; 
        $('.carousel-inner-related-items').animate({scrollLeft: scrollPosition},600); 
    } 
}); 
$('.carousel-control-related-items-prev').on('click', function(){
    if(scrollPosition > 0){ 
        console.log('prev'); 
        scrollPosition = scrollPosition - RelatedItems; 
        $('.carousel-inner-related-items').animate({scrollLeft: scrollPosition},600); 
    } 
}); 


// Customers Search
var carouselWidthCustomersSearch = $('.carousel-inner-customers-search')[0].scrollWidth;
var cardWidthCustomersSearch = $('.carousel-item-customers-search').width();

$('.carousel-control-customers-search-next').on('click', function(){
    if(scrollPosition < (carouselWidthCustomersSearch - (cardWidthCustomersSearch * 4))){
        console.log('next');
        scrollPosition = scrollPosition + cardWidthCustomersSearch;
        $('.carousel-inner-customers-search').animate({scrollLeft: scrollPosition},600);
    }
});
$('.carousel-control-customers-search-prev').on('click', function(){
    if(scrollPosition > 0){
        console.log('prev');
        scrollPosition = scrollPosition - cardWidthCustomersSearch;
        $('.carousel-inner-customers-search').animate({scrollLeft: scrollPosition},600);
    }
}); 