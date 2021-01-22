const addToCartButtons = document.querySelectorAll('#addToCart');
var totalCompra = 0;

addToCartButtons.forEach(addToCartButton => {
    addToCartButton.addEventListener('click', addToCartClicked);
});

const comprar = document.querySelector('.boton-carrito');
comprar.addEventListener('click', finalizarCompra);

const shoppingCartItemsContainer = document.querySelector('#contenido_carrito');

function addToCartClicked(event) {
    const button = event.target;
    const item = button.closest('#libro');
    
    const titulo = item.querySelector('#titulo').textContent;
    const precio = item.querySelector('#precio').textContent;
    // console.log(titulo, precio);

    addItemToShoppingCart(titulo, precio);
}

function addItemToShoppingCart(titulo, precio) {
    const elementsTitle = shoppingCartItemsContainer.querySelectorAll('#titulo');
    // console.log('titulo: ', titulo);
    for(let i = 0; i < elementsTitle.length; i++){
        // console.log(elementsTitle[i].innerHTML);
        if(elementsTitle[i].innerHTML == titulo){
            // console.log('entra en: ', elementsTitle[i].innerHTML);
            elementsTitle[i].parentElement.parentElement.parentElement.querySelector('#cantidad').value++;
            updateShoppingCartTotal(precio, 1, 'add');
            return;
        }
    }

    const shoppingCartRow = document.createElement('tr');
    shoppingCartRow.className = "fila-carrito";
    const shoppingCartContent = `
        <tr>
            <td><p><strong id="titulo">${titulo}</strong><p></td>
            <td id="precio"><p> ${precio} <p></td>
            <td><input id="cantidad" style="width: 55px" type="number" value="1"/></td>
            <td><input id="cantidad_anterior" type="hidden" value="1"/></td>
            <td><button class="delete-item-shopping-cart">X</button></td>
        </tr>`;

    shoppingCartRow.innerHTML = shoppingCartContent;
    shoppingCartItemsContainer.append(shoppingCartRow);

    shoppingCartRow.querySelector('.delete-item-shopping-cart').addEventListener('click', removeShoppingCartItem);
    shoppingCartRow.querySelector('#cantidad').addEventListener('change', updateShoppingCartItem);
    updateShoppingCartTotal(precio, 1, 'add');
}

function updateShoppingCartTotal(precio, cantidad, action) {
    const shoppingCartTotal = document.querySelector('#total');
    if(action == 'add')
        totalCompra = totalCompra + parseFloat(precio.replace('$', ''))*cantidad;
    else if(action == 'delete')
        totalCompra = totalCompra - parseFloat(precio.replace('$', ''))*cantidad;

    if(totalCompra <= -0.00)
        totalCompra = 0.00;

    shoppingCartTotal.innerHTML = `<strong>Total: ${totalCompra.toFixed(2)}$</strong>`;
}

function removeShoppingCartItem(event) {
    const buttonClicked = event.target;
    const item = buttonClicked.closest('.fila-carrito');
    const precio = item.querySelector('#precio').textContent; 
    const cantidad = item.querySelector('#cantidad').value;
    item.remove();
    updateShoppingCartTotal(precio, cantidad, 'delete');
}

function updateShoppingCartItem(event) {
    const input = event.target;
    const cantidad = input.value;
    if(cantidad <= 0)
        input.value = 1
    else{
        const item = input.closest('.fila-carrito');
        const cantidad_anterior = item.querySelector('#cantidad_anterior').value;
        const precio = item.querySelector('#precio').textContent;

        if(cantidad - cantidad_anterior > 0)
            updateShoppingCartTotal(precio, 1, 'add');
        else
            updateShoppingCartTotal(precio, 1, 'delete');

        item.querySelector('#cantidad_anterior').value = cantidad;
    }
}

function finalizarCompra() {
    if(totalCompra == 0)
        alert('Su carrito está vacio.');
    else{
        shoppingCartItemsContainer.innerHTML = '';
        document.querySelector('#total').innerHTML = `<strong>Total: 0.00$</strong>`;
        totalCompra = 0;
        alert('Gracias por realizar su compra. Vuelva pronto.');
    }
}


function iniciarMap() {
    var coord = {lat:37.19711450333406 ,lng: -3.6244384999999912};
    var map = new google.maps.Map(document.getElementById('map'),{
      zoom: 14,
      center: coord
    });
    var marker = new google.maps.Marker({
      position: coord,
      map: map
    });
}