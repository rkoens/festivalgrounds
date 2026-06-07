async function loadData() {

    const response = await fetch("history.json");

    const data = await response.json();

    if (!data.length) return;

    const latest = data[data.length - 1];

    document.getElementById("currentSold").textContent =
        latest.sold;

    if (data.length >= 2) {

        const previous = data[data.length - 2];

        document.getElementById("hourlySales").textContent =
            latest.sold - previous.sold;
    }

    if (data.length >= 25) {

        const yesterday = data[data.length - 25];

        document.getElementById("dailySales").textContent =
            latest.sold - yesterday.sold;
    }

    const labels = data.map(
        x => new Date(x.timestamp).toLocaleString()
    );

    const sold = data.map(
        x => x.sold
    );

    new Chart(
        document.getElementById("salesChart"),
        {
            type: "line",

            data: {
                labels,
                datasets: [
                    {
                        label: "Total Sold",
                        data: sold
                    }
                ]
            }
        }
    );
}

loadData();
