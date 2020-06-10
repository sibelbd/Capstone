(function($) {
  "use strict"; // Start of use strict

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 70)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

  // Scroll to top button appear
  $(document).scroll(function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function() {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 80
  });

  // Collapse Navbar
  var navbarCollapse = function() {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-shrink");
    } else {
      $("#mainNav").removeClass("navbar-shrink");
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

  // Floating label headings for the contact form
  $(function() {
    $("body").on("input propertychange", ".floating-label-form-group", function(e) {
      $(this).toggleClass("floating-label-form-group-with-value", !!$(e.target).val());
    }).on("focus", ".floating-label-form-group", function() {
      $(this).addClass("floating-label-form-group-with-focus");
    }).on("blur", ".floating-label-form-group", function() {
      $(this).removeClass("floating-label-form-group-with-focus");
    });
  });
    
  $(function(){
        let chart = document.querySelector('canvas').chart;
    
        $(document).on('click', function(){

            // When the document is clicked, update the chart 
            // with a random value and animate it.

            chart.data.datasets[0].data[2] = Math.random()*10000;
            chart.update();
        });
  });
  //Chart updating info

  $(function(){

      let chart = document.querySelector('canvas').chart;

      $(submit-button-regions).on('click', function(){

          // When the document is clicked, update the chart
          // with a random value and animate it.

          chart.data.datasets[0].data[2] = Math.random()*10000;
          chart.update();
      });

  });

  $(document).ready(function(){
    // $.ajax({
    // type: "POST",
    // url: "/_get_all_regions",
    // data: "{}",
    // contentType: "application/json; charset=utf-8",
    // dataType: "json",
    //     success: function(msg) {
    //         $("#region-dropdown-regions-1").get(0).options.length = 0;
    //         $("#region-dropdown-regions-1").get(0).options[0] = new Option("Select Region", "-1");
    //
    //         $.each(msg.d, function(index, item) {
    //             $("#region-dropdown-regions-1").get(0).options[$("#region-dropdown-regions-1").get(0).options.length]
    //                   = new Option(item.Display, item.Value);
    //         });
    //     },
    //     error: function() {
    //         alert("Failed to load regions");
    //     }
  // var myOptions = {
  //     val1 : 'text1',
  //     val2 : 'text2'
  // };
  // $.each(myOptions, function(val, text) {
  //     $('#mySelect').append( new Option(text,val) );
  // });
    console.log("ready!")

    });
 
})(jQuery); // End of use strict

