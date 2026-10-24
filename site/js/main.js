(() => {
  const WA = 'https://wa.me/919101780136';
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.documentElement.classList.add('js');

  /* Nav: hairline on scroll + mobile menu */
  const header = document.querySelector('.site-header');
  const toggle = document.querySelector('.nav__toggle');
  const menu = document.getElementById('nav-menu');

  const setMenu = (open) => {
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    menu.classList.toggle('is-open', open);
  };
  toggle.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
  menu.addEventListener('click', (e) => { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setMenu(false); });

  /* Scroll: header hairline */
  let ticking = false;
  const onScroll = () => {
    header.classList.toggle('is-scrolled', window.scrollY > 8);
    ticking = false;
  };
  window.addEventListener('scroll', () => {
    if (!ticking) { requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  onScroll();

  /* Product cards: Buy Now links + demo cart */
  const countEl = document.querySelector('[data-cart-count]');
  const cartEl = document.querySelector('.cart');
  const toast = document.querySelector('.toast');
  let count = 0;
  let toastTimer;

  document.querySelectorAll('.card').forEach((card) => {
    const name = card.dataset.name;
    const what = card.dataset.kind === 'stem' ? `${name} stems` : `${name} bouquet`;
    card.querySelector('[data-buy]').href = `${WA}?text=${encodeURIComponent(`Hi! I'd like to order the ${what}.`)}`;
    card.querySelector('[data-add]').addEventListener('click', () => {
      count += 1;
      countEl.textContent = count;
      cartEl.setAttribute('aria-label', `Cart items: ${count}`);
      countEl.classList.remove('is-pop');
      void countEl.offsetWidth;
      countEl.classList.add('is-pop');
      toast.textContent = `Added ${name}`;
      toast.classList.add('is-visible');
      clearTimeout(toastTimer);
      toastTimer = setTimeout(() => toast.classList.remove('is-visible'), 2200);
    });
  });

  document.querySelectorAll('[data-placeholder]').forEach((a) => a.addEventListener('click', (e) => e.preventDefault()));

  /* Scroll reveal */
  document.querySelectorAll('.cards').forEach((grid) => {
    grid.querySelectorAll('.reveal').forEach((el, i) => el.style.setProperty('--delay', `${i * 70}ms`));
  });
  const reveals = document.querySelectorAll('.reveal');
  if (reduceMotion || !('IntersectionObserver' in window)) {
    reveals.forEach((el) => el.classList.add('is-visible'));
  } else {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target);
      });
    }, { threshold: 0.15 });
    reveals.forEach((el) => io.observe(el));
  }

  /* Testimonials coverflow */
  const carousel = document.querySelector('.carousel');
  const track = carousel.querySelector('.carousel__track');
  const slides = [...track.children];
  const mobile = window.matchMedia('(max-width: 767px)');
  let active = 0;
  let timer;

  const render = () => {
    const n = slides.length;
    slides.forEach((slide, i) => {
      let pos = (i - active + n) % n;
      if (pos > n / 2) pos -= n;
      slide.dataset.pos = Math.abs(pos) <= 2 ? String(pos) : 'hidden';
      slide.setAttribute('aria-hidden', String(pos !== 0 && !mobile.matches));
    });
  };

  const go = (dir) => {
    if (mobile.matches) {
      const w = slides[0].getBoundingClientRect().width;
      const atEnd = track.scrollLeft + track.clientWidth >= track.scrollWidth - 4;
      const left = dir > 0 && atEnd ? -track.scrollLeft : dir * w;
      track.scrollBy({ left, behavior: reduceMotion ? 'auto' : 'smooth' });
      return;
    }
    active = (active + dir + slides.length) % slides.length;
    render();
  };

  const stop = () => clearInterval(timer);
  const start = () => {
    stop();
    if (!reduceMotion) timer = setInterval(() => go(1), 5000);
  };

  carousel.querySelector('[data-prev]').addEventListener('click', () => go(-1));
  carousel.querySelector('[data-next]').addEventListener('click', () => go(1));
  carousel.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') { e.preventDefault(); go(-1); }
    if (e.key === 'ArrowRight') { e.preventDefault(); go(1); }
  });
  carousel.addEventListener('mouseenter', stop);
  carousel.addEventListener('mouseleave', start);
  carousel.addEventListener('focusin', stop);
  carousel.addEventListener('focusout', (e) => { if (!carousel.contains(e.relatedTarget)) start(); });

  // Swipe on touch (desktop/tablet coverflow; mobile uses native scroll-snap)
  let startX = null;
  track.addEventListener('touchstart', (e) => { startX = e.touches[0].clientX; stop(); }, { passive: true });
  track.addEventListener('touchend', (e) => {
    if (startX !== null && !mobile.matches) {
      const dx = e.changedTouches[0].clientX - startX;
      if (Math.abs(dx) > 40) go(dx < 0 ? 1 : -1);
    }
    startX = null;
    start();
  });
  // Click a side card to bring it to the centre
  slides.forEach((slide, i) => slide.addEventListener('click', () => {
    if (!mobile.matches && i !== active) { active = i; render(); }
  }));

  mobile.addEventListener('change', render);
  render();
  start();
})();
