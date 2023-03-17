const initialInput = document.querySelector("#initial");
const monthlyInput = document.querySelector("#monthly");
const targetInput = document.querySelector("#target");

const initialOutput = document.querySelector("#initialInvestment");
const monthlyOutput = document.querySelector("#monthlyInvestment");
const targetOutput = document.querySelector("#targetInvestment");

const finalOutput = document.querySelector("#final");
const earnedOutput = document.querySelector("#earned");
const costsOutput = document.querySelector("#costs");
const saveOutput = document.querySelector("#save");

const finalExpectedOutput = document.querySelector("#finalExpected");
const finalSaveOutput = document.querySelector("#finalSave");
const finalLessOutput = document.querySelector("#finalLess");
const finalMoreOutput = document.querySelector("#finalMore");

const horizonButton1 = document.querySelector("#horizon1");
const horizonButton2 = document.querySelector("#horizon2");
const horizonButton3 = document.querySelector("#horizon3");
const horizonButton4 = document.querySelector("#horizon4");

const horizonOutput = document.querySelector("#horizon");

let yearsHorizon = 30;
let initialValue = 30000;
let monthlyValue = 500;
let targetValue = 50000;

const formatter = new Intl.NumberFormat("en", {
  style: "currency",
  currency: "EUR",
  maximumFractionDigits: 0, // (causes 2500.99 to be printed as $2,501)
});


function horizonChange(value) {
  yearsHorizon = value;
  horizonOutput.textContent = `${value} years`;

  switch (value) {
    case 5:
      horizonButton1.className = "horizonButton h-active";
      horizonButton2.className = "horizonButton";
      horizonButton3.className = "horizonButton";
      horizonButton4.className = "horizonButton";
      break;
    case 15:
      horizonButton1.className = "horizonButton";
      horizonButton2.className = "horizonButton h-active";
      horizonButton3.className = "horizonButton";
      horizonButton4.className = "horizonButton";
      break;
    case 20:
      horizonButton1.className = "horizonButton";
      horizonButton2.className = "horizonButton";
      horizonButton3.className = "horizonButton h-active";
      horizonButton4.className = "horizonButton";
      break;
    case 30:
      horizonButton1.className = "horizonButton";
      horizonButton2.className = "horizonButton";
      horizonButton3.className = "horizonButton";
      horizonButton4.className = "horizonButton h-active";
      break;
  }

  handleOnChange();
}

