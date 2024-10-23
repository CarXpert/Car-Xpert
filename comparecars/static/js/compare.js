const carData = {
    'Honda BR-V': {
        brand: 'Honda',
        model: 'BR-V',
        year: 2023,
        fuel_type: 'Petrol',
        color: 'Gold',
        price: '250.000.000',
        image: 'https://example.com/honda-brv.jpg'
    },
    'Toyota Rush': {
        brand: 'Toyota',
        model: 'Rush',
        year: 2023,
        fuel_type: 'Petrol',
        color: 'Silver',
        price: '282.700.000',
        image: 'https://example.com/toyota-rush.jpg'
    },
    'BMW X5': {
        brand: 'BMW',
        model: 'X5',
        year: 2023,
        fuel_type: 'Diesel',
        color: 'Black',
        price: '1.200.000.000',
        image: 'https://example.com/bmw-x5.jpg'
    }
};

document.getElementById('compare-btn').addEventListener('click', function () {
    const car1 = document.getElementById('car1').value;
    const car2 = document.getElementById('car2').value;

    // Update Car 1 Card
    document.getElementById('car1-card').innerHTML = `
        <img src="${carData[car1].image}" alt="${carData[car1].model}">
        <h2>${carData[car1].brand} ${carData[car1].model}</h2>
        <p>${carData[car1].price} IDR</p>
    `;

    // Update Car 2 Card
    document.getElementById('car2-card').innerHTML = `
        <img src="${carData[car2].image}" alt="${carData[car2].model}">
        <h2>${carData[car2].brand} ${carData[car2].model}</h2>
        <p>${carData[car2].price} IDR</p>
    `;

    // Update Comparison Table
    document.getElementById('car1-name').textContent = `${carData[car1].brand} ${carData[car1].model}`;
    document.getElementById('car2-name').textContent = `${carData[car2].brand} ${carData[car2].model}`;

    document.getElementById('car1-brand').textContent = carData[car1].brand;
    document.getElementById('car2-brand').textContent = carData[car2].brand;

    document.getElementById('car1-model').textContent = carData[car1].model;
    document.getElementById('car2-model').textContent = carData[car2].model;

    document.getElementById('car1-year').textContent = carData[car1].year;
    document.getElementById('car2-year').textContent = carData[car2].year;

    document.getElementById('car1-fuel').textContent = carData[car1].fuel_type;
    document.getElementById('car2-fuel').textContent = carData[car2].fuel_type;

    document.getElementById('car1-color').textContent = carData[car1].color;
    document.getElementById('car2-color').textContent = carData[car2].color;
});
