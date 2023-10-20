(function ($) {
"use strict";

// meanmenu
$('#jm-mobile-menu').meanmenu({
	meanMenuContainer: '.jm-mobile-menu',
	meanScreenWidth: "991"
});

$('#mobile-menu-2').meanmenu({
	meanMenuContainer: '.mobile-menu-2',
	meanScreenWidth: "1199"
});

$(window).on('scroll', function () {
	var scroll = $(window).scrollTop();
	if (scroll < 200) {
		$(".header-sticky").removeClass("sticky");
	} else {
		$(".header-sticky").addClass("sticky");
	}
});

//header menu hide show 
$('.dr-navbar-sign').on('click', function() {
	$('.dr-header-menu').slideToggle(300);
	$(this).toggleClass('active');
});

//mobile side menu
$('.side-toggle').on('click', function () {
	$('.side-info').addClass('info-open');
	$('.offcanvas-overlay').addClass('overlay-open');
})

$('.side-info-close,.offcanvas-overlay').on('click', function () {
	$('.side-info').removeClass('info-open');
	$('.offcanvas-overlay').removeClass('overlay-open');
})


//search form
$('.jm-header-action-search').on('click', function () {
	$('.body-overlay').addClass('active');
	$('.jm-search-popup').addClass('active');
})

$('.body-overlay').on('click', function () {
	$('.body-overlay').removeClass('active');
	$('.jm-search-popup').removeClass('active');
})




function sliderActive() {
	/*------------------------------------
	Slider
	--------------------------------------*/
	if (jQuery(".slider-active").length > 0) {
		let sliderActive1 = '.slider-active';
		let sliderInit1 = new Swiper(sliderActive1, {
			// Optional parameters
			slidesPerView: 1,
			rtl: false,
			slidesPerColumn: 1,
			paginationClickable: true,
			loop: true,

			autoplay: {
				delay: 5000,
			},

			// If we need pagination
	        pagination: {
				el: ".cinkes-swiper-pagination",
				clickable: true,
			},

			// Navigation arrows
			navigation: {
				nextEl: '.swiper-button-next',
				prevEl: '.swiper-button-prev',
			},

			a11y: false
		});

		function animated_swiper(selector, init) {
			let animated = function animated() {
				$(selector + ' [data-animation]').each(function () {
					let anim = $(this).data('animation');
					let delay = $(this).data('delay');
					let duration = $(this).data('duration');

					$(this).removeClass('anim' + anim)
						.addClass(anim + ' animated')
						.css({
							webkitAnimationDelay: delay,
							animationDelay: delay,
							webkitAnimationDuration: duration,
							animationDuration: duration
						})
						.one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function () {
							$(this).removeClass(anim + ' animated');
						});
				});
			};
			animated();
			// Make animated when slide change
			init.on('slideChange', function () {
				$(sliderActive1 + ' [data-animation]').removeClass('animated');
			});
			init.on('slideChange', animated);
		}

		animated_swiper(sliderActive1, sliderInit1);
	}}



	// Category active
	const jmCategoryActive = new Swiper(".jm-category-active", {
		slidesPerView: 4,
		spaceBetween: 30,
		autoplay: {
			delay: 5000,
		},
		grabCursor: true,
		loop: true,
		navigation: {
			nextEl: ".jm-category-3-prev",
			prevEl: ".jm-category-3-next",
			},
			breakpoints: {
			0: {
				slidesPerView: 1,
				},
			480: {
				slidesPerView: 2,
			},
			576: {
				slidesPerView: 2,
			},
			768: {
				slidesPerView: 2,
			},
			992: {
				slidesPerView: 3,
			},
			1200: {
				slidesPerView: 4
			}
		}
	});

	// feature job active
	const jmJobActive = new Swiper(".jm-job-active-3", {
		slidesPerView: 4,
		spaceBetween: 30,
		loop: true,
		grabCursor: true,
		autoplay: {
			delay: 5000,
		},
		navigation: {
			nextEl: ".jm-job-3-prev",
			prevEl: ".jm-job-3-next",
			},
			breakpoints: {
			0: {
				slidesPerView: 1,
				},
			576: {
				slidesPerView: 1,
			},
			768: {
				slidesPerView: 2,
			},
			992: {
				slidesPerView: 3,
			},
			1200: {
				slidesPerView: 3,
			},
			1400: {
				slidesPerView: 4,
			}
		}
	});
	
	// brand active 1 
	const jmBrandActive = new Swiper(".jm-brand-active", {
		slidesPerView: 5,
		spaceBetween: 30,
		loop: true,
		autoplay: {
			delay: 1000,
		},
		navigation: {
			nextEl: ".sg-portfolio-prev",
			prevEl: ".sg-portfolio-next",
			},
			breakpoints: {
			0: {
				slidesPerView: 1,
				},
			576: {
				slidesPerView: 2,
			},
			768: {
				slidesPerView: 3,
			},
			992: {
				slidesPerView: 4,
			},
			1200: {
				slidesPerView: 5
			}
		}
	});
	// brand active 2 
	const jmBrandActiveTwo = new Swiper(".jm-brand-active-2", {
		slidesPerView: 5,
		spaceBetween: 30,
		loop: true,
		autoplay: {
			delay: 1000,
		},
		navigation: {
			nextEl: ".sg-portfolio-prev",
			prevEl: ".sg-portfolio-next",
			},
			breakpoints: {
			0: {
				slidesPerView: 1,
				},
			576: {
				slidesPerView: 2,
			},
			768: {
				slidesPerView: 3,
			},
			992: {
				slidesPerView: 4,
			},
			1200: {
				slidesPerView: 5
			}
		}
	});

	// brand active 
	const jmBrandActiveThree = new Swiper(".jm-brand-active-3", {
		slidesPerView: 5,
		spaceBetween: 30,
		loop: true,
		autoplay: {
			delay: 4000,
			clickable: true,
		},
		navigation: {
			nextEl: ".sg-portfolio-prev",
			prevEl: ".sg-portfolio-next",
			},
			breakpoints: {
			0: {
				slidesPerView: 2,
				},
			576: {
				slidesPerView: 3,
			},
			768: {
				slidesPerView: 3,
			},
			992: {
				slidesPerView: 4,
			},
			1200: {
				slidesPerView: 5
			}
		}
	});

	// team active 2
	const jmTeamActiveTwo = new Swiper(".jm-team-active-2", {
		slidesPerView: 4,
		spaceBetween: 30,
		loop: true,
		grabCursor: true,
		autoplay: {
			delay: 5000,
		},
		navigation: {
			nextEl: ".jm-team-2-prev",
			prevEl: ".jm-team-2-next",
			},
			breakpoints: {
			0: {
				slidesPerView: 1,
				},
			576: {
				slidesPerView: 2,
			},
			768: {
				slidesPerView: 2,
			},
			992: {
				slidesPerView: 3,
			},
			1200: {
				slidesPerView: 4
			}
		}
	});
	// team active 3
	const jmTeamActiveThree = new Swiper(".jm-team-active-3", {
		slidesPerView: 4,
		spaceBetween: 30,
		loop: true,
		grabCursor: true,
		autoplay: {
			delay: 5000,
		},
		navigation: {
			nextEl: ".jm-team-3-prev",
			prevEl: ".jm-team-3-next",
			},
			breakpoints: {
			0: {
				slidesPerView: 1,
				},
			576: {
				slidesPerView: 1,
			},
			768: {
				slidesPerView: 2,
			},
			992: {
				slidesPerView: 3,
			},
			1200: {
				slidesPerView: 3,
			},
			1400: {
				slidesPerView: 4,
			}
		}
	});

	// blog active 2
	const jmBlogActiveTwo = new Swiper(".jm-blog-active-2", {
		slidesPerView: 3,
		spaceBetween: 30,
		loop: true,
		autoplay: {
			delay: 5000,
		},
		navigation: {
			nextEl: ".jm-blog-2-prev",
			prevEl: ".jm-blog-2-next",
			},
			breakpoints: {
			0: {
				slidesPerView: 2,
				},
			576: {
				slidesPerView: 3,
			},
			768: {
				slidesPerView: 3,
			},
			992: {
				slidesPerView: 3,
			},
			1200: {
				slidesPerView: 3
			}
		}
	});

	// blog list active
	const jmBlogListActive = new Swiper(".jm-blog-list-active", {
		slidesPerView: 1,
		spaceBetween: 30,
		loop: true,
		autoplay: {
			delay: 5000,
		},
		navigation: {
			nextEl: '.blog-list-swiper-button-next',
			prevEl: '.blog-list-swiper-button-prev',
		},
			breakpoints: {
			0: {
				slidesPerView: 1,
				},
			576: {
				slidesPerView: 1,
			},
			768: {
				slidesPerView: 1,
			},
			992: {
				slidesPerView: 1,
			},
			1200: {
				slidesPerView: 1
			}
		}
	});


/* magnificPopup img view */
$('.popup-image').magnificPopup({
	type: 'image',
	gallery: {
	  enabled: true
	}
});
/* magnificPopup video view */
$('.popup-video').magnificPopup({
	type: 'iframe'
});
$('select').niceSelect();
// data background
$("[data-background]").each(function(){
	$(this).css("background-image","url("+$(this).attr("data-background") + ") ")
})
// data width
$("[data-width]").each(function(){
	$(this).css("width",$(this).attr("data-width"))
})
// data background color
$("[data-bg-color]").each(function(){
	$(this).css("background-color",$(this).attr("data-bg-color"))
})
//for menu active class
$('.portfolio_nav button').on('click', function(event) {
	$(this).siblings('.active').removeClass('active');
	$(this).addClass('active');
	event.preventDefault();
});

// range slider activation
$(".slider-range-bar").slider({
	range: true,
	min: 0,
	max: 7000,
	values: [1200, 5000],
	slide: function (event, ui) {
		$(".amount").val("$" + ui.values[0] + " - $" + ui.values[1]);
	},
});

$( ".slider-area-range-bar" ).slider({
	range: "min",
	value: 110,
	min: 1,
	max: 700,
	slide: function( event, ui ) {
	  $( ".areaCount" ).val( ui.value + " km" );
	}
  });
  $( "areaCount" ).val( $( ".slider-area-range-bar" ).slider( "value" ) + " km" );



// scrollToTop
$.scrollUp({
	scrollName: 'scrollUp', // Element ID
	topDistance: '300', // Distance from top before showing element (px)
	topSpeed: 300, // Speed back to top (ms)
	animation: 'fade', // Fade, slide, none
	animationInSpeed: 200, // Animation in speed (ms)
	animationOutSpeed: 200, // Animation out speed (ms)
	scrollText: '<i class="icofont icofont-long-arrow-up"></i>', // Text for element
	activeOverlay: false, // Set CSS color to display scrollUp active point, e.g '#00FFFF'
});
// testimonial acitve 1
var testimonialControl = new Swiper(".sg-testimonial-active-control", {
	loop: true,
	spaceBetween: 0,
	slidesPerView: 1,
	freeMode: true,
	autoplay: true,
	watchSlidesProgress: true,
});

var testimonialControlMain = new Swiper(".sg-testimonial-active-main", {
	loop: true,
	spaceBetween: 0,
	navigation: {
		nextEl: ".sg-testimonial-next",
		prevEl: ".sg-testimonial-prev",
	},
	thumbs: {
		swiper: testimonialControl,
	},
});
// testimonial active 2 
const testimonialActiveTwo = new Swiper(".sg-testimonial-active-2", {
	slidesPerView: 3,
	spaceBetween: 30,
	loop: true,
	centeredSlides: true,
	navigation: {
		nextEl: ".sg-portfolio-prev-2",
		prevEl: ".sg-portfolio-next-2",
		},
		breakpoints: {
		0: {
			slidesPerView: 1,
			centeredSlides: false,
		},
		576: {
			slidesPerView: 1,
			centeredSlides: false,
		},
		768: {
			slidesPerView: 2,
			centeredSlides: false,
		},
		992: {
			slidesPerView: 2,
		},
		1199: {
			slidesPerView: 3
		}
	}
});

// instagram active 2 
const instagramActiveTwo = new Swiper(".instagram-active-2", {
	slidesPerView: 5,
	spaceBetween: 0,
	loop: true,
	centeredSlides: false,
	navigation: {
		nextEl: ".sg-insta-prev-2",
		prevEl: ".sg-insta-next-2",
		},
		breakpoints: {
		0: {
			slidesPerView: 1,
			},
		576: {
			slidesPerView: 1,
		},
		768: {
			slidesPerView: 2,
		},
		992: {
			slidesPerView: 3,
		},
		1199: {
			slidesPerView: 4
		}
	}
});

// team active 
const teamActive = new Swiper(".team-active", {
	slidesPerView: 4,
	spaceBetween: 30,
	loop: true,
	navigation: {
		nextEl: ".sg-portfolio-prev",
		prevEl: ".sg-portfolio-next",
		},
		breakpoints: {
		0: {
			slidesPerView: 1,
			},
		576: {
			slidesPerView: 1,
		},
		768: {
			slidesPerView: 2,
		},
		992: {
			slidesPerView: 3,
		},
		1199: {
			slidesPerView: 4
		}
	}
});


//   odometer
$('.aboutCount').appear(function (e) {
	var odo = $(".aboutCount");
	odo.each(function () {
		var countNumber = $(this).attr("data-count");
		$(this).html(countNumber);
	});
});

//   odometer
$('.mainCounter').appear(function (e) {
	var odo = $(".mainCounter");
	odo.each(function () {
		var countNumber = $(this).attr("data-count");
		$(this).html(countNumber);
	});
});

//   odometer
$('.footerCounter').appear(function (e) {
	var odo = $(".footerCounter");
	odo.each(function () {
		var countNumber = $(this).attr("data-count");
		$(this).html(countNumber);
	});
});
// WOW active
new WOW().init();


})(jQuery);