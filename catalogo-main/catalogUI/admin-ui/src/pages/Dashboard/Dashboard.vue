<template>
  <q-page class="q-pa-sm">
    <q-card class="bg-transparent no-shadow no-border">
      <q-card-section class="q-pa-none">
        <div class="row q-col-gutter-sm">
          <div class="col-md-3 col-sm-12 col-xs-12">
            <q-item style="background-color: #5064b5" class="q-pa-none q-ml-xs">
              <q-item-section
                side
                style="background-color: #3e51b5"
                class="q-pa-lg q-mr-none text-white"
              >
                <q-icon name="person" color="white" size="24px"></q-icon>
              </q-item-section>
              <q-item-section class="q-pa-md q-ml-none text-white">
                <q-item-label class="text-white text-h6 text-weight-bolder"
                  >200</q-item-label
                >
                <q-item-label>My Account</q-item-label>
              </q-item-section>
            </q-item>
          </div>
          <div class="col-md-3 col-sm-12 col-xs-12">
            <q-item style="background-color: #f37169" class="q-pa-none q-ml-xs">
              <q-item-section
                side
                style="background-color: #f34636"
                class="q-pa-lg q-mr-none text-white"
              >
                <q-icon name="fab fa-twitter" size="24px"></q-icon>
              </q-item-section>
              <q-item-section class="q-pa-md q-ml-none text-white">
                <q-item-label class="text-white text-h6 text-weight-bolder"
                  >500</q-item-label
                >
                <q-item-label>Followers</q-item-label>
              </q-item-section>
            </q-item>
          </div>
          <div class="col-md-3 col-sm-12 col-xs-12">
            <q-item style="background-color: #ea6a7f" class="q-pa-none q-ml-xs">
              <q-item-section
                side
                style="background-color: #ea4b64"
                class="q-pa-lg q-mr-none text-white"
              >
                <q-icon name="fab fa-google" size="24px"></q-icon>
              </q-item-section>
              <q-item-section class="q-pa-md q-ml-none text-white">
                <q-item-label class="text-white text-h6 text-weight-bolder"
                  >50</q-item-label
                >
                <q-item-label>Connections</q-item-label>
              </q-item-section>
            </q-item>
          </div>
          <div class="col-md-3 col-sm-12 col-xs-12">
            <q-item
              style="background-color: #a270b1"
              class="q-pa-none q-ml-xs q-mr-xs"
            >
              <q-item-section
                side
                style="background-color: #9f52b1"
                class="q-pa-lg q-mr-none text-white"
              >
                <q-icon name="bar_chart" size="24px"></q-icon>
              </q-item-section>
              <q-item-section class="q-pa-md q-ml-none text-white">
                <q-item-label class="text-white text-h6 text-weight-bolder"
                  >1020</q-item-label
                >
                <q-item-label> Website Visits</q-item-label>
              </q-item-section>
            </q-item>
          </div>
        </div>
      </q-card-section>
    </q-card>
    <div class="row q-col-gutter-sm q-py-sm">
      <div class="col-lg-4 col-md-4 col-sm-12 col-xs-12">
        <q-card class="q-ma-xs" style="background-color: #38b1c5">
          <q-card-section class="text-h6 text-white">
            Today's View
          </q-card-section>
          <q-card-section class="q-pa-none"> </q-card-section>
        </q-card>
      </div>
      <div class="col-lg-4 col-md-4 col-sm-12 col-xs-12">
        <q-card class="q-ma-xs" style="background-color: #ea4b64">
          <q-card-section class="text-h6 text-white">
            Daily Sales
          </q-card-section>
          <q-card-section class="q-pa-none"> </q-card-section>
        </q-card>
      </div>
      <div class="col-lg-4 col-md-4 col-sm-12 col-xs-12">
        <q-card class="q-ma-xs" style="background-color: #1e88e5">
          <q-card-section class="text-h6 text-white">
            Today's User Visit
          </q-card-section>
          <q-card-section class="q-pa-none"> </q-card-section>
        </q-card>
      </div>
    </div>

    <div class="row q-col-gutter-sm q-py-sm"></div>
  </q-page>
</template>