function handleOnChange() {
  const monthlyIncrease = monthlyValue;

  let final = initialValue;
  let target = targetValue;

  let save = final;
  let less = final;
  let more = final;
  let costs = 0;
  let earned = 0;
  let maximum = final;

  var label_sa = ["Year0"];
  var s1 = [final];
  var s2 = [less];
  var s3 = [more];
  var s4 = [save];
  var s5 = [target];

  for (let i = 0; i < yearsHorizon; i++) {
    const costsPercent = final > 100000 ? 0.0069 : 0.0099;

    if (monthlyIncrease !== 0) {
      final = final + monthlyIncrease * 12;
      more = more + monthlyIncrease * 12;
      less = less + monthlyIncrease * 12;
      save = save + monthlyIncrease * 12;
    }

    const earnedValue = final * 0.08;
    const costsValue = final * costsPercent;

    maximum = maximum + earnedValue;

    earned = earned + earnedValue - costsValue;
    costs = costs + costsValue;
    final = final + earnedValue - costsValue;

    less = less + less * 0.04 - less * costsPercent;
    more = more + more * 0.10 - more * costsPercent;
    save = save + save * 0.00;

    if ((i + 1) % (yearsHorizon == 5 ? 1 : 5) == 0) {
      label_sa.push("Year" + (i + 1));
      s1.push(final);
      s2.push(less);
      s3.push(more);
      s4.push(save);
      s5.push(target);
    }
  }

  finalOutput.textContent = formatter.format(final);
  costsOutput.textContent = formatter.format(costs);
  earnedOutput.textContent = formatter.format(earned);
  saveOutput.textContent = formatter.format(save);

  finalExpectedOutput.textContent = formatter.format(final);
  finalLessOutput.textContent = formatter.format(less);
  finalSaveOutput.textContent = formatter.format(save);
  finalMoreOutput.textContent = formatter.format(more);
  var data = {
    labels: label_sa,
    series: [{ "name": "Invested", "data": s1 }, { "name": " ", "data": s2 }, { "name": " ", "data": s3 },
    { "name": "Saved", "data": s4 }, { "name": " ", "data": s5 },]
  };

  function ctPointLabels2(options) {
    return function ctPointLabels(chart) {
      var defaultOptions = {
        labelClass: 'ct-label',
        labelOffset: {
          x: 0,
          y: -10
        },
        textAnchor: 'middle'
      };

      options = Chartist.extend({}, defaultOptions, options);

      if (chart instanceof Chartist.Line) {
        chart.on('draw', function (data) {
          if ((data.type === 'point') && (data.index == data.series.data.length - 1)
            && ((data.seriesIndex == 3) || data.seriesIndex == 0)) {
            data.group.elem('text', {
              x: data.x + options.labelOffset.x + 10,
              y: data.y + options.labelOffset.y,
              style: 'text-anchor: right;fill:' + (data.seriesIndex == 0 ? '#882aa0' : (data.seriesIndex == 3 ? '#000000' : '#D0D3D4'))
            }, 'ct-label-seb').text((data.seriesIndex == 0 ? 'Invested' : (data.seriesIndex == 3 ? 'Saved' : '')));  // 07.11.17 added ".y"


            data.group.elem('text', {
              x: data.x + options.labelOffset.x + 10,
              y: data.y + options.labelOffset.y + 15,
              style: 'text-anchor: right;fill:' + (data.seriesIndex == 0 ? '#882aa0' : (data.seriesIndex == 3 ? '#000000' : 'rgba(0,0,0,.2)'))
            }, 'ct-label-seb').text('£' + parseInt(data.value.y / 1000) + 'm');  // 07.11.17 added ".y"

          }
        });
      }
    }
  }

  var options = {
    low: 0,
    showArea: false,
    showPoint: true,
    fullWidth: false,
    responsive: true,
    axisY: {
      // Lets offset the chart a bit from the labels
      offset: 60,
      // The label interpolation function enables you to modify the values
      // used for the labels on each axis. Here we are converting the
      // values into million pound.
      labelInterpolationFnc: function (value) {
        return '£' + value / (final > 100000 ? 1000 : 1) + (final > 100000 ? 'm' : '');
      }
    },
    axisX: {
      // We can disable the grid for this axis
      showGrid: true,
      // and also don't show the label
      showLabel: true
    },
    plugins: [
      Chartist.plugins.legend(),
      ctPointLabels2({
        textAnchor: 'middle',
        labelInterpolationFnc: function (value) {
          console.log("i was called");
          return '£' + parseInt(value / (final > 100000 ? 1000 : 1)) + (final > 100000 ? 'm' : '');
        }
      }),
      Chartist.plugins.ctAxisTitle({
        axisX: {
          axisTitle: '',
          axisClass: 'ct-axis-title',
          offset: {
            x: 0,
            y: 500000
          },
          textAnchor: 'middle'
        },
        axisY: {
          axisTitle: 'Performance',
          axisClass: 'ct-axis-title',
          offset: {
            x: 0,
            y: 0
          },
          textAnchor: 'middle',
          flipTitle: false
        },

      })
    ]
  };
  var chart = new Chartist.Line('.ct-chart', data, options);

  // const labels = ['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020'];
  // const data1 = {
  //   labels: labels,
  //   series: [[211, 326, 165, 352, 420, 370, 500, 375, 415]],
  // };
  // var chart = new Chartist.Line('.myChart', data1, {});

  // This is the bit we are actually interested in. By registering a callback for `draw` events, we can actually intercept the drawing process of each element on the chart.

  // ctx = document.getElementById('.ct-chart').getContext('2d');
  var max = 100;
  // chart.on('draw', function(context) {
  //   // First we want to make sure that only do something when the draw event is for bars. Draw events do get fired for labels and grids too.
  //   if(context.type === 'line') {
  //     // With the Chartist.Svg API we can easily set an attribute on our bar that just got drawn
  //     // console.log(Math.floor(Chartist.getMultiValue(context.value) / max * 100) );

  //     context.element.attr({
  //       // Now we set the style attribute on our bar to override the default color of the bar. By using a HSL colour we can easily set the hue of the colour dynamically while keeping the same saturation and lightness. From the context we can also get the current value of the bar. We use that value to calculate a hue between 0 and 100 degree. This will make our bars appear green when close to the maximum and red when close to zero.
  //       style: 'stroke: hsl(' + Math.floor(Chartist.getMultiValue(ccontext.values[1].y) / max * 100) + ', 50%, 50%);'
  //     });
  //   }
  // });
}

noUiSlider.create(initialInput, {
  start: [30000],
  connect: "lower",
  range: {
    min: [1000, 1000],
    "33%": [10000, 1000],
    "66%": [100000, 10000],
    max: [1000000],
  },
});

initialInput.noUiSlider.on("update", function (values, handle) {
  initialOutput.textContent = formatter.format(values[handle]);
  initialValue = parseInt(values[handle]);

  handleOnChange();
});

noUiSlider.create(monthlyInput, {
  start: [500],
  connect: "lower",
  range: {
    min: [0, 50],
    "50%": [1000, 100],
    max: [5000],
  },
});

monthlyInput.noUiSlider.on("update", function (values, handle) {
  monthlyOutput.textContent = formatter.format(values[handle]);
  monthlyValue = parseInt(values[handle]);

  handleOnChange();
});
noUiSlider.create(targetInput, {
  start: [30000],
  connect: "lower",
  range: {
    min: [1000, 1000],
    "33%": [10000, 1000],
    "66%": [100000, 100000],
    max: [2000000],
  },
});
targetInput.noUiSlider.on("update", function (values, handle) {
  targetOutput.textContent = formatter.format(values[handle]);
  targetValue = parseInt(values[handle]);

  handleOnChange();
});
