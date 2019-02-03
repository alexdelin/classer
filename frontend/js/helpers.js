function updateProgressBar(type) {
    if (type === 'running') {
        $('#progressBar')[0].innerHTML = '<div class="progress-bar progress-bar-striped progress-bar-animated bg-info" role="progressbar" style="width: 100%" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100">Benchmarking...</div>'
    } else if (type === 'done') {
        $('#progressBar')[0].innerHTML = '<div class="progress-bar progress-bar-striped bg-success" role="progressbar" style="width: 100%" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100">Done</div>'
    } else if (type === 'error') {
        $('#progressBar')[0].innerHTML = '<div class="progress-bar progress-bar-striped bg-danger" role="progressbar" style="width: 100%" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100">Error</div>'
    };
};
