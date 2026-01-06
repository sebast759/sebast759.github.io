document.addEventListener("DOMContentLoaded", function () {
    // Define the stock names here
    const stock1Name = "mix";
    const stock2Name = "BTC";

    // Function to calculate performance percentage given two values
    function calculatePerformance(currentValue, previousValue) {
        return ((currentValue - previousValue) / previousValue) * 100;
    }

    // Function to format the number with a + sign on positive performance
    function formatPerformance(performance) {
        return performance >= 0 ? `+${performance.toFixed(2)}%` : `${performance.toFixed(2)}%`;
    }

    // Function to parse CSV data and calculate performance metrics
    function parseCSVAndDisplay(data) {
        const lines = data.trim().split("\n");
        const headers = lines[0].split(",");
        const stock1Index = headers.indexOf(stock1Name)-1;
        const stock2Index = headers.indexOf(stock2Name)-1;
        const lastRow = lines[lines.length - 1].split(",");

        const stock1Value = parseFloat(lastRow[stock1Index + 1]);
        const stock2Value = parseFloat(lastRow[stock2Index + 1]);
        const prevDayStock1Value = parseFloat(lines[lines.length - 2].split(",")[stock1Index + 1]);
        const prevWeekStock1Value = parseFloat(lines[lines.length - 8].split(",")[stock1Index + 1]);
        const prevMonthStock1Value = parseFloat(lines[lines.length - 31].split(",")[stock1Index + 1]);

        const prevDayStock2Value = parseFloat(lines[lines.length - 2].split(",")[stock2Index + 1]);
        const prevWeekStock2Value = parseFloat(lines[lines.length - 8].split(",")[stock2Index + 1]);
        const prevMonthStock2Value = parseFloat(lines[lines.length - 31].split(",")[stock2Index + 1]);
        // Find the value corresponding to the last date of 2022
        let yearStartStock1Value;
        let yearStartStock2Value;
        for (let i = lines.length - 1; i >= 0; i--) {
            const row = lines[i].split(",");
            const dateParts = row[0].split("/");
            const year = parseInt(dateParts[0]);
            if (year === 2022) {
                yearStartStock1Value = parseFloat(row[stock1Index + 1]);
                yearStartStock2Value = parseFloat(row[stock2Index + 1]);
                break;
            }
        }

        const oneDayPerformanceStock1 = calculatePerformance(stock1Value, prevDayStock1Value);
        const oneWeekPerformanceStock1 = calculatePerformance(stock1Value, prevWeekStock1Value);
        const oneMonthPerformanceStock1 = calculatePerformance(stock1Value, prevMonthStock1Value);
        const yearToDatePerformanceStock1 = calculatePerformance(stock1Value, yearStartStock1Value);
        
        const oneDayPerformanceStock2 = calculatePerformance(stock2Value, prevDayStock2Value);
        const oneWeekPerformanceStock2 = calculatePerformance(stock2Value, prevWeekStock2Value);
        const oneMonthPerformanceStock2 = calculatePerformance(stock2Value, prevMonthStock2Value);
        const yearToDatePerformanceStock2 = calculatePerformance(stock2Value, yearStartStock2Value);

        const table = document.getElementById("performance-table");
        const rowStock1 = document.createElement("tr");
        rowStock1.innerHTML = `<td>${stock1Name}</td>
                             <td>${formatPerformance(oneDayPerformanceStock1)}</td>
                             <td>${formatPerformance(oneWeekPerformanceStock1)}</td>
                             <td>${formatPerformance(oneMonthPerformanceStock1)}</td>
                             <td>${formatPerformance(yearToDatePerformanceStock1)}</td>`;
        table.appendChild(rowStock1);

        const rowStock2 = document.createElement("tr");
        rowStock2.innerHTML = `<td>${stock2Name}</td>
                             <td>${formatPerformance(oneDayPerformanceStock2)}</td>
                             <td>${formatPerformance(oneWeekPerformanceStock2)}</td>
                             <td>${formatPerformance(oneMonthPerformanceStock2)}</td>
                             <td>${formatPerformance(yearToDatePerformanceStock2)}</td>`;
        table.appendChild(rowStock2);
    }

    // Fetch the CSV file and process the data
    fetch("data.csv")
        .then((response) => response.text())
        .then((data) => {
            parseCSVAndDisplay(data);
        })
        .catch((error) => {
            console.error("Error fetching data:", error);
        });
});
