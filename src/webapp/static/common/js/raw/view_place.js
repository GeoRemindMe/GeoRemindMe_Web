$(document).ready(function(){
    //Set like & dislike, remember and removable behaviour
    GRM.init()
    
    //Set like&dislike style
    $('.suggestion-element').hover(
        function(){$(this).find('.like-dislike').show()},
        function(){$(this).find('.like-dislike').hide()}
    )
    loadPanoramioPhotos(latlngStr);
});
