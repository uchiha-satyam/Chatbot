let auth_token = localStorage.getItem('wolfpackauthtoken')
const userName = localStorage.getItem('wolfpackusername')
const email = localStorage.getItem('wolfpackemail')
const welcomeText2 = document.querySelector('.welcomeText2')
const logoutBtn = document.getElementsByClassName('logoutButton')[0]
const welcomeTextContainer =  document.getElementsByClassName('welcomeTextContainer')[0]


logoutBtn.addEventListener('click', (e)=>{
    e.preventDefault()
    localStorage.removeItem('wolfpackauthtoken')
    localStorage.removeItem('wolfpackusername')
    localStorage.removeItem('wolfpackemail')
    window.location = './login.html'
})


if(!auth_token)
    window.location = './login.html'