const loginbox = document.querySelector(".login-box");
const loginlink = document.querySelector(".login-link");
const registerlink = document.querySelector(".register-link");
const btnpop = document.querySelector(".btnpop");
const iconclose = document.querySelector(".icon-close");
const profilebtn = document.querySelector(".profilebtn");

registerlink.addEventListener('click', ()=> {
    loginbox.classList.add('active');
})

loginlink.addEventListener('click', ()=> {
    loginbox.classList.remove('active');
})

btnpop.addEventListener('click', ()=> {
    loginbox.classList.add('active-popup');
})

iconclose.addEventListener('click', ()=> {
    loginbox.classList.remove('active-popup')
})

profilebtn.addEventListener('click', ()=> {
    loginbox.classList.add('active-popup');
})