document.getElementById('api-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '';
    document.getElementById('loader').style.display = 'inline-block';

    const p = document.getElementById('p').value;
    const d = document.getElementById('d').value;
    const n_max = document.getElementById('n_max').value;
    const tol_hi = document.getElementById('tol_hi').value;
    const sag_compliant = 1;

    fetch('https://jix6oc21j7.execute-api.us-east-1.amazonaws.com/api/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            p: p,
            d: d,
            n_max: n_max,
            tol_hi: tol_hi,
            sag_compliant: sag_compliant
        })
    })
    .then(response => response.json())
    .then(data => {
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

            item.patrones.forEach(pattern => {
                let [filled, total] = pattern.split('/').map(Number);
                if(isNaN(total)) {
                    total = 1;
                }

                const dots = [];
                let count = filled;
                while(count > 0) {
                    if(count >= total) {
                        dots.push(total);
                        count -= total;
                    } else {
                        dots.push(count);
                        count = 0;
                    }
                }

                let dotString = '';
                for(let i=0; i<20; i++) {
                    if(dots[i%dots.length] !== 1) {
                        dotString += `<span class="dot filled">${dots[i%dots.length]}</span>`;
                    } else {
                        dotString += '<span class="dot filled"></span>';
                    }
                }

                resultDiv.innerHTML += `
                    <div class="pattern-container">
                        <p>${pattern}:</p>
                        <div class="pattern">${dotString}<span class="dots">...</span></div>
                    </div>
                `;
            });
        });
    });
});
