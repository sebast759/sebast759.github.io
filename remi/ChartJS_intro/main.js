const ctx = document.getElementById('myChart').getContext('2d');

const labels = ['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020'];
const data1 = {
  labels: labels,
  series: [[211, 326, 165, 352, 420, 370, 500, 375, 415]],
};
var chart = new Chartist.Line('.ct-chart', data1, {});

const data = {
  labels:labels,
  datasets: [
    {
      data: [211, 326, 165, 352, 420, 370, 500, 375, 415],
      label: "Minecraft"
    },
  ],
};


const config = {
  type: 'line',
  data: data,
  options: {},
};
 const myChart = new Chart(ctx, config);
