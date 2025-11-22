function openRegisterPage(){
    window.location.href= "register.html"
}

function logOut(){
	fetch("/auth/logout").then(
		response=>{
			window.location.href="/auth/login"
		})
}
