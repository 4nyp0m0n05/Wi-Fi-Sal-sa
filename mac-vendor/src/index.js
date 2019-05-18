import axios from "axios";
import Chart from "chart.js";
import _ from "lodash";
import ChartDataLabels from 'chartjs-plugin-datalabels';

const API_HOST = "https://api.macvendors.com/v1/lookup/";
const API_TOKEN =
  "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJtYWN2ZW5kb3JzIiwiZXhwIjoxODYwOTYwODc3LCJpYXQiOjE1NDY0NjQ4NzcsImlzcyI6Im1hY3ZlbmRvcnMiLCJqdGkiOiI1YWY5MTIxYy0zYmM5LTQ0OWYtOTAyNC03Y2NjMzM2NzM5ZjAiLCJuYmYiOjE1NDY0NjQ4NzYsInN1YiI6IjEwNTciLCJ0eXAiOiJhY2Nlc3MifQ.hezi7dUNkRLFJQQz_4LQuHe709UUjiHeeeLvy4ISHoTYuA_vZy0vOYaZUABQ-1GBJLndiCs5eUIgohH7z0ZdvQ";

const request = axios.create({
  baseURL: API_HOST,
  timeout: 10000,
  headers: {
    Authorization: `Bearer ${API_TOKEN}`
  }
});

const ctx = document.getElementById("myChart").getContext("2d");

const myChart = new Chart(ctx, {
  type: "line",
  data: {
    labels: [],
    datasets: []
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      yAxes: [{
        ticks: {
          beginAtZero: true,
          stepSize: 1
        }
      }]
    }
  }
});

function getRandomColor() {
  let letters = "0123456789ABCDEF".split("");
  let color = "#";
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}


function createDataSet(label, data, color) {
  return {
    label: label,
    data: data,
    borderWidth: 1,
    backgroundColor: color,
    borderColor: color,
    fill: false,
    lineTension: 0,
    pointRadius: 6,
  }
}

function onResultSetChange() {
  const vendors = _.countBy(results.map(result => result.name));
  let chartDataSets = myChart.data.datasets;

  myChart.data.labels.push("Request " + (+myChart.data.labels.length + 1));
  Object.keys(vendors).forEach(vendor => {
    const color = getRandomColor();
    let found = _.find(chartDataSets, {
      label: vendor
    });
    if (found) {
      found.data.push(vendors[vendor]);
    } else {
      chartDataSets.push(createDataSet(vendor, [vendors[vendor]], color));
    }
  });
  myChart.update();
  updateTable();
}

function updateTable() {
  let myTable = document.getElementById("myTable");
  while (myTable.rows.length > 1) {
    myTable.deleteRow(1);
  }
  results.forEach(result => {
    if (result.sId !== undefined) {
      let row = myTable.insertRow();
      let cell1 = row.insertCell(0);
      let cell2 = row.insertCell(1);
      cell1.innerHTML = result.sId;
      cell2.innerHTML = result.name;
    }
  });
}


fetch("aps.txt")
  .then(response => response.text())
  .then(text => {
    let lines = text.split("\n");
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      setTimeout(_.partial(makeRequest, line), i * 1000);
    }
  })
  .catch(err => console.log(err));

let results = [];

function makeRequest(line) {
  let splitted = line.split(" ");
  let mac = splitted[0];
  let sid = splitted[1];
  let auth = splitted[2];
  request
    .get(mac)
    .then(response => {
      let name = response.data.data.organization_name;
      let result = {
        name: name,
        mac: mac,
        sId: auth === "OPN" ? sid : undefined
      };
      results.push(result);
      onResultSetChange();
    })
    .catch(error => {
      console.log(error);
    });
}