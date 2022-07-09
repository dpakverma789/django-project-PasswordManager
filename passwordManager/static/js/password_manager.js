	function toggle_check(event)
	{
	    let flag_check = event.currentTarget.checked;
        let dash_check = event.currentTarget.previousElementSibling;
        let field = dash_check != null ? dash_check : event.currentTarget.parentElement.previousElementSibling;
        field.type = flag_check === true ? "text" : "password";
	}