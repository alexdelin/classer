$("#addSubmit").click(function() {

    console.log( "Handler for add submit called." );

    var addLabel = $('#addLabel')[0].value;
    var addText = $('#addText')[0].value
    var addTraining = $('#addTraining')[0].value

    $.ajax({
        url: '/training/add_single',
        data: {
            "label": addLabel,
            "text": addText,
            "training_name": addTraining
        },
        success: function(response) {
            console.log(response)
            var newElement = '<div class="status-message">' + response + '</div>';
            $('#status-window').append(newElement)
        },
    });
});


$("#dedupSubmit").click(function() {

    console.log( "Handler for dedup submit called." );

    var dedupTraining = $('#dedupTraining')[0].value

    $.ajax({
        url: '/training/deduplicate',
        data: {
            "training_name": dedupTraining
        },
        success: function(response) {
            console.log(response)
            var newElement = '<div class="status-message">' + response + '</div>';
            $('#status-window').append(newElement)
        },
    });
});


$("#refreshSubmit").click(function() {

    console.log( "Handler for refresh submit called." );

    $('.training-example').remove()
    var trainingName = $('#addTraining')[0].value

    $.ajax({
        url: '/training/get',
        data: {
            "training_name": trainingName
        },
        success: function(response) {
            console.log(response)
            var newElement = '<div class="status-message">' + response + '</div>';
            $('#status-window').append(newElement)

            var loadedResponse = JSON.parse(response)
            _.each(loadedResponse, function(trainingExample) {
                var exampleElement = '<tr class="training-example"><td>' + trainingExample['label'] + '</td><td>' + trainingExample['text'] + '</td></tr>'
                $('#training-example-list').append(exampleElement)
            });
        },
    });
});


$("#extendSubmit").click(function() {

    console.log( "Handler for extend submit called." );
    // Remove all previous recommendations
    $('.recommendation-row').remove()

    var extendCorpus = $('#extendCorpus')[0].value
    var extendImplementation = $('#extendImplementation')[0].value
    var trainingName = $('#addTraining')[0].value

    $.ajax({
        url: '/training/recommend',
        data: {
            "implementation_name": extendImplementation,
            "corpus_name": extendCorpus
        },
        success: function(response) {
            console.log(response)
            var newElement = '<div class="status-message">' + response + '</div>';
            $('#status-window').append(newElement)

            // Add recommendation to table
            loadedResponse = JSON.parse(response)
            _.each(loadedResponse, function(recElement) {
                var rowElement = '<tr class="recommendation-row"><td class="recText">' + recElement['text'] + '</td><td class="recLabel">' + recElement['label'] + '</td><td><div class="btn btn-default addExample">Add</div></td></tr>'
                $('#training-recommendations').append(rowElement)
            });

            $(".addExample").on('click', function(ev) {
                console.log( "Handler for add example called." );
                debugger;
                var newText = $(ev.target.parentElement.parentElement).find('.recText')[0].innerHTML
                var newLabel = $(ev.target.parentElement.parentElement).find('.recLabel')[0].innerHTML

                $.ajax({
                    url: '/training/add_single',
                    data: {
                        "label": newLabel,
                        "text": newText,
                        "training_name": trainingName
                    },
                    success: function(response) {
                        console.log(response)
                        var newElement = '<div class="status-message">' + response + '</div>';
                        $('#status-window').append(newElement)
                    }
                });
            });
        },
    });
});
