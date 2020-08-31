const urlParams = new URLSearchParams(window.location.search);
const user_id =urlParams.get('user_id');
if (user_id == null){
alert("Please Login")
window.location.replace("D:/profiles/frontend/login.html")
}

function Cart(){
	window.location.replace(`D:/profiles/frontend/cart.html?user_id=${user_id}`)
   }

var todos=fetch("http://127.0.0.1:80/categories");
todos.then(response => response.json())
   .then(json => {
      let ul ='<ul>';
      json.forEach(category => {
          var category_id= category.id;
          ul +='<br><li id="'+category_id+'">'+category.name+ '</a>';
      });
      document.getElementById("categories").innerHTML = ul;
   });
document.getElementsByTagName('ul')[0].addEventListener("click",function(event) {
console.log('id',event.target.id)
var todos=fetch("http://127.0.0.1:80/category/"+event.target.id);
todos.then(response => response.json())
    .then(json=> {
        let li =`<caption>PRODUCTS</caption><tr><th>ID</th><th>NAME</th><th>PRICE</th><th>DESCRIPTION</th><th>CART</th></tr>`;
        json.forEach(data=>{
            li += `<tr>
               <td>${data.id}</td>
               <td>${data.name}</td>
               <td>${data.price}</td>
               <td>${data.description}</td>
               <td><button onclick="addCart(${data.id})">Add to cart</button></td>
            </tr>`;
        });
         document.getElementById('product').innerHTML=li;
    });
});

function addCart(intValue){
	console.log(intValue);
	var pid=intValue
    var data = {
       "product_id":pid
    }
    var todos = fetch(`http://127.0.0.1:80/cart/${user_id}`,{
      method:'POST',
      headers: {
         'Content-Type': 'application/json;charset=utf-8'
      },
      body:JSON.stringify(data)
    });
    todos.then((res)=>{
       res.json()
       .then((data)=>{
            alert(data['ok'])
            console.log(data)
       })
    });
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
