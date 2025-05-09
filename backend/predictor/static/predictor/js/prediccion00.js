document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("btnPredecir");
    const resultado = document.getElementById("resultado");
    const graficoCanvas = document.getElementById("graficoPrediccion");

    btn.addEventListener("click", () => {
        resultado.innerHTML = '<div class="loader"></div>';
        fetch("/predictor/predecir/")
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    resultado.innerHTML = `<p style="color:red;">${data.error}</p>`;
                } else {
                    const html = `
                        <p><strong>📍 Precio actual:</strong> $${data.precio_actual}</p>
                        <p><strong>📈 Predicción para mañana:</strong> $${data.prediccion}</p>
                        <p><strong>🔍 Diferencia:</strong> $${data.diferencia}</p>
                        <p><strong>🔁 Tendencia esperada:</strong> ${data.tendencia}</p>
                        <canvas id="graficoPrediccion" width="400" height="200"></canvas>
                    `;
                    resultado.innerHTML = html;

                    // Mostrar animación de entrada
                    resultado.classList.remove("mostrar");
                    setTimeout(() => resultado.classList.add("mostrar"), 10);

                    // Mostrar gráfico
                    const ctx = document.getElementById("graficoPrediccion").getContext("2d");
                    new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: ['Precio actual', 'Predicción'],
                            datasets: [{
                                label: 'Precio BTC',
                                data: [data.precio_actual, data.prediccion],
                                backgroundColor: ['#58a6ff', '#2ea043']
                            }]
                        },
                        options: {
                            responsive: true,
                            plugins: {
                                legend: { display: false }
                            },
                            scales: {
                                y: {
                                    beginAtZero: false
                                }
                            }
                        }
                    });
                }
            })
            .catch(err => {
                resultado.innerHTML = `<p style="color:red;">Error de conexión: ${err}</p>`;
            });
    });
});
