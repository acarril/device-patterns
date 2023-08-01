document.getElementById('api-form').addEventListener('submit', function(event) {
    event.preventDefault(); // prevent the form from being submitted normally

    // Clear previous results and show the loader
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '';
    document.getElementById('loader').style.display = 'inline-block';

    const p = document.getElementById('p').value;
    const d_min = document.getElementById('d_min').value;
    const n_max = document.getElementById('n_max').value;
    const tolerance_factor = document.getElementById('tolerance_factor').value;
    const sag_compliant = 1; // Always send as checked

    fetch('https://jix6oc21j7.execute-api.us-east-1.amazonaws.com/api/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            p: p,
            d_min: d_min,
            n_max: n_max,
            tolerance_factor: tolerance_factor,
            sag_compliant: sag_compliant
        })
    })
    .then(response => response.json())
    .then(data => {
        // Hide the loader
        document.getElementById('loader').style.display = 'none';

        resultDiv.innerHTML = '<h2>Resultados</h2>';

        ['min_densidad', 'min_hileras'].forEach(key => {
            const item = data[key];
            let title = '';
            if (key === 'min_densidad') {
                title = 'Min. dosis';
            } else if (key === 'min_hileras') {
                title = 'Min. hileras';
            }
            resultDiv.innerHTML += `
                <h3>${title}:</h3>
                <p>Dosis: ${item.densidad}</p>
            `;
            let offset = 0;
            item.patrones.forEach(pattern => {
                let [filled, total] = pattern.split('/').map(Number);
                if(isNaN(total)) {
                    total = 1;
                }
                let dotString = '';
                for (let i = 0; i < 20; i++) {
                    const shouldFill = (i + offset) % total < filled;
                    if (shouldFill) {
                        dotString += '<span class="dot filled"></span>';
                    } else {
                        dotString += '<span class="dot"></span>';
                    }
                }
                resultDiv.innerHTML += `
                    <div class="pattern-container">
                        <p>${pattern}:</p>
                        <div class="pattern">${dotString}<span class="dots">...</span></div>
                    </div>
                `;
                offset += 1;
            });
        });
    });
});