<script>
export default {
  name: "PageIndex",
  components: {},
  data() {
    return {
      filter: "",
      mode: "list",
      columns: [
        {
          name: "id",
          align: "left",
          label: "User ID",
          field: "id",
          sortable: true,
        },
        {
          name: "user_name",
          align: "left",
          label: "User Name",
          field: "user_name",
          sortable: true,
        },
        {
          name: "desc",
          required: true,
          label: "Page",
          align: "left",
          field: (row) => row.name,
          sortable: true,
        },
        {
          name: "date",
          align: "right",
          label: "Date",
          field: "date",
          sortable: true,
        },
      ],
      data: [
        {
          id: "U0001",
          name: "/login",
          date: "12-10-2019",
          user_name: "Pratik Patel",
        },
        {
          id: "U0002",
          name: "/Dashboard",
          date: "11-02-2019",
          user_name: "Razvan Stoenescu",
        },
        {
          id: "U0003",
          name: "/Map",
          date: "03-25-2019",
          user_name: "Pratik Patel",
        },
        {
          id: "U0004",
          name: "/Mail",
          date: "03-18-2019",
          user_name: "Jeff Galbraith",
        },
        {
          id: "U0005",
          name: "/Profile",
          date: "04-09-2019",
          user_name: "Pratik Patel",
        },
      ],
      pagination: {
        rowsPerPage: 10,
      },
      timeline_list: [
        {
          title: "Pratik Likes your product ",
          side: "left",
          desc:
            "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore\n" +
            "                  et dolore magna aliqua.",
          color: "red",
          icon: "thumb_up",
        },
        {
          title: "Product Update",
          side: "left",
          desc:
            "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore\n" +
            "                  et dolore magna aliqua.",
          color: "orange",
          icon: "done_all",
        },
        {
          title: "Jeff Likes your product ",
          side: "left",
          desc:
            "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore\n" +
            "                  et dolore magna aliqua.",
          color: "blue",
          icon: "thumb_up",
        },
      ],
      tab: "contact",
      layout: "dense",
      side: "right",
      series: [
        {
          data: [44, 55, 41, 64, 22, 43, 21],
        },
        {
          data: [53, 32, 33, 52, 13, 44, 32],
        },
      ],
      chartOptions: {
        chart: {
          type: "bar",
          height: 430,
        },
        plotOptions: {
          bar: {
            horizontal: true,
            dataLabels: {
              position: "top",
            },
          },
        },
        dataLabels: {
          enabled: true,
          offsetX: -6,
          style: {
            fontSize: "12px",
            colors: ["#fff"],
          },
        },
        stroke: {
          show: true,
          width: 1,
          colors: ["#fff"],
        },
        xaxis: {
          categories: [2001, 2002, 2003, 2004, 2005, 2006, 2007],
        },
      },
      BarChart: {
        tooltip: { show: true },
        title: {
          show: true,
          textStyle: { color: "rgba(0, 0, 0 , .87)", fontFamily: "sans-serif" },
        },
        grid: { containLabel: true, bottom: "10%", top: "5%" },
        xAxis: {
          show: false,
          type: "category",
          axisLine: {
            lineStyle: { color: "rgba(0, 0, 0 , .54)", type: "dashed" },
          },
          axisTick: {
            show: true,
            alignWithLabel: true,
            lineStyle: {
              show: true,
              color: "rgba(0, 0, 0 , .54)",
              type: "dashed",
            },
          },
          axisLabel: { show: false },
        },
        yAxis: {
          show: false,
          type: "value",
          axisLine: {
            lineStyle: { color: "rgba(0, 0, 0 , .54)", type: "dashed" },
          },
          axisLabel: { show: false },
          splitLine: { lineStyle: { type: "dashed" } },
          axisTick: {
            show: true,
            lineStyle: {
              show: true,
              color: "rgba(0, 0, 0 , .54)",
              type: "dashed",
            },
          },
        },
        series: [
          {
            type: "bar",
            barGap: "-100%",
            itemStyle: { normal: { color: "rgba(0,0,0,0.1)" } },
            barWidth: "50%",
          },
          {
            barWidth: "50%",
            type: "bar",
            itemStyle: { normal: { color: "#ffffff" } },
          },
        ],
        dataset: {
          source: [
            { label: "0D", max: 500, sales: 220 },
            {
              label: "1D",
              max: 500,
              sales: 182,
            },
            { label: "2D", max: 500, sales: 191 },
            {
              label: "3D",
              max: 500,
              sales: 234,
            },
            { label: "4D", max: 500, sales: 290 },
            {
              label: "5D",
              max: 500,
              sales: 330,
            },
            { label: "6D", max: 500, sales: 310 },
            {
              label: "7D",
              max: 500,
              sales: 123,
            },
            { label: "8D", max: 500, sales: 442 },
            {
              label: "9D",
              max: 500,
              sales: 321,
            },
            { label: "10D", max: 500, sales: 90 },
            {
              label: "11D",
              max: 500,
              sales: 149,
            },
            { label: "12D", max: 500, sales: 210 },
            {
              label: "13D",
              max: 500,
              sales: 122,
            },
            { label: "14D", max: 500, sales: 133 },
            {
              label: "15D",
              max: 500,
              sales: 334,
            },
            { label: "16D", max: 500, sales: 198 },
            {
              label: "17D",
              max: 500,
              sales: 123,
            },
            { label: "18D", max: 500, sales: 125 },
            { label: "19D", max: 500, sales: 220 },
          ],
        },
      },
      LineChart: {
        tooltip: { show: true },
        title: {
          show: true,
          textStyle: { color: "rgba(0, 0, 0 , .87)", fontFamily: "sans-serif" },
        },
        grid: { containLabel: true, left: "0", bottom: "0", right: "0" },
        xAxis: {
          show: false,
          type: "category",
          axisLine: {
            lineStyle: { color: "rgba(0, 0, 0 , .54)", type: "dashed" },
          },
          axisTick: {
            show: true,
            alignWithLabel: true,
            lineStyle: {
              show: true,
              color: "rgba(0, 0, 0 , .54)",
              type: "dashed",
            },
          },
          axisLabel: { show: false },
          boundaryGap: false,
        },
        yAxis: {
          show: false,
          type: "value",
          axisLine: {
            lineStyle: { color: "rgba(0, 0, 0 , .54)", type: "dashed" },
          },
          axisLabel: { show: false },
          splitLine: { lineStyle: { type: "dashed" } },
          axisTick: {
            show: true,
            lineStyle: {
              show: true,
              color: "rgba(0, 0, 0 , .54)",
              type: "dashed",
            },
          },
        },
        series: [{ type: "line", areaStyle: {}, smooth: true }],
        dataset: {
          source: [
            { month: "Jan", "Unique Visit": 296, "Page View": 548 },
            {
              month: "Feb",
              "Unique Visit": 1181,
              "Page View": 714,
            },
            { month: "Mar", "Unique Visit": 235, "Page View": 961 },
            {
              month: "Apr",
              "Unique Visit": 294,
              "Page View": 580,
            },
            { month: "May", "Unique Visit": 765, "Page View": 730 },
            {
              month: "Jun",
              "Unique Visit": 412,
              "Page View": 1249,
            },
            { month: "Jul", "Unique Visit": 1125, "Page View": 267 },
            {
              month: "Aug",
              "Unique Visit": 800,
              "Page View": 251,
            },
            { month: "Sep", "Unique Visit": 948, "Page View": 1043 },
            {
              month: "Oct",
              "Unique Visit": 1046,
              "Page View": 1118,
            },
            { month: "Nov", "Unique Visit": 363, "Page View": 573 },
            {
              month: "Dec",
              "Unique Visit": 909,
              "Page View": 283,
            },
          ],
        },
        color: ["#2196f3"],
      },
      LineChart2: {
        tooltip: { show: true },
        title: {
          show: true,
          textStyle: { color: "rgba(0, 0, 0 , .87)", fontFamily: "sans-serif" },
        },
        grid: { containLabel: true, left: "0", bottom: "0", right: "0" },
        xAxis: {
          show: false,
          type: "category",
          axisLine: {
            lineStyle: { color: "rgba(0, 0, 0 , .54)", type: "dashed" },
          },
          axisTick: {
            show: true,
            alignWithLabel: true,
            lineStyle: {
              show: true,
              color: "rgba(0, 0, 0 , .54)",
              type: "dashed",
            },
          },
          axisLabel: { show: false },
          boundaryGap: false,
        },
        yAxis: {
          show: false,
          type: "value",
          axisLine: {
            lineStyle: { color: "rgba(0, 0, 0 , .54)", type: "dashed" },
          },
          axisLabel: { show: false },
          splitLine: { lineStyle: { type: "dashed" } },
          axisTick: {
            show: true,
            lineStyle: {
              show: true,
              color: "rgba(0, 0, 0 , .54)",
              type: "dashed",
            },
          },
        },
        series: [{ type: "line", areaStyle: {}, smooth: false }],
        dataset: {
          source: [
            { month: "Jan", "Unique Visit": 296, "Page View": 548 },
            {
              month: "Feb",
              "Unique Visit": 1181,
              "Page View": 714,
            },
            { month: "Mar", "Unique Visit": 235, "Page View": 961 },
            {
              month: "Apr",
              "Unique Visit": 294,
              "Page View": 580,
            },
            { month: "May", "Unique Visit": 765, "Page View": 730 },
            {
              month: "Jun",
              "Unique Visit": 412,
              "Page View": 1249,
            },
            { month: "Jul", "Unique Visit": 1125, "Page View": 267 },
            {
              month: "Aug",
              "Unique Visit": 800,
              "Page View": 251,
            },
            { month: "Sep", "Unique Visit": 948, "Page View": 1043 },
            {
              month: "Oct",
              "Unique Visit": 1046,
              "Page View": 1118,
            },
            { month: "Nov", "Unique Visit": 363, "Page View": 573 },
            {
              month: "Dec",
              "Unique Visit": 909,
              "Page View": 283,
            },
          ],
        },
        color: ["#45c2c5"],
      },
      series2: [44, 55, 41, 17, 15],
      donutchartOptions: {
        chart: {
          width: 380,
          type: "donut",
        },
        dataLabels: {
          enabled: false,
        },
        fill: {
          type: "gradient",
        },
        legend: {
          formatter: function (val, opts) {
            return val + " - " + opts.w.globals.series[opts.seriesIndex];
          },
        },
        responsive: [
          {
            breakpoint: 480,
            options: {
              chart: {
                width: 200,
              },
              legend: {
                position: "bottom",
              },
            },
          },
        ],
      },
      messages: [
        {
          id: 5,
          name: "Pratik Patel",
          msg:
            " -- I'll be in your neighborhood doing errands this\n" +
            "            weekend. Do you want to grab brunch?",
          avatar: "https://avatars2.githubusercontent.com/u/34883558?s=400&v=4",
          time: "10:42 PM",
        },
        {
          id: 6,
          name: "Winfield Stapforth",
          msg:
            " -- I'll be in your neighborhood doing errands this\n" +
            "            weekend. Do you want to grab brunch?",
          avatar: "https://cdn.quasar.dev/img/avatar6.jpg",
          time: "11:17 AM",
        },
        {
          id: 1,
          name: "Boy",
          msg:
            " -- I'll be in your neighborhood doing errands this\n" +
            "            weekend. Do you want to grab brunch?",
          avatar: "https://cdn.quasar.dev/img/boy-avatar.png",
          time: "5:17 AM",
        },
        {
          id: 2,
          name: "Jeff Galbraith",
          msg:
            " -- I'll be in your neighborhood doing errands this\n" +
            "            weekend. Do you want to grab brunch?",
          avatar: "https://cdn.quasar.dev/team/jeff_galbraith.jpg",
          time: "5:17 AM",
        },
        {
          id: 3,
          name: "Razvan Stoenescu",
          msg:
            " -- I'll be in your neighborhood doing errands this\n" +
            "            weekend. Do you want to grab brunch?",
          avatar: "https://cdn.quasar.dev/team/razvan_stoenescu.jpeg",
          time: "5:17 AM",
        },
      ],
      contacts: [
        {
          name: "Pratik Patel",
          position: "Developer",
          avatar: "https://avatars2.githubusercontent.com/u/34883558?s=400&v=4",
        },
        {
          name: "Razvan Stoenescu",
          position: "Developer",
          avatar: "https://cdn.quasar.dev/team/razvan_stoenescu.jpeg",
        },
        {
          name: "Jeff Galbraith",
          position: "Developer",
          avatar: "https://cdn.quasar.dev/team/jeff_galbraith.jpg",
        },
        {
          name: "Brunhilde Panswick",
          position: "Administrator",
          avatar: "https://cdn.quasar.dev/img/avatar2.jpg",
        },
        {
          name: "Winfield Stapforth",
          position: "Administrator",
          avatar: "https://cdn.quasar.dev/img/avatar6.jpg",
        },
      ],
    };
  },
  methods: {
    exportTable() {
      // naive encoding to csv format
      const content = [this.columns.map((col) => wrapCsvValue(col.label))]
        .concat(
          this.data.map((row) =>
            this.columns
              .map((col) =>
                wrapCsvValue(
                  typeof col.field === "function"
                    ? col.field(row)
                    : row[col.field === void 0 ? col.name : col.field],
                  col.format
                )
              )
              .join(",")
          )
        )
        .join("\r\n");

      const status = exportFile("table-export.csv", content, "text/csv");

      if (status !== true) {
        this.$q.notify({
          message: "Browser denied file download...",
          color: "negative",
          icon: "warning",
        });
      }
    },
  },
};
</script>
