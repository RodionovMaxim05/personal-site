/**
 * Template Name: MyResume
 * Template URL:
 * https://bootstrapmade.com/free-html-bootstrap-template-my-resume/ Updated:
 * Jun 29 2024 with Bootstrap v5.3.3 Author: BootstrapMade.com License:
 * https://bootstrapmade.com/license/
 */

(function() {
'use strict';

/**
 * Header toggle
 */
const headerToggleBtn = document.querySelector('.header-toggle');

function headerToggle() {
  document.querySelector('#header').classList.toggle('header-show');
  headerToggleBtn.classList.toggle('bi-list');
  headerToggleBtn.classList.toggle('bi-x');
}
headerToggleBtn.addEventListener('click', headerToggle);

/**
 * Hide mobile nav on same-page/hash links
 */
document.querySelectorAll('#navmenu a').forEach(navmenu => {
  navmenu.addEventListener('click', () => {
    if (document.querySelector('.header-show')) {
      headerToggle();
    }
  });
});

/**
 * Toggle mobile nav dropdowns
 */
document.querySelectorAll('.navmenu .toggle-dropdown').forEach(navmenu => {
  navmenu.addEventListener('click', function(e) {
    e.preventDefault();
    this.parentNode.classList.toggle('active');
    this.parentNode.nextElementSibling.classList.toggle('dropdown-active');
    e.stopImmediatePropagation();
  });
});

/**
 * Scroll top button
 */
let scrollTop = document.querySelector('.scroll-top');

function toggleScrollTop() {
  if (scrollTop) {
    window.scrollY > 100 ? scrollTop.classList.add('active') :
                           scrollTop.classList.remove('active');
  }
}
scrollTop.addEventListener('click', (e) => {
  e.preventDefault();
  window.scrollTo({top: 0, behavior: 'smooth'});
});

window.addEventListener('load', toggleScrollTop);
document.addEventListener('scroll', toggleScrollTop);
})();
