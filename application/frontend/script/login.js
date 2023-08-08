const backEndUrl = "http://localhost:3000"
const loginText = document.querySelector(".title-text .login");
const loginForm = document.querySelector("form.login");
const signupForm = document.querySelector("form.signup");
const loginBtn = document.querySelector("label.login");
const signupBtn = document.querySelector("label.signup");
const loginSubmit = document.getElementById("loginSubmitButton")
const registerSubmit = document.getElementById("registerSubmitButton")
const errorText = document.querySelector('.errortext')
signupBtn.onclick = (()=>{
  loginForm.style.marginLeft = "-50%";
  loginText.style.marginLeft = "-50%";
});
loginBtn.onclick = (()=>{
  loginForm.style.marginLeft = "0%";
  loginText.style.marginLeft = "0%";
});

console.log(loginBtn)

const setErr = async (msg) =>{
    errorText.innerHTML = msg
    setTimeout(()=>{
        errorText.innerHTML = ""
    }, 2000)
}

const signInWithIdPwd = async (email, password) =>{
    const data={
        email: email,
        pwd: password
    }
    const options={ //configure req
        method: 'POST',
        headers:{
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }

    const response = await fetch(backEndUrl+"/api/auth/login", options)
    const res= await response.json()
    const auth_token=res['auth-token']
        if(auth_token){
            //Save the auth token and redirect on the other site
            localStorage.setItem('wolfpackauthtoken', auth_token);
            localStorage.setItem('wolfpackusername', res.name);
            localStorage.setItem('wolfpackemail', email);
            window.location = "./chatbot.html"
        }
        else{
            if(res.err)
                setErr(res.err)
            else
                setErr("Authentication Failed")
        }
}

const signUpWithIdPwd = async (email, name, password) =>{
    const data={
        email: email,
        name: name,
        pwd: password
    }
    const options={ //configure req
        method: 'POST',
        headers:{
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }

    const response = await fetch(backEndUrl+"/api/auth/createuser", options)
    const res= await response.json()
    const auth_token=res['auth-token']
        if(auth_token){
            //Save the auth token and redirect on the other site
            localStorage.setItem('wolfpackauthtoken', auth_token);
            localStorage.setItem('wolfpackusername', res.name);
            localStorage.setItem('wolfpackemail', email);
            window.location = "./chatbot.html"
        }
        else{
            if(res.err)
                setErr(res.err)
            else
                setErr("Authentication Failed")
        }
}

loginSubmit.addEventListener('click', async (e)=>{
    e.preventDefault()
    const email = loginForm.email.value
    const pwd = loginForm.password.value
    try{
        signInWithIdPwd(email, pwd)
    } catch(err){
        console.log(err)
    }
})

registerSubmit.addEventListener('click', async (e)=>{
    e.preventDefault()
    const email = signupForm.email.value, pwd = signupForm.password.value, confpwd = signupForm.confirmpass.value, name = signupForm.name.value 
    if(confpwd !== pwd){
        setErr("Passwords don't match")
        throw new Error("Passwords don't match")
    }
    try{
        signUpWithIdPwd(email, name, pwd)
    } catch(err){
        console.log(err)
    }
})