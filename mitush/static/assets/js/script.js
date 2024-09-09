
    /**
     * Preloader
     */
    const preloader = document.querySelector('#preloader');
    if (preloader) {
      window.addEventListener('load', () => {
        preloader.remove();
      });
    }
  
    /**
     * Scroll top button
     */
    let scrollTop = document.querySelector('.scroll-top');
  
    function toggleScrollTop() {
      if (scrollTop) {
        window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
      }
    }
    scrollTop.addEventListener('click', (e) => {
      e.preventDefault();
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  
    window.addEventListener('load', toggleScrollTop);
    document.addEventListener('scroll', toggleScrollTop);
  
    /**
     * Animation on scroll function and init
     */
    function aosInit() {
      AOS.init({
        duration: 600,
        easing: 'ease-in-out',
        once: true,
        mirror: false
      });
    }
    window.addEventListener('load', aosInit);
  
    /**
     * Initiate glightbox
     */
    const glightbox = GLightbox({
      selector: '.glightbox'
    });
  
    /**
     * Init swiper sliders
     */
    function initSwiper() {
      document.querySelectorAll(".init-swiper").forEach(function(swiperElement) {
        let config = JSON.parse(
          swiperElement.querySelector(".swiper-config").innerHTML.trim()
        );
  
        if (swiperElement.classList.contains("swiper-tab")) {
          initSwiperWithCustomPagination(swiperElement, config);
        } else {
          new Swiper(swiperElement, config);
        }
      });
    }
  
    window.addEventListener("load", initSwiper);
  
    /**
     * Initiate Pure Counter
     */
    new PureCounter();
  
    /**
     * Init isotope layout and filters
     */
    document.querySelectorAll('.isotope-layout').forEach(function(isotopeItem) {
      let layout = isotopeItem.getAttribute('data-layout') ?? 'masonry';
      let filter = isotopeItem.getAttribute('data-default-filter') ?? '*';
      let sort = isotopeItem.getAttribute('data-sort') ?? 'original-order';
  
      let initIsotope;
      imagesLoaded(isotopeItem.querySelector('.isotope-container'), function() {
        initIsotope = new Isotope(isotopeItem.querySelector('.isotope-container'), {
          itemSelector: '.isotope-item',
          layoutMode: layout,
          filter: filter,
          sortBy: sort
        });
      });
  
      isotopeItem.querySelectorAll('.isotope-filters li').forEach(function(filters) {
        filters.addEventListener('click', function() {
          isotopeItem.querySelector('.isotope-filters .filter-active').classList.remove('filter-active');
          this.classList.add('filter-active');
          initIsotope.arrange({
            filter: this.getAttribute('data-filter')
          });
          if (typeof aosInit === 'function') {
            aosInit();
          }
        }, false);
      });
  
    });
  
  
    /**
     * Correct scrolling position upon page load for URLs containing hash links.
     */
    window.addEventListener('load', function(e) {
      if (window.location.hash) {
        if (document.querySelector(window.location.hash)) {
          setTimeout(() => {
            let section = document.querySelector(window.location.hash);
            let scrollMarginTop = getComputedStyle(section).scrollMarginTop;
            window.scrollTo({
              top: section.offsetTop - parseInt(scrollMarginTop),
              behavior: 'smooth'
            });
          }, 100);
        }
      }
    });
  
  
//Login Functionalities

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {


  // Function to handle checkout page functionalities
  function handleCheckout() {
      const deliveryOptions = document.querySelectorAll('input[name="delivery"]');
      const shippingFeeElement = document.querySelector('.shipping-fee');
      const grandTotalElement = document.querySelector('.grand-total-amount');
      const subtotalElement = document.querySelector('.subtotal-amount');
      const payButton = document.querySelector('.pay-button');
      const subtotal = parseFloat(subtotalElement.textContent.replace('Ksh ', ''));

      function updateTotals(shippingFee) {
          shippingFeeElement.textContent = `Ksh ${shippingFee}`;
          const grandTotal = subtotal + shippingFee;
          grandTotalElement.textContent = `Ksh ${grandTotal}`;
          payButton.textContent = `Pay Ksh ${grandTotal}`;
      }

      // Set initial shipping fee and grand total based on default selected option
      const initialShippingFee = document.querySelector('input[name="delivery"]:checked').value === 'pickup-star-mall' ? 0 :
                                 document.querySelector('input[name="delivery"]:checked').value === 'pickup-mtaani' ? 150 : 350;
      updateTotals(initialShippingFee);

      deliveryOptions.forEach(option => {
          option.addEventListener('change', function() {
              let shippingFee = 0;
              if (this.value === 'pickup-mtaani') {
                  shippingFee = 150;
              } else if (this.value === 'nationwide') {
                  shippingFee = 350;
              }
              updateTotals(shippingFee);
          });
      });
  }

  // Function to get CSRF token
  function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
              const cookie = cookies[i].trim();
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }

  // Initialize all functions
  addToCart();
  handleQuantityChanges();
  removeFromCart();
  handleCheckout();
});
