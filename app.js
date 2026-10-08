const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#primary-nav');
const installButton = document.querySelector('#install-app');
const installNote = document.querySelector('#install-note');
let deferredInstallPrompt = null;

document.querySelector('#year')?.replaceChildren(String(new Date().getFullYear()));

const revealSections = [...document.querySelectorAll('main > section')];
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

document.documentElement.classList.add('js');
revealSections.forEach((section) => section.classList.add('reveal-section'));

if (reduceMotion || !('IntersectionObserver' in window)) {
  revealSections.forEach((section) => section.classList.add('is-visible'));
} else {
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -10% 0px' });

  revealSections.forEach((section) => revealObserver.observe(section));
}

menuButton?.addEventListener('click', () => {
  const open = navigation.classList.toggle('open');
  menuButton.setAttribute('aria-expanded', String(open));
});

navigation?.addEventListener('click', (event) => {
  if (event.target.closest('a')) {
    navigation.classList.remove('open');
    menuButton?.setAttribute('aria-expanded', 'false');
  }
});

window.addEventListener('beforeinstallprompt', (event) => {
  event.preventDefault();
  deferredInstallPrompt = event;
  installButton.hidden = false;
});

installButton?.addEventListener('click', async () => {
  if (deferredInstallPrompt) {
    deferredInstallPrompt.prompt();
    await deferredInstallPrompt.userChoice;
    deferredInstallPrompt = null;
    installButton.hidden = true;
    return;
  }

  const isiOS = /iphone|ipad|ipod/i.test(navigator.userAgent);
  installNote.textContent = isiOS
    ? 'On iPhone or iPad, open Share and choose Add to Home Screen.'
    : 'Use your browser menu and choose Install app or Add to Home Screen.';
});

if (/iphone|ipad|ipod/i.test(navigator.userAgent) && !window.navigator.standalone) {
  installButton.hidden = false;
}

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => navigator.serviceWorker.register('/sw.js'));
}
