// Fetch top-rated products from the API and populate the homepage
document.addEventListener('DOMContentLoaded', () => {
    const topRatedProductsContainer = document.getElementById('top-rated-products');
    
    fetch('http://127.0.0.1:5000/homepage')
        .then(response => response.json())
        .then(data => {
            const topRatedProducts = data.top_rated_products;
            
            topRatedProducts.forEach(product => {
                const productCard = document.createElement('div');
                productCard.classList.add('product-card');
                
                productCard.innerHTML = `
                    <img src="https://via.placeholder.com/250x200" alt="${product.product_name}">
                    <h3>${product.product_name}</h3>
                    <p>${product.description}</p>
                    <p class="price">$${product.price.toFixed(2)}</p>
                `;
                
                topRatedProductsContainer.appendChild(productCard);
            });
        })
        .catch(error => console.log('Error fetching top-rated products:', error));
});
