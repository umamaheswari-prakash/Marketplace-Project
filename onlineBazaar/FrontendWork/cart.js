const urlParams = new URLSearchParams(window.location.search);
const user_id =urlParams.get('user_id');
if (user_id == null){
alert("Please Login!")
window.location.replace("D:/profiles/frontend/login.html")
}


var todos=fetch(`http://127.0.0.1:80/cart/${user_id}`);
    todos.then(response => response.json())
      .then(value=> {
       console.log("ok",value)
       let li = `<tr><th>id</th><th>Name</th><th>seller_name</th><th>price</th><th>quantity</th><th>cart</th></tr>`;
          value.forEach(data=>{
		  console.log(data.Quantity)
          li += `<tr>
             <td>${data.id}</td>
             <td>${data.Product}</td>
			 <td>${data.Seller}</td>
             <td>${data.Price}</td>
             <td><button onclick="updatemin(${data.id},${data.Quantity})">-</button>${data.Quantity}<button onclick="updateplus(${data.id},${data.Quantity})">+</button></td>
             <td><button onclick="remove(${data.id})">remove</button></td>
          </tr>`;
      });
      document.getElementById('product').innerHTML=li;
  });
  function remove(proid){
	var id=proid
    var value={
       "product_id":id
    }
    console.log(value)
    var todos = fetch(`http://127.0.0.1:80/cart/${user_id}`,{
       method:'DELETE',
       headers: {
        'Content-Type': 'application/json;charset=utf-8'
       },
       body:JSON.stringify(value)
    });
    todos.then((res)=>{
      res.json()
      .then((data)=>{
        alert(data['ok'])
      })
    })
   }

function updatemin(pid,qnty){
	var id=pid
    var quantity =qnty
    var val=quantity-1
    var cred={
       'product_id':id,
       'quantity':val
    }
    console.log(cred)
    var todos = fetch(`http://127.0.0.1:80/cart/${user_id}`,{
        method:'PUT',
        headers: {
           'Content-Type': 'application/json;charset=utf-8'
        },
        body:JSON.stringify(cred)
    });
    todos.then((res)=>{
       res.json()
       .then((data)=>{
         alert(data['ok'])
         console.log(data)
       })
    })
}
function updateplus(ids,qnty){
	var id=ids
    var quantity =qnty
    var val=quantity+1
    var cred={
       'product_id':id,
       'quantity':val
    }
    console.log(cred)
    var todos = fetch(`http://127.0.0.1:80/cart/${user_id}`,{
        method:'PUT',
        headers: {
           'Content-Type': 'application/json;charset=utf-8'
        },
        body:JSON.stringify(cred)
    });
    todos.then((res)=>{
       res.json()
       .then((data)=>{
          alert(data['ok'])
          console.log(data)
       })
    })
}
function home(){
	window.location.replace(`D:/profiles/frontend/categories.html?user_id=${user_id}`)
   }
function logout(){
	var todos=fetch(`http://127.0.0.1:80/logout/${user_id}`,{
		method:'post'
    });
    todos.then((res)=>{
       res.json()
       .then((data)=>{
            alert(data['ok'])
			window.location.replace("D:/profiles/frontend/login.html")
       })
    });
}

