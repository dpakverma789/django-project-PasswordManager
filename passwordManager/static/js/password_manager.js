
    function visibility()
	{
  		var password = document.getElementsByClassName("pass")[0];
  		if (password.type === "password")
  		 {
    		password.type = "text";
  		 }
  		else
  		 {
    		password.type = "password";
  		 }

	}

	function copy(event)
    {
      selector = event.currentTarget.previousElementSibling;
	  var copyText = document.getElementsByClassName(selector.className)[0];
	  copyText.select();
	  copyText.setSelectionRange(0, 99999);
	  document.execCommand("copy");
	  event.currentTarget.nextElementSibling.innerHTML = "Copied!";
	}

