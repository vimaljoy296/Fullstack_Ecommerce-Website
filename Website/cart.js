// Fetch cart items from the API and display them
async function fetchCartItems() {
    try {
        const cartId = 193;  // You can dynamically set this if necessary
        const response = await fetch(`http://127.0.0.1:5000/cart/${cartId}`);
        if (!response.ok) {
            throw new Error('Failed to fetch cart items');
        }
        const data = await response.json();
        displayCartItems(data.items, data.total_amount); // Display items and total amount
    } catch (error) {
        console.error(error);
        alert("Something went wrong while fetching the cart items.");
    }
}

// Function to display cart items
function displayCartItems(items, totalAmount) {
    const cartListContainer = document.querySelector('.cart-list');
    const totalAmountContainer = document.getElementById('total-amount');

    cartListContainer.innerHTML = '';  // Clear existing content

    if (!items || items.length === 0) {
        cartListContainer.innerHTML = '<p>Your cart is empty.</p>';
        return;
    }

    // Loop through cart items and display them
    items.forEach(item => {
        const cartItem = document.createElement('div');
        cartItem.classList.add('cart-item');
        cartItem.innerHTML = `
            <h3>${item.product_name}</h3>
            <p>Description: ${item.description}</p>
            <p>Price: $${item.price}</p>
            <p>Quantity: ${item.quantity}</p>
            <p>Total: $${item.total_price}</p>
        `;
        cartListContainer.appendChild(cartItem);
    });

    // Display total amount
    totalAmountContainer.innerHTML = `Total Amount: $${totalAmount}`;
}

// Function to display a success message when the order is placed
function placeOrder() {
    // Display the alert message
    alert('Order has been placed successfully!');
    
    // Optionally, clear the cart items and refresh the cart display
    clearCart();
    fetchCartItems();
}

// Function to clear the cart (for display purposes, if necessary)
function clearCart() {
    const cartListContainer = document.querySelector('.cart-list');
    const totalAmountContainer = document.getElementById('total-amount');

    // Clear cart list and total amount
    cartListContainer.innerHTML = '<p>Your cart is empty.</p>';
    totalAmountContainer.innerHTML = '';  // Clear total amount
}

// Attach event listener to the Place Order button
document.getElementById('place-order-btn').addEventListener('click', placeOrder);

// Fetch cart items when the page loads (optional, based on your requirements)
window.onload = fetchCartItems;

