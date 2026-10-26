(function () {
  var d = document;
  // menu mobile
  var btn = d.querySelector('.menu-btn');
  if (btn) {
    btn.addEventListener('click', function () {
      var open = d.body.classList.toggle('menu-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
  // ombre du header au scroll
  var header = d.querySelector('.site-header');
  function onScroll() {
    if (header) header.classList.toggle('scrolled', window.scrollY > 10);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  // apparition des blocs au scroll
  var items = d.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('in');
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }
  // léger parallaxe sur la photo du hero
  var arch = d.querySelector('.arch');
  if (arch && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    window.addEventListener('scroll', function () {
      var y = Math.min(window.scrollY, 600);
      arch.style.translate = '0 ' + (y * 0.06) + 'px';
    }, { passive: true });
  }
})();

// lightbox : cliquer sur une photo pour l'agrandir
(function () {
  var d = document;
  var box = d.createElement('div');
  box.className = 'lightbox';
  box.innerHTML = '<img alt="">';
  d.body.appendChild(box);
  var big = box.querySelector('img');
  d.addEventListener('click', function (ev) {
    var img = ev.target.closest('.gallery img, .strip img');
    if (img) {
      big.src = img.getAttribute('data-full') || img.src;
      big.alt = img.alt;
      box.classList.add('open');
    } else if (box.classList.contains('open')) {
      box.classList.remove('open');
    }
  });
  d.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape') box.classList.remove('open');
  });
})();
