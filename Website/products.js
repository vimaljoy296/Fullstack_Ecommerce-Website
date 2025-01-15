// Define the products array globally so it can be accessed by other functions
let products = [];

// Fetch products from the API and display them
async function fetchProducts() {
    try {
        const response = await fetch('http://127.0.0.1:5000/products');  // Replace with your API
        if (!response.ok) {
            throw new Error('Failed to fetch products');
        }
        const data = await response.json();  // Parse the JSON data
        products = data.products;  // Store products globally
        displayProducts(products);  // Display the products on the page
    } catch (error) {
        console.error(error);
        alert("Something went wrong while fetching the products.");
    }
}

// Function to display products on the page
function displayProducts(products) {
    const productListContainer = document.querySelector('.product-list');
    productListContainer.innerHTML = '';  // Clear existing content

    // Loop through products and create product items
    products.forEach(product => {
        const productItem = document.createElement('div');
        productItem.classList.add('product-item');

        // Create the product HTML structure
        productItem.innerHTML = `
            <img src="${product.image || 'default-image.jpg'}" alt="${product.product_name}">
            <h3>${product.product_name}</h3>
            <p>${product.description}</p>
            <p>Price: $${product.price}</p>
            <button onclick="addToCart(${product.product_id})">Add to Cart</button>
        `;

        // Append the product item to the product list container
        productListContainer.appendChild(productItem);
    });
}

// Function to add product to the cart
async function addToCart(productId) {
    try {
        const customerId = 193; // Replace with dynamic ID if needed

        // Prepare the data to send to the API
        const data = {
            product_id: productId,
            quantity: 1 // Default quantity is 1
        };

        // Send the POST request to add the product to the cart
        const response = await fetch(`http://127.0.0.1:5000/cart/${customerId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        // Check the response status
        if (!response.ok) {
            const errorText = await response.text();
            console.error(`Error: ${response.status} - ${errorText}`);
            throw new Error(`Failed to add product to the cart: ${errorText}`);
        }

        // Notify the user and refresh cart items (optional)
        alert("Product added to cart successfully!");
        fetchCartItems(); // Refresh cart (defined in `cart.js`)
    } catch (error) {
        console.error(error);
        alert("Something went wrong while adding the product to the cart.");
    }
}

// Fetch products when the page loads
window.onload = fetchProducts;
