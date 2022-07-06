
	function toggle_check(event){

	    var flag_check = event.currentTarget.checked;
        var dash_check = event.currentTarget.previousElementSibling;

        if (event.currentTarget.previousElementSibling != null){
            field = event.currentTarget.previousElementSibling;
        }
        else{
            field = event.currentTarget.parentElement.previousElementSibling;
        }

	    if (flag_check === true){
    		field.type = "text";
    		return
  		 }
  		field.type = "password";
	}


