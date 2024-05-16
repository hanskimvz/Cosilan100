var chart_bar = null;
var chart_line = null;

const lineOption = {
  chart: {
    height: 350,
    type: "line",
    zoom: {
      enabled: false
    },
    toolbar: {
      show: false
    },
    defaultLocale: 'zh-cn',
    locales: [
      {
        name: 'en',
        options: {
          months: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
          shortMonths: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          days: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
          shortDays: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
          toolbar: {
            download: 'Download SVG',
            selection: 'Selection',
            selectionZoom: 'Selection Zoom',
            zoomIn: 'Zoom In',
            zoomOut: 'Zoom Out',
            pan: 'Panning',
            reset: 'Reset Zoom',
          }
        }
      },
      {
        name: "ko",
        options: {
          months: ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"],
          shortMonths: ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"],
          days: ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일"],
          shortDays: ["일", "월", "화", "수", "목", "금", "토"],
          toolbar: {
            exportToSVG: "SVG 다운로드",
            exportToPNG: "PNG 다운로드",
            exportToCSV: "CSV 다운로드",
            menu: "메뉴",
            selection: "선택",
            selectionZoom: "선택영역 확대",
            zoomIn: "확대",
            zoomOut: "축소",
            pan: "패닝",
            reset: "원래대로"
          }
        }
      },
      {
        name: "zh-cn",
        options: {
          months: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
          shortMonths: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
          days: ["星期天", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"],
          shortDays: ["周日", "周一", "周二", "周三", "周四", "周五", "周六"],
          toolbar: {
            exportToSVG: "下载 SVG",
            exportToPNG: "下载 PNG",
            exportToCSV: "下载 CSV",
            menu: "菜单",
            selection: "选择",
            selectionZoom: "选择缩放",
            zoomIn: "放大",
            zoomOut: "缩小",
            pan: "平移",
            reset: "重置缩放"
          }
        }
      }
    ]
  },
  dataLabels: {
    enabled: true,
    textAnchor: 'middle',
    distributed: false,
    offsetX: 0,
    offsetY: 0,
    dropShadow: {
      enabled: false,
      top: 1,
      left: 1,
      blur: 1,
      color: '#000',
      opacity: 0.45
    }
  },
  // stroke: { width: [5, 7, 5], curve: "straight", dashArray: [0, 8, 5] },
  stroke: { curve: "smooth", width:5,},
  series: [],
  title: { text: "", },
  legend: { 
    show:true, 
    showForSingleSeries: true, 
    position:"top", 
    offsetX: 0, 
    floating: true,
  },
  markers: {
    size: 0,
    style: "hollow", // full, hollow, inverted
  },
  xaxis: {
    xaxis: {
      type: "datetime",
      position: 'bottom',
      labels:{
        show:true,
        showDuplicates: true,
        datetimeUTC: false,
        datetimeFormatter: {
          year: "yyyy",
          month: "yyyy-MM",
          day: "MM dd",
          hour: "HH:mm",
        },
      }		
    },    
    categories: [], //["01 Jan", "02 Jan", "03 Jan", "04 Jan", "05 Jan", "06 Jan", "07 Jan", "08 Jan", "09 Jan", "10 Jan", "11 Jan", "12 Jan"],
  },
  tooltip: {
    followCursor: false,
    fillSeriesColor: true,
    x: {
      show: true,
      format: 'yyyy/MM/dd HH:mm',
    },
    marker:{
      show:false
    }
    // y: [{
    //   title: {
    //     formatter: function(val) {
    //       return val + " (mins)"
    //     }
    //   }
    // }, {
    //   title: {
    //     formatter: function(val) {
    //       return val + " per session"
    //     }
    //   }
    // }, {
    //   title: {
    //     formatter: function(val) {
    //       return val;
    //     }
    //   }
    // }]
  },
  grid: {
    show: true,
    borderColor: '#C0C0C0',
    strokeDashArray: 0,
    position: 'back',
    xaxis: {
        lines: {
            show: false
        }
    },   
    yaxis: {
        lines: {
            show: true
        }
    },  
    row: {
        opacity: 0.2
    },  
    column: {
        opacity: 0.5
    },  
    padding: {
        top: 20,
        right: 20,
        bottom: 0,
        left: 20
    }, 
  }
};


const barOption = {
  chart: {
    height: 350,
    type: "bar",
    zoom: {
      enabled: false
    },
    toolbar: {
      show: false
    },
    defaultLocale: 'zh-cn',
    locales: [
      {
        name: 'en',
        options: {
          months: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
          shortMonths: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          days: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
          shortDays: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
          toolbar: {
            download: 'Download SVG',
            selection: 'Selection',
            selectionZoom: 'Selection Zoom',
            zoomIn: 'Zoom In',
            zoomOut: 'Zoom Out',
            pan: 'Panning',
            reset: 'Reset Zoom',
          }
        }
      },
      {
        name: "ko",
        options: {
          months: ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"],
          shortMonths: ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"],
          days: ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일"],
          shortDays: ["일", "월", "화", "수", "목", "금", "토"],
          toolbar: {
            exportToSVG: "SVG 다운로드",
            exportToPNG: "PNG 다운로드",
            exportToCSV: "CSV 다운로드",
            menu: "메뉴",
            selection: "선택",
            selectionZoom: "선택영역 확대",
            zoomIn: "확대",
            zoomOut: "축소",
            pan: "패닝",
            reset: "원래대로"
          }
        }
      },
      {
        name: "zh-cn",
        options: {
          months: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
          shortMonths: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
          days: ["星期天", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"],
          shortDays: ["周日", "周一", "周二", "周三", "周四", "周五", "周六"],
          toolbar: {
            exportToSVG: "下载 SVG",
            exportToPNG: "下载 PNG",
            exportToCSV: "下载 CSV",
            menu: "菜单",
            selection: "选择",
            selectionZoom: "选择缩放",
            zoomIn: "放大",
            zoomOut: "缩小",
            pan: "平移",
            reset: "重置缩放"
          }
        }
      }
    ]
  },
  dataLabels: {
    enabled: true,
    textAnchor: 'middle',
    distributed: false,
    offsetX: 0,
    offsetY: 0,
    dropShadow: {
      enabled: false,
      top: 1,
      left: 1,
      blur: 1,
      color: '#000',
      opacity: 0.45
    }
  },
  // stroke: { width: [5, 7, 5], curve: "straight", dashArray: [0, 8, 5] },
  stroke: { show:true, curve: "straight", width:2,colors: ['transparent']},
  series: [],
  title: { text: "", },
  legend: { 
    show:true, 
    showForSingleSeries: true, 
    position:"top", 
    offsetX: 0, 
    floating: true,
  },
  markers: {
    size: 0,
    style: "hollow", // full, hollow, inverted
  },
  xaxis: {
    xaxis: {
      type: "datetime",
      position: 'bottom',
      labels:{
        show:true,
        showDuplicates: true,
        datetimeUTC: false,
        datetimeFormatter: {
          year: "yyyy",
          month: "yyyy-MM",
          day: "MM dd",
          hour: "HH:mm",
        },
      }		
    },    
    categories: [], //["01 Jan", "02 Jan", "03 Jan", "04 Jan", "05 Jan", "06 Jan", "07 Jan", "08 Jan", "09 Jan", "10 Jan", "11 Jan", "12 Jan"],
  },
  tooltip: {
    followCursor: true,
    fillSeriesColor: true,
    x: {
      show: true,
      format: 'yyyy/MM/dd HH:mm',
    },
    marker:{
      show:false
    }
    // y: [{
    //   title: {
    //     formatter: function(val) {
    //       return val + " (mins)"
    //     }
    //   }
    // }, {
    //   title: {
    //     formatter: function(val) {
    //       return val + " per session"
    //     }
    //   }
    // }, {
    //   title: {
    //     formatter: function(val) {
    //       return val;
    //     }
    //   }
    // }]
  },
  grid: {
    show: true,
    borderColor: '#90A4AE',
    strokeDashArray: 0,
    position: 'back',
    xaxis: {
        lines: {
            show: false
        }
    },   
    yaxis: {
        lines: {
            show: false
        }
    },  
    row: {
        opacity: 0.5
    },  
    column: {
        opacity: 0.5
    },  
    padding: {
        top: 30,
        right: 20,
        bottom: 0,
        left: 20
    }, 
  }
};

const AheatmapOption = {
  chart: {
    height: 350,
    type: "heatmap",
  },
  legend: { show: false},
  dataLabels: {
    enabled: true,
    style: {
      fontSize: '12px',
      colors: ["#3047D8"]
    }	
  },
  colors: ["#330040"], 
  series: [],
  xaxis: { 
    type: "datetime",
    categories: [],
    tickPlacement: 'between',
    floating: false,
    labels: {
      show: false,
      rotate: -45,
      rotateAlways: false,
      hideOverlappingLabels: true,
      showDuplicates: false,
      trim: false,
      minHeight: undefined,
      maxHeight: 120,
      style: {
          colors: [],
          fontSize: '12px',
          fontFamily: 'Helvetica, Arial, sans-serif',
          fontWeight: 400,
          cssClass: 'apexcharts-xaxis-label',
      },
      offsetX: 0,
      offsetY: 0,
      format: undefined,
      formatter: undefined,
      datetimeUTC: true,
      datetimeFormatter: {
          year: 'yyyy',
          month: "MMM 'yy",
          day: 'dd MMM',
          hour: 'HH:mm',
      },
    },
  },
  yaxis: {
    show: true 
  },
  noData: { text: "Loading..." },
  plotOptions: {
    heatmap: {
      shadeIntensity: 0,
      radius: 0,
      useFillColorAsStroke: true,
      colorScale: {
      ranges: []
      }
    }
  },
  tooltip: {
    x: { format: "HH:mm" }
  }
}
export {lineOption, barOption, AheatmapOption };