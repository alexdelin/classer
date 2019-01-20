function makeHeatMapData(dataset) {

    var formattedSeries = []

    for (i = 0; i < dataset.length; i++) {
        for (j = 0; j < dataset[i].length; j++) {
            formattedSeries.push([i, j, dataset[i][j]])
        }
    }

    return formattedSeries
};


function makeStatsElement(precision, recall, fScores, name) {
    var element = '<h3>' + name + ' Precision</h3><ul>'

    _.each(_.keys(precision), function(key) {
        element = element + '<li><b>' + key + '</b> - ' + precision[key]
    });

    element = element + '</ul><h3>' + name + ' Recall</h3><ul>'

    _.each(_.keys(recall), function(key) {
        element = element + '<li><b>' + key + '</b> - ' + recall[key]
    });

    element = element + '</ul><h3>' + name + ' F-Scores</h3><ul>'

    _.each(_.keys(fScores), function(key) {
        element = element + '<li><b>' + key + '</b> - ' + fScores[key]
    });

    element = element + '</ul>'
    return element
};


function drawStats(parsedResults) {

    // Remove any previous stats
    $('#totalConfusionStats')[0].innerHTML = ''
    $('#maxConfusionStats')[0].innerHTML = ''
    $('#thresholdConfusionStats')[0].innerHTML = ''

    // Draw new Stats
    var totalPrecision = parsedResults['total_precision']
    var totalRecall = parsedResults['total_recall']
    var totalF = parsedResults['total_f']
    var totalElement = makeStatsElement(totalPrecision, totalRecall, totalF, 'Total')
    $('#totalConfusionStats').append(totalElement)

    var maxPrecision = parsedResults['max_precision']
    var maxRecall = parsedResults['max_recall']
    var maxF = parsedResults['max_f']
    var maxElement = makeStatsElement(maxPrecision, maxRecall, maxF, 'Max')
    $('#maxConfusionStats').append(maxElement)

    var thresholdPrecision = parsedResults['threshold_precision']
    var thresholdRecall = parsedResults['threshold_recall']
    var thresholdF = parsedResults['threshold_f']
    var thresholdElement = makeStatsElement(thresholdPrecision, thresholdRecall, thresholdF, 'Threshold')
    $('#thresholdConfusionStats').append(thresholdElement)
};


function drawBenchmarkResults(results) {

    // Preprocessing + Label Map Setup
    var parsedResults = JSON.parse(results)
    var labelMap = parsedResults['label_map']
    var inverseLabelMap = {}
    _.each(_.keys(labelMap), function (key) {
        inverseLabelMap[labelMap[key]] = key
    });

    var labelArray = []
    for (i = 0; i < _.keys(labelMap).length; i++) {
        labelArray.push(inverseLabelMap[i])
    }
    var thresholdLabelArray = labelArray
    thresholdLabelArray.push('No label')

    // Get and Format Data series
    var totalSeriesData = parsedResults['confusion']
    var formattedTotalSeriesData = makeHeatMapData(totalSeriesData)

    var maxSeriesData = parsedResults['max_confusion']
    var formattedMaxSeriesData = makeHeatMapData(maxSeriesData)

    var thresholdSeriesData = parsedResults['threshold_confusion']
    var formattedThresholdSeriesData = makeHeatMapData(thresholdSeriesData)

    drawStats(parsedResults)

    // Total Confusion Matrix
    Highcharts.chart('totalConfusionMatrix', {

        chart: {
            type: 'heatmap',
            marginTop: 40,
            marginBottom: 80,
            plotBorderWidth: 1},
        title: {
            text: 'Total Confusion Matrix'},
        xAxis: {
            categories: labelArray,
            title: {
                enabled: true,
                text: 'Ground Truth'}},
        yAxis: {
            categories: labelArray,
            title: {
                enabled: true,
                text: 'Predictions'}},
        colorAxis: {
            min: 0,
            minColor: '#FFFFFF',
            maxColor: Highcharts.getOptions().colors[0]},
        legend: {
            align: 'right',
            layout: 'vertical',
            margin: 0,
            verticalAlign: 'top',
            y: 25,
            symbolHeight: 280},
        tooltip: {
            formatter: function () {
                return '<b>' + this.series.xAxis.categories[this.point.x] +
                    '</b> labeled <b>' + this.series.yAxis.categories[this.point.y] +
                    '<br>' +this.point.value + '</b> times';
            }
        },
        series: [{
            name: 'Confusion',
            borderWidth: 1,
            data: formattedTotalSeriesData,
            dataLabels: {
                enabled: true,
                color: '#000000'}
        }]
    });

    // Max Confusion Matrix
    Highcharts.chart('maxConfusionMatrix', {

        chart: {
            type: 'heatmap',
            marginTop: 40,
            marginBottom: 80,
            plotBorderWidth: 1},
        title: {
            text: 'Max Confusion Matrix'},
        xAxis: {
            categories: labelArray,
            title: {
                enabled: true,
                text: 'Ground Truth'}},
        yAxis: {
            categories: labelArray,
            title: {
                enabled: true,
                text: 'Predictions'}},
        colorAxis: {
            min: 0,
            minColor: '#FFFFFF',
            maxColor: Highcharts.getOptions().colors[0]},
        legend: {
            align: 'right',
            layout: 'vertical',
            margin: 0,
            verticalAlign: 'top',
            y: 25,
            symbolHeight: 280},
        tooltip: {
            formatter: function () {
                return '<b>' + this.series.xAxis.categories[this.point.x] +
                    '</b> labeled <b>' + this.series.yAxis.categories[this.point.y] +
                    '<br>' +this.point.value + '</b> times';
            }
        },
        series: [{
            name: 'Confusion',
            borderWidth: 1,
            data: formattedMaxSeriesData,
            dataLabels: {
                enabled: true,
                color: '#000000'}
        }]
    });

    // Threshold Confusion Matrix
    Highcharts.chart('thresholdConfusionMatrix', {

        chart: {
            type: 'heatmap',
            marginTop: 40,
            marginBottom: 80,
            plotBorderWidth: 1},
        title: {
            text: 'Threshold Confusion Matrix'},
        xAxis: {
            categories: labelArray,
            title: {
                enabled: true,
                text: 'Ground Truth'}},
        yAxis: {
            categories: thresholdLabelArray,
            title: {
                enabled: true,
                text: 'Predictions'}},
        colorAxis: {
            min: 0,
            minColor: '#FFFFFF',
            maxColor: Highcharts.getOptions().colors[0]},
        legend: {
            align: 'right',
            layout: 'vertical',
            margin: 0,
            verticalAlign: 'top',
            y: 25,
            symbolHeight: 280},
        tooltip: {
            formatter: function () {
                return '<b>' + this.series.xAxis.categories[this.point.x] +
                    '</b> labeled <b>' + this.series.yAxis.categories[this.point.y] +
                    '<br>' +this.point.value + '</b> times';
            }
        },
        series: [{
            name: 'Confusion',
            borderWidth: 1,
            data: formattedThresholdSeriesData,
            dataLabels: {
                enabled: true,
                color: '#000000'}
        }]
    });
}
