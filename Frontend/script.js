let cart = [];
let total = 0;

function addToCart(productName, productPrice) {
    cart.push({ name: productName, price: productPrice });
    total += productPrice;
    updateCart();
}

function updateCart() {
    const cartItems = document.getElementById('cart-items');
    cartItems.innerHTML = '';
    cart.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.name} - S/ ${item.price.toFixed(2)}`;
        cartItems.appendChild(li);
    });
    document.getElementById('total').textContent = total.toFixed(2);
}

function checkout() {
    if (cart.length === 0) {
        alert('El carrito está vacío');
        return;
    }
    alert('Gracias por su compra. Total: S/ ' + total.toFixed(2));
    cart = [];
    total = 0;
    updateCart();
}
