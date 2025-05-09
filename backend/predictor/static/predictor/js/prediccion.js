document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("btnPredecir");
    const resultado = document.getElementById("resultado");
    const loader = document.getElementById("loader");
    const canvas = document.getElementById("grafico");

    let chartInstance = null;  // Para destruir el gráfico anterior

    btn.addEventListener("click", () => {
        const modelo = document.getElementById("modelo").value;

        resultado.innerHTML = "";
        loader.style.display = "block";
        canvas.style.display = "none";

        fetch(`/predictor/predecir/?modelo=${modelo}`, {
            method: "GET",
        })
        .then(res => res.json())
        .then(data => {
            loader.style.display = "none";

            if (data.error) {
                resultado.innerHTML = `<p style="color:red;">${data.error}</p>`;
                return;
            }

            resultado.innerHTML = `
                <p><strong>📍 Precio actual:</strong> $${data.precio_actual}</p>
                <p><strong>📈 Predicción para mañana:</strong> $${data.prediccion}</p>
                <p><strong>🔍 Diferencia:</strong> $${data.diferencia}</p>
                <p><strong>🔁 Tendencia esperada:</strong> ${data.tendencia}</p>
            `;

            renderGrafico(data.labels, data.precio_real, data.precio_predicho);
        })
        .catch(err => {
            loader.style.display = "none";
            resultado.innerHTML = `<p style="color:red;">❌ Error de conexión.</p>`;
        });
    });

    function renderGrafico(labels, reales, predichos) {
        if (!labels || !reales || !predichos) {
            document.getElementById("grafico").style.display = "none";
            return;
        }

        const ctx = document.getElementById("grafico").getContext("2d");

        if (chartInstance) {
            chartInstance.destroy();
        }

        chartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: "📊 Precio Real",
                        data: reales,
                        borderColor: "#4CAF50",
                        backgroundColor: "rgba(76, 175, 80, 0.2)",
                        fill: true,
                        tension: 0.4
                    },
                    {
                        label: "🔮 Predicción",
                        data: predichos,
                        borderColor: "#FF9800",
                        backgroundColor: "rgba(255, 152, 0, 0.2)",
                        fill: true,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                animation: {
                    duration: 1000,
                    easing: 'easeOutQuart'
                },
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return `${context.dataset.label}: $${context.parsed.y.toFixed(2)}`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        title: {
                            display: true,
                            text: 'USD'
                        }
                    }
                }
            }
        });

        document.getElementById("grafico").style.display = "block";
    }
});
