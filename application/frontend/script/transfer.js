const backEndUrl = "http://localhost:3000"
const logoutBtn = document.getElementsByClassName('logoutButton')[0]
let auth_token = localStorage.getItem('wolfpackauthtoken')
const userName = localStorage.getItem('wolfpackusername')
const email = localStorage.getItem('wolfpackemail')
const transferForm= document.querySelector('form.transfer')
let transferSubmit = document.querySelector('#formSubmit')
let statusReporter = document.querySelector('.statusReporter')

if(!auth_token)
    window.location='./login.html'

logoutBtn.addEventListener('click', (e)=>{
    e.preventDefault()
    localStorage.removeItem('wolfpackauthtoken')
    localStorage.removeItem('wolfpackusername')
    localStorage.removeItem('wolfpackemail')
    window.location = './login.html'
})

const setStatus = async (status, msg) =>{
    statusReporter.innerHTML = msg
    statusReporter.style.color = (status=='error'?"#ff3636": "#31f351")
    setTimeout(()=>{
        statusReporter.innerHTML = ""
    }, 3500)
}

const transferFunction = async (email, amount) =>{
    const data={
        toEmail: email,
        amount: amount
    }
    const options={ //configure req
        method: 'POST',
        headers:{
            "Content-Type": "application/json",
            'auth-token': auth_token
        },
        body: JSON.stringify(data)
    }

    const response = await fetch(backEndUrl+"/api/transactions/transfer", options)
    const res= await response.json()
   console.log(res)
        if(!(res.err)){
            setStatus('success', 'Transaction Successful')
            console.log(statusReporter)
        }
        else{
            if(res.err)
                setStatus("error", res.err)
            else
                setStatus( "error", "Some Unknown Error Occured")
        }
}

transferSubmit.addEventListener('click', async (e)=>{
    e.preventDefault()
    const email = transferForm.toemail.value
    const amount = transferForm.amount.value
    try{
        transferFunction(email, amount)
    } catch(err){
        console.log(err)
    }
})