async function loadData() {

    const response = await fetch("history.json");

    const data = await response.json();

    if (!data.length) return;

    const latest = data[data.length - 1];
    
    const latestTime = new Date(latest.timestamp);
    
    const cutoff24h = new Date(
        latestTime.getTime() - 24 * 60 * 60 * 1000
    );
    
    let record24hAgo = null;
    
    for (let i = data.length - 1; i >= 0; i--) {
    
        const t = new Date(data[i].timestamp);
    
        if (t <= cutoff24h) {
            record24hAgo = data[i];
            break;
        }
    }
    
    let sold24h = 0;
    
    if (record24hAgo) {
        sold24h =
            latest.sold -
            record24hAgo.sold;
    }

    if (data.length >= 25) {

        const yesterday = data[data.length - 25];

        document.getElementById(
            "sold24h"
        ).textContent = sold24h;

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
