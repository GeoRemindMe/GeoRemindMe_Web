var $lastActiveAnchor;
   var $firstAnchorOffset;
   $(document).ready(function(){
      
      $postContentIndex=185;
      
      //$firstAnchorOffset=$($('a.anchor:first').attr('href')).offset().top;
      $firstAnchorOffset=180;
      
      /* This function and the behaviour to the anchor links at the content-index */
      $('a.anchor').click( function(event){
         event.preventDefault();
         var targetOffset = $($(this).attr('href')).offset().top;
         $('html,body').animate({scrollTop: targetOffset}, 'slow');
         
         //Change the color
         $($lastActiveAnchor).removeClass('activeAnchor');
         $('#back-to-top').removeClass('activeAnchor');
         $(this).addClass('activeAnchor');
         $($($lastActiveAnchor).attr('href')).children().removeClass('activeArticle');
         $($(this).attr('href')).children().addClass('activeArticle');
         
         $lastActiveAnchor=this;
         
         return false;
         
      });
      
      $('a.back-to-top').click( function(event){
            event.preventDefault();
            $('#content-index').animate( { top: "185px" }, "fast");
            $('html,body').animate({scrollTop: 0}, 'fast');
            
            $($lastActiveAnchor).removeClass('activeAnchor');
            $('#back-to-top').addClass('activeAnchor');
            return false;
         });

      $(function() {
         
         //$('a.lightbox').lightBox(); // Select all links with lightbox class
         
      });
   
      $(window).scroll(function(){
            if($(window).scrollTop()>$firstAnchorOffset){
              $('#content-index').css('position','fixed');
              $('#content-index').css('top','0');
            }else{
               $('#content-index').css('position','absolute');
               $('#content-index').css('top',$firstAnchorOffset);
            }
      });
      
      //This checks if you enter to the page to a #
      link = window.location.href;
      equalPosition = jQuery.inArray('#',link); //Get the position of '='
      
      if(equalPosition>-1){
        //Yes, the page have been just loaded and its pointing to an anchor     
        anchor = link.substring(equalPosition + 1, link.length); //Split the string and get the anchor.
         $('#'+anchor).children().addClass('activeArticle');
         $('#content-index').css('position','fixed');
         $('#content-index').css('top','0');        
      }else{
         $('#content-index').css('position','absolute');
         $('#content-index').css('top',$firstAnchorOffset);
      }
   
   });
