const closeBtn = document.querySelector('.close-btn');
const cookieNotice = document.querySelector('.cookie-footer');

closeBtn.addEventListener('click', function() {
  cookieNotice.style.display = 'none';
});
