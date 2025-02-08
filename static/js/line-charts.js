document.addEventListener("DOMContentLoaded", () => {
  function createSeries(seriesArray) {
    return seriesArray.map((d) => ({
      type: "line",
      data: d,
    }));
  }

  function initChart(domId, seriesData, seriesNames) {
    const chartDom = document.getElementById(domId);
    if (!chartDom) return;

    const chart = echarts.init(chartDom, "dark");

    const option = {
      title: { text: domId, left: "center" },
      tooltip: { trigger: "axis" },
      legend: { show: true },
      xAxis: { type: "time" },
      yAxis: { type: "value", splitLine: {show: false} },
      grid: { left: "5%", right: "5%", bottom: "10%", containLabel: true },
      series: createSeries(seriesData),
    };

    chart.setOption(option);
    window.addEventListener("resize", () => chart.resize());
    return chart;
  }

  const data = JSON.parse(document.getElementById("reading-data").textContent);

  console.log(data);

  const temperature = data.map((d) => [new Date(d.timestamp), d.temperature]);
  const humidity = data.map((d) => [new Date(d.timestamp), d.humidity]);
  const luminance = data.map((d) => [new Date(d.timestamp), d.luminance]);
  const moisture_a = data.map((d) => [new Date(d.timestamp), d.moisture_a]);
  const moisture_b = data.map((d) => [new Date(d.timestamp), d.moisture_b]);
  const moisture_c = data.map((d) => [new Date(d.timestamp), d.moisture_c]);

  const charts = [
    { id: "Moisture", series: [moisture_a, moisture_b, moisture_c], names: ["Moisture A", "Moisture B", "Moisture C"] },
    { id: "Temperature", series: [temperature], names: ["Temperature"] },
    { id: "Humidity", series: [humidity], names: ["Humidity"] },
    { id: "Luminance", series: [luminance], names: ["Luminance"] },
  ];

  charts.forEach(({ id, series, names }) => initChart(id, series, names));
});
