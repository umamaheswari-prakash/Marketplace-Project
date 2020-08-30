function afterlogin() {
		var user_name=document.getElementById("Uname").value;
		var password=document.getElementById("pass").value;
		const data={
		    "user_name":user_name,
		    "password":password
		    }
	    console.log('ok',data)
        var todos = fetch(`http://127.0.0.1:80/login`,{
            method: 'Post',
            headers: {
               'Content-Type': 'application/json',
            },
            body:JSON.stringify(data)
        });
        todos.then((response) => response.json())
            .then((data) => {
              console.log('Success:', data);
              if(data['ok']=="200")
               window.location.replace(`D:/profiles/frontend/categories.html?user_id=${data['user_id']}`)
               else{
                alert('Incorrect username/password')
               }
            })
	}