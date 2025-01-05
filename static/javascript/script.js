const switch_btn_navbar = document.querySelector(".switch");
const mobile_menu_toggle = document.querySelector('.mobile-menu-toggle');
const sidebar = document.querySelector('.mobile-menu')
const scrollToTopBtn = document.querySelector('.scroll-to-top');
window.addEventListener("DOMContentLoaded", function () {
  const loader = this.document.querySelector('.loader-container');
  setTimeout(() => {
    loader.classList.add('hidden');
  }, 1000)

  if (localStorage.getItem("theme") == "dark") {
    document.body.classList.add("dark");
  } else {
    document.body.classList.remove("dark");
  }
});

function btn_click() {
  document.body.classList.toggle("dark");
  const currentTheme = document.body.classList.contains("dark")
    ? "dark"
    : "light";
  localStorage.setItem("theme", currentTheme);
}

switch_btn_navbar.addEventListener("click", () => {
  btn_click();
});

mobile_menu_toggle.addEventListener('click', () => {
  document.querySelector('.mobile-menu').classList.toggle('show')
})

document.addEventListener('click', (event) => {
  if (!sidebar.contains(event.target) && event.target !== mobile_menu_toggle) {
    sidebar.classList.remove('show');
}
})


let currentIndex = 0;
const slides = document.querySelectorAll('.slider img');
const totalSlides = slides.length;

function moveSlide(direction) {
  currentIndex += direction;

  if (currentIndex < 0) {
    currentIndex = totalSlides - 1;
  } else if (currentIndex >= totalSlides) {
    currentIndex = 0;
  }

  document.querySelector('.slider').style.transform = `translateX(-${currentIndex * 100}%)`;
}

setInterval(() => {
  moveSlide(1);
}, 4000); 

window.onscroll = function() {
  if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
    scrollToTopBtn.classList.add('show'); 
  } else {
    scrollToTopBtn.classList.remove('show');
  }
};
scrollToTopBtn.addEventListener('click', function() {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
});

function changeProfileImage(event) {
  const file = event.target.files[0]; 
  if (file) {
      const reader = new FileReader();

      reader.onload = function(e) {
          const imageUrl = e.target.result; 
          const profileImage = document.getElementById('profile-img');
          profileImage.src = imageUrl; 
      };

      reader.readAsDataURL(file); 
  }
}