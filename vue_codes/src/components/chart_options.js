const lineOption = {
  chart: {
    height: 350,
    type: "line",
    zoom: {
      enabled: false
    },
    toolbar: {
      show: false
    }
  },
  dataLabels: {
    enabled: true
  },
  // stroke: { width: [5, 7, 5], curve: "straight", dashArray: [0, 8, 5] },
  stroke: { curve: "smooth", width:5,},
  series: [
    // seriese format:
    // { name: "Session Duration", data: [45, 52, 38, 24, 33, 26, 21, 20, 6, 8, 15, 10]},
  ],
  title: { text: "", },
  legend: { show:true, showForSingleSeries: true, position:"top", offsetX: 0, floating: true,},
  markers: {
    size: 0,
    style: "hollow", // full, hollow, inverted
  },
  xaxis: {
    categories: [], //["01 Jan", "02 Jan", "03 Jan", "04 Jan", "05 Jan", "06 Jan", "07 Jan", "08 Jan", "09 Jan", "10 Jan", "11 Jan", "12 Jan"],
  },
  tooltip: {
    y: [{
      title: {
        formatter: function(val) {
          return val + " (mins)"
        }
      }
    }, {
      title: {
        formatter: function(val) {
          return val + " per session"
        }
      }
    }, {
      title: {
        formatter: function(val) {
          return val;
        }
      }
    }]
  },
  grid: {
    borderColor: "#f1f1f1",
  }
};

export { lineOption };