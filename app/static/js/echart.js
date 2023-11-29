function show(){
    // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('range'));

        window.addEventListener('resize', function() {
            myChart.resize();
        });
        // 指定图表的配置项和数据
        var option = {
  title: {
    text: '',
    subtext: '',
    left: 'center'
  },
  tooltip: {
    trigger: 'item'
  },
  legend: {
    orient: 'vertical',
    left: 'left'
  },
  series: [
    {
      name: '隐私场景',
      type: 'pie',
      radius: '50%',
      data: [
        { value: 1048, name: '电信业务类' },
        { value: 735, name: '地图导航类' },
        { value: 580, name: '网上购物类' },
        { value: 484, name: '远程诊疗类' },
        { value: 300, name: '酒店服务类' }
      ],
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
};
    myChart.resize();
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
}
function showl1(){
                var Chart = echarts.init(document.getElementById('first'));
            Chart.resize();
            window.addEventListener('resize', function() {
            Chart.resize();
        });
            var option = {
  xAxis: {
    type: 'category',
    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      data: [120, 200, 150, 80, 70, 110, 130],
      type: 'bar'
    }
  ]
};
            Chart.setOption(option);

}