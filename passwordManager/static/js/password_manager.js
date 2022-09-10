
	function toggle_check(event)
	{
	    let flag_check = event.currentTarget.checked;
        let dash_check = event.currentTarget.previousElementSibling;
        let field = dash_check != null ? dash_check : event.currentTarget.parentElement.previousElementSibling;
        field.type = flag_check === true ? "text" : "password";
	}

	function checkPasswordLength()
	{
	   let password = document.getElementsByClassName('pass');
	   password_length = password[0].value.length;
	   if (password_length > 20){
	        alert('Max 20 character Password is allowed!');
	        return false
	   }
	}