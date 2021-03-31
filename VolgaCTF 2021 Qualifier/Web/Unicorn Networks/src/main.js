$(function() {
    
    "use strict";
    
    //===== Prealoder
    
    $(window).on('load', function(event) {
        $('.preloader').delay(500).fadeOut(500);
        $('#search-btn').on('click', function() {
            let url = $('#search-input').val();
            fetch('/api/getUrl?url=' + encodeURIComponent(url))
                .then(response => {
                    if (response.status == 200) {
                        return response.json();
                    }
                    throw Error('Server is unavailable');
                },
                failResponse => {
                    showError('Server is unavailable');
                })
                .then(result => {
                    if(result.status == 'ok') {
                        var element = document.createElement('a');
                        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(result.content));
                        element.setAttribute('download', 'page.html');

                        element.style.display = 'none';
                        document.body.appendChild(element);

                        element.click();

                        document.body.removeChild(element);
                        return null;
                    } else {
                        return showError(result.content.message);
                    } 
                },
                errorMsg => {
                    showError(errorMsg);
                });
        });
        // Get the modal
        var modal = document.getElementById("myModal");

        // Get the <span> element that closes the modal
        var span = document.getElementsByClassName("close")[0];

        // When the user clicks anywhere outside of the modal, close it
        window.onclick = function(event) {
          if (event.target == modal) {
            modal.style.display = "none";
          }
        }

        // When the user clicks on <span> (x), close the modal
        span.onclick = function() {
          modal.style.display = "none";
        }
    });

    function showError(errorMsg) {
        let content = `<div class="alert alert-danger" role="alert">Error: ${errorMsg}</div>`;
        showModal(content);
    } 

    function showModal(content) {
        $('#modal-content').html(content);
        // Get the modal
        var modal = document.getElementById("myModal");
        modal.style.display = "block";
    }
    
    
    //===== Sticky
    
    $(window).on('scroll', function(event) {    
        var scroll = $(window).scrollTop();
        if (scroll < 10) {
            $(".navbar-area").removeClass("sticky");
        } else{
            $(".navbar-area").addClass("sticky");
        }
    });
    
     //===== close navbar-collapse when a  clicked
    
    $(".navbar-nav a").on('click', function () {
        $(".navbar-collapse").removeClass("show");
    });
    
    //===== Mobile Menu
    
    $(".navbar-toggler").on('click', function(){
        $(this).toggleClass("active");
    });
    
    $(".navbar-nav a").on('click', function() {
        $(".navbar-toggler").removeClass('active');
    });
    
    
    //===== Section Menu Active

    var scrollLink = $('.page-scroll');
        // Active link switching
        $(window).scroll(function() {
        var scrollbarLocation = $(this).scrollTop();

        scrollLink.each(function() {

          var sectionOffset = $(this.hash).offset().top - 73;

          if ( sectionOffset <= scrollbarLocation ) {
            $(this).parent().addClass('active');
            $(this).parent().siblings().removeClass('active');
          }
        });
    });    
    
    
    //===== Sidebar

    $('[href="#side-menu-right"], .overlay-right').on('click', function (event) {
        $('.sidebar-right, .overlay-right').addClass('open');
    });

    $('[href="#close"], .overlay-right').on('click', function (event) {
        $('.sidebar-right, .overlay-right').removeClass('open');
    });

    
    // Show or hide the sticky footer button
    $(window).on('scroll', function(event) {
        if($(this).scrollTop() > 600){
            $('.back-to-top').fadeIn(200)
        } else{
            $('.back-to-top').fadeOut(200)
        }
    });
});